> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Ablation on Repair Rounds and Budget Hyperparameters
**In one sentence:** This chunk reports hyperparameter sensitivity (debugging sessions, repair rounds, augmentation budget), a cost comparison where DebugRepair is cheapest per bug, threats-to-validity mitigations, related-work positioning, and the paper's conclusion.
## Key points
- Fig. 9(a) plots repair performance over Number of Debugging Sessions (Nsession, x-axis 1–10) for Repair Rounds Kround = 1 through 5 (y-axis 80–140 fixes).
- Fig. 9(b) plots Number of Correct Fixes (y-axis 160–240) over Augmentation Numbers (x-axis 0–20).
- DebugRepair uses 32 patches/bug, 38,000 tokens/bug, and $0.036 money/bug — the lowest cost on all three per-bug metrics in Table 8.
- Comparators in Table 8: ChatRepair 500 patches / 210,000 tokens / $0.42 (2024) or $0.14 (today's price); RepairAgent 117 / 270,000 / $0.14; TSAPR 32 / 40,000 / $0.06; ReinFix 45 / no token figure ("-") / $0.06.
- The chunk claims DebugRepair "achieves this superior cost-efficiency while simultaneously delivering a higher number of correct fixes, demonstrating the ability of the proposed framework to yield SOTA performance at a significantly lower budget."
- Construct-validity threat (subjective manual patch-correctness judgment) is mitigated by independent double-blind review by two researchers plus a third arbitrator on disagreement until consensus.
- Internal-validity threat (data leakage from LLM pretraining) is mitigated by evaluation on HumanEval-Java, released after GPT-3.5's training cutoff, with consistent gains attributed to design rather than memorization.
- External-validity threat (generalizability) is addressed via three benchmarks (Defects4J, QuixBugs, HumanEval-Java) across Java and Python; SWE-bench is intentionally excluded because its default setting denies APR tools explicit test cases, rendering DebugRepair inapplicable.
---
## Hyperparameter impact (Fig. 9)
Fig. 9, "Impact of hyper-parameter settings on the repair performance of DebugRepair," contains (a) "Repair performance under different Nsession and Kround settings" and (b) "Repair performance under different augmentation budgets." Axis ranges as extracted: (a) y-axis 80–140 with legend entries "Repair Rounds (Kround = 1)" through "Repair Rounds (Kround = 5)", x-axis "Number of Debugging Sessions (Nsession)" 1–10; (b) y-axis "Number of Correct Fixes" 160–240, x-axis "Augmentation Numbers" 0–20. No per-point numeric values are readable in the extracted chunk body.
## Cost comparison (Table 8)
Table 8. "Cost comparison between DebugRepair and existing APR approaches on Defects4J.":

| Approach | Patch/Bug | Token/Bug | Money/Bug |
|---|---|---|---|
| ChatRepair (2024) [38] | 500 | 210,000 | $0.42 |
| ChatRepair (today's price) | 500 | 210,000 | $0.14 |
| RepairAgent (2024) [4] | 117 | 270,000 | $0.14 |
| TSAPR (2025) [10] | 32 | 40,000 | $0.06 |
| ReinFix (2026) [48] | 45 | - | $0.06 |
| DebugRepair (Ours) | 32 | 38000 | $0.036 |

Table note (verbatim): "II '-' indicates no results reported in the original work, while the lowest cost on patch/token/money consumption per bug is highlighted in bold." Verbatim claim: "achieves this superior cost-efficiency while simultaneously delivering a higher number of correct fixes, demonstrating the ability of the proposed framework to yield SOTA performance at a significantly lower budget."
## Threats to Validity (Section 7)
- Construct: automated testing identifies plausible patches but semantic correctness needs manual inspection (human bias risk); mitigated by two researchers with extensive development backgrounds independently reviewing each plausible patch double-blind against the developer patch, with a third independent researcher arbitrating disagreements until consensus.
- Internal: backbone models pretrained on large-scale public code may have seen repair patterns/fixes; mitigated by evaluating on HumanEval-Java, whose release postdates GPT-3.5's training cutoff — consistent gains there suggest improvements come from DebugRepair's design rather than memorization.
- External: generalizability across datasets and languages; mitigated by evaluating on Defects4J, QuixBugs, and HumanEval-Java (differing bug characteristics/complexity) in both Java and Python; SWE-bench [17] deliberately excluded because it restricts APR tools from accessing explicit test cases by default, making DebugRepair inapplicable.
## Related Work (Section 8)
- APR goal stated verbatim in spirit: "automatically generate patches that fix software bugs, thereby reducing developers' manual debugging effort"; early paradigms: template-based, heuristic-based, constraint-based (e.g., TBar fix patterns; ExtractFix crash-constraint-guided synthesis via symbolic execution) — limited by patch diversity and generality on semantically complex bugs.
- Learning-based shift: NMT-based (repair as code-to-code translation) and PLM-based (large-scale pretraining; e.g., SelfAPR self-supervised execution diagnostics; FitRepair fine-tuning/prompting for fix ingredients) — still reliant on historical fixes, weak on failure-specific execution semantics.
- LLM-based paradigms: (1) retrieval-based (RepairAgent, ReinFix — external fragments/ingredients/history); (2) feedback-based — ChatRepair and ContrastRepair refine candidates directly via execution feedback, while TSAPR [11] feeds it into Monte Carlo Tree Search; (3) hybrid (ThinkRepair two-phase knowledge-pool + few-shot selection, optionally with test-failure feedback).
- Common limitation (verbatim): "Most approaches rely on source code and outcome-level failure symptoms, i.e., stack traces. Although useful for identifying the manifestation of a bug, these signals are often too coarse to expose the intermediate runtime states that directly reveal its root cause. As a result, LLMs may generate plausible yet semantically incorrect patches that only mask symptoms." Concurrent InspectCoder [33] shares the debugging philosophy but uses natural-language task descriptions as specifications — a setting differing from mainstream real-world APR, so it is excluded from comparison; DebugRepair instead combines "test semantic purification, simulated instrumentation, and debugging-driven conversational repair."
## Conclusion (Section 9)
Verbatim: "In this paper, we propose DebugRepair, a novel LLM-based APR framework that enhances repair effectiveness via self-directed debugging. Unlike existing feedback-based APR approaches that mainly rely on outcome-level failure symptoms, DebugRepair equips LLMs with runtime-state evidence through three components, namely test semantic purification, simulated instrumentation, and debugging-driven conversational repair. Experimental results on Defects4J, QuixBugs, and HumanEval-Java show that DebugRepair consistently outperforms existing SOTA baselines across different backbone LLMs, while ablation studies further confirm the effectiveness of all components in the framework." Acknowledgments list NSFC grants 62502283 and U24B20149, Shandong NSF grant ZR2024QF093, and Shandong Young Talent grant SDAST2025QTB031.
**Covers:** Fig. 9(a)–(b) hyperparameter plots + cost-efficiency paragraph, Table 8, Sections 7 (Threats to Validity), 8 (Related Work), 9 (Conclusion) with Acknowledgments.
