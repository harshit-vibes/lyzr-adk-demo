"""Validation for bonus lessons 14 and 15."""
import os, sys, traceback

os.environ["LYZR_API_KEY"] = "sk-default-gqcFW0hH98hyscbMUp8nS9cfHLEoLCDw"

from lyzr import Studio

studio = Studio(api_key=os.environ["LYZR_API_KEY"])

results = []

def test(name, fn):
    try:
        fn()
        results.append((name, "PASS", ""))
        print(f"  ✅ {name}")
    except Exception as e:
        tb = traceback.format_exc().strip().splitlines()[-1]
        results.append((name, "FAIL", tb))
        print(f"  ❌ {name}: {tb}")


# ─── Lesson 14 tests ────────────────────────────────────────────────

ORDERS = {
    "ORD-1001": {"status": "shipped", "delivery": "2026-02-26", "carrier": "FedEx", "tracking": "FX123456"},
    "ORD-1002": {"status": "processing", "delivery": "2026-02-28", "carrier": "UPS", "tracking": "UP789012"},
}

def lookup_order(order_id: str) -> str:
    """Look up a customer order by order ID and return its current status.
    Returns status, carrier, tracking number, and estimated delivery date.
    Use this when a customer asks about order status, location, or delivery date.
    """
    if order_id.upper() in ORDERS:
        o = ORDERS[order_id.upper()]
        return f"Order {order_id.upper()}: {o['status']} via {o['carrier']} (tracking: {o['tracking']}), delivery: {o['delivery']}"
    return f"Order {order_id} not found."

def send_whatsapp_reply(to_number: str, message: str) -> str:
    """Send a WhatsApp reply. In simulation prints instead of calling Meta API."""
    print(f"    [WhatsApp → {to_number}]: {message[:60]}...")
    return f"Sent to {to_number}"

print("\n=== Lesson 14: WhatsApp Co-pilot ===")

def test14_1():
    """Test: agent creation with memory and RAI"""
    agent = studio.create_agent(
        name="WA Test Agent",
        provider="openai/gpt-4o-mini",
        role="Customer service agent",
        goal="Help customers via WhatsApp",
        instructions="Look up orders when asked. Keep replies brief."
    )
    agent.add_tool(lookup_order)
    agent.add_memory(max_messages=5)
    from lyzr.rai import PIIType, PIIAction
    rai = studio.create_rai_policy(name="WA RAI Test", description="Test RAI policy", toxicity_threshold=0.4, pii_detection={PIIType.PHONE: PIIAction.REDACT, PIIType.EMAIL: PIIAction.REDACT})
    agent.add_rai_policy(rai)
    assert agent.id, "No agent ID"

test("14.1 Agent creation + tool + memory + RAI", test14_1)

def test14_2():
    """Test: order lookup tool called by agent"""
    agent = studio.create_agent(
        name="WA Order Test",
        provider="openai/gpt-4o-mini",
        role="Order support agent",
        goal="Look up orders",
        instructions="Use lookup_order for any order status question."
    )
    agent.add_tool(lookup_order)
    r = agent.run("What is the status of order ORD-1001?")
    assert r.response, "Empty response"
    assert "ORD-1001" in r.response or "FedEx" in r.response or "shipped" in r.response, f"Order data not in response: {r.response[:100]}"

test("14.2 Order lookup tool routing", test14_2)

def test14_3():
    """Test: session_id memory across turns"""
    import uuid
    agent = studio.create_agent(
        name="WA Session Test",
        provider="openai/gpt-4o-mini",
        role="Customer service agent",
        goal="Maintain conversation context",
        instructions="Remember context across turns."
    )
    agent.add_memory(max_messages=5)
    session = "+1-555-TEST"
    r1 = agent.run("My name is TestUser and I have a question about order ORD-1001.", session_id=session)
    r2 = agent.run("What was the order number I mentioned?", session_id=session)
    assert r2.response, "Empty response on turn 2"
    assert "ORD-1001" in r2.response or "1001" in r2.response, f"Memory not working: {r2.response[:100]}"

test("14.3 Session memory (session_id=phone)", test14_3)

def test14_4():
    """Test: simulation send_whatsapp_reply explicitly"""
    r = send_whatsapp_reply("+1-555-0147", "Your order ORD-1001 has shipped via FedEx.")
    assert "Sent to" in r

test("14.4 send_whatsapp_reply simulation", test14_4)


# ─── Lesson 15 tests ────────────────────────────────────────────────

print("\n=== Lesson 15: Multi-agent E-commerce ===")

def test15_1():
    """Test: three sub-agents created"""
    global order_agent, product_agent, billing_agent
    order_agent = studio.create_agent(
        name="Order Specialist Test",
        provider="openai/gpt-4o-mini",
        role="Order management specialist",
        goal="Handle order questions",
        instructions="Answer order status, return, and cancellation questions concisely."
    )
    product_agent = studio.create_agent(
        name="Product Specialist Test",
        provider="openai/gpt-4o-mini",
        role="Product specialist",
        goal="Answer product questions",
        instructions="Answer product availability and recommendation questions concisely."
    )
    billing_agent = studio.create_agent(
        name="Billing Specialist Test",
        provider="openai/gpt-4o-mini",
        role="Billing specialist",
        goal="Handle billing questions",
        instructions="Answer refund, payment, and invoice questions concisely."
    )
    assert order_agent.id and product_agent.id and billing_agent.id

test("15.1 Three sub-agents created", test15_1)

def test15_2():
    """Test: wrapper functions and tool routing"""
    def handle_order_query(query: str) -> str:
        """Handle customer questions about orders, returns, cancellations, and shipping status.
        Use for: order tracking, return requests, delivery questions.
        Do NOT use for: product specs, billing, payments.
        """
        return order_agent.run(query).response

    def handle_product_query(query: str) -> str:
        """Answer customer questions about products, availability, specs, and recommendations.
        Use for: product availability, comparisons, purchase recommendations.
        Do NOT use for: order status, billing, payments.
        """
        return product_agent.run(query).response

    def handle_billing_query(query: str) -> str:
        """Resolve billing issues, refund requests, and payment and invoice questions.
        Use for: refunds, payment failures, invoices, duplicate charges.
        Do NOT use for: order logistics, product information.
        """
        return billing_agent.run(query).response

    manager = studio.create_agent(
        name="Support Manager Test",
        provider="openai/gpt-4o-mini",
        role="Customer support routing manager",
        goal="Route queries to the correct specialist",
        instructions=(
            "You do NOT answer questions yourself. Always use a specialist tool. "
            "For orders/shipping: use handle_order_query. "
            "For products: use handle_product_query. "
            "For billing/payments/refunds: use handle_billing_query. "
            "Never answer from your own knowledge."
        )
    )
    manager.add_tool(handle_order_query)
    manager.add_tool(handle_product_query)
    manager.add_tool(handle_billing_query)

    # Test order routing
    r_order = manager.run("Where is my order ORD-1001?")
    assert r_order.response, "Empty order response"

    # Test billing routing
    r_billing = manager.run("I was charged twice. I want a refund.")
    assert r_billing.response, "Empty billing response"

test("15.2 Manager routes order + billing queries", test15_2)

def test15_3():
    """Test: manager handles multi-domain query"""
    def handle_order_query_md(query: str) -> str:
        """Handle order status, cancellations, returns, and shipping. Do NOT use for billing."""
        return order_agent.run(query).response

    def handle_billing_query_md(query: str) -> str:
        """Handle refund requests, payments, invoices, billing issues. Do NOT use for order logistics."""
        return billing_agent.run(query).response

    manager2 = studio.create_agent(
        name="Multi-domain Manager Test",
        provider="openai/gpt-4o-mini",
        role="Customer support routing manager",
        goal="Route queries correctly, call multiple tools for multi-domain questions",
        instructions=(
            "Use handle_order_query_md for order questions. "
            "Use handle_billing_query_md for billing/refund questions. "
            "For queries spanning both domains, call both tools."
        )
    )
    manager2.add_tool(handle_order_query_md)
    manager2.add_tool(handle_billing_query_md)

    r = manager2.run("My order ORD-1002 hasn't arrived. I want to cancel it and get a refund.")
    assert r.response, "Empty multi-domain response"
    assert len(r.response) > 30, f"Response too short: {r.response}"

test("15.3 Manager multi-domain query", test15_3)


# ─── Summary ────────────────────────────────────────────────────────

print("\n" + "=" * 50)
passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
print(f"Results: {passed} passed, {failed} failed out of {len(results)} tests")
if failed:
    print("\nFailed tests:")
    for name, status, err in results:
        if status == "FAIL":
            print(f"  ❌ {name}: {err}")
    sys.exit(1)
else:
    print("All tests passed ✅")
