from dotenv import load_dotenv
import os
import gradio as gr
from openai import OpenAI


def stream_with_perplexity(query):
    try:
        sytem_instruction = "You're an assistant who responds in markdown format."
        load_dotenv(".env")
        perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        if perplexity_api_key:
            print('API Key found')
        else:
            print('API Key not found')
        model = OpenAI(api_key=perplexity_api_key, base_url="https://api.perplexity.ai")
        full_response = ""
        result = model.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": sytem_instruction
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            model="sonar",
            stream=True
        )
        print("*" * 60, "AI Response:", "*" * 60)
        for chunk in result:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                yield full_response
                # print(chunk.choices[0].delta.content, end="", flush=True)
    except Exception as e:
        print(e)
        yield (e)

view = gr.Interface(
    stream_with_perplexity,
    inputs=[gr.Textbox(label="Query")],
    outputs=[gr.Markdown(label="Your Response")],
    flagging_mode="never"
)

if __name__ == '__main__':
    view.launch()