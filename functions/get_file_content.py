import os
from functions.config import CHAR_LIMIT


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
