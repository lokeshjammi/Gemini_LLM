from dotenv import load_dotenv
import os
from google import genai
from google.genai import types


load_dotenv('.env')

if os.getenv('GEMINI_API_KEY'):
    print('API Key found')
else:
    print('API Key not found')

system_instruction = "You're an travel advisor and you only focus to answer for questions related to travel."
system_instruction += "When user asks for one way ticket fare you can call the required tool from tool declarations, otherwise if that is a general query, response"
"should be given normally and if the query is not related to tarvel, please respond like couldn't able to answer other than travelling related questions."
def check_price_of_ticket(destination_city: str):
    city = destination_city.lower()
    ticket_fare = {
        "chennai": 1000,
        "bangalore": 1200,
        "mumbai": 1500, 
    }
    return ticket_fare[city]

#Define function declarations to the model
ticket_calculator_function = {
    "name": "check_price_of_ticket",
    "description": "This function returns the ticket fare based on the given city",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city with you want to travel"
        }
    },
    "required": ["destination_city"]
}
}

#configure the LLM Model with all required things
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
user_prompt = "What's the ticket fare to Chennai?"
tools = types.Tool(function_declarations=[ticket_calculator_function])
config = types.GenerateContentConfig(tools=[tools], system_instruction=system_instruction)

#Send request with function declaration
response = client.models.generate_content(model='gemini-2.0-flash', config=config, 
                                          contents=user_prompt)

if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(function_call)
    function_name = function_call.name
    function_args = function_call.args
    print(function_name)
    print(function_args)
    if function_name == "check_price_of_ticket":
        result = check_price_of_ticket(destination_city=function_args.get('destination_city'))
        print(result)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents = f"The ticket fare for {function_args.get('destination_city')} is {result}",
        config = None
    )
    print(response.candidates[0].content.parts[0].text)
else:
    print(response.candidates[0].content.parts[0].text)