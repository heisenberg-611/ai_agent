from functions.write_file import write_file


def main():
    print("Test: overwrite lorem.txt")
    print(write_file(
        "calculator",
        "lorem.txt",
        "wait, this isn't lorem ipsum"
    ))
    print()

    print("Test: write new file in pkg/")
    print(write_file(
        "calculator",
        "pkg/morelorem.txt",
        "lorem ipsum dolor sit amet"
    ))
    print()

    print("Test: attempt to write outside working directory")
    print(write_file(
        "calculator",
        "/tmp/temp.txt",
        "this should not be allowed"
    ))


if __name__ == "__main__":
    main()

