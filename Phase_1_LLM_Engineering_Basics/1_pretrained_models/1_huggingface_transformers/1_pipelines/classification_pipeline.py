"""
Zero-Shot Text Classification Example using HuggingFace Transformers Pipeline

This script demonstrates how to classify a text into predefined categories
without training a model, using the zero-shot-classification pipeline.

Requirements:
- transformers library: pip install transformers
"""

from transformers import pipeline

# Initialize a zero-shot-classification pipeline
# This loads a pretrained model capable of classifying text into arbitrary categories
classifier = pipeline("zero-shot-classification")

# Define the text to classify
text_to_classify = "This is LangChain Technology"

# Define candidate labels for classification
candidate_labels = ["education", "business", "politics", "technology"]

# Perform zero-shot classification
# The pipeline will return a dictionary with labels and corresponding confidence scores
result = classifier(
    text_to_classify,
    candidate_labels=candidate_labels
)

# Print the classification result
print(result)
