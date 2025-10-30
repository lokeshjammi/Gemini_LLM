from dotenv import load_dotenv
import os
from google import genai
from PIL import Image
from io import BytesIO

load_dotenv('.env')

api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

client = genai.Client(api_key=api_key)

prompt = "Give me an healthy tiger prawn which grown by farmers in Andhra Pradesh, India that image should be highly detailed and realistic. and I want to use the " \
"same image as reference to compare with real time prawn farming images to identify the healthy prawn in the farm. mention the idea weight of the prawn in the image. and current date price per KG on image."

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt
)

for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.show(
            title="Generated Image"
        )