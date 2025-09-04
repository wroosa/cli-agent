from pathlib import Path
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