"""
Coordinator Agent with Delegation using LangChain and Google Generative AI
==========================================================================

This script demonstrates how to build a **Coordinator Agent** that delegates 
user requests to specialized sub-agents (simulated handlers) using LangChain's
`RunnableBranch`.

Requirements:
-------------
- Python 3.9+
- Install required dependencies:
    pip install langchain-core langchain-google-genai

Environment Setup:
------------------
Set the environment variable for your Gemini API key:
    export Gemini_APIKEY="your_api_key_here"   # Linux/Mac
    set Gemini_APIKEY="your_api_key_here"      # Windows (cmd)
    $env:Gemini_APIKEY="your_api_key_here"     # Windows (PowerShell)

Overview of Flow:
-----------------
1. The Coordinator Agent uses a prompt-based LLM router (`coordinator_router_chain`)
   to classify the request into one of three categories: 
   - "booker" → Booking Agent
   - "info"   → Info Agent
   - "unclear"→ Unclear Request Handler

2. The classified decision is combined with the original request and routed 
   via `RunnableBranch` to the correct handler.

3. Each handler simulates performing its task and returns a response.

Example Outputs:
----------------
- Booking request:
    Final Result A: Booking Handler processed request: 'Book me a flight to London.' | Result: Simulated booking action
- Information request:
    Final Result B: Info Handler processed request: 'What is the capital of Italy?' | Result: Simulated Information retrieval
- Unclear request:
    Final Result C: Handler could not delegate request: 'Tell me about quantum physics.'. Please clarify.
"""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough, RunnableBranch


# ---------------------------------------------------------------------------
# Step 1: Configure the LLM
# ---------------------------------------------------------------------------
llm_model = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("Gemini_APIKEY")
)

# Output parser ensures LLM response is a clean string
output_parser = StrOutputParser()


# ---------------------------------------------------------------------------
# Step 2: Define Specialized Handlers (Simulated Sub-Agents)
# ---------------------------------------------------------------------------
def booking_handler(request: str) -> str:
    """
    Simulates a Booking Agent.
    Handles travel or hotel booking requests.

    Args:
        request (str): The original user request.

    Returns:
        str: Simulated booking response.
    """
    print("Delegating to the booking handler agent...")
    return f"Booking Handler processed request: '{request}' | Result: Simulated booking action"


def info_handler(request: str) -> str:
    """
    Simulates an Info Agent.
    Handles general information retrieval requests.

    Args:
        request (str): The original user request.

    Returns:
        str: Simulated information response.
    """
    print("Delegating to info handler agent...")
    return f"Info Handler processed request: '{request}' | Result: Simulated Information retrieval"


def unclear_handler(request: str) -> str:
    """
    Handles unclear or unclassifiable requests.

    Args:
        request (str): The original user request.

    Returns:
        str: Response requesting clarification.
    """
    print("Handling Unclear Request")
    return f"Handler could not delegate request: '{request}'. Please clarify."


# ---------------------------------------------------------------------------
# Step 3: Define the Router Chain (LLM-based Decision Maker)
# ---------------------------------------------------------------------------
coordinator_router_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """Analyze the user's request and determine which specialist handler should process it.
        - If the request is related to booking flights or hotels, output 'booker'.
        - For all other general information questions, output 'info'.
        - If the request is unclear or doesn't fit either category, output 'unclear'.
        ONLY output one word: 'booker', 'info', or 'unclear'."""
    ),
    ("user", "{request}")
])

# Router Chain = Prompt → LLM → Output Parser
coordinator_router_chain = coordinator_router_prompt | llm_model | output_parser


# ---------------------------------------------------------------------------
# Step 4: Define Delegation Branching Logic
# ---------------------------------------------------------------------------
# Each branch calls the corresponding handler.
branches = {
    "booker": RunnablePassthrough.assign(
        output=lambda x: booking_handler(x["request"]["request"])
    ),
    "info": RunnablePassthrough.assign(
        output=lambda x: info_handler(x["request"]["request"])
    ),
    "unclear": RunnablePassthrough.assign(
        output=lambda x: unclear_handler(x["request"]["request"])
    ),
}

# RunnableBranch uses the decision from the router to select the handler
delegation_branch = RunnableBranch(
    (lambda x: x["decision"].strip() == "booker", branches["booker"]),
    (lambda x: x["decision"].strip() == "info", branches["info"]),
    branches["unclear"]  # Default branch
)

# ---------------------------------------------------------------------------
# Step 5: Assemble the Coordinator Agent
# ---------------------------------------------------------------------------
# The coordinator agent passes both:
# - The router decision
# - The original request
# Then routes to the proper handler
coordinator_agent = (
    {
        "decision": coordinator_router_chain,
        "request": RunnablePassthrough()
    }
    | delegation_branch
    | (lambda x: x["output"])  # Extract the handler's final output
)


# ---------------------------------------------------------------------------
# Step 6: Demonstration of the Coordinator Agent
# ---------------------------------------------------------------------------
def main():
    """
    Demonstrates the Coordinator Agent with three example scenarios:
    - A booking request
    - An information request
    - An unclear request
    """
    if not llm_model:
        print("\nSkipping execution due to LLM initialization failure.")
        return

    print("--- Running with a booking request ---")
    request_a = "Book me a flight to London."
    result_a = coordinator_agent.invoke({"request": request_a})
    print(f"Final Result A: {result_a}")

    print("\n--- Running with an info request ---")
    request_b = "What is the capital of Italy?"
    result_b = coordinator_agent.invoke({"request": request_b})
    print(f"Final Result B: {result_b}")

    print("\n--- Running with an unclear request ---")
    request_c = "Tell me about quantum physics."
    result_c = coordinator_agent.invoke({"request": request_c})
    print(f"Final Result C: {result_c}")


if __name__ == "__main__":
    main()