from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
    brave_path = "/snap/bin/brave"
    chrome_options = Options()
    chrome_options.binary_location = brave_path
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager(driver_version="142.0.7444.60").install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.google.com/travel/flights")
    return driver

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

#Define open browser function declaration to the model
open_browser_function = {
    "name": "open_browser",
    "description": "This function opens the chrome browser and navigates to google flights and returns the driver object",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

tools = types.Tool(function_declarations=[ticket_calculator_function, open_browser_function])
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
        response = model.send_message(f"If any of the tokens from user which resembles {user_input.lower()}, respond with a polite goodbye message and end the chat.")
        print("\n"+"Gemini:", response.text)
        break

    response = model.send_message(user_input)

    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name
        function_args = function_call.args
        if function_name == "check_price_of_ticket":
            result = check_price_of_ticket(**function_args)
            result_list = list(result.values())
            for i in range(len(result_list)):
                city = function_args.get('destination_city')[i]
                result = result_list[i]
                response = model.send_message(f"The ticket fare for {city} is {result}")
                print("\n"+"Gemini:", response.text)
        elif function_name == "open_browser":
            driver = open_browser()
            response = model.send_message(f"The browser has been opened to Google Flights and responded with {driver}")
            print("\n"+"Gemini:", response.text)
            driver.close()
    else:
        print("\n"+"Gemini:", response.text)