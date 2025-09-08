from pathlib import Path
from google.genai import types

def get_files_info(working_directory, directory="."):
    base = Path(working_directory).resolve()
    target = Path(working_directory / Path(directory)).resolve()

    if base not in target.parents and base != target:
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
    
    if not target.is_dir():
        return f"Error: '{directory}' is not a directory"

    directory_details = ''
    try:
        for item in target.iterdir():
            item_stats = item.stat()
            directory_details += f'- {item.name}: file_size={item_stats.st_size}, is_dir={item.is_dir()}\n'
        return directory_details
    except:
        return f'Error: Problem reading from a file or directory in {directory}'

# Function Schema
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself"
            )
        }
    )
)
    