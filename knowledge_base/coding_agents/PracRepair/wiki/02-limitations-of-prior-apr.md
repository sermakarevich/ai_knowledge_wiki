> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Limitations of Prior APR
**In one sentence:** Existing LLM-based repair is still largely driven by static or retrieved context, error messages, and coarse-grained validation outcomes, missing the failure-execution and patch-validation dynamics that PracRepair targets with three mapped stages.
## Key points
- Prior repair processes are "still largely driven by static or retrieved context, error messages, and coarse-grained validation outcomes."
- They do not systematically exploit two dynamic information types: failure-execution dynamics (executed paths, runtime states, branch outcomes showing how the failure is triggered) and patch-validation dynamics (how a candidate patch changes behavior during validation).
- Without these signals, LLMs "may miss root causes or generate incomplete and overfitted fixes, especially for bugs whose root causes depend on runtime states and value evolution."
- C1: failure-execution dynamics are large and noisy — "Directly exposing complete traces to the LLM may overwhelm the repair context rather than help identify failure-relevant behavior."
- C2: raw static-dynamic context is not self-explanatory — the LLM must determine "which runtime states matter and how they relate to the faulty logic; otherwise, it may make incorrect behavioral inferences."
- C3: patch-validation dynamics are often underused — "frequently reduced to coarse validation outcomes, such as pass/fail results or error messages," leaving iterations without fine-grained evidence of what changed and why the patch still fails.
- PracRepair maps one stage to each challenge: (1) static-dynamic context construction for C1, (2) question-driven failure diagnosis for C2, (3) feedback-guided patch refinement for C3.
- Reported results: under GPT-3.5 PracRepair fixes 139 bugs on Defects4J V1.2 and 136 on V2.0; under GPT-4o 162 and 171 respectively, including "75 unique correct fixes achieved … with GPT-3.5 and 93 unique correct fixes under GPT-4o when compared with ReInFix."
---
## The gap: static-driven repair misses dynamics
PracRepair's premise is that current LLM-based APR has "not fully exploited three debugging practices that are widely used by developers: static-dynamic evidence gathering, question-driven failure diagnosis, and feedback-guided patch refinement."
The two missing dynamic signals are:
- Failure-execution dynamics: "reveal how the original failure is triggered through executed paths, runtime states, and branch outcomes."
- Patch-validation dynamics: "reveal how a candidate patch changes program behavior during validation."
**Covers:** gaps in static/retrieval-driven LLM repair approaches.
## Three challenges in leveraging dynamic information
- **C1: Failure-execution dynamics are large and noisy.** Complete traces overwhelm context rather than highlighting failure-relevant behavior.
- **C2: Raw static-dynamic context is not self-explanatory.** Even with traces available, the model needs to link runtime states to faulty logic or it makes "incorrect behavioral inferences."
- **C3: Patch-validation dynamics are often underused.** Reduced to pass/fail or error messages, they give "subsequent repair iterations without fine-grained evidence about what behavior has changed and why the current patch still fails."
**Covers:** gaps in static/retrieval-driven LLM repair approaches.
## PracRepair's mapped response
- (1) Static-dynamic context construction addresses C1 "by combining static program context with selectively organized execution traces collected from triggering test runs," indexing and structuring evidence through "a unified interface" for on-demand access to "relevant code context, call relationships, executed paths, and runtime states."
- (2) Question-driven failure diagnosis addresses C2 "by guiding the LLM to ask and answer targeted diagnostic questions about what happens during execution, why the failure occurs, and how the faulty logic should be corrected," progressively narrowing to "an explicit repair hypothesis."
- (3) Feedback-guided patch refinement addresses C3 "by extracting validation diagnostics, code diffs, and trace diffs from failed candidate patches, and feeding these patch-validation dynamics back into diagnosis for iterative refinement," avoiding "incomplete or overfitted fixes."
**Covers:** gaps in static/retrieval-driven LLM repair approaches.
## Claimed effectiveness and contributions
- "Performs strongly from single-line to multi-function bugs, with particularly notable advantages on more challenging cases."
- "Ablation studies further verify the effectiveness of all three stages, showing that these gains come from enriching repair with failure-aware information, question-driven diagnosis, and feedback-guided refinement."
- "Beyond Defects4J, PracRepair also generalizes well to RWB V1.0/V2.0 [27], achieving the best performance across multiple foundation models."
**Covers:** gaps in static/retrieval-driven LLM repair approaches.
