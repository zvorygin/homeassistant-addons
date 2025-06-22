import os
import logging
import random
import requests
from io import BytesIO
from typing import List, Tuple, Optional, Dict
try:
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    logging.error("Google Photos support requires: pip install google-api-python-client google-auth-oauthlib")
    build = None

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
TOKEN_FILE = 'credentials/token.json'

def authenticate():
    """Authenticate with Google Photos API"""
    if build is None:
        return None
    
    # Get credentials from environment variables
    client_id = os.environ.get('GOOGLE_PHOTOS_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_PHOTOS_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        logging.error("Google Photos credentials not provided in configuration")
        logging.error("Please set google_photos_client_id and google_photos_client_secret in addon configuration")
        return None
        
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create client config from environment variables
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }
            
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Ensure credentials directory exists
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

def get_albums(service):
    """Get list of albums from Google Photos"""
    try:
        results = service.albums().list(pageSize=50).execute()
        albums = results.get('albums', [])
        return albums
    except Exception as e:
        logging.error(f"Error fetching albums: {str(e)}")
        return []

def get_album_photos(service, album_id):
    """Get photos from a specific album"""
    try:
        request_body = {
            'albumId': album_id,
            'pageSize': 100
        }
        results = service.mediaItems().search(body=request_body).execute()
        items = results.get('mediaItems', [])
        return items
    except Exception as e:
        logging.error(f"Error fetching photos from album: {str(e)}")
        return []

def get_image_url(args):
    """Get a random image URL from Google Photos album"""
    if build is None:
        logging.error("Google Photos API libraries not available")
        return None
    
    service = authenticate()
    if not service:
        return None
    
    album_name = getattr(args, 'google_photos_album', None)
    if not album_name:
        logging.error("No Google Photos album specified. Use --google-photos-album parameter")
        return None
    
    albums = get_albums(service)
    if not albums:
        logging.error("No albums found in Google Photos")
        return None
    
    target_album = None
    for album in albums:
        if album.get('title', '').lower() == album_name.lower():
            target_album = album
            break
    
    if not target_album:
        logging.error(f"Album '{album_name}' not found in Google Photos")
        logging.info("Available albums:")
        for album in albums[:10]:
            logging.info(f"  - {album.get('title', 'Untitled')}")
        return None
    
    photos = get_album_photos(service, target_album['id'])
    if not photos:
        logging.error(f"No photos found in album '{album_name}'")
        return None
    
    photo_items = [item for item in photos if item.get('mimeType', '').startswith('image/')]
    if not photo_items:
        logging.error(f"No image files found in album '{album_name}'")
        return None
    
    selected_photo = random.choice(photo_items)
    base_url = selected_photo.get('baseUrl')
    if not base_url:
        logging.error("Selected photo has no base URL")
        return None
    
    return f"{base_url}=w3840-h2160-c"

def get_image(args, image_url) -> Tuple[Optional[BytesIO], Optional[str]]:
    """Download image from Google Photos"""
    try:
        logging.info(f'Downloading image from Google Photos: {image_url[:50]}...')
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        return image_data, 'JPEG'
    except requests.RequestException as e:
        logging.error(f"Failed to download image from Google Photos: {str(e)}")
        return None, None