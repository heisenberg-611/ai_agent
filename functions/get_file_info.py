import os
from google.genai import types

def get_files_info(working_directory, directory):
    """
    Returns information about files in a directory inside the working_directory.
    Always returns a string.
    """
    try:
        # Get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize target directory path
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        # Security check: ensure target is inside working directory
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if target path is a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Iterate through directory contents
        result_lines = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)

            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            result_lines.append(
                f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        # Join all results into a single string
        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "Lists files in a specified directory relative to the working directory, "
        "providing file size and directory status"
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Directory path to list files from, relative to the working directory "
                    "(default is the working directory itself)"
                ),
            ),
        },
    ),
)
