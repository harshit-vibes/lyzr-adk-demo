# Bonus Lessons 14 & 15 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create two bonus Jupyter notebooks — a WhatsApp Business co-pilot (Lesson 14) and a multi-agent e-commerce support system (Lesson 15) — each runnable top-to-bottom without real credentials.

**Architecture:** Both notebooks follow the same fixed schema as lessons 1–13 (header → prerequisites → setup → concept sections → common mistake → exercise → summary → next steps). Lesson 14 uses the Meta Cloud API architecture with full simulation mode. Lesson 15 uses the agent-as-tool pattern where three sub-agents are wrapped as Python functions and added to a manager agent via `add_tool()`.

**Tech Stack:** Python 3.8+, `lyzr-adk` (pip), `fastapi`, `uvicorn`, `pydantic`, Jupyter / Google Colab

---

## lyzr-adk API Reference (use in all cells)

```python
from lyzr import Studio
studio = Studio(api_key="YOUR_LYZR_API_KEY")

agent = studio.create_agent(
    name="...",
    provider="openai/gpt-4o",   # or anthropic/claude-sonnet-4-5
    role="...",
    goal="...",
    instructions="...",
    response_model=None,        # optional Pydantic class — goes here NOT in run()
)
response = agent.run(message, session_id=None, stream=False)
print(response.response)        # .response is always a string

# Tools: any Python function with a clear docstring
agent.add_tool(my_function)

# Memory
agent.add_memory(max_messages=10)

# RAI
policy = studio.create_rai_policy(name="...", toxicity=True, pii="redact")
agent.add_rai_policy(policy)
```

**CRITICAL:** `response_model` goes in `create_agent()`, NOT in `run()`. When `response_model` is set, `run()` returns the Pydantic object directly (no `.response` wrapper).

---

## Notebook Cell Format

Use `nbformat` v4. All notebooks must be created with `nbformat.write()` or the NotebookEdit tool. Each cell uses:
```python
nbf.new_markdown_cell(source)   # for markdown
nbf.new_code_cell(source)       # for code
```

Cell IDs follow the pattern: `"a1b2c3d4-14NN-4000-8000-000000000000"` for lesson 14,
`"a1b2c3d4-15NN-4000-8000-000000000000"` for lesson 15.

---

## Task 1: Lesson 14 — WhatsApp Business Co-pilot

**Files:**
- Create: `notebooks/14_whatsapp_business_copilot.ipynb`

**Architecture for this notebook:**

```
[Simulated WhatsApp Message]
         │
         ▼
   FastAPI webhook receiver  ← shown as code, not run inline
         │
         ▼
   lyzr-adk agent
   ├── Tool: lookup_order(order_id)
   ├── Tool: send_whatsapp_reply(to, msg)  ← simulated: prints instead of calling Meta API
   ├── Memory: session_id = customer phone number
   └── RAI: toxicity filter
         │
         ▼
   WhatsApp reply (simulated)
```

**Step 1: Write Cell 1 — Title and overview**

```markdown
# Lesson 14: WhatsApp Business Co-pilot

🔴 **Advanced** · ⏱ **35 min**

---

In production, AI agents often need to operate inside messaging channels rather than APIs.
WhatsApp Business is the world's most-used messaging platform.
This lesson shows how to wire a lyzr-adk agent into the Meta WhatsApp Cloud API architecture —
including a webhook receiver, order lookup tool, and customer session memory.

Every cell in this notebook is **runnable in simulation mode** — no real Meta credentials needed.
The architecture is identical to a production deployment; only the `send_whatsapp_reply` tool
is simulated (it prints instead of calling the Meta API).

## What you'll learn

- Understand the Meta WhatsApp Cloud API webhook architecture
- Build a customer service agent with order lookup tool
- Use `session_id = customer_phone` for per-customer conversation memory
- Simulate an end-to-end WhatsApp conversation (inquiry → order lookup → escalation)
- See the complete production FastAPI webhook receiver code
```

**Step 2: Write Cell 2 — Prerequisites**

```markdown
## Prerequisites

Before running this notebook, you should be familiar with:

- **Lesson 1** — Studio & `agent.run()` basics
- **Lesson 5** — Memory & sessions (`session_id` pattern)
- **Lesson 6** — Custom tools (`agent.add_tool()`, docstrings)
- **Lesson 9** — RAI guardrails (optional but helpful)

You also need your **`LYZR_API_KEY`** set as an environment variable:

```bash
export LYZR_API_KEY="your-api-key-here"
```

> **Note:** No Meta/WhatsApp credentials are required for this notebook.
> All WhatsApp sends are simulated by printing to stdout.
```

**Step 3: Write Cell 3 — Install**

```python
!pip install lyzr-adk fastapi uvicorn -q
```

**Step 4: Write Cell 4 — Imports and Studio init**

```python
import os
import uuid
from lyzr import Studio

API_KEY = os.getenv("LYZR_API_KEY", "YOUR_LYZR_API_KEY")
studio = Studio(api_key=API_KEY)
print("Ready!")
```

**Step 5: Write Cell 5 — Section 1 markdown: Architecture**

```markdown
## 1. Architecture Overview

A production WhatsApp Business integration has three layers:

| Layer | What it does |
|---|---|
| **Meta Webhook** | Meta sends a POST to your server when a customer messages you |
| **FastAPI receiver** | Your server validates the request and routes the message to your agent |
| **lyzr-adk agent** | Processes the message, calls tools, and replies via the Meta API |

```
Customer → [WhatsApp] → Meta servers → POST /webhook → FastAPI → lyzr-adk agent
                                                                         │
                                                               tool: lookup_order()
                                                               tool: send_whatsapp_reply()
                                                                         │
                                                               Reply → Meta API → Customer
```

In **simulation mode** (this notebook), we skip the HTTP layer and call the agent directly,
exactly as the webhook handler would. The `send_whatsapp_reply` tool prints instead of calling Meta.
```

**Step 6: Write Cell 6 — Section 2 markdown: Tools**

```markdown
## 2. Building the Tools

Two tools power this agent:

1. **`lookup_order`** — queries a simulated order database by order ID
2. **`send_whatsapp_reply`** — in production calls `https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages`;
   in simulation mode, prints to stdout

The docstring is critical for both: the agent reads it to decide when and with what arguments to call each tool.
```

**Step 7: Write Cell 7 — Tool definitions**

```python
# Tool 1: Order lookup (simulated database)
ORDERS = {
    "ORD-1001": {"status": "shipped",    "delivery": "2026-02-26", "carrier": "FedEx", "tracking": "FX123456"},
    "ORD-1002": {"status": "processing", "delivery": "2026-02-28", "carrier": "UPS",   "tracking": "UP789012"},
    "ORD-1003": {"status": "delivered",  "delivery": "2026-02-20", "carrier": "DHL",   "tracking": "DH345678"},
}

def lookup_order(order_id: str) -> str:
    """Look up a customer order by order ID and return its current status.

    Returns the shipping status, carrier name, tracking number, and estimated delivery date.
    Use this whenever a customer asks about the status, location, or delivery date of their order.
    Order IDs follow the format ORD-XXXX.
    """
    if order_id.upper() in ORDERS:
        o = ORDERS[order_id.upper()]
        return (
            f"Order {order_id.upper()}: {o['status']} via {o['carrier']} "
            f"(tracking: {o['tracking']}), estimated delivery: {o['delivery']}"
        )
    return f"Order {order_id} not found. Please verify the order ID and try again."


# Tool 2: WhatsApp reply sender (simulated)
def send_whatsapp_reply(to_number: str, message: str) -> str:
    """Send a WhatsApp reply message to a customer's phone number.

    Use this to deliver the final response back to the customer over WhatsApp.
    Always call this at the end of handling a customer request.
    In production this calls the Meta Cloud API. In simulation it prints the message.
    """
    print(f"\n📱 [WhatsApp → {to_number}]\n{message}\n")
    return f"Message delivered to {to_number}"


print("Tools defined: lookup_order, send_whatsapp_reply")
```

**Step 8: Write Cell 8 — Section 3 markdown: Create agent**

```markdown
## 3. Creating the WhatsApp Co-pilot Agent

The agent needs:
- A **role** that establishes it as a customer service agent
- The two tools attached via `agent.add_tool()`
- **Memory** enabled so it remembers context within a WhatsApp conversation thread
- A **RAI policy** to filter harmful or inappropriate messages

We use the customer's phone number as the `session_id` — this means each phone number gets
its own isolated conversation history automatically.
```

**Step 9: Write Cell 9 — Create agent**

```python
# Create the WhatsApp co-pilot agent
whatsapp_agent = studio.create_agent(
    name="WhatsApp Business Co-pilot",
    provider="openai/gpt-4o",
    role="Customer service representative for an e-commerce business",
    goal="Help customers with order inquiries, product questions, and support requests via WhatsApp",
    instructions=(
        "You are a friendly, concise customer service agent. "
        "Always look up order status when a customer provides an order ID. "
        "Use send_whatsapp_reply to deliver your response to the customer. "
        "Keep replies under 300 characters (WhatsApp best practice). "
        "If a customer asks to speak to a human, acknowledge it and say a team member will follow up within 1 hour."
    )
)

# Attach tools
whatsapp_agent.add_tool(lookup_order)
whatsapp_agent.add_tool(send_whatsapp_reply)

# Enable memory — keyed by session_id (customer phone number)
whatsapp_agent.add_memory(max_messages=10)

# RAI: filter harmful content
rai_policy = studio.create_rai_policy(
    name="WhatsApp RAI Policy",
    toxicity=True,
    pii="redact"
)
whatsapp_agent.add_rai_policy(rai_policy)

print(f"Agent ready: {whatsapp_agent.id}")
```

**Step 10: Write Cell 10 — Section 4 markdown: Simulation**

```markdown
## 4. Simulating a Customer Conversation

In production, each inbound WhatsApp message triggers one call to your webhook, which calls
`agent.run(message, session_id=customer_phone)`. We simulate three turns of a real
customer journey:

1. **Product inquiry** — customer asks about a product
2. **Order status** — customer provides their order ID
3. **Escalation** — customer requests a human agent

The `session_id` is the customer's phone number. This ensures the agent remembers context
across all three turns — just as it would in a real WhatsApp thread.
```

**Step 11: Write Cell 11 — Simulate conversation**

```python
# Simulate a customer WhatsApp conversation
CUSTOMER_PHONE = "+1-555-0147"

print("=" * 60)
print(f"Customer: {CUSTOMER_PHONE}")
print("=" * 60)

# Turn 1: Product inquiry
print("\n[Customer]: Do you have wireless headphones? What's the price range?")
r1 = whatsapp_agent.run(
    "Do you have wireless headphones? What's the price range?",
    session_id=CUSTOMER_PHONE
)
print(f"[Agent internal]: {r1.response}")

# Turn 2: Order status lookup
print("\n[Customer]: I placed order ORD-1001 last week. Where is it?")
r2 = whatsapp_agent.run(
    "I placed order ORD-1001 last week. Where is it?",
    session_id=CUSTOMER_PHONE
)
print(f"[Agent internal]: {r2.response}")

# Turn 3: Escalation
print("\n[Customer]: I'd like to speak with a human agent please.")
r3 = whatsapp_agent.run(
    "I'd like to speak with a human agent please.",
    session_id=CUSTOMER_PHONE
)
print(f"[Agent internal]: {r3.response}")
```

**Step 12: Write Cell 12 — Section 5 markdown: Production FastAPI code**

```markdown
## 5. Production Webhook (FastAPI)

In production, replace the direct `agent.run()` calls with this FastAPI webhook receiver.
Meta POSTs to `/webhook` every time a customer sends a WhatsApp message.

This code is **shown here for reference** — it is not run inline in this notebook (it requires
a public HTTPS URL for Meta to reach). Save it as `whatsapp_webhook.py` and run with
`uvicorn whatsapp_webhook:app --host 0.0.0.0 --port 8000`.

```python
# whatsapp_webhook.py — production webhook receiver
from fastapi import FastAPI, Request
from lyzr import Studio
import os

app = FastAPI()
studio = Studio(api_key=os.environ["LYZR_API_KEY"])

# Re-create agent (or load by ID: studio.get_agent("agent-id"))
agent = studio.create_agent(...)
agent.add_tool(lookup_order)
agent.add_tool(send_whatsapp_reply)
agent.add_memory(max_messages=10)

@app.get("/webhook")
async def verify(hub_mode: str, hub_challenge: str, hub_verify_token: str):
    """Meta webhook verification handshake."""
    if hub_verify_token == os.environ["WEBHOOK_VERIFY_TOKEN"]:
        return int(hub_challenge)
    return {"error": "Invalid verify token"}, 403

@app.post("/webhook")
async def receive_message(request: Request):
    """Handle inbound WhatsApp messages."""
    body = await request.json()
    entry = body["entry"][0]["changes"][0]["value"]
    message = entry["messages"][0]
    from_number = message["from"]
    text = message["text"]["body"]

    # Use customer phone number as session ID for per-customer memory
    agent.run(text, session_id=from_number)
    return {"status": "ok"}
```
```

**Step 13: Write Cell 13 — Section 6 markdown: Common mistake**

```markdown
## Common Mistake: Not Using `session_id`

The most critical mistake with WhatsApp integrations is **forgetting `session_id`** or
using a random one each turn. Without it, the agent starts fresh every message — it has
no idea what the customer said previously.

| Turn | Without `session_id` | With `session_id=phone` |
|---|---|---|
| Turn 1 | "Hi, my order is ORD-1001" | "Hi, my order is ORD-1001" |
| Turn 2 | "Where is it?" → ❌ "Where is what?" | "Where is it?" → ✅ looks up ORD-1001 |
| Turn 3 | "Cancel it" → ❌ confused | "Cancel it" → ✅ cancels ORD-1001 |

**Rule:** Always pass `session_id=customer_phone` to keep each customer's conversation coherent.
```

**Step 14: Write Cell 14 — Demonstrate the mistake**

```python
# ❌ Mistake: different session_id each turn (or no session_id)
print("WITHOUT session_id (each turn is isolated):\n")

r1 = whatsapp_agent.run("Hi, my order is ORD-1001", session_id=str(uuid.uuid4()))
print(f"Turn 1: {r1.response[:100]}...")

r2 = whatsapp_agent.run("Where is it?", session_id=str(uuid.uuid4()))  # new session!
print(f"Turn 2: {r2.response[:100]}...")  # agent has no idea what "it" refers to

print("\n✅ Solution: use session_id=customer_phone for the entire conversation thread")
```

**Step 15: Write Cell 15 — Exercise markdown**

```markdown
## Exercise: Add a "Track Shipment" Tool

Your task is to add a third tool to the WhatsApp agent that provides detailed tracking
information for a shipment.

**Steps:**

1. Write a `track_shipment(tracking_number: str) -> str` function with a clear docstring
2. Add simulated tracking events (e.g., "Package picked up", "In transit", "Out for delivery")
3. Attach the tool to `whatsapp_agent` with `whatsapp_agent.add_tool(track_shipment)`
4. Test it: ask the agent "Can you track FX123456 for me?"

Fill in the `...` placeholders below.
```

**Step 16: Write Cell 16 — Exercise scaffold**

```python
# Simulated tracking database
TRACKING_EVENTS = {
    "FX123456": [
        "2026-02-23 09:00 — Package picked up at seller warehouse",
        "2026-02-23 18:30 — In transit to regional sort facility",
        "2026-02-24 06:00 — Arrived at regional sort facility",
        "2026-02-25 08:00 — Out for delivery",
    ],
    "UP789012": [
        "2026-02-24 10:00 — Package picked up",
        "2026-02-24 20:00 — Processing at origin facility",
    ],
}

# TODO: Write a track_shipment tool function with a clear docstring
def track_shipment(tracking_number: str) -> str:
    """..."""  # TODO: Write a clear docstring — this is what the agent reads!
    # TODO: Look up tracking_number in TRACKING_EVENTS
    # Return all events as a formatted string, or a helpful message if not found
    ...


# TODO: Add the tool to whatsapp_agent
# whatsapp_agent.add_tool(...)

# TODO: Test the agent
# response = whatsapp_agent.run("Can you track FX123456 for me?", session_id="+1-555-0147")
# print(response.response)
```

**Step 17: Write Cell 17 — Summary**

```markdown
## Summary

### WhatsApp Business Co-pilot Architecture

| Component | Implementation |
|---|---|
| Inbound message | Meta webhook POST → FastAPI `/webhook` endpoint |
| Agent | `studio.create_agent()` with customer service role |
| Order lookup | `lookup_order(order_id)` tool — reads from DB/API |
| Reply | `send_whatsapp_reply(to, msg)` tool — calls Meta Graph API |
| Conversation memory | `session_id=customer_phone` — one session per customer |
| Safety | `studio.create_rai_policy(toxicity=True, pii="redact")` |

### Key Takeaways

- Use `session_id=customer_phone` — this is the unique identifier for each WhatsApp thread
- The agent-as-webhook pattern is: receive message → `agent.run(text, session_id=phone)` → tool sends reply
- Any business logic (order lookup, CRM queries, inventory checks) becomes a tool with a clear docstring
- Keep WhatsApp replies under 300 characters — set this expectation in `instructions`
- Simulation mode (print instead of call Meta) lets you develop and test without credentials

### Meta Cloud API Quick Reference

```python
# Production send (replaces the simulated send_whatsapp_reply)
import httpx

def send_whatsapp_reply(to_number: str, message: str) -> str:
    """Send a WhatsApp message via Meta Cloud API."""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    r = httpx.post(url, json=payload, headers=headers)
    return f"Sent: {r.status_code}"
```
```

**Step 18: Write Cell 18 — Next Steps**

```markdown
## Next Steps

You have completed Lesson 14. From here you can:

- **Lesson 15: Multi-agent E-commerce** — build a manager agent that routes customer
  queries to three specialist sub-agents using the agent-as-tool pattern

---

| Lesson | Topic |
|---|---|
| [01](./01_getting_started.ipynb) | Getting Started |
| [05](./05_memory_and_sessions.ipynb) | Memory & Sessions |
| [06](./06_tools_and_functions.ipynb) | Tools & Functions |
| [09](./09_rai_guardrails.ipynb) | RAI Guardrails |
| **14** | **WhatsApp Co-pilot (this lesson)** |
| [15](./15_multi_agent_ecommerce.ipynb) | Multi-agent E-commerce |
```

**Step 19: Assemble notebook with nbformat and write to disk**

```python
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.8.0"}}

cells = [
    nbf.v4.new_markdown_cell(CELL_01_SOURCE),
    nbf.v4.new_markdown_cell(CELL_02_SOURCE),
    nbf.v4.new_code_cell(CELL_03_SOURCE),
    nbf.v4.new_code_cell(CELL_04_SOURCE),
    nbf.v4.new_markdown_cell(CELL_05_SOURCE),
    nbf.v4.new_markdown_cell(CELL_06_SOURCE),
    nbf.v4.new_code_cell(CELL_07_SOURCE),
    nbf.v4.new_markdown_cell(CELL_08_SOURCE),
    nbf.v4.new_code_cell(CELL_09_SOURCE),
    nbf.v4.new_markdown_cell(CELL_10_SOURCE),
    nbf.v4.new_code_cell(CELL_11_SOURCE),
    nbf.v4.new_markdown_cell(CELL_12_SOURCE),
    nbf.v4.new_markdown_cell(CELL_13_SOURCE),
    nbf.v4.new_code_cell(CELL_14_SOURCE),
    nbf.v4.new_markdown_cell(CELL_15_SOURCE),
    nbf.v4.new_code_cell(CELL_16_SOURCE),
    nbf.v4.new_markdown_cell(CELL_17_SOURCE),
    nbf.v4.new_markdown_cell(CELL_18_SOURCE),
]

for i, cell in enumerate(cells):
    cell.id = f"a1b2c3d4-14{i+1:02d}-4000-8000-000000000000"
nb.cells = cells

with open("notebooks/14_whatsapp_business_copilot.ipynb", "w") as f:
    nbf.write(nb, f)

print("notebooks/14_whatsapp_business_copilot.ipynb written ✅")
```

**Step 20: Commit**

```bash
git add notebooks/14_whatsapp_business_copilot.ipynb
git commit -m "feat: add lesson 14 — WhatsApp Business Co-pilot"
```

---

## Task 2: Lesson 15 — Multi-agent E-commerce Support

**Files:**
- Create: `notebooks/15_multi_agent_ecommerce.ipynb`

**Architecture for this notebook:**

```
Customer message
      │
      ▼
 Manager Agent
 ├── tool: handle_order_query()   ─→  OrderAgent.run()
 ├── tool: handle_product_query() ─→  ProductAgent.run()
 └── tool: handle_billing_query() ─→  BillingAgent.run()
      │
      ▼
 Synthesized reply to customer
```

Each sub-agent is a regular `studio.create_agent()` call. The wrapper functions are what the manager calls via `add_tool()`. The docstring on each wrapper is critical — it tells the manager LLM when to route to which specialist.

**Step 1: Write Cell 1 — Title and overview**

```markdown
# Lesson 15: Multi-agent E-commerce Support System

🔴 **Advanced** · ⏱ **35 min**

---

Real customer support pipelines rarely use a single agent. Complex queries may span orders,
billing, and product knowledge — domains that benefit from specialization.

In this lesson you will build a **manager + 3 specialist sub-agents** system for e-commerce
customer support. The manager receives every customer message and routes it to the right
specialist by calling it as a Python tool.

## What you'll learn

- Build multiple specialist sub-agents with distinct roles
- Wrap sub-agents as Python tool functions
- Add sub-agent tools to a manager agent
- Understand how the manager uses docstrings to route queries
- Handle multi-domain queries where the manager calls more than one sub-agent
- See the common mistake: vague docstrings cause incorrect routing
```

**Step 2: Write Cell 2 — Prerequisites**

```markdown
## Prerequisites

Before running this notebook, you should be familiar with:

- **Lesson 1** — Studio & `agent.run()` basics
- **Lesson 3** — Agent lifecycle (create, run, manage)
- **Lesson 6** — Custom tools — **especially docstrings** (critical for routing)
- **Lesson 5** — Memory & sessions (optional but helpful)

You also need your **`LYZR_API_KEY`** set as an environment variable:

```bash
export LYZR_API_KEY="your-api-key-here"
```
```

**Step 3: Write Cell 3 — Install**

```python
!pip install lyzr-adk -q
```

**Step 4: Write Cell 4 — Imports and Studio init**

```python
import os
import uuid
from lyzr import Studio

API_KEY = os.getenv("LYZR_API_KEY", "YOUR_LYZR_API_KEY")
studio = Studio(api_key=API_KEY)
print("Ready!")
```

**Step 5: Write Cell 5 — Section 1 markdown: Architecture**

```markdown
## 1. Architecture Overview

The **agent-as-tool** pattern is the simplest and most portable way to compose multiple agents.
Each specialist sub-agent is wrapped in a Python function and attached to the manager agent
as a regular tool.

```
Customer query
       │
       ▼
  Manager Agent  ──reads docstrings──▶  picks tool to call
       │
       ├──▶ handle_order_query()   ──▶  OrderAgent   (orders, returns, shipping)
       ├──▶ handle_product_query() ──▶  ProductAgent  (specs, availability, recommendations)
       └──▶ handle_billing_query() ──▶  BillingAgent  (payments, refunds, invoices)
```

**Why this pattern works:**
- Each sub-agent has a focused role → better, more accurate answers
- The manager never needs to know the implementation details of each specialist
- The docstring on each wrapper function is what guides the manager's routing decision
- Adding a new specialist = create agent + write wrapper function + `manager.add_tool(fn)`
```

**Step 6: Write Cell 6 — Section 2 markdown: Sub-agents**

```markdown
## 2. Creating the Specialist Sub-agents

Create three sub-agents, each with a tightly focused role, goal, and instructions.
The narrower the focus, the more reliably each sub-agent answers questions in its domain.
```

**Step 7: Write Cell 7 — Create three sub-agents**

```python
# Sub-agent 1: Order specialist
order_agent = studio.create_agent(
    name="Order Specialist",
    provider="openai/gpt-4o",
    role="E-commerce order management specialist",
    goal="Resolve all customer questions about orders, returns, cancellations, and shipping",
    instructions=(
        "You specialize exclusively in order management. "
        "For order status queries, always mention the order ID in your response. "
        "For return requests, confirm the return window (30 days) and the process. "
        "For cancellations, check if the order has shipped; if so, initiate a return instead. "
        "Keep responses concise and action-oriented."
    )
)
print(f"OrderAgent: {order_agent.id}")

# Sub-agent 2: Product specialist
product_agent = studio.create_agent(
    name="Product Specialist",
    provider="openai/gpt-4o",
    role="E-commerce product and inventory specialist",
    goal="Answer all customer questions about products, specifications, availability, and recommendations",
    instructions=(
        "You specialize exclusively in product knowledge. "
        "When asked about availability, always give a concrete answer (in stock / out of stock / pre-order). "
        "For product comparisons, use a clear table format. "
        "For recommendations, ask one clarifying question if needed, then suggest 2-3 options with reasoning. "
        "Never speculate about pricing or shipping — route those to the appropriate team."
    )
)
print(f"ProductAgent: {product_agent.id}")

# Sub-agent 3: Billing specialist
billing_agent = studio.create_agent(
    name="Billing Specialist",
    provider="openai/gpt-4o",
    role="E-commerce billing and payments specialist",
    goal="Resolve all billing issues, process refund requests, and answer payment and invoice questions",
    instructions=(
        "You specialize exclusively in billing and payments. "
        "For refund requests, confirm the amount and timeline (5–7 business days to original payment method). "
        "For payment failures, check for common causes (expired card, insufficient funds, bank block). "
        "For invoice requests, confirm what information is needed and the format available. "
        "Never discuss order logistics or product details — those are handled by other teams."
    )
)
print(f"BillingAgent: {billing_agent.id}")
```

**Step 8: Write Cell 8 — Section 3 markdown: Wrap as tools**

```markdown
## 3. Wrapping Sub-agents as Tools

Each sub-agent is wrapped in a Python function. This function:

1. Calls `sub_agent.run(query)` and returns the response string
2. Has a **precise docstring** — this is what the manager LLM reads to decide routing
3. Has a single `query: str` parameter — the manager extracts and passes the user's question

**The docstring is the routing logic.** Make it specific about what types of questions belong to each specialist. Vague or overlapping docstrings cause the manager to pick the wrong sub-agent.
```

**Step 9: Write Cell 9 — Wrapper functions**

```python
def handle_order_query(query: str) -> str:
    """Handle customer questions about orders, returns, cancellations, and shipping status.

    Use this tool for:
    - Order status and tracking ("Where is my order?", "Has ORD-1001 shipped?")
    - Return requests ("I want to return my purchase")
    - Order cancellations ("Can I cancel order ORD-1002?")
    - Delivery timeframe questions ("When will it arrive?")

    Do NOT use for product questions, billing issues, or payment problems.
    """
    response = order_agent.run(query)
    return response.response


def handle_product_query(query: str) -> str:
    """Answer customer questions about products, availability, specifications, and recommendations.

    Use this tool for:
    - Product availability ("Is the blue backpack in stock?")
    - Product specifications ("What are the dimensions of the standing desk?")
    - Product comparisons ("What's the difference between Model A and Model B?")
    - Purchase recommendations ("I need a laptop for video editing under $1500")

    Do NOT use for order status, billing, or payment questions.
    """
    response = product_agent.run(query)
    return response.response


def handle_billing_query(query: str) -> str:
    """Resolve billing issues, process refund requests, and answer payment and invoice questions.

    Use this tool for:
    - Refund requests ("I'd like a refund for my order")
    - Payment failures ("My card was declined")
    - Invoice requests ("I need an invoice for my purchase")
    - Billing statement questions ("I was charged twice")

    Do NOT use for order logistics, shipping, or product information.
    """
    response = billing_agent.run(query)
    return response.response


print("Wrapper functions defined: handle_order_query, handle_product_query, handle_billing_query")
```

**Step 10: Write Cell 10 — Section 4 markdown: Manager agent**

```markdown
## 4. Creating the Manager Agent

The manager agent:
- Has **no knowledge base, no RAG, no specialized knowledge** of its own
- Has all three wrapper functions added as tools
- Has instructions to route carefully based on query intent
- Will call multiple tools if a query spans domains

The manager's `instructions` should emphasize routing precision. It should never try to answer domain questions itself — its job is to understand intent and delegate.
```

**Step 11: Write Cell 11 — Create manager**

```python
manager_agent = studio.create_agent(
    name="Support Manager",
    provider="openai/gpt-4o",
    role="Customer support routing manager",
    goal="Route customer queries to the correct specialist and synthesize their responses",
    instructions=(
        "You are a support routing manager. You do NOT answer questions yourself. "
        "Always use the appropriate specialist tool for every customer query. "
        "For questions about orders or shipping: use handle_order_query. "
        "For questions about products or availability: use handle_product_query. "
        "For billing, payments, or refunds: use handle_billing_query. "
        "If a query spans multiple domains (e.g., order AND refund), call both relevant tools "
        "and synthesize their answers into a single coherent response. "
        "Never guess or answer from your own knowledge — always use a tool."
    )
)

manager_agent.add_tool(handle_order_query)
manager_agent.add_tool(handle_product_query)
manager_agent.add_tool(handle_billing_query)

print(f"Manager agent ready: {manager_agent.id}")
print("Tools: handle_order_query, handle_product_query, handle_billing_query")
```

**Step 12: Write Cell 12 — Section 5 markdown: End-to-end examples**

```markdown
## 5. End-to-end Examples

Let's run four scenarios through the manager:
1. A pure order query (routes to OrderAgent)
2. A pure product query (routes to ProductAgent)
3. A pure billing query (routes to BillingAgent)
4. An ambiguous multi-domain query (manager calls two tools and synthesizes)
```

**Step 13: Write Cell 13 — Run examples**

```python
# Example 1: Order query → routes to OrderAgent
print("=" * 60)
print("QUERY 1: Order status")
r1 = manager_agent.run("Hi, I placed order ORD-1001 last week. Can you tell me where it is?")
print(r1.response)

# Example 2: Product query → routes to ProductAgent
print("\n" + "=" * 60)
print("QUERY 2: Product recommendation")
r2 = manager_agent.run("I'm looking for a wireless keyboard for programming. Budget is $150. Any recommendations?")
print(r2.response)

# Example 3: Billing query → routes to BillingAgent
print("\n" + "=" * 60)
print("QUERY 3: Refund request")
r3 = manager_agent.run("I was charged twice for my last order. I'd like a refund for the duplicate charge.")
print(r3.response)

# Example 4: Multi-domain → manager calls both OrderAgent AND BillingAgent
print("\n" + "=" * 60)
print("QUERY 4: Multi-domain (order + refund)")
r4 = manager_agent.run("My order ORD-1002 still hasn't arrived and I want to cancel it and get a refund.")
print(r4.response)
```

**Step 14: Write Cell 14 — Common mistake markdown**

```markdown
## Common Mistake: Vague Tool Docstrings

If the docstrings on the wrapper functions are vague or overlapping, the manager picks the
wrong specialist — and you get incorrect or irrelevant answers.

**Bad docstring (vague):**
```python
def handle_order_query(query: str) -> str:
    """Handle customer questions."""  # ❌ too vague — what questions?
```

**Better docstring (specific):**
```python
def handle_order_query(query: str) -> str:
    """Handle questions about orders, returns, cancellations, and shipping status.
    Use for: order tracking, return requests, delivery questions.
    Do NOT use for: product specs, payment issues."""  # ✅ clear boundaries
```

**Rule:** Each tool's docstring must:
1. State clearly what kinds of queries it handles
2. Give 2-4 concrete examples
3. Say what it does NOT handle (avoids overlap with other tools)
```

**Step 15: Write Cell 15 — Demonstrate mistake**

```python
# Create an agent with vague docstrings to show what goes wrong
def bad_order_tool(query: str) -> str:
    """Handle customer questions."""  # ❌ vague
    return order_agent.run(query).response

def bad_product_tool(query: str) -> str:
    """Help customers."""  # ❌ vague
    return product_agent.run(query).response

bad_manager = studio.create_agent(
    name="Bad Manager Demo",
    provider="openai/gpt-4o",
    role="Support manager",
    goal="Route customer queries",
    instructions="Use the appropriate tool for each query."
)
bad_manager.add_tool(bad_order_tool)
bad_manager.add_tool(bad_product_tool)

# This query should go to the order tool, but with vague docstrings it may not
r = bad_manager.run("Where is my order ORD-1001?")
print(f"Bad manager response: {r.response[:150]}...")
print("\n✅ Fix: Write specific docstrings that clearly define each tool's domain.")
```

**Step 16: Write Cell 16 — Exercise markdown**

```markdown
## Exercise: Add a Shipping Agent

Your task is to extend the system with a fourth specialist — a shipping agent that
handles shipping cost estimates and delivery time predictions.

**Steps:**

1. Create a `ShippingAgent` with an appropriate role, goal, and instructions
2. Write a `handle_shipping_query(query: str) -> str` wrapper with a precise docstring
3. Add it to `manager_agent` with `manager_agent.add_tool(handle_shipping_query)`
4. Test with: "How much does express shipping to New York cost?" and verify the manager routes to your new agent

Fill in the `...` placeholders below.
```

**Step 17: Write Cell 17 — Exercise scaffold**

```python
# TODO: Create the shipping specialist sub-agent
shipping_agent = studio.create_agent(
    name=...,
    provider="openai/gpt-4o",
    role=...,
    goal=...,
    instructions=...
)

# TODO: Write a wrapper function with a precise docstring
def handle_shipping_query(query: str) -> str:
    """..."""  # TODO: Be specific about what shipping questions this handles
    # TODO: Call shipping_agent.run(query) and return the response string
    ...


# TODO: Add the new tool to the manager
# manager_agent.add_tool(handle_shipping_query)

# TODO: Test the routing
# r = manager_agent.run("How much does express shipping to New York cost?")
# print(r.response)
```

**Step 18: Write Cell 18 — Summary**

```markdown
## Summary

### Multi-agent Architecture Patterns

| Pattern | When to use | Complexity |
|---|---|---|
| **Agent-as-tool** (this lesson) | Each sub-agent is independent, manager routes | Low — uses existing `add_tool()` |
| Parallel agents | Sub-agents run concurrently, results merged | Medium |
| Pipeline agents | Each agent passes output to next | Medium |
| Hierarchical (nested managers) | Large systems with many domains | High |

### Key Takeaways

- **Agent-as-tool** = wrap `sub_agent.run(query)` in a Python function, attach to manager with `add_tool()`
- The **docstring on each wrapper** is the routing logic — make it precise with examples and exclusions
- The manager needs `instructions` that enforce tool-first routing (never answer from knowledge)
- For multi-domain queries, the manager automatically calls multiple tools and synthesizes the result
- Adding a new specialist: create agent + write wrapper + `manager.add_tool(fn)` — nothing else changes

### Quick Reference

```python
# 1. Create sub-agents
specialist = studio.create_agent(name="...", provider="openai/gpt-4o", role="...", ...)

# 2. Wrap as tool
def handle_specialist_query(query: str) -> str:
    """Specific docstring describing what queries this handles."""
    return specialist.run(query).response

# 3. Add to manager
manager.add_tool(handle_specialist_query)

# 4. Run — manager routes automatically
response = manager.run("customer message")
```
```

**Step 19: Write Cell 19 — Next Steps**

```markdown
## Next Steps

You have completed all 15 lessons in the lyzr-adk series.

**What to build next:**
- Combine Lesson 14 + Lesson 15: a multi-agent WhatsApp bot where the manager routes messages to order, product, and billing sub-agents
- Add RAG (Lesson 7) to the ProductAgent so it answers from your real product catalog
- Add memory (Lesson 5) to the manager so customers can refer back to earlier questions

---

| Lesson | Topic |
|---|---|
| [01](./01_getting_started.ipynb) | Getting Started |
| [06](./06_tools_and_functions.ipynb) | Tools & Functions |
| [07](./07_knowledge_bases_rag.ipynb) | Knowledge Bases (RAG) |
| [10](./10_capstone_project.ipynb) | Capstone Project |
| [14](./14_whatsapp_business_copilot.ipynb) | WhatsApp Co-pilot |
| **15** | **Multi-agent E-commerce (this lesson)** |
```

**Step 20: Assemble notebook with nbformat and write to disk**

```python
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.8.0"}}

cells = [
    nbf.v4.new_markdown_cell(CELL_01_SOURCE),
    nbf.v4.new_markdown_cell(CELL_02_SOURCE),
    nbf.v4.new_code_cell(CELL_03_SOURCE),
    nbf.v4.new_code_cell(CELL_04_SOURCE),
    nbf.v4.new_markdown_cell(CELL_05_SOURCE),
    nbf.v4.new_markdown_cell(CELL_06_SOURCE),
    nbf.v4.new_code_cell(CELL_07_SOURCE),
    nbf.v4.new_markdown_cell(CELL_08_SOURCE),
    nbf.v4.new_code_cell(CELL_09_SOURCE),
    nbf.v4.new_markdown_cell(CELL_10_SOURCE),
    nbf.v4.new_code_cell(CELL_11_SOURCE),
    nbf.v4.new_markdown_cell(CELL_12_SOURCE),
    nbf.v4.new_code_cell(CELL_13_SOURCE),
    nbf.v4.new_markdown_cell(CELL_14_SOURCE),
    nbf.v4.new_code_cell(CELL_15_SOURCE),
    nbf.v4.new_markdown_cell(CELL_16_SOURCE),
    nbf.v4.new_code_cell(CELL_17_SOURCE),
    nbf.v4.new_markdown_cell(CELL_18_SOURCE),
    nbf.v4.new_markdown_cell(CELL_19_SOURCE),
]

for i, cell in enumerate(cells):
    cell.id = f"a1b2c3d4-15{i+1:02d}-4000-8000-000000000000"
nb.cells = cells

with open("notebooks/15_multi_agent_ecommerce.ipynb", "w") as f:
    nbf.write(nb, f)

print("notebooks/15_multi_agent_ecommerce.ipynb written ✅")
```

**Step 21: Commit**

```bash
git add notebooks/15_multi_agent_ecommerce.ipynb
git commit -m "feat: add lesson 15 — multi-agent e-commerce support system"
```

---

## Task 3: Update README.md

**Files:**
- Modify: `README.md`

Add lessons 14 and 15 to the lesson table under a new "Bonus Lessons" section header.

**Step 1: Read current README.md**

Check current content around line 70 (end of Optional Advanced Lessons table).

**Step 2: Add bonus lessons section after the optional lessons table**

Insert after the `| 13 | ...` row in the Optional Advanced Lessons table:

```markdown
### Bonus Lessons

| # | Notebook | Topic | Difficulty | Time |
|---|----------|--------|------------|------|
| 14 | [14_whatsapp_business_copilot.ipynb](notebooks/14_whatsapp_business_copilot.ipynb) | WhatsApp Co-pilot — Meta Cloud API + lyzr-adk agent | 🔴 Advanced | 35 min |
| 15 | [15_multi_agent_ecommerce.ipynb](notebooks/15_multi_agent_ecommerce.ipynb) | Multi-agent — manager routes to 3 specialist sub-agents | 🔴 Advanced | 35 min |
```

Also update the project structure section to list the 2 new files.

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add lessons 14 and 15 to README"
```

---

## Verification Checklist

After all tasks are complete, verify:

1. `notebooks/14_whatsapp_business_copilot.ipynb` exists and is valid JSON
2. `notebooks/15_multi_agent_ecommerce.ipynb` exists and is valid JSON
3. README.md contains the "Bonus Lessons" section with both new entries
4. All cells in notebook 14 have IDs matching `a1b2c3d4-14NN-*`
5. All cells in notebook 15 have IDs matching `a1b2c3d4-15NN-*`
6. Both notebooks open in Jupyter without errors on import cells

Quick validation:
```bash
python -c "import json; json.load(open('notebooks/14_whatsapp_business_copilot.ipynb')); print('14 valid JSON ✅')"
python -c "import json; json.load(open('notebooks/15_multi_agent_ecommerce.ipynb')); print('15 valid JSON ✅')"
```
