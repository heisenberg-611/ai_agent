import os
from config import MAX_FILE_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    """
    Reads up to MAX_FILE_CHARS characters from a file inside working_directory.
    Always returns a string.
    """
    try:
        # Absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize target file path
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Security check: file must be inside working directory
        valid_target = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if file exists and is a regular file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file safely
        with open(target_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(MAX_FILE_CHARS)

            # Check if file was truncated
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)