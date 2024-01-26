# Coding Assistant
## Description
Coding Assistant is a Python-based terminal application designed to facilitate conversations with the OpenAI GPT-4 API. It acts as an expert software engineering assistant, providing concise and useful answers. The application supports customization of the AI model and handles streamed responses with special formatting for code blocks.

## Features
Interactive chat with OpenAI's GPT-4 model.
Special formatting for code blocks in terminal.
Customizable AI model through command-line arguments.
Handles API key securely via environment variables or manual input.

## Installation

## Prerequisites
Python 3
openai Python package
colorama Python package
Setup
Clone the repository:
bash

git clone [repository-url]
Navigate to the project directory:
bash

cd [project-directory]
Install dependencies:
pip install openai colorama
Usage
Running the Application
Execute the application with the following command:

python coding_assistant.py
Optionally, specify the AI model:

python coding_assistant.py -m [model-name]

## API Key Configuration
The application requires an OpenAI API key. There are two ways to provide this key:

Environment Variable (Recommended):
Set the OPENAI_API_KEY environment variable with your key. This can be done in your terminal session or shell configuration file. For example:

export OPENAI_API_KEY='your_api_key_here'
Manual Input:
If the environment variable is not set, the application will prompt you to enter the API key manually when it starts.

## Exiting the Application
Type /q and press Enter to quit the application.

## Support
If you encounter any issues or have questions, please file an issue in the GitHub repository.

License
