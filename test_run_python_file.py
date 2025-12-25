from functions.run_python_file import run_python_file


def main():
    print("Test: run main.py (no args)")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Test: run main.py with expression")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print("Test: run tests.py")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Test: outside working directory")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Test: nonexistent file")
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    print("Test: non-python file")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
