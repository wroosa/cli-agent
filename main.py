import os, sys, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():

    # Argument parsing and error logic
    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write(f"Error: {message}\n\n")
            self.print_help()
            sys.exit(1)   # change to exit code 1

    parser = MyParser(description="CLI coding agent")
    parser.add_argument("prompt", help="the prompt you wish to send to the agent")
    parser.add_argument("--verbose", "-v", action="store_true")

    
    args = parser.parse_args()
    limiter = '(Limit your response to one paragraph)'

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    # Add all available function schemas as a Tool
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_get_file_content,
            schema_run_python_file
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt
    )
     
    # Store messages
    messages = [
        types.Content(role="user", parts=[types.Part(text=(args.prompt + limiter))])
    ]

    # Print response
    if args.verbose: print(f'User prompt: {args.prompt}')

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages, config=config
        )
    if response.function_calls is not None:
        for call in response.function_calls:
           print( f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)

    if args.verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    


if __name__ == "__main__":
    main()
