# 14b consistency pass — fixes log (chapters 00–06)

## 00_setup.md
- Latency "10–60 s" → "20–60 s" (per-committed budget) in intro and Troubleshooting
- "79 handbook sections" → "12 handbook sections" (matches `data/handbook/`, 12 files)
- mermaid edge label `HTTP :11435` → `HTTP port 11435` (unquoted colon in text)
- exercise 2: made the cache-entry path glob literal/unambiguous (`<2-char prefix>/<40-hex-key>.json`)
- verified: all numbers (versions, 480/3355/2400 rows, 768 dim, batch ≤ 32, temperature/seed defaults) match committed files (`runs/00_findings.md`, `llm.py`, `check.py`); no "What landed in the results table" needed (not an experiment chapter); 283 lines, just under 300 — noted, not padded

## 01_concepts.md
- "3,300 pairwise human votes" → "3,355" (canonical count from `runs/06_findings.md`; earlier line already said "3.3K", now both agree)
- `## Next:` heading → bare `Next:` line (DoD requires a line starting with `Next:`)

## 02_system_under_test.md
- `## Next` heading → `Next:` line (DoD format)
- verified: 12 categories, triage/answer app names, trace counts (420 traces, 3355 votes ref) all match committed files; 300+ lines, in range

## 03_look_at_your_data.md
- `## Next` heading → `Next:` line (DoD format)
- verified: test-split labels 34 pass / 26 fail, top failure modes match `runs/03_findings.md`

## 04_code_graded_evals.md
- `## Next` heading → `Next:` line (DoD format)
- verified against `runs/results.md`: f1_macro 0.697, all_checks_pass 0.117 (7/60), auroc_embed 0.827, priority acc 0.533 — all match; 251 lines, just under 300 — noted, not padded

## 05_llm_as_judge.md
- no fixes needed: bare `Next:` line already present; TPR/TNR explained at first use (line 13); kappa explained; Likert AUROC 0.360 and per-mode kappa values match `runs/05_findings.md`/`runs/results.md`; 213 lines — below 300 min, noted per policy (not padded)

## 06_judges_under_the_microscope.md
- no fixes needed: bare `Next:` line already present; BT (Bradley–Terry) expanded at first use (line 137); 3,355 votes matches `runs/06_findings.md`; agreement 0.620, ρ = 0.714, 1,689 turn-1 votes all match committed files; 251 lines — below 300 min, noted (not padded)
