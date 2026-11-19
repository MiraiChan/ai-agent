# AI Coding Agent

A command-line coding agent that uses OpenRouter to inspect and modify the included calculator project. It sends a prompt to a model, executes the model's tool calls, and returns the final response.

## Requirements

- Python 3.14 or later
- An [OpenRouter](https://openrouter.ai/) API key
- [uv](https://docs.astral.sh/uv/) for the commands below

## Setup

From the project root, install the dependencies:

```sh
uv sync
```

Create a `.env` file in the project root:

```dotenv
OPENROUTER_API_KEY=your_api_key_here
```

The `.env` file is ignored by Git. You can also set the variable in your shell.

## Usage

Run the agent from the project root, passing the request as a single argument:

```sh
uv run python main.py "Explain how the calculator evaluates expressions"
```

Add `--verbose` to see token usage, tool arguments, and tool results:

```sh
uv run python main.py "Run the calculator tests" --verbose
```

The agent uses the `openrouter/free` model and allows up to 20 model iterations per request. It can list directories, read files, run Python files with arguments, and create or overwrite files. Reads are limited to 10,000 characters, and Python executions time out after 30 seconds.

Tool paths are relative to `./calculator`, which is hard-coded in `call_function.py`; run the agent from the project root so that it resolves correctly. The agent can overwrite files and execute code without asking for confirmation. Its path checks do not provide a secure sandbox (for example, symbolic links and executed Python code can reach outside the directory), so use it only with trusted prompts and code in an appropriate environment.

## Project structure

- `main.py` — CLI and model/tool-calling loop
- `prompts.py` — agent system prompt
- `call_function.py` — tool definitions and dispatch
- `functions/` — file listing, reading, writing, and Python execution tools
- `calculator/` — sample project the agent operates on
- `test_*.py` — standalone scripts for exercising the tools

To run the calculator's own tests:

```sh
uv run python calculator/tests.py
```

The root-level `test_*.py` files are manual scripts that print results rather than an automated assertion suite. In particular, `test_write_file.py` overwrites files in `calculator/`.
