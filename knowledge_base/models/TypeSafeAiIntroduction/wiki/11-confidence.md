> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Confidence

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

---

## Confidence is derived from the probabilities

`confidence` is a statistic computed from the probability distribution the answer already gives you. TypeSafe computes it for you and returns it on every Choice and Score answer, so the common case needs no extra work on your side.

Verbatim default guidance:

> "**A solid default:** We provide `confidence` as a convenient measure that fits most use-cases, but you are never locked into our definition. Depending on what you are evaluating, a different measure may serve you better, which is exactly why we give you the full `probabilities` in the response."

For a Choice the distribution is `probabilities` across your options; for a Score it is the distribution across your levels. In both cases a flatter distribution means lower confidence.

## "I don't know" is a useful signal

> "If an intelligent system, whether human or machine, cannot express honest uncertainty, the system cannot be trusted."

Confidence is the built-in mechanism for the model to say "I'm not sure about this one," letting code implement different behavior per certainty level — the foundation for systems you can actually rely on.

## Three paths for using confidence in your code

Divide confidence into three ranges, each producing different system behavior:

- **High confidence:** Act automatically — the model has a clear read, proceed without human involvement.
- **Medium confidence:** Proceed with caution — reasonable answer but uncertain; ask the user to confirm, flag for review, or gather more information.
- **Low confidence:** Do not act — route to a human, request clarification, or fall back to a different system; the model lacks information or the question is a bad fit.

Where the boundaries sit depends on the stakes.

## Thresholds scale with risk

A confidence threshold is not one number: different actions in the same system are gated at different levels based on the consequences of being wrong. Worked pattern (Choice over `check_balance` / `approve_transfer` / `support`):

- `confidence < 0.5` → model is genuinely unsure, don't guess, `route_to_human`.
- `check_balance` (low stakes, recoverable wrong screen) → `show_balance` without extra confirmation.
- `approve_transfer` with `confidence > 0.9` → `confirm_then_execute`; same action at moderate confidence → `ask_user_to_confirm`.

> "The 0.5 confidence floor catches anything the model reports as genuinely uncertain. Above that, the threshold for acting without confirmation is higher for a destructive operation than for a read-only one. Your code encodes the risk tolerance."

> "The correct threshold values depend on your domain and the performance of the model for your use case. Start with conservative thresholds, test with your own data, and adjust as you observe results."

**Covers:** Confidence — how TypeSafe reports certainty and how to use it architecturally (source/topics/confidence.md)
