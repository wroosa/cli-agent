from pathlib import Path
from google.genai import types
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    base = Path(working_directory).resolve()
    target = Path(working_directory / Path(file_path)).resolve()

    if base not in target.parents and base != target:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not target.exists():
        return f'Error: File "{file_path}" not found.'
    
    if not target.name.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ["python3", target, *args], 
            capture_output=True,
            cwd=working_directory,
            timeout=30,
            text=True
            )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    if result.stdout.strip() == '':
        return "No output produced"
    
    code = ""
    if result.returncode != 0:
        code = f"Process exited with code {result.returncode}"

    return f'STDOUT:{result.stdout} STDERR:{result.stderr}' + code

# Function Schema
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a python file at a specified path with or without arguments passed in, that path is constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to be executed, relative to the working directory. If not provided the function will return an error string"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional list of arguments to be passed when executing the python file found at the file_path. If no list is provided it will default to an empty list which is no arguments",
                items=types.Schema(type=types.Type.STRING)
            )
        },
        required=["file_path"]
    )
)