import os

from dotenv import load_dotenv
import google.generativeai as genai

class PersonalTutor:

    def __init__(self):
        load_dotenv('.env')

        api_key = os.getenv('GEMINI_API_KEY')

        if api_key:
            print('*' * 60)
        else:
            print('API Key not found')

        genai.configure(api_key=api_key)

    def chat_bot_execute(self):
        system_instruction = "Please give me the response in a markdown format"
        model = genai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction=system_instruction)
        chat = model.start_chat(history=[])
        print('Gemini Chatbot is ready to chat, Type Quit/Exit to leave the chat')
        print("*" * 60)
        while True:
            user_query = input('You: ')
            if user_query.lower() in ['quit', 'exit']:
                print('Goodbye, Have a good day')
                break
            if not user_query.strip():
                print('Please enter a query')
                continue
            try:
                response = chat.send_message(user_query, stream=True)
                for chunk in response:
                    print(chunk.text, end="", flush=True)
            except Exception as e:
                print(e)

personal_tutor = PersonalTutor()
personal_tutor.chat_bot_execute()