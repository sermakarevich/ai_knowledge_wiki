# A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty

**Paper:** [A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty (Lin, Li, Chen, 2026)](https://arxiv.org/abs/2604.16548)

## Human Readable TL;DR

Imagine an AI assistant that remembers everything you've ever told it -- your preferences, past conversations, decisions made. Now imagine someone sneaking in and quietly rewriting those memories to make the AI behave differently, or stealing private details from what it remembers. This survey is a comprehensive look at all the ways an AI's "long-term memory" can be attacked, tampered with, or misused -- and what gaps still exist in protecting it. The authors argue that AI systems need not just good recall, but true ownership and control over their own memory, calling this "mnemonic sovereignty."

## TL;DR

This survey examines the emerging security domain of persistent, writable long-term memory in LLM agents, arguing it constitutes an independent class of security problems distinct from prompt injection or training data leakage. The authors propose a six-phase memory lifecycle framework (Write, Store, Retrieve, Execute, Share, Forget/Rollback) cross-tabulated against four security objectives (integrity, confidentiality, availability, governance), covering ~70 primary works from 2023--2026. Three core findings emerge: (1) literature concentrates on write/retrieve integrity attacks while confidentiality, availability, store/forget phases, and benign failures are understudied; (2) no published architecture covers all nine governance primitives the authors identify; (3) LLM-driven automated red-teaming of memory defenses is critically absent. The unifying concept is "mnemonic sovereignty" -- a system's verifiable, recoverable governance over its memory state.

---

## Problem & Motivation

LLM agents are evolving from stateless tools into autonomous systems with persistent, cross-session memory. This introduces three qualitatively new security properties absent from single-session systems:

1. **Persistence** -- malicious content absorbed into memory can influence behavior across many future sessions, unlike one-shot prompt injection.
2. **Statefulness** -- subtle accumulated biases can cause gradual behavioral drift before any single entry triggers safety mechanisms.
3. **Propagation** -- in multi-agent or shared-memory environments, contamination can cascade across session, role, and user boundaries.

Existing surveys address memory architectures or agent designs, but few treat the epistemic and governance properties of persistent, writable memory as the foundational reason memory is an independent security domain. This survey addresses that narrower gap by drawing on cognitive neuroscience (source-monitoring errors, reconsolidation, social contagion) as structural analogies for design requirements -- not mechanistic claims.

---

## Main Original Ideas

1. **Memory-Lifecycle Security Framework** -- A six-phase framework (Write, Store, Retrieve, Execute, Share, Forget/Rollback) cross-tabulated with four security objectives (integrity, confidentiality, availability, governance) provides a systematic backbone for literature organization and gap identification.

2. **Mnemonic Sovereignty** -- A normative concept unifying memory security: a system's verifiable, recoverable governance over what may be written, who may read, when updates are authorized, and which states may be forgotten. Future agents will be differentiated by memory governance quality, not just recall capacity.

3. **Nine Architectural Governance Primitives** -- P1: Memory unit abstraction; P2: Write gate; P3: Provenance metadata; P4: Versioning; P5: Trust/sensitivity labels; P6: Principal scoping; P7: Rollback; P8: Deletion semantics; P9: Internal-channel observability. Comparative analysis across six architectures (MemGPT, MemoryBank, Mem0, MemOS, Collaborative Memory, CoALA) finds none covers all nine.

4. **Five Testable Sovereignty Primitives** -- A dependency tower (Write Authorization -> Provenance Visibility -> Principal-Scoped Retrieval -> Rollbackability -> Verified Forgetting) where each higher layer requires the lower ones. Currently, only the foundation (write authorization) is widely implemented; verified forgetting has no peer-reviewed end-to-end instantiation.

5. **Cognitive-Neuroscience Bridge as Design Pressure** -- Five structural correspondences between human memory mechanisms and LLM agent vulnerabilities (source-monitoring / provenance failure; reconsolidation / read-time rewriting; social contagion / shared-memory contamination; confidence calibration / poisoned confidence; episodic compression / lineage erosion) generate concrete design requirements without claiming biological equivalence.

6. **LLM-as-Tool for Memory Security** -- Identifying that using LLMs for automated red-teaming, defense verification, and counterfactual stress-testing of memory systems is a critically sparse but essential research direction.

---

## Key Findings

### Literature Distribution by Lifecycle Phase

| Phase | Approximate Share | Notes |
|-------|------------------|-------|
| Write (integrity attacks) | ~30% | Most studied; includes MINJA, InjecMEM, eTAMP, MemoryGraft |
| Retrieve (integrity/hijacking) | ~25% | Memory Control Flow Attacks (MCFA), retrieval steering |
| Share/Propagation | ~15% | Multi-agent contamination, cross-session persistence |
| Store/Manage | ~5% | Compression amplification, provenance erosion -- understudied |
| Forget/Rollback | ~5% | Verified deletion, rollback semantics -- understudied |
| Confidentiality / Availability | ~20% | MEXTRA extraction, embedding inversion, sparse availability studies |

### Attack Progression on Write Path
- Attacker privilege has decreased over time: direct DB access -> query-only injection (MINJA, InjecMEM) -> environment-only influence (eTAMP)
- Poisoning targets expanded: factual knowledge -> procedural experience (MemoryGraft) -> graph relations (GraphRAG under Fire)
- RAG corpus poisoning achieves high success rates with minimal poisoned content; standard defenses largely ineffective (PoisonedRAG)

### Control-Flow Hijacking
- Memory Control Flow Attacks (MCFA): retrieved memory overrides user instructions to dictate tool invocation order and arguments -- shifting the problem from data integrity to control-flow integrity
- Corroborated end-to-end chain: external content absorbed -> summarized -> persisted -> retrieved later -> silently steers tool use

### Governance Architecture Gaps
- All six surveyed architectures (MemGPT, MemoryBank, Mem0, MemOS, Collaborative Memory, CoALA) lack write-gate validation and robust post-deletion verification
- Metadata-bearing designs (MemOS, Collaborative Memory) show greater governance potential but remain largely untested adversarially

### Defense Evaluation Gaps
- Every memory defense surveyed has been evaluated only against non-adaptive or weakly adaptive attacks
- Nasr et al. [2025] showed 12 recent prompt-injection defenses with near-zero static-attack bypass rates are defeated >90% by adaptive attackers -- the same gap exists for memory defenses

### Benign-Persistence Failures (non-adversarial)
- Silent cross-user contamination, over-application of profile facts, memory-induced sycophancy
- Arise from ordinary memory operation, not explicit attackers -- span multiple lifecycle phases

---

## Suggestions & Future Directions

1. **Lifecycle-wide benchmark (R1 -- highest priority)** -- A benchmark covering all six phases and four objectives under both adversarial and benign-persistence conditions; currently absent, would immediately anchor the field.

2. **LLM-driven memory red-teaming pipeline (R2)** -- Automated adaptive attacker LLMs targeting write gates, retrieval policies, and reflection loops, evaluated following Nasr et al. [2025] methodology.

3. **Cross-substrate verified deletion (R3)** -- A protocol coordinating deletion across raw logs, summaries, retrieval indices, and model weights, with post-deletion verification (formalized via Hoeffding-bound reappearance testing: ~300 probes for epsilon=0.01 at 95% confidence).

4. **Adversarial evaluation of governance-first architectures (R4)** -- Stress-testing of structured-metadata systems (MemOS-like designs) against the known attack catalog.

5. **Benign-persistence benchmarks (R5)** -- Systematic evaluation of cross-user contamination, over-application of profile memory, context-integrity violations, and memory-induced sycophancy as primary security properties.

6. **Policy-technical tensions** -- The tension between audit retention and right-to-forget cannot be resolved architecturally alone; different jurisdictions will require different resolutions.

7. **Governance overhead costing** -- No study has measured latency, storage, and compute costs of provenance metadata, versioning, and per-write policy evaluation; this data is needed to assess deployability of governance-first designs.

---

## Authors & Institutions

Zehao Lin (MemTensor, Shanghai, China), Chunyu Li (MemTensor, Shanghai, China), Kai Chen (MemTensor, Shanghai, China)
