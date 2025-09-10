import os, sys, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

MAX_ITERATIONS = 20

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

    parser.add_argument(
        "prompt", 
        help="the prompt you wish to send to the agent", 
    )
    parser.add_argument(
        "--verbose", 
        "-v", 
        action="store_true"
    )

    
    args = parser.parse_args()

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

        Be proactiving in using your available tools (function calls) without prompting the user for more information. When you need information about files or code, use your available functions to explore and gather the necessary information. 
        
        You are working in a project directory that contains code files. Always start by calling functions to explore the directory structure and files when you need to understand the codebase and always do this before writing any files or making changes. If you're unsure about file locations or project structure, begin by listing the files and directories to understand what is available. Do not ask the user before writing a new file or writing to a file but still make sure to understand the project directory before writing anything.

        When making function calls, do not include additional explanatory text in your response. Only provide text responses when you have completed all necessary function calls and are ready to give your final answer.
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
        types.Content(role="user", parts=[types.Part(text=args.prompt)])
    ]

    # Print response
    if args.verbose: print(f'User prompt: {args.prompt}')

    working = True
    iterations = 0
    # Thought Loop
    while working and iterations < MAX_ITERATIONS:

        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents=messages, config=config
            )
        iterations +=1
        
        for candidate in response.candidates:
            messages.append(candidate.content)
        
        if response.function_calls is not None:

            for function in response.function_calls:
                function_call_result = call_function(function, args.verbose)
            
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Error: Fatal - No function response")
                elif args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                messages.append(
                    types.Content(role="user", parts=function_call_result.parts)
                )
        else:
            working = False
            print(response.text)

        if args.verbose:
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    


if __name__ == "__main__":
    main()


