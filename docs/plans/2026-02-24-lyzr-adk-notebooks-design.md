# Design: Lyzr ADK Progressive Notebook Lessons

**Date:** 2026-02-24
**Status:** Approved
**Format:** Jupyter Notebooks (.ipynb)

---

## Overview

A collection of 10 progressive Jupyter notebooks teaching developers how to build AI agents using the `lyzr-adk` Python SDK. Notebooks are self-contained, runnable top-to-bottom, and structured as educational lessons from beginner to advanced.

**Target audience:** Python developers new to Lyzr ADK
**Distribution:** GitHub (auto-renders), Google Colab (one-click open)
**Install:** `pip install lyzr-adk`

---

## Lesson Plan

| # | Filename | Topic | Key APIs |
|---|----------|--------|----------|
| 1 | `01_getting_started.ipynb` | Hello, Agent! | `Studio`, `create_agent`, `agent.run` |
| 2 | `02_providers_and_models.ipynb` | LLM Providers & Models | Provider strings, model switching |
| 3 | `03_agent_lifecycle.ipynb` | Agent Management | `get_agent`, `list_agents`, `update`, `clone`, `delete` |
| 4 | `04_structured_outputs.ipynb` | Type-Safe Responses | Pydantic models, structured extraction |
| 5 | `05_memory_and_sessions.ipynb` | Memory & Sessions | `add_memory`, session IDs, multi-turn |
| 6 | `06_tools_and_functions.ipynb` | Custom Tools | `add_tool`, Python functions as tools |
| 7 | `07_knowledge_bases_rag.ipynb` | RAG & Knowledge Bases | `create_knowledge_base`, `add_pdf`, `add_website`, `query` |
| 8 | `08_contexts.ipynb` | Dynamic Contexts | `create_context`, `add_context`, `remove_context` |
| 9 | `09_rai_guardrails.ipynb` | Responsible AI | `create_rai_policy`, toxicity, PII, NSFW, prompt injection |
| 10 | `10_capstone_project.ipynb` | Full Agent App | Combines tools + RAG + memory + guardrails |

---

## Notebook Schema (Per Lesson)

Every notebook follows this cell layout:

```
Cell 1  [markdown]  # Lesson N: Title
                    Badge row: difficulty · estimated time
                    2-3 sentence overview
                    Learning objectives (bulleted)

Cell 2  [markdown]  ## Prerequisites
                    - Prior lessons to complete
                    - External requirements (API key, files)

Cell 3  [code]      # Setup
                    !pip install lyzr-adk
                    imports
                    Studio(api_key=os.getenv("LYZR_API_KEY")) init

Cell 4-N [markdown] ## Concept heading + explanation
                    - What it is, why it matters

Cell 5-N [code]     # Working example, minimal and commented
                    print() all outputs explicitly

...repeat for each concept...

Cell N+1 [markdown] ## Exercise
                    Task description + acceptance criteria

Cell N+2 [code]     # Starter scaffold with # TODO placeholders

Cell N+3 [markdown] ## Summary
                    Key concepts recap (bulleted)
                    Quick-reference API table

Cell N+4 [markdown] ## Next Steps
                    → Link / reference to next notebook
```

---

## Key Constraints

- Every code cell must run **top-to-bottom without manual edits** (except env vars)
- **`print()` all outputs explicitly** — no implicit cell output reliance
- One concept per code cell — don't mix features
- Include a cell showing a **common mistake** and why it fails
- Early lessons hardcode values; later lessons introduce variables and reuse patterns
- Notebooks reference each other in Prerequisites and Next Steps sections

---

## File Structure

```
lyzr-adk-demo/
├── notebooks/
│   ├── 01_getting_started.ipynb
│   ├── 02_providers_and_models.ipynb
│   ├── 03_agent_lifecycle.ipynb
│   ├── 04_structured_outputs.ipynb
│   ├── 05_memory_and_sessions.ipynb
│   ├── 06_tools_and_functions.ipynb
│   ├── 07_knowledge_bases_rag.ipynb
│   ├── 08_contexts.ipynb
│   ├── 09_rai_guardrails.ipynb
│   └── 10_capstone_project.ipynb
├── docs/
│   └── plans/
│       └── 2026-02-24-lyzr-adk-notebooks-design.md
├── requirements.txt
└── README.md
```

---

## lyzr-adk API Reference (for notebook authors)

```python
from lyzr import Studio

studio = Studio(api_key="sk-xxx")  # or reads LYZR_API_KEY env var

# Agent CRUD
agent = studio.create_agent(name, provider, role, goal, instructions)
agent = studio.get_agent(agent_id)
agents = studio.list_agents()
agent.update(**kwargs)
agent.clone()
agent.delete()

# Run
response = agent.run(message, session_id=None, stream=False)
print(response.response)

# Memory
agent.add_memory(max_messages=10)
agent.remove_memory()

# Tools
agent.add_tool(python_function)

# Knowledge Bases
kb = studio.create_knowledge_base(name)
kb.add_pdf(file_path)
kb.add_website(url, max_pages=10)
kb.add_text(text, source)
kb.query(query, top_k=5)

# Contexts
ctx = studio.create_context(name, value)
agent.add_context(ctx)
agent.remove_context(ctx)

# RAI
policy = studio.create_rai_policy(name, **kwargs)
agent.add_rai_policy(policy)

# Structured outputs
agent.run(message, response_format=PydanticModel)
```

---

## Supported Providers

| Provider | Example string |
|----------|---------------|
| OpenAI | `"openai/gpt-4o"` |
| Anthropic | `"anthropic/claude-sonnet-4-5"` |
| Google | `"google/gemini-2.0-flash"` |
| Groq | `"groq/llama-3.3-70b"` |
| Perplexity | `"perplexity/sonar-pro"` |
| AWS Bedrock | `"bedrock/amazon.nova-pro-v1:0"` |
