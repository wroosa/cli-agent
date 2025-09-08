from google.genai import types
from get_file_content import get_file_content
from get_files_info import get_files_info
from run_python_file import run_python_file
from write_file import write_file

functions = {
    "get_file_content": get_file_content,
    "get_file_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose: 
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    selected_function = functions.get(function_name)

    if selected_function == None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    function_result = selected_function('calculator/', **function_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

# Test function call object
# call_object = types.FunctionCall(
#     name='get_file_content',
#     args={
#         "file_path": "pkg/render.py"
#         }
#     ) 

