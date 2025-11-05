import os
from functions.config import CHAR_LIMIT
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_work_dir = os.path.abspath(working_directory)
    abs_join_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_join_dir.startswith(abs_work_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_join_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_join_dir, "r") as f:
            file_content_string = f.read(CHAR_LIMIT + 1)
            if len(file_content_string) > CHAR_LIMIT:
                return (
                    file_content_string[:-1]
                    + f'[...File "{file_path}" truncated at 10000 characters]'
                )
            return file_content_string

    except Exception as e:
        return f"Error:{e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read files of a specified file_path up to 10,000 characters and truncated the rest if is more than 10,000, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path of the file to read from for not more than 10,000 characters, relative to the working directory.",
            ),
        },
    ),
)
