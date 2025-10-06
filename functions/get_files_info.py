import os
from pathlib import Path

def get_files_info(working_directory, directory="."):
    target_directory = os.path.join(working_directory, directory)
    
    # Resolve to absolute path to prevent path traversal
    try:
        resolved_target = Path(target_directory).resolve()
        resolved_working = Path(working_directory).resolve()
    except Exception:
        return f"Error: Invalid path '{directory}'"
    
    if not resolved_target.is_relative_to(resolved_working):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
    if not os.path.exists(target_directory):
        return f"Error: Directory '{directory}' does not exist"
    if not os.path.isdir(target_directory):
        return f"Error: '{directory}' is not a directory"

    try:
        items = os.listdir(target_directory)
    except Exception as e:
        return f"Error: Unable to list directory '{directory}': {str(e)}"

    dir_info = [f"""Result for {"current" if directory == "." else f"'{directory}'"} directory:"""]
    
    for item in items:
        try:
            item_path = os.path.join(target_directory, item)
            item_info = f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
        except Exception as e:
            return f"Error: Unable to get file info for '{item}': {str(e)}"
        dir_info.append(item_info)
        
    info_str = "\n".join(dir_info)
    return info_str
    