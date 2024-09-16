from io import BytesIO
from PIL import Image

def resize_and_crop_image(image_data, target_width=3840, target_height=2160):
    with Image.open(image_data) as img:
        # Calculate the aspect ratio
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height

        if img_ratio > target_ratio:
            # Image is wider than target, resize based on height
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            # Image is taller than target, resize based on width
            new_width = target_width
            new_height = int(new_width / img_ratio)

        # Resize the image
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Calculate dimensions for center cropping
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height

        # Perform center crop
        img = img.crop((left, top, right, bottom))

        # Save the processed image to a BytesIO object
        output = BytesIO()
        img.save(output, format='JPEG', quality=90)
        output.seek(0)
        return output