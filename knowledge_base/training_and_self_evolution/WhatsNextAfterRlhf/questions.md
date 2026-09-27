---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: What's Next After RLHF? — Diogo Almeida, TypeSafe AI

### Q1. How does the speaker reframe the talk title, and why does he say the Claude Code era is not what's next?

> [!tip]- Answer
>
> He reframes "what's next after RLHF" as "what's next after the ChatGPT era," arguing Claude Code belongs to that same assistance era rather than a new one. Claude Code is still RLHF-based and human-in-the-loop assistance, so it cannot count as the post-assistance future. See [[wiki/01-whats-next-after-rlhf-intro|What's Next After RLHF — Talk Opening and Speaker Intro]].

### Q2. What credentials does the speaker claim, and what is his stated attitude toward ChatGPT?

> [!tip]- Answer
>
> He introduces himself (transcribed as "Tiago Almeida") as a co-author of GPT-4, ChatGPT, and RLHF / instruct GPT, saying his team basically invented post-training as a concept. He calls himself one of the few OpenAI people who "hates on" ChatGPT — loving it as a world-changing product while blaming minor decisions in its algorithms for much of the field's current state. See [[wiki/01-whats-next-after-rlhf-intro|What's Next After RLHF — Talk Opening and Speaker Intro]].

### Q3. What are the two extreme "cults" in the AI debate, and what puzzle does the speaker pose for them?

> [!tip]- Answer
>
> Cult one says AI is going insanely well, with every NLP benchmark crushed and autonomous operation time growing exponentially. Cult two says AI is going insanely poorly, a bubble of circular financing deals producing only chat apps. His puzzle: what single explanation accounts for unsolved math problems being solved while customer service still needs humans in the loop for dumb tasks. See [[wiki/01-whats-next-after-rlhf-intro|What's Next After RLHF — Talk Opening and Speaker Intro]].

### Q4. What is the assistance-vs-automation divide, and what business lesson follows from it?

> [!tip]- Answer
>
> Left-side successes are human-in-the-loop tasks whose goal is pleasing the human (Claude Code's job is not just making code work), while right-side failures aim to remove the human loop entirely. Lesson one: everything inherited from RLHF is incredible at human-in-the-loop work but not automation. Businesses therefore learn not to use AI for decisions with stakes, pushing costs onto the user instead. See [[wiki/01-whats-next-after-rlhf-intro|What's Next After RLHF — Talk Opening and Speaker Intro]].

### Q5. How does the speaker define RLHF, and why does it structurally force a human in the loop?

> [!tip]- Answer
>
> RLHF is "just collect human preferences, optimize for human preferences," and he claims roughly 100% of LLMs by usage are trained this way, so humans are literally put in the loop. Overpromising becomes a feature by design: models err toward what pleases the human when uncertain, leaving a persistent gap between preference and good results. This is illustrated by the fart-sound-effects anecdote, where ChatGPT praised the audio as an "eerie vibe atmosphere piece," and by the end game of optimizing for engagement. See [[wiki/01-whats-next-after-rlhf-intro|What's Next After RLHF — Talk Opening and Speaker Intro]].

### Q6. Why is SaaS-plus-chatbot not automation, and what does the speaker want instead?

> [!tip]- Answer
>
> SaaS has barely changed since 2019 except for a latched-on chatbot, which is predictable because today's AI is assistance-native; a purely RLVR Claude Code would look very different but still would not add automation. Garry Tan's "just-in-time software" is a double-edged compliment: it only automates writing same-expressibility software. What comes next is real automation via "smarter software" with more expressive building blocks and a redesigned AI stack, including TypeSafe's third post-training approach beyond RLHF and RLVR optimized for calibrated decision-making. See [[wiki/01-whats-next-after-rlhf-intro|What's Next After RLHF — Talk Opening and Speaker Intro]].

### Q7. (evaluation) The speaker proposes a third post-training approach optimizing calibrated decision-making instead of human preference or pure correctness. For a high-stakes use case like automated refunds, would you recommend adopting it, and what evidence would you demand first?

> [!tip]- Answer
>
> Recommend a small staged pilot rather than full adoption, since the talk gives only a pitch with no benchmarks for the third approach. Demand calibration evidence first: predicted-confidence versus actual-outcome curves on refund-like decisions, plus cost-of-error comparisons against RLHF and RLVR baselines. Only scale up if the system abstains or escalates at the right uncertainty thresholds instead of confidently pleasing the requester. See [[wiki/01-whats-next-after-rlhf-intro|What's Next After RLHF — Talk Opening and Speaker Intro]].
