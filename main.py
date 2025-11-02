import os  # os to explore the root directory
from dotenv import load_dotenv  # dotenv to import en env variables
from google import genai  # import the google library for Ai
import sys  # importing sys to use command line for prompt

load_dotenv()  # loading the env variables
api_key = os.environ.get(
    "GEMINI_API_KEY"
)  # getting the api-key with os from env variables
client = genai.Client(
    api_key=api_key
)  # assing the client with the api key for response


def main():
    # using the command line to ask for a user prompt
    if len(sys.argv) != 2:
        print("Usage: uv run main.py <prompt>")
        sys.exit(1)
    else:
        usr_prompt = sys.argv[1]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=f"{usr_prompt}"
    )  # contents of the prompt and model use

    print(response.text)  # printing the generate_content
    print(
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
    )  # prompt_token_count
    print(
        f"Response tokens: {response.usage_metadata.candidates_token_count}"
    )  # response_token_count


if __name__ == "__main__":
    main()
