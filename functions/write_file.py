import os


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
