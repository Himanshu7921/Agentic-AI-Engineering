"""
Laptop Specification Extractor and Transformer using LangChain + Google Generative AI
-------------------------------------------------------------------------------------

This script demonstrates how to use **LangChain Expression Language (LCEL)** 
with the `GoogleGenerativeAI` model to perform **prompt chaining**.  

Workflow:
1. Extracts technical specifications (CPU, RAM, Storage) from unstructured text.  
2. Transforms the extracted specifications into a structured JSON object.  

Requirements:
- Python 3.9+
- Install the following packages:
    pip install langchain-google-genai langchain-core

Environment Variables:
- `Gemini_APIKEY`: Your API key for Google Generative AI (Gemini).

Example Input:
    "The new laptop model features a 3.5 GHz octa-core processor, 
     16GB of RAM, and a 1TB NVMe SSD."

Example Output:
    {
      "CPU": "3.5 GHz octa-core processor",
      "RAM": "16GB",
      "storage": "1TB NVMe SSD"
    }

Educational Notes:
- **Prompt chaining** is used here to break down a complex task 
  (extracting + structuring specifications) into smaller steps.  
- This improves reliability, modularity, and easier debugging.
"""

import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# -----------------------------------------------------------------------------
# Step 1: Initialize the LLM (Google Gemini)
# -----------------------------------------------------------------------------
llm_model = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("Gemini_APIKEY")  # Make sure your environment variable is set
)


# -----------------------------------------------------------------------------
# Step 2: Define the prompts
# -----------------------------------------------------------------------------

# Prompt 1 - Extraction: Ask the model to extract raw specifications from text
prompt_extract = ChatPromptTemplate.from_template(
    """
    Extract the technical specifications from the following text:
    {text}
    """
)

# Prompt 2 - Transformation: Ask the model to format into JSON
prompt_transform = ChatPromptTemplate.from_template(
    """
    Transform the following specifications into a JSON object with 
    'CPU', 'RAM', and 'storage' as keys.
    
    Specifications: {specifications}
    """
)


# -----------------------------------------------------------------------------
# Step 3: Build the chains using LCEL (LangChain Expression Language)
# -----------------------------------------------------------------------------

# Chain 1: Extract specs → LLM → plain text output
extraction_chain = prompt_extract | llm_model | StrOutputParser()

# Chain 2: Transform extracted specs → JSON → LLM → plain text output
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm_model
    | StrOutputParser()
)


# -----------------------------------------------------------------------------
# Step 4: Run the full chain
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    input_text = (
        "The new laptop model features a 3.5 GHz octa-core processor, "
        "16GB of RAM, and a 1TB NVMe SSD."
    )

    final_result = full_chain.invoke({"text": input_text})

    print("\nFinal Structured Output:\n", final_result)