from functions.get_file_content import get_file_content


def main():
    print("Test: lorem.txt (should truncate)")
    content = get_file_content("calculator", "lorem.txt")
    print("Length:", len(content))
    print(content[-80:])  # show end to verify truncation
    print()

    print("Test: main.py")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Test: pkg/calculator.py")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print("Test: /bin/cat (should error)")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    print("Test: non-existent file")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    main()
