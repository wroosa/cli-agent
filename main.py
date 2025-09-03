import os, sys, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    # Store messages
    messages = [
        types.Content(role="user", parts=[types.Part(text=(args.prompt + limiter))])
    ]

    if args.verbose: print(f'User prompt: {args.prompt}')

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
        )
    
    print(response.text)
    if args.verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    


if __name__ == "__main__":
    main()
