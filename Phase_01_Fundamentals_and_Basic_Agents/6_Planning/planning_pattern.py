"""
Planner and Writer Agent using LangChain and Google Gemini

This script demonstrates how to create a LangChain agent capable of:
1. Researching a topic and generating concise bullet points.
2. Writing a coherent ~200-word article based on the research.

The agent uses:
- GoogleGenerativeAI (Gemini 2.5 Flash) as the LLM.
- LangChain tools to modularize tasks (researching and writing).

Requirements:
- Python 3.10+
- langchain-core
- langchain-google-genai
- Google Gemini API key stored in environment variable 'GOOGLE_API_KEY'

Example:
    $ export GOOGLE_API_KEY="your_key_here"
    $ python planner_writer_agent.py

The agent will output a ~200-word article on the specified topic.
"""

import os
from langchain.prompts import StringPromptTemplate
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import GoogleGenerativeAI
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# -------------------------
# 1. Initialize the LLM
# -------------------------
def build_llm() -> GoogleGenerativeAI:
    """
    Initializes the Google Gemini LLM.

    Returns:
        GoogleGenerativeAI: Configured LLM instance.
    """
    return GoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

# Initialize the LLM
llm_instance = build_llm()

# -------------------------
# 2. Define Tools
# -------------------------

@tool
def researcher(topic: str) -> StrOutputParser:
    """
    Generate 5 concise research bullet points for a given topic.

    Args:
        topic (str): The topic to research.

    Returns:
        StrOutputParser: Parsed output containing 5 bullet points.

    Example:
        notes = researcher("Reinforcement Learning")
        print(notes)
    """
    prompt = ChatPromptTemplate([
        ("system", """
            You are an AI Researcher. Provide 5 concise bullet points explaining
            the importance of the topic below.
        """),
        ("user", "{research_topic}")
    ])
    return prompt | llm_instance | StrOutputParser()


@tool
def write_article(research_notes: str) -> StrOutputParser:
    """
    Write a coherent ~200-word article based on research notes.

    Args:
        research_notes (str): The research notes or bullet points.

    Returns:
        StrOutputParser: Parsed output containing a ~200-word article.

    Example:
        article = write_article("1. RL allows agents to learn from feedback...\n2. RL is key in robotics...")
        print(article)
    """
    prompt = ChatPromptTemplate([
        ("system", """
            You are a Content Writer. Take the following research notes and
            write a coherent ~200-word article:
        """),
        ("user", "{researched_topic}")
    ])
    return prompt | llm_instance | StrOutputParser()


# -------------------------
# 3. Register Tools
# -------------------------
def get_agent_tools() -> list[Tool]:
    """
    Returns the list of tools available to the agent.

    Returns:
        list[Tool]: Tools for research and article writing.
    """
    return [
        Tool.from_function(
            name="ResearchTool",
            func=researcher,
            description="Research key points about any specified topic."
        ),
        Tool.from_function(
            name="ArticleWriterTool",
            func=write_article,
            description="Write an article using research notes."
        ),
    ]


# -------------------------
# 4. Main Agent Execution
# -------------------------
def main():
    # Topic to research and write about
    topic = "reinforcement learning"

    # Get tools for the agent
    tools = get_agent_tools()

    # Initialize a LangChain agent
    agent_executor = initialize_agent(
        llm=llm_instance,
        tools=tools,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Define the goal for the agent
    goal = f"Create a ~200-word article on {topic} starting from research."

    # Execute the agent and get the output
    result = agent_executor.invoke(goal)

    # Display the article
    print(result['output'])


if __name__ == "__main__":
    main()