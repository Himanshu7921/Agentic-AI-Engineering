### **Project Idea: Personal Info & Utilities Agent**

**Goal:** Build an intelligent assistant that can dynamically answer personal info, general knowledge, or do small calculations using tools.

**Concepts Used:**

* Multiple tools (Python functions wrapped with `@tool`)
* LLM agent dynamically choosing tools
* Agent Executor to run tools

---

#### **Tools to Implement**

1. **Calculator Tool**

   * Takes a simple math expression like `"5 + 7 * 2"`
   * Returns the computed result

2. **Weather Info Tool**

   * Simulated, returns weather info for given cities

3. **Personal Info Tool**

   * Returns predefined info like name, age, or favorite color

4. **Random Fun Fact Tool**

   * Returns a random interesting fact

---

#### **Example Flow**

User Input: `"What’s 15 * 3?"`

* LLM generates a JSON-like request → decides **Calculator Tool**
* Agent executes → returns `45`

User Input: `"What’s the weather in London?"`

* LLM decides **Weather Info Tool**
* Agent executes → returns `"Cloudy, 15°C"`

User Input: `"Tell me a fun fact"`

* LLM decides **Fun Fact Tool**
* Agent executes → returns `"Octopuses have three hearts"`

---