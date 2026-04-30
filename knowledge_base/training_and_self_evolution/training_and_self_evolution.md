# Training & Self-Evolution

Research on **LLM training methods, post-training, self-improvement loops, and closed-loop agentic evolution** where systems improve themselves across data, architecture, or algorithms.

## Papers

- [[AgenticQwen/summary]] — Dual-flywheel RL framework trains small models (8B/30B) for industrial tool use by iteratively generating harder tasks from model failures; AgenticQwen-8B doubles vanilla Qwen3-8B's agentic benchmark score.
- [[AgentWorld/summary]] — Mines 1,978 stateful real-world environments (19,822 tools) for agent RL; a diagnostic arena targets weak environments, driving monotonic gains across 23 agentic benchmarks.
- [[AsiEvolveAiAcceleratesAi]] — Closed-loop agentic framework autonomously improves neural architectures, data curation, and RL algorithms in all three domains.
- [[SageMultiAgentSelfEvolutionForLlmReasoning]] — 4-agent Challenger-Planner-Solver-Critic co-evolves reasoning in math/code from 500 seed examples.
- [[SelfEvolvingPostTraining/summary]] — LLMs self-improve math reasoning by fine-tuning on their own low-temperature samples; +11.3 avg on six math benchmarks.
- [[ThinkingWithoutWords/summary]] — Post-training recipe replacing verbal CoT with discrete abstract tokens; bottlenecked SFT + GRPO teaches LLMs a compact reasoning language, achieving 4x–12x fewer tokens at comparable accuracy.
