from google.genai import types

from functions import get_file_content, get_files_info, run_python_file, write_file

def call_function(function_call_part: types.FunctionCall, verbose=False):
  function_name = function_call_part.name or "unknown"
  if verbose:
    print(f"Calling function: {function_name}({function_call_part.args})")
  else:
    print(f" - Calling function: {function_name}")
    
  function_map = {
    "get_files_info": get_files_info.get_files_info,
    "write_file": write_file.write_file,
    "get_file_content": get_file_content.get_file_content,
    "run_python_file": run_python_file.run_python_file,
  }
    
  function_to_call = function_map.get(function_name)
  
  if not function_to_call:
    return types.Content(
      role="tool",
      parts=[
        types.Part.from_function_response(
          name=function_name,
          response={"error": f"Unknown function: {function_name}"},
        )
      ],
    )
    
  args = function_call_part.args or {}
  args["working_directory"] = "./calculator"
  
  function_result = function_to_call(**args)
  
  return types.Content(
    role="tool",
    parts=[
      types.Part.from_function_response(
        name=function_name,
        response={"result": function_result},
      )
    ],
)