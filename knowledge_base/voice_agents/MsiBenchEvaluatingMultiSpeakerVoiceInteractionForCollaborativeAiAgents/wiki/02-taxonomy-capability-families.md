[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Taxonomy and capability families
**In one sentence:** MSI-Bench evaluates speaker-scoped decision making in shared multi-speaker voice conversations across three capability families — multi-speaker memory, instruction following, and reasoning — using 1,152 bilingual audio scenes with atomic rubrics, where even the strongest systems pass all rubrics on only 66.8% of English and 54.5% of Mandarin cases.
## Key points
- MSI-Bench comprises 1,152 test cases, evenly split between Mandarin Chinese and English (576 each), each a short multi-party multi-turn audio scene with participant context, expected tool calls, and atomic rubrics.
- The benchmark targets three capability families — multi-speaker memory, multi-speaker instruction following, and multi-speaker reasoning — with two test-case patterns each (six patterns total).
- The strongest configuration on each split passes all rubrics on only 66.8% of English and 54.5% of Mandarin cases; the strongest open-weight configuration passes 34.0% and 19.3%.
- Failure analysis separates perception from reasoning: open-weight models are bottlenecked by the multi-speaker audio front-end, while frontier systems still fail speaker-scoped decision making on clean transcripts.
- Models across the board often respond when no one has addressed them, identifying conversational restraint alongside speaker-grounded perception and speaker-scoped decision making as targets.
- The paper claims three contributions: the interaction taxonomy, the MSI-Bench structure with normalized outputs and atomic rubrics, and a data-generation pipeline used to build the benchmark and evaluate 12 models under 15 configurations.
---
## Outcome and motivation
**Covers:** Abstract / Section 1 (Introduction), arXiv:2609.24812v1 [cs.CL] 21 Sep 2026

Voice agents must determine both whether they are being addressed and how speakers' identities and roles constrain the next action, since outcome "depends jointly on who provided a piece of information, to whom it applies, who has authority to modify it, what may be disclosed to whom, and which of several speakers' constraints should take priority."

> "Minutes later, the daughter asks what the arriving package is. An agent that answers her fluently has failed: it preserved neither the instruction's speaker, nor the person it protects, nor the boundary on what may be disclosed."

Prior voice assistants assume a one-to-one model where "utterances are directed to the assistant and that instructions, preferences, and permissions belong to the same person," which breaks in shared settings such as meetings, households, collaborative work, Slack channels (Claude Tag), and Teams channels/meetings (Microsoft 365 Copilot).

## Related work contrast
**Covers:** Section 2 (Related Work)

- Full-duplex and turn-taking benchmarks (FDB v1/v1.5/v2/v3, MTR-DuplexBench, HumDial-FDBench, Speak or Stay Silent, Instruct-FD, Omni-DuplexEval, SocialOmni) primarily evaluate when and how an assistant manages the conversational floor; MSI-Bench instead evaluates what it should say or do given the speaker-dependent state of a shared conversation.
- Multi-speaker attribution benchmarks (TPI-Bench, WearVox, MSU-Bench, M3-SLU) test speaker-attributed understanding or question answering; MSI-Bench tests whether a voice agent can use speaker attribution to select the correct next-assistant behavior — "an answer, refusal, clarification, or tool call."
- Multi-turn voice evaluation protocols use either a live model-based examiner/user simulator (FDB v2, EVA-Bench, τ-Voice) or fixed interaction traces (FDB v3, Audio MultiChallenge, IHBench); MSI-Bench uses scripted, prerecorded multi-speaker audio, "avoiding the variability of a live simulator and enabling reproducible comparisons across full-duplex and turn-based models."

## MSI-Bench structure and capability taxonomy
**Covers:** Section 3–3.1 (partial; taxonomy definitions cut off mid-pattern)

Each test case stages "a short multi-party, multi-turn audio scene with participant context, ending in an assistant-directed request," and the model "must produce an answer with optional tool calls" evaluated with atomic rubrics testing "whether the action is grounded to the correct speaker, scope, authority, privacy boundary, and constraint priority."

| Capability family | Patterns defined in this chunk |
|---|---|
| Multi-Speaker Memory | Background speech retrieval; Scope tracking |
| Multi-Speaker Instruction Following | Selective disclosure (definition truncated in chunk) |
| Multi-Speaker Reasoning | Named in taxonomy; patterns not reached in this chunk |

- Background speech retrieval: "Decisive task facts occur only in overlapping background speech. The model must recover and use the relevant facts, preserve their background-speaker source, and avoid substituting foreground assumptions or unrelated context. When it cannot recover them, it should say so rather than invent an answer."
- Scope tracking: "Different speakers contribute at least one global constraint and one local constraint to the same shared task. A global constraint applies to the whole group, whereas a local constraint applies to only certain individuals." The model must attach each constraint to holder and scope "without globalizing a local constraint or localizing a shared one."
- Selective disclosure (partial): "Earlier speech tells the assistant which facts to withhold and from which audience; the exact facts either come from assistant prior memory or are stated aloud to the assistant."
- Every case is "authored natively in English or Mandarin rather than translated"; corpus, voice, and audio statistics are deferred to Appendix A.

**Covers:** Sections 1–3.1 (abstract through selective-disclosure opening; chunk ends mid-sentence at Figure 1 caption and "Examples are condensed from actual benchmark cases, which can include up to three human speakers.")
