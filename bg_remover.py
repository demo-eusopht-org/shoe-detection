import requests
import time
from PIL import Image, ImageEnhance, ImageOps
import os

def remove_background(filename):
    cropped_image_path = "./cropped_images/" + filename
    
    bg_remove_filename = str(int(time.time())) + "-bg-removed-image.png"
    bg_remove_path = "./bg_removed_images/" + bg_remove_filename
    
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(cropped_image_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': os.environ.get('BG_REMOVER_API_KEY')},
    )
    if response.status_code == requests.codes.ok:
        with open(bg_remove_path, 'wb') as out:
            out.write(response.content)
            # image_file = Image.open(bg_remove_path) 
            # Open the image
            image = Image.open(bg_remove_path)

            # Enhance contrast
            contrast_factor = 1.2  # Increase to enhance contrast, decrease to reduce contrast
            contrast = ImageEnhance.Contrast(image)
            image = contrast.enhance(contrast_factor)

            # Enhance sharpness
            sharpness_factor = 2.0  # Increase to enhance sharpness, decrease to reduce sharpness
            sharpness = ImageEnhance.Sharpness(image)
            image = sharpness.enhance(sharpness_factor)

            # Enhance brightness
            brightness_factor = 1.1  # Increase to enhance brightness, decrease to reduce brightness
            brightness = ImageEnhance.Brightness(image)
            image = brightness.enhance(brightness_factor)
            
            # padding_size = 100
            
            # # Add padding with a transparent background color
            # padded_image = ImageOps.expand(image, border=padding_size, fill=(255, 255, 255, 0))

            # # Save the modified image
            # padded_image.save(bg_remove_path)
            
            image.save(bg_remove_path)
            
            # http_url = upload_to_imgbb(bg_remove_path)
            # print("http_url",http_url)
            # removed_person = remove_person(http_url)
            # print("removed_person",removed_person)
            return bg_remove_filename
    else:
        print("Error:", response.status_code, response.text)
        return False