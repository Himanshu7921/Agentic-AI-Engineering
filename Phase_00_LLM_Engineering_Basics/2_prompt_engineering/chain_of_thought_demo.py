"""
Chain-of-Thought Problem Solver using Google Gemini LLM

This script demonstrates how to use a Google Generative AI (Gemini) model
to solve problems step by step using Chain-of-Thought (CoT) prompting.

It is intended for educational purposes and as a reference for building
Python pipelines with LangChain and Google Generative AI.

Requirements:
- Python 3.8+
- langchain_google_genai
- langchain_core
- A valid Google Gemini API key stored in the environment variable "Gemini_APIKEY"

Theory:
-------
1. **Importance of Chain-of-Thought (CoT) Prompting**
   - CoT encourages the LLM to reason **step by step**, rather than providing 
     an immediate answer.
   - Reduces mistakes in multi-step calculations or complex reasoning tasks.
   - Makes the model's reasoning **transparent** and easier to verify.
   - Useful for math problems, logical reasoning, planning tasks, and data analysis.
   - Helps in breaking down complex tasks into smaller, verifiable sub-tasks.

2. **Popular Prompting Techniques**
   - **Zero-shot prompting**: Asking the model to complete a task without 
     providing any examples. Relies purely on instructions.
     Example: "Translate the following sentence to French: 'Hello, how are you?'"

   - **Few-shot prompting**: Providing a few examples in the prompt to guide 
     the model on how to perform the task.
     Example: "English to French translations:\n1. 'Hi' -> 'Salut'\n2. 'Goodbye' -> 'Au revoir'\nTranslate 'Thank you'."

   - **Chain-of-Thought (CoT) prompting**: Instructing the model to reason step 
     by step before giving the answer.
     Example: "Solve the following math problem step by step: 23 × 17"

   - **Instruction-based prompting**: Giving explicit instructions to perform a 
     task in a particular way.
     Example: "Summarize the following text in 3 concise bullet points."

   - **Self-consistency prompting**: Running multiple CoT outputs and selecting 
     the most common answer to improve reliability.
     Example: Generate several reasoning paths for a math problem and pick the majority answer.

   - **Decomposition / Prompt chaining**: Breaking a complex task into multiple 
     prompts where each prompt’s output feeds into the next.
     Example: Summarize a report -> Extract trends -> Draft an email to management.

Example:
----------
Problem: If a train travels 60 km in 1 hour and 90 km in 1.5 hours, what is the average speed of the train?
Output:
Step 1: Calculate total distance = 60 + 90 = 150 km
Step 2: Calculate total time = 1 + 1.5 = 2.5 hours
Step 3: Average speed = Total distance / Total time = 150 / 2.5 = 60 km/h
Answer: 60 km/h
"""

# ---------------------------
# Import required modules
# ---------------------------
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

# ---------------------------
# Initialize the LLM
# ---------------------------
llm_model = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("Gemini_APIKEY"),
    max_output_tokens = 200
)

# ---------------------------
# Define the Chain-of-Thought Prompt Template
# ---------------------------
# `PromptTemplate` is a LangChain utility that allows you to define a reusable,
# structured prompt for the LLM. It separates the prompt's **template** from
# the **dynamic input variables**, making your code modular and easy to maintain.
#
# In this example:
#   - `input_variables=["problem"]` specifies that the prompt expects a variable called "problem".
#   - `template=""" ... """` defines the text structure that the LLM will see.
#
# How it works:
#   1. When the chain runs, the placeholder `{problem}` is replaced with the actual problem text.
#   2. The LLM receives a formatted prompt that instructs it to reason **step by step**.
#
# Benefits of using PromptTemplate:
#   - Promotes **reusability**: the same template can be used for multiple problems.
#   - Improves **readability and organization**: separates logic from text.
#   - Simplifies **dynamic input handling**: easy to plug in new variables.
#   - Supports **prompt chaining and pipelines** seamlessly.
#
# Example usage:
#   chain_of_thought_prompt.format(problem="Calculate 23 × 17")
#   -> Produces the fully formatted prompt ready for the LLM.
chain_of_thought_prompt = PromptTemplate(
    input_variables=["problem"],
    template="""
Solve the following problem step by step.
Show your reasoning before giving the final answer.

Problem: {problem}
"""
)

# ---------------------------
# Output Parser
# ---------------------------
# The output parser is responsible for processing the raw output from the LLM.
# In this case, `StrOutputParser` is used to:
#   1. Simplify the LLM response by extracting the text content.
#   2. Standardize the output format, ensuring consistency across pipeline steps.
#   3. Make the result directly usable in Python code or for further processing in a prompt chain.
output_parser = StrOutputParser()


# ---------------------------
# Example Problem
# ---------------------------
problem_text = "If a train travels 60 km in 1 hour and 90 km in 1.5 hours, what is the average speed of the train?"

# ---------------------------
# Create the Problem-Solving Pipeline
# ---------------------------
# The pipe operator `|` in LangChain is used to chain together different components
# into a single, sequential workflow. Here’s what happens in this line:
#
#   chain_of_thought_prompt | llm_model | output_parser
#
# 1. `chain_of_thought_prompt` generates the initial input for the model.
# 2. `llm_model` (Google Gemini) receives the prompt and produces a raw output.
# 3. `output_parser` cleans and formats the LLM output into a simple string.
#
# Using the pipe operator has several advantages:
#   - Creates a readable and concise pipeline, avoiding nested function calls.
#   - Ensures the output of one step is automatically fed into the next.
#   - Improves modularity, making it easy to swap components (prompts, LLMs, parsers).
#   - Enhances maintainability and clarity, especially for multi-step workflows.
#
# Essentially, the pipe operator allows you to define a **linear, step-by-step
# processing sequence** similar to Unix pipelines or functional composition.
problem_solving_chain = chain_of_thought_prompt | llm_model | output_parser


# ---------------------------
# Solve the problem
# ---------------------------
solution = problem_solving_chain.invoke({"problem": problem_text})

# ---------------------------
# Print the solution
# ---------------------------
print("Problem:\n", problem_text)
print("\nSolution (step-by-step reasoning):\n", solution)