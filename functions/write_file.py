import os

def write_file(working_directory, file_path, content):
  full_file_path = os.path.abspath(file_path)

  # Ensure the working_directory is an absolute path too
  working_directory_abs = os.path.abspath(working_directory)

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