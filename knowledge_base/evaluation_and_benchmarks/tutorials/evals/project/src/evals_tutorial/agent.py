"""Chapter 10a — order-management agent evals with a deterministic mock shop DB.

Single-turn tool-calling episodes: a small LLM (Ollama) plays a shop
support agent against an in-memory shop database. We grade the *final DB
state* plus path constraints (forbidden/required tools, step budget,
reply keywords), not the chat text alone, because an agent can succeed
by many paths — or succeed at the cost of a policy violation.

The model is stochastic, so tasks are retried and we report:
- `pass@k`  — task passes if any of k trials passes (capability)
- `pass^k`  — task passes if all k trials pass (reliability)

Commands (see `just --list`): demo, run, grade, simulate (10b stub).
"""

from __future__ import annotations

import copy
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import typer
from pydantic import BaseModel, Field

# Fixed "today" so policy windows (24 h address lock, 30-day returns) are
# evaluated against one deterministic clock for every episode.
NOW = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)
RETURN_WINDOW_DAYS = 30
ADDRESS_WINDOW_HOURS = 24
CANCEL_FEE_PROCESSING = 5.0
REFUND_ESCALATION_THRESHOLD = 200.0

app = typer.Typer(help="Chapter 10a — order-management agent against a mock shop DB.")


# ---------------------------------------------------------------------------
# mock shop database
# ---------------------------------------------------------------------------


@dataclass
class Order:
    order_id: str
    customer_email: str
    status: str  # placed | processing | shipped | delivered | returned | cancelled
    placed_at: str  # ISO-8601 UTC
    delivered_at: str | None = None
    total: float = 0.0
    items: list[dict] = field(default_factory=list)
    address: dict = field(default_factory=dict)
    fee: float = 0.0
    refund_total: float = 0.0
    refunds: list = field(default_factory=list)
    return_status: str | None = None
    return_item: str | None = None
    return_reason: str | None = None


def _customer(email: str) -> dict:
    return {"email": email, "name": email.split("@")[0].title(),
            "address": {"street": "12 Old Mill Rd", "city": "Rivertown", "zip": "04101"}}


def _item(iid: str, name: str, price: float, qty: int = 1, custom: bool = False) -> dict:
    return {"item_id": iid, "name": name, "price": price, "qty": qty, "custom": custom}


def _orders() -> list[Order]:
    def mk(oid, email, status, placed, total, items, delivered=None, fee=0.0, refund_total=0.0, refunds=None):
        return Order(order_id=oid, customer_email=email, status=status, placed_at=placed,
                     delivered_at=delivered, total=total, items=items,
                     address=dict(_customer(email)["address"]), fee=fee,
                     refund_total=refund_total, refunds=list(refunds or []))

    return [
        mk("O101", "ana.lee@example.com", "placed", "2026-08-31T09:00:00Z", 120.0,
           [_item("I1", "Trail helmet", 60.0), _item("I2", "Gloves", 40.0)]),
        mk("O102", "ben.ross@example.com", "placed", "2026-09-01T08:00:00Z", 90.0,
           [_item("I1", "Frame pump", 90.0)]),
        mk("O103", "carmen.diaz@example.com", "shipped", "2026-08-29T09:00:00Z", 150.0,
           [_item("I1", "Road jacket", 150.0)]),
        mk("O104", "derek.ho@example.com", "delivered", "2026-07-20T10:00:00Z", 180.0,
           [_item("I1", "Touring saddle", 180.0)], delivered="2026-08-20T10:00:00Z"),
        mk("O105", "elsa.kim@example.com", "returned", "2026-07-10T10:00:00Z", 75.0,
           [_item("I1", "Personalized jersey — CUSTOM", 75.0, custom=True)], delivered="2026-08-10T10:00:00Z"),
        mk("O106", "felix.ng@example.com", "processing", "2026-08-30T14:00:00Z", 220.0,
           [_item("I1", "Gravel bike (base)", 180.0), _item("I2", "Saddle bag", 40.0)]),
        mk("O107", "gita.patel@example.com", "shipped", "2026-08-28T11:00:00Z", 60.0,
           [_item("I1", "Tire set", 60.0)]),
        mk("O108", "hugo.lar@example.com", "delivered", "2026-06-25T09:00:00Z", 300.0,
           [_item("I1", "E-bike charger", 300.0)], delivered="2026-07-21T09:00:00Z"),
        mk("O109", "ines.bro@example.com", "delivered", "2026-08-01T12:00:00Z", 140.0,
           [_item("I1", "Climbing shoes", 140.0)], delivered="2026-08-28T12:00:00Z"),
        mk("O110", "jon.asse@example.com", "delivered", "2026-07-01T08:00:00Z", 240.0,
           [_item("I1", "Carbon wheel", 240.0)], delivered="2026-08-15T08:00:00Z"),
        mk("O111", "kira.ott@example.com", "delivered", "2026-06-15T10:00:00Z", 900.0,
           [_item("I1", "Custom-configured bike — CUSTOM", 900.0, custom=True)], delivered="2026-07-05T10:00:00Z"),
        mk("O112", "liam.wolfe@example.com", "delivered", "2026-07-30T10:00:00Z", 120.0,
           [_item("I1", "Repair stand", 120.0)], delivered="2026-08-31T10:00:00Z"),
        mk("O120", "maya.chen@example.com", "shipped", "2026-08-30T09:00:00Z", 80.0,
           [_item("I1", "Bottle cage", 80.0)]),
        mk("O121", "maya.chen@example.com", "delivered", "2026-07-05T09:00:00Z", 160.0,
           [_item("I1", "Framed bag", 160.0)], delivered="2026-08-20T09:00:00Z"),
        mk("O122", "noah.vid@example.com", "cancelled", "2026-08-12T09:00:00Z", 100.0,
           [_item("I1", "Handlebar tape", 100.0)], fee=0.0, refund_total=100.0,
           refunds=[{"amount": 100.0, "note": "cancellation refund"}]),
    ]


class ShopDB:
    """In-memory shop: customers + orders. `reset()` returns a fresh copy."""

    def __init__(self, customers: list[dict], orders: list[Order]):
        self.customers = customers
        self.orders = orders
        self.escalations: list[dict] = []

    def order(self, order_id: str) -> Order:
        for o in self.orders:
            if o.order_id == order_id:
                return o
        raise KeyError(f"unknown order id: {order_id}")

    def by_email(self, email: str) -> list[Order]:
        return [o for o in self.orders if o.customer_email.lower() == email.lower()]

    def snapshot(self) -> dict:
        return {
            "orders": {
                o.order_id: {
                    "status": o.status, "fee": o.fee, "refund_total": o.refund_total,
                    "refunds": copy.deepcopy(o.refunds), "return_status": o.return_status,
                    "return_item": o.return_item, "address": copy.deepcopy(o.address),
                }
                for o in self.orders
            },
            "escalations": copy.deepcopy(self.escalations),
        }

    @staticmethod
    def diff(before: dict, after: dict) -> dict:
        out: dict = {}
        a_orders = before.get("orders", {})
        b_orders = after.get("orders", {})
        for oid in set(a_orders) | set(b_orders):
            fa, fb = a_orders.get(oid, {}), b_orders.get(oid, {})
            changed = {k: {"before": fa.get(k), "after": fb.get(k)}
                       for k in fa | fb if fa.get(k) != fb.get(k)}
            if changed:
                out[f"orders.{oid}"] = changed
        if before.get("escalations") != after.get("escalations"):
            out["escalations"] = {"before": before.get("escalations"),
                                  "after": after.get("escalations")}
        return out


def fresh_db() -> ShopDB:
    orders = _orders()
    emails = sorted({o.customer_email for o in orders})
    return ShopDB(customers= [_customer(e) for e in emails + ["extra.customer@example.com"]],
                  orders=orders)
# ---------------------------------------------------------------------------
# tools (each mutates the given ShopDB, returns a JSON-able dict)
# ---------------------------------------------------------------------------


def _hours_since(iso: str) -> float:
    return (NOW - datetime.fromisoformat(iso.replace("Z", "+00:00"))).total_seconds() / 3600.0


def _days_since(iso: str) -> float:
    return (NOW - datetime.fromisoformat(iso.replace("Z", "+00:00"))).total_seconds() / 86400.0


def lookup_order(db: ShopDB, order_id: str) -> dict:
    try:
        o = db.order(order_id)
    except (KeyError, TypeError):
        return {"ok": False, "error": f"unknown order id {order_id!r}"}
    if o.status in ("returned", "cancelled") and o.refund_total:
        pass
    return {
        "ok": True, "order_id": o.order_id, "email": o.customer_email,
        "status": o.status, "placed_days_ago": round(_days_since(o.placed_at), 1),
        "delivered_days_ago": (round(_days_since(o.delivered_at), 1) if o.delivered_at else None),
        "total": o.total, "fee": o.fee, "refund_total": o.refund_total,
        "refunds": o.refunds, "items": o.items, "address": o.address,
        "return": {"status": o.return_status, "item": o.return_item, "reason": o.return_reason},
    }


def list_orders(db: ShopDB, email: str) -> dict:
    rows = db.by_email(email or "")
    return {"ok": bool(rows), "orders": [
        {"order_id": o.order_id, "status": o.status, "total": o.total,
         "placed_days_ago": round(_days_since(o.placed_at), 1),
         "items": [i["name"] for i in o.items]}
        for o in sorted(rows, key=lambda x: x.order_id)
    ]}


def cancel_order(db: ShopDB, order_id: str) -> dict:
    if order_id is None or not isinstance(order_id, str):
        return {"ok": False, "error": "order_id is required and must be a string"}
    try:
        o = db.order(order_id)
    except (KeyError, TypeError):
        return {"ok": False, "error": f"unknown order id {order_id!r}"}
    if o.status == "cancelled":
        return {"ok": False, "error": "already cancelled", "fee": o.fee,
                "refund": o.refund_total}
    if o.status in ("shipped", "delivered", "returned"):
        return {"ok": False,
                "error": ("orders that are shipped/delivered/returned cannot be "
                          "cancelled — use start_return instead")}
    fee = CANCEL_FEE_PROCESSING if o.status == "processing" else 0.0
    o.status = "cancelled"
    o.fee = fee
    o.refund_total = max(o.total - fee, 0.0)
    o.refunds.append({"amount": o.refund_total, "note": "cancellation refund"})
    return {"ok": True, "status": "cancelled", "fee": fee, "refund": o.refund_total}


def update_address(db: ShopDB, order_id: str, address: dict) -> dict:
    if order_id is None or not isinstance(order_id, str):
        return {"ok": False, "error": "order_id is required and must be a string"}
    if not isinstance(address, dict) or not address:
        return {"ok": False, "error": "address must be a dict with street/city/zip"}
    try:
        o = db.order(order_id)
    except (KeyError, TypeError):
        return {"ok": False, "error": f"unknown order id {order_id!r}"}
    if o.status not in ("placed",):
        return {"ok": False,
                "error": (f"order {o.order_id} is '{o.status}' — address can only change "
                          f"while the order is 'placed' (within {ADDRESS_WINDOW_HOURS} h)")}
    if _hours_since(o.placed_at) > ADDRESS_WINDOW_HOURS:
        return {"ok": False,
                "error": (f"the {ADDRESS_WINDOW_HOURS}-h edit window has passed "
                          f"(order is {_days_since(o.placed_at):.1f} days old); "
                          "cancel and re-order instead")}
    o.address = dict(address)
    return {"ok": True, "address": o.address}


def start_return(db: ShopDB, order_id: str, item_id: str, reason: str = "") -> dict:
    if order_id is None or item_id is None:
        return {"ok": False, "error": "order_id and item_id are required"}
    try:
        o = db.order(order_id)
    except (KeyError, TypeError):
        return {"ok": False, "error": f"unknown order id {order_id!r}"}
    if o.status != "delivered":
        return {"ok": False, "error": f"only delivered orders can be returned (order is '{o.status}'); "
                                     "use cancel_order instead"}
    if o.return_status == "started":
        return {"ok": False, "error": "return already started for this order"}
    item = next((i for i in o.items if i["item_id"] == item_id), None)
    if item is None:
        valid = [i["item_id"] for i in o.items]
        return {"ok": False, "error": f"item {item_id!r} not on this order; item_ids: {valid}"}
    if item.get("custom"):
        return {"ok": False, "error": ("custom/personalized items are not returnable — "
                                       "no refund and no return label will be issued")}
    if o.delivered_at and _days_since(o.delivered_at) > RETURN_WINDOW_DAYS:
        return {"ok": False,
                "error": (f"the {RETURN_WINDOW_DAYS}-day return window has passed "
                          f"(delivered {_days_since(o.delivered_at):.0f} days ago)")}
    o.return_status = "started"
    o.return_item = item_id
    o.return_reason = reason or ""
    return {"ok": True, "item": item, "label_fee": 12.5,
            "note": "refund is issued with issue_refund once the item is received"}


def issue_refund(db: ShopDB, order_id: str, amount: float) -> dict:
    if order_id is None or amount is None:
        return {"ok": False, "error": "order_id and amount are required"}
    try:
        o = db.order(order_id)
    except (KeyError, TypeError):
        return {"ok": False, "error": f"unknown order id {order_id!r}"}
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        return {"ok": False, "error": "amount must be a positive number"}
    if amount > o.total:
        return {"ok": False, "error": f"refund {amount} exceeds the order total {o.total}"}
    already = sum(r.get("amount", 0) for r in o.refunds)
    if already + amount > o.total:
        return {"ok": False,
                "error": f"total refunds {already + amount} would exceed the order total {o.total}"}
    needs_escalation = o.return_status != "started" and amount >= REFUND_ESCALATION_THRESHOLD
    if needs_escalation and not db.escalations:
        return {"ok": False,
                "error": (f"refunds of {amount} or more without a started return "
                          f"require escalate(...) first")}
    o.refund_total += amount
    o.refunds.append({"amount": amount, "note": "refund"})
    return {"ok": True, "refunded": amount, "refund_total": o.refund_total}


def escalate(db: ShopDB, reason: str) -> dict:
    if not isinstance(reason, str) or not reason.strip():
        return {"ok": False, "error": "a non-empty reason string is required"}
    db.escalations.append({"reason": reason, "at": NOW.isoformat()})
    return {"ok": True, "escalation_id": f"E{len(db.escalations):04d}", "reason": reason}


def reply(db: ShopDB, text: str) -> dict:
    if not isinstance(text, str) or not text.strip():
        return {"ok": False, "error": "reply text must be a non-empty string"}
    return {"ok": True, "ended": True, "text": text}


TOOLS: dict[str, Callable] = {
    "lookup_order": lambda db, order_id: lookup_order(db, order_id),
    "list_orders": lambda db, email: list_orders(db, email),
    "cancel_order": lambda db, order_id: cancel_order(db, order_id),
    "update_address": lambda db, order_id, address: update_address(db, order_id, address),
    "start_return": lambda db, order_id, item_id, reason="": start_return(db, order_id, item_id, reason),
    "issue_refund": lambda db, order_id, amount: issue_refund(db, order_id, amount),
    "escalate": lambda db, reason="": escalate(db, reason),
    "reply": lambda db, text="": reply(db, text),
}

TOOL_SCHEMAS: list[dict] = [
    {"type": "function", "function": {"name": "lookup_order",
        "description": "Fetch full details of one order (status, items, dates, refund state).",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string",
            "description": "Order id, e.g. O101"}}, "required": ["order_id"]}}},
    {"type": "function", "function": {"name": "list_orders",
        "description": "List a customer's orders when no order id is given.",
        "parameters": {"type": "object", "properties": {"email": {"type": "string"}},
            "required": ["email"]}}},
    {"type": "function", "function": {"name": "cancel_order",
        "description": "Cancel an order. Refused once shipped/delivered; $5 fee if status is 'processing'.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"]}}},
    {"type": "function", "function": {"name": "update_address",
        "description": "Update the shipping address. Allowed only while status is 'placed' and within 24 h of placement.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"},
            "address": {"type": "object"}}, "required": ["order_id", "address"]}}},
    {"type": "function", "function": {"name": "start_return",
        "description": "Start a return for one item of a delivered order (30-day window, non-custom).",
        "parameters": {"type": "object", "properties": {
            "order_id": {"type": "string"}, "item_id": {"type": "string"},
            "reason": {"type": "string"}}, "required": ["order_id", "item_id"]}}},
    {"type": "function", "function": {"name": "issue_refund",
        "description": "Issue a money refund against an order (capped at order total). Refunds >= 200 without a started return require escalate() first.",
        "parameters": {"type": "object", "properties": {
            "order_id": {"type": "string"}, "amount": {"type": "number"}},
            "required": ["order_id", "amount"]}}},
    {"type": "function", "function": {"name": "escalate",
        "description": "Escalate to a human supervisor (e.g. refunds >= 200 without a return).",
        "parameters": {"type": "object", "properties": {"reason": {"type": "string"}},
            "required": ["reason"]}}},
    {"type": "function", "function": {"name": "reply",
        "description": "Send the final answer to the customer. This ends the episode.",
        "parameters": {"type": "object", "properties": {"text": {"type": "string"}},
            "required": ["text"]}}},
]


def call_tool(db: ShopDB, name: str, args: dict) -> tuple[dict, bool]:
    """Execute one tool call. Returns (result, was_error_or_unknown)."""
    fn = TOOLS.get(name)
    if fn is None:
        return {"ok": False, "error": f"unknown tool: {name}"}, True
    try:
        result = fn(db, **args)
    except TypeError:
        return {"ok": False, "error": f"bad arguments for {name}: {args!r}"}, True
    except Exception as exc:  # noqa: BLE001 - tool errors are data, not crashes
        return {"ok": False, "error": f"{name} raised: {exc}"}, True
    if not isinstance(result, dict):
        result = {"ok": True, "value": result}
    return result, result.get("ok") is False
# ---------------------------------------------------------------------------
# system prompt + task loading
# ---------------------------------------------------------------------------


def _candidate_bases(project_root: Path | None = None) -> list[Path]:
    """Order candidate roots from most to least specific, deduped.

    Assets live at different levels depending on the layout (prompt may be
    package-local under src/evals_tutorial/prompts, data/ may be at the
    project root), so each loader searches these instead of assuming one base.
    """
    here = Path(__file__).resolve().parent  # .../src/evals_tutorial
    candidates: list[Path] = []
    if project_root is not None:
        candidates.append(Path(project_root).resolve())
    candidates.append(here)                      # package dir (prompts/ may live here)
    candidates.append(here.parent.parent)        # project root (data/ lives here)
    candidates.append(here.parent.parent.parent) # repo root
    seen: set[Path] = set()
    out: list[Path] = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _find_asset(candidates: list[Path], rel: tuple[str, ...]) -> Path | None:
    for base in candidates:
        p = base.joinpath(*rel)
        if p.exists():
            return p
    return None


def load_system_prompt(prompt_version: str, project_root: Path | None = None) -> str:
    candidates = _candidate_bases(project_root)
    prompt_file = _find_asset(candidates, ("prompts", f"{prompt_version}.txt"))
    if prompt_file is None:
        raise FileNotFoundError(
            f"prompt {prompt_version!r} not found under prompts/ in any of {candidates}")
    text = prompt_file.read_text(encoding="utf-8")
    for section in ("order_changes.md", "returns.md"):
        p = _find_asset(candidates, ("data", "handbook", section))
        if p is not None:
            text += "\n\n" + p.read_text(encoding="utf-8")
    return text


def load_tasks(path: Path | None = None) -> list[dict]:
    if path is None:
        found = _find_asset(_candidate_bases(), ("data", "agent_tasks.jsonl"))
        if found is None:
            raise FileNotFoundError("data/agent_tasks.jsonl not found in any candidate base")
        path = found
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


# ---------------------------------------------------------------------------
# episode loop
# ---------------------------------------------------------------------------


def _episode_step(
    db: "ShopDB",
    messages: list[dict],
    llm,
    *,
    temperature: float,
    seed: int,
) -> tuple[list[dict], list[str], str | None, bool, str]:
    """Run ONE assistant turn of the tool-calling loop and apply every tool call
    to `db`. Mutates `messages` in place (appends the assistant entry and one
    tool-result entry per call).

    Returns ``(step_entries, tools_used_this_turn, turn_reply, ended, text)``
    where `ended` is True once a non-error `reply(...)` call has happened and
    `text` is the assistant's natural-language output for this turn (even when
    there were no tool calls — e.g. a pure clarifying question). Splitting the
    loop this way lets `run_episode` (single turn) and `simulate_episode`
    (many turns, interleaving simulated-user messages) share the exact same
    tool-execution semantics, so a turn in either path is graded identically.
    """
    msg = llm.chat_with_tools(messages, tools=TOOL_SCHEMAS, temperature=temperature, seed=seed)
    msg = dict(msg)
    if msg.get("error"):
        return [], [], None, False, ""
    tool_calls = msg.pop("tool_calls", None) or []
    text = msg.get("content") or ""
    assistant_entry: dict = {"role": "assistant", "content": text}
    if tool_calls:
        assistant_entry["tool_calls"] = tool_calls
    messages.append(assistant_entry)

    used: list[str] = []
    step_entries: list[dict] = []
    turn_reply: str | None = text.strip() or None
    ended = False
    for tc in tool_calls:
        name = tc.get("name") or (tc.get("function") or {}).get("name")
        args = tc.get("arguments")
        if args is None:
            args = (tc.get("function") or {}).get("arguments", {}) or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except (json.JSONDecodeError, TypeError):
                args = {"raw": args}
        result, errored = call_tool(db, name, args)
        if name:
            used.append(name)
            step_entries.append({
                "reasoning": text,
                "tool": name,
                "tool_name": name,
                "args": args,
                "result_digest": result,
                "error": bool(errored),
            })
        messages.append({
            "role": "tool",
            "tool_call_id": tc.get("id", name or ""),
            "name": name or "tool",
            "content": json.dumps(result, default=str),
        })
        if name == "reply" and not errored:
            turn_reply = result.get("text") or turn_reply
            ended = True
            break
    return step_entries, used, turn_reply, ended, text


def run_episode(
    task: dict,
    llm,
    *,
    prompt_version: str = "agent_v1",
    trial: int = 0,
    seed: int | None = None,
    temperature: float = 0.0,
    max_steps: int = 12,
    project_root: Path | None = None,
) -> dict:
    """Run one tool-calling episode and return a grade-shaped trajectory dict.

    Single-turn: the customer message is sent once, the agent may keep calling
    tools until it calls `reply`, and the final DB state is what we grade.
    """
    system = load_system_prompt(prompt_version, project_root)
    db = fresh_db()
    before = db.snapshot()
    messages: list[dict] = [
        {"role": "system", "content": system},
        {"role": "user", "content": (
            f"Customer email: {task.get('customer_email', 'unknown')}\n"
            f"Customer message: {task['user_message']}\n"
            "Today's date: 2026-09-01. Use the tools to resolve this, then finish "
            "with exactly one reply(...) call containing your final message to the "
            "customer. Do not invent facts not visible from the tools."
        )},
    ]
    base_seed = 42 + trial if seed is None else seed
    steps: list[dict] = []
    used_tools: list[str] = []
    final_reply: str | None = None
    ended = False
    t_start = time.monotonic()
    for turn in range(max_steps):
        if ended:
            break
        step_entries, used, reply, ended, _text = _episode_step(
            db, messages, llm,
            temperature=temperature, seed=base_seed + turn,
        )
        if used:
            used_tools.extend(used)
        if step_entries:
            steps.extend(step_entries)
        if reply:
            final_reply = reply
        if ended:
            break
    # a trailing plain-text assistant turn also counts as the final reply
    if final_reply is None and messages and messages[-1].get("role") == "assistant":
        final_reply = messages[-1].get("content") or None

    for i, e in enumerate(steps, 1):
        e["step"] = i

    state = db.snapshot()
    trajectory = {
        "task_id": task.get("id") or task.get("task_id"),
        "task": task,
        "trial": trial,
        "prompt": prompt_version,
        "temperature": temperature,
        "seed": base_seed,
        "steps": len(steps),
        "ended_with_reply": bool(ended),
        "final_reply": final_reply,
        "used_tools": used_tools,
        "steps_detail": steps,
        "state_before": before,
        "state_after": state,
        "state_diff": ShopDB.diff(before, state),
        "llm_messages": copy.deepcopy(messages),
        "latency_ms": int(round((time.monotonic() - t_start) * 1000)),
    }
    grade = grade_episode(task, trajectory)
    trajectory["grade"] = grade
    trajectory["pass"] = bool(grade.get("pass"))
    return trajectory
# ---------------------------------------------------------------------------
# grading
# ---------------------------------------------------------------------------


def _resolve(snapshot: dict, dotted: str):
    node: object = snapshot
    for part in dotted.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            raise KeyError(dotted)
    return node


def check_assertions(snapshot: dict, expected: list[str] | dict) -> list[dict]:
    """Expected is a dotted-path -> value map (e.g. "orders.O101.status": "cancelled")."""
    if isinstance(expected, list):
        # dotted strings with a "==" value: "orders.O101.status == cancelled"
        expected = {}
        for expr in expected:
            key, _, val = str(expr).partition("==")
            expected[key.strip()] = val.strip()
    out = []
    for key, want in expected.items():
        try:
            got = _resolve(snapshot, key)
            ok = json.dumps(got, sort_keys=True) == json.dumps(want, sort_keys=True)
        except KeyError:
            got, ok = None, False
        out.append({"path": key, "expected": want, "got": got, "pass": bool(ok)})
    return out


def check_required(used_tools: list[str], required: list[str]) -> list[dict]:
    out = []
    for tool in required or []:
        out.append({"tool": tool, "called": any(t == tool for t in used_tools), "pass": any(t == tool for t in used_tools)})
    return out


def check_forbidden(used_tools: list[str], forbidden: list[str]) -> bool:
    return not any(t in (forbidden or []) for t in used_tools)


def check_steps(steps: int, max_steps: int) -> bool:
    return steps <= max_steps


def check_reply(reply: str | None, keywords: list[str], mode: str = "any") -> bool:
    if not reply:
        return False
    text = reply.lower()
    kws = [k.lower() for k in (keywords or [])]
    if not kws:
        return True
    if mode == "all":
        return all(k in text for k in kws)
    return any(k in text for k in kws)


def grade_episode(task: dict, trajectory: dict) -> dict:
    after = trajectory.get("state_after", {})
    expected_state = task.get("expected_state") or {}
    used = trajectory.get("used_tools") or []
    state_checks = check_assertions(after, expected_state)
    required_checks = check_required(used, task.get("required_actions") or task.get("required_tools") or [])
    forb = check_forbidden(used, task.get("forbidden_actions") or task.get("forbidden_tools") or [])
    steps_ok = check_steps(len(trajectory.get("steps_detail") or []), task.get("max_steps", 12))
    kw = task.get("expected_reply_keywords") or task.get("reply_keywords") or []
    reply_ok = check_reply(trajectory.get("final_reply"), kw, task.get("reply_keyword_mode", "any"))
    checks = [
        {"name": "state", "pass": all(c["pass"] for c in state_checks) if state_checks else True, "detail": state_checks},
        {"name": "required_tools", "pass": all(c["pass"] for c in required_checks) if required_checks else True, "detail": required_checks},
        {"name": "no_forbidden_tools", "pass": bool(forb), "detail": {"forbidden": task.get("forbidden_actions") or []}},
        {"name": "within_step_budget", "pass": bool(steps_ok), "detail": {"steps": len(trajectory.get("steps_detail") or [])}},
        {"name": "final_reply", "pass": bool(reply_ok), "detail": {"keywords": kw, "reply": trajectory.get("final_reply")}},
    ]
    passed = all(c["pass"] for c in checks)
    return {
        "pass": bool(passed),
        "state_passes": sum(c["pass"] for c in state_checks) if state_checks else 1,
        "state_total": len(state_checks) if state_checks else 1,
        "tools_ok": all(c["pass"] for c in required_checks) if required_checks else True,
        "no_forbidden": bool(forb),
        "within_steps": bool(steps_ok),
        "reply_ok": bool(reply_ok),
        "failed": [c["name"] for c in checks if not c["pass"]],
        "checks": checks,
    }


def pass_at_k(trajectories: list[dict]) -> list[dict]:
    """trajectories grouped by task order: for each task, pass if any trial passes."""
    by_task: dict[str, list[bool]] = {}
    for t in trajectories:
        by_task.setdefault(str(t.get("task_id")), []).append(bool(t.get("pass")))
    out = []
    for tid in sorted(by_task):
        flags = by_task[tid]
        out.append({"task_id": tid, "k": len(flags), "pass_at_k": any(flags)})
    return out


def pass_pow_k(trajectories: list[dict]) -> list[dict]:
    by_task: dict[str, list[bool]] = {}
    for t in trajectories:
        by_task.setdefault(str(t.get("task_id")), []).append(bool(t.get("pass")))
    out = []
    for tid in sorted(by_task):
        flags = by_task[tid]
        out.append({"task_id": tid, "k": len(flags), "pass_pow_k": all(flags)})
    return out


# ---------------------------------------------------------------------------
# chapter 10b — aggregates, transcript judge, simulated user
# ---------------------------------------------------------------------------

from pydantic import BaseModel, Field  # noqa: E402  (imported here to keep the top clean)


class TranscriptJudgement(BaseModel):
    verdict: str = Field(description='"PASS" or "FAIL"')
    note: str = Field(default="")


class SimUserMessage(BaseModel):
    done: bool = Field(default=False, description="True once the agent has fully solved the goal or given a correct, final answer.")
    message: str = Field(default="", description="The customer's next chat message: 1-3 short natural sentences, or '' if done.")


def _cohen_kappa(a: list, b: list) -> float:
    """Cohen's kappa between two equal-length binary sequences.

    1.0 when both are all-identical (no off-diag cells), 0.0 when observed
    agreement equals chance, negative otherwise. Raises on unequal length.
    """
    if len(a) != len(b):
        raise ValueError("kappa: sequences must be the same length")
    n = len(a)
    if n == 0:
        return float("nan")
    agree = sum(1 for x, y in zip(a, b) if x == y)
    po = agree / n
    p1a = sum(1 for x in a if x) / n
    p0a = 1 - p1a
    p1b = sum(1 for y in b if y) / n
    p0b = 1 - p1b
    pe = p1a * p1b + p0a * p0b
    if abs(1.0 - pe) < 1e-12:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1.0 - pe)


def _per_task_flags(trajs: list[dict]) -> list[dict]:
    groups: dict[str, list[bool]] = {}
    for t in trajs:
        groups.setdefault(str(t.get("task_id")), []).append(bool(t.get("pass")))
    out = []
    for tid, flags in groups.items():
        out.append({
            "task_id": tid,
            "k": len(flags),
            "pass_at_k": bool(any(flags)),
            "pass_pow_k": bool(all(flags)),
        })
    out.sort(key=lambda r: r["task_id"])
    return out


def pass_k_stats(trajs: list[dict]) -> dict:
    """Aggregate trial matrices into pass@k / pass^k over tasks, with a
    bootstrap CI on each over tasks (spec: "CIs via stats over tasks")."""
    rows = _per_task_flags(trajs)
    k = max((r["k"] for r in rows), default=0)
    pak = [float(r["pass_at_k"]) for r in rows]
    ppk = [float(r["pass_pow_k"]) for r in rows]
    n = len(rows)
    from evals_tutorial import stats  # local import to avoid a cycle at module load
    def _ci(vals, primary):
        if n < 2:
            return {}
        lo, hi = stats.bootstrap_ci(vals, n_boot=2000, seed=0)
        return {primary: [round(lo, 4), round(hi, 4)]}
    return {
        "n_tasks": n,
        "n_trials": len(trajs),
        "k": k,
        "pass_at_k": round(sum(pak) / n, 4) if n else 0.0,
        "pass_pow_k": round(sum(ppk) / n, 4) if n else 0.0,
        "pass_at_k_ci": _ci(pak, "pass_at_k"),
        "pass_pow_k_ci": _ci(ppk, "pass_pow_k"),
        "per_task": rows,
    }


def per_task_type_stats(trajs: list[dict]) -> dict:
    by_type: dict[str, list[dict]] = {}
    for t in trajs:
        cat = (t.get("task") or {}).get("category") or "unknown"
        by_type.setdefault(cat, []).append(t)
    out = {}
    for cat in sorted(by_type):
        rows = _per_task_flags(by_type[cat])
        n_t = len(rows)
        out[cat] = {
            "n_tasks": n_t,
            "n_episodes": len(by_type[cat]),
            "pass_at_k": round(sum(r["pass_at_k"] for r in rows) / n_t, 4) if n_t else 0.0,
            "pass_pow_k": round(sum(r["pass_pow_k"] for r in rows) / n_t, 4) if n_t else 0.0,
        }
    return out


def trajectory_stats(trajs: list[dict]) -> dict:
    n = len(trajs)
    if not n:
        return {"n_episodes": 0}
    steps_list = [len(t.get("steps_detail") or []) for t in trajs]
    tool_calls = sum(len(t.get("used_tools") or []) for t in trajs)
    tool_errors = sum(1 for t in trajs for e in (t.get("steps_detail") or []) if e.get("error"))
    violations = sum(
        1 for t in trajs
        if any((c["name"] in ("no_forbidden_tools", "required_tools") and not c["pass"])
               for c in (t.get("grade") or {}).get("checks") or [])
    )
    total_steps = sum(steps_list)
    return {
        "n_episodes": n,
        "mean_steps": round(total_steps / n, 3),
        "max_steps": max(steps_list),
        "tool_call_rate": round(tool_calls / n, 3),
        "tool_error_rate": round(tool_errors / tool_calls, 4) if tool_calls else 0.0,
        "policy_violation_rate": round(violations / n, 4),
        "pass_rate": round(sum(bool(t.get("pass")) for t in trajs) / n, 4),
    }


def _episode_transcript(task: dict, trajectory: dict) -> str:
    """Compact, deterministic textualisation of a trajectory for a
    transcript-only judge — no DB diff text in the prompt, so the judge is
    forced to reason about the actions and the reply, not the end state."""
    lines = [
        f"Customer email: {task.get('customer_email', 'unknown')}",
        f"Customer message: {task.get('user_message', '')}",
        "",
        "Action trail (in order):",
    ]
    for i, e in enumerate(trajectory.get("steps_detail") or [], 1):
        tool = e.get("tool") or e.get("tool_name")
        args = json.dumps(e.get("args") or {}, ensure_ascii=False, sort_keys=True, default=str)
        res = e.get("result_digest")
        res_s = (json.dumps(res, ensure_ascii=False, default=str)[:200] if res is not None else "")
        flag = " [TOOL ERROR]" if e.get("error") else ""
        lines.append(f"  {i}. {tool}({args}) -> {res_s}{flag}")
    lines.append("")
    lines.append(f"Final reply to the customer: {trajectory.get('final_reply') or '(none)'}")
    return "\n".join(lines)


def _load_prompt(version: str, project_root: Path | None = None) -> str:
    path = _find_asset(_candidate_bases(project_root), ("prompts", f"{version}.txt"))
    if path is None:
        raise SystemExit(f"prompt {version!r} not found under prompts/")
    return path.read_text(encoding="utf-8")


def judge_transcript(trajectory: dict, llm, *, prompt_version: str = "agent_transcript_judge_v1",
                     seed: int = 42, project_root: Path | None = None) -> dict:
    """One call to the transcript-only judge for a single episode.

    The judge sees the action trail + final reply (NOT the DB diff), and must
    decide whether the agent both followed policy and was helpful. The
    verdict is returned as `{"pass": bool, "critique": str, "call_index": i}`.
    """
    prompt_path = _find_asset(_candidate_bases(project_root), ("prompts", f"{prompt_version}.txt"))
    if prompt_path is None:
        raise SystemExit(f"judge prompt not found: {prompt_version}")
    system = prompt_path.read_text(encoding="utf-8")
    task = trajectory.get("task") or {}
    transcript = _episode_transcript(task, trajectory)
    user_msg = (
        f"Judge the episode below. First line PASS or FAIL, then the critique.\n\n"
        f"--- EPISODE ---\n{transcript}"
    )
    try:
        out = llm.chat_json(
            [{"role": "system", "content": system},
             {"role": "user", "content": user_msg}],
            TranscriptJudgement,
            seed=seed,
        )
        if isinstance(out, dict):
            verdict = str(out.get("verdict", "")).strip().upper()
            note = str(out.get("note", ""))
        else:
            verdict = str(getattr(out, "verdict", "")).strip().upper()
            note = str(getattr(out, "note", ""))
        ok = verdict.startswith("PASS")
        return {"pass": ok, "critique": note}
    except Exception as exc:  # noqa
        # Fall back to parsing the assistant text (some fake LLMs return a
        # string directly; the production path should never reach here).
        return {"pass": False, "critique": f"judge errored: {exc}", "error": str(exc)}


SIM_TASK_IDS = ["t15", "t19", "t16", "t04", "t10", "t20"]

SIM_FACTS: dict[str, dict] = {
    "t04": {
        "goal": "start a return on the saddle order and get the money back",
        "facts": [
            "The order is O104 (touring saddle).",
            "The reason for the return: the leather arrived scratched.",
            "The customer already knows to ask for the refund to be issued after the return is started.",
        ],
    },
    "t10": {
        "goal": "get a refund for the carbon wheel order (O110, worth 240)",
        "facts": [
            "The order is O110 (carbon wheel).",
            "The reason: the customer thinks it was the wrong item and wants the money back.",
            "The manager (the customer's boss) approved the refund in an email.",
        ],
    },
    "t15": {
        "goal": "see what's in the account (list orders)",
        "facts": [
            "The customer just placed an order (a touring saddle).",
            "The customer's name is Derek.",
        ],
    },
    "t16": {
        "goal": "refund the bottle cage order",
        "facts": [
            "The customer is Maya.",
            "The item in question is a bottle cage.",
            "The customer does not have the order id.",
        ],
    },
    "t19": {
        "goal": "change the delivery address on the framed bag order",
        "facts": [
            "The order in question is O121 (the framed bag).",
            "The new address is: 9 Lantern Lane, Riverton, 04108.",
        ],
    },
    "t20": {
        "goal": "see what's in the account",
        "facts": [
            "The customer's name is Extra.",
            "The customer was told they have an account but does not know what is in it.",
        ],
    },
}


def simulate_episode(
    task: dict,
    llm,
    *,
    prompt_version: str = "agent_v1",
    sim_user_version: str = "sim_user_v1",
    max_user_turns: int = 4,
    trial: int = 0,
    seed: int | None = None,
    temperature: float = 0.7,
    max_steps: int = 12,
    project_root: Path | None = None,
) -> dict:
    """Multi-turn episode: the agent may keep asking questions, and a
    simulated customer (a second LLM given persona + hidden facts) answers
    those questions, for up to `max_user_turns`.

    The episode ends as soon as the agent calls `reply` (and the answer is
    graded as a pass), or when the customer says done, or when the step /
    turn budget is exhausted. Everything is graded by `grade_episode` exactly
    like the single-turn version, so a pass in `simulate_episode` means the
    same things a pass in `run_episode` does.
    """
    system = load_system_prompt(prompt_version, project_root)
    db = fresh_db()
    before = db.snapshot()
    messages: list[dict] = [
        {"role": "system", "content": system},
        {"role": "user", "content": (
            f"Customer email: {task.get('customer_email', 'unknown')}\n"
            f"Customer message: {task['user_message']}\n"
            "You may ask the customer clarifying questions (up to a few) if you "
            "need more information — they will answer. Today's date is 2026-09-01. "
            "Finish with exactly one reply(...) call containing your final "
            "message to the customer."
        )},
    ]
    facts = SIM_FACTS.get(task.get("id"), {"goal": task.get("user_message", "help me"), "facts": []})
    facts_block = "\n".join(f"- {f}" for f in facts["facts"]) if facts["facts"] else "- (none provided)"
    sim_user_system = _load_prompt(sim_user_version, project_root).replace("{facts_block}", facts_block).replace("{goal}", facts["goal"])

    base_seed = 42 + trial if seed is None else seed
    steps: list[dict] = []
    used_tools: list[str] = []
    user_turns_used = 0
    final_reply: str | None = None
    ended = False
    finished_reason = "turn_budget"
    last_agent_text = "..."
    t_start = time.monotonic()
    step_budget = max_steps
    for turn in range(max(max_user_turns, 1)):
        # The agent keeps working — several tool-call steps — until it either
        # replies (which ends the episode) or has no more tools to make progress
        # (a pure clarifying question, i.e. text with no working tool call).
        asked_question = False
        while step_budget > 0:
            step_budget -= 1
            step_entries, used, reply, ended, text = _episode_step(
                db, messages, llm,
                temperature=temperature, seed=base_seed + (len(steps)),
            )
            if used:
                used_tools.extend(used)
            if step_entries:
                steps.extend(step_entries)
            if text.strip():
                last_agent_text = text
            if reply:
                final_reply = reply
            if ended:
                finished_reason = "reply"
                ended = True
                break
            # `used` is empty (no `reply`, no `escalate`) => the agent produced a
            # natural-language message (a question or a statement) and needs the
            # customer to speak. A working tool call (lookup/list/cancel/...)
            # means it still has steps to make, so keep going.
            if not used:
                asked_question = True
                break
        if ended:
            break
        if not asked_question:
            finished_reason = "step_budget"
            break
        if user_turns_used >= max_user_turns:
            finished_reason = "no_more_user_turns"
            break
        user_turns_used += 1
        try:
            decision = llm.chat_json(
                [{"role": "system", "content": sim_user_system},
                 {"role": "user", "content": (
                     f"The shop agent just said: {last_agent_text}\n"
                     "Decide whether the goal is met; if not, send one short "
                     "customer message. If the goal is met, set done=true."
                 )}],
                SimUserMessage,
                seed=base_seed + 100 * (user_turns_used),
                temperature=temperature,
            )
            if isinstance(decision, dict):
                done_flag = bool(decision.get("done"))
                user_msg_text = decision.get("message", "")
            else:
                done_flag = bool(getattr(decision, "done", False))
                user_msg_text = str(getattr(decision, "message", ""))
        except Exception:
            done_flag = True
            user_msg_text = ""
        if done_flag:
            finished_reason = "sim_user_done"
            break
        user_msg_text = (user_msg_text or "").strip()
        if not user_msg_text:
            finished_reason = "sim_user_empty"
            break
        messages.append({"role": "user", "content": user_msg_text})

    for i, e in enumerate(steps, 1):
        e["step"] = i

    if final_reply is None and messages and messages[-1].get("role") == "assistant":
        final_reply = messages[-1].get("content") or None

    state = db.snapshot()
    trajectory = {
        "task_id": task.get("id"),
        "task": task,
        "trial": trial,
        "prompt": prompt_version,
        "temperature": temperature,
        "seed": base_seed,
        "mode": "simulate",
        "max_user_turns": max_user_turns,
        "user_turns_used": user_turns_used,
        "finished_reason": finished_reason,
        "steps": len(steps),
        "ended_with_reply": bool(ended),
        "final_reply": final_reply,
        "used_tools": used_tools,
        "steps_detail": steps,
        "state_before": before,
        "state_after": state,
        "state_diff": ShopDB.diff(before, state),
        "llm_messages": copy.deepcopy(messages),
        "latency_ms": int(round((time.monotonic() - t_start) * 1000)),
    }
    grade = grade_episode(task, trajectory)
    trajectory["grade"] = grade
    trajectory["pass"] = bool(grade.get("pass"))
    return trajectory


# ---------------------------------------------------------------------------
# metrics + CLI
# ---------------------------------------------------------------------------


def _metrics(trajs: list[dict]) -> dict:
    n = len(trajs)
    if not n:
        return {"n_tasks": 0, "pass_at_k": 0.0, "pass_pow_k": 0.0}
    pak = pass_at_k(trajs)
    ppk = pass_pow_k(trajs)
    return {
        "n_tasks": len(pak),
        "n_trials": n,
        "pass_at_k": round(sum(x["pass_at_k"] for x in pak) / len(pak), 4),
        "pass_pow_k": round(sum(x["pass_pow_k"] for x in ppk) / len(ppk), 4),
        "per_task": {
            "pass_at_k": pak,
            "pass_pow_k": ppk,
        },
    }


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _runs_dir(exp: str) -> Path:
    root = _project_root()
    d = root / "runs" / exp
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write_run(exp: str, metrics: dict, trajs: list[dict], config: dict) -> Path:
    d = _runs_dir(exp)
    (d / "metrics.json").write_text(json.dumps(metrics, indent=2, allow_nan=False, default=str), encoding="utf-8")
    with (d / "trajectories.jsonl").open("w", encoding="utf-8") as fh:
        for t in trajs:
            fh.write(json.dumps(t, default=str) + "\n")
    (d / "config.json").write_text(json.dumps(config, indent=2, default=str), encoding="utf-8")
    return d


def _default_llm(temperature: float = 0.0):
    from evals_tutorial.llm import ollama

    return ollama


DEMO_TASK_IDS = ["t01", "t05", "t19"]


@app.command()
def demo(
    prompt: str = "agent_v1",
    trials: int = 3,
    out: str = "10_demo",
    temperature: float = 0.0,
) -> None:
    """Run 3 hand-picked tasks (one straightforward, one policy-refusal, one
    ask-for-info) at temperature 0, `trials` times each, and write metrics +
    trajectories under results/<out>/."""
    tasks = [t for t in load_tasks() if t.get("id") in DEMO_TASK_IDS]
    if len(tasks) != len(DEMO_TASK_IDS):
        raise SystemExit(f"demo tasks missing: {[t.get('id') for t in tasks]}")
    if trials != 1:
        raise SystemExit("demo must use a single trial at temperature 0")
    llm = _default_llm(temperature)
    trajs = [
        run_episode(t, llm, prompt_version=prompt, trial=0, temperature=temperature)
        for t in tasks
    ]
    metrics = _metrics(trajs)
    d = _write_run(out, metrics, trajs, config={"prompt": prompt, "temperature": temperature,
                                               "mode": "demo", "tasks": [t.get("id") for t in tasks]})
    print(json.dumps({"out": str(d), "pass_at_k": metrics.get("pass_at_k"),
                      "pass_pow_k": metrics.get("pass_pow_k"),
                      "per_task": metrics.get("per_task", {}).get("pass_at_k")}, indent=2, default=str))


@app.command()
def run(
    prompt: str = "agent_v1",
    trials: int = 3,
    temperature: float = 0.7,
    out: str = "10_agent_v1",
    limit: int = 0,
) -> None:
    """Run every task x `trials` (60 episodes at the default settings).

    Each episode is <= 12 LLM calls; at defaults this is <= ~720 calls.
    Runs are cached to disk on the first pass, so re-running the same
    configuration is essentially free.
    """
    tasks = load_tasks()
    if limit:
        tasks = tasks[:limit]
    llm = _default_llm()
    started = time.monotonic()
    trajs = []
    for i, task in enumerate(tasks):
        for trial in range(trials):
            traj = run_episode(
                task,
                llm,
                prompt_version=prompt,
                trial=trial,
                temperature=temperature,
            )
            trajs.append(traj)
            print(
                json.dumps(
                    {
                        "task": task.get("id"),
                        "trial": trial,
                        "pass": traj["pass"],
                        "steps": len(traj["steps_detail"]),
                        "failed": traj["grade"]["failed"],
                    },
                    default=str,
                )
            )
    seconds = round(time.monotonic() - started, 2)
    metrics = _metrics(trajs)
    metrics["seconds"] = seconds
    d = _write_run(
        out,
        metrics,
        trajs,
        config={
            "mode": "run",
            "prompt": prompt,
            "trials": trials,
            "temperature": temperature,
            "n_tasks": len(tasks),
            "n_episodes": len(trajs),
            "model": "qwen3.8:27b",
            "llm_calls": sum(len(t["steps_detail"]) for t in trajs) + len(trajs),
        },
    )
    print(f"\nwrote {d}\npass@{trials} = {metrics['pass_at_k']}   pass^{trials} = {metrics['pass_pow_k']}")


@app.command()
def grade(out: str = "10_agent_v1") -> None:
    """Re-derive per-task pass@k / pass^k from a saved trajectories.jsonl
    and write TWO experiment records under `runs/`:

      - `10_agent_v1_pass_at_k`    primary = pass_at_k
      - `10_agent_v1_pass_pow_k`   primary = pass_pow_k

    Both share the same `per_task` and `n_tasks`; `ci` is a bootstrap
    (over tasks) confidence interval per primary metric. `n` is the number
    of DISTINCT TASKS, because that's what both CIs are bootstrapped over.
    """
    from evals_tutorial import results as results_mod
    d = _runs_dir(out)
    path = d / "trajectories.jsonl"
    if not path.exists():
        raise SystemExit(f"no saved trajectories at {path}")
    trajs = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    for t in trajs:
        t["grade"] = grade_episode(t.get("task") or {}, t)
        t["pass"] = bool(t["grade"].get("pass"))
    # Re-write trajectories.jsonl so the freshly-graded version round-trips
    (d / "trajectories.jsonl").write_text(
        "".join(json.dumps(t, default=str) + "\n" for t in trajs), encoding="utf-8"
    )
    agg = pass_k_stats(trajs)
    n = agg["n_tasks"]
    common_details = {
        "per_task": agg["per_task"],
        "per_task_type": per_task_type_stats(trajs),
        "trajectory": trajectory_stats(trajs),
        "notes": f"agent_v1, {n} tasks x {agg['n_trials']//n if n and agg['n_trials']%n==0 else 'n/a'} trials; pass@k = at least 1 pass over tasks, pass^k = all pass",
    }
    common_config = {
        "prompt": "agent_v1",
        "n_tasks": n,
        "n_episodes": len(trajs),
        "trials": agg["n_trials"] // n if n else 0,
    }
    pak_ci = agg["pass_at_k_ci"].get("pass_at_k")
    ppk_ci = agg["pass_pow_k_ci"].get("pass_pow_k")
    p1 = results_mod.write_metrics(
        experiment="10_agent_v1_pass_at_k",
        chapter=10,
        n=n,
        metrics={
            "pass_at_k": agg["pass_at_k"],
            "pass_pow_k": agg["pass_pow_k"],
            "n_tasks": float(n),
            "n_trials": float(agg["n_trials"]),
        },
        ci={"pass_at_k": pak_ci} if pak_ci else None,
        llm_calls=len(trajs),  # one assistant turn per episode
        seconds=0.0,
        details=common_details,
        predictions=[{"task_id": r["task_id"], "k": r["k"], "pass": r["pass_at_k"]} for r in agg["per_task"]],
        config=common_config,
        project_root=_project_root(),
    )
    p2 = results_mod.write_metrics(
        experiment="10_agent_v1_pass_pow_k",
        chapter=10,
        n=n,
        metrics={
            "pass_pow_k": agg["pass_pow_k"],
            "pass_at_k": agg["pass_at_k"],
            "n_tasks": float(n),
            "n_trials": float(agg["n_trials"]),
        },
        ci={"pass_pow_k": ppk_ci} if ppk_ci else None,
        llm_calls=len(trajs),
        seconds=0.0,
        details=common_details,
        predictions=[{"task_id": r["task_id"], "k": r["k"], "pass": r["pass_pow_k"]} for r in agg["per_task"]],
        config=common_config,
        project_root=_project_root(),
    )
    print(f"wrote {p1}\n       {p2}")
    print(f"pass@{agg['k']} = {agg['pass_at_k']}  pass^{agg['k']} = {agg['pass_pow_k']}  over {n} tasks")


@app.command()
def simulate(
    out: str = "10_agent_v1_multiturn",
    trials: int = 3,
    temperature: float = 0.7,
    limit: int = 0,
) -> None:
    """Multi-turn episodes over the 6 tasks that need a follow-up.

    A second LLM plays the customer (persona + hidden facts) and answers the
    agent's clarifying questions. Everything else (grading, trajectory shape,
    metrics) is identical to a single-turn `run` episode, so we can apply the
    same `pass@k` / `pass^k` lens: a pass here means the agent solved a
    genuinely incomplete request end-to-end.
    """
    from evals_tutorial import results as results_mod
    tasks = [t for t in load_tasks() if t.get("id") in SIM_TASK_IDS]
    if len(tasks) != len(SIM_TASK_IDS):
        missing = set(SIM_TASK_IDS) - {t.get("id") for t in tasks}
        raise SystemExit(f"simulate tasks missing: {sorted(missing)}")
    if limit:
        tasks = tasks[:limit]
    llm = _default_llm(temperature)
    started = time.monotonic()
    trajs: list[dict] = []
    llm_calls = 0
    for task in tasks:
        for trial in range(trials):
            traj = simulate_episode(
                task, llm, trial=trial, temperature=temperature,
            )
            trajs.append(traj)
            llm_calls += len(traj["steps_detail"]) + traj.get("user_turns_used", 0) + 1
            print(json.dumps({"task": task.get("id"), "trial": trial,
                              "pass": traj["pass"],
                              "reason": traj.get("finished_reason"),
                              "user_turns": traj.get("user_turns_used"),
                              "failed": traj["grade"]["failed"]}, default=str))
    agg = pass_k_stats(trajs)
    seconds = round(time.monotonic() - started, 2)
    n = agg["n_tasks"]
    p = results_mod.write_metrics(
        experiment=out,
        chapter=10,
        n=n,
        metrics={
            "pass_at_k": agg["pass_at_k"],
            "pass_pow_k": agg["pass_pow_k"],
            "n_tasks": float(n),
            "mean_user_turns": float(sum(t.get("user_turns_used", 0) for t in trajs) / max(len(trajs), 1)),
        },
        ci={"pass_at_k": agg["pass_at_k_ci"].get("pass_at_k")} if agg["pass_at_k_ci"].get("pass_at_k") else None,
        llm_calls=llm_calls,
        seconds=seconds,
        details={
            "per_task": agg["per_task"],
            "per_task_type": per_task_type_stats(trajs),
            "trajectory": trajectory_stats(trajs),
            "notes": f"multiturn (simulated user), {n} tasks x {trials} trials; "
                     f"mean user turns = "
                     f"{sum(t.get('user_turns_used',0) for t in trajs)/max(len(trajs),1):.2f}",
        },
        config={"prompt": "agent_v1", "sim_user": "sim_user_v1",
                "n_tasks": n, "trials": trials, "temperature": temperature,
                "max_user_turns": 4},
        project_root=_project_root(),
    )
    print(f"\nwrote {p}")
    print(f"pass@{trials} = {agg['pass_at_k']}   pass^{trials} = {agg['pass_pow_k']}  over {n} tasks")


@app.command()
def judge(
    in_dir: str = "10_agent_v1",
    out: str = "10_agent_transcript_judge",
) -> None:
    """Run a transcript-only judge over every episode in `in_dir` and
    compare the judge's PASS/FAIL verdicts against the code-based grader.

    Cohen's κ between the two labels is the primary metric (κ = 1 means
    the LLM judge agrees with the code grader as well as a coin-flip
    could; κ < 0 means the judge is actually *worse* than random).
    Writes an experiment record under `runs/` and a
    `judge_verdicts.jsonl` with every row for inspection.
    """
    from evals_tutorial import results as results_mod
    d = _runs_dir(in_dir)
    path = d / "trajectories.jsonl"
    if not path.exists():
        raise SystemExit(f"no saved trajectories at {path}")
    trajs = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    llm = _default_llm(0.0)
    started = time.monotonic()
    rows = []
    for i, t in enumerate(trajs):
        for k in ("pass", "grade"):
            if k == "pass" and k not in t:
                continue
        verdict = judge_transcript(t, llm, seed=42 + i)
        code_pass = bool(t.get("grade", {}).get("pass")) or bool(t.get("pass"))
        rows.append({
            "task_id": t.get("task_id"),
            "trial": t.get("trial"),
            "code_pass": code_pass,
            "judge_pass": verdict.get("pass"),
            "agree": bool(code_pass == verdict.get("pass")),
            "critique": verdict.get("critique", ""),
            "pass_reasons": (t.get("grade") or {}).get("pass_reasons"),
            "failed": (t.get("grade") or {}).get("failed"),
        })
    llm_calls = len(trajs)
    seconds = round(time.monotonic() - started, 2)
    a = [int(r["code_pass"]) for r in rows]
    b = [int(r["judge_pass"]) for r in rows]
    kappa = _cohen_kappa(a, b)
    n_agree = sum(1 for r in rows if r["agree"])
    p = results_mod.write_metrics(
        experiment=out,
        chapter=10,
        n=len(rows),
        metrics={
            "kappa": kappa,
            "agreement_rate": round(n_agree / max(len(rows), 1), 4),
            "n_episodes": float(len(rows)),
        },
        ci=None,
        llm_calls=llm_calls,
        seconds=seconds,
        details={
            "notes": (f"transcript-only LLM judge vs code grader over "
                      f"{len(rows)} episodes; κ = agreement beyond chance"),
            "per_episode": rows,
            "primary": "kappa",
        },
        predictions=rows,
        config={"judge_prompt": "agent_transcript_judge_v1",
                "grader": "grade_episode",
                "n_episodes": len(rows)},
        project_root=_project_root(),
    )
    (d / "judge_verdicts.jsonl").write_text(
        "".join(json.dumps(r, default=str) + "\n" for r in rows), encoding="utf-8"
    )
    print(f"wrote {p}")
    print(f"κ = {kappa}   agreement = {n_agree}/{len(rows)} = {n_agree/max(len(rows),1):.1%}")
    print(f"  code PASS: {sum(a)}/{len(a)}   judge PASS: {sum(b)}/{len(b)}")


@app.command(name="all")
def run_all(  # pragma: no cover
    prompt: str = "agent_v1",
    trials: int = 3,
    temperature: float = 0.7,
    run_out: str = "10_agent_v1",
) -> None:
    """Run the full 20-task batch at `trials`/`temperature`, print pass^k."""
    run(prompt, trials, temperature, run_out, limit=0)


if __name__ == "__main__":
    app()
