> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Discussion, Limitations, and Outlook
**In one sentence:** Unlike approaches treating tests as auxiliary inputs or evaluation metrics, the framework encodes TDD as a process-level constraint architecture whose explicit phase ordering, validation gating, and bounded repair improve stability and reproducibility but remain prompt-level, preliminary, and in need of repository-scale validation.
## Key points
- TDD is encoded as a process-level constraint architecture — phase ordering, validation gating, bounded repair, and state authority integrated into the generative loop — rather than as auxiliary test inputs or post-hoc evaluation metrics.
- Proposal generation is separated from state mutation and TDD principles are distributed across planner, generation, repair, and validation stages, reducing uncontrolled iteration and LLM-driven instability.
- Bounded repair loops plus deterministic validation gates improve reproducibility, while the structured TDD manifesto acts as a runtime constraint preserving behavioral safety during iterative synthesis.
- Current constraints are enforced primarily at the prompt level with only partial runtime verification, leaving full semantic compliance as future work.
- The bounded-autonomy model stabilizes execution but may limit exploration in complex refactoring scenarios, and scaling to large multi-module repositories with complex dependencies needs more advanced planning and invariant enforcement.
- Empirical validation is preliminary: explicit phase separation and validation gating appear to reduce unstable retry cycles versus baseline prompting, and test-first ordering with minimal implementation appears to limit speculative code and unnecessary feature expansion.
- Manifesto injection must be balanced against token constraints, a trade-off between governance strength and prompt compactness.
- Planned future work covers repository-scale industrial evaluation including CI/CD integration (stability, defect rates, reproducibility), configurable governance levels calibrated to project complexity, and auditable AI-assisted development for regulated domains.
---
## Positioning: process constraints, not auxiliary tests
Unlike approaches that treat tests as auxiliary inputs or evaluation metrics, this framework encodes TDD as a process-level constraint architecture. Phase ordering, validation gating, bounded repair, and state authority are integrated into the generative loop itself. As a result, the development discipline shapes the trajectory of model generation rather than being applied after the fact.
**Covers:** positioning vs. auxiliary-test baselines

> This design positions prompt engineering not merely as task phrasing but as a mechanism for encoding software engineering process invariants within AI-assisted development workflows.

## Benefits of explicit discipline encoding
The primary benefit of the AI-native TDD framework is the explicit encoding of development discipline within the generative workflow. By separating proposal generation from state mutation and enforcing phase-ordered execution, the system reduces uncontrolled iteration and mitigates instability common in LLM-driven development. TDD principles are distributed across planner, generation, repair, and validation stages, enabling process-level governance beyond prompt phrasing alone. Bounded repair loops and deterministic validation gates improve reproducibility, while the structured TDD manifesto operationalizes test-first development as a runtime constraint, preserving behavioral safety during iterative synthesis.
**Covers:** Discussion — claimed benefits

## Limitations
The current implementation has several limitations. Manifesto-derived constraints are primarily enforced at the prompt level, with only partial runtime verification, leaving full semantic compliance as future work. While the bounded autonomy model stabilizes execution, it may limit exploration in complex refactoring scenarios. Empirical validation remains preliminary, and broader cross-model and repository-scale evaluations are needed to assess the robustness. Additionally, scaling to large, multi-module repositories with complex dependencies will require more advanced planning and invariant enforcement mechanisms.
**Covers:** Discussion — limitations

## Preliminary findings and trade-offs
Initial experimentation suggests that explicit phase separation and validation gating reduce unstable retry cycles compared to baseline prompting. Enforcing test-first ordering and minimal implementation appears to limit speculative code generation and unnecessary feature expansion. However, manifesto injection must be carefully balanced against token constraints, highlighting a trade-off between governance strength and prompt compactness.
**Covers:** Discussion — preliminary findings

## Future work
Future work will evaluate AI-native TDD in repository-scale industrial settings, including CI/CD integration, to assess stability, defect rates, and reproducibility. We also plan to explore configurable governance levels that allow teams to calibrate strictness based on project complexity. The deterministic validation and bounded autonomy model may further support auditable AI-assisted development, particularly in regulated domains.
**Covers:** Discussion — future work

## Acknowledgments
This work has been supported by Business Finland (projects GENIUS (2545/31/2024) and ANSE (1822/31/2025)). We would also like to acknowledge the use of Google's Nano Banana Pro in generating the visualization for Figure 1.
**Covers:** Acknowledgments
