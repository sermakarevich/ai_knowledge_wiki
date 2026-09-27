> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Motivation: Chart-24 Example Shows Why Repair Needs Runtime State
**In one sentence:** The Defects4J Chart-24 bug shows that feeding an LLM only buggy code plus the outcome-level crash symptom yields a plausible-but-wrong patch that clamps `g`, while observing runtime intermediates (value = -0.5, v = 0.0, g = -127) exposes that `g` was computed from the raw input instead of the clamped `v`.
## Key points
- The motivating example is the Defects4J Chart-24 bug in function `getPaint`, which should return a `Color` based on variable `v` clamped between `lowerBound` and `upperBound` derived from input `Value`.
- The root cause is that the parameter `g` for constructing the `Color` object erroneously uses the raw input value instead of the restricted variable `v`, crashing with `java.lang.IllegalArgumentException`.
- Existing LLM-based APR tools are fed the buggy code plus outcome-level failure symptoms, which only confirm an invalid color parameter while concealing intermediate states.
- From symptoms alone the LLM concludes `g` is simply outside the valid range and generates a plausible but incorrect patch that explicitly clamps `g` before the `Color` constructor (Line 5).
- That incorrect patch merely masks the symptom instead of fixing the mistaken variable reference of `Value` in Line 4.
- A human-style debugging trace (inserted print statements) shows `value` is -0.5, `v` is evaluated as 0.0, and `g` is calculated as -127.
- The conflict — `v` correctly clamped to the legal lower bound 0.0 while `g` is an illegal -127 — reveals `g` was computed from the raw negative value (-0.5) rather than the restricted `v`, enabling the correct patch.
- The chunk's thesis is that runtime intermediate states are the critical bridge between symptom and root cause, so the LLM should proactively insert print statements and analyze debugging output rather than passively consuming outcome-level symptoms.
---
## The limitation of outcome-level failure symptoms
Figure 1(a) shows buggy `getPaint`: `v` is clamped between `lowerBound` and `upperBound` from input `Value`, but `g` for the `Color` constructor uses the raw input value instead of `v`, causing the `java.lang.IllegalArgumentException` crash. Figure 1(b) shows the existing LLM-based APR setup fed with buggy code plus that outcome-level symptom; the symptom confirms the manifestation (an invalid color parameter) while concealing intermediate states, so the LLM hypothesizes `g` just needs a proper bound and emits the incorrect patch — explicitly clamping `g` before the `Color` constructor (Line 5) — which masks the symptom rather than fixing the mistaken `Value` reference in Line 4.

## The necessity of debugging
Figure 1(c) shows the human-developer alternative: insert print statements to visualize the intermediate execution trace, yielding `value` = -0.5, `v` = 0.0, `g` = -127. Inspecting these values makes the root cause transparent: `v` is correctly clamped to the legal lower bound (0.0) yet `g` still yields the illegal negative value (-127), proving `g` is computed from the raw negative value (-0.5) rather than the properly restricted `v`. Verbatim thesis:

> "This example demonstrates that runtime intermediate states act as a critical bridge between the symptom and the root cause."
> "By enabling the LLM to proactively insert print statements and analyze the resulting debugging output, rather than passively consuming outcome-level failure symptoms, we can empower the model to precisely resolve the underlying logic errors."

**Covers:** chunk 03-2-motivation-in-this-section-we (plan: motivating Chart-24 bug example — symptom-only repair failure vs runtime-state debugging; Section 2 Motivation)
