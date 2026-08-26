> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Benchmark Design

**In one sentence:** Because every injected Agent Skill expands the prompt of every query, WebDev-Skills-Bench measures not just whether an agent solves a task but whether a matched Skill should have been injected at all, using 31 public Skills on Web-Bench's 50 projects / 1,000 tasks under four matched conditions (C0 no Skill, C1 target Skill, C2 length-matched irrelevant Skill, C3 component ablation) with a workspace-aware protocol that puts only SKILL.md in the prompt — and finds target injection is on net harmful (−1.3 to −4.2 pp Pass@2, +72% to +394% tokens) with gains in only 17–36% of (Skill, project) pairs.

## Key points

- Agent Skills are reusable procedural modules (Markdown + optional auxiliary scripts/references) injected into every prompt of a session; because they act as a persistent behavioral prior, a Skill's utility is a property of the (Skill, project, model) triple, not of the Skill itself.
- WebDev-Skills-Bench is a pre-deployment benchmark on 31 third-party WebDev Skills (none authored by the authors) over Web-Bench's 50 projects and 1,000 ordered tasks, with 117 "core" (Skill, project) routing pairs selected from 1,550 candidate pairs.
- Four matched conditions: C0 (no Skill, baseline), C1 (target Skill), C2 (length-matched irrelevant Skill within ±5% bytes), C3 (leave-one-out slice ablation of positive rules −Rp, anti-patterns −Rn, example code −X) — isolating content effect (C1−C2) from length effect (C2−C0).
- The workspace-aware injection protocol injects only SKILL.md into the prompt; auxiliary files (references/, examples/, scripts/) are mounted under `.skills/<skill-id>/` in the agent filesystem, so prompt length is determined by SKILL.md alone and the byte-matched C2 control is well defined even for multi-file Skills.
- Across four models (Claude Sonnet 4, GPT-5.1, DeepSeek-V4-flash, Qwen3-Coder-30B-A3B), C1 vs C0 yields negative mean ∆Pass@2 of −1.3 to −4.2 pp, lower Task Completion Depth, and +72% to +394% relative total-token cost, with gains in only 17–36% of (Skill, project) pairs.
- The C2 length-matched control splits the failure into two mechanisms: Sonnet 4 and Qwen3 Coder are length-distracted (an equally long irrelevant Skill reproduces most of the loss), while GPT-5.1 and DeepSeek-V4-flash are content-misled (length is neutral but content still lowers Pass@2 by 1.1–1.4 pp).
- Losses concentrate on easy early tasks where the model already holds a strong prior; per-pair Skill effects are nearly uncorrelated across models (Pearson |r| ≤ 0.12 on ∆Pass@2), so static cross-model Skill rankings transfer weakly.
- C3 ablation on helpful Skills shows cheap anti-pattern rules carry the most reliable benefit, while example code helps weaker models but hurts the strongest; the paper advocates length-matched controls and per-model audits as a minimum standard for Agent-Skill evaluation.

---

## Abstract — the benchmark question

Agent Skills are increasingly injected into coding-agent sessions to encode framework conventions, anti-patterns, and reusable tools. Since each injected Skill expands the prompt of every query, an effective benchmark must determine not only whether an agent can solve a task but whether the Skill **should have been injected at all**. The WebDev-Skills-Bench study covers 31 public WebDev Skills on 50 Web-Bench projects and 1,000 ordered tasks, compares four matched conditions (including a length-matched irrelevant control and leave-one-out component ablations), and — to isolate Skill effects from prompt-length artifacts — places only SKILL.md in the prompt while mounting auxiliary files into the agent workspace. Headline results: target injection reduces mean Pass@2 by 1.3% to 4.2%, lowers task completion depth, and increases token cost by 72% to 394%, with gains in only 17% to 36% of Skill-project pairs.

## Section 1 — Introduction

### Why WebDev and why now

- Every injected Skill enlarges the prompt of every query; when it does not help, the agent pays token and latency overhead with no reliability gain, sometimes a net loss.
- Web development is a natural focus: JavaScript/TypeScript and HTML/CSS account for a large share of LLM coding traffic and dominate developer activity (GitHub, Stack Overflow 2025), and WebDev-targeted Skills are widely published.
- Existing evidence is conflicting and indirect:
  - Native WebDev benchmarks (Web-Bench, ArtifactsBench) measure generation capability but never vary Skill injection.
  - Cross-domain Skill benchmarks disagree on direction: **SkillsBench reports +16.2 pp gain** over heterogeneous tasks, whereas **SWE-Skills-Bench finds 39 of 49 Skills yield zero pass-rate improvement** on SWE-bench-style problems.
  - None isolates WebDev, and none separates Skill content from the prompt-length increase injection introduces.

### The four conditions and the core protocol device

- C0 (no Skill), C1 (target Skill), C2 (length-matched irrelevant Skill separating content from prompt-length effects), C3 (leave-one-out slice ablation attributing a Skill's effect to positive rules, anti-patterns, and example code).
- Core device — workspace-aware injection protocol: only SKILL.md enters the prompt, while auxiliary files (references/, examples/, scripts/) are mounted into the agent's filesystem, so prompt length is determined by SKILL.md alone and the length-matched control is well defined even for multi-file Skills.

### Five controlled-study findings

1. On all four models, target injection produces a negative average ∆Pass@2 (−1.3 to −4.2 pp), lowers Task Completion Depth, raises token cost by 72–394%, and yields gains in only 17–36% of (Skill, project) pairs.
2. The C2 length-control splits the average into two mechanisms: Sonnet and Qwen are **length-distracted** (equally long irrelevant Skill reproduces most of the loss); GPT-5.1 and DeepSeek are **content-misled** (length neutral, but content still steers off-target).
3. The loss concentrates on **easy early tasks**, not challenging ones — injection is most costly where the model already holds a strong prior.
4. Per-pair Skill effects are nearly uncorrelated across models (cross-model Pearson |r| ≤ 0.12 on ∆Pass@2), limiting static cross-model recommendations.
5. C3 decomposition of a helpful Skill: cheap **anti-pattern rules** carry its most reliable benefit, while example code helps weaker models but hurts the strongest — making example-heavy Skills a poor default.

The benchmark, the injection harness, and all per-(model, condition, pair) outputs are open-sourced. The paper frames this as recasting injection as a **per-deployment routing decision** — find the beneficial minority before paying the injection cost — and argues length-matched controls and per-model audits should be a minimum standard for future Agent-Skill benchmarks.

## Section 2 — Related Work

| Area | Prior work | Gap this paper fills |
|---|---|---|
| Agent Skills as a prompting paradigm | Skills package procedural knowledge as prompt-readable Markdown + optional workspace resources (Anthropic, 2025b); distinct from RAG and few-shot prompting because the same content is injected for every query in a session (persistent behavioral prior) | Public marketplaces treat Skill quality as intrinsic to the Skill; this paper treats utility as a property of the (Skill, project, model) tuple |
| Skill benchmarks | SWE-Skills-Bench: 39 of 49 Skills with zero pass-rate improvement on SWE-bench-style tasks; SkillsBench: +16.2 pp gain over heterogeneous domains | Neither isolates WebDev; neither uses a length-matched irrelevant control to separate content from prompt-length effects. This paper holds the Web-Bench task harness fixed and varies only the Skill condition |
| WebDev benchmarks | Functional code generation: Web-Bench, ArtifactsBench, WebApp1K, WebGen-Bench; design/screenshot-to-code: Design2Code, WebSight, WebCode2M, Web2Code; autonomous web agents: WebArena, Mind2Web | All measure capability on a fixed prompt; isolating the marginal effect of a matched Skill is orthogonal to these efforts |

## Section 3 — Benchmark Design

### Task corpus and Skill suite

WebDev-Skills-Bench is a **pre-deployment** Skill benchmark: it uses reproducible project tasks as a proxy for production WebDev work and measures the **marginal effect of Skill injection** rather than absolute model capability.

- **Task corpus: Web-Bench** (Xu et al., 2025), chosen because among recent WebDev benchmarks it is not yet saturated by frontier models, relies on **deterministic Playwright tests** rather than LLM-as-judge scoring, and uses **sequentially dependent tasks** that expose long-horizon resilience.
- Scale: **50 projects across 11 stack categories** (React/Vue/Angular/Svelte front-ends, Express/Fastify back-ends, ORM/DB, CSS, Canvas/SVG/Three.js, bundlers, DOM apps), **20 ordered tasks per project = 1,000 tasks total**.
- **Skill suite: 31 third-party Skills** from prominent public repositories (Anthropic, Mindrally, Osmani, Vercel Labs); the authors authored none.
- Selection followed six principles: stack relevance, non-leakage, authoritative provenance, best-effort self-containedness, structural decomposability, and length coverage (SKILL.md files — the only text injected into the prompt — span roughly **1.2K–22K characters**, so the byte-matched C2 control has comparable-length substitutes across the range).
- The Skill manifest and the full **31 × 50 routing matrix** are in the supplementary material.

### Routing (Skill → project matching)

- Indiscriminate injection would mostly produce toolchain mismatches and dilute the utility signal.
- Two annotators (both authors, professional WebDev experience) independently judged each of the **1,550 (Skill, project) pairs** as **core** (the Skill's declared frameworks, libraries, or domain directly cover the project's primary stack) or **skip** (no meaningful overlap), at roughly 5 minutes per pair — about **129 hours per annotator (≈258 person-hours total)**.
- Agreement: **1,495 pairs** (raw agreement **96.5%**, Cohen's **κ ≈ 0.74**); the 55 disagreements were resolved by discussion, with any unreconcilable pair assigned **skip** to keep routing conservative.
- Result: **117 core pairs**, covering all 50 projects.

### Workspace-aware injection protocol

- Many Skills ship auxiliary assets alongside SKILL.md; concatenating them into the prompt would inflate length unequally and break the length-matched control.
- Protocol: inject **only SKILL.md**; mount the auxiliary directories into the agent's filesystem under `.skills/<skill-id>/`.
- Consequence: prompt length depends on SKILL.md alone, making the byte-matched C2 control tractable for any (including multi-file) Skill.

### The four matched conditions

All conditions hold fixed: project workspace, execution harness, task order, decoding settings, and Playwright test suite. The only intended variable is prompt-level SKILL.md content.

| Condition | Injection | Meaning / effect measured |
|---|---|---|
| **C0** (native baseline) | no Skill content | establishes intrinsic project difficulty; zero-point for all ∆P_k = P_k(C_x) − P_k(C0) |
| **C1** (target Skill) | core-matched Skill's SKILL.md | ∆Total = C1 − C0 = **gross utility** |
| **C2** (length-matched irrelevant Skill) | skip-tier Skill of ≈ equal byte length (**±5%**) | separates content from length: ∆Length = C2 − C0 and ∆Content = C1 − C2 |
| **C3** (leave-one-out slice ablation) | target SKILL.md minus one structural slice at a time: positive rules (−R_p), anti-patterns (−R_n), or example code (−X) | attributes ∆Total to components on a focused subset of helpful pairs (§4.5; slice definitions and per-pair protocol in Appendix D) |

**C0–C2 measure whether a Skill helps; C3 attributes which part of it does.**

### Models, protocol, and metrics

- **Four-model panel** spanning contrasts likely to modulate Skill utility: closed frontier (Claude Sonnet 4 — `claude-sonnet-4-20250514`, GPT-5.1) vs open-weight (DeepSeek-V4-flash, Qwen3-Coder-30B-A3B); general-purpose vs coding-specialized (Qwen3-Coder); larger vs smaller backends.
- Protocol: greedy decoding (temperature=0), 64k maxTokens budget, **N = 3 independent replicates per (model, condition, pair) cell** so within-condition variance is estimated uniformly; workspace reset (`git clean -fdx`) before every agent execution.
- All comparisons are **paired at the (Skill, project) level**.
- Metrics (each with 95% paired-bootstrap intervals, 1,000 resamples over the pair set):
  - mean **∆Pass@1** and **∆Pass@2**
  - mean **∆Task Completion Depth (TCD)** — the longest consecutive Pass@2 prefix in the 20-task chain
  - relative token overhead **ρ = (tokens_Cx − tokens_C0) / tokens_C0**

## C0/C1 effects at a glance (from Table 1)

Table: Model-level **C1 − C0** effects on the 117 core pairs (N = 3 per cell; brackets = 95% paired-bootstrap CIs; ρ = relative total-token overhead)

| Model | N | ∆P@1 (pp) | ∆P@2 (pp) | ∆TCD | Win/Tie/Loss (%) | ρ (tokens) |
|---|---|---|---|---|---|---|
| Claude Sonnet 4 | 3 | −2.8 [−4.6, −1.1] | −4.2 [−6.9, −1.9] | −0.85 | 30/9/61 | +72% |
| GPT-5.1 | 3 | −1.6 [−3.3, −0.1] | −1.3 [−3.4, +0.5] | −0.26 | 35/20/45 | +74% |
| Qwen3 Coder 30B | 3 | −3.2 [−4.3, −2.1] | −2.3 [−3.4, −1.3] | −0.47 | 17/35/48 | +91% |
| DeepSeek V4 Flash | 3 | −4.1 [−5.8, −2.2] | −2.0 [−3.8, −0.2] | −0.40 | 36/16/48 | +394% |

And by Web-Bench task difficulty (Table 2, ∆Pass@2, pp; bold = CI excludes zero; dash = fewer than five pair-cells):

| Model | easy | moderate | challenging |
|---|---|---|---|
| Sonnet 4 | **−5.3 [−10.0, −0.7]** | +3.3 [−2.7, +8.9] | −2.6 [−11.5, +6.4] |
| GPT-5.1 | **−4.0 [−7.8, −0.4]** | −7.5 [−23.3, +7.5] | +6.6 [−12.2, +22.7] |
| Qwen3 Coder 30B | **−10.7 [−16.7, −5.4]** | — | — |
| DeepSeek V4 Flash | **−7.3 [−14.6, −0.5]** | +11.7 [+0.4, +24.3] | +0.8 [−10.0, +10.4] |

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Work), Section 3 (Benchmark Design)
