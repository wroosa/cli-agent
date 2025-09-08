from pathlib import Path
from google.genai import types
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


# Function Schema
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read a file's content up to 10000 lines, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that will be read, relative to the working directory."
            )
        },
        required=["file_path"]
    )
)