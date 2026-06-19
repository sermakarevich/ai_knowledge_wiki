# My Week with Fable

**Source:** [My Week with Fable (Matthew Berman, Jun 9 2026)](https://x.com/MatthewBerman/status/2064393462028669176)

## Human Readable TL;DR

Imagine hiring a brilliant but quirky contractor who is more capable than anyone you've worked with, but insists on asking 10 clarifying questions before starting any project, writes reports that are exhaustingly detailed, and sometimes takes twice as long to do something simple because they refuse to cut corners. That's Fable. It can handle your most complex projects better than anything else, but you'll need to adjust how you work with it to get the most out of it.

## TL;DR

Matthew Berman's week-long evaluation of Anthropic's Fable model (internally called MYTHOS) found it to be the most capable model he has ever used, particularly excelling at long-horizon agentic tasks. Its "workflow mode" can spawn hundreds of parallel agents to conduct exhaustive code reviews. Key friction points are extreme verbosity, a tendency to ask for confirmation at every step, and noticeably slower output speed compared to previous Opus models.

---

## Problem & Motivation

What does a next-generation frontier model feel like in day-to-day engineering work? Berman spent a week stress-testing Fable (MYTHOS) on real coding tasks to report on its practical strengths and weaknesses before broader awareness.

---

## Main Original Ideas

1. **Parallel agent swarm for code review** -- Fable's "workflow mode" spawned hundreds of agents simultaneously, assigning one agent per file in the codebase. This produced more bug reports, edge-case findings, missing-documentation flags, and UX suggestions than the same prompt given to other frontier models.

2. **Extreme willingness to work autonomously** -- Fable is far more willing than prior Claude or GPT models to take an open-ended goal and pursue it for hours, burning large token budgets without hand-holding.

3. **Long-horizon task superiority** -- The model appears uniquely suited for tasks that require sustained, multi-step reasoning and execution. Berman found it hard to identify a problem complex enough to make it stumble.

4. **Information density as a force multiplier** -- A quirk observation: Fable's dense, technical explanations highlighted that higher information density per token is equivalent to making the model "effectively smarter at a cheaper cost." Berman notes this as a strong argument for agents developing hyper-dense internal languages in the future.

---

## Key Findings

| Dimension | Verdict |
|-----------|---------|
| Agentic / workflow mode | **Best in class** -- hundreds of parallel agents, exhaustive code review |
| Long-horizon autonomy | **Best in class** -- works for hours without guidance |
| Complex task confidence | **Best in class** -- the harder the task, the more it seems to thrive |
| Verbosity | **Needs tuning** -- too dense even after `CLAUDE.md` updates |
| Decision-making autonomy | **Needs tuning** -- over-asks for confirmation before acting |
| Speed | **Needs improvement** -- slower than prior Opus and GPT; token output sometimes stalls for minutes |

- Berman updated his `CLAUDE.md` to suppress verbosity; it wasn't sufficient.
- A single prompt can generate the pipeline: questions → answer summary → confirm summary → spec → confirm spec → confirm agent plan → build. Anthropic acknowledged this and said it is fixed in an updated system prompt.
- Even at the lowest effort setting, Fable thinks for a while and still delivers highly capable output.

---

## Suggestions & Future Directions

1. **Reduce effort level** -- Berman's top practical tip: dial effort well below where you'd set it for other models. Even "low" effort is still strong, and it cuts latency significantly.

2. **System prompt adjustments will address verbosity and over-confirmation** -- Anthropic confirmed the over-cautious confirmation loop is being fixed with system prompt updates.

3. **Model optimization and compute scaling** -- Berman expects speed and verbosity quirks to be resolved through standard model optimization and increased compute capacity.

4. **Fine-tuning / RL for decision-making style** -- The pattern of deferring choices back to the user is expected to be addressed via fine-tuning or RL to make the model more decisive by default.

---

## Authors & Institutions

Matthew Berman (@MatthewBerman), independent AI researcher and YouTuber.
