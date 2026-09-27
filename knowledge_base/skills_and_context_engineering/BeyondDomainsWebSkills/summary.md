# Beyond Domains: Reusing Web Skills via Transferable Interaction Patterns

**Paper:** [Beyond Domains: Reusing Web Skills via Transferable Interaction Patterns (He et al., 2026)](https://arxiv.org/abs/2606.17645)

## Human Readable TL;DR

Imagine you've learned how to fill out a form on Amazon -- you know to type in a title, add a description, then click "Save." Now you go to GitHub and need to open an issue: same pattern, different labels and layout. SkillMigrator is a web-browsing AI that recognizes "hey, this page looks structurally similar to something I've done before" and reuses that saved recipe -- even across completely unrelated websites. This cuts down how many times it needs to "think" (call an expensive AI model) per task, making automation faster and cheaper without losing accuracy.

## TL;DR

SkillMigrator introduces **Transferable Interaction Patterns (TIPs)**, a memory unit that pairs each induced web skill with a structural sketch (accessibility-tree skeleton) of the page where it was validated. At inference, skills are retrieved via a hybrid score combining semantic text similarity and layout tree-edit-distance, then grounded to live page controls without any new LLM call. On WebArena and Mind2Web, this reduces the average LLM-action count on successful trajectories by 8--10% relative to state-of-the-art baselines at matched task success rate.

---

## Problem & Motivation

LLM web agents operate as tool callers -- each step reads a fresh page snapshot and emits one primitive action (click, fill, scroll). Long tasks require many sequential LLM calls, dominating latency and cost. Prior work wraps repeated primitives into *web skills* to shorten trajectories, but existing skill libraries retrieve candidates by instruction similarity or coarse site metadata. Because surface wording varies across sites while interaction structure stays consistent (e.g. "fill a form and submit" looks the same on Shopify, GitLab, and a forum), purely semantic retrieval under-reuses skills on held-out domains, leaving most of the possible step and token savings on the table.

---

## Main Original Ideas

1. **Transferable Interaction Pattern (TIP).** Each skill is stored as a 4-tuple `(ι, σ, Φ, τ)`: a natural-language intent `ι`, an operation template `σ` (e.g. *fill-and-submit*), a slot schema `Φ` (abstract slot names + synonym pools, no site-specific element refs), and an accessibility-tree skeleton `τ` recording the page structure at induction time. Removing concrete element refs makes the skill portable across sites that relabel their controls.

2. **Layout-conditioned retrieval.** Skills are scored by a convex combination of a text signal (cosine similarity of sentence embeddings over intent + slot descriptors) and a layout signal (1 − TED(τ_k, τ(o_{t-1})) / max(|τ_k|, |τ(o_{t-1})|)) computed via tree-edit distance between the stored skeleton and the live page. α = 0.6 weights text vs layout. This allows the agent to distinguish same-wording-different-structure pages from same-structure-different-wording pages.

3. **Two-stage slot binding.** Once the best-matching TIP passes a gate threshold β = 0.20, execution splits into Stage A (Hungarian-solve slot values from the task instruction's instantiation dict, with synonym-pool matching) and Stage B (Hungarian-solve slot-to-control bindings from the live page's interactive nodes). Any unbound required slot escalates back to the primitive policy, preventing silent failures.

4. **Gate-controlled fallback.** If `score(k*, s, o) < β`, the agent falls back to standard ReAct primitive generation rather than forcing a weakly matched skill. This preserves success rate while still capturing most reuse opportunities.

5. **Composition with existing libraries.** When the gate fails, control can route to a secondary skill library (ASI, PolySkill) rather than raw ReAct. The TIP retrieval layer behaves as an add-on over any existing skill-induction backend.

---

## Key Findings

### WebArena per-domain results (SR % / avg LLM-action count N̄)

| Method | Shop SR | Shop N̄ | Admin SR | Admin N̄ | Reddit SR | Reddit N̄ | GitLab SR | GitLab N̄ | Map SR | Map N̄ | Multi SR | Multi N̄ | Avg SR | Avg N̄ |
|--------|---------|--------|---------|--------|---------|--------|---------|--------|--------|-------|--------|--------|--------|-------|
| ReAct | 37.4 | 6.1 | 44.0 | 7.0 | 66.0 | 5.0 | 38.9 | 7.5 | 16.4 | 4.5 | 10.3 | 10.5 | 43.6 | 6.5 |
| SkillWeaver | 39.3 | 5.7 | 48.2 | 6.5 | 71.2 | 4.7 | 50.3 | 7.0 | 17.2 | 4.2 | 16.3 | 9.8 | 43.6 | 6.1 |
| ASI | 46.3 | 5.8 | 53.6 | 6.6 | 73.7 | 4.8 | 46.8 | 7.1 | 21.5 | 4.3 | 15.1 | 10.0 | 46.5 | 6.2 |
| PolySkill | 51.4 | 5.5 | 54.8 | 6.3 | 73.2 | 4.5 | 54.2 | 6.8 | 18.9 | 4.0 | 18.9 | 9.5 | **49.3** | 5.9 |
| **SkillMigrator** | 45.5 | **4.8** | 52.7 | **5.6** | 72.6 | **4.5** | 46.7 | **6.7** | 19.3 | **3.0** | 16.7 | **9.4** | 45.7 | **5.4** |

### Mind2Web generalisation splits (GPT-4.1, static library)

| Method | Cross-task SR | N̄ | \|K\| | Cross-website SR | N̄ | \|K\| | Cross-domain SR | N̄ | \|K\| | Reuse % |
|--------|--------------|---|-------|-----------------|---|-------|----------------|---|-------|---------|
| ReAct | 53.8 | 7.0 | -- | 56.2 | 7.5 | -- | 62.3 | 8.0 | -- | -- |
| ASI | 52.3 | 6.6 | 50 | 54.9 | 7.1 | 47 | 57.3 | 7.6 | 33 | 17.4 |
| PolySkill | 55.4 | 6.3 | 43 | 57.6 | 6.8 | 44 | 60.1 | 7.2 | 36 | 22.7 |
| **SkillMigrator** | 54.8 | **5.8** | **35** | 57.1 | **6.2** | **38** | 59.4 | **6.6** | **31** | **28.1** |
| PolySkill (+Update) | 63.2 | 6.0 | 47 | 61.3 | 6.5 | 53 | 63.4 | 6.9 | 56 | 31.0 |
| **SM (+Update)** | 62.7 | **5.5** | **41** | 60.5 | **5.9** | **47** | **63.0** | **6.2** | **49** | **35.4** |

- SkillMigrator achieves cross-domain reuse of **35.4%** vs PolySkill's 31.0% in +Update mode, with a smaller library (49 vs 56 skills).
- Hybrid **SkillMigrator + PolySkill** reaches N̄ = 5.3 (best on WebArena), SR = 47.7% -- the two libraries cover complementary slices.
- Claude-4 backbone: SR = **54.7%**, N̄ = **5.1** vs GPT-4.1 SR = 45.7%, N̄ = 5.4 (+9 SR points, gains ride on top of the retrieval design).

### Ablation (WebArena average / Mind2Web cross-domain)

| Variant | WA SR % | WA N̄ | M2W CD SR % | M2W CD N̄ |
|---------|---------|-------|------------|---------|
| Full SkillMigrator | **45.7** | 5.4 | **59.4** | **6.6** |
| text only (α=1) | 39.2 | 5.7 | 55.8 | 7.3 |
| no synonyms | 45.4 | 5.4 | 57.0 | 7.1 |
| no gate (β=0) | 45.3 | **4.7** | 57.8 | 6.3 |

Layout signal is the dominant component: removing it collapses SR by 6.5 points on WebArena. Removing synonyms hurts cross-domain most (−2.4 SR). The gate mainly trades off N̄ vs SR -- setting β=0 saves more LLM calls but costs accuracy.

---

## Suggestions & Future Directions

1. **Multimodal extension** -- current work uses text-only accessibility snapshots; pixel-space agents are explicitly left out of scope. Extending TIPs to visual/screenshot observations is an open direction.
2. **Better skeleton compression** -- the stored tree skeleton `τ` currently keeps role and name per node; richer structural signatures could improve layout matching for dynamic or heavily JS-rendered pages.
3. **Hierarchical skill organisation** -- skills are currently in a flat global library; hierarchical clustering could improve retrieval speed and precision at scale.
4. **Tighter integration with skill-induction systems** -- SkillMigrator currently wraps ASI/PolySkill as a fallback; a joint training objective could yield a tighter coupling.
5. **Evaluation beyond WebArena/Mind2Web** -- the benchmarks cover structured web apps; social-media, document-editing, and highly dynamic SPA environments remain untested.

---

## Authors & Institutions

Shiqi He (University of Michigan), Yue Cui (Alibaba Group), Feijie Wu (Purdue University), Xinyu Ma (McMaster University), Jiaheng Lu (University of Pennsylvania), Yaliang Li (Alibaba Group), Bolin Ding (Alibaba Group), Mosharaf Chowdhury (University of Michigan)
