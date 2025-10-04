"""
Title: ChatMessageHistory-Based Conversational Memory System
Author: Himanshu Singh
Description:
    This script demonstrates how to manually manage conversational memory using 
    LangChain's `ChatMessageHistory` and integrate it with a Google Gemini LLM 
    (via `langchain_google_genai`).

    It simulates an AI chatbot that remembers past interactions by explicitly 
    passing stored messages to the model each time a new query is made.

Core Concepts:
    - `ChatMessageHistory`: Stores messages between the user and AI.
    - Manual Memory Injection: Passes conversation history into the prompt manually.
    - Context Retention: Maintains continuity between user queries.

LangChain's Equivalent Automation:
    - This approach conceptually replicates what `ConversationBufferMemory` does 
      automatically inside a LangChain `LLMChain`.

Disadvantages of Manual Memory Management:
    1. Manual Overhead - Each user and AI message must be explicitly added to 
       `ChatMessageHistory` by the developer, which increases boilerplate code.
    2. Context Window Limitation - The entire message history is re-passed to 
       the model at every turn. As the chat grows longer, token usage rises, which 
       can exceed the model's context window and increase API costs.
    3. Lack of Summarization - The model receives raw chat logs rather than a 
       summarized context. This can make reasoning less efficient compared to 
       using `ConversationSummaryMemory`.
    4. No Long-Term Persistence - Once the program ends, the chat history is 
       lost unless explicitly saved to an external storage or vector database.

Requirements:
    - Python 3.10+
    - `langchain_core`
    - `langchain_community`
    - `langchain_google_genai`
    - A valid Google Gemini API key stored in your environment as "GOOGLE_API_KEY".

Usage:
    Run the script and interact with the chatbot in the terminal.
    Type 'quit' or 'Quit' to exit the conversation.

Example Output:
    ----------------- AI Chatbot -----------------
    Enter 'quit' or 'Quit' for Quitting the AI-Chatbot
    User: What is my name?
    Agent: Your name is Himanshu Singh.
===============================================================================
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import os
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# -----------------------------------------------------------------------------
# Function: Initialize the LLM
# -----------------------------------------------------------------------------
def initialize_llm(api_key_env: str = "GOOGLE_API_KEY") -> GoogleGenerativeAI:
    """
    Initializes a Google Gemini LLM using an API key from environment variables.

    Parameters:
        api_key_env (str): The environment variable name containing the API key.
                           Defaults to "GOOGLE_API_KEY".

    Returns:
        GoogleGenerativeAI: A configured Gemini LLM instance.

    Raises:
        ValueError: If the API key is not found in environment variables.
    """
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise ValueError(f"API key not found in environment variable '{api_key_env}'")

    return GoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key
    )

# -----------------------------------------------------------------------------
# Section 1: Initialize Conversation History
# -----------------------------------------------------------------------------
# ChatMessageHistory acts as a manual message tracker.
# Every user or AI message is appended to this object.
history = ChatMessageHistory()

# Preload initial conversation context
history.add_user_message("I'm heading to New York next week.")
history.add_ai_message("Great! It's a fantastic city.")
history.add_user_message("My name is Himanshu Singh.")
history.add_ai_message("Hello, Himanshu!")
history.add_user_message("What is my name?")
history.add_ai_message("Your name is Himanshu Singh.")

# Print stored messages (for reference)
print("Initial Chat History:")
print(history.messages)
print("-" * 80)

# -----------------------------------------------------------------------------
# Section 2: Define Prompt Template and Response Pipeline
# -----------------------------------------------------------------------------
# The pipeline connects: Prompt → LLM → Output Parser
llm_pipeline = (
    ChatPromptTemplate([
        (
            "user",
            "This is the conversation history between the AI and the user. "
            "Use it only for context.\n\nPrevious Chat: {conversation}\n\n"
            "Question for you: {user_query}"
        )
    ])
    | initialize_llm()
    | StrOutputParser()
)

# -----------------------------------------------------------------------------
# Section 3: Start Chatbot Loop
# -----------------------------------------------------------------------------
def start_chatbot():
    """
    Launches an interactive chatbot session.
    
    The chatbot uses stored conversation history to maintain context manually.
    Each user query and AI response is added to `ChatMessageHistory`.
    """
    print("\n----------------- AI Chatbot -----------------")
    print("Enter 'quit' or 'Quit' to exit the chatbot.\n")

    while True:
        # Get user input
        user_input = input("User: ").strip()

        # Exit condition
        if user_input.lower() == "quit":
            print("\nAgent: Okay, you've entered 'quit'.")
            print("It was nice chatting with you! Exiting chatbot...")
            break

        # Generate AI response using current conversation history
        agent_response = llm_pipeline.invoke({
            "conversation": history.messages,
            "user_query": user_input
        })

        # Display the AI response
        print(f"Agent: {agent_response}\n")

        # Update conversation history
        history.add_user_message(user_input)
        history.add_ai_message(agent_response)

        print("----------------- AI Chatbot -----------------")

# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    start_chatbot()