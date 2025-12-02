import os
from subprocess import run
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
  name="run_python_file",
  description="Runs a specified Python file with optional arguments, constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The file path to run, relative to the working directory.",
      ),
      "args": types.Schema(
        type=types.Type.ARRAY,
        items=types.Schema(type=types.Type.STRING),
        description="Optional arguments to pass to the Python file.",
      ),
    },
  ),
)

def run_python_file(working_directory, file_path, args=None):
  # sourcery skip: extract-method
  if args is None:
    args = []
  
  full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
  working_directory_abs = os.path.abspath(working_directory)
  
  if os.path.commonpath([full_file_path, working_directory_abs]) != working_directory_abs:
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.exists(full_file_path):
    return f'Error: File "{file_path}" not found.'
  
  if not file_path.endswith(".py"):
    return f'Error: "{file_path}" is not a Python file.'
  
  try:
    result = run(args=["python", full_file_path, *args], text=True, timeout=30, capture_output=True, cwd=working_directory)
    
    output = []
    if result.stdout:
        output.append(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        output.append(f"STDERR:\n{result.stderr}")

    if result.returncode != 0:
        output.append(f"Process exited with code {result.returncode}")

    return "\n".join(output) if output else "No output produced."
    
  except Exception as e:
    return f"Error: executing Python file: {e}"
  
  