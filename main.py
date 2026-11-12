import os
import json
import argparse

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY not found. Please check your .env file.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def main():
    parser = argparse.ArgumentParser(description="AI Coding Agent")
    
    parser.add_argument(
        "user_prompt",
        type=str,
        help="The prompt to send to the AI model"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
 
    messages = [
        {"role": "system", "content": system_prompt},       
        {"role": "user","content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    print(f"Model used: {response.model}")        

    if response.usage is None:
        raise RuntimeError("Token usage information is missing from the API response.")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

        print(f"Prompt tokens: {response.usage.prompt_tokens}")

        print(f"Response tokens: {response.usage.completion_tokens}")

        print("Response:")
    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        print(message.content)

if __name__ == "__main__":
    main()
