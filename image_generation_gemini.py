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

prompt = "Generate an image of a tollywood hero pawankalyan in a stylish pose with sunglasses."

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