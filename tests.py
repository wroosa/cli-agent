from functions.write_file import write_file

def show(title, wd, dir_, cont):
    print(title)
    result = write_file(wd, dir_, cont)

    # indent each line appropriately
    indent = "    " if result.startswith("Error:") else " "
    for line in result.splitlines():
        print(f"{indent}{line}")

if __name__ == "__main__":
    # show("Result for main.py:", "calculator", "main.py")
    # show("Result for pkg/calculator.py:", "calculator", "pkg/calculator.py")
    # show("Result for '/bin/cat' directory:", "calculator", "/bin/cat")
    # show("Result for pkg/does_not_exist.py", "calculator", "pkg/does_not_exist.py")

    show("Result for lorem.txt", "calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # show("Result for pkg/morelorem.txt:", "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # show("Result for /tmp/temp.txt:", "calculator", "/tmp/temp.txt", "this should not be allowed")

