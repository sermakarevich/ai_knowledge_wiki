> [[index|Wiki]] | [[digest|Digest]]

# Toolformer: Language Models Can Teach Themselves to Use Tools — In Plain Language

## What is this about?

Imagine a smart student who has memorized a huge library, but the library is a few years old. Ask about something recent, a tricky calculation, or a language they barely know, and they will guess — confidently, but often wrong. That is a language model working from memory alone.

Toolformer is a way to teach that student to reach for tools: a search engine for facts, a calculator for math, a translator for other languages, and a calendar for today's date. The key idea is that the model teaches itself when to use each tool.
People show only a handful of examples, and the model then practices on a large collection of ordinary text, tries out tool calls, and keeps only the ones that actually help it predict what comes next.
No new vocabulary or special architecture is needed — the calls are written with plain symbols so they blend into normal text.

## Why does it matter?

Language models have four predictable weak spots: they invent facts, they struggle in languages with little training data, they make arithmetic mistakes, and they have no sense of what day it is. The usual fix is to build ever-bigger models, which is expensive and still leaves these gaps.

Toolformer shows a smaller model — GPT-J with 6.7B parameters in this paper — can beat much larger models (OPT-66B, GPT-3-175B) on factual, math, and date questions simply by calling the right tool at the right time. It does this in zero-shot tests, meaning no extra examples at test time: the model itself decides when, which, and how to call a tool. And it learns this without losing its general language ability.

## How does it work?

1. **Start with a few demonstrations.** For each tool, people write a handful of examples showing how a call looks inside normal text, using markers like `<API> call </API>`.
2. **Let the model try calls everywhere.** The model reads a large corpus of ordinary text. Wherever it thinks a tool call might fit (probability of `<API>` above a threshold), it proposes several candidate calls.
3. **Keep only calls that help.** Each candidate is scored: does inserting the call plus its result make the following words easier to predict (lower loss) than no call? Only calls that clear a filtering threshold are kept.
4. **Build an augmented dataset.** The kept calls are inserted into the original texts. The texts themselves are unchanged — they just gain useful tool uses.
5. **Finetune on the augmented texts.** The model trains on this enriched data, learning where and how to use tools while keeping its normal language skills.
6. **Use tools at test time.** When answering, the model writes normally until it emits the signal to call a tool. Decoding pauses, the tool runs, the result is inserted, and the model continues with the answer.

The five tools in the paper are: a factoid question-answering system, a Wikipedia search engine, a four-operation calculator, a translator into English covering 200 languages, and a simple calendar that returns the current date.

## Where can this be used?

- **Factual questions.** Answering who-did-what style questions with a search or QA tool instead of guessing from memory.
- **Math word problems.** Solving school-style problems (the ASDiv, SVAMP, MAWPS benchmarks) by handing arithmetic to the calculator.
- **Open-domain questions.** Looking up Wikipedia passages to answer general knowledge questions.
- **Other languages.** Translating a non-English question into English first, then answering.
- **Date questions.** Checking the calendar or looking up facts to answer "what day" and "when" style queries.
- **Any assistant setting.** Anywhere a chatbot would otherwise guess a fact, botch a sum, or miss a date, a tool call can ground the answer.

A good rule of thumb from the paper: if a person would open a tab to check, the model probably should too.

## Conclusions & takeaways

- A 6.7B model that uses tools can beat models ten to twenty times larger on several factual and math tasks, with almost 100% tool use on those tasks.
- General language quality is preserved: with tools switched off, perplexity is the same as a baseline trained on the same data without tools.
- Tool ability only appears at scale — small models (124M, 355M parameters) gain nothing; it starts to work around 775M parameters.
- Honest limits: the model can make only one tool call per input, so it cannot chain steps like "check the date, then search". It cannot refine a search interactively, it is sensitive to how prompts are worded, sampling many candidate calls is wasteful, and it has no sense of tool cost.
- Translation helps every language tested, but side effects of finetuning mean it does not always beat the base model on multilingual questions.

## Jargon decoder

| Term | What it means |
| ---- | ------------- |
| Language model (LM) | A program that predicts the next word in a text, used to answer questions and write |
| Zero-shot | Answering a new task with no examples at test time, just an instruction |
| API call | Asking an outside tool to do something and return a result |
| Self-supervised | Learning from ordinary text without people labeling every answer |
| In-context learning | Showing the model a few examples in its input so it copies the pattern |
| Cross-entropy loss | A score for how surprised the model is by the real next words — lower is better |
| Perplexity | Another way to say average surprise on a text — lower means better language modeling |
| Filtering threshold | The minimum improvement a tool call must bring before it is kept |
| Finetuning | Extra training on special data to add a skill without starting over |
| GPT-J (6.7B) | The base model used here, with 6.7 billion adjustable settings |
