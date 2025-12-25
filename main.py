import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import call_function, available_functions


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
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

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
        ),
    )
    except Exception as e:
        print(f"Error: {e}")
        return  # EXIT main() cleanly


    # Ensure usage metadata exists
    if response.usage_metadata is None:
        raise RuntimeError("Failed to retrieve token usage metadata.")

    # Verbose output
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Always print the model response
    # Output logic: function calls OR text
    function_results = []

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(
                function_call,
                verbose=args.verbose
            )

        # Safety checks (required by assignment)
        if not function_call_result.parts:
            raise RuntimeError("Function call returned no parts")

        function_response = function_call_result.parts[0].function_response
        if function_response is None:
            raise RuntimeError("Missing function response")

        if function_response.response is None:
            raise RuntimeError("Missing function response payload")

        function_results.append(function_call_result.parts[0])

        if args.verbose:
            print(f"-> {function_response.response}")
    else:
        print(response.text)



if __name__ == "__main__":
    main()
