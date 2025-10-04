"""
Text Generation Example using HuggingFace Transformers Pipeline

This script demonstrates how to generate text continuations using a pretrained
model through the transformers pipeline.

Requirements:
- transformers library: pip install transformers
"""

from transformers import pipeline

# Initialize a text-generation pipeline
# This loads a pretrained language model capable of generating text continuations
generator = pipeline("text-generation")

# Input prompt for the model
prompt_text = "In this course i'll will teach you how to use LangChain, but first let us"

# Generate text continuations
# - max_length: maximum length of generated text including the prompt
# - num_return_sequences: number of different continuations to generate
result = generator(
    prompt_text,
    max_length=20,
    num_return_sequences=2
)

# Print the generated text sequences
print(result)
