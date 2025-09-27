"""
hf_pytorch_demo.py

Demonstrates how to use Hugging Face Transformers models with PyTorch.

Requirements:
    pip install torch transformers

Overview:
    - Loads a pretrained DistilBERT model using Hugging Face.
    - Tokenizes text into input tensors compatible with PyTorch.
    - Performs a forward pass through the model to obtain embeddings.
    - Explains how to interact with the output tensors.

Key Concepts:
    - Hugging Face models are subclasses of torch.nn.Module, so you can:
        - Move models to GPU
        - Compute gradients and backpropagate
        - Fine-tune on custom datasets
        - Combine with custom PyTorch layers
    - AutoTokenizer and AutoModel simplify loading pretrained models.
"""

import torch
from transformers import AutoTokenizer, AutoModel

def demonstrate_hf_pytorch(model_name: str, text: str):
    """
    Loads a Hugging Face model and tokenizer, tokenizes input text,
    and runs a forward pass to obtain embeddings.

    Args:
        model_name (str): Name of the pretrained Hugging Face model.
        text (str): Input sentence to process.

    Example:
        >>> demonstrate_hf_pytorch("distilbert-base-uncased", "Hello world!")
        Last hidden state shape: torch.Size([1, 6, 768])
    """
    # Step 1: Load pretrained tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Step 2: Load pretrained model
    # Hugging Face models inherit from torch.nn.Module
    model = AutoModel.from_pretrained(model_name)

    # Step 3: Tokenize the input text and convert to PyTorch tensors
    inputs = tokenizer(text, return_tensors="pt")  # Returns dict with 'input_ids' and 'attention_mask'

    # Step 4: Forward pass through the model to obtain embeddings
    # Using **inputs unpacks the dictionary into model arguments
    output = model(**inputs)

    # Step 5: Inspect the output
    # output.last_hidden_state contains embeddings for each token
    print("Input Text:", text)
    print("Tokenized Inputs:", inputs)
    print("Output type:", type(output))
    print("Last hidden state shape:", output.last_hidden_state.shape)  # [batch_size, seq_len, hidden_size]

    # Optional: Move to GPU if available
    if torch.cuda.is_available():
        model = model.to("cuda")
        inputs = {k: v.to("cuda") for k, v in inputs.items()}
        output = model(**inputs)
        print("Moved model and inputs to GPU. Last hidden state shape:", output.last_hidden_state.shape)

if __name__ == "__main__":
    model_name = "distilbert-base-uncased"
    text = "Hey this is me!"
    demonstrate_hf_pytorch(model_name, text)