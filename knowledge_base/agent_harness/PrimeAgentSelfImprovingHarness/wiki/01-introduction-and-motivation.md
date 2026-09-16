> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Motivation

**In one sentence:** A language model is only a bounded sequential processor, so Prime Agent provides a standardized, expressive, self-improving harness that manages external information (L0–L3 state caches) and test-time compute — with recursive subagents, direct agent-to-agent communication, and a Continual Harness — so that measured performance reflects the model's true maximal capability rather than harness failures.

## Key points

- An LLM is a "bounded sequential processor whose next decision can use only state information exposed in its weights and active context"; a harness supplies the missing computational substrate for external actions via tool-calls, including information management beyond prior knowledge in the weights.
- The paper organizes the system's information state into four cache levels (Figure 2): L0 = model weights, L1 = active context, L2 = persistent REPL + recursive subagents, L3 = disk-backed history, memories, and skills — which makes the system "more von Neumann-like" (model reads, transforms, and writes addressable state outside the instruction being generated).
- "Expressivity" is the key property of a good harness: rather than encoding one workflow, an expressive harness exposes primitives from which the model constructs programs, subagents, and feedback loops at inference time (RLMs make context and recursive invocation programmable; Continual Harness makes prompts, subagents, skills, and memories revisable from trajectory history).
- Prime Agent is designed first as a standardized harness for long-horizon evaluation, scored by the most popular metrics: score at a fixed expenditure (cost/tokens, time) or, especially for long-horizon tasks, score at practical plateau, which allows analyzing the shape of performance over time.
- A model should fail an evaluation "because the task exceeds its capability, not because the harness dropped state, restricted useful actions, miscounted resources, or terminated prematurely" — Prime Agent standardizes execution, recovery, verification, and resource accounting while leaving strategy construction to the model.
- Prime Agent raises ARC-AGI-3 RHAE Best@1 from 30% to 95.5% (abstract), and the introduction reports improving ARC-AGI-3 performance from 30% to 95%, matching or exceeding Pi, Claude Code, and Codex (and outperforming Hermes Agent, OpenCode, and Kimi-Code on other benchmarks) across long-context coding, GPU-kernel generation, and emulator construction.
- Prime Agent sustains an 85.5-hour nanoGPT speedrun with 19 validated records, supports four-character Factorio control (where refinement enables continuous technology progression and dedicated subagents enable parallelized work), and supports long-horizon MazeBench exploration.
- Prime Agent is open-source (https://github.com/PrimeIntellect-ai/prime-agent), authored by Seth Karten (Princeton), Alex L. Zhang (MIT), and Kevin Thomas, Sebastian Müller, Elie Bakouch, Daniel Auras, Mika Senghaas, Fares Obeid, Konstantin Dunas, Johannes Hagemann, Sami Jaghouar (Prime Intellect); first published August 5, 2026, current version August 24, 2026.

---

## Title, authors, and provenance

The paper "Prime Agent: A Self-Improving RLM Harness" (arXiv:2608.23552) is a technical report by Seth Karten (Princeton University), Alex L. Zhang (MIT), and eleven Prime Intellect colleagues (Kevin Thomas, Sebastian Müller, Elie Bakouch, Daniel Auras, Mika Senghaas, Fares Obeid, Konstantin Dunas, Johannes Hagemann, Sami Jaghouar). Correspondence: seth@primeintellect.ai, altzhang@mit.edu. First published August 5, 2026; current version August 24, 2026.

The abstract states: Language models are sequential processors, but long-horizon agency requires external information and computation beyond model weights and active context. Prime Agent is an open-source harness for long-horizon evaluation and coding-agent workflows. A persistent IPython REPL follows the Recursive Language Model abstraction for programmatic context processing and test-time compute, while Continual Harness preserves histories, memories, skills, prompts, and subagent specifications across trajectories. Recursive subagents coordinate through direct agent-to-agent communication, and the Agents View lets humans inspect and manage daemon-backed sessions. Prime Agent standardizes execution, recovery, verification, and resource accounting while leaving strategy construction to the model. This low-friction, expressive membrane prevents harness failures from becoming model failures and pushes measurement toward the model's true maximal underlying capability. Prime Agent raises ARC-AGI-3 RHAE Best@1 from 30% to 95.5% and matches or exceeds native and popular harnesses across long-context coding, GPU-kernel generation, emulator construction, and autonomous nanoGPT speedruns. On Factorio, refinement allows for continuous technology progression and dedicated subagents enable parallelized work.

## LLMs as bounded sequential processors; the harness as missing substrate

Section 1 opens with the core framing: "A strong language model on its own does not have the full capabilities of a computer." An LLM is a bounded sequential processor whose next decision can use only state information exposed in its weights and active context. A harness supplies the missing computational substrate that allows for external actions via tool-calls. These external actions also include information management beyond prior knowledge stored in the model weights. Context management was first enabled by agentic compaction — the process by which a model selectively analyzes its own context to reduce tokens while keeping essential information. However, the full information state has grown beyond the weights and token context.

## The state information cache (L0–L3) and the von Neumann framing

Imagined as a state information cache (Figure 2), model weights are L0, active context is L1, a persistent REPL and recursive subagents form L2, and disk-backed history, memories, and skills form L3. This makes the system more "von Neumann-like": the model can read, transform, and write addressable state outside the instruction currently being generated.

## Expressivity as the key harness property

This perspective makes expressivity the key property of a harness. Rather than encode one workflow, an expressive harness exposes primitives from which the model constructs programs, subagents, and feedback loops at inference time. Recursive Language Models (RLMs) make context and recursive invocation programmable; Continual Harness makes prompts, subagents, skills, and memories revisable from the trajectory history. Prime Agent also enables large-scale coordination and orchestration of multi-agent swarms through direct agent-to-agent communication. These components let a fixed model use information management and test-time compute to expand its reachable strategy set.

## Prime Agent as standardized long-horizon evaluation harness

Prime Agent is designed first as a standardized harness for long-horizon evaluation. The most popular metric is score at a fixed expenditure (cost/tokens and time) or, especially for long-horizon tasks, score at practical plateau, which allows analyzing the shape of performance over time. The harness is the membrane through which the model observes and acts on the world. A model should fail an evaluation because the task exceeds its capability, not because the harness dropped state, restricted useful actions, miscounted resources, or terminated prematurely. Prime Agent therefore combines standardized, reliable execution with a low-friction and expressive interface for programmatic tools, information management, and swarm management. This lets the model fully use its test-time compute, pushing measured performance toward its true maximal underlying capability rather than the limitations of its harness.

## Joint information and computation management

Prime Agent jointly manages information and computation. Information management moves state across L1–L3 through programmatic context processing, compaction, persistent histories, and revisable memories. Computation management allocates test-time compute to programs, tool calls, reusable skills, and parallel recursive subagents. Direct agent-to-agent communication connects the two, routing information across distributed computation so the swarm can coordinate dynamically rather than follow a fixed graph. These communication links also let humans inspect, message, attach to, and intervene in subagent sessions without following every exchange. Together, these interactions produce retained trajectories that improve future computation and can train later model generations.

## What Prime Agent presents and the headline results

We present Prime Agent, an open-source harness for long-horizon model evaluation and coding-agent workflows. Prime Agent integrates information and computation management across active context, persistent programmatic execution, recursive subagents, and retained histories, memories, and reusable skills, connected through direct agent-to-agent and human-agent communication. Its Agents View provides a visual interface for inspecting, attaching to, and managing persistent daemon-backed agent sessions. We standardize evaluation infrastructure while preserving the model's freedom to construct its own strategy. Prime Agent improves ARC-AGI-3 performance from 30% to 95%, matches or exceeds Pi, Claude Code, and Codex (and outperforms other harnesses, Hermes Agent, OpenCode, and Kimi-Code, on other benchmarks) across long-context coding, GPU-kernel generation, and emulator construction, sustains an 85.5-hour nanoGPT run with 19 validated records, and supports four-character Factorio control and long-horizon MazeBench exploration.

Figure 1 (architecture overview) depicts how Prime Agent connects persistent root and subagent sessions to a daemon, the Continual Harness, the Agents View, and the environment; solid arrows carry execution and messages, dashed arrows carry persistent state.

**Covers:** Title/Abstract, Section 1 (Introduction)
