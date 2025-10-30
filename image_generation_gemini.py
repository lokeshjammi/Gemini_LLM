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

prompt = "Give me an tiger prawn which has some fungal infection that image should be highly detailed and realistic. and I want to use the " \
"same image as reference to compare with real time prawn farming images to identify the healthy prawn in the farm."

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
        image.save("generated_prawn_image.png")