# CLI Coding Agent

This is a CLI coding agent that works on a hardcoded project for a simple CLI calculator app. It uses the `gemini-2.0-flash-001` model and google's generative AI library.

## The model access to perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

**All of these operations are restricted within the bounds of the project's working directory (calculator folder).**

In the current implementation the agent takes a "one-shot" prompt then performs all operations (function calls) it needs and responds with the final result of those function calls.

## Possible future changes

- Make the system prompt a text file that is read in by main.py
- Add the ability to point to the working directory of a project
- Allow follow up prompts and conversation history
- Write a more robust test suite
