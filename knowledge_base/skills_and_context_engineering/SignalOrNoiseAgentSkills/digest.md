> [[index|Wiki]] | [[summary|Summary]]

# Signal or Noise? A Benchmark Study of Agent Skills in Web Development — Digest

The whole paper at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction-and-benchmark-design|Introduction and Benchmark Design]]

**In one sentence:** Because every injected Agent Skill expands the prompt of every query, WebDev-Skills-Bench measures not just whether an agent solves a task but whether a matched Skill should have been injected at all, using 31 public Skills on Web-Bench's 50 projects / 1,000 tasks under four matched conditions (C0 no Skill, C1 target Skill, C2 length-matched irrelevant Skill, C3 component ablation) with a workspace-aware protocol that puts only SKILL.md in the prompt — and finds target injection is on net harmful (−1.3 to −4.2 pp Pass@2, +72% to +394% tokens) with gains in only 17–36% of (Skill, project) pairs.

- Agent Skills are reusable procedural modules (Markdown + optional auxiliary scripts/references) injected into every prompt of a session; because they act as a persistent behavioral prior, a Skill's utility is a property of the (Skill, project, model) triple, not of the Skill itself.
- WebDev-Skills-Bench is a pre-deployment benchmark on 31 third-party WebDev Skills (none authored by the authors) over Web-Bench's 50 projects and 1,000 ordered tasks, with 117 "core" (Skill, project) routing pairs selected from 1,550 candidate pairs.
- Four matched conditions: C0 (no Skill, baseline), C1 (target Skill), C2 (length-matched irrelevant Skill within ±5% bytes), C3 (leave-one-out slice ablation of positive rules −Rp, anti-patterns −Rn, example code −X) — isolating content effect (C1−C2) from length effect (C2−C0).
- The workspace-aware injection protocol injects only SKILL.md into the prompt; auxiliary files (references/, examples/, scripts/) are mounted under `.skills/<skill-id>/` in the agent filesystem, so prompt length is determined by SKILL.md alone and the byte-matched C2 control is well defined even for multi-file Skills.
- Across four models (Claude Sonnet 4, GPT-5.1, DeepSeek-V4-flash, Qwen3-Coder-30B-A3B), C1 vs C0 yields negative mean ∆Pass@2 of −1.3 to −4.2 pp, lower Task Completion Depth, and +72% to +394% relative total-token cost, with gains in only 17–36% of (Skill, project) pairs.
- The C2 length-matched control splits the failure into two mechanisms: Sonnet 4 and Qwen3 Coder are length-distracted (an equally long irrelevant Skill reproduces most of the loss), while GPT-5.1 and DeepSeek-V4-flash are content-misled (length is neutral but content still lowers Pass@2 by 1.1–1.4 pp).
- Losses concentrate on easy early tasks where the model already holds a strong prior; per-pair Skill effects are nearly uncorrelated across models (Pearson |r| ≤ 0.12 on ∆Pass@2), so static cross-model Skill rankings transfer weakly.
- C3 ablation on helpful Skills shows cheap anti-pattern rules carry the most reliable benefit, while example code helps weaker models but hurts the strongest; the paper advocates length-matched controls and per-model audits as a minimum standard for Agent-Skill evaluation.

## 2. [[wiki/02-results-and-mechanisms|Results and Mechanisms]]

**In one sentence:** Average Skill injection is a net negative that pays for itself in tokens (+394% to +91% overhead), the harm concentrates on easy tasks the model already solves, the same aggregate loss splits into two distinct mechanisms (length distraction vs content misalignment) across models, per-pair effects decorrelate across models so no static Skill ranking transfers, and within genuinely helpful Skills, anti-pattern rules are the only directionally reliable and most cost-effective slice.

- Mean C1−C0 ∆Pass@2 is negative for all four models on the 117 core pairs: Sonnet 4 −4.2 pp, Qwen −2.3, DeepSeek −2.0, GPT-5.1 −1.3; Task Completion Depth falls in parallel (−0.85/−0.47/−0.40/−0.26), while token overhead ρ rises +72–+91% (three models) and +394% for DeepSeek.
- Despite negative means, every model has a positive-gain tail: GPT-5.1 wins on 35% of pairs, DeepSeek 36%, Sonnet 30%, Qwen only 17%.
- Easy-task degradation is large and significant on every model (CI excludes zero), from −4.0 pp (GPT-5.1) to −10.7 pp (Qwen); moderate/challenging buckets are noisy and show no consistent loss (DeepSeek even improves on moderate tasks).
- The length/content decomposition splits the panel: length distraction for Sonnet 4 (∆Length = −3.3 pp, ∆Content = −0.9) and Qwen (∆Length = −3.5, ∆Content = +1.2), content misalignment for GPT-5.1 (∆Length = −0.2, ∆Content = −1.1) and DeepSeek (∆Length = −0.6, ∆Content = −1.4).
- Survival of C1 wins after the length control: Sonnet 4 60%, Qwen 95%, GPT-5.1 71%, DeepSeek 64% — most individual wins stay content-positive even where the mean is length-driven.
- Cross-model Pearson correlations of per-pair ∆Pass@2 are all near zero (−0.08 to +0.12, mean ≈ 0.00; Spearman ≤ 0.16); 74% of pairs have at least one positive and one negative model sign, only 1% gain on all four models.
- Starkest counterexample: lowdb × database-optimizer (S14) — Sonnet 4 +33 pp, DeepSeek −22 pp, Qwen −22 pp, GPT-5.1 unchanged: a 55 pp swing on one core-tier pair.
- C3 slice ablation on five robustly positive (Skill, project) pairs (each +3.3 to +6.7 pp; complete Skill +5.1 pp): anti-patterns Rn are the only directionally reliable slice (p = 0.008, +3.1 pp pooled), rules Rp neutral (+0.0), examples X null (−0.7) yet costliest — removing X saves 34,482 input tokens per run (~22.7% of the SKILL.md budget); dropping Sonnet, examples flip to the strongest effect (+4.2 pp; DeepSeek +8.3, Qwen +3.7, GPT-5.1 +0.7, Sonnet −15.3).

## 3. [[wiki/03-implications-and-conclusion|Implications and Conclusion]]

**In one sentence:** Skill injection is a deployment routing decision rather than a configuration default — a Skill's value is a hypothesis about a specific (Skill, project, model) triple, and capturing it requires per-model, position-aware evaluation before paying the injection cost.

- Unconditional Skill injection is small-and-negative on every model while adding 72–394% token cost, so injection must be opt-in and crossed against an empirical utility threshold at the (model, project, possibly task-difficulty) level.
- Skill-induced degradation concentrates on easy initial tasks where the model already succeeds, so a reasonable heuristic is to skip the Skill on early tasks and inject only once error rates rise — contradicting the common practice of attaching Skills before any task begins.
- Per-pair Skill effects are near-uncorrelated across models, so marketplaces publishing a single ranking are of limited use; multi-model deployment needs per-model evaluation traces and rankings conditioned on the model backend.
- A useful marketplace listing should report model-conditioned utility, the target stack, prompt length, and whether the gain survives a length-matched control.
- Without the length-matched control (C2), the benchmark would have reported a uniform negative effect, missing that it actually combines a small positive tail with easy-task losses requiring opposite mitigations.
- The paper frames its contribution as methodological: a byte-matched control plus a slice ablation turn a single negative average into a mechanistic account, and these controls should become a default in Agent-Skill benchmarking.
- Seed spread across the three Sonnet replicates (4.4 pp for C0 Pass@2, 3.6 pp for C1) is comparable to the headline effect size, so pair-level estimates need caution even though model-level means are stable at N=3.
- A Skill is a hypothesis about a particular (Skill, project, model) triple, not a portable asset — capturing its value is a routing problem of finding the beneficial minority before paying its injection cost.

## 4. [[wiki/04-appendices-worked-examples|Appendices: Worked Examples and Protocol Detail]]

**In one sentence:** Concrete traces show that a single injected Skill can produce opposite per-pair outcomes — a retry lock-in loss (−15 pp), a content-driven win (+18 pp), and cross-model sign reversal — while the C3 slice-ablation protocol isolates anti-patterns (Rn) as the only reliably positive slice.

- **Retry lock-in (Appendix A):** On zustand × react-expert (S07), injecting the most stack-aligned Skill lowers Sonnet C0 Pass@2 from 55% to 40% (Δ = −15 pp), with the entire loss coming from a single seed: both conditions fail identically on task-4, but on the C1 retry the model renames the submit button to "Create Blog Post" (following the Skill's operation-restating naming rule), which still substring-collides with the `<h2>Create Blog</h2>` heading, so strict mode fails again and the chain terminates at task-4.
- **Content-driven win (Appendix B):** On pull-loading × js-dom-web-components (S31), the C0 baseline is 0% Pass@2 on all three seeds because an empty `<div id="noticeTxt">` has zero box dimensions and `toBeVisible()` fails; S31 raises it to 18% while the length-matched control returns to 0%, giving ΔContent = +18 pp — an order of magnitude above Sonnet's −0.9 pp model-level average, per-pair effects can far exceed the panel mean.
- **Cross-model sign reversal (Appendix C):** On lowdb × database-optimizer (S14) the same Skill content yields opposite-signed effects: Sonnet 4 +33 pp (33%→67%), GPT-5.1 −2 pp (22%→20%), DeepSeek −22 pp (42%→20%), Qwen −22 pp (22%→0%) — a 55 pp gap on one core-tier pair, and baseline difficulty does not explain it (DeepSeek has the strongest C0 baseline yet drops most).
- **C3 slice definitions (Appendix D):** Each SKILL.md is segmented into a meta/overview header (always retained so the prompt stays well-formed), positive rules Rp ("do" conventions), anti-patterns Rn ("don't" rules), and example code X (fenced code blocks); each ablation removes exactly one slice (−Rp, −Rn, −X), and only Skills with at least two removable slices are eligible.
- **Pair selection for C3:** Pairs were screened by two rules — the Skill must contain ≥2 cleanly removable slices (excluding svelte/S22 rules-only and backend-patterns/S15 examples-only) and the pair must gain (C1>C0) on at least two of four models; the five selected pairs (S13 on vite/svg-chart, S29 on webpack, S07 on fastify-react, S14 on sequelize) retain positive cross-model mean gains of +3.3 to +6.7 pp.
- **C3 statistics:** 5×3×3×4 = 180 ablation runs at N=3 seeds across all four models; the inference unit is the cell (model × project, N=20); per-slice contributions are tested with a Wilcoxon signed-rank test over cells with a 10,000-resample paired-bootstrap CI, corroborated by task-level McNemar tests on discordant counts.
- **Reported C3 p-values:** The pooled anti-pattern (Rn) contribution has McNemar discordants b=111, c=74 (p=0.008); excluding Sonnet, the example-code (X) contribution of +4.2 pp has Wilcoxon p=0.005 — the most significant slice effect in the panel.
- **Released artifacts (Appendix E):** Analysis code, routing for all conditions (C1 core, C2 length-matched, C3 candidate pairs), the 31 Skills with provenance, C3 slice definitions, and derived per-pair/per-task CSVs (C0–C3 values, pairwise Δs, per-slice C3 contributions, chain-position data, per-model rankings, seed-variance tables) are at https://anonymous.4open.science/r/webdev-skills-bench-1C32/; the raw evaluation reports and Web-Bench harness are omitted, so the release reproduces the analyses but not byte-for-byte trajectories.

## The argument in five moves

1. Agent Skills are injected persistently into every prompt of a session, so a proper benchmark must ask whether the Skill should have been injected at all, not just whether the agent can solve the task.
2. WebDev-Skills-Bench isolates that question with four matched conditions — a no-Skill baseline, the target Skill, a length-matched irrelevant Skill, and a leave-one-out slice ablation — run on 117 conservatively-routed (Skill, project) pairs across four models.
3. Target injection is net-harmful on every model on average (−1.3 to −4.2 pp Pass@2, +72–394% tokens), with gains in only 17–36% of pairs, and the harm concentrates on easy tasks via a "retry lock-in" mechanism that removes the model's usual self-repair flexibility.
4. The length-matched control splits that average into two distinct causes across models — pure prompt-length distraction (Sonnet, Qwen) vs actual content misalignment (GPT-5.1, DeepSeek) — which require opposite fixes (shorten the prompt vs review the content).
5. Per-pair effects barely correlate across models (|r| ≤ 0.12), so a Skill's value is a hypothesis about one specific (Skill, project, model) triple, not a portable, marketplace-rankable asset.
6. Within Skills that do help, a slice ablation shows cheap anti-pattern ("don't") rules carry the reliable signal, while example code is the costliest slice and actively hurts the strongest model even as it helps weaker ones.
7. The paper's proposed fix is procedural: treat injection as an opt-in, per-deployment routing decision, gated by chain position and a length-matched control, rather than a session-start default.
