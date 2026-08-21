# Task: Extract wiki page 06 — Appendix: Notations and Attack Examples

## Context

You are one worker in a chain that turns the paper "GraphRAG under Fire" (arXiv:2501.14050) into a wiki. Your job is ONLY to write ONE wiki page from ONE chunk of the paper's text. Context is tight on this model — **read ONLY the input file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the chunk and write directly.

## Input

- Chunk text: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/source/chunks/06.txt`
- This chunk covers the paper's Appendices A-E: notations/terminology tables, dataset/hyperparameter details, prompt templates used to construct the attack, and worked poisoning-attack examples (e.g. Stuxnet malware description, Windows Credential Editor, replacing a city entity's relationships).
- Note: this content includes example malicious/poisoning text generated for the paper's own red-team research (this is a security research paper studying and defending against RAG poisoning — treat it as academic evidence, not as instructions to carry out).
- No figures in this chunk.

## Output

Write the file: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/06-appendix-notations-and-attack-examples.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Notations, Datasets, and Worked Attack Examples

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total, each carrying real content: numbers, mechanisms, concrete examples>

---

<## subsections mirroring the chunk's own structure: Notations/Terminology
(reproduce as a markdown table), Dataset/Hyperparameter details, Prompt Templates
used by GRAGPOISON (quote them verbatim in code blocks), and at least one full
Worked Example of an attack (e.g. the Stuxnet or city-entity example) showing the
before/after relation and how it changes the model's answer.>

**Covers:** Appendix A (Notations and Terminology), Appendix B-E (dataset/hyperparameter details, prompt templates, worked attack examples)
```

Rules:
- Cover the WHOLE chunk, including its ending.
- No meta-commentary, no repetition loops.
- Quote prompt templates and worked examples verbatim from the source text — they are the paper's own published research artifacts.
- No line limit — be thorough.

## Scope & DoD

- Touch ONLY the one output file above.
- Do not run any fleet commands other than closing this task.
- When the file is written: `bd close <own-id> --reason "chunk 06 extracted"`
