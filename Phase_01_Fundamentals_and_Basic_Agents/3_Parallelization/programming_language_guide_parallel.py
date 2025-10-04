"""
Parallelized LangChain Pipeline Example
---------------------------------------

This script demonstrates how to build a parallelized pipeline using LangChain
and Google's Generative AI (`gemini-2.5-flash`). It takes a programming language
as input and produces a beginner-friendly guide containing:

1. A simple explanation of the programming language.
2. A list of 5 popular frameworks or libraries.
3. Three project ideas suitable for beginners.
4. A synthesized guide combining all of the above.

✨ Requirements:
- Install `langchain-core` and `langchain-google-genai`:
    pip install langchain-core langchain-google-genai

- Set your Google Generative AI API key as an environment variable:
    export Gemini_APIKEY="your_api_key_here"   # Linux/Mac
    setx Gemini_APIKEY "your_api_key_here"     # Windows

⚡ Educational Purpose:
This script is structured to show how to:
- Use `RunnableParallel` to run multiple chains in parallel.
- Combine chain outputs into a final synthesis chain.
- Build modular, composable pipelines in LangChain.

Example:
    python parallel_llm_pipeline.py
"""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


def build_llm_model():
    """
    Initialize the Google Generative AI model.

    Returns:
        GoogleGenerativeAI: Configured LLM model.
    """
    return GoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("Gemini_APIKEY"),
    )


def build_explanation_chain(llm):
    """
    Create a chain to explain a programming language in simple terms.
    """
    return (
        ChatPromptTemplate.from_messages([
            ("system", "Explain the following programming language in simple terms: "),
            ("user", "{programming_language}")
        ])
        | llm
        | StrOutputParser()
    )


def build_frameworks_chain(llm):
    """
    Create a chain to list 5 popular frameworks or libraries for a language.
    """
    return (
        ChatPromptTemplate.from_messages([
            ("system", "List 5 popular frameworks or libraries for the following programming language: "),
            ("user", "{programming_language}")
        ])
        | llm
        | StrOutputParser()
    )


def build_projects_chain(llm):
    """
    Create a chain to suggest 3 beginner-friendly project ideas.
    """
    return (
        ChatPromptTemplate.from_messages([
            ("system", "Suggest 3 beginner-friendly project ideas in the following programming language: "),
            ("user", "{programming_language}")
        ])
        | llm
        | StrOutputParser()
    )


def build_parallel_chain(explain_chain, framework_chain, project_chain):
    """
    Bundle all sub-chains into a parallel pipeline.

    Args:
        explain_chain: Chain to generate explanations.
        framework_chain: Chain to list frameworks.
        project_chain: Chain to suggest projects.

    Returns:
        RunnableParallel: Parallelized pipeline combining all outputs.
    """
    return RunnableParallel(
        {
            "explanation": explain_chain,
            "popular_frameworks": framework_chain,
            "project_ideas": project_chain,
            "programming_language": RunnablePassthrough(),  # passthrough input
        }
    )


def build_synthesis_chain(llm):
    """
    Build the final synthesis chain that combines outputs into a guide.
    """
    return (
        ChatPromptTemplate.from_messages([
            ("system", """Based on the following:
            Explanation: {explanation}
            Frameworks: {popular_frameworks}
            Project Ideas: {project_ideas}
            Write a beginner-friendly guide to this programming language."""),

            ("user", "Language: {programming_language}")
        ])
        | llm
        | StrOutputParser()
    )


def run_pipeline(language: str = "Python"):
    """
    Run the full pipeline for a given programming language.

    Args:
        language (str): The programming language to analyze. Default is "Python".

    Returns:
        str: Synthesized beginner-friendly guide.
    """
    # Initialize LLM model
    llm = build_llm_model()

    # Build sub-chains
    explain_chain = build_explanation_chain(llm)
    framework_chain = build_frameworks_chain(llm)
    project_chain = build_projects_chain(llm)

    # Parallel execution
    parallel_chain = build_parallel_chain(explain_chain, framework_chain, project_chain)

    # Combine into synthesis
    synthesis_chain = build_synthesis_chain(llm)

    # Full pipeline
    full_chain = parallel_chain | synthesis_chain

    # Execute pipeline
    return full_chain.invoke({"programming_language": language})


if __name__ == "__main__":
    # Example: Generate a guide for Python
    guide = run_pipeline("Python")
    print("=== Beginner-Friendly Guide ===\n")
    print(guide)