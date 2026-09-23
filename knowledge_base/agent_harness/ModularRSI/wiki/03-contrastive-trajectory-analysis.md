[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Contrastive Trajectory Analysis and Trajectory Memory
**In one sentence:** Historical trajectories stored per task across epochs supply contrastive evidence for the Code-Modify Agent's group-wise diagnosis, whose consolidated JSON findings then drive voted, history-aware module modifications gated by validation, cross-module integration, library management, and a 2,000-instance evolution set.
## Key points
- Trajectory Memory stores historical trajectories and their rewards for each task across evolution epochs, supplying extra contrastive evidence when current rollouts alone are insufficient.
- For the Contrastive group, successful and failed trajectories of the same task are paired and compared to identify function-level factors tied to different outcomes.
- For the Negative group (all current rollouts fail), the agent queries Trajectory Memory for a prior success on the same task and pairs it contrastively if found, otherwise performs single-sided diagnosis of deficiencies such as repetitive loops, incorrect tool usage, ineffective recovery, or premature termination.
- For the Positive group (all rollouts succeed), analysis targets execution quality and efficiency such as redundant actions, repetitive exploration, or unnecessary tool calls.
- Modification Target Selection consolidates semantically similar diagnoses on the same function into candidates with a vote count from distinct supporting tasks, prioritizing the highest-ranked, multi-task-supported candidates.
- Validation gates (Program Check, Diff Review, Execution Validation on two sampled tasks) roll back failures via recorded diffs, and after independent evolution of five modules a cross-module integration epoch resolves conflicts before freezing the library.
- Function Merge plus Task-Aware Function Composition control library complexity, and the evolution set holds 2,000 benchmark-disjoint Harbor-format instances (1,000 SWE-related + 1,000 Terminal-related).
---
## Trajectory Memory
**Covers:** Sec. 3.3 tail — Trajectory Memory

> "We further maintain a Trajectory Memory that stores historical trajectories and their rewards for each task across evolution epochs. This allows experience from previous epochs to provide additional contrastive evidence when the current rollouts alone are insufficient."

## Group-wise analysis by the Code-Modify Agent
**Covers:** Sec. 3.3 — Contrastive / Negative / Positive groups; findings consolidation

- **Contrastive group:** "successful and failed trajectories of the same task are paired and compared to identify function-level factors associated with different outcomes."
- **Negative group (all current rollouts fail):** "the agent first queries the Trajectory Memory for a previously successful trajectory of the same task. If one exists, it is paired with a current failed trajectory for contrastive analysis. Otherwise, the agent performs single-sided diagnosis over the failed trajectories to identify evident execution deficiencies, such as repetitive loops, incorrect tool usage, ineffective recovery, or premature termination."
- **Positive group (all rollouts succeed):** "the analysis focuses on opportunities to improve execution quality and efficiency, such as redundant actions, repetitive exploration, or unnecessary tool calls."
- **Consolidation:** "After analyzing all tasks in a batch, the Code-Modify Agent consolidates the diagnoses into structured findings in JSON format. Each finding specifies the module under analysis, supporting trajectory evidence, the rationale for or against modification, and a proposed change when applicable."
- Prompts/schema: "The detailed analysis prompt and output schema are provided in Appendix B and Appendix C.1."

## Module-wise harness modification
**Covers:** Sec. 3.4 — Modification Target Selection; Evolution History

- **Modification Target Selection:** "For each batch, we first consolidate semantically similar diagnoses that target the same function into candidate modifications. Each candidate is then assigned a vote count based on the number of distinct tasks that provide supporting evidence. We prioritize the highest-ranked candidates for subsequent evolution, favoring modifications supported across multiple tasks while reducing the influence of instance-specific failures."
- **Evolution History:** "we maintain an Evolution History for each function being updated. The history records previous code changes and the functionality introduced by each revision. By exposing these historical changes to the Code-Modify Agent, subsequent updates can better preserve previously evolved functionality while avoiding repeated or contradictory modifications."
- Stated purpose: "two mechanisms designed to improve modification reliability" and to "reduce redundant or conflicting modifications and mitigate evolution oscillation across iterations."
- "The prompts used for harness evolution are provided in Appendix C.2."

## Validation gates
**Covers:** Sec. 3.5 — Program Check; Diff Review; Execution Validation

- Gate rule: "Only validated modifications are retained during evolution."
- **Program Check:** "static checks on the modified harness, including AST validation, import checks, protocol compliance, discovery-contract verification, and static self-attribute audits. If a modification fails any of these checks, we use the recorded diffs to roll back the affected function to its previous version."
- **Diff Review:** "we ask the Code-Modify Agent to review each modification diff. The agent checks whether the introduced changes encode task-specific solutions, heuristics, or conditions that are unlikely to generalize beyond the current training instances. Modifications identified as overly task-specific are rejected and rolled back. The review prompt is provided in Appendix C.3."
- **Execution Validation:** "After each modification, we randomly sample two tasks from the current batch and execute them using the updated harness. If the modification introduces runtime errors or violates the expected execution protocol, we use the recorded diffs to roll back the harness to its previous version."

## Cross-module integration
**Covers:** Sec. 3.6

- "After the five modules have been evolved independently, their validated variants are combined into a unified harness."
- Rationale: "Since independently optimized modules may introduce duplicated mechanisms, conflicting behaviors, or inconsistent interactions when composed together, direct combination may not produce a coherent final system."
- Procedure: "We therefore perform an additional cross-module integration epoch on the evolution set. The integrated harness is executed on evolution tasks, and the Code-Modify Agent analyzes the resulting trajectories to identify cross-module conflicts. It then refines module interactions by removing duplicated mechanisms, clarifying module responsibilities, and adjusting coordination logic where necessary."
- Freeze rule: "After integration, the evolved function library is frozen and no further modifications are allowed during downstream evaluation. The prompt used for cross-module integration is provided in Appendix C.4."

## Function library management
**Covers:** Sec. 3.7

- "ModularRSI maintains an expanding library of evolved functions. We introduce two complementary mechanisms to control its complexity: Function Merge reduces redundancy in the persistent library, while Task-Aware Function Composition restricts the functions activated for each task."
- **Function Merge:** "Within each module, an LLM compares the descriptions and behaviors of its functions and merges those with highly similar or overlapping functionality, reducing redundancy while preserving their learned capabilities."
- **Task-Aware Function Composition:** "Each evolved function is associated with a natural-language description of its current behavior. Given the task description and the descriptions of all candidate functions, an LLM selects a subset of task-relevant functions, and only these functions are activated during execution."
- Scope: "Those mechanisms are used during both trajectory collection and downstream evaluation. This allows the underlying function library to expand through evolution while keeping the active harness compact and task-specific."

## Evolution dataset and protocol
**Covers:** Sec. 4; Figure 2 — 2,000-instance evolution pool

- Construction: category labels from "mainstream terminal-related benchmarks, including the TerminalBench and SWE-Bench families" guide human retrieval from "GitHub repositories, Hugging Face, Kaggle, and Linux kernel documentation"; retrieved resources become "new executable tasks in the Harbor format"; "no benchmark instances or task-specific information are used during task construction."
- Quality control: LLM filtering on "Environment Completeness," "Practicality and Non-triviality," and "Evaluator Validity"; executable validation requiring "the reference solution.sh to pass all task-specific tests while ensuring that a no-op submission cannot receive a positive reward"; manual review plus "LLM-based semantic similarity screening to remove instances with high overlap with downstream benchmarks."
- Yield: "this pipeline yields 2,000 high-quality, benchmark-disjoint evolution instances," "relatively balanced across task categories, with broadly comparable distributions for TB-related and SWE-related instances"; "SWE-related tasks are built around GitHub repositories and require repository-level software engineering, whereas TB-related tasks are constructed for direct interaction with terminal environments."

| Category | Count | Share |
|---|---|---|
| Data processing | 381 | 19.1% |
| ML & science | 272 | 13.6% |
| Build & deps | 244 | 12.2% |
| Systems & OS | 236 | 11.8% |
| Lang & API | 227 | 11.3% |
| Web & network | 189 | 9.4% |
| Algorithms | 176 | 8.8% |
| Security & crypto | 150 | 7.5% |
| Database | 125 | 6.2% |
| Total (SWE n=1000 + Terminal n=1000) | 2000 | 100% |

**Covers:** Sec. 3.3 (Trajectory Memory and group-wise analysis) through Sec. 4 (Evolution Dataset and Protocol), Fig. 2
