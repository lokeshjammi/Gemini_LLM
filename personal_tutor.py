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
        system_instruction = "Please give me the response in a markdown format and for any negative sentimental queries like kill, crash from user, response should be like sorry I can't respond this should be maintained strictly"
        model = genai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction=system_instruction)
        chat = model.start_chat(history=[])
        print('Gemini Chatbot is ready to chat, Type Quit/Exit to leave the chat')
        print("*" * 60)
        while True:
            user_query = input('You: ')
            file_path = input("Attach file (optional, press Enter to skip, if needed make sure attachment file should be from input folder): ")
            if user_query.lower() in ['quit', 'exit']:
                print('Goodbye, Have a good day')
                break
            if not user_query.strip():
                print('Please enter a query')
                continue
            try:
                prompt_list = [user_query]
                if file_path.strip():
                    uploaded_file = genai.upload_file(path=file_path)
                    prompt_list.append(uploaded_file)
                response = chat.send_message(prompt_list, stream=True)
                for chunk in response:
                    print(chunk.text, end="", flush=True)
            except Exception as e:
                print(e)

personal_tutor = PersonalTutor()
personal_tutor.chat_bot_execute()