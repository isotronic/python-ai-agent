import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
  name="write_file",
  description="Writes content to a specified file, constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The file path to write to, relative to the working directory.",
      ),
      "content": types.Schema(
        type=types.Type.STRING,
        description="The content to write to the file.",
      ),
    },
  ),
)

def write_file(working_directory, file_path, content):
  working_directory_abs = os.path.abspath(working_directory)
  full_file_path = os.path.abspath(os.path.join(working_directory_abs, file_path))

  if not full_file_path.startswith(working_directory_abs):
    return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"

  parent_dir = os.path.dirname(full_file_path) or working_directory_abs
  try:
    os.makedirs(parent_dir, exist_ok=True)
  except Exception as e:
    return f"Error: Cannot create directories at path '{parent_dir}': {e}"

  try:
    with open(full_file_path, "w") as f:
      f.write(content)
  except Exception as e:
    return f"Error: Cannot write content to '{full_file_path}': {e}"

  return f"Successfully wrote to '{full_file_path}' ({len(content)} characters written)"