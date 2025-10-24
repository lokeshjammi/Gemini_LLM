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

#configure the LLM Model with all required things
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
user_prompt = "What's the ticket fare to Chennai and Dubai?"
tools = types.Tool(function_declarations=[ticket_calculator_function])
config = types.GenerateContentConfig(tools=[tools], system_instruction=system_instruction)

#Send request with function declaration
response = client.models.generate_content(model='gemini-2.0-flash', config=config, 
                                          contents=user_prompt)

if response.candidates[0].content.parts[0].function_call:
    llm_response_list = []
    function_call = response.candidates[0].content.parts[0].function_call
    function_name = function_call.name
    function_args = function_call.args
    if function_name == "check_price_of_ticket":
        result = check_price_of_ticket(destination_city=function_args.get('destination_city'))
        result_list = list(result.values())
    for i in range(len(result_list)):
        city = function_args.get('destination_city')[i]
        result = result_list[i]
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents = f"The ticket fare for {city} is {result}",
            config = None
        )
        llm_response_list.append(response.candidates[0].content.parts[0].text)
        print(response.candidates[0].content.parts[0].text)
else:
    print(response.candidates[0].content.parts[0].text)