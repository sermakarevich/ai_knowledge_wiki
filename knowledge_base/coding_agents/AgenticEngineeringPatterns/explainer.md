> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Agentic Engineering Patterns - Simon Willison's Weblog — In Plain Language
This is a plain-language guide to what Simon Willison's "Agentic Engineering
Patterns" project is, based on the material captured so far — which is only
the landing page: a title, a one-line description, and a table of contents.
Think of this explainer as a map of the map: it tells you what the guide
promises to teach, what each planned section means in everyday words, and
which words to learn first, without pretending the details were captured.
## What is this about?
In one sentence: it is a practical handbook of repeatable patterns for
getting the best results out of AI coding agents such as Claude Code and
OpenAI Codex.
A "coding agent" here means an AI assistant that does not just answer
questions but actually works inside your codebase: it reads files, runs
commands, edits code, runs tests, and reports back, going around a loop
until the task is done.
The word "patterns" matters. This is not a list of clever one-off prompts.
It is meant to be a collection of named, reusable ways of working — habits
and setups you can apply again and again across projects.
The captured material is only the front door of the guide: the title, the
one-line promise quoted above, a pointer to a separate introduction that
was not captured, and a long list of chapter headings with no body text.
So everything below explains the shape and intent of the project as shown
by that front door, not the full lessons inside each chapter.
## Why does it matter?
Writing code has become cheap: an agent can produce pages of working-looking
code in minutes. But cheap output is not the same as good software.
Someone still has to review it, test it, secure it, and maintain it for years.
That gap — fast generation versus lasting quality — is exactly what this
guide is trying to close.
It matters for three everyday reasons. First, without good habits, AI help
can quietly pile up "technical debt": shortcuts and messy code that slow
everyone down later. Second, with good habits, the same tools can raise
quality instead of lowering it: more options considered, more tests written,
more careful review. Third, the habits themselves are new — working with an
agent that edits, runs, and loops is genuinely different from typing every
line yourself, and most developers are still figuring out the playbook.
That is why a patterns guide is useful: it turns early trial and error into
shared, teachable habits.
## How does it work?
The guide is organized into five groups. Here is what each group means in
plain words, based on its listed headings.
**1. Principles — the mindset.** This group sets the ground rules before any
tool talk. Its headings contrast "vibe coding" (casually accepting whatever
the AI produces) with disciplined engineering, warn that good code still has
a cost even when writing it is cheap, and urge readers to build new habits.
Two memorable ideas appear here: "hoarding" techniques you know how to do
so you can recombine them later, and the "compound engineering loop," where
each improvement makes the next one easier. It closes with anti-patterns —
things to avoid, such as pushing AI-written code onto teammates unreviewed.
**2. Working with coding agents — the machinery.** This group explains what
happens under the hood: large language models, the hidden system prompt
that steers them, chat-style prompt templates, token caching for speed and
cost, tool calls that let the model touch files and commands, and the
"reasoning" steps some models show. The key picture is a loop: model plus
prompt plus tools, running around and around. It also covers teamwork tools:
Git essentials, rewriting history cleanly, and subagents — small specialist
helpers (for example, an Explore agent that investigates code) that can run
alone or in parallel.
**3. Testing and QA — proving it works.** This group is about trust. Its
headings point to test-driven habits ("red/green" testing, running the test
suite first), plus "agentic manual testing": asking the agent to click
through your app like a human would, using browser automation for web pages,
and having it take notes with a tool called Showboat so you can watch and
learn from what it tried.
**4. Understanding code — learning faster.** This group treats the agent as
a reading tutor, not just a writer. Headings mention linear walkthroughs of
a codebase, interactive explanations, "word clouds" of unfamiliar terms,
annotated prompts you can reuse, and worked examples such as an image-tool
project and a blog-to-newsletter tool — each showing how to ask follow-up
questions that deepen understanding.
**5. Appendix — the toolbox.** A grab bag of ready-to-use prompts, notes on
AI-generated artifacts, small helpers (a proofreader, an alt-text writer, a
podcast-highlights tool), plus disclosures and colophon notes about how the
guide itself was made.
## Where can this be used?
Anywhere a developer works with a coding agent on real software. The most
direct use is day-to-day feature work: drafting code with an agent, then
reviewing, testing, and committing it with Git, following the guide's loop
instead of blindly accepting output.
A second use is quality control and security review: one captured teaser
mentions engineers "pressure washing" a whole codebase with language models
and stresses quality over quantity when hunting vulnerabilities — a hint
that agents can systematically sweep large codebases a human would never
have time to read line by line.
A third use is learning and onboarding: new team members (or anyone facing
an unfamiliar codebase) can use walkthroughs, annotated prompts, and
interactive explanations to get oriented in hours rather than weeks.
A fourth use is testing web apps: browser-automation patterns let the agent
act as a tireless manual tester that clicks, screenshots, and reports back.
In short: writing, reviewing, testing, learning, and cleaning up — the full
cycle of keeping software healthy.
## Conclusions & takeaways
- This is a habits guide, not a tricks list: repeatable patterns for making
  coding agents produce better, safer, more maintainable software.
- The core tension it addresses is cheap writing versus costly ownership:
  generating code is fast, but reviewing, securing, and maintaining it is
  where the real work — and the real risk — lives.
- The working model is a loop, not a single answer: model plus prompt plus
  tools, circling through code, tests, and review, sometimes with specialist
  subagents helping in parallel.
- Testing and understanding get equal billing with writing: the guide treats
  proving the code works and learning how it works as first-class skills.
- An honest limit: the captured material so far contains only the guide's
  framing and table of contents, so no specific pattern, prompt, or result
  can be quoted yet — this explainer maps the promise, not the proof.
- If you remember one line: let the agent be fast, but keep the engineer's
  judgment in charge — review everything, test everything, hoard what works.
## Jargon decoder
| Term | What it means in plain words |
|---|---|
| Coding agent | An AI helper that works inside your project: reads, edits, and runs code in a loop until done. |
| Large language model (LLM) | The AI brain behind the agent: software trained on huge amounts of text that predicts good answers. |
| System prompt | Hidden instructions that steer the AI's behavior before you even ask anything. |
| Token | A small chunk of text the model reads or writes; usage is often counted and billed in tokens. |
| Token caching | Reusing earlier work instead of re-reading it, to make the agent faster and cheaper. |
| Tool call | The moment the AI stops just writing words and actually does something: opens a file, runs a test. |
| Subagent | A small specialist helper the main agent sends off to do one job, like exploring a folder. |
| Vibe coding | Casually accepting AI output by feel, without reviewing or testing — the habit this guide warns against. |
| Technical debt | Messy shortcuts that work today but slow everyone down tomorrow, like clutter in a workshop. |
| Red/green testing | Write a failing test first (red), then make it pass (green) — proof the code really works. |
| Browser automation | Letting the agent click through your website like a human tester, checking what actually happens. |
| Git history rewriting | Tidying up your saved checkpoints so teammates see a clean, sensible story of the work. |
