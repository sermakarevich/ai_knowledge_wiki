# Plan — Just-in-Time Memory: Learning to Curate Task-Adaptive Memory for LLM Agents

Source: https://arxiv.org/pdf/2609.27334 (pdf, via pdftotext)
Run dir: /Users/sergii/.fleet/workflows/summarise/wfr-0c6xtl7b

| Chunk slug | Planned wiki page | Covers |
|---|---|---|
| 01-preprint-salesforce-ai-research-just-in-time | 01-introduction-and-problem.md | Covers paper framing: write-time vs read-time (just-in-time) curation problem and contributions |
| 02-providing-another-with-an-object-placement-strat | 02-background-and-related-work.md | Covers background/motivation tail and related write-time memory work |
| 03-1-retrieve-t-r-xt | 03-method-retrieve-curate-execute.md | Covers JITMEM method: retrieve raw trajectories, curate task-adaptive payload, execute, GRPO training |
| 04-table-1-results-on-alfworld-and | 04-main-results-alfworld-webshop.md | Covers main results table on ALFWorld/WebShop across executors |
| 05-write-time-distillation-discards-information-the | 05-ablations-and-analysis.md | Covers ablations: write-time distillation loss, task-adaptivity, storage filtering, bank refresh |
| 06-zichen-liu-changyu-chen-wenjun-li | 06-references.md | Covers reference list tail (author-block chunk) |
| 07-prior-to-this-step-you-have | 07-appendix-prompts-a.md | Covers appendix: curator/executor prompt details |
| 08-hyperparameter-value-optimization-base-policy-cu | 08-appendix-training-setup.md | Covers appendix: hyperparameters and optimization/training setup |
| 09-example-payloads-below-we-show-one | 09-appendix-example-payloads.md | Covers appendix: example curated payloads |
