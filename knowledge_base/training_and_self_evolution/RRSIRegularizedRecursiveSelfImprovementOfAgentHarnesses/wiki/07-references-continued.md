> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References (continued) and Appendix: Evaluation, Baselines, Method Details
**In one sentence:** This chunk gives three continued bibliography entries and the appendix opening — a paired-window evaluation protocol across eight benchmark surfaces (Terminal-Bench 2.1, SWE-bench Verified, Harvey LAB, JobBench, GDPval, APEX-Agents, EngDesign, Frontier-Eng), summaries of four harness-evolution baselines, and the start of the round-level RRSI formulation.
## Key points
- Harness and baseline are always evaluated in the same window with the same tool environment, same judge, and same number of trials, with containers/environments reset so no state carries between arms.
- Terminal-Bench 2.1 reports fraction of 89 containerized shell tasks solved (hidden unit tests must pass); SWE-bench Verified reports resolve rate requiring both fail-to-pass and pass-to-pass tests to hold.
- Harvey LAB grades exact-filename deliverables from Word/Excel/PDF sources on 20–100 criteria per task (~14,000 verdicts per full evaluation) via isolated Gemini-3.5-Flash judgments, split once into 120 evolve / 40 held-out tasks.
- GDPval reports win rate vs. human expert over 185 tasks by majority vote of three judges (Qwen3.6-35B-A3B, Claude Sonnet 4.6, Gemini-3.1 Pro) with both presentation orders; APEX-Agents reports pass@1 over all 480 tasks with missing/failed rollouts counted as failures.
- Frontier-Eng is used only out-of-distribution with a Medal Score (1 / 0.67 / 0.33 for gold/silver/bronze thresholds from the frozen v1 snapshot, mean over 47 v1 tasks as a percentage), excluding its EngDesign domain and scoring only the 38 buildable tasks in both arms.
- The four baselines are Meta-Harness (outer-loop optimization over harness code from scores/traces), AHE (observability-driven component/experience/edit representations), TTHE (test-time multi-candidate evolution with fixed weights and agentic judge), and HarnessX (modular typed primitives with trace-driven adaptation).
- RRSI's method note states L0/Lasso-L1/Ridge-L2 language is analogy-only for complexity control: it does not optimize norm-penalized objectives and does not treat heterogeneous harness components as coordinates of a shared continuous vector.
---
## Continued references
| Entry | Detail in chunk |
|---|---|
| J. Zhang, B. Zhao, W. Yang, et al., Hyperagents | arXiv:2603.19461, 2026c |
| L. Zhang, R. Zhou, D. Song, et al., HarnessCompass: Guiding automatic harness evolution toward generalizable and effective agent harnesses | arXiv:2608.01918, 2026d |
| Y. Zhang, Y. Dai, J. Tan, et al., DarwinX: Evolving agent harnesses through natural selection | arXiv:2608.07545, 2026e |

## Appendix contents map
| Section | Title | Page in source |
|---|---|---|
| A | Evaluation (A.1 Terminal-Bench 2.1 through A.8 Frontier-Eng) | 17–18 |
| B | Baseline Methods | 18 |
| C | Method Details (C.1 Round-Level Formulation, C.2 Proposal-Side Bookkeeping, C.3 Selection-Side Bookkeeping) | 19–21 |
| D | Experiments (D.1 Hyperparameter Setting) | 22 |
| E | Qualitative Case Study | 23 |

## A. Evaluation — shared protocol
- Verbatim: "A harness and its baseline are always evaluated in the same window, with the same tool environment, the same judge and the same number of trials."
- "Containers are torn down and rebuilt between arms so that no state carries from one evaluation to the next" (stated for Terminal-Bench 2.1).

## A.1–A.8 environment scoring
| Env | N / split | Task form | Grading |
|---|---|---|---|
| Terminal-Bench 2.1 | 89 tasks | Container image + description + working dir; real shell; hidden tests | Accuracy = fraction solved; solved only if task test suite passes after agent stops |
| SWE-bench Verified | instances (count not in chunk) | GitHub issue + repo snapshot; produce patch | Resolve rate = fraction satisfying fail-to-pass (failing→passing) AND pass-to-pass (remain passing) |
| Harvey LAB | 160 tasks: 120 evolve / 40 held-out, fixed | Folder of Word/Excel/PDF sources; deliverables under exact filenames | Fraction of criteria passed over all tasks; 20–100 criteria/task, ~14,000 verdicts; isolated LLM judge (Gemini-3.5-Flash) per criterion; missing deliverable fails all its criteria |
| JobBench | evaluated split (count not in chunk) | Task folder + wrapper prompt; reference material withheld (genuine retrieval); filesystem + code-execution + grounded web search | Benchmark weighted rubric; reported number is weighted rubric score; judge is average of Gemini-3.5-Flash and Claude Opus 4.8 |
| GDPval | 185 tasks | Harness deliverable side-by-side with shipped human-expert deliverable | Win rate vs. expert; panel of Qwen3.6-35B-A3B + Claude Sonnet 4.6 + Gemini-3.1 Pro, both orders, majority vote; "Each judge therefore issues 204 comparisons per harness"; ">50% means the harness produces the preferred deliverable more often than the human expert" |
| APEX-Agents | 480 tasks, full denominator | Sandboxed world with MCP surface (filesystem, PDF, spreadsheets, mail, chat, calendar, documents, code execution); three professional domains | Per-task rubric via Gemini-3.5-Flash; pass@1 on single rollout; missing rollout (e.g. infra failure) counts as failure |
| EngDesign | 61 license-free tasks running without proprietary simulators; no held-out split | Design goal + physical constraints | Frozen simulation/testbench per task, deterministic, no judge model; evolution on all 61 |
| Frontier-Eng | 47 v1 tasks from 26 domains; OOD-only; 38 contribute credit | Design/program scored by frozen task-specific simulator on continuous objective | Medal Score: gold/silver/bronze thresholds from three best feasible frozen-v1 results; credit 1 / 0.67 / 0.33; mean over tasks as percentage; EngDesign domain excluded; unbuildable envs get no credit in either arm |

## B. Baseline methods
- "Meta-Harness (Lee et al., 2026b). Meta-Harness formulates harness engineering as an outer-loop optimization problem over executable harness code. Its agentic proposer has access to the source code, evaluation scores, and execution traces of previous candidates, and uses this accumulated experience to propose improved harnesses."
- "Agentic Harness Engineering (AHE) (Lin et al., 2026a). AHE uses an observability-driven evolution loop for coding-agent harnesses. It organizes harness components, execution experience, and edit outcomes into explicit representations so that an evolving agent can diagnose failures, propose changes, and evaluate the effects of previous edits."
- "Test-Time Harness Evolution (TTHE) (Nie et al., 2026). TTHE evolves executable harnesses during test-time adaptation while keeping the underlying model weights fixed. It maintains multiple candidate harnesses, proposes modifications from execution traces, and uses an agentic judge to select a harness that persists to subsequent inputs."
- "HarnessX (Chen et al., 2026). HarnessX represents an agent harness as a composition of modular, typed primitives spanning components such as prompts, tools, memory, and control flow. Its trace-driven adaptation mechanism uses execution feedback to modify and select harness configurations, enabling the runtime scaffold to evolve over time."

## C. Method details (opening) and C.1 Round-Level Formulation
- "This section gives the round-level formulation and implementation details omitted from Section 3. It specifies the same proposal- and selection-side regularizers used in the experiments."
- "As in the main text, the 𝐿0, Lasso/𝐿1, and Ridge/𝐿2 terminology is used only to indicate analogous roles in complexity control. The procedure does not optimize the corresponding norm-penalized objectives, and heterogeneous harness components are not treated as coordinates of a shared continuous parameter vector."
- "Let Ω(𝐻) denote the set of harnesses reachable from 𝐻 by arbitrary source edits. RRSI leaves Ω(𝐻) open and instead regularizes the transition through this space."
- Round form (Eq. 8, truncated in chunk): "𝐻𝑡 ∼ 𝑃reg · |𝐻𝑡, F𝑡, L𝑡, 𝑏𝑡, E𝑡, B𝑡 ⊆ Ω(𝐻𝑡), 𝐻𝑡₊₁ = arg max 𝑆ˆ(𝐻′) / 𝐻′ ∈ H𝑡 ∩ A𝑡" — chunk breaks off mid-equation, so the acceptance set and selector are not fully visible here.

**Covers:** chunk 07-j-zhang-b-zhao-w-yang.md, refs J. Zhang/Hyperagents through Y. Zhang/DarwinX plus Appendix contents and Sections A–C.1 (Eq. 8 truncated).
