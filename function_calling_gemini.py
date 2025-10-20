# --- 1. Import the NEW library ---
# Note: The new library is 'google-genai', not 'google-generativeai'
# You must install it: pip install google-genai
from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv('.env')
if os.getenv("GEMINI_API_KEY"):
    print('API Key found')
else:
    print('API Key not found')


# --- 2. API Key Configuration ---
try:
    # The new library uses genai.configure() at the top level
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set the variable or hardcode your API key in the script.")
    exit()

# --- 3. Define Your Python Function (The "Tool") ---
# This part remains exactly the same.
def calculate_ticket_fare(origin: str, destination: str, adults: int, children: int = 0):
    """
    Calculates the ticket fare based on origin, destination, and passenger count.
    """
    print(f"--- Running Python function: calculate_ticket_fare({origin}, {destination}, {adults}, {children}) ---")
    
    base_fare = 150.0
    distances = {
        ("NYC", "LA"): 2450,
        ("SFO", "NYC"): 2570,
        ("BOS", "MIA"): 1250,
    }
    
    distance = distances.get((origin, destination), 2000) 
    
    adult_fare = (base_fare + (distance * 0.15)) * adults
    child_fare = ((base_fare / 2) + (distance * 0.15)) * children
    total_fare = adult_fare + child_fare
    
    return {
        "origin": origin,
        "destination": destination,
        "adults": adults,
        "children": children,
        "calculated_distance_km": distance,
        "total_fare": round(total_fare, 2),
        "currency": "USD"
    }

# --- 4. Define the Tool Declaration for Gemini ---
# The structure of the tool definition itself is unchanged.
ticket_tool = {
    "function_declarations": [
        {
            "name": "calculate_ticket_fare",
            "description": "Calculates the ticket fare for a trip based on origin, destination, and number of passengers.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "origin": {
                        "type": "STRING",
                        "description": "The starting city or airport code (e.g., 'NYC', 'SFO')."
                    },
                    "destination": {
                        "type": "STRING",
                        "description": "The destination city or airport code (e.g., 'LA', 'MIA')."
                    },
                    "adults": {
                        "type": "INTEGER",
                        "description": "The total number of adult passengers."
                    },
                    "children": {
                        "type": "INTEGER",
                        "description": "The total number of child passengers. Defaults to 0 if not specified."
                    }
                },
                "required": ["origin", "destination", "adults"]
            }
        }
    ]
}

# --- 5. Initialize the Model ---
# We use the *new* model name here.
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # <-- LATEST MODEL
    tools=[ticket_tool] # Pass the tool as a list
)

# --- 6. Start the Chat Conversation ---
# This is still the same.
chat = model.start_chat(enable_automatic_function_calling=False)

# --- 7. First Turn: Send the User's Prompt ---
prompt = "How much would it cost for 2 adults and 1 child to fly from SFO to NYC?"
print(f"USER: {prompt}\n")

response = chat.send_message(prompt)

# --- 8. Second Turn: Check the Model's Response ---
# The way to access the response is slightly different.
# We get the first 'part' from the response's content.
message = response.parts[0]

if not message.function_call:
    print(f"Error: Model did not request a function call. It said: {message.text}")
else:
    function_call = message.function_call
    function_name = function_call.name
    
    # Arguments are now in a simple dictionary, which is easier
    function_args = dict(function_call.args) 
    
    print(f"GEMINI: I need to call a function:")
    print(f"  -> Function: {function_name}")
    print(f"  -> Arguments: {function_args}\n")

    # --- 9. Our Script: Execute the Function ---
    if function_name == "calculate_ticket_fare":
        
        function_response_data = calculate_ticket_fare(
            origin=function_args['origin'],
            destination=function_args['destination'],
            adults=function_args['adults'],
            children=function_args.get('children', 0)
        )
        
        print(f"\nSCRIPT: Ran function, got result: {function_response_data}\n")

        # --- 10. Third Turn: Send the Function's Result Back ---
        # This is the same corrected syntax from the previous answer.
        response = chat.send_message(
            content=[
                {
                    "function_response": {
                        "name": function_name,
                        "response": function_response_data
                    }
                }
            ]
        )
        
        # --- 11. Final Turn: Get Gemini's Natural Language Answer ---
        # We access the final text from the response parts.
        final_answer = response.parts[0].text
        print(f"GEMINI: {final_answer}")

    else:
        print(f"Error: Model tried to call an unknown function: {function_name}")