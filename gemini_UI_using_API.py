from dotenv import load_dotenv
import os
from google import genai as genai
import gradio as gr

def stream_with_gemini_api(query):
    try:
        load_dotenv('.env')
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                print('GEMINI API KEY FOUND')
            else:
                print('GEMINI API KEY NOT FOUND')
        except Exception as e:
            print(e)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='gemini-2.5-flash')
        response = model.generate_content(query, stream=True)
        full_response = ""
        for chunk in response:
            full_response += chunk.text
            yield full_response
    except Exception as e:
        print(e)

view = gr.Interface(
    fn = stream_with_gemini_api,
    inputs=[gr.Textbox(label="Query")],
    outputs=[gr.Markdown(label="Your Response")],
    flagging_mode="never"
)
view.launch()