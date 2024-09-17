import os
import logging
import random
from io import BytesIO

class MediaFolder:
    def __init__(self, folder_path, uploaded_files, upload_all=False):
        self.folder_path = folder_path
        self.uploaded_files = uploaded_files
        self.upload_all = upload_all

    def get_media_folder_images(self):
        """Get a list of JPG/PNG files in the folder, and search recursively if you want to use subdirectories"""
        return [os.path.join(root, f) for root, dirs, files in os.walk(self.folder_path) for f in files if f.endswith('.jpg') or f.endswith('.png')]

    def get_image(self):
        files = self.get_media_folder_images()

        if self.upload_all:
            logging.info('Bulk uploading all photos. This may take a while...')
            # Remove the filenames of images that have already been uploaded
            files = list(set(files) - set([f['file'] for f in self.uploaded_files]))
            files_to_upload = files
        else:
            if len(files) == 0:
                logging.info('No new images to upload.')
                return None, None, None, None
            else:
                logging.info('Choosing random image.')
                files_to_upload = [random.choice(files)]

        for file in files_to_upload:
            # Read the contents of the file
            # Check if the file is found in get_remote_filename()
            file_type = 'JPEG' if file.endswith('.jpg') else 'PNG'
            remote_filename = self.get_remote_filename(file)
            if remote_filename:
                return None, file_type, file, remote_filename
            else:
                with open(file, 'rb') as f:
                    data = BytesIO(f.read())
                return data, file_type, file, None

        return None, None, None, None  # If no files were processed

    def get_remote_filename(self, file):
        for uploaded_file in self.uploaded_files:
            if uploaded_file['file'] == file:
                return uploaded_file['remote_filename']
        return None