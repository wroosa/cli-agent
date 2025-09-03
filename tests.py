from functions.get_file_content import get_file_content

def show(title, wd, dir_):
    print(title)
    result = get_file_content(wd, dir_)

    # indent each line appropriately
    indent = "    " if result.startswith("Error:") else " "
    for line in result.splitlines():
        print(f"{indent}{line}")

if __name__ == "__main__":
    show("Result for main.py:", "calculator", "main.py")
    show("Result for pkg/calculator.py:", "calculator", "pkg/calculator.py")
    show("Result for '/bin/cat' directory:", "calculator", "/bin/cat")
    show("Result for pkg/does_not_exist.py", "calculator", "pkg/does_not_exist.py")

