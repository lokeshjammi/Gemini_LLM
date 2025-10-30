from dotenv import load_dotenv
import os
from google import genai
from PIL import Image
from io import BytesIO
from google.genai import types

load_dotenv('.env')

api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

client = genai.Client(api_key=api_key)
cwd = os.getcwd()
img_path = os.path.join(cwd, 'generated_prawn_image.png')
print(img_path)

with open(img_path, 'rb') as f:
    image_data = f.read()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(
            data=image_data,
            mime_type="image/png"
        ),
        'Based on the image provided, suggest whether it is healthy or not. Also provide suggestions to improve the health if it is not healthy. and generate me the response in telugu language.'
        'Suggest me some common medications which is available in local market to treat the fungal infection in prawn farming.'
    ]
)

print(response.text)