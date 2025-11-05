import os
from re import VERBOSE  # os to explore the root directory
from dotenv import load_dotenv  # dotenv to import en env variables
from google import genai  # import the google library for Ai
import sys  # importing sys to use command line for prompt
from google.genai import types
from enum import Enum
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from system_prompt_config import system_prompt

load_dotenv()  # loading the env variables
api_key = os.environ.get(
    "GEMINI_API_KEY"
)  # getting the api-key with os from env variables
client = genai.Client(
    api_key=api_key
)  # assing the client with the api key for response


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content,
    ]
)


class options(Enum):
    no_verbose = 2
    with_verbose = 3


def message(usr_prompt):
    messages = [types.Content(role="user", parts=[types.Part(text=usr_prompt)])]
    return messages


def response_from_ia(messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    return response


def main():
    usr_prompt = sys.argv[1]
    message_roles = message(usr_prompt)
    response = response_from_ia(message_roles)

    # using the command line to ask for a user prompt
    match len(sys.argv):
        case options.no_verbose.value:
            if response.function_calls:
                for item in response.function_calls:
                    print(f"Calling function: {item.name}({item.args})")
            else:
                print(response.text)

        case options.with_verbose.value if sys.argv[2] == "--verbose":
            response = response_from_ia(message(sys.argv[1]))
            if response.function_calls:
                for item in response.function_calls:
                    print(f"Calling function: {item.name}({item.args})")
            else:
                print(f"User prompt:\n {usr_prompt}\n")
                print(f"gemini-2 response:\n {response.text}")
                print(
                    f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
                )  # prompt_token_count
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )  # response_token_count

        case _:
            print(
                "Usage of the tool: uv run main.py <'usr_prompt'> [optional: --verbose]"
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
