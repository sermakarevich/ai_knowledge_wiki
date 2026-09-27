# [2608.25218] TurnBench: A Multi-Domain Benchmark for Turn-Taking Dynamics in Spoken Dialogue

**Article:** [TurnBench: A Multi-Domain Benchmark for Turn-Taking Dynamics in Spoken Dialogue](https://doi.org/10.48550/arxiv.2608.25218) — arXiv, 25 Aug 2026

## Human Readable TL;DR

Natural conversation is like a dance where partners constantly sense when to step forward and when to hold back, and TurnBench is a judging panel that scores how well machines dance that dance. The authors recorded 30 hours of two-person conversations across six different styles and had every conversation labeled three times over, so disagreements about who spoke when could be ironed out. They then tested 14 different talking-and-listening systems and found that spotting the end of a turn works about equally well everywhere, while mistaking friendly little "uh-huh" noises for interruptions happens far more in chatty, backchannel-heavy styles. The sobering headline is that people smoothly start talking about 151 milliseconds before the other person finishes, and no current system can match that timing without constantly jumping the gun.

## TL;DR

TurnBench pairs a 30-hour hand-labeled corpus of dyadic human conversation with a standardized evaluation protocol for end-of-turn and interruption detection, using conversation type across six interaction styles as a controllable experimental variable with triple annotation per conversation. Benchmarking 14 heterogeneous turn-taking systems shows end-of-turn recall is stable across conversation types while interruption false positives are strongly type-dependent and concentrate in backchannel-dense styles. Although humans begin speaking a median 151 ms before the current turn ends in smooth floor transfers, no evaluated system matches that behavior without excessive false positives. The release includes the corpus, a 104-hour training set, and a public leaderboard with an interactive dataset viewer, and the paper (8 pages, 2 figures) was accepted to IEEE SLT 2026 with a camera-ready v2 on 16 Sep 2026.

---

## Problem & Motivation

Speakers in natural conversation take turns speaking and listening, deciding in real time when to take, hold, or yield the floor, yet turn-taking evaluation has remained limited by the lack of a consistent, linguistically grounded evaluation protocol and hand-annotated data covering diverse conversation types. Without shared data and a standard way to score the two core decisions of end-of-turn and interruption detection, results across systems are hard to compare and it is unclear whether a system that works in one conversational setting generalizes to others. TurnBench is motivated by this gap: it treats conversation type as a controllable experimental variable rather than background noise, so that robustness across interaction styles can be measured directly instead of assumed.

## Main Original Ideas

1. **Multi-domain turn-taking benchmark with paired corpus and protocol.** TurnBench combines a 30-hour hand-labeled corpus of dyadic human conversation with a standardized evaluation protocol for end-of-turn and interruption detection, giving the field a single consistent yardstick instead of scattered ad hoc evaluations.
2. **Conversation type as a controllable experimental variable.** Rather than pooling all dialogue together, the benchmark covers six distinct interaction styles and makes conversation type an explicit axis of analysis, so type-dependent effects such as backchannel-driven false positives can be isolated and studied.
3. **Triple-annotated hand-labeled corpus plus large training set and live infrastructure.** Each conversation is triple-annotated to ground the labels linguistically, and the release couples the 30-hour evaluation corpus with a 104-hour training set, a public leaderboard, and an interactive dataset viewer to support reproducible training and comparison.

## Key Findings

Benchmarking 14 heterogeneous turn-taking systems reveals a split picture in which end-of-turn recall is stable across conversation types while interruption false positives are strongly type-dependent and concentrated in backchannel-dense interaction styles. This means systems hold up reasonably well at recognizing when a turn is over regardless of setting, but they stumble when conversations are full of short listener signals, misreading engagement cues as attempts to grab the floor. The human reference point sharpens the challenge: in smooth floor transfers, human listeners begin speaking a median 151 ms before the current turn ends, effectively anticipating the handover, yet no current system performs equivalently without incurring excessive false positives. In other words, the timing precision that makes human turn-taking feel seamless remains out of reach for machines that try to match it with current approaches.

## Suggestions & Future Directions

The findings point toward building systems that can anticipate turn endings the way humans do, starting slightly early without tipping over into constant false interruptions. A natural priority is handling backchannel-dense interaction styles specifically, since that is where interruption false positives concentrate and where a one-size-fits-all detector evidently breaks down. The released artifacts directly support this work: the 104-hour training set enables training more robust and style-aware models, while the corpus, public leaderboard, and interactive dataset viewer provide the shared ground for iterating on linguistically grounded evaluation and tracking genuine progress across conversation types.

## Authors & Institutions

Freeman Jiang, Ramon Sanabria, Soham Deshmukh, Bandhav Veluri, Simon Michael Vuch Williams, Elliott K. Suen, Garreth Lee, Kevin Yoonho Choi, Takuya Umeki, Riku Kubo, Sathvik Udupa, Chien-yu Huang, Shih-Yun Shan Kuan, Zhuoyan Tao, Satyapriya Krishna, Sefik Emre Eskimez, Yu Tsao, Hung-yi Lee, Shinji Watanabe. Institutions were not specified in the wiki material used for this summary. The paper is listed under Audio and Speech Processing (eess.AS), cross-listed as Computation and Language (cs.CL), as arXiv:2608.25218 (v1 25 Aug 2026; v2 camera-ready 16 Sep 2026), accepted to IEEE SLT 2026.
