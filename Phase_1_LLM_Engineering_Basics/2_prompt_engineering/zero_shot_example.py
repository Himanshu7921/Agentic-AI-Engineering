"""
Zero-Shot Translation using Google Gemini LLM and LangChain

This script demonstrates how to use a Google Generative AI (Gemini) model to perform
translation from one language to another using **Zero-Shot Prompting**. The model is
given instructions only, without any example translations (hence "zero-shot").

Requirements:
- Python 3.8+
- langchain_google_genai
- langchain_core
- A valid Google Gemini API key stored in the environment variable "Gemini_APIKEY"

Example:
--------
Input Sentence: "Hi, my name is Himanshu Singh!"
Translate from English to Japanese

Expected Output:
Original Language English: Hi, my name is Himanshu Singh!
Translated Language Japanese: こんにちは、私の名前はヒマンスです！
"""

# ---------------------------
# Import required modules
# ---------------------------
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------------------
# Initialize the LLM
# ---------------------------
# GoogleGenerativeAI connects to the Gemini model.
# - `model="gemini-2.5-flash"` specifies the model version.
# - `api_key` is retrieved securely from environment variables.
llm_model = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("Gemini_APIKEY"),
    max_output_tokens = 200
)

# ---------------------------
# Define the Zero-Shot Prompt Template
# ---------------------------
# PromptTemplate allows you to create a structured prompt with placeholders for
# dynamic variables (`from`, `to`, and `sentence` in this case).
# This template instructs the model to translate a sentence and return the output
# in a specific format.
zero_shot_translation_prompt = PromptTemplate(
    input_variables=["from", "to", "sentence"],
    template="""
You are the world's best translator who translates sentences from {from} to {to}. 
Translate the following sentence and provide the output in the specified format:

-> Original Language {from}: 
-> Translated Language {to}: 

Sentence: {sentence}
"""
)

# ---------------------------
# Define the Output Parser
# ---------------------------
# StrOutputParser extracts the text from the LLM response and standardizes it,
# making it easier to use in Python code.
output_parser = StrOutputParser()

# ---------------------------
# Define the Pipeline
# ---------------------------
# The pipe operator `|` chains components sequentially:
#   1. zero_shot_translation_prompt generates the prompt
#   2. llm_model produces the translation
#   3. output_parser cleans the output
translation_chain = zero_shot_translation_prompt | llm_model | output_parser

# ---------------------------
# Input Sentence
# ---------------------------
input_sentence = "Hi, my name is Himanshu Singh!"

# ---------------------------
# Run the translation pipeline
# ---------------------------
# The input dictionary maps template variables to actual values.
translated_sentence = translation_chain.invoke({
    "from": "English",
    "to": "Japanese",
    "sentence": input_sentence
})

# ---------------------------
# Print the Result
# ---------------------------
print(translated_sentence)

"""
Zero-Shot Prompting Explanation:

- Zero-shot prompting is a technique where the model is given **instructions only**
  without any examples of the task. 
- The model relies entirely on its pre-trained knowledge and the prompt instructions
  to complete the task correctly.
- This is in contrast to few-shot prompting, where a few examples are provided to
  guide the model.
- In this script, the model translates a sentence between two languages without
  seeing any translation examples in the prompt.
"""