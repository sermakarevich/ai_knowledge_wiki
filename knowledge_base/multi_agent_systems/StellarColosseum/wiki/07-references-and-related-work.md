> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References and Related Work ([41]–[65]) plus Appendix Prompts
**In one sentence:** This chunk lists references [41]–[65] and opens Appendix A with the shortened prompt templates for strategy exploration (explorer, falser, aggregator, readiness gate).
## Key points
- Lists 25 references numbered [41]–[65], spanning NeurIPS 2023 through arXiv preprints dated 2024, 2025, and 2026.
- Reference [41] is Honghao Lin, Vahab Mirrokni, and David P. Woodruff, "Pairwise-independent dithering for single-stage Hadamard quantization," arXiv:2608.02564, 2026.
- Appendix A states its templates are "shortened versions of the prompts used by the harness" with "items in braces filled in by the harness at runtime" and repeated instructions omitted.
- The Explorer must "Develop one promising high-level solution strategy before decomposition" and "Return one strategy card, not a proof, section plan, or LaTeX document," keeping exactly one primary route and at most two backup routes.
- The Exploration Falser must "Attack the supplied strategy card. Do not rewrite, polish, or defend it, except to name a minimal weakening," returning categorized objections, cheap tests, and a survive / weaken-or-repair / reject / falsified verdict.
- The Exploration Aggregator must "Produce one new strategy card, not a list and not a decomposition," preserving the narrowest repairable primary route and at most two backups while addressing every serious falser objection.
- The Readiness Gate does not solve or repair but audits fatal bridge claims, cited theorems, equivalences, invariants, bound directions, and code results, classifying the card as ready, eligible with explicit obligations, needing further exploration, or rejected.
---
## References [41]–[65]
**Covers:** pp. 19–21, refs [41]–[65]

| Ref | Authors (as listed) | Title / venue | Year |
|---|---|---|---|
| [41] | Honghao Lin, Vahab Mirrokni, and David P. Woodruff | Pairwise-independent dithering for single-stage Hadamard quantization. arXiv:2608.02564 | 2026 |
| [42] | Jihao Liu, Guoxiong Gao, Zeming Sun, Bin Wu, Shurui Liu, Jiedong Jiang, Haocheng Ju, Leheng Chen, Ronnie Cheng, Xiping Zhang, and Bin Dong | Danus: Orchestrating mathematical reasoning agents with fact-graph memory. arXiv:2607.06447 | 2026 |
| [43] | Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha | The AI Scientist: Towards fully automated open-ended scientific discovery. arXiv:2408.06292 | 2024 |
| [44] | Aman Madaan et al. (16 authors) | Self-Refine: Iterative refinement with self-feedback. NeurIPS vol. 36 | 2023 |
| [45] | Alexander Novikov et al. | AlphaEvolve: A coding agent for scientific and algorithmic discovery. arXiv:2506.13131 | 2025 |
| [46] | OpenAI | Our First Proof submissions. OpenAI Research, Feb 20, 2026 | 2026 |
| [47] | OpenAI | Ten advances in mathematics and theoretical computer science. Aug 1, 2026 | 2026 |
| [48] | Shanghaoran Quan et al. | CodeElo: Benchmarking competition-level code generation of LLMs with human-comparable Elo ratings. arXiv:2501.01257 | 2025 |
| [49] | Bernardino Romera-Paredes et al. | Mathematical discoveries from program search with large language models. Nature, 625:468–475 | 2024 |
| [50] | Johannes Schmitt et al. | ProofCouncil: An LLM agent for solving open mathematical problems. arXiv:2607.09474 | 2026 |
| [51] | Shiven Sinha et al. | Can language models falsify? evaluating algorithmic reasoning with counterexample creation. Second Conference on Language Modeling | 2025 |
| [52] | Trieu H. Trinh et al. | Solving olympiad geometry without human demonstrations. Nature, 625:476–482 | 2024 |
| [53] | George Tsoukalas et al. | Advancing mathematics research with AI-driven formal proof search. arXiv:2605.22763 | 2026 |
| [54] | Peisong Wang et al. | CP-Agent: A calibrated risk-controlled agent for feedback-driven competitive programming. arXiv:2605.24693 | 2026 |
| [55] | Xuezhi Wang et al. | Self-consistency improves chain of thought reasoning in language models. ICLR | 2023 |
| [56] | David P. Woodruff et al. | Accelerating scientific research with Gemini: Case studies and common techniques. arXiv:2602.03837 | 2026 |
| [57] | David P. Woodruff and Taisuke Yasuda | Root ridge leverage score sampling for ℓp subspace approximation. Proc. 66th FOCS | 2025 |
| [58] | Yangzhen Wu et al. | Inference scaling laws: An empirical analysis of compute-optimal inference for LLM problem-solving. ICLR | 2025 |
| [59] | Yutaro Yamada et al. | The AI Scientist-v2: Workshop-level automated scientific discovery via agentic tree search. arXiv:2504.08066 | 2025 |
| [60] | Shunyu Yao et al. | Tree of thoughts: Deliberate problem solving with large language models. NeurIPS vol. 36 | 2023 |
| [61] | Yuanhe Zhang et al. | LeanMarathon: Toward reliable AI co-mathematicians through long-horizon Lean autoformalization. arXiv:2606.05400 | 2026 |
| [62] | Zelin Zhao et al. | RMA: An agentic system for research-level mathematical problems. arXiv:2605.22875 | 2026 |
| [63] | Daniel Zheng et al. | AI co-mathematician: Accelerating mathematicians with agentic AI. arXiv:2605.06651 | 2026 |
| [64] | Zihan Zheng et al. | LiveCodeBench Pro: How do olympiad medalists judge LLMs in competitive programming? NeurIPS vol. 38 | 2025 |
| [65] | Shang Zhou et al. | OpenDeepThink: Parallel reasoning via Bradley–Terry aggregation. arXiv:2605.15177 | 2026 |

## Appendix A — Selected Prompt Templates and Information Flow
**Covers:** p. 22, Appendix A opening paragraph

Verbatim framing: "The templates below are shortened versions of the prompts used by the harness. They show what each stage does, what information it receives, and what it passes to later stages. Repeated instructions and implementation details are omitted. Items in braces are filled in by the harness at runtime."

## A.1 Strategy Exploration
**Covers:** pp. 22–23, §A.1 (Explorer, Exploration Falser, Exploration Aggregator, Readiness Gate)

Short definition from chunk: "Strategy exploration combines an explorer, a paired falser, an exploration aggregator, and a readiness gate. The gate approves a strategy for decomposition, allows a stable route to proceed with explicit proof obligations, or returns it for further exploration."

### Explorer
Inputs listed: `{problem}`; `{knowledge directory, when available}`; `{exploration round}`; `{previous strategy, falser report, and readiness-gate report, when available}`; `{previous proof and verifier feedback, when available}`.

Verbatim duties:
- "Develop one promising high-level solution strategy before decomposition."
- "Return one strategy card, not a proof, section plan, or LaTeX document."
- "Normalize the target, state a candidate reduction and core mechanism, and identify the first hard obstruction."
- "Maintain exactly one concrete primary route and at most two genuinely distinct backup routes."
- "Preserve an affirmative route unless a reproducible counterexample or symbolic contradiction already refutes the target."
- "Distinguish proved facts from partial, heuristic, or unverified claims."
- "Treat the strategy as ready for decomposition only when no unresolved fatal obligation remains."

### Exploration Falser
Inputs listed: `{problem}`; `{knowledge directory, when available}`; `{strategy card, including executed code-probe result when available}`; `{previous proof and verifier feedback, when available}`; `{falser reports inherited from child nodes, when available}`.

Verbatim duties:
- "Attack the supplied strategy card. Do not rewrite, polish, or defend it, except to name a minimal weakening."
- "Test the weakest central lemmas, hidden assumptions, overstrong claims, boundary or counterexample regimes, dropped objections, theorem hypotheses, inequality directions, and any mismatch between a code probe and the claim it is said to test."
- "A failed program is missing evidence, not a mathematical counterexample; reserve falsified for a valid argument or reproducible test."
- Output: "overall assessment, categorized objections, cheap falsification tests, unresolved objections that later stages must preserve, minimal weakenings to try, and a verdict indicating whether the route survives, requires weakening or repair, should be rejected, or has been falsified."

### Exploration Aggregator
Inputs listed: `{problem}`; `{knowledge directory, when available}`; `{(strategy card, falser report) pairs sampled at this tree node}`; prior strategy/falser/gate reports and prior proof/verifier feedback when available.

Verbatim duties:
- "Produce one new strategy card, not a list and not a decomposition. Do not average the children or merely select one of them."
- "Preserve the narrowest concrete, repairable route as the single primary route unless its core mechanism has been killed."
- "Retain at most two nonduplicative backup routes, including a useful minority route when warranted."
- "A route with an unresolved fatal obligation is not ready for decomposition."

### Readiness Gate
Inputs listed: `{problem}`; `{knowledge directory, when available}`; `{final strategy card}`; `{attached falser report, when available}`; `{previous proof and verifier feedback, when available}`.

Verbatim duties:
- "Do not solve the problem or repair the strategy. Decide whether the card is safe to turn into a proof decomposition."
- "Audit every fatal bridge claim, cited theorem and hypothesis, target equivalence, induction or construction invariant, compatibility condition, hidden hard step, bound direction, unresolved falser objection, and central code result."
- "Classify the strategy as ready for decomposition, eligible for decomposition with explicit obligations, in need of further exploration, or to be rejected."

**Covers:** References [41]–[65] (pp. 19–21); Appendix A opening and §A.1 Strategy Exploration (pp. 22–23)
