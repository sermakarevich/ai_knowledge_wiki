> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Related Work — Pipelines and Similar Code Fragments
**In one sentence:** The chunk positions PracRepair against prior repair pipelines that retrieve similar code fragments as repair ingredients, task-specific learning-based methods, and prompt-based / iterative / agent-based LLM repair, then concludes with PracRepair's static-dynamic, question-driven, feedback-guided design and future multi-language extension.
## Key points
- Prior pipelines retrieve similar code fragments as repair ingredients [51], [52].
- Beyond functional bugs, prior studies also address syntax errors, performance bugs, vulnerabilities, type errors, and build failures [53], [54].
- Early learning-based methods use machine learning to rank or prioritize candidate patches [55].
- More recent learning-based approaches adopt neural machine translation to directly transform buggy code into fixed code [56], [57], or predict tree-level / syntax-aware code transformations [58], [59].
- Some methods train repair-specific models on curated bug-fix datasets [19], [60], unlike LLM-based APR which uses general-purpose foundation models without explicit repair-specific training.
- Early LLM-based APR relies on prompt engineering for one-shot repair generating a candidate patch in a single interaction [24], [45], [61]; later methods add iterative repair with validation feedback across rounds [12], [25], [27]; agent-based methods let the LLM invoke external tools [26], [28].
- PracRepair differs by structuring repair around static-dynamic information integration, question-driven failure diagnosis, and feedback-guided patch refinement.
- Extensive experiments with state-of-the-art baselines, scenario-based analysis, and ablation studies show PracRepair consistently outperforms existing methods, with future work extending to more languages.
---
## Retrieval pipelines and bug scope
**Covers:** Covers positioning vs retrieval/augmented repair pipelines.

Prior work includes pipelines that "pipelines or retrieves similar code fragments as repair ingredients [51], [52]." Beyond functional bugs, the chunk lists additional targets: "syntax errors, performance bugs, vulnerabilities, type errors, and build failures [53], [54]."

## Learning-based approaches
Learning-based repair is described as increasingly data-driven: early methods "use machine learning to rank or prioritize candidate patches [55]"; more recent work adopts "neural machine translation models to directly transform buggy code into fixed code [56], [57]", designs "neural architectures that predict tree-level or syntax-aware code transformations [58], [59]", and trains "repair-specific models on curated bug-fix datasets [19], [60]". Verbatim contrast: "Unlike these task-specific learning approaches, recent LLM-based APR methods use general-purpose foundation models without explicit repair-specific training."

## LLM-based approaches
The chunk traces three LLM repair paradigms: (1) "prompt engineering to perform one-shot repair, where the model directly generates a candidate patch from buggy code and related inputs in a single interaction [24], [45], [61]"; (2) "iterative repair by repeatedly querying the LLM with validation feedback and refining patches across multiple rounds [12], [25], [27]"; (3) "agent-based approaches" that "allow[...] the LLM to invoke external tools during repair [26], [28]". Positioning quote: "Our work is most closely related to this line of research, but differs in that it is inspired by practical debugging behaviors and structures repair around static-dynamic information integration, question-driven failure diagnosis, and feedback-guided patch refinement."

## Conclusion included in chunk
Verbatim: "In this work, we present PRACREPAIR, a fully automated program repair framework inspired by real-world debugging practices. Specifically, PRACREPAIR constructs static and dynamic context, performs question-driven failure diagnosis to formulate explicit repair hypotheses, and iteratively refines candidate patches using validation feedback." Reported outcome: "Extensive experiments, including comparisons with state-of-the-art baselines, scenario-based analysis, and ablation studies, show that PRACREPAIR consistently outperforms existing methods." Interpretation: "These results suggest that developer-inspired debugging workflows can substantially improve APR effectiveness." Future work: "we plan to extend PRACREPAIR to more languages for stronger generalizability."
