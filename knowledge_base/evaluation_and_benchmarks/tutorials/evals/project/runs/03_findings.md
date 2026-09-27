# 03 — Look at your data: findings

The 80 `answer_v1` traces had no human looking at them. This note records what we
found when we opened them, coded the failures, and built the label set chapters 05
and 07 will align against.

## How the labels were made (read this first)

A domain expert would have read all 80 tickets and labelled each by hand. We did
not have one. Instead we used a **reference-aware grader**: the LLM was given the
ticket, the gold answer points, the gold handbook section texts and the app's
reply (none of which the app itself sees), plus a rubric
(`prompts/reference_grader_v1.txt`). It returned `pass`, the specific missing
facts, the unsupported claims, a tone/promise flag, a did-not-answer flag, and a
one-sentence open-coding note. Then **axial coding**: I read the 30 failing
notes, clustered them into 6 failure modes (below), and mapped each failing
trace to ≥1 mode. Finally a **manual review** of a seeded 12-trace sample
(6 pass / 6 fail).

This is a stand-in for human labelling. The grader can only check against the
reference standard we handed it; it cannot judge whether the customer felt
resolved, whether the tone was human, or whether a "correct" answer was actually
unhelpful. Where those matter, the labels are optimistic. Chapters 06 discusses
how to replace this with real annotators and agreement measurement.

## Pass rates

| run | pass | fail | pass rate |
|---|---|---|---|
| answer_v1 | 50 | 30 | **62.5 %** |
| triage_v1 | 24 | 56 | **30.0 %** |

Triage is graded by pure code (compare `category`, `priority`,
`needs_escalation` with gold). The app is far worse at classifying a ticket than
at answering one.

## Failure taxonomy (axial coding)

Six modes, stable snake_case ids, written to `data/labels/taxonomy.yaml`.

| mode | count | definition | one real example |
|---|---|---|---|
| `missing_required_fact` | 18 | The handbook covers it; the reply omits a fact the reference standard requires | tkt-013 — reply omits the $25.00 expedited cost and the $150.00 free-shipping threshold |
| `unsupported_claim` | 13 | The reply asserts policy the retrieved sections do not state — an invention | tkt-001 — claims the handbook gives no self-verify/override mechanism |
| `wrong_section_retrieved` | 8 | Retrieval never surfaced the covering section; the model answered without it | tkt-010 — privacy section never retrieved; 90-day audit fact absent |
| `did_not_answer` | 6 | Redirect to callback/refusal; the customer's actual ask is ignored | tkt-011 — refuses to act, offers only a callback |
| `wrong_value` | 2 | The reply states a concrete figure that contradicts the reference standard | tkt-040 — gives a $10.00 refer-a-friend discount; gold is $20.00 |
| `over_promise` | 1 | Promises an exception (refund, fee, mechanism) the handbook never grants | tkt-068 — invents a 15 % restocking fee |

## Per-topic (answer_v1)

| topic | pass/total | rate |
|---|---|---|
| accounts | 7/7 | 100 % |
| returns | 6/7 | 86 % |
| payments | 6/7 | 86 % |
| discounts | 5/7 | 71 % |
| damaged_items | 4/6 | 67 % |
| warranty | 4/7 | 57 % |
| gift_cards | 4/7 | 57 % |
| order_changes | 4/7 | 57 % |
| privacy | 3/6 | 50 % |
| loyalty | 3/6 | 50 % |
| shipping | 3/7 | 43 % |
| **international** | **1/6** | **17 %** |

## Per-scenario (answer_v1)

| scenario | pass/total | rate |
|---|---|---|
| simple_question | 21/23 | 91 % |
| problem_report | 14/22 | 64 % |
| out_of_policy_request | 9/18 | 50 % |
| **urgent_blocker** | **6/17** | **35 %** |

## Per-scenario (triage_v1)

| scenario | pass/total | rate |
|---|---|---|
| simple_question | 10/23 | 43 % |
| problem_report | 7/22 | 32 % |
| urgent_blocker | 4/17 | 24 % |
| **out_of_policy_request** | **3/18** | **17 %** |

## Observations

1. **`urgent_blocker` is the weakest scenario** (35 % answer, 24 % triage).
   These are the tickets a stressed customer who is about to escalate; the app
   fails exactly where it costs the most. `out_of_policy_request` is the worst
   **triage** scenario — the app can't even classify a request that should be
   refused.
2. **`international` is the weakest answer topic** (17 %). The handbook's
   international section is thin; the model leans on `unsupported_claim` and
   `missing_required_fact` to fill the gap.
3. **Retrieval is a real but minority contributor.** Of the 30 failing answer
   traces, the gold section was *not retrieved* in a small minority of cases
   (`wrong_section_retrieved` = 8, and 3 fully un-retrieved). The bulk of
   failures are generation-side: the right section was in front of the model and
   it still dropped a fact or invented one. Fixing generation (fewer omissions,
   no inventions) will move the score more than a better retriever.
4. **`missing_required_fact` + `unsupported_claim` = 31 of 30-fails (31 counts
   since modes overlap).** The two most common sins are the opposite pair: too
   little and made-up. Both point at the same fix — a rubric that forces the
   model to answer only from retrieved text and to flag when it can't.
5. **Triage and answer failure are correlated but distinct.** Triage fails on
   `wrong_priority` (40) and `wrong_escalation` (23) far more than on category
   (22): the app knows what a ticket is about but misjudges how urgent and how
   hand-off-able it is. This is a labelling/rubric problem in the triage
   prompt, not a retrieval one.

## Manual review

Seeded 12-trace sample (6 pass, 6 fail), read with `viewer show`.
**n agree / disagree = 12 / 0** — no label flipped. See
`data/labels/review_answer_v1.md`.

Two non-flips worth flagging:

- **tkt-068 (fail)**: the reply *does* state the correct 30-day return window
  (the reference-standard fact) but invents a 15 % restocking fee. Fail is
  correct on the fabrication; the `over_promise` mode is catching something the
  binary fact check alone would not.
- **tkt-059 (pass)**: the customer is in a rush and rejects the callback path;
  the reply is deflected in a way a human would dislike. Both gold facts are
  present, so it scores pass. The rubric is fact-grounded, not tone-grounded —
  a documented optimist bias in these labels.

## Resource use

- LLM calls for answer grading: **80** (all via `Ollama.chat_json`, disk-cached;
  total stays well under the ≤100 budget). Triage is code-only.
- Total wall time for the two `labels grade` passes: **~5 min** (mixed
  cache-hit + live 27b calls).
- No new SUT changes; the `v1` traces are unchanged.
