import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('Unsplash_API_KEY')

def Image_Unsplash(search_term):

    access_key = API_KEY
    url = f"https://api.unsplash.com/search/photos?query={search_term}&client_id={access_key}"

    response = requests.get(url).json()
    image_url = response['results'][0]['urls']['regular']
    return image_url



