"""
===============================================================================
Title: AI Chatbot with ConversationSummaryMemory
Author: Himanshu Singh
Description:
    This script demonstrates how to use LangChain's `ConversationSummaryMemory`
    to create an intelligent chatbot capable of remembering past conversations
    by summarizing older interactions automatically.

    Unlike manual message tracking (using ChatMessageHistory),
    this approach automatically compresses older context using a language model.

Core Concepts:
    - ConversationSummaryMemory: Stores a summarized version of previous dialogue.
    - Memory Integration: Automatically injects summaries into LLM prompts.
    - Context Retention: Maintains continuity without overloading the context window.

Requirements:
    - Python 3.10+
    - langchain
    - langchain_google_genai
    - A valid Google Gemini API key in environment variable "GOOGLE_API_KEY".
===============================================================================
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain


# -----------------------------------------------------------------------------
# Function: Initialize the LLM
# -----------------------------------------------------------------------------
def initialize_llm(api_key_env: str = "GOOGLE_API_KEY") -> GoogleGenerativeAI:
    """
    Initializes the Google Gemini LLM using an API key from environment variables.
    """
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise ValueError(f"API key not found in environment variable '{api_key_env}'")

    return GoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)


# -----------------------------------------------------------------------------
# Section 1: Initialize Memory and LLM Chain
# -----------------------------------------------------------------------------
# ConversationSummaryMemory automatically summarizes older messages.
llm = initialize_llm()
memory = ConversationSummaryMemory(llm=llm)

# ConversationChain ties together LLM + Memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True   # Set to True to view internal prompt construction
)


# -----------------------------------------------------------------------------
# Section 2: Interactive Chatbot Loop
# -----------------------------------------------------------------------------
def start_chatbot():
    """
    Launches an interactive chatbot using ConversationSummaryMemory.
    The chatbot remembers key information through summarized memory.
    """
    print("\n----------------- AI Chatbot with Summarized Memory -----------------")
    print("Type 'quit' or 'exit' to end the chat.\n")

    while True:
        user_input = input("User: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("Exiting chat... Goodbye!")
            break

        response = conversation.predict(input=user_input)
        print(f"Agent: {response}\n")


# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    start_chatbot()
