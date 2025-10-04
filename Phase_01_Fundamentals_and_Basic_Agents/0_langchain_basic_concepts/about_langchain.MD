# LangChain Overview

LangChain is a powerful **framework for building applications with Large Language Models (LLMs)** such as OpenAI GPT, Google Gemini, Anthropic Claude, and many others.  
It simplifies how developers interact with LLMs by providing structured tools for **prompting, chaining, memory, agents, and integrations**.

---

## Why Use LangChain?

Building directly with LLM APIs is possible, but it gets messy when your application grows. LangChain solves this by:

1. **Abstraction & Modularity**  
   - Provides consistent interfaces for different LLM providers (OpenAI, Gemini, Hugging Face, etc.).  
   - Makes it easy to switch or compare models.

2. **Prompt Engineering Support**  
   - Offers `PromptTemplate`, `ChatPromptTemplate`, and chaining tools to build **reusable, modular prompts**.  
   - Enables advanced techniques like **zero-shot**, **few-shot**, and **chain-of-thought** prompting.

3. **Chaining & Workflows**  
   - With **LangChain Expression Language (LCEL)**, you can connect multiple prompts, models, and parsers together.  
   - Example: Extracting info → Transforming → Formatting to JSON → Final output.

4. **Memory & Context**  
   - Add short-term or long-term memory to your chatbot or app so it can recall earlier interactions.  

5. **Integration with External Tools**  
   - Easily connect to APIs, databases, vector stores (like Pinecone, FAISS), and document loaders.  
   - Build real-world apps like **retrieval-augmented generation (RAG)** systems.

---

## 🛠 Core Components

### 1. **Models (LLMs)**
The engine behind LangChain. Supports text generation, chat models, and embeddings.

```python
from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="gemini-2.5-flash")
````

---

### 2. **Prompts**

Reusable templates that structure the input given to LLMs.

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Translate this sentence to French: {sentence}"
)
```

---

### 3. **Output Parsers**

Convert raw LLM text into structured formats like JSON, lists, or custom objects.

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
```

---

### 4. **Chains**

Connect multiple steps together. For example:

```python
chain = template | llm | parser
result = chain.invoke({"sentence": "Hello"})
print(result)  # -> "Bonjour"
```

---

### 5. **Agents**

Dynamic systems that use LLM reasoning to decide **which tools to call** (e.g., web search, calculator, APIs).

---

## Example Use Cases

* **Chatbots** with context and memory
* **Data extraction** (e.g., extract structured JSON from messy text)
* **Summarization** of long documents
* **Retrieval-Augmented Generation (RAG)** using vector databases
* **Educational demos** (prompt engineering, chaining, few-shot learning)

---

## Why It Matters

LangChain bridges the gap between **research-level LLM usage** and **production-ready AI apps**.
Instead of reinventing the wheel, developers can use LangChain to **prototype quickly, scale easily, and integrate seamlessly**.

---

## This Repository

This repo contains demos of different prompt engineering techniques using LangChain:

* `about_prompt_engineering.md` → Concepts explanation
* `zero_shot_example.py` → Zero-shot demo
* `few_shot_example.py` → Few-shot demo
* `chain_of_thought_demo.py` → Chain-of-thought demo
* `prompt_chaining.py` → Multi-step chaining workflow

---

## ✅ Requirements

* Python 3.9+
* Install dependencies:

```bash
pip install langchain langchain-google-genai
```

* Set up your API key for Gemini (or other LLMs):

```bash
export Gemini_APIKEY="your_api_key_here"
```

---

## 🌟 Next Steps

1. Learn prompt engineering basics (`zero_shot`, `few_shot`, `CoT`).
2. Explore chaining workflows (`prompt_chaining.py`).
3. Extend demos into real-world projects like chatbots or data pipelines.

---

💡 *LangChain gives you the building blocks to turn raw LLM power into structured, reusable, and scalable AI applications.*
