import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

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
    
    args = parser.parse_args()

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ],
    )

    if response.usage is None:
        raise RuntimeError("Token usage information is missing from the API response.")

    print(f"User prompt: {args.user_prompt}")

    print(f"Prompt tokens: {response.usage.prompt_tokens}")

    print(f"Response tokens: {response.usage.completion_tokens}")

    print("Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
