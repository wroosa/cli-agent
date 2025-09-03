from pathlib import Path

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