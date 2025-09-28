"""
Few-Shot Translation using Google Gemini LLM

This script demonstrates how to use the Google Generative AI (Gemini) model
to perform a **few-shot prompting** translation from English to French.

Few-shot prompting involves giving the model a few examples of the task
inside the prompt, so it understands the format and style of the expected output.
Unlike zero-shot prompting, which provides only instructions, few-shot gives
contextual examples to guide the LLM's behavior.

Requirements:
- Python 3.8+
- langchain_google_genai
- langchain_core
- A valid Google Gemini API key stored in the environment variable "Gemini_APIKEY"

Example Output:
----------------
Input sentence: "Thanks"
Output: "Merci"
"""

# ---------------------------
# Import required modules
# ---------------------------
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------------------
# Initialize the LLM
# ---------------------------
# The 'max_output_tokens' parameter controls the maximum number of tokens
# the model can generate. Set it according to expected output length.
llm_model = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("Gemini_APIKEY"),
    max_output_tokens=200
)

# ---------------------------
# Define the Few-Shot Prompt Template
# ---------------------------
# A few-shot prompt provides a few examples of input-output pairs to guide the model.
# This makes the model understand the expected translation pattern.
#
# In this example:
# - The model sees that "Hi" maps to "Salut" and "Bye" maps to "Au revoir"
# - Then it is asked to translate a new sentence following the same pattern
translation_prompt_template = PromptTemplate(
    input_variables=["sentence"],
    template="""
Translate English to French using the following examples:
'Hi' -> 'Salut'
'Bye' -> 'Au revoir'

Now translate this sentence: {sentence}
"""
)

# ---------------------------
# Example sentence to translate
# ---------------------------
sentence_to_translate = "Thanks"

# ---------------------------
# Create the Translation Pipeline
# ---------------------------
# The pipe operator '|' chains the prompt, LLM, and output parser together:
# 1. The prompt formats the input with the example sentence.
# 2. The LLM generates the translation.
# 3. The output parser converts the LLM response into a clean string.
translation_chain = (translation_prompt_template | llm_model | StrOutputParser())

# ---------------------------
# Execute the translation
# ---------------------------
translated_sentence = translation_chain.invoke({"sentence": sentence_to_translate})

# ---------------------------
# Display the result
# ---------------------------
print(f"Original Sentence: {sentence_to_translate}")
print(f"Translated Sentence: {translated_sentence}")