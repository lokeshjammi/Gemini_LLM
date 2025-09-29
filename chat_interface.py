from dotenv import load_dotenv
import os
import gradio as gr
from openai import OpenAI

load_dotenv('.env')

perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
if perplexity_api_key:
    print('API Key found')
else:
    print('API Key not found')

# system_instruction = "You're an helpful assistant"
openai = OpenAI(api_key=perplexity_api_key, base_url="https://api.perplexity.ai")

def chat(query, chat_history):
    messages = chat_history + [
        {
            "role": "user",
            "content": query
        }
    ]
    print(chat_history)
    print(messages)
    stream = openai.chat.completions.create(model='sonar', messages=messages, stream=True)
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            yield full_response

gr.ChatInterface(
    fn=chat,
    type="messages"
).launch()