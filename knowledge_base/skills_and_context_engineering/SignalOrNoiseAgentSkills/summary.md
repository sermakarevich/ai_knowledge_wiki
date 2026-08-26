# Signal or Noise? A Benchmark Study of Agent Skills in Web Development

**Paper:** [Signal or Noise? A Benchmark Study of Agent Skills in Web Development (Yang & Ding, 2026)](https://arxiv.org/abs/2608.23067)
**Wiki:** [[index]] | **Digest:** [[digest]]

## Human Readable TL;DR

An "Agent Skill" is like handing a new employee a cheat-sheet before every task — a page of house rules, dos and don'ts, and example snippets for working in, say, a React codebase. The obvious assumption is that a good cheat-sheet always helps. This paper tests that assumption carefully, on 31 real public cheat-sheets and 50 realistic web-coding projects, across four different AI coding models. The surprising finding: on average, handing over the cheat-sheet makes the AI *worse* at the job — it solves fewer tasks and burns far more effort reading the extra paperwork — and only bumps performance for a minority of cheat-sheet/project combinations. Worse, a cheat-sheet that helps one AI model can actively hurt a different model on the exact same job. The paper argues cheat-sheets should be handed out selectively — per task, per project, per specific AI model — rather than attached automatically to every session.

## TL;DR

WebDev-Skills-Bench is a controlled benchmark that injects 31 third-party Agent Skills into 50 Web-Bench projects (1,000 ordered tasks) across four coding models (Claude Sonnet 4, GPT-5.1, DeepSeek-V4-flash, Qwen3-Coder-30B-A3B), using four matched conditions — no-Skill baseline (C0), target Skill (C1), length-matched irrelevant-Skill control (C2), and leave-one-out slice ablation (C3) — to separate a Skill's content effect from the pure prompt-length cost of injecting it. Target injection lowers mean Pass@2 by 1.3–4.2 pp and Task Completion Depth on every model while raising token cost 72–394%, with gains in only 17–36% of the 117 core (Skill, project) pairs; the loss splits into two mechanisms (length distraction for Sonnet/Qwen vs content misalignment for GPT-5.1/DeepSeek), concentrates on easy tasks the model already solves, and barely correlates across models (|r| ≤ 0.12). A slice ablation on genuinely helpful Skills finds anti-pattern ("don't") rules are the one reliably positive, cheap component, while example code is null on average and actively hurts the strongest model.

---

## Problem & Motivation

Agent Skills — reusable Markdown modules of framework conventions, anti-patterns, and example code injected into every prompt of a coding-agent session — are proliferating on public marketplaces, but their value is assumed rather than measured. Because a Skill is injected persistently (unlike RAG or few-shot examples used per-query), it expands every prompt in a session even when irrelevant, so a benchmark needs to ask not just "can the agent solve this task" but "should this Skill have been injected at all." Prior evidence is thin and contradictory: SkillsBench reports a +16.2 pp aggregate gain, while SWE-Skills-Bench finds 39 of 49 Skills produce zero pass-rate improvement — and neither isolates web development or separates a Skill's content from the simple fact that it lengthens the prompt.

## Main Original Ideas

1. **Workspace-aware injection protocol.** Only `SKILL.md` is placed in the prompt; auxiliary files (references, examples, scripts) are mounted into the agent's filesystem under `.skills/<skill-id>/`. This makes prompt length depend on `SKILL.md` alone, so a byte-matched control is well-defined even for Skills that ship many auxiliary files.
2. **Four matched conditions (C0–C3).** C0 (no Skill) and C1 (target Skill) give gross utility. C2 injects a length-matched (±5% bytes) but *irrelevant* Skill, splitting gross utility into a length artifact (C2−C0) and a content effect (C1−C2) — the paper's central methodological device. C3 is a leave-one-out slice ablation (drop positive rules, drop anti-patterns, drop example code) run on the positive-gain tail, attributing *which part* of a helpful Skill actually helps.
3. **Chain-position-aware task corpus.** Built on Web-Bench's 20 sequentially-dependent tasks per project (deterministic Playwright tests, not LLM-as-judge), which exposes how injection affects early-easy vs late-hard tasks differently — a dimension flat pass-rate benchmarks collapse away.
4. **Conservative expert routing.** 1,550 candidate (Skill, project) pairs were manually judged "core" or "skip" by two annotators (96.5% agreement, κ≈0.74, ~258 person-hours), yielding 117 core pairs used for the main comparison, so indiscriminate mismatches don't dilute the signal.

## Key Findings

**Table 1 — model-level C1−C0 effects on 117 core pairs (N=3 per cell):**

| Model | ∆Pass@1 (pp) | ∆Pass@2 (pp) | ∆TCD | Win/Tie/Loss (%) | Token overhead ρ |
|---|---|---|---|---|---|
| Claude Sonnet 4 | −2.8 | **−4.2** | −0.85 | 30/9/61 | +72% |
| GPT-5.1 | −1.6 | −1.3 | −0.26 | 35/20/45 | +74% |
| Qwen3 Coder 30B | −3.2 | −2.3 | −0.47 | 17/35/48 | +91% |
| DeepSeek V4 Flash | −4.1 | −2.0 | −0.40 | 36/16/48 | +394% |

- Every model has a negative mean ∆Pass@2 yet a nontrivial positive-gain tail (17–36% of pairs win) — the effect is not uniform, it's a routing problem.
- Losses concentrate on **easy early tasks** (−4.0 to −10.7 pp, CI excludes zero on every model); moderate/challenging tasks show no consistent loss. Mechanism: "retry lock-in" — an injected Skill fixes a superficial choice (e.g. button label) in a way that removes the model's usual self-repair flexibility on Web-Bench's two-attempt budget, converting a recoverable miss into a chain-terminating failure.
- The C2 length control splits the panel into two mechanisms: **length distraction** for Sonnet 4 and Qwen (an equally-long irrelevant Skill reproduces most of the loss) vs **content misalignment** for GPT-5.1 and DeepSeek (length is neutral, the specific content still hurts).
- Cross-model correlation of per-pair effects is near zero (Pearson −0.08 to +0.12; 74% of pairs have mixed signs across models); one pair (lowdb × database-optimizer) swings from +33 pp on Sonnet to −22 pp on DeepSeek/Qwen — the same Skill content, opposite outcomes.
- C3 slice ablation on 5 robustly-positive pairs: anti-pattern rules are the only slice with a statistically reliable effect (p=0.008, +3.1 pp pooled); example code is null pooled (−0.7 pp) but costs ~22.7% of the SKILL.md token budget, and it helps weaker models (DeepSeek +8.3 pp, Qwen +3.7 pp) while hurting the strongest one (Sonnet −15.3 pp).

## Suggestions & Future Directions

1. Treat Skill injection as an **opt-in, per-deployment routing decision** — inject only when a pair-level signal crosses an empirical utility threshold, not as a session-start default.
2. Evaluate and inject **by chain position**: skip Skills on early/easy tasks, inject only once error rates rise, rather than attaching a Skill before any task begins.
3. Marketplaces should publish **model-conditioned** utility, not a single ranking — a Skill validated on a frontier model gives no signal about a cheaper backend.
4. Adopt **length-matched controls** (C2-style) as a minimum standard for future Agent-Skill benchmarks; without one, this study would have reported only a flat negative effect and missed the length/content mechanism split.
5. Acknowledged limitations: seed spread (4.4 pp across Sonnet replicates) comparable to the headline effect size; only 109 unique C2 runs across 117 pairs; C1 evaluated only on core-tier (on-target) pairs, so off-target deployment is untested; the Skill set is drawn only from high-visibility public repos; metrics are functional-correctness-only (Playwright), missing readability/UX/accessibility gains a Skill might produce.

## Authors & Institutions

Ziyue Yang, Ding Fan — Baidu NLP, Beijing, China.
