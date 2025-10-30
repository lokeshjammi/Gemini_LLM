from dotenv import load_dotenv
import os
from google import genai

load_dotenv('.env')

api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

client = genai.Client(api_key=api_key)

model = client.chats.create(
    model="gemini-2.5-flash"
)
response = model.send_message_stream("Hello! How can I use Gemini API with Python?")

for chunk in response:
    if chunk.text:
        print(chunk.text, end='', flush=True)