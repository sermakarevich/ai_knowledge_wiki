# Do Proactive Agents Really Need an LLM to Decide When to Wake and What to Anchor?

**Paper:** [Do Proactive Agents Really Need an LLM to Decide When to Wake and What to Anchor? (Liu et al., 2026)](https://arxiv.org/abs/2605.30152)

## Human Readable TL;DR

Imagine a proactive AI assistant as an office with two staff: a fast, cheap "watchman" and a brilliant-but-slow expert consultant. Current systems make the expensive consultant check every email, file change, and calendar update -- hundreds of times a day -- to decide whether to help you. This paper replaces that watchman role with a tiny specialized model that watches your computer activity as a web of connections (a graph), instantly deciding both *when* something is worth interrupting you about and *exactly which files/apps/URLs* to mention. The consultant (the big LLM) only gets called when the watchman says something is important, making the system 4-83x faster, far cheaper, and laser-focused on what you're actually doing rather than vague general suggestions.

## TL;DR

This paper argues that the always-on "trigger" and "context-routing" components of proactive LLM agents don't need to be LLMs themselves. Instead, user activity is natively a structured event stream -- a heterogeneous temporal graph -- so a small Temporal Graph Learning (TGL) model can jointly produce: (1) a per-event wake-up probability, and (2) per-entity routing scores for grounding, in a single forward pass. Evaluated on 14 LLM backbones across the ProactiveAgent benchmark, TGL improves F1 by +3.1 to +46.0 points (mean +16.7) while running at 11.13 ms/event -- 4-83x faster than LLM-based triggers -- with a ~220 MiB footprint enabling on-device deployment.

---

## Problem & Motivation

Proactive agents run continuously, checking every user event to decide: (1) *when* to intervene, and (2) *what* context to ground the intervention on. Current systems implement all three roles (trigger, context provider, downstream agent) with LLM-shaped components, causing two problems:

**Expensive and slow triggering.** An LLM trigger running on every event (e.g., every 15 seconds = 240 calls/hour) incurs full LLM cost regardless of whether any action is needed. LLM latency sits on the always-on critical path.

**Ungrounded, decoupled suggestions.** Trigger and context modules are separate stages, so the wake-up signal and supporting evidence can disagree. Suggestions often default to the session topic or active application rather than the specific entity the user is actually working on.

The root cause: user activity is not natively text. The OS logs structured events `(actor, verb, object, timestamp)`, which are then serialized to text just so an LLM can re-infer the structure -- a round-trip the system never had to take. The native representation is a heterogeneous temporal graph.

---

## Main Original Ideas

1. **User Activity as Heterogeneous Temporal Graph** -- Convert the timestamped event stream into a graph where event nodes are linked temporally and entity nodes (files, apps, URLs, queries) are linked to the events that touched them. Construction is deterministic and rule-based, requiring no LLM calls.

2. **Joint Trigger + Routing in One Forward Pass** -- A single shared TGL backbone (3-layer relation-aware GATv2 + Jumping Knowledge head) produces both a per-event trigger probability (trigger head over event nodes) and per-entity relevance scores (routing head over entity nodes) from the same hidden state. Both heads are trained jointly.

3. **Graph-First, LLM-Reserved Design Principle** -- Keep a lightweight temporal model always on; reserve full LLM reasoning only for moments that survive the trigger. The downstream LLM receives the routed entity list as structured context and only runs when the trigger fires.

4. **Anchor Routing Labels** -- Routing supervision is derived deterministically: extract entities mentioned in the ground-truth `proposed_task` string and match them to graph nodes. No human annotation needed beyond the existing ProactiveAgent benchmark labels.

5. **Node Featurization with Frozen Text Encoder** -- Each node combines: a 768-dim frozen BGE sentence embedding of its surface label, a 32-dim learned type embedding, and a 32-dim learned time-gap MLP (for event nodes). Projected to 256-dim for the GNN.

---

## Key Findings

| Backbone | Vanilla F1 | + TGL F1 | Δ F1 |
|---|---|---|---|
| Qwen3-8B | 26.14 | 72.14 | **+46.0** |
| Qwen3-4B | 38.54 | 66.77 | **+28.2** |
| DeepSeek-V4-Pro | 47.12 | 73.70 | **+26.6** |
| Gemma-3-12B | 58.04 | 77.30 | **+19.3** |
| LLaMA-3.1-8B | 55.06 | 72.07 | **+17.0** |
| Claude-Sonnet-4.6 | 58.64 | 76.20 | **+17.6** |
| Claude-Opus-4.7 | 74.44 | **79.86** | +5.4 |
| GPT-5.4 | 73.47 | **76.57** | +3.1 |

- TGL improves F1 on **all 14 backbones** (range +3.1 to +46.0, mean +16.7); no backbone regresses
- TGL with Qwen2-7B-Instruct (F1=70.68) **outperforms full proactive fine-tuning** of Qwen2-7B (F1=66.47)
- One checkpoint, one threshold aligns all 14 backbones to R ≥ 96%, P ≥ 50%

**Trigger architecture comparison:**

| Trigger | AUC (must-fire) | Brier | Server latency | Laptop latency | Memory |
|---|---|---|---|---|---|
| TGL (Ours) | **0.738** | 0.308 | **11.13 ms** | **13.99 ms** | **~220 MiB** |
| Qwen3-0.6B | 0.668 | 0.584 | 40.4 ms | 162.3 ms | ~1.5 GB |
| Qwen3-8B | 0.644 | 0.580 | 78.6 ms | 1,156.8 ms | ~16 GB |
| Proactive-Qwen3-0.6B (full SFT) | 0.505 | 0.657 | 3,927 ms | 11,966 ms | ~1.5 GB |

- TGL: 4-7x faster than LLM triggers on server; 12-83x faster on laptop
- TGL has lowest Trigger std (0.035) -- single threshold near-optimal for every backbone; LLM triggers require per-backbone calibration
- LLM triggers collapse probabilities to extremes (94-98% of events at [0,0.05) ∪ [0.95,1]); TGL produces a continuous, well-calibrated distribution

**Ablation (mean F1 drop vs. full TGL):**
- No TGL trigger (always fire, keep routing): -3.2 F1
- Random routing instead of TGL routing: -8.6 F1
- No TGL at all (prompt-only control): -12.7 F1

---

## Suggestions & Future Directions

1. **On-device personalization** -- Fine-tune the lightweight TGL model with user feedback (accepted = positive fire signal, dismissed = over-fire signal) while keeping the downstream LLM fixed. User-specific state lives locally in the graph model.

2. **Direct system identifiers** -- The ProactiveAgent benchmark releases text-serialized logs; a production deployment that owns the data pipeline can feed native file names, app names, URL domains directly, skipping entity reconstruction.

3. **Subjective UX evaluation** -- The offline RM-judge protocol measures task suggestion quality but does not capture interruption timing, attentional cost, or user experience under deployment conditions.

4. **Fairness and privacy analysis** -- Demographic subgroups in FingerTip (gender, age, occupation, location, device) must be analyzed for routing bias before deployment. Production systems require data minimization, sensitive-entity filtering, and opt-out controls.

5. **Broader modalities** -- The graph-first, lightweight-controller principle may transfer to voice, wearable, and IoT activity streams where the always-on cost constraint is even more critical.

---

## Authors & Institutions

Xiaoze Liu (Purdue University), Ruowang Zhang (Purdue University), Amir H. Abdi (Microsoft), Michel Galley (Microsoft), Zhikai Chen (Michigan State University), Siheng Xiong (Georgia Institute of Technology), Xiaoqian Wang (Purdue University), Jing Gao (Purdue University)
