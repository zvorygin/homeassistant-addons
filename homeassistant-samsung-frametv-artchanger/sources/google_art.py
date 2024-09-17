import logging
import random
import requests
import subprocess
import os
from io import BytesIO
from typing import Optional, Tuple, Union

class GoogleArt:
    def __init__(self, download_high_res: bool = False) -> None:
        self.download_high_res = download_high_res

    def get_image(self) -> Optional[Tuple[Optional[BytesIO], Optional[str], Optional[str], Optional[str]]]:
        logging.info('Fetching image list from Google Arts & Culture...')
        json_url = "https://www.gstatic.com/culturalinstitute/tabext/imax_2_2.json"
        try:
            response = requests.get(json_url)
            response.raise_for_status()
            image_list: list[dict[str, Union[str, dict]]] = response.json()
            if not image_list:
                raise ValueError("Empty image list received")

            selected_image: dict[str, Union[str, dict]] = random.choice(image_list)

            if self.download_high_res:
                logging.info(f'Downloading high-res image: {selected_image["title"]} by {selected_image["creator"]}')
                image_url: str = f"https://artsandculture.google.com/{selected_image['link']}"
                output_file: str = f"{selected_image['link'].replace('/', '_')}.jpg"

                try:
                    subprocess.run(["dezoomify-rs", "--max-width", "5001", "--compression", "0", image_url, output_file], check=True)
                    with open(output_file, 'rb') as f:
                        image_data: BytesIO = BytesIO(f.read())
                    os.remove(output_file)  # Clean up the temporary file
                except subprocess.CalledProcessError as e:
                    logging.error(f"Failed to download high-res image: {str(e)}")
                    return None, None, None, None
                except OSError as e:
                    logging.error(f"Failed to remove temporary file: {str(e)}")
                    # Continue execution even if file removal fails
            else:
                image_url = selected_image['image'] + "=w3840-h2160-c"
                logging.info(f'Downloading image: {selected_image["title"]} by {selected_image["creator"]}')
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                image_data = BytesIO(image_response.content)

            return image_data, 'JPEG', f"{selected_image['title']} by {selected_image['creator']}", None
        except requests.RequestException as e:
            logging.error(f"Failed to fetch image list: {str(e)}")
            return None, None, None, None
        except (ValueError, KeyError) as e:
            logging.error(f"Error processing image data: {str(e)}")
            return None, None, None, None