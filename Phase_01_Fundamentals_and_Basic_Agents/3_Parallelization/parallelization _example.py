"""
parallelization_example.py
---------------------------

This script demonstrates how to build a **parallelized LangChain pipeline**
using `RunnableParallel` with Google's Gemini LLM.

⚡ What the script does:
1. Creates three independent tasks (chains):
   - Summarization
   - Question Generation
   - Key Term Extraction
2. Runs these tasks **in parallel** using `RunnableParallel`.
3. Combines their outputs into a **final synthesized response**.

📦 Requirements:
- Python 3.9+
- langchain-core
- langchain-google-genai
- Google API key set as an environment variable: `Gemini_APIKEY`

👉 Example usage:
    $ python parallelization_example.py

Expected output:
    --- Final Response ---
    A structured, synthesized text that summarizes the topic, 
    highlights key terms, and proposes related questions.

"""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough, RunnableParallel


# -------------------------------------------------------------------
# 1. Configure the Large Language Model (LLM)
# -------------------------------------------------------------------
# We use Google's Gemini model. The API key must be set as an environment variable.
llm_model = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("Gemini_APIKEY")
)


# -------------------------------------------------------------------
# 2. Define individual chains (independent tasks)
# -------------------------------------------------------------------

# Chain A: Summarization
summarize_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "Summarize the following topic concisely: "),
        ("user", "{topic}")
    ])
    | llm_model
    | StrOutputParser()
)

# Chain B: Question Generation
questions_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "Generate three interesting questions about the following topic: "),
        ("user", "{topic}")
    ])
    | llm_model
    | StrOutputParser()
)

# Chain C: Key Term Extraction
terms_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "Identify 5-10 key terms from the following topic, separated by commas: "),
        ("user", "{topic}")
    ])
    | llm_model
    | StrOutputParser()
)


# -------------------------------------------------------------------
# 3. RunnableParallel - Running multiple tasks simultaneously
# -------------------------------------------------------------------
"""
🔎 What is RunnableParallel?

- `RunnableParallel` is a LangChain utility that allows you to run
  **multiple chains in parallel**.
- Each chain gets the same input, but produces its own output.
- The outputs are collected into a dictionary, which you can pass into
  a downstream chain.

Think of it as a **map-reduce style step**:
    - Map step → run chains in parallel
    - Reduce step → combine results

Here, we run: summarize_chain, questions_chain, and terms_chain
all at once, along with a passthrough for the original topic.
"""

map_chain = RunnableParallel(
    {
        "summary": summarize_chain,
        "questions": questions_chain,
        "key_terms": terms_chain,
        "topic": RunnablePassthrough(),  # forwards input topic unchanged
    }
)


# -------------------------------------------------------------------
# 4. Final synthesis step
# -------------------------------------------------------------------
# This chain takes the results of map_chain and produces a polished answer.
synthesis_chain = (
    ChatPromptTemplate.from_messages([
        ("system", """Based on the following information: 
        Summary: {summary}
        Related Questions: {questions}
        Key Terms: {key_terms}
        Synthesize a comprehensive, educational response."""),

        ("user", "Original topic: {topic}")
    ])
    | llm_model
    | StrOutputParser()
)


# -------------------------------------------------------------------
# 5. Combine everything into the full pipeline
# -------------------------------------------------------------------
# Execution order:
#   map_chain (parallel step) → synthesis_chain (final step)
full_parallel_chain = map_chain | synthesis_chain


# -------------------------------------------------------------------
# 6. Execution function
# -------------------------------------------------------------------
def run_parallel(topic: str) -> None:
    """
    Run the full parallel chain on a given topic.

    Args:
        topic (str): The input topic to analyze.

    Prints:
        A synthesized response that includes a summary,
        key terms, and related questions.
    """
    # Invoke the full pipeline with just the topic
    response = full_parallel_chain.invoke({"topic": topic})

    print("\n--- Final Response ---")
    print(response)


# -------------------------------------------------------------------
# 7. Entry point
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Example input topic
    test_topic = "The History of Space Exploration"
    run_parallel(test_topic)