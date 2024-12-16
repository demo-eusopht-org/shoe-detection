import requests
from helper import image_to_base64
import json

def upload_to_imgur(image_path):
    client_id = '9d2f09895f53d2a'
    headers = {'Authorization': f'Client-ID {client_id}'}
    url = 'https://api.imgur.com/3/image'

    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        img_url = data['data']['link']
        return img_url
    else:
        print('Error uploading image to Imgur:', response.status_code)
        return None
    

def upload_to_imgbb(image_path):
    # URL of the endpoint
    url = "https://api.imgbb.com/1/upload"
    # Your client API key
    api_key = "062ddb23b2795203cd7934caab5d3d56"
    base64_image = image_to_base64(image_path)
    # Image data (base64-encoded)
    image_data = base64_image
    # Request parameters
    params = {
        "expiration": "600",
        "key": api_key
    }
    # Construct the payload
    payload = {
        "image": image_data
    }
    # Send the POST request
    response = requests.post(url, params=params, data=payload)
    return json.loads(response.text)['data']['url']