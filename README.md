
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
python coding_assistant.py
```
To specify a different AI model, use the `-m` option:
```
python coding_assistant.py -m [model-name]
```

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
