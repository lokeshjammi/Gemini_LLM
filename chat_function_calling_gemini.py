from google import genai
from dotenv import load_dotenv
import os
import gradio as gr

load_dotenv('.env')

api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

client = genai.Client(api_key=api_key)

model = client.chats.create(
    model="gemini-2.0-flash",
    history=[]
)

while True:
    user_input = input("User: ")
    
    if user_input.lower() in ['exit', 'quit']:
        print("Exiting the chat.")
        break

    response = model.send_message(user_input)

    if response.candidates[0].content.parts[0].function_call:
        pass
    else:
        print("\n"+"Gemini:", response.text)