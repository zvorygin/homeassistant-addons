import sys
import logging
import os
import json
import argparse
from io import BytesIO
import random
from typing import List, Optional, Union

sys.path.append('../')

from samsungtvws import SamsungTVWS
from sources.bing_wallpapers import BingWallpapers
from sources.google_art import GoogleArt
from sources.media_folder import MediaFolder
from utils.utils import resize_and_crop_image

# Add command line argument parsing
parser = argparse.ArgumentParser(description='Upload images to Samsung TV.')
parser.add_argument('--upload-all', action='store_true', help='Upload all images at once')
parser.add_argument('--debug', action='store_true', help='Enable debug mode to check if TV is reachable')
parser.add_argument('--tvip', help='IP address of the Samsung the Frame')
parser.add_argument('--googleart', action='store_true', help='Download and upload image from Google Arts & Culture')
parser.add_argument('--download-high-res', action='store_true', help='Download high resolution image using dezoomify-rs')
parser.add_argument('--bing-wallpapers', action='store_true', help='Download and upload image from Bing Wallpapers')
parser.add_argument('--media-folder', action='store_true', help='Use images from the local media folder')
parser.add_argument('--debugimage', action='store_true', help='Save downloaded and resized images for inspection')

args = parser.parse_args()

# Set the path to the folder containing the images
folder_path = 'frame'

# Set the path to the file that will store the list of uploaded filenames
upload_list_path = 'uploaded_files.json'

# Load the list of uploaded filenames from the file
if os.path.isfile(upload_list_path):
    with open(upload_list_path, 'r') as f:
        uploaded_files = json.load(f)
else:
    uploaded_files = []

# Increase debug level
logging.basicConfig(level=logging.INFO)

tvip = args.tvip
# Set your TVs local IP address. Highly recommend using a static IP address for your TV.
tv = SamsungTVWS(tvip)

# Check if TV is reachable in debug mode
if args.debug:
    try:
        logging.info('Checking if the TV can be reached.')
        info = tv.rest_device_info()
        logging.info('If you do not see an error, your TV could be reached.')
        sys.exit()
    except Exception as e:
        logging.error('Could not reach the TV: ' + str(e))
        sys.exit(1)

def save_debug_image(image_data: BytesIO, filename: str) -> None:
    if args.debugimage:
        with open(filename, 'wb') as f:
            f.write(image_data.getvalue())
        logging.info(f'Debug image saved as {filename}')

# Checks if the TV supports art mode
art_mode: bool = tv.art().supported()

if art_mode != True:
    logging.warning('Your TV does not support art mode.')
    sys.exit(1)

# Retrieve information about the currently selected art
current_art: Optional[dict] = tv.art().get_current()

sources: List[Union[BingWallpapers, GoogleArt, MediaFolder]] = []
if args.bing_wallpapers:
    sources.append(BingWallpapers())
if args.googleart:
    sources.append(GoogleArt(args.download_high_res))
if args.media_folder:
    sources.append(MediaFolder(folder_path, uploaded_files, args.upload_all))

if not sources:
    logging.error('No image source specified. Please use --googleart, --bing-wallpapers, or --media-folder')
    sys.exit(1)

selected_source = random.choice(sources)
logging.info(f'Selected source: {selected_source.__class__.__name__}')

image_data: Optional[BytesIO]; file_type: Optional[str]; image_info: Optional[str]; remote_filename: Optional[str] = selected_source.get_image()
if image_data is None:
    sys.exit(1)

save_debug_image(image_data, f'debug_{selected_source.__class__.__name__}_original_{image_info}.jpg')

logging.info('Resizing and cropping the image...')
resized_image_data = resize_and_crop_image(image_data)

save_debug_image(resized_image_data, f'debug_{selected_source.__class__.__name__}_resized_{image_info}.jpg')

image_data = resized_image_data

if remote_filename is None:
    try:
        logging.info(f'Uploading image')
        remote_filename = tv.art().upload(image_data.getvalue(), file_type=file_type, matte="none")
        tv.art().select_image(remote_filename, show=True)
        logging.info(f'Image uploaded and selected')
        # Add the filename to the list of uploaded filenames
        uploaded_files.append({'file': image_info, 'remote_filename': remote_filename})
        # Save the list of uploaded filenames to the file
        with open(upload_list_path, 'w') as f:
            json.dump(uploaded_files, f)
    except Exception as e:
        logging.error(f'There was an error uploading the image: ' + str(e))
        sys.exit()
else:
    if not args.upload_all:
        # Select the image using the remote file name only if not in 'upload-all' mode
        logging.info('Setting existing image, skipping upload')
        tv.art().select_image(remote_filename, show=True)
