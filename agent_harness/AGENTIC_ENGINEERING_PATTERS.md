# Agentic Engineering Patterns — Instructive Summary

Summary of Simon Willison's guide: https://simonwillison.net/guides/agentic-engineering-patterns/

A distillation of the key ideas, workflows, and prompts an engineer can actually apply.

---

## The Through-Line

Coding agents reduce the cost of producing code to near zero. That does **not** reduce the cost of producing *good* code — it shifts the engineer's job from "typing code" to:

1. Deciding what to build.
2. Specifying the problem at the right level of detail.
3. Verifying the result.
4. Curating reusable knowledge so agents can recombine it later.

Standards do not drop. Responsibility does not distribute. The author still owns correctness, review, and the narrative a PR tells.

---

## Section 1 — Principles

### 1.1 What is agentic engineering?
- **Definition:** developing software with coding agents in the loop, where the agent can execute code and iterate toward working software.
- **Distinct from "vibe coding"** (Karpathy, Feb 2025), which is unreviewed prototype LLM output. Agentic engineering is *intentional refinement* toward production quality.
- LLMs don't learn from their own mistakes — you must deliberately update instructions, skills, and harness tooling based on lessons.
- *"Writing code has never been the sole activity of a software engineer."*

### 1.2 Writing code is cheap now
- All classic engineering economics (planning, prioritization, refactoring, build-vs-buy) were built on the assumption that coding time is expensive. That foundation is gone.
- **Second-guess your instincts.** Whenever you think "not worth the time to build," fire off a prompt anyway — check results later.
- Parallel agents multiply this: one engineer can run several background tasks simultaneously.
- **The gap agents do not close:** correctness, error handling, tests, minimalism, docs, security, observability, maintainability. That gap is on you.

> *"Delivering new code has dropped in price to almost free... but delivering good code remains significantly more expensive than that."*

### 1.3 Hoard things you know how to do
- Build a personal library of working proof-of-concept code. *Knowing* something is possible ≠ *having seen it done yourself*.
- Agents are recombination machines. **Favorite pattern:** provide 2+ working examples and ask the agent to synthesize a new solution.
- Storage formats: a TIL blog, personal GitHub repos, single-page HTML tools, a research repo.
- Prompt agents to `curl` your existing tools, `git clone` public repos into `/tmp`, or search local directories for implementation patterns.
- *"Coding agents mean we only ever need to figure out a useful trick once."*

### 1.4 AI should help us produce better code
- Shipping worse code with agents is a choice — blame the process, not the tool.
- **Zero tolerance for code smells is now viable** because the cost of minor refactors has collapsed.
- Best use cases: refactoring (API redesigns, naming cleanup, dedup, splitting large files), not greenfield features.
- **Asynchronous workflow:** background agents handle refactors while you keep working. Review via low-stakes PRs.
- Use agents for technology-selection research and cheap exploratory prototypes before committing to architecture.
- **Compound engineering loop:** document what works, refine agent instructions across projects; each project improves the next.

### 1.5 Anti-patterns
- **Never file a PR containing code you haven't reviewed yourself.** Reviewers could have prompted the agent themselves — your value is the first review pass.
- Unreviewed agent text in the PR description is rude. Validate everything you put your name on.
- A good agentic PR: small, author-validated, includes testing notes, rationale, and screenshots/video.
- *"It's rude to expect someone else to read text that you haven't read and validated yourself."*

---

## Section 2 — Working with Coding Agents

### 2.1 How coding agents work
- The fundamental architecture is **LLM + system prompt + tools, in a loop.** A minimal implementation is dozens of lines.
- LLMs are **stateless**. Every call replays the entire conversation history. The harness fakes memory.
- LLMs process *tokens*, not words; images become tokens too. Billing and context limits are per-token.
- **Token caching** is a first-class optimization: don't modify earlier conversation content, don't swap models mid-session, don't add/remove tools. Cache invalidation is expensive on every subsequent call.
- **Tool calls** are implemented by injecting schemas into the system prompt, parsing the LLM's output with regex, executing the function, and appending a `<tool-result>` block.
- **Reasoning mode** (2025+): scratchpad tokens before the response. Useful for debugging.

### 2.2 Using Git with coding agents
- Reframe git history as **authored narrative**, not an immutable record.
- Agents handle git syntax fluently — stop memorizing commands.
- **Session seeding:** open each session with *"Review changes made today"* — the agent runs `git log`, loads recent diffs, and gains continuity from your previous session.
- **Useful prompts:**
  - *"Commit these changes"* — writes a meaningful message.
  - *"Sort out this git mess for me"* — resolves conflicts and staging.
  - *"Find and recover my code that does..."* — searches reflog and branches.
  - *"Combine the last three commits with a better message"* — interactive squash without the pain.
  - *"Integrate latest changes from main"* — handles merge strategy.
- Agents are strong at **merge conflict resolution** and **`git bisect`** (describe the bug, let it binary-search).
- **History rewriting is cheap now:** remove files from specific commits, extract a module into its own repo while preserving authorship and dates.
- Safety: git is reversible, making agent-assisted experimentation low-risk by default.

### 2.3 Subagents
- The core problem: **context exhaustion.** LLMs cap around 1M tokens, perform best under 200k. Subagents dispatch fresh instances with empty context windows.
- Mechanically, a subagent is just a tool call — the parent pauses, waits for the result, resumes.
- **Explore pattern:** *"Find the code that implements [feature]. Search thoroughly — check [dirs]. Look for keywords like [terms]."* Report back, don't dump.
- **Parallel subagents:** *"Use subagents to find and update all affected templates."* Real wall-clock speedup on independent files.
- **Specialist subagents** with custom system prompts: code reviewers, test runners (hide verbose output, surface failures), debuggers.
- **Don't over-fragment.** The parent's accumulated context is valuable. Use cheaper/faster models (e.g. Haiku) for parallel subagent work.

---

## Section 3 — Testing and QA

### 3.1 Red/green TDD
- TDD pairs especially well with agents because it guards against two failure modes: (a) non-functional code, (b) unnecessary code.
- The red phase is not optional — without it, tests can pass trivially without validating anything.
- **Prompt shorthand:** *"Use red/green TDD."* Modern models understand this as: write tests first, confirm they fail, implement until green.
- Example: *"Build a Python function to extract headers from a markdown string. Use red/green TDD."*

### 3.2 First run the tests
- Agents eliminate the old excuse for skipping tests. Automated tests are now baseline, not optional.
- An existing test suite **shapes agent behavior** — agents that see tests naturally add more tests.
- **Session-opening habit:** on every existing project, start with *"First run the tests."* (Python/uv variant: *"Run 'uv run pytest'."*)
- Three purposes at once: discover where the suite lives, establish complexity context, create a coverage-expansion mindset.

### 3.3 Agentic manual testing
- **Never assume LLM code works until it has been executed.** Passing automated tests is not sufficient.
- Agents can manually test themselves: spin up servers, run `curl`, take screenshots, verify visual output.
- Feed bugs found during manual testing back into automated tests via red/green TDD — close the loop.
- **Techniques:**
  - Python functions: inline with `python -c "..."` against edge cases.
  - Throw-away demo scripts in `/tmp` to avoid repo pollution.
  - JSON APIs: start a dev server, exercise via `curl`.
  - Browser: Playwright, or agent-native tools like **Rodney** (Chrome DevTools Protocol + screenshots) or Vercel's agent-browser.
- **Showboat** — a session documentation tool with three commands that produce a tamper-evident log:
  - `note` — append Markdown observations.
  - `exec` — record a command and its real output (stops the agent fabricating results).
  - `image` — embed screenshots inline.
- Example prompt: *"Start a dev server and use `uvx rodney --help` to test the new homepage, look at screenshots to confirm the menu placement."*

---

## Section 4 — Understanding Code

### 4.1 Linear walkthroughs
- Agent-generated code creates **cognitive debt**: working code, no mental model. This blocks future feature work.
- Use the agent to rebuild your understanding: ask for a structured linear walkthrough of the codebase.
- **Anti-hallucination rule:** instruct the agent to use `sed`/`grep`/`cat` to pull code snippets into the walkthrough. Never let it reproduce snippets from memory.
- Showboat is the recommended vehicle: `showboat note` for Markdown, `showboat exec` for real shell output.

> *"By telling it to use sed or grep or cat... Claude Code would not manually copy snippets into the document, since that could introduce a risk of hallucinations."*

### 4.2 Interactive explanations
- Static documentation is often inferior to **interactive, animated** explanations for building algorithmic intuition.
- The cost of building a custom animated explainer is now near zero — the agent can write both the algorithm and its explainer in one session.
- **Concrete case:** Simon had an agent animate the Archimedean spiral placement algorithm in a word cloud tool — words appear sequentially, collision boxes are shown, a spiral is drawn outward, with pause/speed/step controls plus PNG export. (Model: Claude Opus 4.6.)
- **Pipeline:** generate code → linear walkthrough for structure → interactive animation for algorithmic intuition.

---

## Section 5 — Annotated Prompts (Case Studies)

### 5.1 GIF optimizer via WebAssembly + Gifsicle
Simon compiled Gifsicle to WASM and wrapped it in `gif-optimizer.html` — drag-and-drop, multiple preview modes, download buttons.

**Lessons:**
- **Filename as spec anchor.** Specifying `gif-optimizer.html` establishes context with zero ceremony.
- **Trust agent domain knowledge.** No need to explain widely-known tools (Gifsicle, WASM toolchain).
- **Agents brute-force compiler errors better than humans:** *"They can often brute force their way to a solution where I would have given up after the fifth inscrutable compiler error."*
- **Testing is non-negotiable.** Name a real test artifact (a specific GIF) and a browser automation tool (Rodney) upfront.
- **Vague specs work when you trust the agent's taste.** Don't over-specify settings you don't care about.
- **Pattern reuse by reference.** Mention "drag-and-drop, a pattern I've used in my other tools" — the agent inspects those and matches the UX.
- **Mid-flight additions are normal.** Adding "use a build script cloning Gifsicle to `/tmp` pinned to a commit" and "credit the author in the footer" while watching the agent work is the expected rhythm.

### 5.2 Adding a new content type to a blog-to-newsletter tool
Three-sentence prompt, merged on first attempt:
1. Clone `simonwillisonblog` from GitHub to `/tmp` for reference.
2. Update `blog-to-newsletter.html` to include "beats" with descriptions, mirroring the Atom feed's filtering logic.
3. Test with `python -m http.server` and `uvx rodney`; compare output to the live homepage.

**Lessons:**
- **Clone the reference, don't describe it.** Point the agent at existing code rather than explaining semantics.
- **Use `/tmp` for reference repos** so they can't accidentally be committed.
- **Name the specific file,** not the project — eliminates ambiguity among many tools in one repo.
- **Validate against a live reference.** "Compare to homepage" is a better correctness target than "make sure it works."
- **`uvx rodney --help`** lets the agent learn a tool's interface on the fly — no need to document it in the prompt.

**Core thesis across both case studies:** *the prompt is a pointer, not a spec.* Point the agent at existing code, give it a testable environment, name the target file, and let it read its way to the answer.

---

## Section 6 — Appendix: Reusable Prompts

### 6.1 Artifacts (custom instruction for Claude Projects)

> Never use React in artifacts - always plain HTML and vanilla JavaScript and CSS with minimal dependencies. CSS should be indented with two spaces and should start like this: `<style> * { box-sizing: border-box; }` Inputs and textareas should be font size 16px. Font should always prefer Helvetica. JavaScript should be two space indents and start like this: `<script type="module"> // code in here should not be indented at the first level` Prefer Sentence case for headings.

Persistent custom instruction so you don't repeat it per conversation.

### 6.2 Proofreader

> You are a proofreader for posts about to be published.
> 1. Identify spelling mistakes and typos
> 2. Identify grammar mistakes
> 3. Watch out for repeated terms like "It was interesting that X, and it was interesting that Y"
> 4. Spot any logical errors or factual mistakes
> 5. Highlight weak arguments that could be strengthened
> 6. Make sure there are no empty or placeholder links

Run as a final pass before publishing. Item 3 catches filler-phrase habits that erode quality.

### 6.3 Alt text

> You write alt text for any image pasted in by the user. Alt text is always presented in a fenced code block to make it easy to copy and paste out. It is always presented on a single line so it can be used easily in Markdown images. All text on the image (for screenshots etc) must be exactly included. A short note describing the nature of the image itself should go first.

Fenced single-line output is directly usable in `![alt](url)`. Paste multiple images into one conversation for coherent descriptions.

### 6.4 Podcast highlights

> You will be given a transcript of a podcast episode. Find the most interesting quotes in that transcript - quotes that best illustrate the overall themes, and quotes that introduce surprising ideas or express things in a particularly clear or engaging or spicy way. Answer just with those quotes - long quotes are fine.

*"Answer just with those quotes"* suppresses preamble. *"Long quotes are fine"* prevents premature truncation.

---

## A Condensed Daily Workflow

1. **Open session:** *"Review changes made today"* (git seeding) and *"First run the tests."*
2. **For new features / bug fixes:** *"Use red/green TDD."*
3. **For refactors / cross-file changes:** farm out to parallel subagents (or a background agent for async async).
4. **For unfamiliar codebases:** spawn an Explore subagent; then ask for a Showboat linear walkthrough using `sed`/`grep` to extract real snippets.
5. **For algorithms you don't yet intuit:** ask the agent to build an interactive animated explainer.
6. **Before committing:** manual-test via dev server + browser automation; capture with Showboat.
7. **Before opening a PR:** review every line yourself, validate the PR description, include screenshots and rationale.
8. **After shipping:** capture the reusable bits (proof-of-concepts, prompts, instructions) into your hoard. Each project should improve the next.

---

## The Five Principles Worth Tattooing

1. **Code is cheap; good code is not.** The quality gap is yours to close.
2. **The prompt is a pointer, not a spec.** Point to existing code and runnable tests — don't re-describe.
3. **Never ship unreviewed agent output.** Your name, your review.
4. **Context is the scarce resource.** Cache it, subagent it, and don't break the prefix.
5. **Hoard what works.** You only need to figure out each useful trick once.
