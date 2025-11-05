import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_working_path = os.path.abspath(working_directory)
    if not abs_working_path.endswith(os.sep):
        abs_working_path = abs_working_path + os.sep

    abs_path_join = os.path.abspath(os.path.join(abs_working_path, file_path))

    if not abs_path_join.startswith(abs_working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_path_join):
        return f'Error: File "{file_path}" not found.'

    if not abs_path_join.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", file_path, *args],
            cwd=working_directory,
            timeout=30,
            capture_output=True,
            text=True,
        )

        output_list = []
        if result.stdout:
            output_list.append(f"STDOUT:{result.stdout}")
        if result.stderr:
            output_list.append(f"STDERR:{result.stderr}")
        if result.returncode != 0:
            output_list.append(f"Process exited with code {result.returncode}")

        output_string = "\n".join(output_list)

        if not output_list:
            output_string = "No output produced"

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"


# declaration of the funcion for llm tools
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified python script in the file_path , constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path of the python script to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Dont ask for args if user dont give them. Take optionals arguments as an array if the script need them to execute with other properties, if user dont specified any run without it",
                items=types.Schema(
                    type=types.Type.STRING, description="aditional args"
                ),
            ),
        },
    ),
)
