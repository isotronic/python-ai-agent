import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

load_dotenv()  # Load environment variables from a .env file if present
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    client = genai.Client(api_key=api_key)
    
    if len(sys.argv) < 2:
        print("Usage: python main.py '<your prompt here>'")
        sys.exit(1)

    user_prompt = sys.argv[1]
    command_flag = sys.argv[2] if len(sys.argv) > 2 else None
    
    messages = types.Content(role="user", parts=[types.Part(text=user_prompt)])

    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=messages, 
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    print(response.text)
    if command_flag == "--verbose":
        print(f"User prompt: {user_prompt}")
        if response.usage_metadata:
            print(f"Prompt tokens: {getattr(response.usage_metadata, 'prompt_token_count', 'N/A')}")
            print(f"Response tokens: {getattr(response.usage_metadata, 'candidates_token_count', 'N/A')}")
        else:
            print("Usage metadata not available.")


if __name__ == "__main__":
    main()
