"""
=====================================================
Educational Example: Using OpenAI Chat Completions API
=====================================================

This script demonstrates how to interact with the OpenAI API 
using the official Python client library (`openai`).

What it does:
-------------
- Initializes an OpenAI client.
- Sends a prompt to the Chat Completions API.
- Receives and prints the response in a user-friendly format.

Requirements:
-------------
1. Install the OpenAI Python library:
   pip install openai

2. Set your OpenAI API key as an environment variable:
   For Linux/macOS:
       export OPENAI_API_KEY="your_api_key_here"
   For Windows (Command Prompt):
       setx OPENAI_API_KEY "your_api_key_here"

3. Replace the model name with any supported model if needed.
   Example: "gpt-4o-mini", "gpt-4.1", etc.

Example Output:
---------------
When running this script, you may see output like:

    Neural Networks are computer systems inspired by how the human brain works.
    They consist of layers of "neurons" that process data and learn patterns 
    from it. This makes them useful for tasks like image recognition, 
    language translation, and more.

Notes:
------
- The model choice (`gpt-4o-mini`) is lightweight and good for 
  quick educational examples.
- Modify the `system_message` and `user_message` variables 
  to experiment with different contexts or queries.

"""

from openai import OpenAI

def get_ai_response(system_message: str, user_message: str, model_name: str = "gpt-4o-mini") -> str:
    """
    Generate a response from the OpenAI Chat Completions API.

    Parameters
    ----------
    system_message : str
        Instruction for the AI assistant that defines its role or behavior.
        Example: "You are a helpful tutor for Machine Learning."
    user_message : str
        The actual query or request from the user.
        Example: "Explain Neural Networks in Simple."
    model_name : str, optional
        The OpenAI model to use. Defaults to "gpt-4o-mini".
        You may replace this with another model (e.g., "gpt-4.1")
        depending on your subscription and availability.

    Returns
    -------
    str
        The text content of the AI’s response.

    Example
    -------
    >>> response = get_ai_response(
    ...     system_message="You are a helpful tutor for Machine Learning",
    ...     user_message="Explain Neural Networks in Simple"
    ... )
    >>> print(response)
    "Neural Networks are computer systems inspired by the human brain..."
    """
    # Initialize the client (automatically uses the API key from environment variable)
    client = OpenAI()

    # Send messages to the Chat Completions API
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )

    # Extract and return the assistant's reply text
    return response.choices[0].message["content"]


if __name__ == "__main__":
    # Define role and query
    system_instruction = "You are a helpful tutor for Machine Learning"
    user_query = "Explain Neural Networks in Simple"

    # Fetch AI response
    ai_reply = get_ai_response(system_instruction, user_query)

    # Print the result in a clean format
    print("\nAI Response:\n" + "-" * 40)
    print(ai_reply)