import openai
import os
from dotenv import load_dotenv


def Chat_GPT_request(foodName,quantity,quantityValue):

    message = f"""
        Give me the total calories, grams of protein, grams of fat, and grams of carbs in {quantity}{quantityValue} of {foodName}. 
        Is it food or not? , and if so, correct any mistakes in the name (e.g., 'brow white' should be 'brown rice', or 'which bread' should be a specific bread type like 'whole wheat bread').
        Only return a valid JSON object with the following structure and do not include 'json':

        {{
            "FoodName": "foodName",
            "Calories": null,  # Use null if the value is not available
            "Protein": null,   # Use null if the value is not available
            "Fat": null,       # Use null if the value is not available
            "Carb": null,      # Use null if the value is not available
            "Quantity": {quantityValue},
            "Food": "true" or "false"
        }}
        """


    load_dotenv()
    API_KEY = os.getenv('ChatGPT_API_KEY')
    openai.api_key = API_KEY
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": message}
    ]
    )
    result = response['choices'][0]['message']['content']
    return result
