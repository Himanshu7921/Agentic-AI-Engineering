"""
Multi-Agent Blog Post Generation using LangChain and Google Gemini

This script demonstrates a simple multi-agent workflow where specialized agents
collaborate to produce a research-informed blog post.

Agents:
1. Research Agent: Gathers and summarizes top AI trends for 2024-2025.
2. Writer Agent: Converts the research summary into a 500-word engaging blog post.

Requirements:
- Python 3.10+
- langchain-core
- langchain-google-genai
- An environment variable 'GOOGLE_API_KEY' with your Gemini API key

Example Output:
-----------------
## Research Summary ##
1. Trend Name: AI-driven Healthcare
   Summary: Rapid adoption of AI in diagnostics and personalized treatment.
   Source/Notes: Various healthcare journals, 2024.

2. Trend Name: Autonomous Agents in Finance
   Summary: AI agents managing portfolio optimization and fraud detection.
   Source/Notes: Financial tech reports, 2024.

3. Trend Name: AI for Climate Solutions
   Summary: Predictive modeling for climate events and resource optimization.
   Source/Notes: Environmental research publications, 2024.

## Final Blog Post ##
[500-word engaging blog post summarizing the research above]
"""

import os
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI


def initialize_llm(api_key_env: str = "GOOGLE_API_KEY") -> GoogleGenerativeAI:
    """
    Initialize the Google Gemini LLM using an API key stored in environment variables.

    Args:
        api_key_env (str): Environment variable name containing the API key.

    Returns:
        GoogleGenerativeAI: Configured LLM instance ready for generating content.
    """
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise ValueError(f"API key not found in environment variable '{api_key_env}'")

    llm = GoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key
    )
    return llm


def build_prompts() -> tuple[ChatPromptTemplate, ChatPromptTemplate]:
    """
    Define prompts for the research and writing agents.

    Returns:
        tuple: research_prompt, writing_prompt
    """
    research_prompt = ChatPromptTemplate.from_template(
        """
You are a research agent. Your task is to find and summarize the top 3 emerging trends in AI for 2024-2025.
Focus on practical applications and potential impact. Present your summary in clear points.

Output format: 
1. Trend Name: ...
2. Summary: ...
3. Source/Notes: ...
"""
    )

    writing_prompt = ChatPromptTemplate.from_template(
        """
You are a writer agent. Using the research summary provided below, write a 500-word engaging blog post suitable for a general audience.

Research Summary:
{research_summary}
"""
    )

    return research_prompt, writing_prompt


def create_chains(llm: GoogleGenerativeAI, research_prompt: ChatPromptTemplate,
                  writing_prompt: ChatPromptTemplate) -> SequentialChain:
    """
    Create LLMChains for research and writing, and combine them in a SequentialChain.

    Args:
        llm (GoogleGenerativeAI): Initialized language model.
        research_prompt (ChatPromptTemplate): Prompt for the research agent.
        writing_prompt (ChatPromptTemplate): Prompt for the writer agent.

    Returns:
        SequentialChain: Combined workflow chain.
    """
    # LLMChain for research agent
    research_chain = LLMChain(
        llm=llm,
        prompt=research_prompt,
        output_key="research_summary"
    )

    # LLMChain for writer agent
    writing_chain = LLMChain(
        llm=llm,
        prompt=writing_prompt,
        output_key="blog_post"
    )

    # SequentialChain to run agents one after another
    workflow_chain = SequentialChain(
        chains=[research_chain, writing_chain],
        input_variables=[],  # No initial input; agents rely on prompts
        output_variables=["research_summary", "blog_post"],
        verbose=True
    )

    return workflow_chain


def run_blog_creation_workflow():
    """
    Executes the multi-agent blog post creation workflow and prints the results.
    """
    # Step 1: Initialize LLM
    llm = initialize_llm()

    # Step 2: Build prompts
    research_prompt, writing_prompt = build_prompts()

    # Step 3: Create multi-agent chains
    blog_chain = create_chains(llm, research_prompt, writing_prompt)

    # Step 4: Run the workflow
    result = blog_chain({})

    # Step 5: Display results
    print("\n## Research Summary ##")
    print(result["research_summary"])
    print("\n## Final Blog Post ##")
    print(result["blog_post"])


if __name__ == "__main__":
    run_blog_creation_workflow()