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

    MAX_ITERATIONS = 20

    try:
        for _ in range(MAX_ITERATIONS):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
                ),
            )

            # Add all model candidates to the conversation
            finished = False
            for candidate in response.candidates:
                messages.append(candidate.content)

            # If no function calls AND text exists → done
            if not response.function_calls and response.text:
                print("Final response:")
                print(response.text)
                finished = True

            if finished:
                break

            # Handle tool calls
            function_results = []

            if response.function_calls:
                for function_call in response.function_calls:
                    function_call_result = call_function(
                        function_call,
                        verbose=args.verbose
                    )

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

            # Add tool results back into the conversation
            if function_results:
                messages.append(
                    types.Content(
                        role="user",
                        parts=function_results,
                    )
                )

        else:
            print("Error: Reached maximum number of iterations without finishing.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
