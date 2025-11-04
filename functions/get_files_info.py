import os
from os.path import abspath


def get_files_info(working_directory, directory="."):
    abs_path_join_dir = os.path.abspath(os.path.join(working_directory, directory))
    abs_path_work_dir = os.path.abspath(working_directory)
    if not abs_path_join_dir.startswith(abs_path_work_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_path_join_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        list_of_file_info = []
        for item in os.listdir(abs_path_join_dir):
            item_size = os.path.getsize(os.path.join(abs_path_join_dir, item))
            item_type = (
                True if os.path.isdir(os.path.join(abs_path_join_dir, item)) else False
            )
            new_string = f"-{item}: file_size={item_size} bytes, is_dir={item_type}"
            list_of_file_info.append(new_string)

        return "\n".join(list_of_file_info)

    except Exception as e:
        return f"Error:{e}"
