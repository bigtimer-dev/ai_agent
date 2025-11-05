import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_path_working = os.path.abspath(working_directory)
    if not abs_path_working.endswith(os.sep):
        abs_path_working = abs_path_working + os.sep

    abs_path_join = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_path_join.startswith(abs_path_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        parent_dir = os.path.dirname(abs_path_join)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(abs_path_join, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write with content a specified file_path file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path of the file to write, relative to the working directory. if the file_path does not exists it create it from the one you specified",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be write into the file that is specified in the file_path",
            ),
        },
    ),
)
