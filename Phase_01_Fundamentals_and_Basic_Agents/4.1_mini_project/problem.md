we’ve already learned the **four most powerful patterns in LangChain** for building intelligent agents:

* **Prompt Chaining** (step-by-step breakdown of tasks)
* **Parallelization** (run tasks simultaneously for efficiency)
* **Reflection** (self-check and improve its own answers)
* **Routing** (decide which sub-agent or tool is best for a given query)

To build confidence, let’s design a **mini AI Research Assistant** project that combines all 4.

---

# Mini-Project: **AI Research & Summarization Agent**

### **Project Idea**

Build an agent that takes a **user query (like “Explain the applications of blockchain in supply chains”)**, fetches relevant data from different sources, processes it step by step, and outputs a clean final answer after checking itself.