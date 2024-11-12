import google.generativeai as genai
import requests
import io
from PIL import Image
from pathlib import Path
import os
from dotenv import load_dotenv

# Print the current working directory
print("Current working directory:", os.getcwd())
Quantity = '100g'

load_dotenv()
Gemini_API_KEY = os.getenv('Gemini_API_KEY')


# Configure the API key for Google Generative AI (keep this secure)
def SacnImage(img_url):
    genai.configure(api_key=Gemini_API_KEY) 

# Set generation configuration
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048
    }

    # Initialize the Generative Model with the updated model name
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)

    
    # Read the image from the URL
    try:
        response = requests.get(img_url)
        response.raise_for_status()  # Raise an error for bad responses
        image_data = response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the image: {e}")
        exit()

    # Prepare the image part
    image_part = {
        "mime_type": "image/jpeg",
        "data": image_data
    }

    # Prepare the prompt part
    # Prepare the prompt part
    prompt_part = [
        f"Please return the following details in JSON format: the name of the object, total calories, grams of protein, grams of fat, and grams of carbs in {Quantity},it is food or not. Only return a valid JSON object with the following structure and not include json:\n\n",
        '''
        {
            "name": "string",
            "calories": number_or_null,
            "protein": number_or_null,
            "fat": number_or_null,
            "carb": number_or_null,
            "quantity": "{Quantity}"  # Use curly braces for JSON formatting,
            "food": true_or_false
        }
        ''',
        "\n\nImage description:",
        image_part  # This should be the description or data related to the image you're processing
    ]


    # Generate content based on the prompt
    try:
        response = model.generate_content(prompt_part)
        print(response.text)  # Adjust according to the actual response structure
        result = response.text
    except Exception as e:
        print(f"Error generating content: {e}")
    return result
