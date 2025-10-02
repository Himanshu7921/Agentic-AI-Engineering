"""
LangChain Tool Use & Agents – Educational Example

This script demonstrates how to enable a Language Model (LLM) to interact with the real world
using LangChain tools and agents. 

Key Concepts:
1. LLMs (Language Models) generate text but cannot directly interact with external systems.
2. Tools are Python functions wrapped to allow LLMs to request their execution.
3. Agents combine LLMs with tools, enabling the LLM to decide which tool to call based on the input.
4. AgentExecutor runs the agent in a runtime environment, invoking the selected tool(s) and returning responses.

Requirements:
- Python 3.10+
- LangChain libraries: langchain, langchain_google_genai
- Gemini API key set as environment variable `Gemini_APIKEY`
"""

import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType, Tool

# -------------------------
# 1. Build the LLM Model
# -------------------------
def build_llm_model() -> GoogleGenerativeAI:
    """
    Initializes the Google Generative AI model (Gemini).

    Returns:
        GoogleGenerativeAI: Configured LLM instance that can generate text.
    
    Notes:
    - The LLM by itself cannot execute Python functions or access external data.
    - Tools and agents are needed to extend its capabilities.
    """
    return GoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("Gemini_APIKEY"),
    )

# -------------------------
# 2. Define a Tool
# -------------------------
@tool
def search_information(query: str) -> str:
    """
    A tool to provide factual information for simple queries.

    Args:
        query (str): A natural language question such as "capital of France".

    Returns:
        str: A simulated answer for the given query.

    Notes:
    - The @tool decorator converts a standard Python function into a LangChain Tool.
    - The LLM will only generate a JSON-like request to use this tool; the agent executes it.
    """
    print(f"\n--- 🛠️ Tool Called: search_information with query: '{query}' ---")
    
    # Predefined simulated results for demonstration
    simulated_results = {
        "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
        "capital of france": "The capital of France is Paris.",
        "population of earth": "The estimated population of Earth is around 8 billion people.",
        "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
        "default": f"Simulated search result for '{query}': No specific information found, but the topic seems interesting."
    }

    # Lookup the query, or return a default response
    result = simulated_results.get(query.lower(), simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result

# -------------------------
# 3. Wrap Tools for the Agent
# -------------------------
def get_tools():
    """
    Wraps Python functions into LangChain Tool objects.

    Returns:
        list[Tool]: A list of tools available for the agent.
    
    Notes:
    - Each tool requires a name and a description.
    - The description helps the LLM choose which tool to use dynamically.
    """
    return [
        Tool.from_function(
            func=search_information,
            name="SearchInformation",
            description="Provides factual information for queries like 'capital of France' or 'weather in London'."
        )
    ]

# -------------------------
# 4. Initialize the Agent Executor
# -------------------------
def get_agent_executor(tools, llm):
    """
    Creates an agent executor that runs the agent and invokes tools as needed.

    Args:
        tools (list[Tool]): List of tools accessible to the agent.
        llm (GoogleGenerativeAI): The LLM model instance.

    Returns:
        agent_executor: A runtime object to run the agent with given queries.
    
    Notes:
    - The agent itself contains the logic to choose which tool to call.
    - The executor actually runs the tool and returns the response.
    """
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Agent type that dynamically chooses tools
        verbose=True
    )

# -------------------------
# 5. Run the Agent for a Query
# -------------------------
def run_agent_with_tool(query: str):
    """
    Executes a single query through the agent executor.

    Args:
        query (str): The user query to process using the agent.
    
    Steps:
    1. Build the LLM model.
    2. Wrap tools into LangChain Tool objects.
    3. Initialize the agent executor.
    4. Run the agent executor with the query.
    5. Print the final response.
    """
    llm = build_llm_model()      # Step 1
    tools = get_tools()          # Step 2
    agent_executor = get_agent_executor(tools, llm)  # Step 3

    print(f"\n--- 🏃 Running Agent with Query: '{query}' ---")
    response = agent_executor.invoke({"input": query})  # Step 4
    print("\n--- ✅ Final Agent Response ---")
    print(response)  # Step 5

# -------------------------
# 6. Main Execution
# -------------------------
def main():
    """
    Runs a set of example queries through the agent to demonstrate tool use.

    Example queries:
        - "What is the capital of France?"
        - "What's the weather like in London?"
        - "Tell me something about dogs."
    """
    example_queries = [
        "What is the capital of France?",
        "What's the weather like in London?",
        "Tell me something about dogs."
    ]

    for query in example_queries:
        run_agent_with_tool(query)  # Run each query through the agent

# Entry point of the script
if __name__ == "__main__":
    main()

# -------------------------
# ✅ Key Beginner-Friendly Takeaways
# -------------------------

# 1. LLM Alone = Text Generator
#    - Can generate text but cannot execute code or access real-world data.
#    - Example: Asking "capital of France" will return text but won't query a database.

# 2. Tools = Python Functions for Real-World Interaction
#    - Wrapped using @tool decorator or Tool.from_function.
#    - Can fetch information, perform calculations, call APIs, etc.
#    - The LLM only generates a JSON-like request; the agent executes the tool.

# 3. Agent = LLM + Tools
#    - Combines the LLM with tools to allow interaction with the environment.
#    - Decides which tool to call based on the user query.
#    - Chooses dynamically using the tool's description.

# 4. Agent Executor = Runtime
#    - Executes the agent in a runtime environment.
#    - Calls the selected tools and returns the final output.
#    - Always invoke the executor, not the agent or LLM directly.