import os
from config import MAX

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