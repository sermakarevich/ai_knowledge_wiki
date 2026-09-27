> [[index|Wiki]] | [[digest|Digest]]

# Self-Refine: Iterative Refinement with Self-Feedback — In Plain Language

## What is this about?

Imagine a writer who drafts an article, then puts on an editor's hat to
write margin notes ("this paragraph is slow, reorder it"), then puts the
writer's hat back on to fix the draft using those notes. They repeat this
a few times until the piece reads well.

Self-Refine does the same thing with a single large language model
(LLM — a large neural network (a computer program inspired by the brain
that learns patterns from data) trained on text that writes word by word).
One frozen model (frozen means its internal settings are locked, no extra
training happens) plays all three roles in a loop: it writes a first draft,
critiques its own draft in plain words, and then rewrites the draft using
that critique.

Across 7 different tasks, this simple loop lifts strong models like
GPT-3.5, ChatGPT, and GPT-4 by about 20% absolute on average, without any
extra training.

## Why does it matter?

First, the gains are broad. They hold across all base models and all
7 tasks tested. For example, GPT-4 with Self-Refine improves over plain
GPT-4 by 8.7 points on code optimization (making programs run faster),
by 49.2 points on dialogue response preference (25.4% to 74.6%), and by
30.0 points on constrained generation (15.0% to 45.0%).

Second, it is cheap and practical. No new training data and no retraining
are needed — just carefully written prompts (written instructions with
a few examples). On code optimization it uses at most 4 tries, compared
to 16–32 tries for rival methods, and still reaches 36.0% optimized programs.

Third, blind human judges (judges who do not know which answer came from
which method) prefer Self-Refine by wide margins. For sentiment rewriting
they pick Self-Refine 75.00% of the time versus 21.43% for the plain
baseline. It also beats the closest prior method on math problems
(55.7% versus 45.9%).

## How does it work?

1. **Write a first draft.** The model gets a generation prompt (`p_gen` —
   instructions plus a few input-output examples) and produces an initial
   answer, called y0. Example: a slow program, a first-draft reply, or
   a sentence covering only some required words.
2. **Critique the draft.** The same model gets a feedback prompt (`p_fb` —
   the input, the current draft, and examples of good critiques) and writes
   specific, actionable feedback. Good feedback says *what* is wrong and
   *how* to fix it, like "slow for-loop, use the formula n(n+1)/2".
3. **Rewrite using the feedback.** The model gets a refine prompt
   (`p_refine` — the input, the draft, and the feedback) and produces an
   improved version, y1.
4. **Repeat a few times.** Steps 2–3 loop for up to 4 rounds, or stop early
   when the feedback contains a stop signal (a phrase meaning "this looks
   good, no more changes needed").
5. **Keep the best version where quality jumps around.** Most tasks just
   take the last version, since scores climb each round. For acronyms,
   where quality can go up and down, the method keeps the highest-scoring
   round.
6. **Most progress comes early.** On constrained generation, scores rise
   from 29.0 to 40.3 after one round, then 46.7, then 49.7. Code and
   sentiment tasks show the same pattern: big first-step jump, then
   smaller gains.

The feedback quality is load-bearing (it carries most of the weight).
Replacing specific feedback with generic "improve this" feedback drops
sentiment reversal from 43.2 to 31.2 and acronym generation from 56.4
to 48.0. Removing feedback entirely collapses sentiment reversal to 0.

## Where can this be used?

- **Code optimization (faster programs):** rewriting slow programs into
  faster ones, reaching about 15–16% optimized with roughly 3x speedup in
  one setup, and 36.0% with GPT-4.
- **Code readability (clearer programs):** renaming variables, adding
  comments, and splitting code into functions. At one setting it beats
  human rewrites written from 60 examples.
- **Dialogue responses (better chat replies):** scoring drafts on 10 traits
  such as relevant, informative, interesting, consistent, and helpful, then
  rewriting low-scoring replies (for example, a 17/30 reply) into strong
  ones (30/30).
- **Math reasoning (word problems):** writing solutions as Python programs
  (step-by-step code that computes the answer) and looping to catch errors,
  climbing from 71.34% to 76.19% over rounds 0–4 when a correctness check
  gates the loop.
- **Sentiment reversal (flipping tone):** rewriting a glowing review into a
  strongly negative one (or the reverse) while keeping it natural, reaching
  93.6% accuracy on negative targets.
- **Acronym generation (short names from titles):** improving bad guesses
  like STSLWN into Seq2Seq for "Sequence to Sequence Learning with Neural
  Networks," judged on pronunciation, spelling, relation to the title,
  connotation, and familiarity.
- **Constrained generation (one sentence, many required words):** the hard
  version demands 20–30 concepts in a single coherent sentence (normal
  tests use only 3–5), and Self-Refine wins clearly on coverage and
  commonsense.
- **Beyond benchmarks (practical demo):** iteratively refining website
  layouts, such as an ice-cream parlor page or a photosynthesis explainer,
  from plain-word feedback.

## Conclusions & takeaways

Self-Refine is a simple loop — draft, critique, fix, repeat — that reliably
improves strong models without retraining, with most of the benefit in the
first one or two rounds.

It has honest limits. Math barely moves on its own (+0.0 to +0.2 points)
because the model cannot spot its own mistakes — ChatGPT says "everything
looks good" on 94% of math cases. An outside correctness signal restores
5%+ gains. When drafts fail, the feedback is usually at fault: about 33%
of failures mislocate the error and 61% suggest a wrong fix, while only 6%
come from the rewriter mishandling good feedback. The bright side is that
the rewriter is forgiving: it still fixes the answer from partly wrong
feedback in 33% of successes.

It also needs a strong instruction-following model (a model good at obeying
formatting and multi-step directions). A smaller model, Vicuna-13B, cannot
reliably produce feedback in the required format and fumbles rewriting even
when given perfect feedback. But pairing a weak writer with a strong
critic helps: Vicuna drafts plus ChatGPT feedback and rewriting jump math
accuracy from 24.18% to 40.5%.

## Jargon decoder

| Term | What it means in plain language |
| ---- | ------------------------------- |
| LLM (large language model) | A large neural network trained on text that writes answers word by word |
| Frozen model | A model whose settings are locked; it is used as-is, with no extra training |
| Few-shot prompt | Instructions plus a few worked examples showing the desired pattern |
| Generation (y0) | The model's first draft answer before any self-correction |
| Self-feedback | The model's own written critique of its draft, naming what to change |
| Refinement | The rewrite step that applies the feedback to produce a better version |
| Iteration | One full pass of critique plus rewrite; Self-Refine uses up to 4 |
| Stop signal | A phrase in the feedback meaning the answer is good and looping can end |
| Oracle feedback | Perfect or outside correctness information, used to test the upper limit |
| Ablation | A test that removes one piece (like feedback) to see how much it mattered |
| Blind human A/B eval | Human judges compare two answers without knowing which method made each |
| GPT-4 as judge | Using GPT-4 with fixed scoring instructions as an automatic grader |
