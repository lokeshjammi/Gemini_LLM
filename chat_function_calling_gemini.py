from google import genai
from google.genai import types
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

system_instruction = "You're an travel advisor and you only focus to answer for questions related to travel."
system_instruction += "When user asks for one way ticket fare you can call the required tool from tool declarations, otherwise if that is a general query, response"
"should be given normally and if the query is not related to tarvel, please respond like couldn't able to answer other than travelling related questions."

config = types.GenerateContentConfig(system_instruction=system_instruction)

model = client.chats.create(
    model = "gemini-2.0-flash",
    config=config
)