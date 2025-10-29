from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import gradio as gr

load_dotenv('.env')

api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

client = genai.Client(api_key=api_key)

system_instruction = "You're an travel advisor and you only focus to answer for questions related to travel."
system_instruction += "When user asks for one way ticket fare you can call the required tool from tool declarations, otherwise if that is a general query, response"
"should be given normally and if the query is not related to tarvel, please respond like couldn't able to answer other than travelling related questions."

#ticket fare for the given city
def check_price_of_ticket(destination_city: list[str]):
    result = {}
    ticket_fare = {
        "chennai": {
            "price": 1000,
            "currency": "INR"
        },
        "bangalore": {
            "price": 1200,
            "currency": "INR"
        },
        "mumbai": {
            "price": 1500,
            "currency": "INR"
        }
    }
    for city in destination_city:
        city_lower = city.lower()
        if city_lower in ticket_fare:
            result[city_lower] = ticket_fare[city_lower]
        else:
            result[city_lower] = {"error": "The given city is not found in the database"}
    return result

#Open Chrome browser using selenium
def open_browser():
    pass

#Define function declarations to the model
ticket_calculator_function = {
    "name": "check_price_of_ticket",
    "description": "This function returns the ticket fare based on the given city",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "The list of cities which user wants to know the ticket fare"
        }
    },
    "required": ["destination_city"]
}
}
tools = types.Tool(function_declarations=[ticket_calculator_function])
config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    tools=[tools]
)

model = client.chats.create(
    model="gemini-2.0-flash",
    history=[],
    config=config
)

while True:
    user_input = input("User: ")
    
    if user_input.lower() in ['exit', 'quit']:
        print("Exiting the chat.")
        break

    response = model.send_message(user_input)

    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name
        function_args = function_call.args
        if function_name == "check_price_of_ticket":
            result = check_price_of_ticket(**function_args)
            result_list = list(result.values())
            print(result_list)
            for i in range(len(result_list)):
                city = function_args.get('destination_city')[i]
                result = result_list[i]
                response = model.send_message(f"The ticket fare for {city} is {result}")
                print(response.text)
    else:
        print("\n"+"Gemini:", response.text)