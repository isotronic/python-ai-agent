from call_function import call_function
from google.genai import types
from prompts import system_prompt

def generate_content(client, messages, available_functions, verbose=False):
  response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=messages, 
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
  )
  
  if not response.usage_metadata:
    raise RuntimeError("Gemini API response appears to be malformed")

  if verbose:
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
  
  # Check if we're finished (no function calls and we have text)
  if not response.function_calls and response.text:
    return response.text

  # Add model responses to messages
  if response.candidates:
    messages.extend(candidate.content for candidate in response.candidates if candidate.content)
    
  # Handle function calls
  if response.function_calls:
    function_response_parts = []

    for function_call in response.function_calls:
      call_function_result = call_function(function_call, verbose=verbose)

      if not call_function_result or not call_function_result.parts or not call_function_result.parts[0].function_response or not call_function_result.parts[0].function_response.response:
        raise ValueError("No valid response from function call.")

      # Collect the entire part, not just the response value
      function_response_parts.append(call_function_result.parts[0])

      if verbose:
        print(f"-> {call_function_result.parts[0].function_response.response}")

    # Add function responses as a user message
    function_response_content = types.Content(
      role="user",
      parts=function_response_parts,
    )
    
    messages.append(function_response_content)
  
  # Not finished yet, return None to continue the loop
  return None