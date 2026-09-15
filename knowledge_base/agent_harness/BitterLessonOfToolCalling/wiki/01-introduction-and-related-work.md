> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Related Work

**In one sentence:** Replacing rigid JSON tool calls with executable Python scripts (programmatic tool calling) matches or beats native JSON tool calling on BFCL v4 for 11 of 14 models, with the advantage dividing along model generation lines and growing with task complexity (chaining, fan-out, context load).

## Key points

- Programmatic tool calling (PTC) matches or exceeds native JSON tool calling in 11 of 14 models on BFCL v4, with the GPT-5.6 family achieving a 10.6% improvement over the JSON baseline.
- Result splits by model generation, not family: all five Anthropic models and the three newest GPT generations match or exceed baseline; three older GPT models do not.
- On sequential tasks, PTC's accuracy advantage scales with chain length, reaching an 18.8% absolute gap over JSON tool calling at lengths ≥ 12 — an effect absent at short chains, driven by the extra inference turn JSON tool calling incurs per link.
- JSON tool calling drops tool calls entirely above a model-specific fan-out threshold (N = 70 – 72 for Claude Sonnet 5), while PTC maintains 100% enumeration accuracy at N = 100 — a hard structural limit in the native paradigm.
- Under context flooding, PTC holds stable; the JSON baseline degrades 2.3% on average and a filesystem-discovery comparison approach degrades 32% (PTC sees an absolute 5.5% improvement on average).
- Prior theoretical work (CodeAct, Wang et al., 2024) showed code actions achieve up to 20% higher task success with 30% fewer interaction turns on multi-tool tasks; Yang et al., 2026 found code-only output restrictions shift pass rates by fewer than 3% absolute on coding-agent tasks — but function calling, with precise argument serialization, multi-step chaining, and fan-out, remained untested across paradigm choices.
- The evaluation covers a 309-entry subset of BFCL v4 spanning eight task categories, 14 models released between November 2024 and July 2026, and three ablations targeting sequential chaining, parallel fan-out, and context rot.
- Existing tool-calling benchmarks (API-Bank, T-Eval, API-BLEND, UltraTool, CONFETTI, ToolHop) each evaluate calling accuracy but none compares paradigms; an audit of BFCL (Vaghasiya et al., 2026) found 20% evaluator-human misalignment in LLM-judge mode, which this work sidesteps by scoring against stub outputs directly.

---

## Abstract framing

Tool use transforms LLMs into agents that act beyond their training data, and for code-capable models, programmatic tool calling extends this further by replacing rigid JSON calls with scripts that chain and parallelize naturally. However, a systematic evaluation of tools as code on an established benchmark across current and prior model generations under real-world task conditions has not been conducted. This work empirically compares programmatic tool calling (PTC) to native JSON tool calling across 14 language models on BFCL v4. In the PTC paradigm, tools are exposed as typed Python stubs that the model invokes through code, with execution and results handled in a single agent turn. PTC matches or exceeds native JSON tool calling in 11 of 14 models on BFCL v4, with the GPT-5.6 family achieving a 10.6% improvement over the JSON baseline. Further, it matches or outperforms baseline in 13 of 14 models under parallel fan-out, and holds stable under context rot conditions where baseline degrades 2.3% on average. The results demonstrate that programmatic tool calling is a viable and robust alternative to JSON tool calling, with performance tracking model capability across release generations.

## Motivation

Large language models (LLMs) now act as tool-calling agents, invoking external services through APIs that require the model to emit a structured JSON object at each function call (Anthropic, 2024; Guo et al., 2026). For models that can already write executable code, this format is a design choice, not a necessity.

Prior work has established a theoretical case for replacing JSON tool calls with executable code. CodeAct (Wang et al., 2024) showed that code actions achieve up to 20% higher task success with 30% fewer interaction turns on multi-tool tasks, with gains concentrated in parallel and compositional scenarios. A more recent study found that code-only output restrictions change pass rates by an absolute change of fewer than 3% on coding-agent tasks (Yang et al., 2026). Function calling is a harder test case. It requires precise argument serialization, multi-step chaining, and fan-out across heterogeneous APIs, constraints absent from coding-agent evaluations and exactly where paradigm choice has the largest claimed effect. Whether programmatic tool calling matches JSON tool calling under these conditions, across model families and adversarial context loads, remains untested.

### Approach

To address this gap, the authors evaluate programmatic tool calling against JSON tool calling on a representative 309-entry subset of BFCL v4 spanning eight task categories, using 14 models released between November 2024 and July 2026. In programmatic tool calling, the model writes a Python script using typed Python stubs compiled from the benchmark's function schemas. The agent loop executes it in a shell subprocess, producing tool-call results without additional inference turns. The authors run three ablation studies targeting sequential chaining, parallel fan-out, and context rot, the task structures where the limitations of JSON tool calling have been most commonly claimed.

### Findings

The authors find that 11 of 14 models match or exceed baseline accuracy under programmatic tool calling on BFCL v4, with results dividing along model generation lines. All five Anthropic models and the three newest GPT generations match or exceed baseline accuracy, while three older GPT models do not. On context flooding, programmatic tool calling sees an absolute improvement of 5.5% on average, compared to an absolute 32% degradation for the filesystem-discovery comparison approach.

The contributions are:

1. Programmatic tool calling viability divides along model generation lines rather than model family. All five Anthropic models and the three newest GPT generations match or exceed JSON tool calling accuracy on BFCL v4, while three older GPT models do not.
2. Programmatic tool calling's accuracy advantage on sequential tasks scales with chain length, reaching an 18.8% absolute gap over JSON tool calling at lengths ≥ 12, an effect absent at short chains and driven by the extra inference turn JSON tool calling incurs per link.
3. JSON Tool Calling drops tool calls entirely above a model-specific fan-out threshold (N = 70 – 72 for Claude Sonnet 5). Programmatic tool calling maintains 100% enumeration accuracy at N = 100, exposing a hard structural limit in the native paradigm.
4. Under context flooding, programmatic tool calling holds stable while JSON tool calling degrades 2.3% on average and the filesystem-discovery approach degrades 32%, demonstrating robustness to adversarial context load.

## Related Work

### Code-action agents and production adoption

Two lines of work motivate replacing JSON tool calls with executable code. The first is code-action agents. CodeAct (Wang et al., 2024) showed that code actions outperform JSON alternatives on multi-tool tasks, with gains concentrated in parallel and compositional scenarios. Recursive Agent Harnesses (Lumer et al., 2026) extends the same code-execution primitive to parallel subagent spawning, showing that executing code in a subprocess bypasses the per-turn tool-call cap that constrains native JSON function calling at high fan-out. Practitioner frameworks extended this finding into production, treating code composition as the default interface (Hugging Face, 2024; Anthropic, 2024; Karten et al., 2026). Production memory systems such as Chronos (Sen et al., 2026b) deploy iterative JSON tool-calling loops as their core agent mechanism, confirming that JSON tool calling remains the dominant interface in deployed agentic systems. Infrastructure providers are adopting the same pattern. Cloudflare's Agents platform ships code execution as its native tool-use interface (currently experimental) (Cloudflare, 2026). A recent survey argues that code is the ideal substrate for agentic reasoning because it is executable, inspectable, and stateful (Ning et al., 2026). The Deterministic Horizon (Guo et al., 2026) provides theoretical grounding. Tool delegation is necessary precisely where chain-of-thought reasoning fails to produce verifiable answers, the same regime where tool-calling accuracy is measured. However, none of these works evaluate code-execution against JSON tool calling on a standardized benchmark across multiple model families.

### Prior benchmarks and their gaps

Several benchmarks measure LLM tool-calling accuracy, including API-Bank (Li et al., 2023), T-Eval (Chen et al., 2024), API-BLEND (Basu et al., 2024), UltraTool (Huang et al., 2024), CONFETTI (Alkhouli et al., 2025), and ToolHop (Ye et al., 2025). Each evaluates how accurately models call the right function with the right arguments, but none compares paradigms. BFCL v4 covers eight task categories with a deterministic scorer. A recent audit (Vaghasiya et al., 2026) found 20% evaluator-human misalignment in its LLM-judge mode, which our evaluation sidesteps by scoring against stub outputs directly. Work on agentic tool-calling training efficiency (Liu et al., 2026) and context inflation (Du et al., 2026) identifies format and prompt engineering as dominant sources of variance in tool-calling benchmarks, motivating the controlled three-way paradigm comparison we conduct. Unlike prior work, we evaluate programmatic tool calling against JSON tool calling on BFCL v4 across 14 models spanning 20 months of releases, with three ablation studies targeting chaining, parallel fan-out, and context rot.

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Work)
