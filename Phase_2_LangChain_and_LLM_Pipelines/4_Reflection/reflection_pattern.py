"""
LangChain Reflection Loop for Python Code Generation

This script demonstrates a structured approach to generating, refining, and critically
evaluating Python code using LangChain with Google Generative AI (Gemini). 

Specifically, it automates the creation of a Python function to calculate factorials,
iteratively improving the code based on expert critique.

Requirements:
- Python 3.8+
- LangChain Core and Google Generative AI libraries installed
- Set the environment variable 'Gemini_APIKEY' with your Google Generative AI API key
"""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


def build_llm_model() -> GoogleGenerativeAI:
    """
    Initialize and return the Google Generative AI model.

    Returns:
        GoogleGenerativeAI: Configured LLM model with Gemini API key.
    """
    return GoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("Gemini_APIKEY"),
    )


def build_producer_template() -> ChatPromptTemplate:
    """
    Create a ChatPromptTemplate for generating or refining Python code.

    Returns:
        ChatPromptTemplate: Template instructing the LLM to generate
        a factorial function with specific requirements and optional refinement instructions.
    """
    return ChatPromptTemplate.from_messages([
        SystemMessage(content="You are an expert Python developer."),
        HumanMessage(content="""
        Your task is to create a Python function named `calculate_factorial`.
        
        Requirements:
        1. Accept a single integer `n` as input.
        2. Return its factorial (n!).
        3. Include a detailed docstring explaining the function, its parameters,
           return value, exceptions, and usage examples.
        4. Handle edge cases:
           - Factorial of 0 is 1.
           - Raise ValueError for negative inputs.
        5. Validate input type; raise TypeError for non-integer input.
        
        {refinement_instructions}
        """)
    ])


def build_critic_template() -> ChatPromptTemplate:
    """
    Create a ChatPromptTemplate for critically reviewing Python code.

    Returns:
        ChatPromptTemplate: Template instructing the LLM to provide
        structured critiques or confirm code correctness.
    """
    return ChatPromptTemplate.from_messages([
        SystemMessage(content="""
        You are a senior Python engineer and code reviewer.
        Critically evaluate ONLY the provided Python code for the factorial function.
        
        Check for:
        - Correctness (does it compute factorial correctly?)
        - Edge case handling (0, negative numbers, non-integers)
        - Python best practices and style
        - Clear and correct docstring
        - Possible improvements
        
        Respond strictly in one of the following ways:
        1. If the code is perfect, respond with: CODE_IS_PERFECT
        2. Otherwise, provide a concise bulleted list of issues and suggested improvements.
        Do NOT reference any other functions or tasks.
        """),
        HumanMessage(content="Original Task:\n{task_prompt}\n\nCode to Review:\n{code}")
    ])


def run_reflection_loop(max_iterations: int = 3):
    """
    Run the iterative reflection loop for code generation and critique.

    Args:
        max_iterations (int): Maximum number of generate-refine cycles.
    """
    current_code = ""  # Stores the latest version of the generated code
    refinement_instructions = ""  # Stores the latest critique instructions

    llm = build_llm_model()
    producer_template = build_producer_template()
    critic_template = build_critic_template()

    for iteration in range(max_iterations):
        print("\n" + "="*25 + f" REFLECTION LOOP: ITERATION {iteration + 1} " + "="*25)

        # --- Stage 1: Code Generation / Refinement ---
        print("\n>>> STAGE 1: Generating / Refining code...")
        producer_prompt = producer_template.format_messages(
            refinement_instructions=refinement_instructions
        )

        current_code = llm.invoke(producer_prompt)
        print(f"\n--- Generated Code (v{iteration + 1}) ---\n{current_code}")

        # --- Stage 2: Critique / Reflection ---
        print("\n>>> STAGE 2: Reflecting on the code...")
        task_text = producer_template.format_messages(refinement_instructions="")[1].content
        critic_prompt = critic_template.format_messages(
            task_prompt=task_text,
            code=current_code
        )

        refinement_response = llm.invoke(critic_prompt)
        refinement_instructions = refinement_response

        if "CODE_IS_PERFECT" in refinement_instructions:
            print("\n--- Critique ---\nNo further critiques found. The code is satisfactory.")
            break

        print("\n--- Refinement Instructions ---\n" + refinement_instructions)
        refinement_instructions = f"Refine the code based on these critiques:\n{refinement_instructions}"

    # --- Final Output ---
    print("\n" + "="*30 + " FINAL RESULT " + "="*30)
    print("\nFinal refined code:\n")
    print(current_code)


if __name__ == "__main__":
    run_reflection_loop(max_iterations=3)