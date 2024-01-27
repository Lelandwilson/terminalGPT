#!/usr/bin/env -S poetry run python
import argparse
from colorama import Fore, Back, Style, init
import shutil
from openai import OpenAI
import re
import os
import tiktoken

# Initialize Colorama
init()


class ConversationHistory:
    def __init__(self, token_limit, assistant):
        self.history = []
        self.token_limit = token_limit
        self.assistant = assistant  # Reference to the CodingAssistant instance

    def clear_history(self):
        self.history = []

    def print_formatted_history(self):
        # Combine and format the history for display
        formatted_history = ""
        for interaction in self.history:
            user_text = interaction["user"]
            model_text = interaction["model"]
            formatted_history += f"User: {self.assistant.format_response(user_text)}\n"
            formatted_history += f"Model: {self.assistant.format_response(model_text)}\n"
        return formatted_history
    def add_interaction(self, user_query, model_response):
        self.history.append({"user": user_query, "model": model_response})
        self._truncate_history()

    def _truncate_history(self):
        # Truncate the oldest interactions if the token limit is exceeded
        while self._calculate_total_tokens() > self.token_limit:
            self.history.pop(0)

    def _calculate_total_tokens(self):
        # Use the count_tokens method from the CodingAssistant instance
        total_tokens = sum(self.assistant.count_tokens(interaction["user"], self.assistant.model) +
                           self.assistant.count_tokens(interaction["model"], self.assistant.model)
                           for interaction in self.history)
        return total_tokens

    def get_current_context(self):
        # Combine the history into a single string to be used as context
        context = ""
        for interaction in self.history:
            context += f"User: {interaction['user']}\nModel: {interaction['model']}\n"
        return context


class CodingAssistant:
    def __init__(self, model, temperature, response_color, background_color, show_context_usage):

        print("<INIT>")

        # Token limits for different models
        token_limits = {
            'gpt-4-0125-preview': 128000,
            'gpt-4-turbo-preview': 128000,
            'gpt-4-1106-preview': 128000,
            'gpt-4': 8192,
            'gpt-4-0613': 8192,
            'gpt-4-32k': 32768,
            'gpt-4-32k-0613': 32768,
            'gpt-3.5-turbo-1106': 16385,
            'gpt-3.5-turbo': 4096,
            'gpt-3.5-turbo-16k': 16385,
            'gpt-3.5-turbo-instruct': 4096,
            'gpt-3.5-turbo-0613': 4096,
            'gpt-3.5-turbo-16k-0613': 16385,
            'gpt-3.5-turbo-0301': 4096
        }

        # Attempt to get the API key from the environment variable
        api_key = os.getenv('OPENAI_API_KEY')

        # If the API key is not set, prompt the user to enter it
        if not api_key:
            api_key = input("Enter your OpenAI API key: ").strip()

        # Set the API key for the OpenAI client
        self.client = OpenAI(api_key=api_key)

        self.model = model
        self.temperature = temperature
        self.response_color = response_color
        self.background_color = background_color
        self.show_context_usage = show_context_usage
        self.token_limit = token_limits.get(model, 4096)  # Default to 4,096 tokens if the model is not listed

        # Initialize the conversation history object
        self.conversation_history = ConversationHistory(self.token_limit, self)

    def count_tokens(self, text, model):
        """
        Count the number of tokens in a text string for a given model.
        """
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))

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
            formatted_text += f"{self.background_color}{self.response_color}\n{code_block}\n{Style.RESET_ALL}"
            start = match.end()

        # Add any remaining non-code text
        formatted_text += response_text[start:]
        return formatted_text

    def query_gpt(self, modelInUse, max_response_tokens, user_input):
        in_code_block = False  # Flag to track if we are inside a code block
        model_response = ""  # Initialize model_response

        try:
            # Count the number of prompt tokens
            prompt_tokens = self.count_tokens(user_input, modelInUse)

            # Prepare the request to the OpenAI API
            # Retrieve the current context
            current_context = self.conversation_history.get_current_context()

            # Include the current context in the API request
            stream = self.client.chat.completions.create(
                model=modelInUse,
                messages=[
                    {"role": "system", "content": current_context},
                    {"role": "user", "content": user_input}
                ],
                temperature=self.temperature,
                max_tokens=max_response_tokens,  # Use the max_response_tokens parameter
                logprobs=None,  # This is optional for token-level information
                stream=True,
            )
            completion_tokens = 0  # Initialize completion token count

            # Process each chunk received from the API
            for chunk in stream:
                if not chunk.choices:
                    continue

                chunk_text = chunk.choices[0].delta.content
                if chunk_text is None:
                    continue

                # Count tokens in this chunk and add to completion_tokens
                completion_tokens += self.count_tokens(chunk_text, modelInUse)

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

                model_response += chunk_text  # Append the chunk to the model response

            # Update conversation history with the new interaction after processing all chunks
            self.conversation_history.add_interaction(user_input, model_response)

            # Display context usage after processing the entire response
            self.display_context_usage(prompt_tokens, completion_tokens)
            print(Style.RESET_ALL)  # Reset style at the end

        except Exception as e:
            print(f"An error occurred [query_gpt]: {e}")

    def display_context_usage(self, prompt_tokens, completion_tokens):
        if self.show_context_usage:
            total_tokens = prompt_tokens + completion_tokens
            usage_percent = (total_tokens / self.token_limit) * 100
            term_width = shutil.get_terminal_size((80, 20)).columns
            usage_str = f"Context Usage: {usage_percent:.2f}%"
            print(f"{Fore.RED}{'':>{term_width - len(usage_str)}}{usage_str}{Style.RESET_ALL}")

    def run(self, model, max_response_tokens):
        print(f"Coding Assistant ({model}). Type '/q' to exit, '/c' to clear history,"
              f" '/pct' to print conversation context.")
        while True:
            user_input = input(">>> Prompt: ")
            if user_input.lower() == '/q':
                break
            elif user_input.lower() == '/c':
                self.conversation_history.clear_history()
                print("Conversation history cleared.")
                continue
            elif user_input.lower() == '/pct':
                print(self.conversation_history.print_formatted_history())
                continue

            try:
                self.query_gpt(model, max_response_tokens, user_input)
            except OpenAI.error.InvalidRequestError as e:
                print(f"Model '{model}' not found. Falling back to 'gpt-4'.")
                # model = "gpt-4"
                model = "gpt-4-0125-preview"
                self.query_gpt(model, max_response_tokens, user_input)
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

    parser.add_argument("-mrt", "--max_response_tokens", type=int, default=1000, help="Set the maximum response token limit.")
    parser.add_argument("-t", "--temperature", type=float, default=0.2, help="Set the response temperature.")
    parser.add_argument("-c", "--color", default=Fore.GREEN, help="Set the response text color.")
    parser.add_argument("-bc", "--background-color", default=Back.RESET, help="Set the response background color.")
    parser.add_argument("-cc", "--context-usage", type=bool, default=True, help="Toggle context usage display.")

    args = parser.parse_args()

    assistant = CodingAssistant(args.model, args.temperature, args.color, args.background_color, args.context_usage)
    assistant.run(model=args.model, max_response_tokens=args.max_response_tokens)
