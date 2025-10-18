You can check out the solution here: [PolicyPal-RAG-Agent GitHub Repository](https://github.com/Himanshu7921/PolicyPal-RAG-Agent)

**PolicyPal AI** is an intelligent assistant designed to make company policies and FAQs **quickly searchable and easy to understand**. Organizations often store their policies in PDFs or documents, making it cumbersome to locate specific information manually. PolicyPal addresses this challenge by leveraging **Retrieval-Augmented Generation (RAG)** to deliver **context-aware answers** to user queries.

The workflow of the system is as follows:

1. **Document Ingestion** – Converts PDFs of policies and FAQs into a structured format for processing.
2. **Vector Embeddings** – Generates embeddings of the documents using my custom RAG framework, **RetrievalMind**.
3. **Information Retrieval** – Searches the vector store to find the most relevant content for a user query.
4. **Answer Generation** – Uses a language model to create clear, contextually accurate responses.
5. **Frontend Delivery** – Presents answers via a lightweight web interface for interactive querying.

I’ve used **my own RAG framework, RetrievalMind**, for building this project. It is also **published on PyPI**, so you can install it with:

```
pip install RetrievalMind==0.1.1
```

You can also explore the framework on GitHub: [RetrievalMind Repository](https://github.com/Himanshu7921/RetrievalMind)

This project served as both a learning experience and a practical demonstration of building **RAG-based AI systems**, combining document retrieval, embedding management, and LLM-powered response generation.