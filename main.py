import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from call_function import call_function

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
  
  available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_write_file, schema_get_file_content, schema_run_python_file])

  response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=messages, 
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
  )
  
  if response.function_calls:
    function_responses = []
    
    for function_call in response.function_calls:
      call_function_result = call_function(function_call, verbose=(command_flag == "--verbose"))
      
      if not call_function_result or not call_function_result.parts or not call_function_result.parts[0].function_response or not call_function_result.parts[0].function_response.response:
        raise ValueError("No valid response from function call.")
      
      function_responses.append(call_function_result.parts[0].function_response.response)
      
      if command_flag == "--verbose":
        print(f"-> {call_function_result.parts[0].function_response.response}")

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
