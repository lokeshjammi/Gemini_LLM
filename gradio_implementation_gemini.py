from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import gradio as gr
from PIL import Image
from io import BytesIO

load_dotenv('.env')

api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

client = genai.Client(api_key=api_key)

def chat_with_gemini(query, history):
    model = client.chats.create(
        model="gemini-2.5-flash-image"
    )
    response = model.send_message_stream(query)
    full_response = ""
    for chunk in response:
        if chunk.text:
            full_response += chunk.text
            yield full_response

gr.ChatInterface(
    fn=chat_with_gemini,
    type="messages",
    title="Gemini-2.5-Flash Chat Interface",
    description="Chat with Google's Gemini-2.5-Flash model using Gradio.",
    theme="soft"
).launch()