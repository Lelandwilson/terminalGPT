
# Coding Assistant

## Description

Coding Assistant is a Python-based terminal application that facilitates conversations with the OpenAI GPT-4 API. Designed to act as an expert software engineering assistant, it provides concise and useful answers. The application supports custom AI models and features special formatting for code blocks in the terminal.

## Features

- Interactive chat with OpenAI's GPT-4 model.
- Special formatting for code blocks.
- Customizable AI model via command-line arguments.
- Secure handling of the OpenAI API key.

## Installation

### Prerequisites

- Python 3
- Access to OpenAI API (API key)

### Setup

1. **Clone the Repository**:
   ```
   git clone https://github.com/Lelandwilson/terminalGPT/tree/main
   ```
   
2. **Navigate to the Project Directory**:
   ```
   cd terminalGPT
   ```
   
3. **Install Dependencies**:
   Install the required Python packages using:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

Execute the application with the following command:
```
python terminalGPT.py
```
To specify a different AI model, use the `-m` option:
```
python terminalGPT.py -m [model-name]
```
## Current chatGPT models:
For an up to dat elist of models available see:
https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo

| MODEL                | DESCRIPTION | CONTEXT WINDOW | TRAINING DATA |
|----------------------|-------------|----------------|---------------|
| gpt-4-0125-preview   | New GPT-4 Turbo: The latest GPT-4 model intended to reduce cases of “laziness” where the model doesn’t complete a task. [Learn more](#). | 128,000 tokens | Up to Apr 2023 |
| gpt-4-turbo-preview  | Currently points to gpt-4-0125-preview. | 128,000 tokens | Up to Apr 2023 |
| gpt-4-1106-preview   | GPT-4 Turbo model featuring improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens. This preview model is not yet suited for production traffic. [Learn more](#). | 128,000 tokens | Up to Apr 2023 |
| gpt-4                | Currently points to gpt-4-0613. [See continuous model upgrades](#). | 8,192 tokens | Up to Sep 2021 |
| gpt-4-0613           | Snapshot of gpt-4 from June 13th 2023 with improved function calling support. | 8,192 tokens | Up to Sep 2021 |
| gpt-4-32k            | Currently points to gpt-4-32k-0613. [See continuous model upgrades](#). This model was never rolled out widely in favor of GPT-4 Turbo. | 32,768 tokens | Up to Sep 2021 |
| gpt-4-32k-0613       | Snapshot of gpt-4-32k from June 13th 2023 with improved function calling support. This model was never rolled out widely in favor of GPT-4 Turbo. | 32,768 tokens | Up to Sep 2021 |



### API Key Configuration

The application requires an OpenAI API key. You can provide this key in two ways:

1. **Environment Variable**:
   Set the `OPENAI_API_KEY` environment variable in your terminal or shell configuration file. Example:
   ```
   export OPENAI_API_KEY='your_api_key_here'
   ```

2. **Manual Input**:
   If the environment variable is not set, the application will prompt you to enter the API key manually upon startup.

### Exiting the Application

Type `/q` and press Enter to exit the application.

## Support

For any issues or questions, please open an issue in the GitHub repository.

## License

Apache
