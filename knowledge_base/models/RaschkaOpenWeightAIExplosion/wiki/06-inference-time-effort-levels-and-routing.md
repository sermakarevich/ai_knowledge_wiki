> [[../index|Wiki]] | [[../summary|Summary]]

# Inference-Time Effort Levels and the Case for Automatic Routing

This page covers a segment where Raschka lays out how modern model families (proprietary and open-weight alike) are actually configured along two independent axes — model size and inference-time "effort" level — and argues that choosing between them is currently a manual, gut-feeling-driven user decision that should instead be delegated to the harness. He grounds the effort-level mechanism in his same-day reading of the Kimi K3 technical report (token-budget penalties in RLVR, per-effort "specialist" training, and distillation into one selectable release model), notes this system-prompt-selectable pattern already existed in GPT-OSS, and connects it to an adjacent idea Hugo raises just before — orchestrators like Fable routing tasks across different models (Opus, Sonnet, even GPT models from inside Claude Code).

## Fable, Routing, and the Segue Into Effort Levels

Just before this segment, Hugo frames model/size choice as something increasingly handled by orchestration tools rather than by the user directly: "the frontier models are getting better at routing," and "Fable is a fantastic orchestrator and great at routing things to tasks to... the correct model, whether it's Opus or Sonnet" [42:19]. He adds a concrete example from a guest ("Ship") coming on his show, who "built a runner inside Claude Code for herself or adjacent to Claude Code, which will... get Fable to send tasks to GPT models among other things" [42:19]-[43:05]. Raschka calls this "a good segue" into the topic of effort levels [43:05], treating cross-model orchestration and within-model effort selection as adjacent instances of the same underlying problem: deciding, automatically, which computational resource to spend on a given task.

## The Disappearing GPT-5.5 Auto Mode

Raschka recalls that "when GPT 5.5 came out, there was this auto mode like routing to or like at least setting the inference scaling budget like the effort level for reasoning" [43:05]. He reports that this appears to have since been removed: "I think they moved away from that again... I haven't seen that in the UI anymore. In my at least in my UI, it's not there anymore. You have to manually select the effort level" [43:05]. He frames this as his own current, unverified UI experience rather than an announced product change.

## Two Independent Levers: Model Size and Effort Level

Raschka generalizes the pattern beyond GPT: "even like a proprietary model like Claude or GPT, you have different model sizes... you as a user you have to choose between do I use sole, terra, luna different sizes" — using placeholder names to illustrate the tier structure [43:51]. He notes these size tiers are "all like independently trained except the smaller ones are kind of distilled from the larger ones," and that they trade off "costs and tokens per second and of course also performance in terms of solving the problem" [43:51].

Orthogonal to size, "for each of them you also have effort levels like medium, high, extra high, ultra and so forth" [43:51]. He summarizes: "there are basically two levers moving forward like making bigger models, but then also the effort level can be controlled with RLVR" [43:51].

## Effort-Level Training Per the Kimi K3 Report

Raschka explains the effort-level mechanism "based on the report I just skimmed today," i.e. the Kimi K3 technical report [44:38]. The core device is a token-budget penalty: "they have a budget token budget. So they say for example, you can only have so and so many tokens. If you exceed that, you get a reward of minus one in the RLVR and that the model is discouraged from doing that" [44:38] — i.e., exceeding the budget is directly penalized during RLVR training, discouraging excessive output length.

On top of this, distinct "specialists" are trained: "they have different they call them specialists. They have one for very long high effort, very long outputs, some for medium, some for light" [44:38]. Combined with the domain dimension he raises elsewhere in this stretch of conversation (math, coding, general knowledge), this yields — by his rough recollection — on the order of three effort specialists crossed with three domains, i.e., roughly nine specialists in total. These specialists are not shipped separately: "they distill that down into one final model and then you as a user you can select that with a system prompt" [44:38].

He is explicit that this selectable-mode pattern is not novel: "this is not new. Most of the models do that even back the GPT-OSS model from OpenAI had that in the system prompt" [44:38].

## The Problem: This Is Currently a User Decision

Raschka states the core issue plainly: "you as the user you kind of have to decide... So you have to decide what size even if you are staying within one provider, what size do I use? What effort do I use?" [45:24]. The mechanism people currently use to make this decision is experience-based intuition: "you have to kind of like develop... a kind of a gut feeling like when you... use[d] cloud for this one time line, you kind of like intuitively know okay this is like a high end model task" [45:24].

He calls this suboptimal: "it is kind of tedious... but it's maybe also not optimal because we human have biases where we have a gut feeling. It can be a very good gut feeling, but we might also be just wasting compute on simple problems by just always using the most expensive model" [45:24].

He then distinguishes the two failure directions and their relative costs. Under-provisioning (starting too small) is, in his view, the more benign failure: "that is usually easier to correct because... if you start with a simple model, you get better results, you just switch to the bigger one and hope fingers crossed that it works. I think that is more natural" [46:10]. Over-provisioning is the costlier mistake: "you use the most expensive model because you only think that solves it and then you just waste a lot of waiting time on the results if you didn't [sic] money and usages and stuff" [46:10].

## The Proposed Fix: Push the Decision Into the Harness

Raschka's proposed direction is to move this decision out of the user's hands entirely: "I do think would be best handled in the harness itself. Like, the harness should [decide] based on the context. So, not like the user... turning the knob. It should be a harness feature, in my opinion" [46:10]. The decision mechanism itself could take several forms — "based on how many loops... it could be a different model. Could be a heuristic or a mix I think, ideally, a mix of the two" — and should ideally draw on more than just the immediate task: "based on the task, but also not just the task, but the history, the context and everything to decide what model to use" [46:57].

Crucially, he wants this to be dynamic within a single session, not a one-time choice made up front: "change it... inside a loop. Like, we can steer an LLM... notice... this was not powerful enough. And you have the context from the LLM, you can just pass it to the... other model or... change the system prompt. Like, steering, you can say from low effort to high effort. You... still use the same model" [46:57]. That is, the harness could either escalate to a different model or keep the same model but raise its effort level mid-task, passing accumulated context between calls either way.

His closing caveat is that this remains unbuilt: "that I think is something no one is doing it as far as I know. Maybe, please correct me if I'm wrong, but I think... because it's hard, right? It's not easy. It's not trivial, but I think that is a good optimization in the future" [46:57]-[47:43]. Hugo agrees he hasn't seen it either and would be "very excited" to [47:43].

---

**Covers:** [40:46]-[49:15] segment of the transcript (topic: effort levels and routing)
