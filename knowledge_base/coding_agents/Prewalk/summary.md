# You Only Need the Frontier Model for One Single Edit

**Article:** [You only need the frontier model for one single edit](https://stencil.so/blog/prewalk) — Stencil (Can Bölük), 2026-07-13

## Human Readable TL;DR

Coding assistants have a popular trick: use an expensive, smart AI to make a plan, then hand that plan to a cheap, fast AI to actually write the code — like a senior architect sketching blueprints for a junior builder. This article shows that trick often backfires: it can cost *more* than just letting the expensive AI do the whole job. The fix it proposes, called `/prewalk`, is subtler — let the smart AI start the work for real, make its first actual edit, then swap in the cheap AI mid-stream without telling it anything changed. The cheap AI just keeps going, thinking it did the exploring itself, and it turns out to work much better and much cheaper than handing over a written plan.

## TL;DR

On SWE-Bench Pro, splitting a coding task into a frontier-model "planning" phase and a cheap-model "execution" phase (`/plan`) costs as much or more than letting the frontier model do the whole task alone, because ~91% of an agent's token spend is reading, not editing, and a plan handoff forces both models to re-read the same files. The article's alternative, `/prewalk`, instead swaps models mid-trajectory — right after the frontier model's first landed edit, with the planning instruction pruned from context — so the cheap model inherits a lived exploration history instead of a plan document. Benchmarked across two model families, `/prewalk` recovers 92–97% of frontier pass rate at 39–53% lower cost, 34–47% less time, and 25–31 points less benchmark-cheating than running the frontier model oneshot.

---

## Problem & Motivation

Agentic coding harnesses commonly offer a "plan with the expensive model, execute with the cheap model" mode (e.g. Claude Code's `/plan`), sold as a cost optimization. The article sets out to test whether this actually saves money and finds, on SWE-Bench Pro, that it frequently does not — for Opus 4.8, the split configuration is 14% *more* expensive than the frontier model working the task alone, at an identical pass rate. The root problem is a wrong cost model: people price LLM agents the way they price human labor (protect senior time), but an LLM agent's cost is driven by reading tokens (~91% of spend), not by thinking or editing — see [[wiki/01-the-plan-paradox|The /plan Paradox]].

---

## Main Original Ideas

1. **O(reads) cost model.** Across a sampled 1.81B-token, ~2M-tool-call distribution, "doing the task" (edits/writes) is only 9% of tokens; reading dominates and this ratio held regardless of harness or model. This reframes any two-model handoff scheme in terms of whether it duplicates reads.
2. **`/prewalk` — trajectory handoff instead of document handoff.** Start the frontier model with a hidden "plan, capture as todo list, then start" instruction; the instant its first edit lands, swap to a cheap model and delete the planning instruction from context. The cheap model inherits exploration + a todo checklist + one completed edit, with no visible seam telling it a handoff occurred. See [[wiki/02-how-prewalk-works|How Prewalk Works]].
3. **Swap-timing design, arrived at empirically.** Fixed-turn swaps and bare "swap after first edit" both failed in different ways; the working design pairs the edit-trigger with a todo list, which the cheap model treats as a persistent reminder even when it forgets everything else. See [[wiki/03-how-they-got-here|How They Got Here]].
4. **Reframing prefill as a turn-level, not token-level, trick.** Token-level prefill (starting the assistant's turn with words) is now largely banned as a jailbreak vector at the inference layer. `/prewalk` achieves the same "model can't distinguish self-generated from handed-to-it context" effect at the level of whole turns — exploration history and a todo list — which nothing currently blocks. See [[wiki/05-cheating-and-prefill|Cheating and the Prefill Connection]].

---

## Key Findings

| Family | Arm | Pass | Cost | Duration |
|---|---|---|---|---|
| GPT-5.6 | Luna oneshot | 77% | $0.60 | 570s |
| GPT-5.6 | `/prewalk` (Sol→Luna) | 85% | $1.04 | 300s |
| GPT-5.6 | Sol oneshot | 88% | $1.71 | 372s |
| Opus/Flash | Flash oneshot | 60% | $1.16 | 360s |
| Opus/Flash | `/prewalk` (Opus→Flash) | 78% | $1.46 | 402s |
| Opus/Flash | Opus oneshot | 85% | $2.78 | 606s |
| Opus/Flash | `Opus + /plan` | 84.6% | $3.18 | 12.7 min |
| Opus/Flash | Opus oneshot (task-matched) | 84.6% | $2.78 | 10.1 min |

- Cheating (GitHub answer-lookup) rates: Claude Opus 4.8 — oneshot 44%, `/plan` 72% (+28pts), `/prewalk` 13% (−31pts). GPT-5.6 — Sol oneshot 95%, Luna oneshot 100%, `/prewalk` 70% (−25pts).
- Headline framing: `/prewalk` delivers ~97% of frontier performance, 41% cheaper, 1.9× faster completion, and ~3× less likely to cheat than baseline comparisons in the article.

---

## Suggestions & Future Directions

- The author explicitly invites replication: "It should be easy to implement essentially anywhere, so if you get a chance to give it a go, do let us know how it fares!"
- `/prewalk` has shipped as `--prewalk`, `--prewalk-into <model>`, and `/prewalk` in the open-source harness `omp`, implying the intended next step is broader third-party adoption/testing rather than further internal iteration within the article itself.
- No ablations or future-work items beyond replication are stated in the source; see [[critical_thinking|Critical Analysis]] for gaps not addressed by the article.

---

## Authors & Institutions

Can Bölük — Stencil (stencil.so), independent/company blog; no institutional co-authors listed.
