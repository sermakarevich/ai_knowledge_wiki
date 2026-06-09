# How Anthropic Enables Self-Service Data Analytics with Claude

**Paper:** [How Anthropic Enables Self-Service Data Analytics with Claude (Chen Chang, Clement Peng, Justin Leder, Johanne Jiao, Josh Cherry, 2026)](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude)

## Human Readable TL;DR

Imagine you could ask a smart assistant any business question -- "how many active users did we have last month?" -- and get a correct, sourced answer automatically. Anthropic built exactly that by training Claude to be a data analyst for their company. The trick wasn't just making Claude smart; it was organizing all their data carefully, writing detailed "cheat sheets" for Claude to consult, and constantly checking its answers for mistakes. With this system, 95% of routine data questions are now answered automatically without any human analyst involvement.

## TL;DR

Anthropic achieved 95% automation and ~95% accuracy on business analytics queries by deploying Claude as an agentic analytics system built on four layers: canonical data foundations, curated semantic reference surfaces, procedural skill files, and continuous offline/online validation. The critical insight is that accuracy improvements come from collapsing data ambiguity and making governed answers discoverable -- not from model capability alone. Skills elevated baseline accuracy from 21% to 95%+, while adversarial review added 6% further at a 32% token cost.

---

## Problem & Motivation

Traditional self-service analytics faces two structural problems: wide denormalized tables create inconsistent metric definitions as companies scale, and ringfenced dashboard environments miss long-tail business questions causing dashboard proliferation. LLM-based agents offer an alternative but introduce three failure modes -- concept-to-entity ambiguity (which "active users" definition?), data staleness (schemas and definitions change), and retrieval failure (correct answers exist but remain undiscovered). These three failure modes, not model intelligence, are the root cause of analytics agent inaccuracy.

---

## Main Original Ideas

1. **Four-Layer Agentic Analytics Stack** -- A systematic architecture addressing each failure mode: canonical data foundations to eliminate ambiguity, curated reference surfaces as sources of truth, skill files encoding procedural knowledge, and validation layers for continuous quality assurance.

2. **Skills as Accuracy Multipliers** -- Markdown files encoding senior analyst workflows that Claude loads on demand. Without skills, accuracy was 21%; with skills it reached 95%+. Knowledge skills narrow search from million-field warehouses to dozens of curated fields before query execution.

3. **Semantic Layer Priority** -- Agents are structurally required to consume compiled metric/dimension definitions before falling back to raw SQL. Auto-generated definitions encoded existing ambiguities; human-curated layers proved superior. Every correct answer should route through the semantic layer.

4. **Adversarial Review Sub-Agents** -- A Claude sub-agent aggressively challenges underlying assumptions in every response, yielding +6% accuracy at a cost of 32% more tokens and 72% higher latency. Trade-off must be calibrated per use case.

5. **Correction Harvesting Pipeline** -- Scheduled agents scan stakeholder Slack channels hourly for correction language, draft reference doc fixes, and open PRs tagged to domain owners. Corrections feed back into offline eval sets, creating a self-improving loop.

6. **Provenance Footers** -- Every response includes source tier (semantic layer > curated reference > raw table), data freshness, and ownership -- enabling stakeholders to judge whether answers need pre-verification before upstream use.

---

## Key Findings

| Metric | Value |
|---|---|
| Queries automated | 95% |
| Aggregate accuracy | ~95% |
| Accuracy without skills | 21% |
| Accuracy with full skills | 95%+ |
| Accuracy in best domains | ~99% |
| Improvement from raw SQL corpus retrieval | <1 pp |
| Improvement from adversarial review | +6% |
| Token cost of adversarial review | +32% |
| Latency cost of adversarial review | +72% |
| Data model PRs including skill updates | 90% |
| Failed questions with answer in corpus but unused | 80% |

- **Raw query corpus retrieval is a trap** -- 80% of failed questions had correct answers in thousands of SQL files, but agents couldn't use them; the bottleneck was structural mapping of questions to entities, not information access.
- **Documentation stacking has diminishing returns** -- Beyond three refinement rounds, docs became longer but not better; accuracy declined.
- **Cheaper adversarial models fail** -- Swapping the adversarial reviewer to a cheaper model eliminated most accuracy gains without meaningful latency improvement.
- **Eval ceilings drop with new model generations** -- Calibrate eval quantity; diminishing returns appear past dozens per topic.

---

## Suggestions & Future Directions

1. **Start minimal** -- Canonical datasets + dozens of offline evals + thin knowledge skills capture most upside before adding more complex infrastructure.
2. **Gate domain launches on eval thresholds** -- Domain owners cannot announce agents until ~90% offline accuracy is cleared.
3. **Anchor evals to stable snapshots** -- Pin to git SHAs and snapshot dates to prevent drift; store results as warehouse telemetry for longitudinal analysis.
4. **Address silent failures** -- Wrong-but-plausible answers used unchallenged remain incompletely solved; provenance footers and explicit human sign-off for leadership-bound outputs are partial mitigations.
5. **Resolve organizational tradeoffs explicitly** -- Correctness priority vs. speed to deploy, technical vs. non-technical audiences, accuracy vs. cost, and broad vs. scoped data access all require deliberate decisions before deployment.

---

## Authors & Institutions

Chen Chang, Clement Peng, Justin Leder, Johanne Jiao, Josh Cherry -- Data Science and Data Engineering teams, Anthropic
