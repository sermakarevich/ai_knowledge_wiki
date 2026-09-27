> [[index|Wiki]] | [[summary|Summary]]

# Introduction - TypeSafe AI — Digest

## 1. [[wiki/01-documentation-index|Documentation Index — Introduction - TypeSafe AI]]

**In one sentence:** TypeSafe's Jev is a System One model that makes fast, structured decisions software can use directly, exposing three composable primitives (Choice, Score, Noul) evaluated in parallel against the same state instead of generating text to parse.

## Key points

- Large language models (LLMs) produce text for humans to read, so using them for code-consumed judgments means coercing text generation into structured decisions and parsing the results back.
- Jev is TypeSafe's flagship model and the first System One model, built to make fast, structured decisions that software can use directly.
- Jev evaluates typed questions against a state and returns structured results directly with no text generation and no parsing: typed values and probability distributions that code can branch on, sort by, and route with.
- TypeSafe exposes three modular, composable primitives: Choice (choose an option from a list), Score (score the state on a rubric), and Noul (is this statement true?).
- Choice returns choice, probabilities, confidence; Score returns score, probabilities, confidence; Noul returns noul (0–1).
- All three question types can be mixed in a single API call, with every question evaluated in parallel and in isolation against the same state in one go, so adding questions barely changes response time and does not create context-rot.
- System One models work best with atomic, well-scoped questions (a gut-check determination); multi-factor questions should be decomposed into separate questions and combined with logic in code, e.g. market size, technical feasibility, and differentiation instead of "rate this startup pitch".

## 2. [[wiki/02-quick-start|Quick Start]]

**In one sentence:** You can try TypeSafe in the Playground with pasted text and mixed Noul/Choice/Score questions, call it via POST to `https://api.typesafe.ai/v1/systemone` with model `jev-latest`, use the Python SDK (`typesafe-sdk`, Python >= 3.10), or install the TypeSafe agent skill for coding agents.

## Key points

- The Playground path is: open the Playground and log in, paste any text as the state, add a Noul question such as `"Does this message express urgency?"`, then mix Noul, Choice, and Score in one call and see all results at once.
- The sample state used throughout is: "Hi, I've been trying to connect my Stripe account for 3 days and it keeps failing. I'm losing sales. Please help ASAP."
- The HTTP API path is: get an API key from the dashboard, then make a POST request to `https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer <API_KEY>` and `Content-Type: application/json`; full details are in the API Reference.
- The sample request body sends one state plus the `model` field (`jev-latest`) and a `questions` map with a Choice (department: billing/technical/sales), a Score (frustration over three levels), and a Noul (is_urgent).
- The sample response returns `choice: "technical"` with probabilities billing 0.159 / technical 0.84 / sales 0.001 and confidence 0.596; `score: 1.035` with confidence 0.842; `noul: 0.999`; and usage of 312 input tokens and 48 output tokens.
- The Python SDK path is: install with `pip install typesafe-sdk` (or `uv add typesafe-sdk`, requires Python >= 3.10), then call `client.system_one(state=..., questions={...})` with `Choice`, `Score`, `Noul` objects; the client reads `TYPESAFE_API_KEY` from the environment and calls `jev-latest` by default.
- The agent-skill path is: install via the Claude Code plugin (`claude plugin marketplace add typesafe-ai/skills`, then `claude plugin install typesafe@typesafe-ai`) or via `npx skills add typesafe-ai/skills --skill typesafe-ai` for other agents, then tell the coding agent to use the TypeSafe skill while building.

## 3. [[wiki/03-system-one|System One]]

**In one sentence:** System One models (starting with TypeSafe's flagship Jev) make fast, structured decisions for software by evaluating a state and returning typed answers plus probabilities instead of generated text.

## Key points

- System One models are a class of AI models built to make fast, structured decisions that software can use directly: a System One model evaluates a state and returns typed answers and probabilities.
- Jev is TypeSafe's flagship model and the first System One model; like an LLM it understands natural-language input, but it returns typed decisions and probabilities rather than generated text.
- System One models are trained for calibrated decisions — probabilities optimized against outcomes to reflect uncertainty — where calibration is measured across groups of predictions and does not guarantee that an individual answer is correct.
- System One models do not write replies, produce code, or generate explanations of their reasoning; instead the user defines the possible answers through primitives (Choice, Score, Noul).
- Answers include confidence, so code can decide when to act and when to escalate to a person or a reasoning model.
- The refund-request workflow pattern is: build a state with the message, transactions, and policy; ask independent questions together (refund requested, duplicate-charge evidence, policy support); combine answers with deterministic checks in code, then route for action or review.
- System One is called through a client SDK or `POST /v1/systemone` in the HTTP API, where the `model` field selects the model; examples use `jev-latest`, which is also the SDK default.

## 4. [[wiki/04-state|State]]

**In one sentence:** State is the content passed in the `state` field for the model to evaluate — one state per request against one or more independently-evaluated questions — structured as a string, object, or array with the facts kept separate from the judgment questions.

## Key points

- State is the content you ask a System One model to evaluate — a support message, a passage of text, or the current state of an application — passed in the `state` field alongside the questions to answer.
- Each request evaluates one state against one or more questions; all questions see the same state, are evaluated independently, and Choice, Score, and Noul questions can be mixed in one request.
- The simplest state is a plain string such as `"My card was charged twice."`; state can also be a JSON object or array with related context, examples, and other information that helps answer the questions.
- Think of state as the material presented to a panel of experts before asking them to make a judgment; in Python, pass the corresponding string, dictionary, or list directly to `client.system_one(state=...)`.
- Use an object for most requests so each part has a descriptive name and relationships stay clear; a string suits simple single-text use cases.
- The worked object example is one state containing a ticket (duplicate-charge subject plus customer/support messages), an order (id A-104 with two captured $49 charges), and a `refund_policy` string — related information is kept together when the decision requires comparing those parts.
- The state holds the content and supporting facts while questions define the judgments — e.g. keep the refund request and policy in the state, then ask whether the customer requested a refund and whether the policy supports it.

## 5. [[wiki/05-primitives-overview|Primitives Overview]]

**In one sentence:** TypeSafe's three primitives — Choice (which option), Score (which level on a spectrum), Noul (is it true, 0–1) — are question/answer pairs evaluated independently and in parallel against the same state, with answers constrained to the supplied options so code can compose them directly.

## Key points

- Primitives come in pairs: a question defines one judgment for a System One model to make about a state, and its answer is the typed value that comes back, composed in code to make decisions.
- The three types are: Choice (which of these options — returns `choice`, `probabilities`, `confidence`), Score (which level — returns `score`, `legend`, `probabilities`, `confidence`), Noul (is this true — returns `noul`, 0 to 1).
- Every question has an ID (the response key, e.g. `refund_requested`), a `type` (`choice`/`score`/`noul`), `instructions` (the actual question), and `criteria` (options map for Choice, ordered levels for Score, optional yes/no clarification for Noul); question IDs are for code only and are not sent to the model.
- Choice fits unordered known options (ticket routing, document type, language detection, with an `other`/`none of the above` fallback); Score fits a describable spectrum (severity, frustration, skill level); Noul fits clean yes/no where the probability itself is the signal.
- Noul 0.5 means equal yes/no probability, not a medium level — so measure levels with Score (e.g. no experience → deep expertise) and reserve Noul for clearly defined conditions; prefer the type whose answer maps directly onto code (Choice → branches, Score → threshold, Noul → `if`).
- Every question in a request sees the same state and is evaluated independently in parallel, so adding questions barely changes response time and costs only the cheap extra question tokens; answers are constrained to the supplied options/levels, never outside values, and one answer never becomes hidden context for another.
- The shared request token budget is around 32,000 tokens (~150,000 characters of English) for state plus questions; when judgments genuinely depend on each other (fetching more data, building the next state, picking next options) make a second request, otherwise ask everything together and let code ignore unneeded answers (speculative fan-out).

## 6. [[wiki/06-choice|Choice]]

**In one sentence:** A Choice picks one option from a fixed set and returns the selected option plus a full probability distribution and confidence, so code can route, threshold, and fan out on typed values instead of parsing text.

## Key points

- Use a Choice when the answer is one of a fixed set of options (which team handles a ticket, which product category, which programming language); if the answer is a position on a spectrum use a Score, and if it is yes-or-no use a Noul.
- A Choice answer is the selected option in `choice`, a probability for every option in `probabilities` (summing to 1), and a `confidence` value from 0 to 1 computed from how spread the distribution is.
- A Choice accepts up to 255 options at a few tokens each, so pass the full list of teams, categories, or products rather than a shortlist, and add an `other` or `none of the above` option when the list may not cover every input.
- Ask every Choice the code might need in a single request instead of one request per question: questions are evaluated in parallel, adding questions barely changes response time, and the code can ignore answers it does not need (extra questions still cost tokens).
- Speculative questions are cheap and safe: ask follow-ups that only matter conditionally (e.g. `return_reason`, `shipping_issue`), then let ordinary `if` statements use or ignore each answer based on the top-level result.
- Low confidence is a reason to ask rather than act: the reference triage code sends tickets with `department` confidence below 0.3 to manual triage, notifies any second team with probability above 0.25, and asks the customer what they want when `requested_resolution` confidence is below 0.5.
- When two options are confused, describe each with a structured object (`what` it covers, `not_for` what belongs to the neighbor, `examples`) instead of a one-line string; field names are not part of the API and none are reserved.

## 7. [[wiki/07-score|Score]]

**In one sentence:** A Score rates content against ordered descriptive levels and returns a fractional position plus per-level probabilities and confidence, so code can rank, threshold, and combine one-dimension judgments with explicit weights.

## Key points

- Use a Score when the answer is a position on a spectrum describable in steps (bug severity, customer happiness, candidate experience); for unordered fixed options use a Choice, for yes-or-no use a Noul.
- A Score answer is a `score` that can fall between two levels, a `probabilities` map over every level summing to 1, a `legend` mapping level numbers back to descriptions, and a `confidence` from 0 to 1 computed from the spread.
- The score is the probability-weighted mean of the level numbers: the reference bug report scores 0 × 0.0 + 1 × 0.70 + 2 × 0.30 = 1.30 at confidence 0.54, i.e. mostly level 1 with weight on level 2.
- Each level is judged on its own against the state — the model sees descriptions only, never level numbers or neighbors — so describe situations, not degrees ("Broken or degraded feature, but workaround exists", not "Moderately severe").
- Criteria take 2 to 10 levels; use as many as can be described distinctly, keep each Score to one dimension, and give rare must-act-on extremes their own level.
- Different distributions can yield the same score (all mass on level 1 vs. half on 0 and half on 2), so always read `probabilities` and `confidence` alongside the score before rounding or ranking.
- Split complex judgments into one Score per dimension, normalize each by dividing by its top level number `len(criteria) − 1`, and combine with weights in code — the reference priority is 0.6 × 0.62 + 0.3 × 0.725 + 0.1 × 1.0 = 0.6895 ≈ 0.69 (the Composite scoring pattern).

## 8. [[wiki/08-noul|Noul]]

**In one sentence:** A Noul answers a single yes-or-no question with one number — the probability that the answer is yes — which code thresholds into a boolean, with no separate confidence value.

## Key points

- Use a Noul when the answer is yes or no (does the message ask for a refund, does the resume mention distributed systems, does the comment contain personal data); for several options use a Choice, for a spectrum position use a Score.
- A Noul answer is a single number, `noul`, from 0 to 1: the probability that the answer is yes, most often thresholded into a boolean when code needs a hard decision.
- A Noul returns no separate confidence value: near 1 means strong yes, near 0 means strong no, and near 0.5 gives yes and no similar probability.
- Phrase instructions so a high probability means "yes" (or phrase as a statement to evaluate for truthfulness), keeping the returned answer unambiguous in meaning.
- Optional `criteria` with `true` and `false` descriptions pins down subtle yes/no boundaries — e.g. `true`: "Mentions a prior attempt, ticket, or that they have asked before" vs `false`: "No sign of any previous contact" — and is worth A/B testing with and without.
- The reference request sends two Nouls in one call (`is_human_escalation`, `is_repeat_contact`) and gets back 0.99 and 0.93 at a cost of 360 input and 39 output tokens.
- A value of 0.5 is ambiguity, not a middle grade: for "Is the candidate strong in Python?", define what "strong" means, and use a Score with defined levels to measure skill along a scale.

## 9. [[wiki/09-advanced-structure|Advanced structure]]

**In one sentence:** Instructions, Choice options, Score levels, and Noul criteria all accept JSON structure (string, object, array, or null), letting labeled keys, supporting data, and examples carry meaning the model actually uses.

## Key points

- System One models are trained to understand structure: every `instructions` field and every Choice option, Score level, and Noul `true`/`false` description is an `EntryType` accepting `string`, `object`, `array`, or `null`.
- Structure when it helps clarity (multi-part questions read better as labeled JSON keys) or when the question needs supporting data (a schema, taxonomy, or database row can be passed as JSON instead of serialized into a string template).
- One shared `field` object shape can drive all three primitives at once: the invoice example uses the same field-description pattern for a Noul verifying a value, a Choice picking among candidates, and two Scores placing values on scales.
- Choice options accept rubric objects (`what` / `not_for` / `examples`) that sharpen boundaries — e.g. billing vs orders vs account — and whole taxonomy subtrees as values, so the model sees what lives under a branch before committing to it.
- Walking a deep taxonomy means asking one Choice per level with the current node's children as options, using `probabilities` to decide whether to explore both branches, trimming oversized subtrees, and optionally beam-searching the best K paths.
- Score levels accept objects like `{summary, signals}` (PR-focus example) and `{what, examples}` mirroring the Score page's finding that matching examples concentrate probability on one level.
- Noul's optional `criteria` accepts structured `true`/`false` objects (`what` plus `examples` on each side), as in the credential-request check that inspects `message` for a request to send the credential itself rather than reset it.

## 10. [[wiki/10-ai-primer|AI primer]]

**In one sentence:** TypeSafe bets large-scale automation will be ~99% machine-to-machine, so instead of RLHF chatbots it trains decision models with RLCD (reinforcement learning for calibrated decisions) that return decisions plus calibrated probabilities rather than generated text.

## Key points

- Most AI products are built around model-to-person conversation, but TypeSafe bets large-scale automation will be closer to 99% machine-to-machine and 1% human interaction, so the machine interface matters more than the chat interface.
- Machine Native Intelligence means AI with software-like properties: structure, reliability, observability, testability, speed, consistency, and low cost.
- TypeSafe is not trying to build a model that does everything; it targets production systems where code needs a narrow decision it can inspect and act on.
- Pretrained language models branch into three post-training paths: RLHF (human feedback → chatbots), RLVR (verifiable rewards → reasoning models, strong at math but slower and more expensive), and TypeSafe's RLCD (calibrated decisions instead of generated text).
- RLHF was used to train InstructGPT and ChatGPT and was co-invented by Diogo Almeida, cofounder of TypeSafe.
- RLCD's output contract: the model does not generate text, it returns decisions and probabilities, and higher probability should correspond to a greater chance the answer is correct.
- Calibration is a group rate, not a per-answer guarantee: outcomes assigned 0.2 should occur ~20% of the time, 0.8 ~80%, and 1.0 100% of the time across many predictions (see Confidence for act-vs-escalate guidance).
- RLHF rewards what people prefer, which can produce sycophancy and confident-sounding hallucinations plus mode dropping (a milder version of GAN-style mode collapse where the generator repeats one fooling output), so human preference and machine trustworthiness are different optimization targets.

## 11. [[wiki/11-confidence|Confidence]]

**In one sentence:** Every Choice and Score answer carries a full probability distribution plus a 0-to-1 confidence number derived from its shape, and code should gate actions on confidence with risk-scaled thresholds (e.g. a 0.5 floor for acting at all and 0.9 for destructive operations).

## Key points

- All Score and Choice answers include a `probabilities` property: the distribution across options (Choice) or levels (Score), and its shape is the certainty signal — concentrated means confident, spread out means uncertain.
- The answer's `confidence` property collapses that shape into a single number from 0 to 1 for thresholding without doing the math; Noul answers don't carry one.
- `confidence` is a statistic computed from the probability distribution the answer already gives you, returned on every Choice and Score answer so the common case needs no extra work.
- The full `probabilities` are always returned, so you are never locked into TypeSafe's confidence definition and can use a different measure for your evaluation.
- Low confidence on a Choice often means no option is a clear winner; low confidence on a Score often means the levels are ambiguous or multi-dimensional, or the state lacks enough to go on.
- The three-range starting pattern is: high confidence → act automatically, medium → proceed with caution (confirm, flag, gather more info), low → do not act (route to a human, clarify, fall back).
- Thresholds scale with risk within one system: the worked example uses a 0.5 confidence floor below which anything routes to a human, while `approve_transfer` needs > 0.9 plus confirmation but read-only `check_balance` proceeds below that.
- Threshold values depend on your domain and model performance — start conservative, test with your own data, and adjust as you observe results.

## 12. [[wiki/12-how-to-build-with-system-one|How to build with TypeSafe]]

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

## 13. [[wiki/13-use-case-map|Example use cases]]

**In one sentence:** The map groups TypeSafe fits into five capability categories (background automation, 150 ms real-time, 100×-cheaper big-data map-reduce, universal verification of other AIs, harness engineering) plus ~19 automation domains and a 10-row decision-shape table for turning ideas into code-owned workflows.

## Key points

- AI Automation Software means interleaving AI with reliable software runnable a million times in the background with no human co-pilot — code owns control flow (not markdown files) while TypeSafe handles semantic decisions and language understanding.
- Real-time applications use frontier intelligence at ~150 ms (faster than human perception) for games or UI-embedded decisions.
- AI Map Reduce over Big Data exploits ~100× cheaper inference to search, classify, and extract features over giant corpuses, agent traces, and datasets.
- Universal Verification checks prompts, extractions, reasoning traces, tool calls, or any other AI's inputs at a fraction of the LLM call cost — jailbreaks, citation errors, hallucinations, and other error modes.
- Harness Engineering uses Jev queries for model routing, semantic context retrieval, LLM error detection, guardrails, and reasoning-trace classification at lightspeed and a fraction of the cost.
- The automation list spans search/retrieval, scientific discovery, model routing, guardrails, semantic code linting, feature extraction, recruiting, lead gen, support, insurance, financial crime, legal/compliance, marketplaces, moderation, advertising, gaming, risk, forecasting, and knowledge graphs.
- The decision-shape table maps ten shapes (classification, detection, scoring, routing, search, retrieval, ranking, verification, ML feature extraction, structured extraction) to when to reach for each, e.g. routing when a category selects the next code path.
- Usage recipe: open the closest industry, scan the example decisions, and adapt them to the documents and actions in your own workflow.

## 14. [[wiki/14-patterns|Patterns]]

**In one sentence:** TypeSafe is designed to sit inside a larger system powering decisions with AI, and getting the most out of it means thinking in discrete atomic decisions composed in code, using four documented patterns that trade off cost, speed, reliability, and safety.

## Key points

- TypeSafe powers decisions with AI from within a larger system; the key skill is thinking in discrete, atomic decisions that compose into complex system behavior.
- The patterns section assumes knowledge of the TypeSafe primitives and how confidence works, and says to read those first if not.
- Speculative Fan-Out sends many questions in a single call, including speculative ones, and lets code decide what's relevant; benefits are cost and speed.
- Confidence-Gated Routing uses confidence as a second decision axis to build safer systems; benefits are reliability and safety.
- Composite Scoring combines several dimensions of analysis into a single score; benefits are cost, reliability, and speed.
- Intent Routing classifies a user's intent and routes to the appropriate handler; benefits are cost and speed.
- The page invites readers to share killer use cases they think should be mentioned.

## 15. [[wiki/15-speculative-fan-out|Speculative Fan-Out]]

**In one sentence:** Because TypeSafe evaluates many questions in a single API call in parallel with typically no added latency, put every question the system might need — including speculative ones — into one request and let code ignore what's irrelevant after the fact.

## Key points

- All questions in one call are evaluated in parallel, so adding more questions to a call typically doesn't add any latency to the response.
- The recommendation is explicit: put all of the questions the system needs in a single request, then use code to decide what is relevant after the fact.
- Speculative questions are ones asked before knowing whether they're relevant — e.g. `bug_severity` and `has_reproducible_steps` only matter if the ticket is a bug report, `refund_requested` only matters for billing — included upfront because there is no speed cost.
- The triage example classifies a ticket's category (Choice: bug_report / billing / feature_request / account) while speculatively scoring bug severity, checking for reproducible steps (Noul), checking refund requests (Noul), and scoring frustration (Score).
- Routing thresholds from the example code: escalate to engineering when `bug_severity.score > 1.5 and has_reproducible_steps.noul > 0.6`; route billing with a refund flag when `refund_requested.noul > 0.7`; flag for priority response when `frustration.score > 1.5`.
- If the ticket turns out to be a feature request, the bug-severity result is simply ignored by the code path — speculative questions save a round trip when relevant and cost nothing when not.
- Everything needed for the full decision tree comes from one call instead of chaining a category call followed by a severity follow-up call.

## 16. [[wiki/16-confidence-gated-routing|Confidence-Gated Routing]]

**In one sentence:** Use confidence as a second axis alongside the answer — the answer tells you what, confidence tells you whether to act — gating each action at a threshold scaled to its risk.

## Key points

- Confidence is described as one of TypeSafe's most powerful features, and being intentional about gating decisions on it builds systems that are both reliable and safe.
- The core maxim is: "The answer tells you what; confidence tells you whether to act."
- The voice-banking example classifies intent with a Choice over `check_balance` (check an account balance), `approve_transfer` (approve a pending transfer), and `other`.
- A 0.6 confidence floor catches anything genuinely uncertain: below 0.6 on any action, the system routes to a human support agent.
- Low-stakes `check_balance` at or above 0.6 proceeds automatically (`show_balance`), because the worst case is the user hearing a balance read-out.
- High-stakes `approve_transfer` needs confidence above 0.85 to act automatically; at moderate confidence (0.6–0.85) the system asks the user to confirm ("Just to confirm: you would like to approve this transfer, is that correct?").
- The page defers to the Confidence page for more on how to think about confidence in systems.

## 17. [[wiki/17-composite-scoring|Composite Scoring]]

**In one sentence:** To rank items on several criteria at once, break the judgment into independent Score dimensions, normalize each to 0–1, and combine them with weights controlled in code so priorities can shift without rewriting prompts.

## Key points

- The method is: break the judgment into independent dimensions, score each one separately, and combine them with weights controlled in code.
- The resume-screening example scores four dimensions, each a 0–4 Score over five rubric levels: `python_depth`, `team_leadership`, `system_design`, and `generalist` (evidence of picking up unfamiliar tools, roles, or domains).
- Each dimension is normalized to 0–1 by dividing its score by 4, and weights adjust relative importance without losing the nuance of individual scores.
- The Senior IC composite is `(0.40 * py) + (0.10 * lead) + (0.40 * arch) + (0.10 * general)` — Python depth and system design dominate.
- The Engineering Manager composite is `(0.15 * py) + (0.40 * lead) + (0.20 * arch) + (0.25 * general)` — leadership dominates with generalist second.
- Beyond ranking, the formula gives visibility into exactly how the final score is calculated: if top-ranked candidates don't match expectations, adjust the weights to find the right balance.
- The same per-dimension scores serve multiple rankings — one API call feeds both the IC and EM formulas.

## 18. [[wiki/18-intent-routing|Intent Routing]]

**In one sentence:** TypeSafe sits in front of all handlers as a fast, cheap classifier — one quick call determines intent and complexity, then code routes each request to deterministic logic, a specialist LLM, or a human, so expensive resources run only where needed.

## Key points

- Not every request needs the same handler: some need a database lookup, some an LLM with domain-specific context, some a human — TypeSafe classifies first as the fast, cheap front door.
- The customer-service example classifies two things at once: `intent` (Choice over order_status / product_question / return_exchange / complaint) and `complexity` (Score: simple lookup / needs judgment or multi-step / unusual, edge case, or escalation).
- If `intent.confidence < 0.5`, the ticket routes to a human agent because classification itself is too uncertain.
- `order_status` routes to deterministic code with no LLM involved; `product_question` and `return_exchange` each route to a different specialist LLM loaded with different context.
- `complaint` uses the complexity score as a second axis: `complexity.score > 1` (leaning toward "escalation needed") or `complexity.confidence < 0.5` routes to a human, otherwise a complaint-resolution LLM handles it.
- The page adds an explicit confidence check on the complexity score itself, noting it is always important to consider what a low confidence score means given the system and the stakes.
- TypeSafe handles the classification all in a single quick call; the expensive handlers only get invoked for the requests that actually need them.

## 19. [[wiki/19-demos|Demos]]

**In one sentence:** The Demos page is a thin index of interactive examples showing what's possible with TypeSafe, currently listing a single Smart Home Assistant demo that evaluates user requests with speculative questions and LLM fallback.

## Key points

- The page's stated purpose is to collect interactive examples showing what's possible with TypeSafe.
- It lists exactly one available demo: the Smart Home Assistant Demo, which evaluates user smart home requests with speculative questions and LLM fallback.
- The demo entry links to the Smart Home demo detail page for the full walkthrough.
- The page carries an invitation tip: readers with a killer use case they think should be mentioned should drop a note.
- This page is intentionally thin — it is an index, not a walkthrough; for the substantive content (speculative fan-out in action, TypeSafe-plus-LLM pairing, run-it-yourself instructions), see the richer neighbour page on the Smart Home Assistant demo (wiki page 20).
- No code, thresholds, or API details live on this page; all mechanisms are documented on the demo detail page it points to.

## 20. [[wiki/20-smart-home-demo|Smart Home Assistant Demo]]

**In one sentence:** The smart home demo evaluates every user request against a long list of questions — many speculative — in one parallel call and pairs TypeSafe with an LLM that splits compound requests and handles conversational fallback, so deterministic commands stay fast and cheap while open-ended chat still works.

## Key points

- The chief pattern demonstrated is speculative fan-out: each user request is evaluated against a long list of questions, including many that end up irrelevant for most requests.
- The worked request is "Turn off all of the lights in the house", for which code only needs four answers: request category (smarthome command), domain (whole house), device type (lights), and action on the lights (turn off).
- The lights-action question is speculative — written assuming a lights command and asked before knowing the request is one — so all questions evaluate in parallel and code filters out irrelevant results after the fact, handling a wide variety of requests with a single question set.
- The wrong way is sequential API calls (ask category, then domain/device only once it's known to be a smarthome command, then action only once lights are known): it minimizes question count but ends up much slower and more expensive than one upfront batched call.
- A Noul question detects whether the request asks for more than one distinct action; if true, an LLM splits it into atomic commands that TypeSafe evaluates individually.
- When TypeSafe determines the query is general information or conversation, the system falls back to a conversational LLM for a freeform response — deterministic behavior stays fast and cost-efficient while the LLM adds flexibility, and the initial TypeSafe response is so fast it adds negligible latency.
- The demo is a Vite/React single-page app using the TypeSafe API; full source will be available on GitHub at release, with local run instructions and a code-to-demo-part overview in its README.
- A demo video is embedded on the page ("Check it out in action").

## 21. [[wiki/21-client-sdks|Client SDKs]]

**In one sentence:** Install a TypeSafe client SDK to use typed questions and answers with automatic retries under the default retry policy — Python and JavaScript/TypeScript flavors — or call the HTTP API directly from any language.

## Key points

- The page's stated purpose is: install a TypeSafe client SDK and use typed questions and answers in the application.
- Client SDKs provide typed questions and answers for the TypeSafe API and handle retries automatically with their default retry policy.
- The Python card points to installation instructions, examples, and API details for installing the Python client SDK and making a first request.
- The JavaScript/TypeScript card points to installation instructions, examples, and API details for installing the JavaScript client SDK and making a first typed request.
- Any other language can call the HTTP API directly instead of using an SDK.
- This page is intentionally thin — it is a chooser between two SDK tracks plus the direct-API escape hatch; for the endpoint, request/response shapes, and error codes, see the richer neighbour API Reference (wiki page 22).

## 22. [[wiki/22-api-reference|API Reference]]

**In one sentence:** POST a `state` plus a caller-named map of typed `questions` to `https://api.typesafe.ai/v1/systemone` with model `jev-latest`, and get back structured `answers` keyed by the same ids plus token `usage`, with standard HTTP error codes and SDK-automatic retries on rate limits.

## Key points

- The evaluation endpoint is `POST https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer <API_KEY>` and `Content-Type: application/json`; for a guided introduction the page defers to the primitives docs.
- Every request sends three required top-level fields: `state` (string, object, or array — text, chat logs, records, or app state), `model` (`"jev-latest"`, the flagship model), and `questions` (a map of typed Question objects under caller-chosen keys, with answers returned under the same keys).
- Question keys are not sent to the underlying model and are not used in inference — they are pure caller-side labels.
- The three question types share `type` and `instructions` and differ in `criteria`: Noul takes optional true/false meaning descriptions; Choice requires a map of option to rubric description (null allowed); Score requires an ordered array of at least two level descriptions and returns a probability-weighted value that can land between levels.
- Every answer carries the question's `type`; Choice answers return `choice` plus `probabilities` summing to 1 plus `confidence`; Score answers return `score` plus `legend` plus per-level `probabilities` plus `confidence`; Noul answers return `noul` on a 0–1 scale with no confidence field.
- Choice and Score `confidence` (0 to 1) is derived from the answer's probability distribution; the worked examples show choice confidence 0.82 and score confidence 0.78.
- Errors use standard HTTP codes with a JSON body: 401 for missing/invalid API key, 422 for body validation failures (missing field or malformed question, body names the field), 429 for rate limits, 529 for temporary overload.
- On 429 or 529, retry with exponential backoff rather than immediately; client SDKs handle this automatically under the default retry policy, so SDK users need no extra handling.

## 23. [[wiki/23-agent-skill|Agent Skill]]

**In one sentence:** The TypeSafe agent skill is a drop-in package for Claude Code, Codex, and other agent environments that gives a coding agent full TypeSafe API context — question types, patterns, best practices — installed via plugin, skills CLI, or a pasted prompt, and driven by naming the skill in prompts.

## Key points

- The skill gives an AI coding agent full context on the TypeSafe API: the three question types, the architectural patterns, and best practices for structuring evaluations.
- Three installation paths are documented: the Claude Code plugin (two terminal commands), the skills CLI for other agents (`npx skills add typesafe-ai/skills --skill typesafe-ai`, project-local by default, `-g` for global), and pasting an install prompt into the agent that reads SKILL.md from GitHub.
- Manual installation means copying the entire skills/typesafe-ai directory, including reference files, into the agent's skills directory; only one installation method should be used to avoid duplicate copies.
- Updates run through the same channel: plugin marketplace/plugin update commands plus `/reload-plugins` or auto-update for Claude Code, `npx skills update` for skills.sh installs, or replacing the whole directory for manual copies.
- Three example prompts are given — brainstorming where TypeSafe fits ("explore the project and find opportunities for using intelligent judgement to stand in for complex parsing"), running cheap API experiments with an exported `TYPESAFE_API_KEY`, and checking applicable cookbooks — where naming the skill ("use the TypeSafe skill") works in any agent and the Claude Code plugin also accepts `/typesafe:typesafe-ai`.
- Four good-vibe-coding principles apply: talk it out from the example prompts, review the plan before implementing, keep questions and thresholds as constants in a single reviewable place (agents write poor questions, so edit collaboratively), and don't take assertions at face value — have the agent validate assumptions.
- Five common issues are diagnosed: agent not using the skill (invoke `/typesafe:typesafe-ai` or "use the TypeSafe skill", confirm installer target, restart), routing surprises (check questions and thresholds for false negatives/positives or vague questions), overusing confidence thresholds (highest confidence wins when only the best option matters; probabilities when a statistical algorithm is in mind), review difficulty (questions plus thresholds in one file), and invented request/response fields (stale skill — update and retry).

## The argument in five moves

1. Software needs judgments that code can consume, but large language models (LLMs — AI models trained to predict text) only produce text for humans to read, so forcing them into structured decisions means generating text and parsing it back (01).
2. TypeSafe's answer is Jev, the first System One model: a fast, calibrated decision model trained with RLCD (reinforcement learning for calibrated decisions) that evaluates a state and returns typed decisions plus probabilities instead of text — reached via Playground, HTTP API, SDK, or agent skill (02, 03, 10, 21, 22, 23).
3. Every judgment is expressed through three composable primitives evaluated independently and in parallel against one shared state: Choice picks from a fixed set with probabilities and confidence, Score rates against ordered levels with a fractional probability-weighted value, and Noul returns a single 0–1 yes-probability with no separate confidence — with JSON structure allowed anywhere clarity demands it (04, 05, 06, 07, 08, 09).
4. Reliability comes from keeping questions atomic and gating on uncertainty: every Choice/Score answer carries a distribution-derived confidence number, code acts automatically when confident, confirms or escalates when not, and scales thresholds to the stakes of each action (11, 12).
5. Complex behavior is composed in code, not prompts: speculative fan-out asks everything possibly relevant in one parallel call, confidence-gated routing uses confidence as a second axis, composite scoring blends normalized per-dimension Scores with explicit weights, and intent routing fronts cheap classification before expensive handlers — one set of moves that covers background automation, real-time, big-data map-reduce, verification, and harness use cases, as the smart-home demo shows in action (13, 14, 15, 16, 17, 18, 19, 20).
6. The payoff is control: weighting, thresholds, and priorities live in reviewable code constants and formulas, so shifting behavior means changing a coefficient or a weight rather than rewriting a prompt (12, 17).
