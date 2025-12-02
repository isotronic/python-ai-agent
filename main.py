import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from generate_content import generate_content
from config import MAX_ITERS

load_dotenv()  # Load environment variables from a .env file if present
api_key = os.environ.get("GEMINI_API_KEY")

def main():
  client = genai.Client(api_key=api_key)

  parser = argparse.ArgumentParser(description="AI Code Assistant")
  parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
  parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
  args = parser.parse_args()

  user_prompt = args.user_prompt

  messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

  available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_write_file, schema_get_file_content, schema_run_python_file])

  for _ in range(MAX_ITERS):
    try:
      if final_response := generate_content(client, messages, available_functions, args.verbose):
        print(final_response)
        break
    except Exception as e:
      print(f"Error in generate_content: {e}")

if __name__ == "__main__":
  main()
