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

system_instruction = ("Your role is a specialized technical expert. You MUST ONLY answer questions related to technical courses, "
    "specifically Python, Java, and web development. Your primary function is to teach and assist with these topics. "
    "Under no circumstances should you answer questions outside of this scope. "
    "If a user asks about any other topic (such as sports, history, geography, or personal advice), "
    "you MUST respond with the following exact phrase and nothing else: "
    "'I am sorry, but I am a technical assistant and can only answer questions related to programming and web development.'")
openai = OpenAI(api_key=perplexity_api_key, base_url="https://api.perplexity.ai")

def chat(query, chat_history):
    messages = [
        {
            "role": "system",
            "content": system_instruction
        }
    ] + chat_history + [
        {
            "role": "user",
            "content": query
        }
    ]
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