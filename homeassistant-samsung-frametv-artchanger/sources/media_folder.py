import os
import logging
import random
from io import BytesIO

def get_media_folder_images(folder_path):
    """Get a list of JPG/PNG files in the folder, and search recursively if you want to use subdirectories"""
    return [os.path.join(root, f) for root, dirs, files in os.walk(folder_path) for f in files if f.endswith('.jpg') or f.endswith('.png')]

def process_media_folder_images(folder_path, uploaded_files, upload_all=False):
    files = get_media_folder_images(folder_path)

    if upload_all:
        logging.info('Bulk uploading all photos. This may take a while...')
        # Remove the filenames of images that have already been uploaded
        files = list(set(files) - set([f['file'] for f in uploaded_files]))
        files_to_upload = files
    else:
        if len(files) == 0:
            logging.info('No new images to upload.')
            return None, None, None
        else:
            logging.info('Choosing random image.')
            files_to_upload = [random.choice(files)]

    for file in files_to_upload:
        # Read the contents of the file
        with open(file, 'rb') as f:
            data = BytesIO(f.read())
        
        file_type = 'JPEG' if file.endswith('.jpg') else 'PNG'
        return data, file_type, file

    return None, None, None  # If no files were processed

def get_remote_filename(file, uploaded_files):
    for uploaded_file in uploaded_files:
        if uploaded_file['file'] == file:
            return uploaded_file['remote_filename']
    return None