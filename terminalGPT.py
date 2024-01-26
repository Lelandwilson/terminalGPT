#!/usr/bin/env -S poetry run python
import argparse
from colorama import Fore, Back, Style
from openai import OpenAI
import re
import os

class CodingAssistant:
    def __init__(self):
        print("<INIT>")
        # Attempt to get the API key from the environment variable
        api_key = os.getenv('OPENAI_API_KEY')

        # If the API key is not set, prompt the user to enter it
        if not api_key:
            api_key = input("Enter your OpenAI API key: ").strip()

        # Set the API key for the OpenAI client
        self.client = OpenAI(api_key=api_key)

    def format_response(self, response_text):
        # Detect code blocks and format them with colors
        code_block_pattern = r"```(.*?)```"
        formatted_text = ""
        start = 0

        for match in re.finditer(code_block_pattern, response_text, re.DOTALL):
            # Add non-code text
            formatted_text += response_text[start:match.start()]
            # Add formatted code block
            code_block = match.group(1).strip()
            print("***")
            formatted_text += f"{Back.BLACK}{Fore.GREEN}\n{code_block}\n{Style.RESET_ALL}"
            start = match.end()

        # Add any remaining non-code text
        formatted_text += response_text[start:]
        return formatted_text

    def query_gpt(self, modelInUse, user_input):
        in_code_block = False  # Flag to track if we are inside a code block

        try:
            stream = self.client.chat.completions.create(
                model=modelInUse,
                messages=[
                    {"role": "system",
                     "content": "You are an expert software engineer, you always give concise and useful answers."
                                "Assume you are talking with another expert in your field."},
                    {"role": "user", "content": user_input}
                ],
                stream=True,
            )
            for chunk in stream:
                if not chunk.choices:
                    continue

                chunk_text = chunk.choices[0].delta.content
                if chunk_text is None:
                    continue

                # Check for code block start or end
                if '``' in chunk_text:
                    in_code_block = not in_code_block
                    chunk_text = (chunk_text
                                  .replace('```', '')
                                  .replace('``', '')
                                  .replace('`', '')
                                  )

                    if in_code_block:
                        print(f"{Fore.GREEN}", end="")  # Start coloring
                    else:
                        print(f"{Style.RESET_ALL}", end="")  # End coloring

                chunk_text = (chunk_text
                              .replace('```', '')
                              .replace('``', '')
                              .replace('`', ''))

                if in_code_block:
                    print(chunk_text, end="")  # Print code block content with color
                else:
                    print(self.format_response(chunk_text), end="")  # Format non-code text

            print(Style.RESET_ALL)  # Reset style at the end
        except Exception as e:
            print(f"An error occurred [query_gpt]: {e}")

    def run(self, model):
        print(f"Coding Assistant ({model}). Type '/q' to exit.")
        while True:
            user_input = input(">>> Prompt: ")
            if user_input.lower() == '/q':
                break
            try:
                self.query_gpt(model, user_input)
            except OpenAI.error.InvalidRequestError as e:
                print(f"Model '{model}' not found. Falling back to 'gpt-4'.")
                # model = "gpt-4"
                model = "gpt-4-0125-preview"
                self.query_gpt(model, user_input)
            except Exception as e:
                print(f"An error occurred [run]: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Coding Assistant with a specified model.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-m", "--model", default="gpt-4-0125-preview",
                        help="Specify the model to use. Default is 'gpt-4-0125-preview'.\n"
                             "Available models and their details:\n"
                             "- 'gpt-4-0125-preview' (CT Window: 128,000 tokens, Training: Up to Apr 2023)\n"
                             "- 'gpt-4-turbo-preview' (CT Window: 128,000 tokens, Training: Up to Apr 2023)\n"
                             "- 'gpt-4-1106-preview' (CT Window: 128,000 tokens, Training: Up to Apr 2023)\n"
                             "- 'gpt-4' (CT Window: 8,192 tokens, Training: Up to Sep 2021)\n"
                             "- 'gpt-4-0613' (CT Window: 8,192 tokens, Training: Up to Sep 2021)\n"
                             "- 'gpt-4-32k' (CT Window: 32,768 tokens, Training: Up to Sep 2021)\n"
                             "- 'gpt-4-32k-0613' (CT Window: 32,768 tokens, Training: Up to Sep 2021)\n"
                             "- 'gpt-3.5-turbo-1106' (CT Window: 16,385 tokens, Training: Up to Sep 2021)\n"
                             "- 'gpt-3.5-turbo' (CT Window: 4,096 tokens, Training: Up to Sep 2021)")

    args = parser.parse_args()

    assistant = CodingAssistant()
    assistant.run(model=args.model)