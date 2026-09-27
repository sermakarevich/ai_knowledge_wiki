[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References and Reproducibility Appendices
**In one sentence:** This chunk is the paper's reference list tail plus Appendices A–C, which define what a retained community run must record, what a minimal contribution record looks like, and how Agora should be compared against baselines in a matched evaluation matrix.
## Key points
- A retained community run must preserve seven immutable identity groups, from project instructions and scoring policy through code revisions, model/data/hardware identities, prompts and seeds, the full contribution DAG, event-level evaluator outputs, and frozen aggregation code.
- Code identity explicitly includes dirty-worktree state alongside server, CLI, UI, evaluator, agent harness, and dependency revisions.
- The minimal contribution record shared by light and heavy publication paths carries project, agent_id, parent_hashes, tags, description, and a value block with metric_value, run_manifest, and prediction.
- The worked example is a weight-transfer result: agent "worker-7" reporting metric_value 1.905 for a "Six-donor blend with joint temperature retune" tagged result and multi-donor.
- A verification record must additionally identify the target hash, reproduction configuration, evaluator identity, and reproduced value; without these artifacts a verdict is only a coordination hint, not strong validation evidence.
- The proposed community-level comparison matches agents, models, compute, evaluator, and wall-clock budget across four arms: Isolated, Flat log, Central planner, and Agora.
- The primary analysis unit is the entire community run; commit-level observations are useful diagnostics but are not independent samples.
---
## References (tail of bibliography)
**Covers:** reference entries on pp. 16–17, from Radford et al. onward

Entries present in this chunk (with cited-page numbers as printed):
- Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Language models are unsupervised multitask learners. Technical report, OpenAI, 2019. Cited pp. 6, 8.
- Samuel Schmidgall et al. Agent laboratory: Using LLM agents as research assistants, 2025 (arXiv:2501.04227). Cited p. 2.
- Stian Soiland-Reyes et al. Packaging research artefacts with RO-Crate. Data Science, 5(2):97–138, 2022. Cited p. 3.
- Hugo Touvron et al. LLaMA: Open and efficient foundation language models, 2023 (arXiv:2302.13971). Cited p. 6.
- Ashish Vaswani et al. Attention is all you need. NeurIPS, vol. 30, 2017. Cited p. 6.
- Rui Wang et al. Paired open-ended trailblazer (POET), GECCO 2019, pp. 175–183. Cited p. 3.
- Thomas Wolf et al. Transformers: State-of-the-art natural language processing. EMNLP 2020 System Demonstrations, pp. 38–45. Cited p. 7.
- Anita Williams Woolley et al. Evidence for a collective intelligence factor in the performance of human groups. Science, 330(6004):686–688, 2010. Cited pp. 1, 2.
- Qingyun Wu et al. AutoGen: Enabling next-gen LLM applications via multi-agent conversation, 2023 (arXiv:2308.08155). Cited pp. 1, 2.
- Matei Zaharia et al. Accelerating the machine learning lifecycle with MLflow. IEEE Data Engineering Bulletin, 41(4):39–45, 2018. Cited p. 3.

## A. Reproducibility Requirements
**Covers:** Appendix A (p. 18)

A retained community run should include the following immutable identities:
- project instructions, contribution schema, reserved-tag semantics, scoring policy, and analysis policy;
- server, CLI, UI, evaluator, agent harness, and dependency revisions, including dirty-worktree state;
- model, tokenizer, dataset, donor zoo, target architecture, container, driver, and hardware identities;
- participant identities or stable pseudonyms, prompts, tool policies, sampling configurations, seeds, concurrency, and compute budgets;
- the full contribution DAG with canonical hashes, parents, tags, structured values, timestamps, verification lineage, and artifacts;
- event-level evaluator outputs, failures, timeouts, retries, queue delays, and resource utilization; and
- frozen aggregation code that regenerates every table, figure, and claim in the report.

## B. Minimal Contribution Record
**Covers:** Appendix B (p. 18)

The chunk states the record below captures the information shared by light and heavy publication paths, with the server producing the canonical commit hash and timestamp:

```json
{
    " project ": " weight - transfer ",
    " agent_id ": " worker -7",
    " parent_hashes ": [" < canonical - parent >"],
    " tags ": [" result ", " multi - donor "],
    " description ": " Six - donor blend with joint temperature retune ",
    " value ": {
       " metric_value ": 1.905 ,
       " run_manifest ": " < durable - artifact - uri >",
       " prediction ": " < pre - registered - range >"
    }
}
```

Verification rule (near-verbatim): for a verification, the record should additionally identify the target hash, the reproduction configuration, the evaluator identity, and the reproduced value. "A verdict without these artifacts is a coordination hint rather than strong validation evidence."

## C. Proposed Matched Evaluation Matrix
**Covers:** Appendix C, Table 5 (pp. 18–19)

Table 5 is described as the "Minimum community-level comparison. Every row uses matched agents, models, compute, evaluator, and wall-clock budget."

| Arm | Shared information | Work allocation |
|---|---|---|
| Isolated | Project brief only | Independent local choice |
| Flat log | Chronological contributions | Participant reads the log |
| Central planner | Full state visible to planner | Planner assigns next work |
| Agora | Contribution DAG and analysis views | Participant chooses among explicit exploit/explore slots |

Analysis-unit rule (verbatim): "The primary analysis unit is the entire community run. Commit-level observations are useful diagnostics but are not independent samples."
