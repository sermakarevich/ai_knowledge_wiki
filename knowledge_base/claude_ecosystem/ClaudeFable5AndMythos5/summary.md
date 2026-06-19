# Claude Fable 5 and Claude Mythos 5

**Source:** [Claude Fable 5 and Claude Mythos 5 (Anthropic, 2026)](https://www.anthropic.com/news/claude-fable-5-mythos-5)

## Human Readable TL;DR

Anthropic has released two new AI models: Claude Fable 5 (available to everyone) and Claude Mythos 5 (restricted to vetted researchers and security professionals). Think of Fable 5 as a very capable AI assistant that can write millions of lines of code overnight or analyze complex scientific data -- but with guardrails built in. Mythos 5 is the same engine with some of those guardrails removed for people doing sensitive work like drug discovery or cybersecurity defense. Anthropic also built a safety system that quietly redirects dangerous requests to a safer model, rather than simply refusing them.

## TL;DR

Anthropic launched Claude Fable 5 (general availability) and Claude Mythos 5 (restricted access) as Mythos-class models achieving SOTA across software engineering, long-context reasoning, vision, and life sciences. Fable 5 replaces harmful-request refusals with a silent fallback to Opus 4.8 (<5% of sessions). Mythos 5 is initially gated to cyber defenders and approved biology researchers due to dual-use risks demonstrated in protein design and genomics benchmarks.

---

## Problem & Motivation

AI models at the frontier increasingly demonstrate dual-use capabilities -- the same reasoning that accelerates drug discovery can enable biosecurity threats. Anthropic's challenge is deploying maximally capable models while preventing catastrophic misuse, specifically in cybersecurity exploitation, biological/chemical weapons, and model distillation by adversarial actors. The Mythos-class architecture attempts to solve this by separating capability tiers with different access controls rather than universally restricting all users.

---

## Main Original Ideas

1. **Fallback-as-Safeguard** -- Instead of outright refusal, Fable 5 silently reroutes flagged requests to Claude Opus 4.8. This preserves user experience for the >95% of sessions that never trigger classifiers, while maintaining safety boundaries without visible friction.

2. **Tiered Access Architecture** -- Mythos 5 is the same base model as Fable 5 but with safeguards removed for authorized users. This creates a capability ladder: broad public access (Fable 5) → vetted professionals (Mythos 5 with cyber safeguards) → authorized biology researchers (Mythos 5 full access).

3. **Dual-Use Capability Benchmarking** -- Anthropic used AAV (adeno-associated virus) assembly prediction as a concrete dual-use benchmark: Mythos-class models outperformed specialized protein language models in predicting gene therapy properties, establishing a measurable threshold where AI capability creates real-world biosecurity risk.

4. **Autonomous Research Execution** -- Mythos 5 demonstrated end-to-end autonomous genomics research: assembled single-cell data across 138 species, trained a machine learning model, and outperformed a published Science paper result with a model 100x smaller -- suggesting the models can substitute for multi-person research teams on specific tasks.

5. **Distillation Protection** -- A new safeguard category explicitly targets extraction of Mythos-class capabilities for use in competing models, particularly by adversarial state actors. This is framed as a national security concern, not just commercial IP protection.

---

## Key Findings

| Domain | Result |
|--------|--------|
| Software engineering (FrontierCode) | Highest performance at medium effort |
| Finance reasoning (Hebbia benchmark) | Top score on senior-level knowledge work |
| Pokémon FireRed (vision-only) | Completed game using only visual input |
| Slay the Spire (long-context memory) | 3x improvement over Opus 4.8 with persistent file memory |
| Drug design (protein targets) | 9/14 targets yielded strong candidates; ~10x acceleration for experts |
| Molecular biology hypotheses | ~80% preferred vs. Opus-class in blinded scientist comparisons |
| Genomics ML model | Outperformed recent Science publication; 100x smaller model |
| Jailbreak resistance | 0 harmful single-turn requests across 30 techniques in external testing |
| Misalignment level | "Low, similar to Opus 4.8" per automated assessment |

- Stripe completed a 50-million-line codebase migration in one day (estimated two months with human team)
- UK AISI made progress toward a universal jailbreak in brief testing; production has not confirmed success on complex realistic tasks
- Fallback to Opus 4.8 triggered in <5% of sessions on average

---

## Suggestions & Future Directions

1. Broader trusted access for cybersecurity organizations beyond Project Glasswing (planned)
2. Expanded biology researcher trusted access program (launching)
3. Anthropic acknowledges universal jailbreak prevention is "likely impossible" -- stated goal is making remaining exploits slow and costly enough to detect before scale-based deployment
4. 30-day mandatory data retention for Mythos-class traffic, with logged human access and guaranteed deletion, sets a privacy precedent for future model generations

---

## Authors & Institutions

Anthropic (no individual authors listed for the announcement)
