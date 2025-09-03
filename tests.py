from functions.get_files_info import get_files_info

def show(title, wd, dir_):
    print(title)
    result = get_files_info(wd, dir_)
    
    # indent each line appropriately
    indent = "    " if result.startswith("Error:") else " "
    for line in result.splitlines():
        print(f"{indent}{line}")

if __name__ == "__main__":
    show("Result for current directory:", "calculator", ".")
    show("Result for 'pkg' directory:", "calculator", "pkg")
    show("Result for '/bin' directory:", "calculator", "/bin")
    show("Result for '../' directory:", "calculator", "../")

