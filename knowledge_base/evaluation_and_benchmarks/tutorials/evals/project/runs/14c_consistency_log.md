# 14c — consistency pass log (chapters 07–13)

Per-chapter fix list. One line per fix. Numbers only changed to values present
in committed files (`results.md`, `07_findings.md`, `07a_findings.md`, `metrics.json`).

## 07_statistics.md
- power-conclusion: n=60 row said "reliably catch ~20-point-or-bigger + pairing" — contradicted by committed findings (`07_findings.md`, `07a_findings.md` §5: "smallest honest pass-rate change ~24–25 points"); 20-pt row is 93/arm (above 60). Rewrote punchline to the committed ~24–25-pt floor.
- "What landed" summary line: "reliable only for ≥ ~20-point gaps, and with pairing" → replaced with committed ~24–25-pt floor + pairing effect (388/arm → 236 pairs at 10-pt gap).
- Added per-method citation line: bootstrap (Efron & Tibshirani 1993; Miller 2024 arXiv 2411.00640).
- Added per-method citation line: Wilson interval (Wilson, 1927).
- Added per-method citation line: McNemar (McNemar, 1947).
- Added per-method citation line: Bonferroni / Benjamini-Hochberg (Bonferroni 1936; Benjamini & Hochberg 1995).
- Verified vs committed files (no change, numbers already traced): v1/v2 pass 0.70; paired diff 0.0 CI [-0.117, +0.117]; McNemar 7/7 p=1.0; Wilson 42/60 [0.575, 0.801] (recomputed matches); plain bootstrap [0.583, 0.817]; clustered [0.567, 0.833]; 6-check table p-values; 12 topics.
- Structure/abbrev/links checked: `# 07 —`, What you will learn, Troubleshooting table, Exercises, `Next:` → 08, results-table section present, bootstrap_ci/wilson_ci/paired_bootstrap/mcnemar funcs exist, Miller 2411.00640 citation present.

## 08_rag_evals.md
- `Next:` line was `[09 — (placeholder chapter)] — coming soon.` → replaced with real link `[09 — Hallucination detectors: five methods, one question](09_hallucination_detectors.md)` (title taken from ch-09 H1).
- Verified vs committed files (no change, numbers already traced): recall@2 0.842 CI [0.758, 0.917]; hit@2 0.917; precision@2 0.475; MRR 0.869; nDCG@2 0.838 (`metrics.json`); recall@k curve k=1..8 (recall 0.708→0.958, precision 0.800→0.142, hit 0.800→0.983); failure_split {18, 1, 17}; RAGAS 0.676 CI [0.590, 0.760]; DeepEval 0.987 CI [0.973, 0.998]; Spearman −0.234/+0.379/−0.239; AUROC 0.578/0.567/0.756 (label) and 0.578/0.520/0.571 (verdict); n=28 alignment; tkt-012 (0.250/1.000) and tkt-014 (0.222/1.000) counter-examples from `08_agreement.md`.
- Citations: RAGAS (Es et al. 2023, arXiv 2309.15217) present; DeepEval referenced by version.
- Structure: 468 lines, What-you-will-learn / Troubleshooting / Exercises / results table all present.

## 09_hallucination_detectors.md
- `Next:` line was `[10 — (placeholder chapter)] — coming soon.` → replaced with real link `[10 — Guardrails: refusing the unsafe ticket](10_guardrails.md)` (title taken from ch-10 H1).
- Verified vs committed files (no change, numbers already traced): HHEM AUROC 0.7581 F1 0.1702 recall 0.103 0.071s; LettuceDetect AUROC 0.7681 F1 0.6107 0.139s; NLI AUROC 0.4835 0.942s; SelfCheckGPT AUROC 0.412 (42 rows) 0.412 CI [0.300,0.624] 180 calls 3.14s; LLM judge F1 0.7692 AUROC 0.859 (70 rows) 100 calls 1.765s; helpdesk LettuceDetect 0.5469 / HHEM 0.3958, 12/60 positive; HHEM dev-threshold 0.973 recall 0.103; per-task F1 QA 0.735 / Summary 0.476; span token-F1 0.082 — all confirmed in `metrics.json`, `results.md` (rows 59–64), `09_findings.md`, `09_compare.md`.
- Citations: HHEM (Vectara 2024), LettuceDetect (Kovács & Recski 2025, arXiv 2502.17125), SelfCheckGPT (Manakul et al. 2023, arXiv 2303.08896), RAGTruth (Niu et al. 2024, arXiv 2401.00396) all present in "What you will learn" + each method's advantage table.
- Structure: 339 lines, What-you-will-learn / Troubleshooting / Exercises / results table all present; counter-example tickets (tkt-021 0.9993, tkt-047 0.9985, tkt-071 0.9978) trace to `09_findings.md`.
- `Next:` link fix (2 passes): first set to `10_guardrails.md` (wrong target — file does not exist); corrected to `[10 — Agent evals: grading what an agent did to your system, not what it said](10_agent_evals.md)`, the real ch-10 file/title. Task description said ch-10 = "guardrails/safety" but the actual repo chapter is agent evals — logged as a task-vs-repo discrepancy (task description was stale about chapter titles).

## 10_agent_evals.md
- Fixed 7 **broken line-splits** (long identifiers/words split mid-token across a newline — these broke markdown table rows and a `just` command): `forbidden_`+`actions` (line 186 table cell), `"d`+`one"` signal, `10`+`_agent_v1_pass_at_k` and `10`+`_agent_transcript_judge` (results-table cells), `out=10`+`_agent_v1` (a broken `just agent-grade` command), `temperature`+nl+backtick (troubleshooting table cell), `metrics.json`+nl+` (` (exercise 2 code path). All merged onto single lines.
- One self-introduced error caught and reverted: while fixing the s/item cell I first wrote `0.2862`; `results.md` row 23 confirms s/item is genuinely `28.62` (transcript judge ≈ 28.6 s/episode). Reverted to `28.62`.
- `Next:` was `[11 — (placeholder chapter)] — coming soon.` → real link `[11 — Model benchmarks: running GSM8K and IFEval yourself, and learning why the numbers move](11_model_benchmarks.md)` (title taken from ch-11 H1).
- Verified vs committed files (no change, numbers already traced): pass@3 0.85 (17/20) CI [0.70,1.00]; pass^3 0.75 (15/20) CI [0.55,0.90]; flaky t04/t10, never-pass t09/t14/t17; mean_steps 2.52, tool_error_rate 0.046, policy_violation_rate 0.15, per-episode pass 0.80 (48/60); transcript judge κ −0.24 (−0.2366, agreement 61.7%); multiturn pass@3 0.83 / pass^3 0.67, mean user turns 0.11; t01 trajectory (cancel O101, refund 120.0, fee 0.0) — all confirmed in `metrics.json`, `results.md` (rows 23–26), `10_findings.md`.
- Citations: Anthropic "Demystifying evals for AI agents" (2026) present in What-you-will-learn + grading section; τ-bench / Yao et al. 2024 present in pass@k section.
- Structure: 454 lines, What-you-will-learn / Troubleshooting / Exercises / results table / advantages (state-grade primary) all present.

## 11_model_benchmarks.md
- Fixed one **number transposition** at line 191: it read "GSM8K scores 0.46/0.74/0.00 and IFEval 0.82/0.14", but 0.74 is gemma4's *IFEval* score, not its GSM8K. Correct per `results.md` rows 30 and 35 (gemma4 gsm8k 0.06, ifeval 0.74; qwen gsm8k 0.46; tiny gsm8k 0.00) and the main score table (rows 97–102): **GSM8K = 0.46 / 0.06 / 0.00** (qwen/gemma4/110M), **IFEval = 0.82 / 0.74 / 0.14**. Rewrote to list both rows explicitly with model order.
- `Next:` was prose ("chapter 12 builds the *same* Northwind helpdesk eval as an Inspect AI `Task`…", no markdown link). Converted to the same `[title](file)` convention as ch-08–10, keeping the descriptive clause: `[12 — Inspect AI: turning chapters 05 and 11 into a proper eval framework](12_inspect_ai.md)` (target title = ch-12 H1).
- Verified every score against `results.md` (all match): qwen gsm8k 0.46 [0.32, 0.60]; qwen ifeval 0.82 [0.72, 0.92]; gemma4 gsm8k 0.06 [0.00, 0.14]; gemma4 ifeval 0.74 [0.62, 0.86]; tiny gsm8k 0.00 [0.00, 0.00]; tiny ifeval 0.14 [0.06, 0.24]; sensitivity variants 0.46/0.46/0.52/0.96; sensitivity summary range 0.50; "total s" column = s/item × 50 (368.8 = 7.376×50, 429.1 = 8.581×50, 110.4 = 2.208×50, 258.8 = 5.176×50, 23.2 = 0.464×50, 38.6 = 0.772×50).
- Verified stderr column against each `runs/<dir>/metrics.json` `details/harness_stderr`: qwen 0.0712 ✓, qwen ifeval 0.0549 ✓, gemma 0.0339 ✓, gemma ifeval 0.0627 ✓, tiny 0.0 ✓, tiny ifeval 0.0496 ✓.
- Verified prompt-sensitivity flips (29 of 50), p=0.001, CIs (−0.64/−0.36 for 0-shot/5-shot vs plain; −0.56/−0.30 for CoT vs plain), Josh example (gold 70000; 0-shot 80000 ✗; 5-shot None; CoT 800 ✗; plain 70000 ✓), and `bench.py` line refs (gsm8k_extract:84, harness_run:114, OPENAI_API_KEY:149, find_harness_output:160) — all present in findings/bench.py.
- Citations present: GSM8K (Cobbe 2110.14168), IFEval (Zhou 2311.07911), harness (Gao 2405.14782), Miller (2411.00640), GSM1k (Zhang 2405.00332), saturation 2602.16763, MMLU-Pro 2406.01574, HLE 2501.14249, Arena 2403.04132, judge audits 2606.19544 / 2607.08535 / 2512.22245.
- Structure: WYWL + Troubleshooting + Exercises + results table + Advantages/Disadvantages all present. **275 lines** — under the 300–500 target, but no broken splits and every section is present; per 14b "note, don't pad" rule, left as-is (no artificial length added).

## 12_inspect_ai.md
- `Next:` was bold `**Next:** chapter 13 — CI/CD for evals…` — two issues: (a) the bold `**` prefix breaks the bare-`Next:` convention used in ch-07–11, and (b) it was a prose-only pointer with no link. Fixed to bare `Next:` + the real ch-13 title link `[13 — Production: from scripts to a running system](13_production.md)` (target title taken from ch-13 H1), plus one line of ch-13 preview.
- Verified all results-table numbers against `results.md` rows 38–39 and `12_findings.md` / `12_reconcile.md`: helpdesk pass_rate 0.70 [0.583, 0.817], accuracy 0.60 [0.483, 0.733], Cohen's kappa 0.1549, code_checks mean 0.819, includes hit 0.0, GSM8K accuracy 0.96 [0.90, 1.00]. Reconciliation: 0/60 judge disagreements vs ch-05, 0/60 code-check disagreements vs ch-10, 0/50 GSM8K disagreements vs ch-11 — confirmed in reconcile tables ("Disagreements: 0 / 60", "0 / 50").
- Verified non-number facts: Inspect AI 0.3.263 (`12_findings.md` line 4), viewer port 7575 (line 104), cached-bridge zero-fresh-calls claim (line 41: 119 + 50 cache hits), `inspect_tasks.py` line references (71 bridge, 266 helpdesk_task, 368 gsm8k_task, 150 _mode_scores, 296 _gold_number) all present on those exact lines.
- Citations: none required as arXiv papers (ch-12 is a framework chapter) — Hamel Husain / UK-AISI named in prose; `UK AISI` + `inspect-ai MIT` both stated. OK.
- Structure: WYWL / Troubleshooting / Exercises / results table / Advantages-vs-Disadvantages table all present. **266 lines** — below 300 target; no broken splits, no TODO; 14b says note-don't-pad, so left as-is.

## 13_production.md
- No numeric fixes needed. Verified against `results.md` rows 40–41 (gate delta 0.0; monitor 0.00893 [0.0, 0.0264]), `13_findings.md` lines 22–26 (80 traces, 60/20 datasets, scores attached 80), lines 55–67 (pass 0.700→0.700, all_checks 0.1167→0.1333 drop −0.0167→−0.017, CI gate Δ=0, p=1.000, Decision PASS), lines 95–99 (112, 7 days, sample 0.2, alerts 0, pooled 0.0089, Wilson CI, HHEM daily sequence 0.933/0.889/0.881/0.928/0.782/0.933/0.889); `13_landscape.md` 8 tools present.
- One small consistency nit: line 153 has `0.117 → 0.133 (drop -0.017)` in the prose while the gate output block at lines 185–187 also has `0.117 → 0.133 (drop -0.017)` — both agree with findings (0.1167→0.1333, drop −0.0167; chapter rounds to 0.117/0.133). Left as-is, consistent.
- `**Next:** chapter 14 — …` on line 320 pointed to a **planned, not-yet-written** chapter (task 14d in `specs/TASK_14_INDEX_AND_CONSISTENCY.md`). Fixed the bold `**Next:` → bare `Next:` (matching ch-07–12), kept it as prose with no link and a "(planned; … not written yet)" qualifier, since target chapter 14 does not exist. No link added (per 14b "no link to non-existent files").
- Troubleshooting table present (4 rows: ClickHouse memory, `@observe` no-op, v4 `events_only` 404, port 3030 in-use) — matches the chapter's actual failure modes from `13_findings.md`.
- Exercises section present (2 exercises) — one about a `latency_pass` score, one about extending the gate with `recall@2`; both reference real files.
- Structure: WYWL / Troubleshooting / Exercises / landscape table / Advantages/Disadvantages all present. **320 lines** — in 300–500 range. Citations: Hamel Husain "Your AI Product Needs Evals" (2024) + arXiv refs in what-you-will-learn.

## Cross-chapter consistency (07–13)
- All 7 chapters now share the same Next-chain: `07 → 08 → 09 → 10 → 11 → 12 → 13 → (14: TODO, 14d)`. No `chapter 14` links are broken (ch-13 intentionally points to the planned 14d task).
- `**Next:**` vs `Next:` style: all of ch-07 through ch-13 now use bare `Next:`. Ch-07–12 add a markdown link to the next chapter's file; ch-13 has no link (target chapter 14 is not yet a file — prose only, per 14b "no link to non-existent files").
- No TODO / "placeholder" / "coming soon" strings in any of ch 07–13 (grep empty).
- 14b rule (300–500 lines) status: ch-07 360, ch-08 ?, ch-09 339, ch-10 454, ch-11 275, ch-12 266, ch-13 320. Two under — left per "no padding" policy.
- One open: ch-08 line count was not re-checked in 14c. Not a 14c issue (already committed in d2fc0dfe6 with a structure PASS); noted only.
