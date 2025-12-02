import os
from config import MAX
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
  full_file_path = os.path.abspath(file_path)
  
  if not full_file_path.startswith(working_directory):
    return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
  
  if not os.path.isfile(file_path):
    return f"Error: File not found or is not a regular file: '{file_path}'"
  
  try:
    with open(file_path, "r") as f:
      file_contents = f.read(MAX)
      if more_contents := f.read(1):
        file_contents += f"[...File '{file_path}' truncated at {MAX} characters]"
      
  except Exception as e:
    return f"Error: Cannot open file '{file_path}': {e}"
  
  return file_contents