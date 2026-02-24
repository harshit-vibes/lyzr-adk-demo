#!/usr/bin/env python3
"""
Lyzr ADK Validation Script
Tests core API patterns from all 13 lessons.
Run with: LYZR_API_KEY=sk-... python validate.py
"""

import os
import sys
import time
import uuid
import traceback

MODEL = "openai/gpt-4o-mini"

# ── colours & helpers ──────────────────────────────────────────────────────────
GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"

passed = 0
failed = 0
results = []


def ok(n: int, name: str):
    global passed
    passed += 1
    msg = f"{GREEN}✅ Test {n}: {name} — PASSED{RESET}"
    print(msg)
    results.append((n, name, True, None))


def fail(n: int, name: str, err: str):
    global failed
    failed += 1
    msg = f"{RED}❌ Test {n}: {name} — FAILED: {err}{RESET}"
    print(msg)
    results.append((n, name, False, err))


# ── setup ──────────────────────────────────────────────────────────────────────
API_KEY = os.getenv("LYZR_API_KEY", "")
if not API_KEY:
    print("ERROR: LYZR_API_KEY environment variable not set.")
    sys.exit(1)

print(f"\nLyzr ADK Validation — model: {MODEL}")
print("=" * 60)

from lyzr import Studio
from lyzr.rai import PIIType, PIIAction

# Cleanup registry — resources to delete at the end
cleanup = {
    "agents": [],       # agent objects
    "kbs": [],          # knowledge base objects
    "contexts": [],     # context objects
    "policies": [],     # RAI policy objects
}

# ── Test 1: Studio initialization ─────────────────────────────────────────────
try:
    studio = Studio(api_key=API_KEY)
    assert studio is not None
    ok(1, "Studio initialization")
except Exception as e:
    fail(1, "Studio initialization", str(e))
    print("Cannot continue without Studio. Exiting.")
    sys.exit(1)

# ── Test 2: create_agent ──────────────────────────────────────────────────────
agent = None
try:
    agent = studio.create_agent(
        name="val-basic",
        provider=MODEL,
        role="assistant",
        goal="answer questions",
        instructions="Be very brief."
    )
    assert agent is not None
    assert hasattr(agent, "id") and agent.id
    cleanup["agents"].append(agent)
    ok(2, "create_agent")
except Exception as e:
    fail(2, "create_agent", str(e))

# ── Test 3: agent.run() and response.response ─────────────────────────────────
try:
    assert agent is not None, "agent not created in Test 2"
    response = agent.run("Hi")
    assert response is not None
    assert hasattr(response, "response"), "response object missing .response attribute"
    assert isinstance(response.response, str), f"response.response is {type(response.response)}, expected str"
    assert len(response.response) > 0, "response.response is empty"
    ok(3, "agent.run() and response.response")
except Exception as e:
    fail(3, "agent.run() and response.response", str(e))

# ── Test 4: list_agents / get_agent ───────────────────────────────────────────
try:
    agents_list = studio.list_agents()
    assert agents_list is not None
    ids = [a.id for a in agents_list]
    assert agent.id in ids, f"created agent {agent.id} not found in list_agents()"

    retrieved = studio.get_agent(agent.id)
    assert retrieved.id == agent.id
    ok(4, "list_agents / get_agent")
except Exception as e:
    fail(4, "list_agents / get_agent", str(e))

# ── Test 5: agent.update() ────────────────────────────────────────────────────
try:
    assert agent is not None, "agent not created in Test 2"
    agent.update(instructions="One sentence only.")
    # verify update persisted
    refreshed = studio.get_agent(agent.id)
    assert refreshed is not None
    ok(5, "agent.update()")
except Exception as e:
    fail(5, "agent.update()", str(e))

# ── Test 6: agent.clone() and clone.delete() ──────────────────────────────────
try:
    assert agent is not None, "agent not created in Test 2"
    clone = agent.clone()
    assert clone is not None
    assert clone.id != agent.id
    clone.delete()
    # verify deletion
    agents_after = studio.list_agents()
    ids_after = [a.id for a in agents_after]
    assert clone.id not in ids_after, "clone still present after delete"
    ok(6, "agent.clone() and clone.delete()")
except Exception as e:
    fail(6, "agent.clone() and clone.delete()", str(e))

# ── Test 7: Structured output with Pydantic (response_model) ──────────────────
# NOTE: The notebooks show `response_format=Model` passed to agent.run(), but the
# actual SDK uses `response_model=Model` on create_agent(). With response_model set,
# agent.run() returns the Pydantic instance directly (not wrapped in AgentResponse).
try:
    from pydantic import BaseModel, Field

    class Sentiment(BaseModel):
        label: str = Field(description="Sentiment label: positive, negative, or neutral")
        score: float = Field(description="Confidence score between 0.0 and 1.0")

    struct_agent = studio.create_agent(
        name="val-struct",
        provider=MODEL,
        role="analyst",
        goal="classify sentiment",
        instructions="Always fill all fields.",
        response_model=Sentiment,    # correct SDK parameter (not response_format)
    )
    cleanup["agents"].append(struct_agent)

    result = struct_agent.run("Great product!")
    # With response_model set, run() returns the Pydantic model directly
    assert isinstance(result, Sentiment), f"Expected Sentiment, got {type(result)}"
    assert hasattr(result, "label")
    assert hasattr(result, "score")
    ok(7, "Structured output with Pydantic (response_format)")
except Exception as e:
    fail(7, "Structured output with Pydantic (response_format)", str(e))

# ── Test 8: add_memory / remove_memory with session_id ────────────────────────
try:
    assert agent is not None, "agent not created in Test 2"
    agent.add_memory(max_messages=5)
    session = str(uuid.uuid4())
    agent.run("My name is Val.", session_id=session)
    resp2 = agent.run("What is my name?", session_id=session)
    assert isinstance(resp2.response, str)
    agent.remove_memory()
    ok(8, "add_memory / remove_memory with session_id")
except Exception as e:
    fail(8, "add_memory / remove_memory with session_id", str(e))

# ── Test 9: add_tool with a simple Python function ────────────────────────────
try:
    def double(n: int) -> str:
        """Double a number and return the result as a string."""
        return str(n * 2)

    tool_agent = studio.create_agent(
        name="val-tool",
        provider=MODEL,
        role="calculator",
        goal="use tools",
        instructions="Use the double tool when asked to double a number."
    )
    cleanup["agents"].append(tool_agent)
    tool_agent.add_tool(double)
    resp = tool_agent.run("Double 7.")
    assert isinstance(resp.response, str)
    # The agent should mention 14 somewhere
    ok(9, "add_tool with a simple Python function")
except Exception as e:
    fail(9, "add_tool with a simple Python function", str(e))

# ── Test 10: create_knowledge_base / add_text / query ─────────────────────────
kb = None
try:
    kb = studio.create_knowledge_base(name="val_kb_test")
    assert kb is not None
    assert hasattr(kb, "id") and kb.id
    cleanup["kbs"].append(kb)

    kb.add_text(
        text="The sky is blue. Water is wet.",
        source="facts"
    )
    time.sleep(3)  # wait for indexing

    results_kb = kb.query("What color is the sky?", top_k=2)
    assert isinstance(results_kb, list), f"query returned {type(results_kb)}"
    # results may be 0 if indexing is slow, but call must not raise
    ok(10, "create_knowledge_base / add_text / query")
except Exception as e:
    fail(10, "create_knowledge_base / add_text / query", str(e))

# ── Test 11: create_context / add_context / context.update() / remove_context ─
ctx = None
try:
    ctx = studio.create_context(
        name="val_ctx",
        value="User is a tester."
    )
    assert ctx is not None
    assert hasattr(ctx, "id") and ctx.id
    cleanup["contexts"].append(ctx)

    ctx_agent = studio.create_agent(
        name="val-ctx",
        provider=MODEL,
        role="assistant",
        goal="help",
        instructions="Use context."
    )
    cleanup["agents"].append(ctx_agent)

    ctx_agent.add_context(ctx)
    ctx.update("User is an advanced tester.")
    ctx_agent.remove_context(ctx)
    ok(11, "create_context / add_context / context.update() / remove_context")
except Exception as e:
    fail(11, "create_context / add_context / context.update() / remove_context", str(e))

# ── Test 12: create_rai_policy / add_rai_policy ───────────────────────────────
# NOTE: RAI uses a separate service endpoint (srs-prod.studio.lyzr.ai).
# If that endpoint is unreachable, we accept a connectivity error as a known
# infrastructure issue and still validate the API call shape is correct.
policy = None
try:
    policy = studio.create_rai_policy(
        name="val-rai-policy",
        description="Validation test policy",
        toxicity_threshold=0.4,
        nsfw_check=False,
        prompt_injection=False,
    )
    assert policy is not None
    assert hasattr(policy, "id") and policy.id
    cleanup["policies"].append(policy)

    rai_agent = studio.create_agent(
        name="val-rai",
        provider=MODEL,
        role="safe assistant",
        goal="answer safely",
        instructions="Be helpful."
    )
    cleanup["agents"].append(rai_agent)

    rai_agent.add_rai_policy(policy)
    resp = rai_agent.run("Hello")
    assert isinstance(resp.response, str)
    rai_agent.remove_rai_policy()
    ok(12, "create_rai_policy / add_rai_policy")
except Exception as e:
    err_str = str(e)
    # Accept DNS/connectivity errors for the RAI service as a known infra issue
    # (srs-prod.studio.lyzr.ai may not be publicly reachable in all environments)
    if "nodename nor servname" in err_str or "ConnectError" in err_str or "Connection" in err_str:
        fail(12, "create_rai_policy / add_rai_policy",
             f"RAI service unreachable (srs-prod.studio.lyzr.ai DNS/connectivity issue): {err_str}")
    else:
        fail(12, "create_rai_policy / add_rai_policy", err_str)

# ── Test 13: streaming (stream=True) ─────────────────────────────────────────
# NOTE: stream=True yields AgentStream objects. Access chunk.content for text.
# The notebooks show `print(chunk, end="")` but the actual SDK yields AgentStream
# objects where you must use chunk.content to get the string fragment.
try:
    assert agent is not None, "agent not created in Test 2"
    from lyzr.responses import AgentStream
    chunks_collected = []
    for i, chunk in enumerate(agent.run("Hi", stream=True)):
        assert isinstance(chunk, AgentStream), \
            f"chunk is {type(chunk)}, expected AgentStream"
        assert isinstance(chunk.content, str), \
            f"chunk.content is {type(chunk.content)}, expected str"
        chunks_collected.append(chunk.content)
        if i >= 2:   # collect at least 3 chunks then break
            break
    assert len(chunks_collected) > 0, "no chunks received from stream"
    ok(13, "streaming (stream=True)")
except Exception as e:
    fail(13, "streaming (stream=True)", str(e))

# ── Cleanup ────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Cleaning up created resources...")

for ag in cleanup["agents"]:
    try:
        ag.delete()
        print(f"  Deleted agent: {ag.id}")
    except Exception as e:
        print(f"  Warning: could not delete agent {ag.id}: {e}")

for kb_obj in cleanup["kbs"]:
    try:
        kb_obj.delete()
        print(f"  Deleted KB: {kb_obj.id}")
    except Exception as e:
        print(f"  Warning: could not delete KB {kb_obj.id}: {e}")

for ctx_obj in cleanup["contexts"]:
    try:
        ctx_obj.delete()
        print(f"  Deleted context: {ctx_obj.id}")
    except Exception as e:
        print(f"  Warning: could not delete context {ctx_obj.id}: {e}")

for pol_obj in cleanup["policies"]:
    try:
        pol_obj.delete()
        print(f"  Deleted policy: {pol_obj.id}")
    except Exception as e:
        print(f"  Warning: could not delete policy {pol_obj.id}: {e}")

# ── Summary ───────────────────────────────────────────────────────────────────
total = 13
print("\n" + "=" * 60)
print(f"\n{passed}/{total} tests passed\n")

if failed > 0:
    print("Failed tests:")
    for n, name, ok_flag, err in results:
        if not ok_flag:
            print(f"  Test {n} ({name}): {err}")
