from pathlib import Path
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    base = Path(working_directory).resolve()
    target = Path(working_directory / Path(file_path)).resolve()

    if base not in target.parents and base != target:
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
    
    if not target.is_file():
        return f"Error: File not found or is not a regular file: '{file_path}'"
    
    with open(target, "r") as f:
        file_content_string = f.read(MAX_CHARS)
    
    return file_content_string