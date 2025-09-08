from pathlib import Path
from google.genai import types

def write_file(working_directory, file_path, content):
    base = Path(working_directory).resolve()
    target = Path(working_directory / Path(file_path)).resolve()

    if base not in target.parents and base != target:
        return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"
    
    if not target.exists():
        # Create the directory if does not exist
        if not target.parent.exists():
            target.parent.mkdir(parents=True)

    # Create the file and write to it
    with target.open("w") as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

# Function Schema
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a new file at a specified path or overwrite to an existing file at that same specified path, that path is constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that will be written or overwritten, relative to the working directory. If not provided the function will return an error string"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string content being written to the file."
            )
        },
        required=["file_path", "content"]
    )
)

