# Skill-RAG: Failure-State-Aware Retrieval Augmentation via Hidden-State Probing and Skill Routing

**Paper:** [Skill-RAG: Failure-State-Aware Retrieval Augmentation via Hidden-State Probing and Skill Routing (Wei, Li, Zhu, Xue, Han, Niu, Yang, 2026)](https://arxiv.org/abs/2604.15771)

## Human Readable TL;DR

When a chatbot looks up information in a library and still can't answer your question, today's systems just send it back to the shelves and tell it to try again -- same question, same library, same shrug. This paper argues that repeated failures are almost never because the book is missing; they are because the question and the book shelf speak slightly different languages, and the *type* of mismatch matters. The authors add a tiny "mood reader" that peeks at the model's internal state to spot when it is stuck, then a "skill picker" that decides which trick to use next -- rephrase the question, break it into smaller ones, focus on the key evidence, or give up cleanly -- rather than blindly retrying.

## TL;DR

Skill-RAG reframes persistent retrieval failures in RAG pipelines as a **typed query-evidence alignment problem** rather than a "not enough retries" problem. It pairs (1) a lightweight hidden-state probe that gates retrieval at two pipeline stages and flags failure states, with (2) a prompt-based skill router that diagnoses the cause and dispatches one of four corrective skills -- query rewriting, question decomposition, evidence focusing, or a principled exit -- before the next generation attempt. Across multiple open-domain QA and multi-hop reasoning benchmarks, Skill-RAG substantially improves accuracy on hard cases that survive multi-turn retrieval, with especially strong gains on out-of-distribution datasets; representation-space analyses further show that the four skills occupy structured, separable regions of the failure manifold.

---

## Problem & Motivation

Adaptive-retrieval RAG systems have become competent at *deciding whether* to retrieve more context, but they remain crude about *what to do when retrieval has already failed*. The default fallback is to retry the same query or keep iterating, treating failure as transient noise. The authors observe that a large share of persistent failures are *not* caused by missing evidence in the corpus -- the right documents are often there -- but by a structural **alignment gap** between the way the user phrased the query and the way evidence is expressed. Treating that as a monolithic "retry" problem wastes compute and never addresses the root cause, so pipelines plateau precisely on the hard cases where grounding matters most.

---

## Main Original Ideas

1. **Failure-State-Aware Retrieval.** The paper reframes persistent retrieval failure as a *diagnosable state* rather than a signal to re-run. A decision step is inserted into the RAG loop that explicitly asks "why are we stuck?" before choosing what to do next, shifting the research question from "retrieve more" to "retrieve differently."

2. **Hidden-State Probe as a Lightweight Gate.** A small probe reads the LLM's hidden activations to detect alignment failure, gating retrieval at two points in the pipeline. Because the probe operates on representations the model already produces, it adds negligible overhead while giving the router a principled trigger signal.

3. **Prompt-Based Skill Router with Four Typed Skills.** Upon triggering, a skill router dispatches one of four corrective skills tailored to distinct failure modes: **query rewriting** (the query is vague or lexically off), **question decomposition** (the query is compound/multi-hop), **evidence focusing** (relevant context exists but is drowned out), and **exit** (the case is genuinely irreducible and further retries are wasteful).

4. **Typed View of Query-Evidence Misalignment.** Representation-space analysis shows the four skills occupy structured, separable regions of the failure state space, providing empirical support that misalignment is a *typed* phenomenon with identifiable sub-categories -- not a single blob to be handled with generic retries.

5. **A Principled Exit Skill.** Unlike most RAG literature that assumes more turns always help, Skill-RAG explicitly models "give up cleanly" as a first-class action, which both saves compute and prevents confident hallucination on unanswerable cases.

---

## Key Findings

- **Substantial gains on hard, persistent cases.** The biggest accuracy improvements concentrate on examples that continue to fail after multi-turn retrieval -- precisely the regime where naive retry-based adaptive RAG plateaus.
- **Strongest gains on out-of-distribution benchmarks.** Skill-RAG's advantage widens when the evaluation data is shifted from the training distribution, consistent with the claim that it is fixing structural misalignment rather than memorizing retrieval patterns.
- **Structured failure manifold.** Representation-space analyses show each of the four skills is deployed in its own separable region of hidden-state space, supporting the typed view of alignment failure.
- **Two-stage gating is load-bearing.** Placing the probe at two pipeline stages (rather than only post-retrieval) lets the router catch failures both before and after the retrieval step, enabling earlier course-correction.

---

## Suggestions & Future Directions

1. **Expand the skill library.** The four skills are a starting point; the typed view naturally invites additional skills for other identifiable failure modes (e.g., time-sensitivity, numeric reasoning, contradiction resolution).
2. **Learn the router end-to-end.** The current skill router is prompt-based; moving to a trained router could sharpen skill selection, especially on OOD data.
3. **Richer failure-state taxonomies.** The representation-space analysis hints at finer-grained sub-regions inside each skill's territory -- future work can formalize these into a failure ontology.
4. **Beyond open-domain QA.** Extending Skill-RAG to long-form generation, tool-augmented agents, and multi-modal retrieval is a natural next step since the probe/router pattern is architecture-agnostic.
5. **Cost-aware dispatch.** Each skill has different compute cost (decomposition is expensive, exit is free); learning to weigh skill cost against expected accuracy gain is an open optimization problem.

---

## Authors & Institutions

Kai Wei, Raymond Li, Xi Zhu, Zhaoqian Xue, Jiaojiao Han, Jingcheng Niu, Fan Yang -- first author based at Ann Arbor, Michigan (University of Michigan). Full affiliation list not disclosed in the public metadata.
