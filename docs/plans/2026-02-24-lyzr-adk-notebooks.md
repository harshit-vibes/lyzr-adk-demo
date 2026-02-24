# Lyzr ADK Notebooks Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create 10 progressive Jupyter notebooks teaching developers how to build AI agents with `lyzr-adk`, each runnable top-to-bottom.

**Architecture:** Each notebook is a self-contained `.ipynb` file following a fixed schema: header → prerequisites → setup → concept sections (markdown + code pairs) → mini-exercise → summary → next steps. No shared state between notebooks — each installs and initializes independently.

**Tech Stack:** Python 3.8+, `lyzr-adk` (pip), Jupyter / Google Colab, `pydantic` (for lesson 4)

---

## Notebook Schema (apply to every lesson)

```
Cell 1  [markdown]  Title, badge row (difficulty · time), overview, learning objectives
Cell 2  [markdown]  Prerequisites
Cell 3  [code]      !pip install, imports, Studio init
...     [md+code]   One concept per section: explanation → example → output
...     [md+code]   Common mistake cell (show wrong usage + error)
Last-3  [markdown]  ## Exercise  (task + acceptance criteria)
Last-2  [code]      Starter scaffold with # TODO
Last-1  [markdown]  ## Summary  (bullets + quick-ref table)
Last    [markdown]  ## Next Steps → next notebook
```

### lyzr-adk API cheatsheet (use in all notebooks)

```python
from lyzr import Studio
studio = Studio(api_key="YOUR_LYZR_API_KEY")  # or LYZR_API_KEY env var

agent = studio.create_agent(name, provider, role, goal, instructions)
response = agent.run(message, session_id=None, stream=False)
print(response.response)

# Providers: "openai/gpt-4o", "anthropic/claude-sonnet-4-5",
#            "google/gemini-2.0-flash", "groq/llama-3.3-70b"
```

---

## Task 0: Project Scaffold

**Files:**
- Create: `notebooks/` directory
- Create: `requirements.txt`
- Create: `README.md`
- Create: `.env.example`

**Step 1: Create directory structure**

```bash
mkdir -p notebooks docs/plans
```

**Step 2: Write requirements.txt**

```
lyzr-adk>=0.1.5
python-dotenv
pydantic
jupyter
```

**Step 3: Write .env.example**

```
LYZR_API_KEY=your_api_key_here
```

**Step 4: Write README.md**

```markdown
# Lyzr ADK — Progressive Notebook Lessons

10 hands-on Jupyter notebooks for building AI agents with [lyzr-adk](https://pypi.org/project/lyzr-adk/).

## Quick Start

\`\`\`bash
pip install lyzr-adk python-dotenv pydantic jupyter
cp .env.example .env   # add your LYZR_API_KEY
jupyter notebook
\`\`\`

## Lessons

| # | Notebook | Topic |
|---|----------|-------|
| 1 | 01_getting_started.ipynb | Hello, Agent! |
| 2 | 02_providers_and_models.ipynb | LLM Providers & Models |
| 3 | 03_agent_lifecycle.ipynb | Agent Management |
| 4 | 04_structured_outputs.ipynb | Type-Safe Responses |
| 5 | 05_memory_and_sessions.ipynb | Memory & Sessions |
| 6 | 06_tools_and_functions.ipynb | Custom Tools |
| 7 | 07_knowledge_bases_rag.ipynb | RAG & Knowledge Bases |
| 8 | 08_contexts.ipynb | Dynamic Contexts |
| 9 | 09_rai_guardrails.ipynb | Responsible AI |
| 10 | 10_capstone_project.ipynb | Full Agent App |

Open on Colab: replace `github.com` with `githubtocolab.com` in the notebook URL.
```

**Step 5: Commit scaffold**

```bash
git init
git add requirements.txt README.md .env.example docs/
git commit -m "chore: project scaffold for lyzr-adk notebooks"
```

---

## Task 1: `notebooks/01_getting_started.ipynb`

**Concepts:** Install, import, `Studio` init, `create_agent`, `agent.run`, `response.response`
**Difficulty:** Beginner · ~15 min

**Cell layout:**

```
[md]  # Lesson 1: Hello, Agent!
      🟢 Beginner · ⏱ 15 min
      Overview: Create your first AI agent in 5 lines of Python.
      Objectives:
      - Install lyzr-adk
      - Initialize Studio with your API key
      - Create an agent with role, goal, instructions
      - Run the agent and read the response

[md]  ## Prerequisites
      - Python 3.8+
      - A Lyzr API key (sign up at https://lyzr.ai)
      - No prior lessons required

[code] # 1. Install
       !pip install lyzr-adk -q

[code] # 2. Imports & API key
       import os
       from lyzr import Studio

       API_KEY = os.getenv("LYZR_API_KEY", "YOUR_LYZR_API_KEY")

[md]  ## Creating a Studio instance
      Studio is the main entry point. It manages all your agents,
      knowledge bases, and settings. Pass your API key directly or
      set the LYZR_API_KEY environment variable.

[code] studio = Studio(api_key=API_KEY)
       print("Studio initialized:", studio)

[md]  ## Creating your first agent
      An agent needs four things:
      - name: human-readable label
      - provider: the LLM to use ("openai/gpt-4o")
      - role: who the agent is
      - goal: what it's trying to achieve
      - instructions: how it should behave

[code] agent = studio.create_agent(
           name="My First Agent",
           provider="openai/gpt-4o",
           role="Friendly assistant",
           goal="Answer questions helpfully and concisely",
           instructions="Keep responses under 3 sentences. Be friendly."
       )
       print("Agent created:", agent.id)

[md]  ## Running the agent
      Call agent.run() with your message. The response object has
      a .response attribute with the text reply.

[code] response = agent.run("What is artificial intelligence?")
       print(response.response)

[md]  ## Common mistake: forgetting to print response.response

[code] # ❌ This prints the raw response object, not the text:
       response2 = agent.run("Hello!")
       print(response2)          # <AgentResponse object>

       # ✅ Always access .response:
       print(response2.response)  # "Hello! How can I help you?"

[md]  ## Exercise
      Create a new agent that acts as a "Python tutor" and ask it
      to explain what a list comprehension is.

      Acceptance criteria:
      - Agent has a relevant role, goal, and instructions
      - Response is printed using .response

[code] # TODO: create a Python tutor agent
       tutor = studio.create_agent(
           name=...,
           provider="openai/gpt-4o",
           role=...,
           goal=...,
           instructions=...
       )

       # TODO: run it with a question about list comprehensions
       answer = tutor.run(...)
       print(answer.response)

[md]  ## Summary
      | Concept | Code |
      |---------|------|
      | Init Studio | `Studio(api_key="sk-...")` |
      | Create agent | `studio.create_agent(name, provider, role, goal, instructions)` |
      | Run agent | `agent.run("your message")` |
      | Read reply | `response.response` |

[md]  ## Next Steps
      → **Lesson 2:** [Providers & Models](02_providers_and_models.ipynb)
      Learn to switch between OpenAI, Anthropic, Google, and Groq.
```

**Step: Write the notebook file** using NotebookEdit / Write with proper .ipynb JSON.

**Step: Verify runs clean**
Open in Jupyter, Kernel → Restart & Run All. Expect no exceptions.

**Step: Commit**
```bash
git add notebooks/01_getting_started.ipynb
git commit -m "feat: add lesson 1 - getting started"
```

---

## Task 2: `notebooks/02_providers_and_models.ipynb`

**Concepts:** Provider strings, switching LLMs, comparing responses
**Difficulty:** Beginner · ~20 min

**Key cells:**

```
[md]  # Lesson 2: LLM Providers & Models
      🟢 Beginner · ⏱ 20 min
      Objectives: Use 4 different LLM providers, understand provider strings

[md]  ## Prerequisites
      - Lesson 1 completed
      - API keys for providers you want to test (at minimum: one)

[code] !pip install lyzr-adk -q
       import os
       from lyzr import Studio
       studio = Studio(api_key=os.getenv("LYZR_API_KEY", "YOUR_KEY"))

[md]  ## Provider string format
      Format: "provider/model-name"
      Examples:
      - "openai/gpt-4o"
      - "anthropic/claude-sonnet-4-5"
      - "google/gemini-2.0-flash"
      - "groq/llama-3.3-70b"

[code] # All supported providers
       PROVIDERS = {
           "OpenAI":    "openai/gpt-4o",
           "Anthropic": "anthropic/claude-sonnet-4-5",
           "Google":    "google/gemini-2.0-flash",
           "Groq":      "groq/llama-3.3-70b",
       }
       print("Available providers:")
       for name, provider in PROVIDERS.items():
           print(f"  {name}: {provider}")

[md]  ## Creating agents with different providers

[code] openai_agent = studio.create_agent(
           name="OpenAI Agent",
           provider="openai/gpt-4o",
           role="Assistant", goal="Answer questions", instructions="Be concise."
       )

       # Change provider string to switch models:
       google_agent = studio.create_agent(
           name="Google Agent",
           provider="google/gemini-2.0-flash",
           role="Assistant", goal="Answer questions", instructions="Be concise."
       )
       print("Both agents created.")

[md]  ## Comparing responses

[code] question = "In one sentence, what is machine learning?"

       openai_response = openai_agent.run(question)
       google_response = google_agent.run(question)

       print(f"OpenAI:  {openai_response.response}")
       print(f"Google:  {google_response.response}")

[md]  ## Switching provider on an existing agent
      Use agent.update() to change the provider without recreating.

[code] # Update provider in-place
       openai_agent.update(provider="anthropic/claude-sonnet-4-5")
       response = openai_agent.run("What is 2 + 2?")
       print(f"Now using Anthropic: {response.response}")

[md]  ## Common mistake: invalid provider string

[code] try:
           bad_agent = studio.create_agent(
               name="Bad Agent",
               provider="openai/gpt-99",  # ❌ model doesn't exist
               role="Test", goal="Test", instructions="Test"
           )
       except Exception as e:
           print(f"Error: {e}")

[md]  ## Exercise
      Create two agents using different providers and ask each:
      "Give me a one-line fun fact about space."
      Print both responses side-by-side.

[code] # TODO: pick two providers from PROVIDERS dict
       agent_a = studio.create_agent(name=..., provider=..., role=..., goal=..., instructions=...)
       agent_b = studio.create_agent(name=..., provider=..., role=..., goal=..., instructions=...)

       # TODO: run both and compare
       ...

[md]  ## Summary
      | Provider | String | Notes |
      |----------|--------|-------|
      | OpenAI | `"openai/gpt-4o"` | Default choice |
      | Anthropic | `"anthropic/claude-sonnet-4-5"` | Strong reasoning |
      | Google | `"google/gemini-2.0-flash"` | Fast, multimodal |
      | Groq | `"groq/llama-3.3-70b"` | Very fast inference |

      Switch provider: `agent.update(provider="new/model")`

[md]  ## Next Steps → Lesson 3: Agent Lifecycle
```

**Step: Write notebook, verify, commit.**

---

## Task 3: `notebooks/03_agent_lifecycle.ipynb`

**Concepts:** `list_agents`, `get_agent`, `update`, `clone`, `delete`
**Difficulty:** Beginner · ~20 min

**Key cells:**

```
[md]  # Lesson 3: Agent Management
      Objectives: list, retrieve, update, clone, delete agents

[code] # Setup
       !pip install lyzr-adk -q
       import os
       from lyzr import Studio
       studio = Studio(api_key=os.getenv("LYZR_API_KEY", "YOUR_KEY"))

[md]  ## Listing all agents

[code] agents = studio.list_agents()
       print(f"You have {len(agents)} agents:")
       for a in agents:
           print(f"  - {a.name} ({a.id})")

[md]  ## Retrieving an agent by ID

[code] agent = studio.create_agent(
           name="Lifecycle Demo", provider="openai/gpt-4o",
           role="Demo agent", goal="Demonstrate lifecycle", instructions="Be brief."
       )
       agent_id = agent.id
       print(f"Created agent: {agent_id}")

       # Retrieve later using ID
       retrieved = studio.get_agent(agent_id)
       print(f"Retrieved: {retrieved.name}")

[md]  ## Updating an agent

[code] agent.update(
           name="Lifecycle Demo v2",
           instructions="Be very brief. One sentence only."
       )
       response = agent.run("Explain gravity.")
       print(response.response)

[md]  ## Cloning an agent

[code] clone = agent.clone()
       print(f"Clone ID: {clone.id}")
       print(f"Clone name: {clone.name}")
       # Clone is independent — changes don't affect original

[md]  ## Deleting an agent

[code] clone.delete()
       print("Clone deleted.")

       # Verify it's gone
       all_agents = studio.list_agents()
       ids = [a.id for a in all_agents]
       print(f"Clone in list: {clone.id in ids}")  # False

[md]  ## Common mistake: using deleted agent

[code] try:
           clone.run("Hello?")  # ❌ agent is deleted
       except Exception as e:
           print(f"Error (expected): {e}")

[md]  ## Exercise + Summary + Next Steps
```

**Step: Write notebook, verify, commit.**

---

## Task 4: `notebooks/04_structured_outputs.ipynb`

**Concepts:** Pydantic response models, `response_format`, accessing typed fields
**Difficulty:** Intermediate · ~25 min

**Key cells:**

```
[md]  # Lesson 4: Structured Outputs
      Objectives: Define Pydantic models, get type-safe agent responses

[code] !pip install lyzr-adk pydantic -q
       import os
       from lyzr import Studio
       from pydantic import BaseModel, Field
       from typing import List
       studio = Studio(api_key=os.getenv("LYZR_API_KEY", "YOUR_KEY"))

[md]  ## Why structured outputs?
      By default agent.run() returns free-form text. With structured
      outputs you get typed Python objects — IDE autocomplete, validation,
      easy to pass to other functions.

[md]  ## Defining a Pydantic response model

[code] class MovieReview(BaseModel):
           title: str = Field(description="Movie title")
           rating: float = Field(description="Rating out of 10")
           summary: str = Field(description="One sentence summary")
           pros: List[str] = Field(description="List of positives")
           cons: List[str] = Field(description="List of negatives")

[md]  ## Creating an agent for structured extraction

[code] reviewer = studio.create_agent(
           name="Movie Reviewer",
           provider="openai/gpt-4o",
           role="Film critic",
           goal="Analyze movies and return structured reviews",
           instructions="Always return complete structured data as requested."
       )

[md]  ## Getting a structured response

[code] response = reviewer.run(
           "Review the movie Inception (2010)",
           response_format=MovieReview
       )

       review: MovieReview = response.response
       print(f"Title:  {review.title}")
       print(f"Rating: {review.rating}/10")
       print(f"Pros:   {review.pros}")

[md]  ## Nested models

[code] class Person(BaseModel):
           name: str
           age: int
           occupation: str

       class PersonList(BaseModel):
           people: List[Person]
           count: int

       extractor = studio.create_agent(
           name="Entity Extractor",
           provider="openai/gpt-4o",
           role="NLP extractor",
           goal="Extract structured entities from text",
           instructions="Extract all mentioned people."
       )

       text = "Alice (32, engineer) and Bob (28, designer) founded the startup."
       result = extractor.run(text, response_format=PersonList)
       data: PersonList = result.response

       for person in data.people:
           print(f"{person.name}, {person.age}, {person.occupation}")

[md]  ## Exercise + Summary + Next Steps
```

**Step: Write notebook, verify, commit.**

---

## Task 5: `notebooks/05_memory_and_sessions.ipynb`

**Concepts:** `session_id`, multi-turn, `add_memory`, `remove_memory`, external providers
**Difficulty:** Intermediate · ~25 min

**Key cells:**

```
[md]  # Lesson 5: Memory & Sessions

[code] # Setup + create agent with memory
       import os, uuid
       from lyzr import Studio
       studio = Studio(api_key=os.getenv("LYZR_API_KEY", "YOUR_KEY"))

       agent = studio.create_agent(
           name="Memory Agent", provider="openai/gpt-4o",
           role="Assistant", goal="Have coherent conversations",
           instructions="Remember context from earlier in our conversation."
       )

[md]  ## Session IDs for multi-turn conversations
      Pass the same session_id to link messages into one conversation.

[code] session = str(uuid.uuid4())
       print(f"Session: {session}")

       r1 = agent.run("My name is Alice.", session_id=session)
       print(f"Turn 1: {r1.response}")

       r2 = agent.run("What is my name?", session_id=session)
       print(f"Turn 2: {r2.response}")  # Should say "Alice"

[md]  ## Without session_id — no memory

[code] r3 = agent.run("What is my name?")  # new session each time
       print(f"No session: {r3.response}")  # Won't know "Alice"

[md]  ## Enabling built-in memory

[code] agent.add_memory(max_messages=10)

       session2 = str(uuid.uuid4())
       agent.run("I love hiking and coffee.", session_id=session2)
       r = agent.run("What are my hobbies?", session_id=session2)
       print(r.response)

[md]  ## Removing memory

[code] agent.remove_memory()
       r = agent.run("What are my hobbies?", session_id=session2)
       print(r.response)  # Won't remember anymore

[md]  ## Common mistake: different session IDs

[code] # ❌ Each run gets a different session - no continuity
       agent.run("My name is Bob.")          # session A
       r = agent.run("What is my name?")     # session B
       print(r.response)                     # Won't say "Bob"

[md]  ## Exercise + Summary + Next Steps
```

**Step: Write notebook, verify, commit.**

---

## Task 6: `notebooks/06_tools_and_functions.ipynb`

**Concepts:** Python functions as tools, `add_tool`, docstrings matter, tool calling flow
**Difficulty:** Intermediate · ~30 min

**Key cells:**

```
[md]  # Lesson 6: Custom Tools & Functions

[code] import os
       from lyzr import Studio
       studio = Studio(api_key=os.getenv("LYZR_API_KEY", "YOUR_KEY"))

[md]  ## What are tools?
      Tools are Python functions the agent can call to take actions
      or fetch real-time data. The agent decides WHEN to call them.

[md]  ## Defining a tool function
      The docstring is critical — it tells the agent what the tool does.

[code] def get_weather(city: str) -> str:
           """Get the current weather for a city. Returns temperature and conditions."""
           # In real life this would call a weather API
           weather_data = {
               "london": "15°C, cloudy",
               "tokyo": "22°C, sunny",
               "new york": "18°C, partly cloudy"
           }
           return weather_data.get(city.lower(), f"Weather data not available for {city}")

[code] agent = studio.create_agent(
           name="Weather Agent",
           provider="openai/gpt-4o",
           role="Weather assistant",
           goal="Help users with weather information",
           instructions="Use the get_weather tool when asked about weather."
       )

       agent.add_tool(get_weather)

       response = agent.run("What's the weather like in London?")
       print(response.response)

[md]  ## Multiple tools

[code] def calculate(expression: str) -> float:
           """Evaluate a mathematical expression and return the result."""
           return eval(expression)

       def word_count(text: str) -> int:
           """Count the number of words in a text string."""
           return len(text.split())

       multi_agent = studio.create_agent(
           name="Multi-Tool Agent", provider="openai/gpt-4o",
           role="Utility assistant", goal="Perform calculations and text analysis",
           instructions="Use tools when needed."
       )
       multi_agent.add_tool(calculate)
       multi_agent.add_tool(word_count)

       r = multi_agent.run("How many words are in 'the quick brown fox' and what is 144/12?")
       print(r.response)

[md]  ## Common mistake: missing docstring

[code] def no_docs(x):
           return x * 2
       # ❌ Agent can't understand what this tool does without a docstring

[md]  ## Exercise + Summary + Next Steps
```

**Step: Write notebook, verify, commit.**

---

## Task 7: `notebooks/07_knowledge_bases_rag.ipynb`

**Concepts:** `create_knowledge_base`, `add_text`, `add_website`, `query`, `top_k`, attach to agent
**Difficulty:** Intermediate · ~30 min

**Key cells:**

```
[md]  # Lesson 7: RAG & Knowledge Bases

[code] import os
       from lyzr import Studio
       studio = Studio(api_key=os.getenv("LYZR_API_KEY", "YOUR_KEY"))

[md]  ## What is RAG?
      Retrieval-Augmented Generation: agent retrieves relevant chunks
      from your documents before answering. Grounds responses in your data.

[md]  ## Creating a knowledge base

[code] kb = studio.create_knowledge_base(name="Product FAQ")
       print(f"Knowledge base created: {kb.id}")

[md]  ## Adding text content

[code] kb.add_text(
           text="""
           Q: What is lyzr-adk?
           A: Lyzr ADK is a Python SDK for building production-ready AI agents.

           Q: What LLM providers are supported?
           A: OpenAI, Anthropic, Google, Groq, Perplexity, and AWS Bedrock.

           Q: Is there a free tier?
           A: Yes. Sign up at lyzr.ai to get started with free credits.
           """,
           source="product-faq"
       )
       print("Text added.")

[md]  ## Adding a website

[code] kb.add_website(url="https://docs.lyzr.ai", max_pages=5, max_depth=1)
       print("Website added.")

[md]  ## Querying the knowledge base directly

[code] results = kb.query("What providers does lyzr support?", top_k=3)
       for r in results:
           print(f"Score: {r.score:.2f} | {r.text[:100]}...")

[md]  ## Attaching KB to an agent

[code] agent = studio.create_agent(
           name="FAQ Bot", provider="openai/gpt-4o",
           role="Support agent", goal="Answer questions using the knowledge base",
           instructions="Only answer from the provided knowledge base. Say 'I don't know' if not found."
       )

       # Attach KB — agent now retrieves before answering
       # (follow lyzr-adk docs for exact attach API)

       response = agent.run("What LLM providers does Lyzr support?")
       print(response.response)

[md]  ## Listing and resetting documents

[code] docs = kb.list_documents()
       print(f"Documents in KB: {len(docs)}")
       for doc in docs:
           print(f"  - {doc.id}: {doc.source}")

[md]  ## Exercise + Summary + Next Steps
```

**Step: Write notebook, verify, commit.**

---

## Task 8: `notebooks/08_contexts.ipynb`

**Concepts:** `create_context`, `add_context`, `remove_context`, `update`, dynamic background info
**Difficulty:** Intermediate · ~20 min

**Key cells:**

```
[md]  # Lesson 8: Dynamic Contexts

[code] import os
       from lyzr import Studio
       studio = Studio(api_key=os.getenv("LYZR_API_KEY", "YOUR_KEY"))

[md]  ## What are contexts?
      Contexts inject key-value background information into every agent
      request. Useful for: user profile, current date, company info,
      environment flags — anything the agent should always know.

[md]  ## Creating a context

[code] user_ctx = studio.create_context(
           name="user_profile",
           value="User: Alice, Role: Senior Engineer, Timezone: UTC+5:30"
       )
       print(f"Context created: {user_ctx.id}")

[md]  ## Attaching context to an agent

[code] agent = studio.create_agent(
           name="Personalized Assistant", provider="openai/gpt-4o",
           role="Personal assistant", goal="Give personalized responses",
           instructions="Use the user profile context to personalize your responses."
       )
       agent.add_context(user_ctx)

       r = agent.run("What time zone should I schedule my meeting for?")
       print(r.response)  # Should mention UTC+5:30

[md]  ## Updating a context value

[code] user_ctx.update("User: Alice, Role: Engineering Manager, Timezone: UTC+5:30")
       r2 = agent.run("What is my current role?")
       print(r2.response)  # Should say "Engineering Manager"

[md]  ## Multiple contexts

[code] company_ctx = studio.create_context(
           name="company_info",
           value="Company: Acme Corp, Industry: SaaS, Founded: 2020"
       )
       agent.add_context(company_ctx)

       r3 = agent.run("Tell me about my company.")
       print(r3.response)

[md]  ## Removing a context

[code] agent.remove_context(user_ctx)
       r4 = agent.run("What is my timezone?")
       print(r4.response)  # Won't know anymore

[md]  ## Exercise + Summary + Next Steps
```

**Step: Write notebook, verify, commit.**

---

## Task 9: `notebooks/09_rai_guardrails.ipynb`

**Concepts:** `create_rai_policy`, toxicity, PII (block/redact/mask), topic filter, `add_rai_policy`
**Difficulty:** Advanced · ~30 min

**Key cells:**

```
[md]  # Lesson 9: Responsible AI Guardrails

[code] import os
       from lyzr import Studio
       studio = Studio(api_key=os.getenv("LYZR_API_KEY", "YOUR_KEY"))

[md]  ## Why guardrails?
      Production agents need safety layers: prevent harmful content,
      protect user PII, block off-topic requests, stop prompt injection.

[md]  ## Creating a basic RAI policy

[code] policy = studio.create_rai_policy(
           name="Basic Safety",
           toxicity=True,
           nsfw=True,
           prompt_injection=True
       )
       print(f"Policy created: {policy.id}")

[md]  ## PII protection modes

[code] # Three modes:
       # "block"  — reject the message entirely
       # "redact" — remove PII from input before sending to LLM
       # "mask"   — replace PII with placeholders like [EMAIL]

       pii_policy = studio.create_rai_policy(
           name="PII Protection",
           pii="redact"   # or "block" or "mask"
       )

[md]  ## Topic filtering

[code] topic_policy = studio.create_rai_policy(
           name="On-Topic Only",
           banned_topics=["politics", "religion", "competitors"],
           allowed_topics=["technology", "programming", "AI"]
       )

[md]  ## Attaching policy to agent

[code] safe_agent = studio.create_agent(
           name="Safe Agent", provider="openai/gpt-4o",
           role="Customer support bot",
           goal="Help customers with product questions only",
           instructions="Stay on topic. Be professional."
       )
       safe_agent.add_rai_policy(policy)

       # Test: normal message
       r1 = safe_agent.run("How do I reset my password?")
       print(f"Normal: {r1.response}")

       # Test: off-topic (will be blocked/redirected)
       r2 = safe_agent.run("Tell me something offensive.")
       print(f"Blocked: {r2.response}")

[md]  ## Note: streaming is disabled when RAI is active

[code] # ❌ This won't work with RAI policies active:
       # agent.run(message, stream=True)
       # RAI requires full content inspection before delivery.

[md]  ## Exercise + Summary + Next Steps
```

**Step: Write notebook, verify, commit.**

---

## Task 10: `notebooks/10_capstone_project.ipynb`

**Concepts:** Combines lessons 1–9 into a full "Research Assistant" agent
**Difficulty:** Advanced · ~45 min

**What it builds:** A research assistant that:
- Uses a knowledge base (RAG) with injected text
- Has memory for multi-turn research sessions
- Has a `web_search` stub tool
- Has RAI guardrails for PII and toxicity
- Uses structured output for a `ResearchReport` Pydantic model
- Accepts dynamic context (current project name)

**Key cells:**

```
[md]  # Lesson 10: Capstone — Full Research Assistant Agent
      This lesson builds a production-grade agent combining every
      concept from lessons 1–9.

[code] # Full setup: all imports, Studio init
       import os, uuid
       from lyzr import Studio
       from pydantic import BaseModel, Field
       from typing import List
       studio = Studio(api_key=os.getenv("LYZR_API_KEY", "YOUR_KEY"))

[md]  ## Step 1: Define structured output

[code] class ResearchReport(BaseModel):
           topic: str
           summary: str
           key_findings: List[str]
           confidence: float = Field(ge=0.0, le=1.0)
           sources: List[str]

[md]  ## Step 2: Create knowledge base

[code] kb = studio.create_knowledge_base(name="Research KB")
       kb.add_text(text="...", source="background-docs")

[md]  ## Step 3: Define tools

[code] def search_web(query: str) -> str:
           """Search the web for current information on a topic."""
           return f"[Simulated search results for: {query}]"

[md]  ## Step 4: Create RAI policy

[code] policy = studio.create_rai_policy(
           name="Research Safety", toxicity=True, pii="redact"
       )

[md]  ## Step 5: Create context

[code] project_ctx = studio.create_context(
           name="project", value="Project: AI Market Analysis 2026"
       )

[md]  ## Step 6: Assemble the agent

[code] agent = studio.create_agent(
           name="Research Assistant",
           provider="openai/gpt-4o",
           role="Senior research analyst",
           goal="Produce structured research reports grounded in facts",
           instructions="..."
       )
       agent.add_tool(search_web)
       agent.add_memory(max_messages=20)
       agent.add_context(project_ctx)
       agent.add_rai_policy(policy)
       print("Research assistant ready.")

[md]  ## Step 7: Run a research session

[code] session = str(uuid.uuid4())

       r1 = agent.run("What are the top AI trends in 2026?", session_id=session)
       print(r1.response)

       report = agent.run(
           "Compile a formal report on AI agent frameworks.",
           session_id=session,
           response_format=ResearchReport
       )
       data: ResearchReport = report.response
       print(f"Topic: {data.topic}")
       print(f"Findings: {data.key_findings}")
       print(f"Confidence: {data.confidence}")

[md]  ## Congratulations!
      You've built a production-ready AI agent using:
      ✅ Custom LLM provider   ✅ Knowledge base (RAG)
      ✅ Custom tools          ✅ Conversation memory
      ✅ Structured outputs    ✅ Dynamic contexts
      ✅ RAI guardrails

      → Explore the [Lyzr docs](https://docs.lyzr.ai) for deployment options.
```

**Step: Write notebook, verify, commit.**

**Final commit:**
```bash
git add notebooks/
git commit -m "feat: complete 10-lesson lyzr-adk notebook series"
```

---

## Execution Order

Tasks must be done sequentially (each notebook builds on vocabulary from previous ones):

```
Task 0 (scaffold) → Task 1 → Task 2 → Task 3 → ... → Task 10
```

Each task = write notebook → restart kernel & run all → commit.
