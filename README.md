# AI Agent with Tool Integration

A powerful, Python-based AI agent that leverages Google's Gemini API to interact with the file system and execute code. This agent is designed to be extensible, secure, and capable of performing complex tasks through autonomous tool calling.

## 🚀 Features

- **Autonomous Tool Calling**: Automatically decides when to use tools based on user prompts.
- **File System Interaction**:
  - List files and directories within a safe working directory.
  - Read file contents with safety truncation.
  - Write or overwrite files with automatic directory creation.
- **Python Code Execution**: Run Python scripts with optional arguments and capture output.
- **Security First**: All operations are restricted to a defined working directory to prevent unauthorized access.
- **Robust Error Handling**: Gracefully handles API rate limits and execution errors.

## 🛠️ Tech Stack

- **Core**: Python 3.12+
- **LLM**: Google Gemini (via `google-genai`)
- **Dependency Management**: `uv` (preferred) or `pip`
- **Environment**: `python-dotenv`

## 📋 Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [Gemini API Key](https://aistudio.google.com/app/apikey)
- [uv](https://github.com/astral-sh/uv) (recommended)

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. **Set up virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   # OR
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## 📖 Usage

Run the agent via the CLI with a prompt:

```bash
uv run main.py "what files are in the root directory?"
```

### Examples

- **List files**: `uv run main.py "list files in calculator directory"`
- **Read file**: `uv run main.py "read main.py"`
- **Execute code**: `uv run main.py "run the calculator tests"`
- **Write file**: `uv run main.py "create a file named hello.txt with content 'Hello World'"`

## 📂 Project Structure

- `main.py`: Entry point for the AI agent.
- `call_function.py`: Orchestrates function calling logic and tool mapping.
- `functions/`: Contains individual tool implementations.
- `prompts.py`: Defines the system instructions for the agent.
- `calculator/`: Example workspace for tool testing and demonstration.
- `tests/`: Automated test suite for all agent capabilities.

## 🧪 Testing

Run the included test scripts to verify functionality:

```bash
./.venv/bin/python test_get_files_info.py
./.venv/bin/python test_get_file_content.py
./.venv/bin/python test_write_file.py
./.venv/bin/python test_run_python_file.py
./.venv/bin/python calculator/tests.py
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
