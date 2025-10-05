import os

from dotenv import load_dotenv
import google.generativeai as genai

ticket_prices = {
        "chennai": 100,
        "bangalore": 500,
        "mysore": 250
}
def get_ticket_prices(destination_city):
    print("Tool get_ticket_prices call for destination city")
    city = destination_city.lower()
    return ticket_prices.get(city)

price_function = {
    "name": "get_ticket_prices",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price of a destination city, for example when a customer ask 'What is the cost of ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The name of the city where the customer want to travel"
            }
        }
    },
    "required": ["destination_city"],
    "additionalProperties": False
}
tools = [
    {
        "type": "function",
        "name": price_function,
    }
]
def airlines_ai(query):
    load_dotenv('.env')
    api_key = os.getenv('GEMINI_API_KEY')

    if api_key:
        print('API Key found')
    else:
        print('API Key not found')

    genai.configure(api_key=api_key)
    system_instruction = "Your role is an airlines guide now and you should answer only to be queries related to travel like flights availability, tickets fare, airport location, baggage weight"
    system_instruction += "Any questions asked outside of travel, please respond that you don't have info about that query in a polite and friendly manner only."
    system_instruction += "You must respond only in markdown format only"
    model = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=system_instruction)
    response =  model.generate_content(query, stream=True)
    for chunk in response:
        print(chunk.text, end="", flush=True)

airlines_ai("What's the ticket fare cost to chennai?")