> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Fold Splits, Transfer Results, and End-to-End Experiment Details
**In one sentence:** Task-disjoint Fold 1 / Fold 2 splits (195 questions each) support distillation transfer evaluation where the student beats the base model (187 vs 117 both-presentations-correct of 390) and selects the supported fork candidate on 77 of 98 end-to-end forks across 41 held-out SWE-bench Pro tasks.
## Key points
- Each fold has 195 questions with identical parallel/detour splits (62/133), but different task counts (86 in Fold 1, 72 in Fold 2) and different per-repo mixes (e.g. ansible 29 vs 43, tutanota 21 vs 7).
- Transfer scoring presents each of the 390 questions in both orders and counts a question correct only when both presentations are answered correctly, with unparseable answers counted wrong.
- The student answers both presentations correctly on 187 questions vs 117 for the base model: +104 gained where the base is wrong, −34 lost where the base is right.
- On the training fold the gain from 48.6% to 92.9% has p ≈ 8 × 10−9, and Figure 7 intervals use item bootstrap with 4,000 draws as in Figure 3.
- Under the same scoring the student ranks below GPT-5.6 Sol (56.9%) and GPT-5.6 Terra (50.0%), equal to GLM-5.2 (47.9%), above Claude Opus 5 (46.7%), while the base model sits just below GPT-5.4 Nano (32.1%).
- For advice (one decision per question), summing log-odds over both presentations selects the supported candidate on 287/390 (student) vs 207/390 (base) — higher than accuracy because only the combined decision must be right.
- The end-to-end test uses 41 held-out SWE-bench Pro tasks (98 forks, 11 repos) with advice from the fold not containing the task; the executor is SWE-agent 1.1.0 with Qwen3.6-27B, and correct-advice gain over no advice has exact McNemar p ≤ 0.004.
- With student advice (supported candidate on 77/98 forks) the executor reaches 33.7% success, with per-task results in Table 12 (e.g. all 8 ansible tasks mostly correct; navidrome 8383527 0/2; element-web 494d9de 0/1).
---
## Fold 1 / Fold 2 question splits
**Covers:** chunk table "Fold 1 Fold 2 Questions 195"

| Row | Fold 1 | Fold 2 |
|---|---|---|
| Questions | 195 | 195 |
| Parallel / detour questions | 62 / 133 | 62 / 133 |
| Tasks | 86 | 72 |
| NodeBB | 11 | 2 |
| ansible | 29 | 43 |
| element-web | 16 | 12 |
| flipt | 15 | 13 |
| vuls | 10 | 12 |
| teleport | 11 | 11 |
| openlibrary | 38 | 35 |
| navidrome | 13 | 23 |
| webclients | 7 | 16 |
| qutebrowser | 24 | 21 |
| tutanota | 21 | 7 |

## G.3 Transfer results
**Covers:** Section 5.2 transfer scoring, Section 3.4 protocol, Figure 3 / Figure 7 placement

- "each of the 390 questions is presented in both orders, a question counts as correct only when both presentations are answered correctly, and a presentation without a parseable answer counts as wrong."
- Student: both presentations correct on 187 questions; base model: 117 questions.
- Relative to base: student correct where base is wrong on 104 questions; student wrong where base is correct on 34 questions.
- "On the training fold, the gain from 48.6% to 92.9% in Section 5.2 has p ≈ 8 × 10−9."
- "The 95% intervals of Figure 7 are computed by item bootstrap with 4,000 draws, as in Figure 3."
- Engineering ranking (Figure 3) placement: "below GPT-5.6 Sol (56.9%) and GPT-5.6 Terra (50.0%), equal to GLM-5.2 (47.9%), and above Claude Opus 5 (46.7%), while the base model is just below GPT-5.4 Nano (32.1%)."
- Advice decision rule: "For each question, we sum over the two presentations the log-odds that the student assigns to the two answer tokens, and we select the candidate that the sum favors."
- Under this rule: student selects supported candidate on 287 of 390; base model on 207 of 390; "higher than the accuracy above because the rule needs only the combined decision and not a correct answer on both presentations."

## H End-to-end experiment details: tasks and executor
**Covers:** 41 held-out tasks, 98 forks, executor config

- "The 41 held-out tasks are SWE-bench Pro tasks from which the pipeline of Section 3 mined at least one engineering question, and they cover 11 repositories: ansible (8), openlibrary (8), qutebrowser (6), vuls (4), tutanota (4), element-web (3), flipt (2), teleport (2), webclients (2), NodeBB (1), and navidrome (1)."
- "Together they contain 98 forks. For every task, the advice is written by the student trained on the fold that does not contain the task, so the student is never trained on the task."
- "Two tasks have forks from both constructions, and for these we use the forks of the parallel construction."
- Executor: "SWE-agent 1.1.0 with Qwen3.6-27B as the model, with thinking disabled, temperature 0.7, top-p 0.8, top-k 20, and presence penalty 1.5."
- Limits: "75 model calls, 600 seconds per command, and 4,800 seconds in total", run "in the official SWE-bench Pro container of the task."
- Success: "official SWE-bench Pro evaluation accepts its patch."
- "The gain of correct advice over no advice in Section 5.3 has an exact McNemar p ≤ 0.004."

## H Advice text: template and example note
**Covers:** advice header/note template plus Teleport example

- Placement: "placed before the problem statement in the first user message of the executor, followed by a heading and the original problem statement."
- Content: "one note per fork of the task, and each note contains the situation at the fork, the candidate to avoid, and the candidate to take, followed by a reminder that the note is not evidence about the current patch."
- Template header (verbatim): "# Task-specific pitfall notes (from prior runs on this exact task)"
- Template warnings (verbatim excerpts): "They are NOT evidence about YOUR patch. They describe other runs, not this one."; "Do not submit because your approach matches a passed route."; "SUBMISSION CONTRACT (mandatory): before you submit, you must (1) run the project's relevant tests or, if they cannot run, a focused check you construct yourself, (2) observe the actual output, and (3) fix and re-run until it passes or your budget runs out."
- Usage rule (verbatim gist): "Work on the task in your normal way. Do not spend actions searching the codebase for the situations below, and do not restructure your plan around them. Only if you find yourself already facing one of these decisions, use the note to avoid the known trap – then verify as usual."
- Note structure: "## Decision trap {n} [{construction}] (step {fork step})" with "### Situation where prior runs diverged", "### Known trap (this route produced a FAILING patch)", "### Route that avoided the trap in a prior run", plus "Reminder: choosing this route is not verification. After acting, produce your own evidence that the resulting behavior is correct."
- Example: "## Decision trap 1 [parallel] (step 79)" for Teleport HSM/KMS test config ('lib/auth/keystore/testhelpers.go', 'HSMTestConfig(t *testing.T) Config'); trap = "Keep the existing PKCS#11-specific alert assertion unchanged and limit the refactor to centralized configuration and availability plumbing."; route = "Review integration assertions for assumptions invalidated by the expanded backend selector. Replace the alert check that specifically expects "PKCS#11 HSM keys" with a backend-neutral assertion so the same test remains valid for KMS configurations."

## H Student advice and per-task decisions (Table 12)
**Covers:** 77/98 fork decisions, 33.7% success, Table 12

- "The student answers the taste question of every fork, and each note recommends the candidate that the student selects and marks the other candidate as the one to avoid."
- "Across the 41 tasks, the student selects the supported candidate on 77 of the 98 forks."
- "With student advice, the executor achieves the 33.7% success rate reported in Section 5.3."
- Table 12 (Task, Forks, Student correct): NodeBB (3c85b94) 1/1; ansible (0fd8871) 1/1; ansible (395e5e2) 4/4; ansible (7094849) 1/1; ansible (7765870) 3/2; ansible (be2c376) 3/3; ansible (cd9c4eb) 4/3; ansible (ea04e00) 7/6; ansible (ed6581e) 1/1; element-web (494d9de) 1/0; element-web (b7fea97) 1/1; element-web (ca8b1b0) 2/2; flipt (3ef34d1) 3/1; flipt (b22f5f0) 1/1; vuls (4c04acb) 2/2; vuls (abd8041) 1/1; vuls (dc49646) 2/2; vuls (e52fa8d) 1/1; teleport (6eaaf3a) 2/2; teleport (baeb269) 1/1; openlibrary (08ac40d) 3/3; openlibrary (3c48b4b) 3/1; openlibrary (3f580a5) 2/2; openlibrary (5899980) 3/3; openlibrary (6a117fa) 1/0; openlibrary (9cd47f4) 3/3; openlibrary (b4f7c18) 3/1; openlibrary (e010b2a) 1/1; navidrome (8383527) 2/0; webclients (01b519c) 3/3; webclients (4feccbc) 4/4; qutebrowser (1943fa0) 1/1; qutebrowser (2dd8966) 2/1; qutebrowser (9902914) 1/1; qutebrowser (996487c) 1/1; qutebrowser (a84ecfb) 5/4; qutebrowser (de4a1c1) 4/2; tutanota (09c2776) 3/1; tutanota (1e516e9) 4/4; tutanota (219bc8f) 3/2; tutanota (da4edb7) 4/3; Total 98/77.
