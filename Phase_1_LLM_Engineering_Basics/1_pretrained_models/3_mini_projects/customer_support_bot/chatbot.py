"""
=====================================================
      Customer Support Chatbot - OpenAI API
=====================================================

A professional, AI-powered customer support chatbot that classifies
user queries into categories like 'billing', 'technical', or 'general'
and provides context-aware responses.

Requirements:
-------------
1. Python 3.10+
2. Install OpenAI Python library:
   pip install openai
3. Set your OpenAI API key as an environment variable:
   Linux/macOS:
       export OPENAI_API_KEY="your_api_key_here"
   Windows (Command Prompt):
       setx OPENAI_API_KEY "your_api_key_here"

Usage:
------
Run the script and interact with the chatbot in the terminal.
Type 'exit' to quit.

Example:
--------
Enter Prompt: I forgot my password and can't log in
AI Response:
Category: Technical
Answer: "It seems like you are having a login issue. Please try resetting
your password using the 'Forgot Password' option. If the problem persists,
contact our support team."
"""

import os
from openai import OpenAI
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class Chatbot:
    """
    Professional AI-powered Chatbot using OpenAI API.

    Attributes
    ----------
    model_name : str
        Name of the OpenAI model (default: "gpt-4o-mini")
    client : OpenAI
        OpenAI API client
    system_instructions : str
        Instructions for the AI system prompt

    Methods
    -------
    get_ai_response(query: str) -> str
        Sends a query to the AI and returns the response
    """

    def __init__(self, model_name: str = "gpt-4o-mini", *, system_instructions: str):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "ERROR: OPENAI_API_KEY not found. "
                "Please set your API key in environment variables."
            )

        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.system_instructions = system_instructions

    def get_ai_response(self, query: str) -> str:
        """
        Send a user query to the OpenAI API and return the AI's response.

        Parameters
        ----------
        query : str
            The user's query

        Returns
        -------
        str
            AI-generated response
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_instructions},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content


def main():
    # System instructions for AI
    system_instructions = """
    You are a professional customer support assistant.
    Analyze the user's query and categorize it as 'billing', 'technical',
    or 'general'. Provide a concise and helpful response.
    """

    # Initialize chatbot
    bot = Chatbot(model_name="gpt-4o-mini", system_instructions=system_instructions)

    print(Fore.CYAN + "="*60)
    print(Fore.CYAN + "        Welcome to the Customer Support Chatbot")
    print(Fore.CYAN + "="*60)
    print(Fore.YELLOW + "Type your query below. Enter 'exit' to quit.\n")

    while True:
        user_input = input(Fore.GREEN + "You: " + Style.RESET_ALL)
        if user_input.strip().lower() == "exit":
            print(Fore.MAGENTA + "\nThank you for using the Customer Support Chatbot! Goodbye!")
            break

        print(Fore.BLUE + "\nProcessing your request...\n" + Style.RESET_ALL)
        ai_response = bot.get_ai_response(user_input)

        print(Fore.CYAN + "-"*60)
        print(Fore.CYAN + "AI Response:\n")
        print(Fore.WHITE + ai_response)
        print(Fore.CYAN + "-"*60 + "\n")


if __name__ == "__main__":
    main()