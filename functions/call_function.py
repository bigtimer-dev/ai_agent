from os import name
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    if not verbose:
        print(f" - Calling function: {function_call_part.name}")

    dict_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    name_of_function_call = function_call_part.name
    kwargs_dict = dict(function_call_part.args)
    kwargs_dict["working_directory"] = "./calculator"

    if name_of_function_call not in dict_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name_of_function_call,
                    response={"error": f"Unknown function: {name_of_function_call}"},
                )
            ],
        )

    result = dict_functions[name_of_function_call](**kwargs_dict)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name_of_function_call,
                response={"result": result},
            )
        ],
    )
