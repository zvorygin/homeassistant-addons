import logging
import random
import requests
from io import BytesIO
from datetime import datetime, timedelta
from typing import Tuple, Optional

class BingWallpapers:
    def get_image(self) -> Tuple[Optional[BytesIO], Optional[str], Optional[str], Optional[None]]:
        # wallpapers before 2021-08-28 are not available in 4k from https://bing.npanuhin.me/US/en/2021-08-28.jpg
        start_date: datetime = datetime(2021, 8, 28)
        end_date: datetime = datetime.now()
        random_date: datetime = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        formatted_date: str = random_date.strftime("%Y-%m-%d")

        url: str = f"https://bing.npanuhin.me/US/en/{formatted_date}.jpg"

        try:
            response: requests.Response = requests.get(url)
            response.raise_for_status()
            image_data: BytesIO = BytesIO(response.content)
            return image_data, "JPEG", formatted_date, None
        except requests.RequestException as e:
            logging.error(f"Failed to fetch Bing Wallpaper: {str(e)}")
            return None, None, None, None