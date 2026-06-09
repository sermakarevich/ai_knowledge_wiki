# Building Long-Running Agentic AI Systems

**Source:** [Building Long-Running Agentic AI Systems (Ash & Andrew, Anthropic, AI Engineer Conference 2025/2026)](https://youtu.be/mR-WAvEPRwE)

## Human Readable TL;DR

Getting an AI to work reliably for hours on a complex task is like managing a forgetful contractor who tends to declare the job "done" prematurely. Anthropic's solution is to stop having the AI check its own work -- instead, hire a separate "quality inspector" who actually opens the app, clicks around, and reports real bugs back to the builder. Think of it like a PM, a developer, and a QA tester each having their own desk and notepad, rather than one person trying to juggle all three roles from memory. The teams also learned that as the AI models get better over time, some of the scaffolding you built to work around their weaknesses can simply be removed -- the harness needs to evolve alongside the model. The end result is AI that can build a fully featured, working application -- complete with an embedded AI assistant inside it -- in about 6 hours for around $200, something that was impossible just one model generation ago.

## TL;DR

The talk presents a Generator-Evaluator-Planner harness pattern for building long-running LLM agents (5+ hours). The core insight is that separating generation and evaluation into distinct context windows with adversarial pressure -- inspired by GANs -- dramatically outperforms self-evaluation within a single agent loop. The Evaluator uses Playwright (live browser interaction, screenshots, clicking) to verify behavior at runtime rather than reading diffs or running static tests. A Planner provides a high-level sprint spec that generators and evaluators negotiate into a concrete, testable contract of 20--30 granular criteria before any code is written. As frontier models improve (Opus 4.5 → 4.6), harness complexity can be reduced: context-window resets and sprint-by-sprint evaluation become unnecessary, replaced by continuous sessions with server-side compaction.

---

## Problem & Motivation

LLM agents are bad at running reliably for extended periods due to three structural weaknesses:

1. **Context limitations** -- Context windows are finite; starting a new session causes "amnesia." As context fills, "context rot" reduces coherence. Near the window end, models exhibit "context anxiety," rushing to finish prematurely.
2. **Planning failures** -- Models try to do everything in one shot, stop halfway through a feature, or run out of context mid-build.
3. **Self-evaluation blindness** -- Models are sycophantic about their own output. They will declare a half-implemented feature "done," build a button with no working backend, and mark it complete. This is the hardest problem to fix by prompting alone.

Reliable agent runtime went from ~20 min (Claude 3.5 Sonnet) to 12+ hours (Opus 4.6) over one year -- the talk explains what engineering changes made this possible.

---

## Main Original Ideas

1. **GAN-Inspired Generator-Evaluator Pattern** -- Directly adapted from Generative Adversarial Networks: a Generator agent builds, a separate Evaluator agent critiques. Tuning a standalone critic to be harsh is tractable; tuning a builder to be self-critical is not. The analogy: it's easy to critique a painting or meal, much harder to actually produce one.

2. **Live Playwright-Based Evaluation** -- The Evaluator is not reading diffs or running unit tests. It launches a real browser via Playwright MCP, navigates the live running app, clicks through features, and reports actual runtime failures. This catches things like broken arrow keys in a game, FastAPI route ordering bugs, and boolean logic errors -- things that pass CI but fail in production.

3. **Pre-Build Contract Negotiation** -- Before any code is written, the Generator proposes what it will build and how it will be tested. The Evaluator pushes back ("scope is too large, tests are too weak, you've missed edge case X"). They negotiate via files on disk until both agree on a contract -- typically 27 granular criteria for a full app. Evaluation is then graded against this agreed contract, not the original vague spec.

4. **Rubric-Based Aesthetic Grading** -- Quality is graded on four weighted criteria: **Design, Originality, Craft, and Functionality**. Design and Originality are weighted higher because Opus 4.6 is already strong at functionality. The rubric is calibrated using few-shot examples of reference sites vs. "AI slop" to give the evaluator consistent taste.

5. **Harness Co-Evolution with Model Capabilities** -- The harness is explicitly designed to shrink and simplify as models improve. Sprint decomposition was critical for Opus 4.5 but unnecessary for Opus 4.6 (which can sustain coherent 2-hour builds). Context resets were dropped entirely for 4.6. The harness "fills gaps" in the current model and gets trimmed when the model improves.

6. **Structured Persistent Artifacts for Long-Running State** -- Rather than relying on context windows for multi-hour state, the harness uses the filesystem: `featurelist.json` (models are less likely to overwrite JSON than Markdown), a `progress.json` with per-feature pass/fail flags, an `init.sh` to reliably boot the server each session, and a timestamped "learnings log" as breadcrumbs for the next agent or human.

---

## Key Findings

| Insight | Detail |
|---------|--------|
| Self-evaluation is a trap | Even when explicitly instructed to self-critique, LLMs exhibit sycophancy toward their own outputs |
| JSON beats Markdown for state | Models are empirically less likely to overwrite `.json` files than `.md` files |
| Opus 4.5 → 4.6 gap is large | 4.5 required aggressive sprint decomposition; 4.6 runs a continuous 2-hour build coherently |
| Evaluator context isolation | Giving the evaluator the generator's trace is counterproductive; judge the output only, not the process |
| Meter benchmark | Reliable agent runtime went from ~1 hour (Opus 3.7) to 12 hours (Opus 4.6) in one year |
| Practical cost | Fully featured greenfield apps: 3--5 hours at ~$200 with simplified harness |

- Server-side compaction enables indefinite runs without context resets
- Models will demand a restart from scratch far more readily as an Evaluator than as a Generator -- the generator is "proud of its work"
- Manual trace reading (like reading a stack trace) is the primary and most effective debugging method for agent pipelines
- Opus 4.6 vision is good enough to identify overlapping text, layout bugs, and navigate a live app -- not the case one generation prior

---

## Suggestions & Future Directions

1. **Harness-model co-evolution as a permanent discipline** -- Regularly strip out harness complexity after each major model release and re-evaluate what the model now handles natively.
2. **Breadcrumb-driven long-lived products** -- For iterative projects, embed prompting that writes timestamped learnings to JSON so future agents or humans can pick up mid-run cleanly.
3. **Human-in-the-loop via hooks** -- Use stop hooks to inject review checkpoints rather than hardcoding human review; longer-term goal is full autonomy.
4. **Autonomous software development lifecycle** -- Monitoring → issue generation → coding agent → PR → review agent → human merge review as a brownfield automation pipeline.
5. **Generator-evaluator pattern beyond coding** -- Eval generation, synthetic dataset creation, multi-step workflows with QA agents at each step.
6. **Training the generator to predict critic outputs** -- Making the generator model more honest by training it to anticipate what a harsh critic would say (audience suggestion acknowledged as future work).

---

## Key Tools & Techniques

- **Playwright MCP** -- live browser automation for the evaluator (navigate, click, screenshot, verify)
- **Agent SDK** (renamed from Claude Code SDK) -- general-purpose agentic orchestration
- **Model selection strategy** -- Opus 4.6 for planning, Sonnet 4.6 for execution (Opus-level at Sonnet pricing), Haiku 4.5 for parallel sub-agents
- **Server-side compaction** -- continuous session with automatic summarization, enables indefinite runs
- **Skills** -- packaged rubrics and grading criteria with progressive disclosure (front matter loaded first, full body on instantiation)
- **Hooks** -- stop hooks and pre-tool hooks to inject behavior at specific loop points
- **RALF Loop** -- Run And Loop Forever pattern (attributed to Jeffrey Huntley, July 2024); Anthropic's version runs within a single session rather than creating fresh context windows
- **Checkpoints (Claude Code 2.0)** -- session rewind capability

---

## Authors & Institutions

**Ash** -- Engineer, Applied AI Team, Anthropic  
**Andrew** -- Solutions Architect, Applied AI Team, Anthropic (London; works with digital native and enterprise customers)
