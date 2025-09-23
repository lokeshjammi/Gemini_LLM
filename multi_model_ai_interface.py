import os
from dotenv import load_dotenv
import google.generativeai as genai
import gradio as gr

from WebScraping import Website


def main(company, query, url):
    website = Website(url)
    website_details = website.get_webpage_details()
    # website_title = website_details[0]
    website_content = website_details[1]
    load_dotenv('.env')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if GEMINI_API_KEY:
        print('GEMINI API KEY ENABLED')
    else:
        print('GEMINI API KEY NOT ENABLED')

    genai.configure(api_key=GEMINI_API_KEY)
    system_instruction = (
        f"You an assistant who analyze the content of several webpages from a company website {company} and create a short broucher about the company which should look little funny and crispy"
        "That broucher should able to share with customers, investors and include the content like about company, company culture, future projects, careers etc..."
        "Response should be in Markdown format only")

    system_instruction += f"You can use the {website_content} content for reference"

    system_instruction += """
        Broucher must follow the below format
        [Company Name]
            [A catchy, one-sentence tagline for the company]

        About Us
            [A short, engaging paragraph describing the company's mission and history.]

        Our Services/Products
        Service 1: [Brief description]

        Service 2: [Brief description]

        Service 3: [Brief description]

        Why Choose Us?
            [A paragraph highlighting 2-3 key benefits of choosing this company.]

        Contact Us
            [Provide contact information, including website and phone number.]
    """
    model = genai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction=system_instruction)
    user_query = query
    response = model.generate_content(user_query, stream=True)
    for chunk in response:
        print(chunk.text, end="", flush=True)

def get_selected_model(model, company, query, url):
    if model == 'gemini':
        main(company, query, url)
    else:
        pass

if __name__ == '__main__':
    view = gr.Interface(
        fn=get_selected_model,
        inputs = [gr.Dropdown(label="Select a model", choices=["GEMINI", "Perplexity"]), gr.Textbox(label="Company Name"), gr.Textbox(label="User Query"), gr.Textbox(label="URL")],
        outputs = gr.Markdown(label="Response"),
        flagging_mode="never"
    )
    view.launch()