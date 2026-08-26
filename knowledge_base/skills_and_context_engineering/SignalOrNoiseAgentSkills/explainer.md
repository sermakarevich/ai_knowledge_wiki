> [[index|Wiki]] | [[summary|Summary]]

# Signal or Noise? A Benchmark Study of Agent Skills in Web Development — In Plain Language

## What is this about?

Imagine you hire a new employee and, before every single task you give them, you hand them a laminated cheat-sheet: "here's how we name our buttons, here's a pattern we like, here's a mistake people commonly make, here's a worked example." That cheat-sheet is what AI researchers call an **Agent Skill** — a page of instructions and examples fed to an AI coding assistant at the start of every task, so it follows house conventions instead of guessing.

The obvious assumption is that more guidance can only help. This paper tests that assumption directly, using four different AI coding assistants and 31 real, publicly-published cheat-sheets, on 50 realistic website-building projects. The surprising result: on average, handing over the cheat-sheet makes the AI assistant *worse* at the job — not slightly worse, and not for free either, since reading the extra page costs real time and money (measured as "tokens," the units an AI is billed and slowed down by).

## Why does it matter?

Every time you paste extra instructions into an AI's prompt, two things happen at once: the AI gets more information, and the prompt gets longer. A longer prompt is not free — it can distract the AI, and it definitely costs more to process. If a cheat-sheet actually helps, that cost is worth paying. If it doesn't, you're paying for both the distraction *and* the extra bill. Most people who attach cheat-sheets to AI assistants never separate these two effects — they just see "did it get better with the cheat-sheet" and never ask "would it have gotten just as much worse from *any* equally-long piece of paper, useful or not?"

## How does it work?

The researchers ran the same task four different ways for each (cheat-sheet, project) combination, to cleanly separate causes:

1. **No cheat-sheet at all** — the AI's natural baseline performance on the task.
2. **The matching cheat-sheet** — the AI gets the cheat-sheet that's actually relevant to this project (e.g. a React cheat-sheet on a React project).
3. **A random, equal-length cheat-sheet** — the AI gets a cheat-sheet about something completely irrelevant to the project, but exactly as long (within 5%) as the real one. This is the trick that makes the study rigorous: if performance drops just as much with an irrelevant cheat-sheet as with the real one, the problem isn't the cheat-sheet's *content* — it's simply that the prompt got longer and the AI got distracted (**length-matched control**).
4. **A cheat-sheet with one section removed at a time** — a "leave-one-out" test that isolates whether it's the dos, the don'ts, or the example code doing the work (or the harm).

Running conditions 1 and 3 side by side is what lets the researchers tell whether a Skill's effect is really about its *content*, or just about how much extra text got stuffed into the prompt.

They then measured, for each AI model, how many tasks it solved correctly on the first two tries (**Pass@2**), how far it got through a 20-step chain of related tasks before failing (**Task Completion Depth**), and how many extra tokens it burned.

The headline finding: with the real, relevant cheat-sheet, all four AI models did *worse* on average than with no cheat-sheet at all, and cost 72% to nearly 400% more tokens to do it. Only 17–36% of cheat-sheet/project pairings actually helped. And the reason splits into two camps: two of the models (Claude Sonnet and Qwen) got worse mostly just because the prompt got *longer* — an irrelevant cheat-sheet of the same length hurt them almost as much. The other two models (GPT-5.1 and DeepSeek) weren't bothered by extra length, but the specific *content* of the cheat-sheet actively misled them.

One especially counterintuitive detail: the harm was worst on **easy tasks the AI already knew how to do**, not hard ones. The mechanism (nicknamed "retry lock-in" by the paper's reasoning): AI assistants get two attempts at each task, and a small mistake on the first try is usually fixable on the second. But if the cheat-sheet locks the AI into one particular way of naming or structuring something, that "fix" option disappears — the AI keeps making the same cheat-sheet-approved mistake on the retry too, and the whole task chain stalls there.

## Where can this be used?

- **Any team deploying AI coding assistants with attached style guides, playbooks, or "skill" documents** should test whether the guide is actually helping *their specific model*, rather than assuming a cheat-sheet that worked for one AI model or one project will work everywhere.
- **Marketplaces or libraries of AI-agent instructions** (skills, playbooks, system-prompt add-ons) should report per-model results, not one blanket "this works" rating.
- **Anyone tuning system prompts or RAG-injected context** for an AI application faces the same length-vs-content confound this paper isolates — it's a useful diagnostic technique well beyond web coding.

## Conclusions & takeaways

A cheat-sheet for an AI coding assistant is not automatically good. It's a bet on one specific (cheat-sheet, project, AI model) combination, and that bet frequently loses — especially on easy tasks and especially when different AI models are involved, since a cheat-sheet that helps one model can actively hurt a different one on the identical job. The paper's fix is not "don't use cheat-sheets" — it's "test each combination before deploying it, and reconsider handing them out by default." The cheapest, most reliable part of a good cheat-sheet turned out to be its "don't do this" warnings; example code was the most expensive part and the least reliably helpful, hurting the strongest AI model even while it helped weaker ones.

**Honest limitation:** this study measured functional correctness (does the code pass automated tests) — not whether the cheat-sheet made code more readable, more accessible, or easier for a human reviewer to review. A cheat-sheet could lose on this benchmark's metric while still improving things the benchmark didn't measure.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Agent Skill | A reusable instruction document (plus optional example files) fed into every prompt of an AI coding session, like a cheat-sheet for house conventions |
| Pass@k | Whether the AI got a correct, test-passing answer within k attempts (here k=1 or 2) |
| Task Completion Depth (TCD) | How many steps into a 20-step chain of related tasks the AI got before its first unrecoverable failure |
| Length-matched control | Swapping in an irrelevant document of the same length, to check whether a change in performance is caused by the document's content or simply by the prompt getting longer |
| Content effect | The part of a performance change attributable to what the document actually says, once the length effect has been subtracted out |
| Leave-one-out (slice) ablation | Removing one section of a document at a time (e.g. just the example code) to see which section is doing the work |
| Retry lock-in | A cheat-sheet fixing a superficial choice (like a naming pattern) so rigidly that the AI's usual "try something different on the second attempt" recovery strategy stops working |
| Core (Skill, project) pair | A cheat-sheet/project combination that human experts judged genuinely relevant (e.g. a React guide on a React project), as opposed to an obvious mismatch |
| Token overhead | The extra cost (in the units AI usage is billed/measured by) of processing the longer, cheat-sheet-augmented prompt |
| Workspace-aware injection | Putting only the main instruction file in the AI's prompt and placing any extra example files in its working folder instead, so prompt length stays controlled and comparable |
