> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Human-AI Experience in Integrated Development Environments: A Systematic Literature Review — In Plain Language

This explainer translates a large research roundup into everyday language.
The paper reviews 90 studies from 2022–2024 about using AI assistants
directly inside code editors. No math or prior research background needed.

## What is this about?

Imagine an AI helper living inside the place where you write code.
It finishes your lines, answers questions, explains errors, and writes
chunks of new code without you leaving the editor.

Researchers call this "in-IDE Human-AI Experience," or in-IDE HAX.
The "IDE" is the editor workspace, such as VS Code, IntelliJ, or Jupyter.
"HAX" means the AI is treated less like a hammer and more like a junior
partner you collaborate with.

This paper does not test one new tool. It collects and compares 90
separate studies, then sorts what they found into three buckets:
what changes for developers, how the helper should be designed,
and how good the AI-written code actually is.

## Why does it matter?

AI coding helpers are already everywhere. Surveys cited in the review
say about three-quarters of developers use them or plan to, and over
half report faster coding and less time searching the web.

But faster is not the same as better. The review finds a repeated
trade-off: people finish routine work sooner, then spend extra time
checking, fixing, and rewording what the AI produced. In one study,
checking took up to half of developers' time.

There are also quieter risks. Beginners can lean on the AI too much
and miss basic ideas. Experienced developers sometimes reject good
suggestions because no reason is shown. And AI-written code can look
correct while hiding bugs or security holes.

Because individual studies are small and short, this roundup matters:
it shows which results keep repeating and where the evidence is thin.

## How does it work?

Think of the review as a careful library project, not an experiment.

First, the authors searched eight research libraries plus arXiv,
added papers from an earlier survey and from experts, and followed a
standard checklist called PRISMA for transparent reviews.

Second, they filtered hundreds of candidates down to 90 studies that
tested real developers or students using AI inside a real editor,
then scored each study for clear reporting, careful methods,
believable evidence, and relevance.

Third, they tagged every study with three labels: which part of the
software life cycle it covered, whether the setting was professional
or educational, and which of the three big questions it answered.

Finally, they looked for patterns. For example, 74 of 90 studies said
something about impact on people, 28 about interface design, and 19
about code quality. The most studied helper by far was GitHub Copilot,
appearing in 36 of 90 studies.

## Where can this be used?

- **Code editors:** autocomplete that finishes lines, chat panels that
  explain or rewrite code, and newer hybrids that mix both styles.
- **Learning to program:** students solve exercises faster, but teachers
  need guardrails so students still learn the underlying concepts.
- **Everyday professional coding:** writing routine code, documentation,
  tests, debugging help, refactoring, and moving code between setups.
- **Code review and testing:** automatic test suggestions, highlighting
  risky lines, comparing alternative AI answers, and filtering bad output.
- **Team and tool design:** settings for suggestion frequency, clearer
  explanations, privacy-aware prompts, and assistants tuned to a person's
  skill level and current task.
- **Beyond writing code:** the authors note requirements, design,
  deployment, and maintenance are under-explored and need more tools.

## Conclusions & takeaways

1. AI helpers genuinely speed up routine coding and reduce interruptions,
   especially for experienced developers on familiar tasks.
2. The time saved is partly spent on checking: review, re-prompting,
   and rework are now a core part of coding, not an afterthought.
3. Trust depends on context. People trust the AI more for small or
   experimental tasks and less for production, complex, or open-ended work.
4. Good design shows its work: relevant context, short explanations,
   visible uncertainty, and easy ways to accept, edit, or silence help.
5. AI code needs auditing. It can be subtly wrong, hard to read, or
   insecure, so verification habits and tests matter more than before.
6. The evidence base is narrow: mostly Copilot, mostly short studies
   with a median of 17 people, mostly about writing new code.
7. Next steps are bigger and longer studies, better checking tools,
   coverage of earlier and later project stages, and assistants that
   adapt while leaving the developer in control.

## Jargon decoder

| Term | What it means in plain language |
|------|----------------------------------|
| IDE | The editor workspace where you write, run, and test code. |
| In-IDE HAX | What it feels like to collaborate with AI inside that editor. |
| Autocompletion | The AI quietly finishes your current line or block. |
| Conversational assistant | A chat panel where you ask questions and refine answers. |
| Hybrid assistant | A mix of quiet autocomplete plus chat for harder problems. |
| Verification overhead | The extra time spent checking and fixing AI suggestions. |
| Over-reliance | Accepting AI answers without checking, especially by beginners. |
| Under-reliance | Rejecting a correct AI answer because no explanation was given. |
| Automation bias | Assuming the machine must be right and skipping your own review. |
| SDLC stage | Which project phase the work belongs to, such as design, coding, or testing. |
| PRISMA | A standard checklist for doing transparent literature reviews. |
| Snowballing | Finding extra papers by following citations of papers already selected. |
