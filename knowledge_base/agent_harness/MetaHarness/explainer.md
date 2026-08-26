> [[index|Wiki]] | [[summary|Summary]]

# Meta-Harness — In Plain Language

## What is this about?

Imagine you hire a brilliant chef (a large language model, or LLM — an AI system trained to read and write text). The chef is very good at cooking, but how good the final meal is doesn't just depend on the chef's skill — it also depends on the kitchen: how ingredients are organized, what's within reach, what recipe cards are pinned to the wall, and what gets thrown away versus kept for later. In AI systems, that "kitchen" is called a **harness**: all the code around the AI model that decides what information it gets to see, what it remembers from past attempts, and how its answers get checked. This paper shows that changing only the kitchen — keeping the same chef — can swing performance by 6x. Yet most people still design kitchens by hand, tweaking them based on gut feeling and trial and error.

This paper builds a system, called Meta-Harness, that designs the kitchen automatically. It works by hiring a second AI — one that can write and edit code — and giving it a very simple instruction: "here is a folder containing every kitchen layout we've tried so far, along with how well each one cooked, and a full replay of everything that happened during each meal. Go look through it and design a better kitchen." No pre-built strategy, no forced summary — the AI decides for itself what to look at.

## Why does it matter?

Right now, building a good AI application means paying a human engineer to sit down, look at where the AI is failing, and manually redesign its memory, retrieval, and prompting logic. That's slow, expensive, and doesn't scale as new, more capable base models come out every few months — because someone has to redo the kitchen design each time. If a system can instead design and refine its own kitchen automatically, engineering effort shifts from "hand-tune this exact setup" to "build a good enough automated search," which keeps working as the underlying chef (model) keeps improving.

## How does it work?

Think of it as a loop with three steps, repeated over and over, like a chef running dozens of test dinners and keeping detailed notes each time:

1. **Propose.** The "kitchen designer" AI reads through a folder containing every past kitchen layout's code, its scores, and a full replay log of what happened when it was used — then writes a new kitchen layout (a new harness).
2. **Evaluate.** That new kitchen is paired with the chef (the fixed underlying model) and run through a batch of test dinners (evaluation tasks), producing a score plus another detailed replay log.
3. **Store.** Everything from that round — the new kitchen's code, its score, and its replay log — gets saved into the same folder, growing the pile of past experience for the next round.

The key trick is that the designer AI is never handed a squeezed-down, one-paragraph summary of "what went wrong." It gets the *raw* replay logs and can use ordinary file-searching tools (like `grep`, which searches text, and `cat`, which prints a file) to dig into exactly the detail it needs — sometimes checking dozens of past attempts before writing the next one. That turns out to matter a lot: a version of the system given only scores, or only AI-written summaries, performs far worse than the version given the raw logs.

## Where can this be used?

- **Customer-support or classification bots** that need to remember and use past examples well (the paper tests this on legal case classification, disease-symptom prediction, and patent classification).
- **Research-assistant tools** that retrieve relevant prior work or solved problems to help answer hard questions (tested here on olympiad-level math problems, using retrieval from solved problem archives).
- **Coding assistants** that need to work autonomously on long, multi-step tasks in a terminal (tested on TerminalBench-2, where AI agents must complete real software tasks end-to-end).
- More broadly, anywhere an AI system's surrounding "plumbing" — memory, retrieval, prompt construction — currently gets hand-tuned by an engineer.

## Conclusions & takeaways

- The harness genuinely is a lever as powerful as the model itself, and it's now automatable, not just tunable by hand.
- The magic ingredient isn't a clever search algorithm — it's giving the "kitchen designer" AI *unfiltered, full access* to what happened before, and trusting it to decide what's relevant, rather than pre-digesting the information for it.
- This only works because coding-agent AIs recently became good enough to navigate large piles of files and reason about them — the authors note this approach wasn't practical even a year earlier.
- A caveat worth remembering: everything here was tested with one particular "kitchen designer" AI (Claude Code). Whether cheaper or different coding-agent tools work as well is still untested.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Harness | The code wrapped around an AI model that decides what information it stores, retrieves, and is shown — the "kitchen" around the "chef" |
| Proposer | The AI that designs new harnesses, based on reading past attempts |
| Coding agent | An AI system that can not just chat, but actually run commands, read/write files, and edit code |
| Text optimizer | An earlier category of automatic tools (like GEPA, AlphaEvolve, TextGrad) that try to improve a prompt or piece of text using feedback, but only look at compressed summaries or scores |
| Execution trace | A detailed replay log of everything that happened during one run — every prompt shown, every tool used, every response given |
| Pareto frontier | The set of "best trade-off" options when you care about two things at once (e.g., accuracy vs. cost) — no other option beats one on *both* dimensions simultaneously |
| Search set / test set | The batch of practice problems used to grade candidates during the search (search set) vs. a separate, never-touched final exam used only at the very end (test set) |
| Out-of-distribution (OOD) generalization | How well a discovered harness performs on brand-new tasks it was never tuned on, not just the ones used to design it |
| Retrieval-augmented | An AI setup that looks up relevant past examples or documents before answering, instead of relying purely on what it already "knows" |
| BM25 | A classic text-search algorithm (older than modern AI) that ranks documents by keyword overlap, used here as the retrieval engine inside a discovered math harness |
| TerminalBench-2 | A benchmark of 89 hard, realistic software tasks that an AI agent must complete autonomously in a computer terminal |
| Confound | When two changes are bundled together and you can't tell which one caused an effect — the paper's case study shows the AI figuring out and untangling exactly this |
