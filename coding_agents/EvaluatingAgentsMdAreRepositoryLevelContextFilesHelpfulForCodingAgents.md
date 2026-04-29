# Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?

**Paper:** [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? (Gloaguen et al., 2025)](https://arxiv.org/abs/2602.11988)

## Human Readable TL;DR

Imagine you hire a contractor to fix things around your house, and you leave them a detailed instruction manual about how your house works. You would expect this to help them do a better job. This paper tested whether giving AI coding assistants similar "instruction manuals" (called AGENTS.md or CLAUDE.md files) for software projects actually helps them fix bugs and add features. Surprisingly, auto-generated instruction manuals made the AI perform slightly worse and cost over 20% more, while hand-written ones helped only a little. It turns out the AI already figures out most of what it needs from the existing documentation -- the extra instructions are mostly redundant and can even be distracting.

## TL;DR

This paper empirically evaluates whether repository-level context files (AGENTS.md, CLAUDE.md) improve coding agent performance on real-world software engineering tasks. Using a novel benchmark (AGENTBENCH) with 138 tasks from repositories with developer-committed context files and SWE-BENCH LITE, the authors find that LLM-generated context files reduce success rates while increasing cost by 20%+, and human-written files yield only marginal gains (~4%). Context files are largely redundant with existing documentation and only help when other docs are scarce.

---

## Problem & Motivation

Coding agent developers (OpenAI, Anthropic, and others) widely recommend creating repository-level context files to tailor agents to specific codebases. Over 60,000 open-source repositories have adopted this practice. However, no rigorous empirical study had investigated whether these context files actually improve agent performance on real-world tasks. Prior work only catalogued and categorized the content of such files without measuring their impact. This paper fills that gap with the first large-scale quantitative evaluation.

---

## Main Original Ideas

1. **AGENTBENCH benchmark** -- A new benchmark of 138 Python software engineering tasks drawn from 12 recent, niche repositories that contain developer-committed context files. Unlike SWE-BENCH, which focuses on popular repositories, AGENTBENCH targets less prominent codebases where context files are most likely to matter, with LLM-generated unit tests covering 75% of modified code on average.

2. **Three-condition experimental design** -- A systematic comparison of agent performance under three context settings: no context file (NONE), LLM-generated context file (LLM), and human-written context file (HUMAN), evaluated across four coding agents (Claude Code, Codex, Qwen Code) with multiple underlying models.

3. **Behavioral trace analysis** -- Beyond success rates, the authors analyze agent traces to understand how context files change behavior, including tool usage frequency, command intent categorization, reasoning token consumption, and time-to-first-relevant-file interaction.

4. **Documentation redundancy hypothesis** -- An ablation study removing existing documentation from repositories reveals that LLM-generated context files only improve performance when other documentation is absent, demonstrating that their content is largely redundant with existing docs.

---

## Key Findings

| Setting | Avg. Success Rate Change | Avg. Cost Change | Avg. Extra Steps |
|---|---|---|---|
| LLM-generated (SWE-BENCH LITE) | -0.5% | +20%+ | +2.45 |
| LLM-generated (AGENTBENCH) | -2% | +20%+ | +3.92 |
| Human-written (AGENTBENCH) | +4% | up to +19% | +3.34 |

- LLM-generated context files **reduce** task success rates while **increasing** inference cost by over 20% on average
- Human-written context files provide only a **marginal ~4% improvement** at a notable cost increase
- Agents **do follow instructions** in context files -- they use specified tools (e.g., `uv`, repo-specific CLIs) almost exclusively when mentioned
- Context files encourage **more exploration and testing** but also increase reasoning tokens by 14--22%, suggesting agents perceive tasks as harder
- Context files **fail to help agents orient faster** -- they do not reduce the number of steps before agents first interact with relevant files
- When existing documentation is **removed**, LLM-generated context files consistently improve performance by ~2.7%, even outperforming developer-written docs -- confirming their content is redundant with existing documentation
- Using a **stronger model** (GPT-5.2) to generate context files does not consistently improve outcomes

---

## Suggestions & Future Directions

1. **Omit LLM-generated context files** for the time being -- they are generally counterproductive when other documentation exists, contrary to current agent-developer recommendations.

2. **Keep human-written context files minimal** -- include only essential requirements such as specific tooling, testing commands, or repository-specific constraints rather than comprehensive overviews.

3. **Investigate niche programming languages** -- context files may prove more valuable for languages underrepresented in LLM training data, where agents cannot rely on parametric knowledge.

4. **Evaluate beyond task resolution** -- future work should study the impact of context files on code efficiency, security, and maintainability, not just whether tasks are resolved.

5. **Improve automatic context file generation** -- the gap between human-written and LLM-generated files motivates research into more principled generation techniques, potentially leveraging planning and dynamic context engineering.

6. **Leverage the AGENTBENCH framework** -- the authors hope their benchmark and evaluation methodology will aid agent and model developers in improving context file helpfulness.

---

## Authors & Institutions

Thibaud Gloaguen (ETH Zurich), Niels Mundler (ETH Zurich), Mark Muller (LogicStar.ai), Veselin Raychev (LogicStar.ai), Martin Vechev (ETH Zurich)
