from dotenv import load_dotenv
import os
import google.generativeai as genai
import gradio as gr

load_dotenv('.env')
api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

def chat(query, history):
    system_instruction = (
        "Your role is a specialized technical expert. You MUST ONLY answer questions related to technical courses, "
        "specifically Python, Java, Generative AI and web development. Your primary function is to teach and assist with these topics. "
        "Under no circumstances should you answer questions outside of this scope. "
        "If a user asks about any other topic (such as sports, history, geography, or personal advice), "
        "you MUST respond with the following exact phrase and nothing else: "
        "'I am sorry, but I am a technical assistant and can only answer questions related to programming and web development.'")
    if "Generative" or "AI" in query:
        system_instruction += "System is still learning about AI, sometimes wrong information may be given, please double check the response."
    if "Hi" or "Hello" or "Good Morning" in query:
        system_instruction += "Any greeting from user query is allowed and can respond in a friendly way."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name='gemini-2.5-pro', system_instruction=system_instruction)
    chat_with_LLM = model.start_chat(history=[])
    response = chat_with_LLM.send_message(query, stream=True, generation_config={
        "temperature": 0.8,
    })
    full_response = ""
    for chunk in response:
        if chunk.text:
            full_response += chunk.text
            yield full_response

gr.ChatInterface(
    fn=chat,
    type="messages"
).launch()
