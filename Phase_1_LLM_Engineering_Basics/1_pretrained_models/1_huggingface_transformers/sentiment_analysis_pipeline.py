"""
Sentiment Analysis Example using HuggingFace Transformers Pipeline

This script demonstrates how to perform sentiment analysis on a given text
using a pretrained model through the transformers pipeline.

Requirements:
- transformers library: pip install transformers
"""

from transformers import pipeline

# Initialize a sentiment-analysis pipeline
# This loads a pretrained model capable of detecting positive/negative sentiment
classifier = pipeline("sentiment-analysis")

# Define the text to analyze
text_to_analyze = "I love to code!"

# Perform sentiment analysis
# The pipeline will return a list of dictionaries with 'label' and 'score'
result = classifier(text_to_analyze)

# Print the sentiment analysis result
print(result)
