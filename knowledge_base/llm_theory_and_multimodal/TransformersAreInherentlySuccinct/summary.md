# Transformers are Inherently Succinct

**Paper:** [Transformers are Inherently Succinct (Bergsträßer, Cotterell, Lin, 2026)](https://arxiv.org/abs/2510.19315)

## Human Readable TL;DR

Imagine you need to write instructions for a complex board game. A transformer can write those instructions in one short paragraph, while older rule systems (like finite automata or recurrent networks) would need entire books to say the same thing. This paper proves mathematically just *how* much more concise transformers are: exponentially more compact than recurrent networks and logic formulas, and doubly exponentially more compact than automaton-style rule tables. The downside of being so compact is that checking whether two transformers do the same thing becomes a nightmarishly hard problem -- it requires resources that grow doubly exponentially with the transformer's size.

## TL;DR

This paper introduces *succinctness* as a new lens for comparing neural architectures: instead of asking which languages a model can recognize, it asks how compactly each language can be described. The main result is that fixed-precision Unique-Hard Attention Transformers (UHATs) are exponentially more succinct than both Linear Temporal Logic (LTL) and RNNs, and doubly exponentially more succinct than finite automata. As a direct consequence, basic verification problems for UHATs (emptiness and equivalence) are EXPSPACE-complete -- no algorithm can solve them in less than doubly exponential time under standard assumptions.

---

## Problem & Motivation

Prior theoretical work established that fixed-precision transformers recognize only *subregular* languages, placing them below RNNs (which recognize all regular languages) in expressive capacity. Yet transformers dramatically outperform RNNs empirically, suggesting expressive capacity is an incomplete metric. The paper asks: can transformers describe the same languages *much more compactly* than competing formalisms, even if they can't describe strictly more of them? A secondary motivation is that succinctness directly implies computational hardness for verification -- a richer representation forces any decision procedure to unfold more underlying structure -- making succinctness a bridge between model architecture and formal analysis.

---

## Main Original Ideas

1. **Succinctness as an expressivity metric.** Rather than "what languages can a formalism recognize?", succinctness asks "how many symbols are needed to describe a given language within that formalism?". Greater succinctness implies harder decision problems; the paper formalizes this and applies it to transformers for the first time.

2. **Doubly exponential counters via attention.** The key technical engine: a UHAT of polynomial size can implement a binary counter that counts from 0 to 2^(2^N). This is achieved through a subtle encoding in the attention mechanism -- the attention operation can locate, in a single layer, the most recent position with the same counter value, enabling doubly-exponential time/space simulation in a linearly-growing network.

3. **EXPSPACE-hardness via tiling reduction.** The 2^N-tiling problem (EXPSPACE-complete) is encoded into a B-RASP program of polynomial size. B-RASP uses attention to enforce horizontal adjacency (tile-row transitions) and vertical adjacency (same-column, different-row constraints). A polynomial-time translation from this B-RASP class to UHATs transfers EXPSPACE-hardness.

4. **Exponential UHAT → LTL translation (improved upper bound).** By proving that all rational values arising in a UHAT's computation have at most polynomial bit-length (Proposition 12), the paper constructs an exponential-time translation from any UHAT to an equivalent LTL formula -- improving the prior doubly exponential translation of Yang et al. (2024).

5. **Succinctness hierarchy.** Using the same witness language family {L_n} (encodings of correct 2^N-tilings, whose shortest accepted word has length ≥ 2^(2^N)), the paper pins the three succinctness gaps simultaneously:
   - UHAT (poly-size) vs. LTL (needs exponential size) → exponential gap
   - UHAT (poly-size) vs. RNN (needs exponential size, since fixed-precision RNNs convert to automata with exponential state count) → exponential gap
   - UHAT (poly-size) vs. finite automaton (needs doubly exponential size) → doubly exponential gap

---

## Key Findings

| Result | Statement | Theorem |
|--------|-----------|---------|
| Non-emptiness complexity | EXPSPACE-complete for UHATs and B-RASP | Theorem 4 |
| UHAT vs. LTL succinctness | UHATs are exponentially more succinct than LTL | Theorem 15 |
| LTL → UHAT expansion | Polynomially bounded (LTL converts to UHAT in poly time) | Proposition 16 |
| UHAT vs. finite automata | UHATs are **doubly** exponentially more succinct | Theorem 17 |
| UHAT vs. RNNs | UHATs are exponentially more succinct | Corollary 18 |
| Equivalence complexity | EXPSPACE-complete for UHATs | Theorem 19 |
| Improved LTL translation | UHAT → LTL in exponential time (was doubly exponential) | Proposition 13 |
| Restricted UHATs (strict-future/rightmost) | Non-emptiness in NEXP (not EXPSPACE) | Corollary 14 |

- The witness family {L_n} consists of languages encoding valid 2^N-tiling solutions; L_n has a poly-size UHAT but requires exponential LTL formulas and doubly exponential automata.
- The key numerical fact: the smallest word in L_n has length ≥ 2^(2^N), which forces the automaton size lower bound directly (any automaton accepting a non-empty language must accept a word of length ≤ its state count).
- Previous best result (Sälzer et al., 2025): NEXP-hardness and singly-exponential succinctness over automata; this paper improves to EXPSPACE-complete and doubly-exponential succinctness.
- The gap between UHATs and LTL is asymmetric: UHATs are exponentially more succinct than LTL (lower bound), but LTL converts to UHATs in polynomial time (upper bound on the other direction).

---

## Suggestions & Future Directions

1. **Identify subclasses with tractable verification.** EXPSPACE-hardness requires transformers that encode large counters. The authors challenge researchers to characterize subclasses of UHATs that cannot encode such counters and thus admit lower-complexity verification algorithms.

2. **Transfer model-checking techniques.** Bring symbolic methods, simulation, abstraction, and other tools from classical model checking (Clarke et al., 2018) and the VNN competition tradition to bear on transformer verification in practice, despite worst-case intractability.

3. **Succinctness of softmax and average-hard attention transformers.** The current results are for UHATs; extending to fixed-precision softmax transformers (which UHATs overapproximate) and average-hard attention transformers is listed as explicit future work.

4. **Learnability of succinct transformers.** Does gradient descent actually learn the succinct representations that theory guarantees exist? Empirical evidence on length generalization is mixed (Garg et al., 2022; Naim et al., 2025; Huang et al., 2025); the theoretical succinctness bounds motivate a sharper theoretical treatment of learnability.

5. **Undecidability boundary.** Sälzer et al. (2026) showed that without positional encodings, verification becomes undecidable for average-hard-attention and softmax-attention transformers with finite but unbounded precision -- mapping where decidability ends is an open frontier.

---

## Authors & Institutions

Pascal Bergsträßer (RPTU Kaiserslautern-Landau, Germany), Ryan Cotterell (ETH Zürich, Switzerland), Anthony W. Lin (RPTU Kaiserslautern-Landau and MPI-SWS, Germany)
