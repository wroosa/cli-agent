from pathlib import Path

def is_within_directory(base_dir, target_path):
    base = Path(base_dir).resolve()
    target = Path(target_path).resolve()
    return base in target.parents or base == target

def is_directory(target_path):
    return Path(target_path).is_dir()

def get_files_info(working_directory, directory="."):

    if not is_within_directory(working_directory, directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not is_directory(directory):
        return f'Error: "{directory}" is not a directory'
    

    directory_details = ''
    try:
        for item in Path(directory).iterdir():
            item_stats = item.stat()
            directory_details += f'- {item.name}: file_size={item_stats.st_size}, is_dir={item.is_dir()}\n'
        return directory_details
    except:
        return f'Error: Problem reading from a file or directory in {directory}'

print(get_files_info(".", '.'))

    