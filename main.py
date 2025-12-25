import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Please set it in your .env file."
        )

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # Create conversation messages
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    # Generate response using conversation history
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )

    # Ensure usage metadata exists
    if response.usage_metadata is None:
        raise RuntimeError("Failed to retrieve token usage metadata.")

    # Print token usage
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Print model response
    print(response.text)


if __name__ == "__main__":
    main()
