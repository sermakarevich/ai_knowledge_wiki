> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# How to build with TypeSafe

**In one sentence:** Build normal software where code owns control flow and side effects, and insert System One only for narrow, atomic, typed questions over minimal relevant state — asking many in parallel and composing their probabilities and confidence in code.

## Key points

- System One is TypeSafe's model for AI-powered software, not agents: it does not generate code or choose its own next action, it provides AI primitives that embed into software so code stays in control while the model handles common-sense judgments over unstructured data.
- The build summary is: keep control flow, deterministic rules, and side effects in code; break broad judgments into narrow typed questions; give each question only needed context; use probabilities/confidence to act, review, or escalate; ask independent questions together and compose answers in code.
- System One is composable because outputs are structured (type-safe JSON schema, no parsing prose), parallel (independent, no hidden cross-context), comparable (sortable, threshold-able), fast (~100 ms, real-time-ready), calibrated via RLCD, and self-consistent across repeated evaluations.
- Because outputs are constrained to supplied options, the model returns a full probability distribution over those options instead of inventing out-of-schema values; TypeSafe's target is a greater than 100× intelligence-to-speed-and-cost ratio.
- Agents loop and choose their next step (fine with a human watching, but each loop risks going off the rails), while AI-powered software keeps atomic constrained AI tasks inside code-owned workflows — and deterministic work like `days_overdue > 30 → route_to_collections` stays in code, never in agent `while` loops.
- Decompose ruthlessly: send only relevant state (e.g. ticket message + refund policy for one Noul), use nested JSON with backticked dot-and-index paths like `support.tickets[0].message`, and split broad questions (one "is this spam?" becomes six atomic Nouls; one "are tool calls correct?" becomes nine checks).
- For Choice, use structured contrastive criteria with the same fields per option (`what` / `not_for` / `examples`); short unambiguous questions can stay strings, and structure goes where guidance would otherwise blur.
- Scale by asking many narrow questions in one parallel request (no extra round trips), combine with weighted sums like `0.4·answers_request + 0.4·citations_supported + 0.2·(1−contradicts_context)`, and route on uncertainty (e.g. `confidence < 0.8 → human review`; plot confidence vs accuracy to set thresholds).

---

## Three software architectures

TypeSafe is designed for **AI-powered software**, where code owns the workflow and AI handles narrow, structured decisions:

| Architecture | How it works | Trade-off |
|---|---|---|
| Traditional software | Complex decision tree from simple reliable primitives, composed into higher-level abstractions. | Reliable but no common-sense over unstructured data. |
| LLM agents | Agent processes instructions and chooses its next step. | Works with a person monitoring; every loop is another chance to go off the rails. |
| AI-powered software | Code handles deterministic work and owns control flow; the model appears only where programmable common sense or unstructured-data interpretation is needed, each task atomic and constrained. | Bounded AI inside reliable software. |

## What makes System One composable

- **Structured:** type-safe by construction — decisions and probabilities conform to the JSON schema code expects, never recovered from generated prose.
- **Parallel:** questions evaluated independently and in parallel; one primitive's result never becomes hidden context for another.
- **Comparable:** outputs are sortable and drive `if` statements, thresholds, and comparisons.
- **Fast:** most queries complete in about 100 ms — fast enough for real-time request paths and UIs.
- **Calibrated confidence:** RLCD communicates uncertainty through calibrated probabilities instead of overconfidence.
- **Self-consistent:** designed for stable answers across repeated evaluations (see the self-consistency cookbook).

> "Because every output is constrained to the supplied options, the model returns a full probability distribution over those options rather than inventing a value outside the schema."

TypeSafe's target is a greater than 100× intelligence-to-speed-and-cost ratio, betting cheaper intelligence creates much more demand.

## Design a System One workflow

1. **Use code when you can.** Keep deterministic work in code — reliable and cheap; avoid agent `while` loops where a workflow suffices (e.g. `days_overdue > 30 → route_to_collections`). Browse the System One patterns for bounded compositions.
2. **Decompose the input state.** Include only relevant context to avoid distractions and context rot; don't rely on model weights when your knowledge base has current info (example: just `ticket_message` + `refund_policy` for one refund-support Noul).
3. **Use structure in the input state.** Nested JSON for `state`/`questions`; point questions at values with backticked paths like `` `support.tickets[0].message` `` or `` `commerce.orders[0].charges` `` to remove ambiguity.
4. **Decompose the questions.** Ask the most explicit, narrow, atomic questions; broad questions hide judgments behind one answer while atomic ones expose them for inspection and tuning. Spam: one bad `Is message spam?` vs six good Nouls (`requests_credentials`, `offers_unexpected_reward`, `creates_time_pressure`, `sender_identity_mismatch`, `link_domain_mismatch`, `disguises_link_destination`). Tool-trace check: one bad `Is trace.tool_calls correct?` vs nine good Nouls (tool relevance, location match, schema conformance, result linkage, coordinates/date/unit matches).
5. **Use structure in the questions.** Keep atomic questions short; when guidance needs kinds (e.g. Choice options), use objects/arrays with named fields and identical field names across options — `what` / `not_for` / `examples` (card-topic example: `get_disposable_virtual_card` vs `disposable_card_limits`).
6. **Ask a lot of questions.** Many narrow independent questions over one state in one request run in parallel — effectiveness and intelligence-per-dollar without serial round trips (Speculative Fan-Out pattern).
7. **Combine outputs in code (or a classical ML model).** Deterministic rules/weighted sums, or probabilities as features for a downstream classifier; example weight `0.4 * answers["answers_request"].noul + 0.4 * answers["citations_are_supported"].noul + 0.2 * (1 - answers["contradicts_context"].noul)`. Without labels, use expensive-reasoning-model ensembles for labels (AutoResearch cookbook).
8. **Route on uncertainty.** Confident vs unconfident answers take different actions; escalate to a person or bigger reasoning model (example gate `answer.confidence < 0.8 → route_to_human_review`); test thresholds by plotting confidence against accuracy.

> "Decomposition does not require more round trips. Questions over the same state run in parallel."

## Putting it all together

The `triage_ticket.py` workflow keeps deterministic work in code (skip closed tickets, filter undelivered orders), sends only structured context (ticket message/sender/links, customer plan/open orders, sensitive-credential policy), asks seven atomic questions in one parallel request (topic Choice, five Nouls, frustration Score), then composes in code:

- Spam risk `= 0.45·requests_credentials + 0.30·sender_identity_mismatch + 0.25·unexpected_reward`; uncertain band `0.4 < spam_risk < 0.6` or `topic.confidence < 0.75` → human review; `spam_risk ≥ 0.6` → quarantine.
- Billing path uses `refund_requested.noul ≥ 0.7`, orders path uses `mentions_open_order.noul ≥ 0.7`; account-support priority is high only if `frustration.confidence ≥ 0.7` and `frustration.score ≥ 1.5`.

**Covers:** How to build with TypeSafe — code in control, System One for narrow structured decisions (source/topics/concepts_how-to-build-with-system-one.md)
