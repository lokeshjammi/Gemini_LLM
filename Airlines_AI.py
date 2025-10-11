import os

from dotenv import load_dotenv
import google.generativeai as genai
import gradio as gr
from google.generativeai.types import PartType

load_dotenv('.env')
api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print('API Key found')
else:
    print('API Key not found')

def get_ticket_prices(destination_city: str):

    """
    This method helps to know the ticket prices based on the destination city.
    """
    ticket_prices = {
        "chennai": 100,
        "bangalore": 500,
        "mysore": 250
    }
    print("Tool get_ticket_prices call for destination city")
    city = destination_city.lower()
    return ticket_prices.get(city)

# price_function = {
#     "name": "get_ticket_prices",
#     "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price of a destination city, for example when a customer ask 'What is the cost of ticket to this city'",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "destination_city": {
#                 "type": "string",
#                 "description": "The name of the city where the customer want to travel"
#             }
#         }
#     },
#     "required": ["destination_city"],
#     "additionalProperties": False
# }
# tools = [
#     {
#         "type": "function",
#         "name": price_function,
#     }
# ]

def airlines_ai(query):
    genai.configure(api_key=api_key)
    system_instruction = "Your role is an airlines guide now and you should answer only to be queries related to travel like flights availability, tickets fare, airport location, baggage weight"
    system_instruction += "Any questions asked outside of travel, please respond that you don't have info about that query in a polite and friendly manner only."
    system_instruction += "You must respond only in markdown format only"
    model = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=system_instruction, tools=[get_ticket_prices])
    first_response =  model.generate_content(query)
    if first_response.candidates[0].content.parts[0].function_call:
        function_call = first_response.candidates[0].content.parts[0].function_call
        tool_name = function_call.name
        tool_args = function_call.args
        print(f"Agent want's to use tool called {tool_name}")
        if tool_name == 'get_ticket_prices':
            tool_result = get_ticket_prices(**tool_args)
        conversation_history = [
            {"role": "user", "parts": [{"text": query}]},
            first_response.candidates[0].content,
            {"function_response": {"name": tool_name, "response": {"price": tool_result}}}
        ]
        final_response = model.generate_content(conversation_history)
    else:
        final_response = ""
        for chunk in first_response:
            if chunk.text:
                final_response += chunk.text
                yield final_response

    full_response = ""
    for chunk in final_response:
        if chunk.text:
            full_response += chunk.text
            yield final_response


view = gr.Interface(
    fn=airlines_ai,
    inputs = [gr.Textbox(label="You'r question here")],
    outputs = [gr.Markdown(label="Your Response")],
    flagging_mode="never"
)
view.launch()