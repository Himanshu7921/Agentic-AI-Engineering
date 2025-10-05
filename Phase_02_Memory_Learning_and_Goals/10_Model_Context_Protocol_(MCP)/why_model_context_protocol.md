# **Model Context Protocol (MCP)**

## 1. What Is MCP?

**Definition**
Model Context Protocol (MCP) is a standardized, open protocol that lets LLM-powered applications (or agents) *discover, invoke, and interact* with external tools, data resources, and prompt templates in a consistent way. It establishes a **client–server contract** so that any MCP-aware LLM (via its client) can connect to any MCP server, use its tools/resources, and receive structured responses — without bespoke integrations per LLM or system.
> **Reference Document:** [Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)

**Key Aspects / Intent**

* **Interoperability**: Different LLMs (GPT, Claude, Gemini, etc.) can all speak MCP and share tool servers.
* **Modularity & Reuse**: Build a tool once (wrapped in MCP), reuse it across many agents/applications.
* **Discoverability**: Agents can query what tools/resources a server offers at runtime.
* **Separation of concerns**: The LLM handles reasoning/planning, while the MCP server handles tool logic, data access, security, etc.

---

## 2. Client–Server Communication in MCP

### 2.1 What Is Client–Server Communication?

**Definition**
A **client–server architecture** is a model in which a *client* (requester) sends requests to a *server* (provider) over a network or interface; the server processes the request (often involving backend logic or data) and responds. This model cleanly separates concerns: clients focus on logic and orchestration; servers focus on execution, data, and tools.

**In the context of MCP:**

* The **MCP Client** acts as the intermediary between the LLM and external services.
* The **MCP Server** wraps external tools, data stores, or APIs and exposes them through a manifest.
* Communication typically uses JSON-RPC over STDIO (local) or HTTP/S with streaming (remote), depending on deployment.

### 2.2 Workflow: LLM ⇄ MCP Client ⇄ MCP Server (Detailed Step-by-Step)

Below is a detailed, step-wise description of how a query or request flows through an MCP-enabled system:

| Step                               | Actor / Layer           | Action                                                                                      | Purpose / Notes                                                                                                     |
| ---------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **1. Discovery**                   | MCP Client → MCP Server | The client requests the server’s *manifest* or capability description                       | The manifest lists available tools, resources, and prompt templates (with schemas, names, parameters, descriptions) |
| **2. Manifest Response**           | MCP Server → MCP Client | Sends structured manifest JSON (tools, resources, prompts, metadata)                        | Enables dynamic discoverability                                                                                     |
| **3. Planning (LLM side)**         | LLM (via client)        | Based on user intent, the LLM decides which tool(s) to call and in what order               | The agent plans its next action(s)                                                                                  |
| **4. Request Formulation**         | MCP Client / LLM        | Build a request object specifying tool name, parameters, idempotency key, possibly context  | E.g. `{ "tool": "send_email", "params": { … }, "request_id": "r123" }`                                              |
| **5. Authorization & Validation**  | MCP Server              | Check client credentials, validate parameters, check quotas/permissions                     | Reject requests early if invalid                                                                                    |
| **6. Execution / Tool Invocation** | MCP Server → 3P Service | The server invokes the underlying tool, API, or data access logic                           | Could be a DB call, REST API call, internal library, etc.                                                           |
| **7. Response / Output**           | MCP Server → MCP Client | Return standardized result object: success (with output) or error (with structured info)    | E.g. status, output data, error codes if any                                                                        |
| **8. Context Update**              | MCP Client → LLM        | The client feeds the tool’s output (or error) back into the LLM’s context                   | The LLM “knows” what happened and can plan next steps                                                               |
| **9. Next Step**                   | LLM                     | Continue planning, optionally call more tools, refine prompts, or deliver final user answer | The chain continues until the agent completes its goal                                                              |

#### Example Walkthrough (Send Email)

1. MCP Client fetches manifest; sees a tool `send_email` with parameters `(to, subject, body)`.
2. LLM (agent) decides: user asked “Email Alice — meeting notes.”
3. Client constructs request:

   ```json
   {
     "request_id": "r-42",
     "tool": "send_email",
     "params": {
       "to": "alice@example.com",
       "subject": "Meeting Notes",
       "body": "Here are the notes from today’s meeting..."
     }
   }
   ```
4. MCP Server authorizes the client (token, scopes).
5. Server invokes underlying email API/service.
6. Server responds:

   ```json
   {
     "request_id": "r-42",
     "status": "success",
     "output": {
       "message_id": "m-1234",
       "delivered": true
     }
   }
   ```
7. MCP Client feeds the result into the LLM context: `"Sent email with message_id = m-1234"`.
8. LLM may confirm to user: “Email sent successfully”.

---

## 3. Tool Function Calling vs. MCP (with Definitions and Examples)

### 3.1 Tool Function Calling

**Definition**
A mechanism by which an LLM (or its wrapper) directly calls a predefined tool or function to execute a task. The tool and its interface are known in advance; there is no discovery or protocol abstraction across multiple tools/systems.

**Example (simple)**
Suppose you're using GPT and you expose two functions:

* `get_weather(city: string) → {temperature, description}`
* `translate(text: string, target_lang: string) → string`

When the user says, “Translate this into French,” the LLM outputs something like:

```
{"tool": "translate", "text": "Hello, world", "target_lang": "fr"}
```

The host executes that function and returns `"Bonjour, le monde"`.
There’s no discovery; the LLM was preconfigured to know `translate`.

**Pros & Cons**

* ✅ Simpler to implement (for small scope).
* ✅ Lower overhead.
* ❌ Not reusable across LLMs or apps.
* ❌ Doesn’t scale well as tool set grows.
* ❌ Lacks dynamic discovery and modularity.

### 3.2 MCP (revisited)

**Definition**
A generic, open protocol for discovering and using tools, resources, and prompts between LLM clients and servers. It decouples the reasoning layer from the execution layer via a manifest-based interface, enabling modular, interoperable connections.

**Example (MCP style)**
Imagine a server with manifest:

```json
{
  "tools": [
    {
      "id": "translate",
      "params": {
        "text": "string",
        "target_lang": "string"
      }
    },
    {
      "id": "summarize",
      "params": {
        "document": "string"
      }
    }
  ]
}
```

An LLM client can query the manifest, see `translate`, and decide to call it dynamically:

```json
{
  "request_id": "r-77",
  "tool": "translate",
  "params": {
    "text": "Good morning",
    "target_lang": "es"
  }
}
```

The server executes and returns:

```json
{
  "request_id": "r-77",
  "status": "success",
  "output": "Buenos días"
}
```

This same protocol works irrespective of which LLM is used — as long as it supports MCP.

### 3.3 Comparative Table

| Aspect              | Tool Function Calling       | MCP                                                       |
| ------------------- | --------------------------- | --------------------------------------------------------- |
| **Discovery**       | Static, known ahead of time | Dynamic — client can ask server “what tools do you have?” |
| **Standardization** | Vendor-specific integration | Open standard, works across LLMs and servers              |
| **Scalability**     | Hard to scale many tools    | Scales well, modular architecture                         |
| **Reusability**     | Tied to a specific system   | Tools and servers are reusable across apps                |
| **Flexibility**     | Low — need manual updates   | High — can evolve servers independently                   |

---

## 4. Error Handling in MCP

Error handling is **crucial** in any agent-tool protocol. The LLM must understand what went wrong so it can decide a fallback or retry strategy.

### 4.1 Error Types & Schema (Recommended)

When a tool fails, the MCP server should return a structured error object, not just a plain string. A minimal error schema:

```json
{
  "request_id": "...",
  "status": "error",
  "error": {
    "code": "TOOL_EXECUTION_FAILED",
    "message": "Underlying API returned HTTP 500",
    "retryable": true,
    "details": {
      "http_status": 500,
      "api_name": "sendgrid"
    }
  }
}
```

**Fields explained:**

* `code` — machine-friendly error code (e.g. `INVALID_PARAMS`, `AUTH_DENIED`, `RATE_LIMIT`, `UNAVAILABLE`, `TOOL_EXECUTION_FAILED`)
* `message` — human-readable summary
* `retryable` — boolean whether the LLM/client should attempt again
* `details` — additional structured info for logic (e.g. error codes, service names)

### 4.2 Workflow on Failure & Retry Logic

1. **Server returns error**
   Example: `"status":"error", "error":{ "code":"RATE_LIMIT", "retryable": true, ... }`

2. **MCP Client passes error back to LLM in context**
   E.g. “Tool `send_email` failed: RATE_LIMIT; retryable.”

3. **LLM reasons / reacts**
   The agent might choose to:

   * Wait and retry after a delay (if `retryable` is true)
   * Switch to a fallback tool or approach
   * Abort the workflow and raise the failure to the user

4. **Client or LLM may catch and reissue** (using idempotency keys if stateful)

   * If the tool supports idempotency, resending with same key leads to safe retry.
   * If not, the agent may try alternative routes or prompt for user intervention.

### 4.3 Example Scenario: Summarizing 1,000 Documents

* Agent calls `summarize_batch(docs=1000)`
* Server times out or returns `TOOL_EXECUTION_FAILED` with `retryable = true`
* LLM logic: split into two `summarize_batch(500)` calls and reattempt
* If still fails, abort and fall back to summarizing smaller chunks or send error message

### 4.4 Best Practices for Error Design

* Distinguish between **transient** vs **permanent** errors
* Provide **retry guidance** and backoff recommendations
* Support **partial results** when possible
* Use **idempotency keys** for state-changing tools to avoid double side-effects
* Use structured metadata so agents can automate decisions (versus opaque errors)

---

## 5. Local vs Remote MCP Servers

**Local Server**

* Runs on the same host or network as the LLM/agent
* Communication via STDIO or local IPC (fast, low latency)
* Suitable for **private, sensitive, or latency-critical** tasks
* Less scalable / harder to share with multiple agents

**Remote Server**

* Runs on a different machine or cloud service
* Communication via HTTP, WebSockets, SSE, or other network protocols
* Good for **scalable, shareable, multi-client** use
* Introduces network latency, greater security surface, and more operational overhead

**When to use which?**

* Use **local** when data sensitivity is high (e.g. internal documents, secrets) and you want minimal latency.
* Use **remote** when multiple agents or services need to share the same tools or resources, or when centralized management is needed.

---

## 6. Real-World Use Cases, When to Use / When Not to Use MCP

### 6.1 Use Cases Where MCP Excels

| Scenario                 | Why MCP Pattern Works Well                                                                                                   |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| Enterprise AI assistants | Centralize email, calendar, document tools once via MCP servers; multiple agents (sales, support, analytics) can reuse them. |
| Multi-agent systems      | Agents orchestrate workflows across different domains (research, writing, evaluation) via shared MCP servers.                |
| Legacy system bridging   | Wrap old APIs / databases in MCP so new agents can consume them without rewriting core systems.                              |
| Plugin / tool ecosystems | Offer a marketplace of tools (e.g. translation, summarization, code execution) that any agent can discover and use.          |
| Scaling across domains   | Add new capability (e.g. a new CRM or analytics server) just by spinning up a new MCP server — agents adapt dynamically.     |

### 6.2 Cases Where MCP May Be Overkill or Poor Fit

* **Very small, fixed toolset** — if your agent only ever needs 2 functions, direct tool calling may suffice.
* **Extremely low-latency constraints** where even network overhead is unacceptable.
* **Ad-hoc scripts / prototypes** — in early experiments, the abstraction overhead may slow you down.
* **Tools with highly complex custom stateful logic** that don’t map cleanly to a standard manifest → you may end up building wrappers anyway.
* **When agents must operate completely offline** and can't host or access servers at all (unless local MCP is embedded).

---

## 7. Summary (Key Takeaways)

* MCP provides a **unified, open protocol** for LLMs to discover and access external tools, resources, and prompt templates, removing the need for bespoke integrations per-model.
* The **client–server architecture** separates reasoning from execution, enabling modular, scalable, and secure systems.
* The request workflow (discovery → planning → request formulation → authorization → execution → response → context update) is central to how MCP integrates LLMs and tools.
* **Tool Function Calling** is a simpler but more brittle alternative; MCP is more robust, reusable, and future-proof.
* **Error handling** in MCP is critical: servers must return structured errors, with retryable flags and metadata, and clients/LLMs must be able to react (retry, fallback, abort).
* Choosing **local vs remote MCP** depends on trade-offs between latency, security, shareability, and scalability.
* MCP is powerful in environments with many agents, shared resources, or evolving tool landscapes; but for very minimal or static setups, simpler approaches might suffice.

---