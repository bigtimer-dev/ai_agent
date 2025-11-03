import os
from os.path import abspath


def get_files_info(working_directory, directory="."):
    abs_path = os.path.abspath("../")
    join_directory = os.path.join(working_directory, directory)
    print(join_directory)
    print(abs_path)
    # if join_directory.startswith(working_directory):
    # return "yes its inside of it"
    # else:
    #   return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


get_files_info("aiagent", "/workspace")
