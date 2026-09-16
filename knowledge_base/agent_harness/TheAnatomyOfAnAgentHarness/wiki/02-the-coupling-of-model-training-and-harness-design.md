> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Coupling of Model Training and Harness Design

**In one sentence:** Models and harnesses are post-trained together in a feedback loop that makes models highly capable inside their own harness but overfitted to it, so the best harness for a given task is often a different, task-optimized one — and harness engineering remains valuable even as models absorb more capabilities.

## Key points

- Agent products like Claude Code and Codex are post-trained with models and harnesses in the loop, improving models at harness-designer-chosen skills: filesystem operations, bash execution, planning, and parallelizing work with subagents.
- This creates a repeating feedback loop: useful primitives are discovered, added to the harness, and then used when training the next generation of models, making models more capable within the harness they were trained in.
- Co-evolution causes overfitting: changing tool logic degrades model performance, e.g. the Codex-5.3 prompting guide's apply_patch tool logic for editing files — switching patch methods should be trivial for a truly intelligent model.
- The post-training harness is not necessarily the best harness for your task: on the Terminal Bench 2.0 Leaderboard, Opus 4.6 in Claude Code scores far below Opus 4.6 in other harnesses.
- Harness-only changes carry large gains: the authors improved their coding agent from Top 30 to Top 5 on Terminal Bench 2.0 by only changing the harness.
- As models get more capable, harness functions get absorbed into the model — better native planning, self-verification, and long-horizon coherence requiring less context injection — yet harness engineering stays useful, just as prompt engineering does.
- Harnesses do two jobs: patch over model deficiencies, and engineer systems around model intelligence (well-configured environment, right tools, durable state, verification loops) that make any model more efficient regardless of base intelligence.

---

## Post-training with the harness in the loop

Today's agent products like Claude Code and Codex are post-trained with models and harnesses in the loop. This helps models improve at actions that the harness designers think they should be natively good at like filesystem operations, bash execution, planning, or parallelizing work with subagents.

This creates a feedback loop. Useful primitives are discovered, added to the harness, and then used when training the next generation of models. As this cycle repeats, models become more capable within the harness they were trained in.

**Covers:** post-training loop and native-skill targets

## Overfitting and generalization side effects

But this co-evolution has interesting side effects for generalization. It shows up in ways like how changing tool logic leads to worse model performance. A good example is described here in the Codex-5.3 prompting guide with the apply_patch tool logic for editing files. A truly intelligent model should have little trouble switching between patch methods, but training with a harness in the loop creates this overfitting.

But this doesn't mean that the best harness for your task is the one a model was post-trained with. The Terminal Bench 2.0 Leaderboard is a good example. Opus 4.6 in Claude Code scores far below Opus 4.6 in other harnesses. In a previous blog, we showed how we improved our coding agent Top 30 to Top 5 on Terminal Bench 2.0 by only changing the harness. There's a lot of juice to be squeezed out of optimizing the harness for your task.

| Claim | Detail from chunk |
|---|---|
| Overfitting example | Codex-5.3 prompting guide, apply_patch tool logic for editing files |
| Leaderboard evidence | Terminal Bench 2.0 Leaderboard: Opus 4.6 in Claude Code scores far below Opus 4.6 in other harnesses |
| Harness-only gain | Coding agent improved Top 30 to Top 5 on Terminal Bench 2.0 by only changing the harness |

**Covers:** generalization side effects and Terminal Bench 2.0 evidence

## Where harness engineering is going

As models get more capable, some of what lives in the harness today will get absorbed into the model. Models will get better at planning, self-verification, and long horizon coherence natively, thus requiring less context injection for example.

That suggests harnesses should matter less over time. But just as prompt engineering continues to be valuable today, it's likely that harness engineering will continue to be useful for building good agents.

It's true that harnesses today patch over model deficiencies, but they also engineer systems around model intelligence to make them more effective. A well-configured environment, the right tools, durable state, and verification loops make any model more efficient regardless of its base intelligence.

Harness engineering is described as a very active area of research used to improve the harness building library deepagents at LangChain. Open problems being explored:

- orchestrating hundreds of agents working in parallel on a shared codebase
- agents that analyze their own traces to identify and fix harness-level failure modes
- harnesses that dynamically assemble the right tools and context just-in-time for a given task instead of being pre-configured

> "The model contains the intelligence and the harness is the system that makes that intelligence useful."

**Covers:** future absorption of harness into models, enduring value, and open research problems
