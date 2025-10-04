"""
embedding_faiss_demo.py

This script demonstrates how to:
1. Use a local HuggingFace embedding model to convert text documents into vector embeddings.
2. Store these embeddings in a FAISS vector database.
3. Perform a similarity search to find the most relevant document for a given query.

Requirements:
- Python 3.8+
- langchain >= 0.2.x
- sentence-transformers
- faiss (CPU or GPU version depending on your system)

Example Output:
> The vector embedding of the second document (list of floats)
> [Document(id='...', metadata={}, page_content='Embeddings represent text in a vector space.')]

Author: Himanshu Singh
Date: 2025-10-04
"""

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def create_embeddings(documents, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Generate vector embeddings for a list of text documents using a HuggingFace model.

    Args:
        documents (list[str]): List of textual documents to embed.
        model_name (str, optional): HuggingFace model to use. Defaults to "sentence-transformers/all-MiniLM-L6-v2".

    Returns:
        list[list[float]]: List of embeddings, one per document.
    """
    # Initialize the HuggingFace embedding model
    embeddings_model = HuggingFaceEmbeddings(model_name=model_name)
    
    # Embed all documents
    return embeddings_model.embed_documents(documents)


def build_faiss_index(documents, embeddings_model):
    """
    Create a FAISS vector store from documents and embeddings.

    Args:
        documents (list[str]): List of textual documents.
        embeddings_model (HuggingFaceEmbeddings): The embeddings model instance.

    Returns:
        FAISS: FAISS vector database containing document embeddings.
    """
    return FAISS.from_texts(documents, embeddings_model)


def search_similar_documents(vector_db, query, top_k=1):
    """
    Perform a similarity search on the FAISS vector database.

    Args:
        vector_db (FAISS): The FAISS vector database.
        query (str): User query to find similar documents.
        top_k (int, optional): Number of top similar documents to retrieve. Defaults to 1.

    Returns:
        list[Document]: List of documents most similar to the query.
    """
    return vector_db.similarity_search(query, k=top_k)


if __name__ == "__main__":
    # Sample documents to embed
    documents = [
        "LangChain is a framework for building LLM applications.",
        "Embeddings represent text in a vector space."
    ]
    
    # Step 1: Generate embeddings
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    document_embeddings = embeddings_model.embed_documents(documents)
    
    # Print embedding for the second document as an example
    print("Embedding vector for the second document:")
    print(document_embeddings[1])
    
    # Step 2: Build FAISS vector store
    vector_db = build_faiss_index(documents, embeddings_model)
    
    # Step 3: Query the vector database
    query = "Tell me about embeddings"
    results = search_similar_documents(vector_db, query, top_k=1)
    
    print("\nMost similar document to the query:")
    for doc in results:
        print(doc)