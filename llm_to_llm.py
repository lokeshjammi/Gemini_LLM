import os

import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI


def setup_api_key():
    load_dotenv('.env')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
    if not gemini_api_key or not perplexity_api_key:
        raise Exception('GEMINI_API_KEY or PERPLEXITY_API_KEY not set')

def main():
    try:
        setup_api_key()
        smooth_bot_system_instruction = "You are a smooth, clam and reasonable AI, your goal is to solve the escalations and you will never get anger for any reason"
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        smooth_bot = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=smooth_bot_system_instruction)

        aggresive_bot_instruction = "You are an aggresive and impatient AI, you have to oppose every point and strongly state you opinions, your goal is not to agree with other AI"
        aggresive_bot = OpenAI(api_key=os.getenv('PERPLEXITY_API_KEY'), base_url="https://api.perplexity.ai")

        debate_topic = 'Will AI replace most of the jobs or create lot of jobs?'
        print(debate_topic)
        next_query = debate_topic

        while True:
            print("*" * 60)
            smooth_bot_response = smooth_bot.generate_content(next_query, stream=True)
            for chunk in smooth_bot_response:
                print("Smooth_bot_response:- "+chunk.text, flush=True, end="")
            next_query = smooth_bot_response.text

            aggresive_bot_text = aggresive_bot.chat.completions.create(
                model="sonar",
                messages=[
                    {
                        "role": "system",
                        "content": aggresive_bot_instruction
                    },
                    {
                        "role": "user",
                        "content": next_query
                    }
                ]
            )
            aggresive_bot_response = aggresive_bot_text.choices[0].message.content
            print("Aggresive bot response:-" +aggresive_bot_response)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()

