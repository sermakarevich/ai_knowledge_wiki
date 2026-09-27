---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Introduction - TypeSafe AI

### Q1. Why does using a large language model (LLM — AI model trained to predict text) for a judgment that code will consume create a mismatch, and how does Jev resolve it?

> [!tip]- Answer
> LLMs are designed to produce text for humans to read, so getting a code-consumable judgment means coercing text generation into structured decisions and parsing the results back — a fragile step for code to depend on. Jev, TypeSafe's flagship and first System One model, instead evaluates typed questions against a state and returns structured results directly: typed values and probability distributions that code can branch on, sort by, and route with.
> See [[wiki/01-documentation-index|Documentation Index — Introduction - TypeSafe AI]].

### Q2. What are the four ways to try TypeSafe from the Quick Start, and what does the sample mixed request return?

> [!tip]- Answer
> You can try TypeSafe in the Playground (paste text as state, mix Noul/Choice/Score in one call), via POST to `https://api.typesafe.ai/v1/systemone` with model `jev-latest`, via the Python SDK (`pip install typesafe-sdk`, Python >= 3.10, `client.system_one(state=..., questions={...})`), or via the TypeSafe agent skill for coding agents. The sample Stripe-complaint request returns `choice: "technical"` (probabilities 0.159/0.84/0.001, confidence 0.596), `score: 1.035` (confidence 0.842), `noul: 0.999`, with usage of 312 input and 48 output tokens.
> See [[wiki/02-quick-start|Quick Start]].

### Q3. What is a System One model, and what does calibration mean — and not mean — for its answers?

> [!tip]- Answer
> A System One model evaluates a state and returns typed answers and probabilities for software to use directly; like an LLM it understands natural-language input, but it never writes replies, produces code, or explains its reasoning. Its probabilities are trained to be calibrated — optimized against outcomes so that, across groups of predictions, outcomes assigned 0.8 occur ~80% of the time — but calibration does not guarantee any individual answer is correct, which is why answers carry confidence for act-vs-escalate decisions.
> See [[wiki/03-system-one|System One]].

### Q4. What is `state`, and how should you shape it for a request?

> [!tip]- Answer
> State is the content in the `state` field that the model evaluates — one state per request, seen identically and independently by every question, with Choice, Score, and Noul freely mixed. The simplest state is a plain string like `"My card was charged twice."`, but prefer a JSON object with descriptive names for multi-part decisions (e.g. ticket + order with two $49 charges + refund_policy kept together), so the state holds the facts while the questions define the judgments.
> See [[wiki/04-state|State]].

### Q5. What are the three primitives, what does each return, and what are the rules for picking between them?

> [!tip]- Answer
> Choice answers which option (returns `choice`, `probabilities`, `confidence`), Score answers which level (returns `score`, `legend`, `probabilities`, `confidence`), and Noul answers is-it-true (returns `noul`, 0 to 1). Pick the type whose answer maps directly onto code — Choice for unordered known options (add an `other` fallback), Score for a describable spectrum, Noul for clean yes/no — and remember Noul 0.5 means ambiguity, not a middle grade, so measure levels with Score instead.
> See [[wiki/05-primitives-overview|Primitives Overview]].

### Q6. When should you use a Choice, and how do you handle low confidence and confused options?

> [!tip]- Answer
> Use a Choice when the answer is one of a fixed set (up to 255 options at a few tokens each — pass the full list, not a shortlist), asking every Choice the code might need in one parallel request and letting `if` statements ignore unneeded answers. Treat low confidence as a reason to ask rather than act (e.g. department confidence below 0.3 → manual triage; second team with probability above 0.25 → notify), and when two options are confused, describe each with a structured `what` / `not_for` / `examples` object instead of a one-line string.
> See [[wiki/06-choice|Choice]].

### Q7. How is a Score computed, and what must you read alongside it before ranking or thresholding?

> [!tip]- Answer
> A Score is the probability-weighted mean of its level numbers — e.g. 0 × 0.0 + 1 × 0.70 + 2 × 0.30 = 1.30 — and it can land between levels, so describe situations per level, not degrees, keep one dimension per Score (2–10 distinctly describable levels), and give rare must-act-on extremes their own level. Because different distributions can yield the same score, always read `probabilities` and `confidence` alongside it; to combine dimensions, normalize each by its top level number and weight in code (reference priority 0.6 × 0.62 + 0.3 × 0.725 + 0.1 × 1.0 ≈ 0.69).
> See [[wiki/07-score|Score]].

### Q8. What does a Noul return, and how should you phrase and bound its questions?

> [!tip]- Answer
> A Noul returns a single number, `noul` from 0 to 1 — the probability the answer is yes, usually thresholded into a boolean — with no separate confidence value (near 1 strong yes, near 0 strong no, near 0.5 ambiguity). Phrase instructions so high probability means "yes" (or state a claim to judge true), pin subtle boundaries with optional `true`/`false` criteria worth A/B testing, and for graded skill questions define "strong" explicitly or switch to a Score with levels.
> See [[wiki/08-noul|Noul]].

### Q9. Where is JSON structure allowed in questions, and how does it help Choice, Score, and Noul?

> [!tip]- Answer
> Every `instructions` field and every Choice option, Score level, and Noul `true`/`false` description accepts string, object, array, or null, because System One models are trained to understand structure — use it for clarity (multi-part questions as labeled keys) or to pass supporting data (schemas, taxonomies, rows) as JSON. Choice options take `what` / `not_for` / `examples` rubric objects (walk deep taxonomies one Choice per level using `probabilities`), Score levels take `{summary, signals}` or `{what, examples}` objects, and Noul criteria take structured `true`/`false` objects with `what` plus `examples`.
> See [[wiki/09-advanced-structure|Advanced structure]].

### Q10. Why does TypeSafe bet on machine-to-machine intelligence, and how does RLCD differ from RLHF and RLVR?

> [!tip]- Answer
> TypeSafe bets large-scale automation will be ~99% machine-to-machine and 1% human, so it targets Machine Native Intelligence — structure, reliability, observability, testability, speed, consistency, low cost — for production systems where code needs a narrow inspectable decision. Pretrained models split three ways: RLHF (human feedback → chatbots, co-invented by TypeSafe cofounder Diogo Almeida, but rewards likability → sycophancy and confident hallucinations), RLVR (verifiable rewards → slower, pricier reasoning models), and TypeSafe's RLCD, which returns decisions plus calibrated probabilities instead of generated text.
> See [[wiki/10-ai-primer|AI primer]].

### Q11. Where does `confidence` come from, and how do you set thresholds for acting on it?

> [!tip]- Answer
> Every Choice and Score answer carries full `probabilities` plus a 0-to-1 `confidence` statistic computed from the distribution's shape (concentrated = confident, spread = uncertain), so you are never locked into TypeSafe's definition; Noul answers carry none. Start with three bands — high → act automatically, medium → confirm/flag/gather info, low → route to human or fall back — then scale thresholds to risk within one system (worked example: 0.5 floor for acting at all, >0.9 plus confirmation for destructive `approve_transfer`, lower bar for read-only `check_balance`), starting conservative and tuning on your own data.
> See [[wiki/11-confidence|Confidence]].

### Q12. What is the System One build recipe, and why does code — not agents — own the workflow?

> [!tip]- Answer
> Build AI-powered software, not agents: keep control flow, deterministic rules, and side effects in code; decompose broad judgments into narrow typed questions over minimal relevant state (one "is this spam?" becomes six atomic Nouls); ask many in parallel in one call; and compose probabilities and confidence in code with weighted sums plus uncertainty routing (e.g. `confidence < 0.8 → human review`). Agents loop and choose their own next step — fine with a human watching, but each loop risks going off the rails — while outputs stay composable because they are structured, parallel, comparable, fast (~100 ms), RLCD-calibrated, and self-consistent.
> See [[wiki/12-how-to-build-with-system-one|How to build with TypeSafe]].

### Q13. What are the five capability categories and the ten decision shapes in the use-case map, and how do you use them?

> [!tip]- Answer
> The five categories are background AI Automation Software (code owns control flow, runnable a million times unwatched), 150 ms real-time apps, 100×-cheaper AI Map Reduce over big data, Universal Verification of other AIs' inputs, and Harness Engineering (routing, retrieval, guardrails at lightspeed) — plus ~19 automation domains from recruiting to gaming. The ten decision shapes (classification, detection, scoring, routing, search, retrieval, ranking, verification, ML feature extraction, structured extraction) tell you which primitive pattern to reach for; the recipe is to open the closest industry, scan its example decisions, and adapt them to your own documents and actions.
> See [[wiki/13-use-case-map|Example use cases]].

### Q14. What are the four documented patterns, and how does Speculative Fan-Out work in the ticket-triage example?

> [!tip]- Answer
> The four patterns are Speculative Fan-Out (cost, speed), Confidence-Gated Routing (reliability, safety), Composite Scoring (cost, reliability, speed), and Intent Routing (cost, speed) — the skill is thinking in discrete atomic decisions composed in code. Speculative Fan-Out puts every possibly-needed question in one parallel call (typically no added latency) and lets code ignore what's irrelevant: the triage example asks category Choice plus speculative `bug_severity`, `has_reproducible_steps`, `refund_requested`, and `frustration` together, then routes in code (e.g. `bug_severity.score > 1.5 and has_reproducible_steps.noul > 0.6` → escalate to engineering; `refund_requested.noul > 0.7` → billing with refund flag; `frustration.score > 1.5` → priority response).
> See [[wiki/14-patterns|Patterns]]. See [[wiki/15-speculative-fan-out|Speculative Fan-Out]].

### Q15. How does Confidence-Gated Routing gate the voice-banking actions, and how does Composite Scoring rank resumes?

> [!tip]- Answer
> The maxim is "the answer tells you what; confidence tells you whether to act": below 0.6 confidence on any intent the voice system routes to a human; low-stakes `check_balance` at ≥0.6 acts automatically, while high-stakes `approve_transfer` needs >0.85 to act and otherwise asks the user to confirm. Composite Scoring breaks one judgment into independent 0–4 Score dimensions, normalizes each to 0–1, and blends with code-owned weights — Senior IC `(0.40·py)+(0.10·lead)+(0.40·arch)+(0.10·general)` vs Engineering Manager `(0.15·py)+(0.40·lead)+(0.20·arch)+(0.25·general)` — so one call feeds multiple rankings and retuning means changing weights, not prompts.
> See [[wiki/16-confidence-gated-routing|Confidence-Gated Routing]]. See [[wiki/17-composite-scoring|Composite Scoring]].

### Q16. How does Intent Routing assign handlers in the customer-service example, and what is the Demos page?

> [!tip]- Answer
> TypeSafe classifies first as the fast, cheap front door — `intent` Choice (order_status / product_question / return_exchange / complaint) plus `complexity` Score — and code routes: `intent.confidence < 0.5` → human; `order_status` → deterministic code with no LLM; product/returns questions → different specialist LLMs; complaints use the complexity axis (`complexity.score > 1` or `complexity.confidence < 0.5` → human, else complaint-resolution LLM). The Demos page itself is intentionally thin — a one-entry index pointing to the Smart Home Assistant Demo with an invitation to suggest more use cases, no code or thresholds of its own.
> See [[wiki/18-intent-routing|Intent Routing]]. See [[wiki/19-demos|Demos]].

### Q17. What does the Smart Home Assistant demo prove about speculative fan-out and LLM pairing, and how do the client SDKs fit in?

> [!tip]- Answer
> The demo evaluates every request ("Turn off all of the lights in the house" needs only category, domain, device type, lights action) against one long speculative question list in a single parallel call — the lights-action question is asked before knowing the request concerns lights — because sequential calls that minimize question count end up slower and more expensive. A Noul detects multi-action requests for an LLM to split into atomic commands, and conversational queries fall back to a freeform LLM, so deterministic paths stay fast and cheap; it runs as a Vite/React app with source on GitHub at release. The client SDKs (Python and JavaScript/TypeScript) provide typed questions/answers with automatic retries under the default retry policy, while any other language calls the HTTP API directly.
> See [[wiki/20-smart-home-demo|Smart Home Assistant Demo]]. See [[wiki/21-client-sdks|Client SDKs]].

### Q18. What is the exact evaluation endpoint contract, and how do you install and drive the agent skill?

> [!tip]- Answer
> POST `https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer <API_KEY>`, sending `state` (string/object/array), `model: "jev-latest"`, and `questions` keyed by caller-chosen labels the model never sees; answers return under the same keys (Choice/Score add `confidence` from the distribution — examples 0.82/0.78 — Noul returns only `noul`), with errors 401/422/429/529 and SDK-automatic exponential-backoff retries on 429/529. The agent skill (question types, patterns, best practices for Claude Code, Codex, and others) installs via the Claude Code plugin, `npx skills add typesafe-ai/skills --skill typesafe-ai`, or a pasted install prompt — one method only — and is driven by naming it ("use the TypeSafe skill" or `/typesafe:typesafe-ai`), keeping questions and thresholds in one reviewable file.
> See [[wiki/22-api-reference|API Reference]]. See [[wiki/23-agent-skill|Agent Skill]].

### Q19 (evaluation). Your team proposes one omnibus Score, "Rate this startup pitch", plus a single "Should we approve this transfer?" Choice at 0.65 confidence, to run unreviewed. What do you recommend and why?

> [!tip]- Answer
> Recommend against both as designed: decompose "rate this startup pitch" into atomic per-factor questions (market size, technical feasibility, differentiation) and recombine with an explicit weighted formula in code so trade-offs stay visible and retunable. For the transfer, 0.65 confidence sits in the medium band for a destructive action — route it to user confirmation or a human (auto-act only above ~0.85–0.9 with a 0.5–0.6 floor for acting at all), and keep the thresholds plus question definitions as constants in one reviewable place.
> See [[wiki/01-documentation-index|Documentation Index — Introduction - TypeSafe AI]]. See [[wiki/11-confidence|Confidence]].
