import os

import google.generativeai as genai
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

from WebScraping import Website
import numpy as np

load_dotenv('.env')

api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

genai.configure(api_key=api_key)

system_instruction = ("You are assigned with list of links from an webpage"
                      "Response should be in json format only same as like below links")

system_instruction += """
    {
        links = [
            {
                "type": "About-us",
                "url": "https://full/url/goes/here/about-us"
            }
        ]
    }
"""

model = genai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction = system_instruction)

website = Website('https://courses.rahulshettyacademy.com/')
links_list = website.get_links_url()

user_input = (f"Here are the list of links {links_list}, from the list pick the url which suits for broucher making and that should contains only links related to "
              f"about us, company culture, career etc...")

response = model.generate_content(user_input)
# print(response.text)

print(f'User_Query: {user_input}')
print(f'Response_Generated: {response.text}')

embedding_model = 'models/text-embedding-004'

query_embedding = genai.embed_content(model=embedding_model, content=user_input, task_type='RETRIEVAL_DOCUMENT')['embedding']

response_embedding = genai.embed_content(model=embedding_model, content=user_input, task_type='RETRIEVAL_DOCUMENT')['embedding']

query_vector = np.array(query_embedding).reshape(1, -1)
response_vector = np.array(response_embedding).reshape(1, -1)

similarity_score = cosine_similarity(query_vector, response_vector)[0][0]

print(f"Semantic Similarity Score: {similarity_score:.4f}")

threshold_score = 0.7

if similarity_score > threshold_score:
    print('query and response are relavant')
else:
    print('query and response is not relavant')