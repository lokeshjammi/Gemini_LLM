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

system_instruction = ("You are provided with list of links found on a webpage."
                      "You should able to decide which links would be most relevant to include in a broucher about a company,"
                      "such as links About page, company culture, career.")

system_instruction += "Response should be in json format only same as like below links"

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

website = Website('https://www.anthropic.com/')
links_list = website.get_links_url()

user_input = (f"Here are the list of links {links_list}, from the list pick the url which suits for broucher making and that should contains only links related to "
              f"about us, company culture, career etc...")

response = model.generate_content(user_input)
# print(response.text)

# print(f'User_Query: {user_input}')
# print(f'Response_Generated: {response.text}')

embedding_model = 'models/text-embedding-004'
query_embedding = genai.embed_content(model=embedding_model, content=user_input, task_type='RETRIEVAL_DOCUMENT')['embedding']
response_embedding = genai.embed_content(model=embedding_model, content=response.text, task_type='RETRIEVAL_DOCUMENT')['embedding']

query_vector = np.array(query_embedding).reshape(1, -1)
response_vector = np.array(response_embedding).reshape(1, -1)

similarity_score = cosine_similarity(query_vector, response_vector)[0][0]

print(f"Semantic Similarity Score: {similarity_score:.4f}")

threshold_score = 0.7

if similarity_score > threshold_score:
    print('query and response are relavant')
else:
    print('query and response is not relavant')



def get_broucher_user_prompt():
    website_broucher = Website('https://www.anthropic.com/')
    website_details = website_broucher.get_webpage_details()
    system_instruction = (
        "You an assistant who analyze the content of several webpages from a company website and create a short broucher about the company"
        "That broucher should able to share with customers, investors and include the content like about company, company culture, future projects, careers etc..."
        "Response should be in Markdown format only")
    website_title = website_details[0]
    website_content = website_details[1]
    user_prompt = (f"You're looking at a company broucher called {website_title}, here is the relavent content of the website {website_content} use this information to build a short "
                   f"broucher of a company, pickup the proper content to make a short broucher for a company and that should include about company, company culture, future projects, careers etc..."
                   f"make sure the output should be in Markdown format")
    model = genai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction = system_instruction)
    broucher_response = model.generate_content(user_prompt)

    # print(broucher_response.text)

    embedding_model = 'models/text-embedding-004'
    query_embedding = genai.embed_content(model=embedding_model, content=user_prompt, task_type='RETRIEVAL_DOCUMENT')[
        'embedding']
    response_embedding = genai.embed_content(model=embedding_model, content=broucher_response.text, task_type='RETRIEVAL_DOCUMENT')[
        'embedding']

    query_vector = np.array(query_embedding).reshape(1, -1)
    response_vector = np.array(response_embedding).reshape(1, -1)

    similarity_score = cosine_similarity(query_vector, response_vector)[0][0]

    print(f"Semantic Similarity Score: {similarity_score:.4f}")

    threshold_score = 0.7

    if similarity_score > threshold_score:
        print('query and response are relavant')
    else:
        print('query and response is not relavant')


get_broucher_user_prompt()