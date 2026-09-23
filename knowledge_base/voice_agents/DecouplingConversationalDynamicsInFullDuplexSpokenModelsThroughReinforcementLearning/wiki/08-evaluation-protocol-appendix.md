[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluation Protocol Appendix
**In one sentence:** This appendix chunk reports DuplexPO's attention redistribution away from the BOS sink toward real-text, recent-context and PAD-state positions, calibrates the pairwise LLM judge with synthetic ±1.0s timing shifts, details the dynamics-only judging protocol with Fisher/Seamless win rates, and reproduces the system and user prompt templates keyed by Interaction ID.
## Key points
- DuplexPO reduces <BOS> sink mass from 70.2% (Moshi 7B) to 14.5% and first-4-positions mass from 74.2% to 37.9%, while raising PAD mass from 28.0% to 77.5%.
- Real-text attention rises from 1.8% to 22.5%, last-16-tokens mass from 13.5% to 33.4%, and attention entropy from 1.63 to 3.19 versus Moshi 7B.
- PAD positions encode non-speech/waiting states that inform speaking and yielding decisions in the streaming representation.
- Judge calibration on 26 Fisher conversations with identical transcripts but ±1.0s agent-timestamp shifts prefers original timing: 69.2% vs delayed (p=0.076) and 80.8% vs advanced (p=0.002).
- Stronger sensitivity to premature (−1.0s) than delayed (+1.0s) entry supports FCDR's onset reward with narrower tolerance for early initiation than delayed responses.
- Pairwise judging uses Gemini 3.0 Pro, blinded randomized candidate order, JSON-schema-valid outputs only, Candidate A = SFT Baseline vs Candidate B = DuplexPO, judging only turn-taking, backchannel, and barge-in handling.
- DuplexPO (B) beats SFT Baseline (A) overall 76.9% on Fisher (20–6, p=0.009) and 69.3% on Seamless (264–117, p<1e-13), with backchannel highs of 91.7% Fisher and 82.9% Seamless.
---
## Attention mass distribution (Figure 4 / Table 6)
Table 6: Attention mass distribution (%) across token categories.

| Metric | Moshi 7B | DuplexPO |
|---|---|---|
| <BOS> sink (pos. 0) | 70.2 | 14.5 |
| First 4 positions | 74.2 | 37.9 |
| PAD positions | 28.0 | 77.5 |
| Real-text positions | 1.8 | 22.5 |
| Last 16 tokens | 13.5 | 33.4 |
| Attention entropy | 1.63 | 3.19 |

> "Attention mass is averaged across layers and grouped by token category, including the <BOS> token, early positions, PAD positions, real-text tokens, and recent-context tokens."
> "Compared with Moshi 7B, DuplexPO assigns less mass to the initial <BOS> sink and more mass to real-text, recent-context, and PAD-state positions."

**Covers:** Figure 4 / Table 6 attention-mass comparison (chunk pp. 18)

## Judge calibration with synthetic timing perturbations (Appendix E)
Controlled check on Fisher: user timeline and agent transcript unchanged, agent timestamps shifted by ±1.0s; +1.0s makes responses/backchannels systematically late, −1.0s makes agent speech premature during user speech; same blinded pairwise protocol as Appendix F with randomized order and aggregate dynamics statistics removed from judge input; win rates over non-tie judgments with two-sided binomial sign test.

Table 7: Judge calibration under synthetic timing perturbations on Fisher.

| Perturbation | # Conv. | Original Wins | Perturbed Wins | Ties | Original Win Rate | p-value |
|---|---|---|---|---|---|---|
| Delayed by +1.0s | 26 | 18 | 8 | 0 | 69.2% | 0.076 |
| Advanced by −1.0s | 26 | 21 | 5 | 0 | 80.8% | 0.002 |

> "Because the transcript content is identical across candidates, the results indicate a timing preference aligned with human conversational perception, with stronger sensitivity to premature turn entry than to comparable response delays"

**Covers:** Appendix E timing-perturbation calibration (chunk p. 18)

## LLM pairwise judge for full-duplex dialogue naturalness (Appendix F)
Design: evaluate conversational dynamics, not semantic answer quality; Gemini 3.0 Pro; count only JSON-schema-valid, error-free outputs; anonymized labels; Table 8 overall + dimension preferences; win rates exclude ties; two-sided binomial sign test.

Table 8: Conversation-level LLM pairwise judge results (B = DuplexPO, A = SFT Baseline).

| Dataset | Criterion | Total | B wins | A wins | Ties | B win rate | p-value |
|---|---|---|---|---|---|---|---|
| Fisher | Overall | 26 | 20 | 6 | 0 | 76.9 | 0.009 |
| Fisher | Turn-taking | 26 | 20 | 6 | 0 | 76.9 | 0.009 |
| Fisher | Backchannel | 26 | 22 | 2 | 2 | 91.7 | < 1e-4 |
| Fisher | Barge-in handling | 26 | 21 | 3 | 2 | 87.5 | < 1e-3 |
| Seamless | Overall | 383 | 264 | 117 | 2 | 69.3 | < 1e-13 |
| Seamless | Turn-taking | 383 | 250 | 123 | 10 | 67.0 | < 1e-10 |
| Seamless | Backchannel | 383 | 261 | 54 | 68 | 82.9 | < 1e-32 |
| Seamless | Barge-in handling | 383 | 237 | 70 | 76 | 77.2 | < 1e-21 |

**Covers:** Appendix F judge setup and Table 8 results (chunk pp. 18–19)

## Reward visualisation (Appendix G, partial)
> "As shown in Figure 5, the reward curve increases monotonically and then stabilises, suggesting that training is robust and generalises across dialogue contexts."
> "the stop reward provides the strongest signal" (sentence truncated in chunk)

**Covers:** Appendix G opening lines (chunk p. 19)

## System prompt for pairwise judging (Table 9)
Verbatim rules: expert evaluator for full-duplex spoken dialogue rhythm; compare two candidate system turns from same local context; evaluate ONLY turn-taking, backchanneling, user barge-in handling; use only observable local context; do NOT evaluate factual correctness, knowledge, helpfulness, informativeness, or completeness; do NOT prefer longer/more detailed candidates; tie if similar; penalise competitive interruption, awkward delayed feedback, excessive overlap, failure to yield; required JSON fields include:

```
"interaction_id": "string",
"pair_id": "string",
"candidate_a_id": "string",
"candidate_b_id": "string",
"inferred_turn_state": "user_holding_floor|user_yielding_floor|backchannel_opportunity|full_turn_opportunity|uncertain",
"preferred_candidate": "A|B|tie",
```

plus `dimension_preferences` for turn_taking / backchannel / user_barge_in_handling, `major_rhythm_issues`, `content_quality_ignored_note`, and `confidence` 0.0–1.0.

**Covers:** Table 9 system prompt (chunk pp. 19–20)

## User-prompt template with Interaction ID (Table 10)
Template instructs: compare A vs B for overall rhythm across the conversation sample; ignore factual correctness, answer completeness, informativeness; output only valid JSON. Sections:

```
## Interaction ID
{interaction_id}
## Shared user timeline
- [user] ({user_turn_1_start_s:.2f}s--{user_turn_1_end_s:.2f}s) {user_turn_1_text}
## Candidate A assistant timeline
- [candidate] ({candidate_a_turn_1_start_s:.2f}s--{candidate_a_turn_1_end_s:.2f}s) {candidate_a_turn_1_text}
## Candidate A observable rhythm summary
- n_turns, total_speech_ms, total_user_overlap_ms, n_user_overlaps, n_interrupted_by_user, median_pause_after_user_ms
## Candidate B assistant timeline
- [candidate] ({candidate_b_turn_1_start_s:.2f}s--{candidate_b_turn_2_end_s:.2f}s) {candidate_b_turn_2_text}
```

Chunk truncates after Candidate B timeline opening.

**Covers:** Table 10 user-prompt template including Interaction ID header (chunk p. 20)
