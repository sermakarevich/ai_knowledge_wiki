> [[../index|Wiki]] | [[../summary|Summary]]

# Pre-Training and Post-Training Trends

Prompted by Hugo's observation that the field's attention seems to be swinging from post-training and inference-time scaling back toward pre-training, Raschka lays out what has actually changed on both sides of the training pipeline — with an upfront caveat about how much of this is verifiable versus inferred from ambiguous technical reports. On pre-training, he points to synthetic data as a moderate-dose "kickstart" mechanism and to a roughly 30-trillion-token scale that he recalls as 2-3x last year's typical size. On post-training, he describes the shift from a simple SFT-plus-long-context pipeline to a longer, multi-stage, back-and-forth process built around agentic trajectory data. The segment closes with an unrelated but revealing habit: Raschka's use of a trivial "what is 1+1" prompt as an informal test of a freshly-set-up model's reasoning efficiency, not just its correctness.

## Why Architecture, Not Training Details

Responding to Hugo's question about the pre-training/post-training pendulum [61:36], Raschka first explains why his own commentary throughout the conversation leans on architecture rather than training procedure: "I could just talk about the architecture, right? But the reason why I also talk a lot about the architecture is because that's known" [62:24]. Training, by contrast, is much less transparent: "for the training not everything is so transparent... it's not what it used to be... back in academia 20 years ago where everything was fully reproducible and clear" [62:24].

He qualifies this further — technical reports do mention training details, but often ambiguously: "some of the stuff is mentioned, but it's not always... sometimes it's ambiguous. They say it in a sentence, but it's not 100% spelled out" [62:24]. His example is the effort-level "specialists" mechanism (covered in depth on the [[06-inference-time-effort-levels-and-routing|effort levels and routing]] page): for Kimi K3 specifically, he recalls the report being "pretty clear" — "three specialists for the effort levels... and then for each domain like math, coding, and general knowledge... nine in total" [62:24]. But he notes that other papers describing the same kind of specialist training leave the breakdown genuinely unclear: if a report says six specialists, "you don't know was it like 3 by 3 or was it... six specialists could also be six... a light, medium, hard effort, and then it could be math, coding, and so on. So, like, is it combined?" [62:24]-[63:10]. His conclusion: "a lot of that is speculation also sometimes when you read these papers" [63:10].

## Synthetic Data in Pre-Training: a Kickstart, Not a Shortcut

Turning to what has actually changed in pre-training, Raschka notes there is now "a lot of more good stuff in the pre-training data" — for example, "5 years ago, 4 years ago, you had probably very few chain-of-thought type of data in the training set," whereas now models themselves "produce synthetic data also for the pre-training" [63:10]-[63:56].

He is explicit that this is not inherently a bad practice at moderate levels: "synthetic data is not necessarily bad in certain amounts. It's almost like kickstarting the model in a sense that if you have... messy data, you learn everything from scratch from messy data, but if you have a portion of high-quality data, even if it's synthetic," the model gets to good style and formatting faster [63:56]. He immediately flags the standard counterargument and agrees with it as a boundary case: "if we only train on synthetic data, we will never improve. It's kind of like going in circles" [63:56]-[64:42]. The synthetic-data value, in other words, is specifically in a *mixed* regime, not a closed self-training loop.

The practical payoff of getting the mix right is a baseline reached with less pre-training effort: "if you mix it right, you can probably not get the model to outperform the models that have been trained on bigger pre-training sets... but you can get to a baseline quicker. Like, you need fewer iterations, fewer data to get to a certain baseline level" [64:42]. He connects this directly to resource allocation: "then you can focus more on the post-training also... you free up the compute. You are basically less wasteful with pre-training" [64:42]-[65:28].

## Pre-Training Dataset Scale: Roughly 30 Trillion Tokens

Raschka gives a scale estimate, hedged as an imprecise recollection rather than a verified figure: "I don't recall from the Ki[mi] report just too many numbers... or maybe I'm conflating it with another recent model I looked at, but I think 30 trillion is currently like... the common size nowadays" [65:28]. He estimates this as roughly "two to three times bigger than last year, for example" [65:28].

He frames this alongside the synthetic-data point as one of several simultaneous levers rather than a single explanation: pre-training data sets are getting larger *and* better-mixed at the same time — "it's also better pre-training data, more synthetic in there, better mixes... it's all being improved at the same time. So, it's not just... making a bigger [model]... multiple levers to pull" [65:28].

## Post-Training's Evolution Into a Multi-Stage Pipeline

Raschka describes how post-training used to be comparatively simple: "it used to be just... supervised fine-tuning and then... long context fine-tuning... because you don't have infinite long context data that is good quality" [66:15]. Agentic use changes this: "now with agents, you kind of do again. You know, like you have a lot of trajectories you can train on" [66:15].

He then walks through the resulting pipeline, which recombines several techniques already discussed earlier in the conversation:

- **RLVR** on the agent harness — "just if it can solve the problem" [66:15], the same mechanism discussed on the [[04-harness-model-coupling-and-overfitting|harness-coupling page]].
- **SFT-based distillation** from successful trajectories — "kind of like a distillation from... the long collected successful traces from other models or even your own model. You also use SFT for that" [66:15].
- **SFT for effort modes** — a distinct stage tied to training the effort-level specialists described above and on the effort-levels page.
- **A preference-tuning round (RLHF)** — "doing another... preference tuning with... RLHF" [67:03].
- **Potentially another RLVR round** afterward — "you may do another RLVR round" [67:03].

Raschka is explicit that none of the individual techniques is new — "it's not a new technique in there in a sense, but it is more complicated... pipeline. It's more steps" [67:03] — and that the stages recur rather than running once in a clean sequence: "there are multiple stages going back and forth now again, too. You have SFT, RLVR, then going back to SFT for effort modes, some distillation, then doing another... preference tuning... and you may do another RLVR round" [66:15]-[67:03].

## The "What Is 1+1" Efficiency Probe

Earlier in the conversation, discussing the satisfaction of getting a from-scratch or freshly-set-up local model working, Raschka describes a personal ritual: "there is like it's usually frustrating but if it doesn't work... and then it works and then you understand it, it's just like this pure joy dopamine hit" [56:13]. This extends to trying out a new local model: "that's the same with running a local model — you have the setup and you don't fully know [if it works], and then you ask it [a] simple prompt. I usually... do... what is one plus one... and then I use it as my first prompt and then it starts answering... I'm like super happy... it actually works" [56:58].

He then reframes the prompt as more than a sanity check — it is also a rough efficiency probe: "the one plus one is actually... a stupid prompt, but it is actually also quite useful because... if we go back a few years a model would just say two." He contrasts this with older-generation reasoning models: "if we go forward a few years and maybe we are... [at the] beginning of 2025... if you ask a model what is one plus one it would not say two, it would give you a whole 2000 token answer, like a deep seek[R1] model" [56:58]-[57:44]. Current-generation reasoning models, by contrast, answer efficiently: "the newer models again, they would answer two... the smarter reasoning models[.] but the first generation of reasoning models... would really [give a] 2000 token answer, and that's also not good. So, you want a model that... can be... efficient when it needs to be" [57:44].

He adds one more efficient-answer path beyond a short direct response: "or use a tool also in that case, by the way" [57:44] — Hugo completes the thought, and Raschka confirms the idea of getting the model "to write some Python code and to execute it" rather than reasoning the trivial arithmetic out in tokens [57:44]-[58:29]. The prompt's value, in other words, is as an informal signal of a model's or generation's reasoning efficiency — how much unnecessary token overhead it spends on something that needs none — rather than a test of correctness, which virtually every model already passes.

---

**Covers:** [61:36]-[67:03] and [56:13]-[58:29] segments of the transcript (topic: pretraining/post-training trends)
