---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: [2608.25218] TurnBench: A Multi-Domain Benchmark for Turn-Taking Dynamics in Spoken Dialogue

### Q1. What gap does TurnBench address, and what does it contribute?

> [!tip]- Answer
> Turn-taking evaluation lacks a consistent, linguistically grounded protocol plus hand-annotated data across diverse conversation types. TurnBench answers with a 30-hour hand-labeled corpus of dyadic human conversation paired with a standardized protocol for end-of-turn and interruption detection. Conversation type is treated as a controllable experimental variable over six distinct interaction styles. See [[wiki/01-electrical-engineering-and-systems-science-audio|Electrical Engineering and Systems Science > Audio and Speech Processing]].

### Q2. How is TurnBench listed on arXiv, and what are its publication details?

> [!tip]- Answer
> TurnBench is arXiv:2608.25218, listed under Audio and Speech Processing (eess.AS) and cross-listed as Computation and Language (cs.CL). The listing notes 8 pages, 2 figures, and acceptance to IEEE SLT 2026. Version v1 was submitted 25 Aug 2026 and v2, the camera-ready revision, on 16 Sep 2026. See [[wiki/01-electrical-engineering-and-systems-science-audio|Electrical Engineering and Systems Science > Audio and Speech Processing]].

### Q3. What are the corpus design choices that make conversation type an experimental variable?

> [!tip]- Answer
> The corpus covers six distinct interaction styles so that turn-taking behavior can be compared across conversation types under one protocol. Each conversation is triple-annotated to support reliable hand-labeled evaluation. The dyadic human-conversation design keeps the focus on two-speaker floor management decisions. See [[wiki/01-electrical-engineering-and-systems-science-audio|Electrical Engineering and Systems Science > Audio and Speech Processing]].

### Q4. What did benchmarking 14 heterogeneous systems reveal about end-of-turn recall versus interruption detection?

> [!tip]- Answer
> End-of-turn recall proved stable across conversation types, suggesting that turn-yield detection generalizes reasonably well. Interruption false positives, by contrast, were strongly type-dependent and concentrated in backchannel-dense interaction styles. This split implies interruption handling, not turn-end detection, is the domain-robustness bottleneck. See [[wiki/01-electrical-engineering-and-systems-science-audio|Electrical Engineering and Systems Science > Audio and Speech Processing]].

### Q5. What is the key human timing finding, and why does it matter for systems?

> [!tip]- Answer
> In smooth floor transfers, human listeners begin speaking a median 151 ms before the current turn ends, showing that natural takeovers overlap rather than wait for silence. No current system matches this anticipatory timing without incurring excessive false positives. The result sets a concrete human-parity bar: early entry with low false-alarm cost. See [[wiki/01-electrical-engineering-and-systems-science-audio|Electrical Engineering and Systems Science > Audio and Speech Processing]].

### Q6. What artifacts does the TurnBench release provide?

> [!tip]- Answer
> The release includes the 30-hour annotated corpus plus a larger 104-hour training set for building turn-taking models. It also provides a public leaderboard with an interactive dataset viewer for standardized comparison. Together these support reproducible benchmarking and error analysis across the six interaction styles. See [[wiki/01-electrical-engineering-and-systems-science-audio|Electrical Engineering and Systems Science > Audio and Speech Processing]].

### Q7. Your team is building a voice agent for backchannel-heavy casual chat — what should you prioritize and validate with TurnBench, and why?

> [!tip]- Answer
> Prioritize interruption precision over aggressive early entry, since false positives concentrate exactly in backchannel-dense styles like your target domain. Validate on TurnBench's backchannel-heavy interaction types and the interruption-detection split, holding end-of-turn recall steady while driving false positives down. I recommend this because the benchmark shows turn-end recall already generalizes, so your differentiating risk is mistaking backchannels for floor yields. See [[wiki/01-electrical-engineering-and-systems-science-audio|Electrical Engineering and Systems Science > Audio and Speech Processing]].
