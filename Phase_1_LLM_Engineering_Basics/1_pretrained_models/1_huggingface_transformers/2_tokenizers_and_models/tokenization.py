"""
Educational script demonstrating how Hugging Face Transformers tokenizers work.

Requirements:
    pip install transformers

Overview:
    - Uses a pretrained DistilBERT sentiment-analysis model
    - Shows how text is split into tokens (subwords) using the tokenizer
    - Converts tokens into IDs (the numeric form models understand)
    - Decodes IDs back into text, showing reconstruction differences
    - Explains why certain tokens appear with markers like '##'

Key Concepts:
    - DistilBERT (like BERT) uses WordPiece tokenization.
    - Unknown or uncommon words are split into smaller subwords.
    - '##' prefix means "this token continues from the previous one."
      Example:
        'lang', '##chai', '##n' → together form 'langchain'
    - Lowercasing: DistilBERT is an "uncased" model, so the tokenizer
      automatically lowercases input. That’s why 'I' becomes 'i' when decoded.
"""

from transformers import AutoTokenizer


def demonstrate_tokenization(model_name: str, text: str) -> None:
    """
    Demonstrates how a Hugging Face tokenizer processes text.

    Args:
        model_name (str): Name of the pretrained model from Hugging Face Hub.
        text (str): Input sentence or phrase to tokenize.

    Example:
        >>> demonstrate_tokenization(
        ...     "distilbert-base-uncased-finetuned-sst-2-english",
        ...     "I love LangChain!"
        ... )
        Input Text: I love LangChain!
        Tokens: ['i', 'love', 'lang', '##chai', '##n', '!']
        Token IDs: [1045, 2293, 11374, 24925, 2078, 999]
        Decoded Text: i love langchain!
    """
    # Load tokenizer for the given model
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Step 1: Break text into tokens (subwords)
    tokens = tokenizer.tokenize(text)

    # Step 2: Convert tokens into numeric IDs (the model input format)
    token_ids = tokenizer.convert_tokens_to_ids(tokens)

    # Step 3: Decode IDs back into text
    decoded_text = tokenizer.decode(token_ids)

    # Display results
    print(f"Input Text: {text}")
    print(f"Tokens: {tokens}")
    print(f"Token IDs: {token_ids}")
    print(f"Decoded Text: {decoded_text}")


if __name__ == "__main__":
    # Pretrained model for tokenization demonstration
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"

    # Example text
    text = "I love LangChain!"

    demonstrate_tokenization(model_name, text)