from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv('.env')
api_key = os.getenv('PERPLEXITY_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

import requests

api_url = "https://api.perplexity.ai/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "sonar-pro",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What are the main differences between renewable and non-renewable energy sources?"}
    ]
}

response = requests.post(api_url, headers=headers, json=payload)
print(response.json())