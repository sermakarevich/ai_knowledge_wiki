> [[../index|Wiki]] | [[../summary|Summary]]

# Harness-Model Coupling and the Overfitting Question

In this segment, Hugo Bowne-Anderson and Sebastian Raschka discuss the tight coupling between open-weight models and the agent harnesses built for them, prompted by a discussion of "steering" (interrupting and redirecting a running agent). Raschka describes his personal habit of always reaching for a model's native harness, Hugo raises the hypothesis that models and harnesses may be "overfitting to each other," and the two work through a plausible training-pipeline explanation (RLVR concentrated in one harness, SFT across harnesses only at the end), possible symptoms of that overfitting, and a concrete anecdote about Claude Code's token usage. The discussion closes with Raschka's "Pareto frontier" framing for both models and harnesses, and his admission that he relies on intuitive feel rather than formal benchmarking to judge a model-harness combination.

## Native Harness as Habit

The topic grows directly out of the preceding discussion of steering [21:28]-[22:59] — the ability to interject more instructions into an agent mid-task rather than waiting for it to finish. Raschka connects this to how "the harness supports contexts and how it uh manages context" [22:59]. He then describes his own workflow habit: despite trying different things, he has "muscle memory" and tends "to use the harness that comes with a model" — Qwen Code for Qwen, the Kimi CLI for Kimi models, and so on [22:59]-[23:44], even though it is possible to run these models inside other harnesses like Codex CLI or Claude Code "to some extent" [23:44].

His stated justification is empirical, not just habitual: "based on what I've been seeing in benchmarks, they are working better if you have them in the native harness" [23:44].

## The Overfitting Hypothesis

Hugo immediately picks up on this and names the underlying worry: "I think models and harnesses are maybe overfitting to each other" [23:44]. He clarifies the mechanism he suspects — models "perform better in benchmarks, but then on other tasks that are not benchmark tasks" they are worse, i.e., harness-specific benchmark performance may not generalize [23:44]. Raschka's reaction ("Ah... I see") signals this reframes something he'd only partly noticed as a benchmarks-based habit into a possible systematic bias.

Hugo pushes the hypothesis one step further into the training pipeline, asking "whether the models are kind of RLVR on their own harnesses and it just gets baked into the... weights" [23:44]-[24:30].

## The RLVR-then-SFT Training Hypothesis

Raschka engages with this directly, prefacing that "how people fine-tune on their harnesses" is "not so clear" from public information, and that he doesn't know the proprietary specifics of how frontier labs do it [24:30]. He mentions wanting to check the Poolside "Laguna" model's technical report as a possible source of transparency on this point [24:30].

Based on what he knows from colleagues, the general pattern he describes is: "it's mostly like you said RLVR on their own harness just for the trajectories to get going to train something... to make it intelligent. But then later at the end of that, you do the fine-tuning on harnesses, like some adjustments with... SFT... but that is like at the very end" [24:30]-[25:16]. In other words, "during the training basically, most of it was RLVR" and "that was in one harness" — so the model "has seen a lot of that harness basically." His conclusion: "you might be over-fitting to some extent, yeah" [25:16].

## Symptoms of Harness Overfitting

Hugo then asks the diagnostic question directly: if a model is overfit to a harness, "what would be like a hallmark of that? Would... they be using the wrong tools all the time?" and how would this differ from a model simply "memorizing things" [25:16]-[26:03]?

Raschka calls it "a good question" and offers two candidate symptoms [26:03]:

- **Incorrect tool use** — the model reaches for the wrong tool given the harness it's running in.
- **Longer reasoning loops** — even when the model uses "the correct tool," it "may use it... far too many times and shoot too many tokens," i.e., inefficient looping rather than outright wrong actions [26:03].

## The Claude Code Token-Usage Anecdote

Raschka supplies a concrete personal observation to anchor this: "Claude code is also notorious for that. I tried to use, for example, Claude 3.6 [sic, i.e. Claude Sonnet/Opus-era] in other harnesses besides Claude code, and I remember Claude code was using two or three times as many tokens as other harnesses" for comparable tasks [26:03].

He immediately adds an important caveat, however: this discrepancy is "not necessarily over-fitting" — "it's also just like how... efficient the harness compacts information, how much context it provides" [26:03]-[26:49]. That is, higher token usage in the native harness could equally reflect differences in context-management engineering (compaction strategy, how much repo/history context is stuffed into the prompt) rather than a trained-in behavioral bias from RLVR exposure.

## The Pareto Frontier Framing

Raschka generalizes this into a dual "sweet spot" problem [26:49]:

- **For models:** "what LLMs do I use for efficiency, like to get something done efficiently, what's the... sweet spot, the Pareto frontier?"
- **For harnesses:** the analogous question is "how much info do I really need — everything from that repo in context, or do I only need a few files?"

Both are optimization problems along a capability/efficiency axis, and combining them compounds the difficulty: finding "the good combination of model and harness" is itself a search problem, and it has to be redone whenever either side changes — "you do use that for a few months, and then the next model comes, and you have to start all over again" [26:49]-[27:36].

## Practical Approach: Feel Over Formal Benchmarking

Raschka is explicit that he does not run systematic evaluations himself: "I honestly don't really... benchmark things myself. I just use them, and... you kind of get a feeling, okay, this is not working well, this is working well." He does consult public benchmarks but doesn't rerun them, citing cost ("thousands of dollars") relative to the payoff [27:36].

His rule of thumb is time-based: "after half a day or day, you kind of get a feeling" for whether a model/harness combination is working, with the honest caveat that a bad feeling might just mean "maybe I'm not using it well" rather than the combination genuinely underperforming [27:36].

This same intuition-over-measurement theme recurs later in the conversation regarding model-size/effort-level selection (e.g., his remark that switching to a proprietary model for a task is "just like something a muscle memory" [40:46]), reinforcing that his harness judgments are part of a broader pattern of experience-based rather than benchmark-based decision-making.

---

**Covers:** [21:28]-[27:36] segment of the transcript (topic: harness-model coupling)
