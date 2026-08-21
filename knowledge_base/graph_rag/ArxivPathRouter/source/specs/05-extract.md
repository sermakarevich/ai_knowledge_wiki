# Extract task: ArxivPathRouter wiki page 05

**Context is tight on this model — read ONLY the input file(s) listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- `/Users/sergii/.kb/papers/ArxivPathRouter/source/chunks/05.txt` — plain text covering: Section 5 Conclusion, Limitations, Ethical Considerations, References (skip — do not summarize the bibliography itself), Appendix A (Evaluation Metrics), Appendix B (Implementation Details), Appendix C (Dataset Details), Appendix D (Additional Experimental Results: KL selection/threshold sensitivity, training dynamics, baseline cross-dataset transfer), Appendix E (Case Studies), of the paper "PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation" (arXiv 2606.16409).
- Figure descriptions (read these too):
  - `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/images/05-fig5-training-dynamics-description.md` — Figure 5, training dynamics on HotpotQA. Embed as `![Figure 5: Training dynamics](images/05-fig5-training-dynamics.png)`.
  - `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/images/05-fig6-baseline-cross-dataset-description.md` — Figure 6, baseline cross-dataset generalization heatmaps. Embed as `![Figure 6: Baseline cross-dataset generalization](images/05-fig6-baseline-cross-dataset.png)`.

## Output

Write the full wiki page to: `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/05-limitations-and-appendix.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Limitations, Implementation Details, and Appendix

**In one sentence:** <the whole section's substance in one sentence — the paper's acknowledged limitations plus the key implementation/dataset/appendix details that support reproducibility and the qualitative case studies>

## Key points

- <5-8 bullets with real content: the concrete limitations acknowledged (extra hyperparameters, more exploration turns, per-step teacher cost), key hyperparameter values (learning rate, group size K, clip range, KL coefficients, thresholds theta_C/theta_P), key evaluation metric definitions (F1, EM, SF-F1, UAR, G-E), the KL selection/threshold sensitivity findings, and the case-study takeaway about outcome-only training's failure modes.>

---

## Conclusion and limitations

<full detail: conclusion summary, limitations, ethical considerations (brief)>

## Evaluation metrics (Appendix A)

<full detail: definitions of Token-level F1, EM, SF-F1, UAR, GPT-4o-mini Evaluation (G-E) — reproduce formulas>

## Implementation and dataset details (Appendix B, C)

<full detail: training framework (veRL), key hyperparameters as a markdown table (learning rate, batch size, group size K, max retrieval turns T, clip range, top-K vocab, KL coefficients, routing thresholds, reward weights), datasets used (HotpotQA, 2WikiMultiHopQA, MuSiQue, etc.) with train/dev/test sizes>

## Additional experimental results (Appendix D)

<full detail: KL selection strategy and threshold sensitivity (Tables 7-8), training dynamics over steps>

![Figure 5: Training dynamics](images/05-fig5-training-dynamics.png)

<baseline cross-dataset transfer comparison>

![Figure 6: Baseline cross-dataset generalization](images/05-fig6-baseline-cross-dataset.png)

## Case studies (Appendix E)

<full detail: summarize the 2-3 case studies (Tables 9-11) — what each demonstrates about failure modes of outcome-only training (e.g., correct answer from parametric memory with no evidence, hallucinated bridge entity, unsupported exact-match answer) and how PathRouter's trajectory differs>

**Covers:** Section 5 (Conclusion), Limitations, Ethical Considerations, Appendix A-E
```

## Rules

- Do NOT summarize or list the References/bibliography — skip it entirely.
- Reproduce hyperparameter values and metric formulas exactly as in the source.
- The page must be self-contained.
- No line limit — be thorough.
- Do not invent content not present in the chunk or figure descriptions.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 05 extracted"`

## Scope

Touch ONLY `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/05-limitations-and-appendix.md`. Do not run any fleet commands other than `bd close`. No git commands.
