# Refined main_app.py using Gemini
import google.generativeai as genai
import json
from tool_definitions import dispense_drink

# --- Configuration ---
# Get your API key from Google AI Studio: https://aistudio.google.com/app/apikey
# It's better to set this as an environment variable, but this is fine for testing.
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

genai.configure(api_key="AIzaSyALVuqFwCV75ungfdOKHLMK18cn6Xi1jH8")

# Tool mapping with drink dispenser added
available_tools = {
    "dispense_drink": dispense_drink
}

# System prompt to make the AI more action-oriented
SYSTEM_PROMPT = """You are an AI assistant controlling physical devices. You have access to tools that can control real hardware.

IMPORTANT: When someone expresses thirst or wants a drink in ANY way, immediately use the dispense_drink() function. Do NOT ask questions or provide alternatives - just dispense the drink.

Examples of when to dispense a drink:
- "I'm thirsty"
- "I need a drink" 
- "Give me something to drink"
- "I want water"
- "I could use a drink"
- "Wish I had a drink"
- "I'm parched"
- "Get me a beverage"
- Any mention of being thirsty or wanting liquid refreshment

Your role is to take action, not to explain limitations. If someone wants a drink, dispense it immediately using the available tool."""

def run_gemini_conversation(user_prompt: str):
    """
    Handles a single, stateless conversation with Gemini to execute a tool.
    """
    print(f"\n--- New Request ---")
    print(f"USER: {user_prompt}")
    
    # Combine system prompt with user prompt
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser request: {user_prompt}"
    
    # BEST PRACTICE: Create the model for each self-contained request.
    # This prevents chat history from growing and causing issues.
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        tools=[dispense_drink]
    )
    
    # We send the message directly instead of starting a persistent chat session.
    # This is more robust for a command-and-control system.
    response = model.generate_content(full_prompt)
    print(response)
    
    try:
        # The function call is in the first part of the first candidate
        function_call = response.candidates[0].content.parts[0].function_call
        if function_call is not None:
            function_name = function_call.name
            args = function_call.args or {}
            print(f"GEMINI: Wants to call '{function_name}' with args: {dict(args)}")
            
            function_to_call = available_tools.get(function_name)
            if function_to_call:
                result = function_to_call(**dict(args))
                print(f"Function result: {result}")
            else:
                print(f"SYSTEM: Error - Model tried to call unknown function '{function_name}'")
        else:
            print("GEMINI: No function call in this response.")
    
    except (AttributeError, IndexError):
        # This happens if the model responds with text instead of a function call
        print(f"GEMINI: Responded with text: '{response.text}'")

# --- Main Execution Block ---
if __name__ == "__main__":
    print("🤖 Drink Dispensing Assistant Ready!")
    print("💡 Say things like: 'I'm thirsty'")
    print("Type 'quit' to exit.\n")
    
    while True:
        prompt = input("Enter your command (or 'quit' to exit): ")
        if prompt.lower() in ['quit', 'exit']:
            break
        if not prompt:  # Skip empty inputs
            continue
        
        run_gemini_conversation(prompt)