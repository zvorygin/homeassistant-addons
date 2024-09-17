import logging
import random
import requests
from io import BytesIO
from datetime import datetime, timedelta

class BingWallpapers:
    def get_image(self):
        # wallpapers before 2021-08-28 are not available in 4k from https://bing.npanuhin.me/US/en/2021-08-28.jpg
        start_date = datetime(2021, 8, 28)
        end_date = datetime.now()
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        formatted_date = random_date.strftime("%Y-%m-%d")

        url = f"https://bing.npanuhin.me/US/en/{formatted_date}.jpg"

        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            return image_data, "JPEG", formatted_date, None
        except requests.RequestException as e:
            logging.error(f"Failed to fetch Bing Wallpaper: {str(e)}")
            return None, None, None, None