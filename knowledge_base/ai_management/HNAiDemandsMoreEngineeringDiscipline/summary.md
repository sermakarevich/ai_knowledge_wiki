# AI demands more engineering discipline. Not less

**Thread:** [AI demands more engineering discipline. Not less](https://news.ycombinator.com/item?id=48570948)
**Submitted by:** BerislavLopac | **Score:** 222 | **Comments:** 110 | **Date:** 2026-06-17

## What's Being Discussed

Charity Majors (author of the Substack post at charitydotwtf) argues that AI code generation has inverted traditional software economics — generated code is nearly free to produce but the real cost has shifted to verification, design, and intent. The post claims this demands _more_ engineering discipline (specs-as-infrastructure, explicit documentation of decisions, human-in-the-loop intent capture), not less. HN commenters push back, extend, and complicate this thesis from many angles.

---

## Key Themes

1. **Signal vs. noise in engineering teams.** The most-upvoted thread opens with ryandvm's observation that AI makes it nearly impossible to distinguish engineers who genuinely understand systems from those slinging LLM copypasta. Before 2025, underperformers were identifiable by sparse output. Now every engineer files PRs and design docs with perfect formatting and superficial plausibility, driven by C-level pressure to maximize AI usage. The result is an exotic form of technical debt: a codebase that looks legitimate but was never deeply understood by its authors.

2. **Code volume vs. meaningful output.** A sustained sub-thread debates whether net Lines of Code (LoC) removed is a useful proxy for senior engineering capability. The productive engineers thread (strix_varius, pydry) argues that truly capable engineers achieve more business outcomes with fewer moving parts — LLMs love to add code, so the best humans constrain that proliferation. Critics (4lx87, ecshafer) push back: zero or negative net LoC sounds like digging ditches to fill them, and the correlation between output and LoC still holds for most engineers below staff level. AnimalMuppet synthesizes cleanly: "big-picture lazy" (reducing overall system complexity) is a virtue; "individually lazy" (rubber-stamping AI output) is a vice.

3. **Code review at scale.** trjordan opens a major thread on the collapse of the PR review loop: a 5k-line PR from a human colleague would be rejected outright for being too large, but the same constraint has been quietly abandoned for AI-generated PRs. roncesvalles notes managers cannot block oversized PRs when 5× more code is produced than before — LLMs don't help review, so rubber-stamping becomes the norm. darth_aardvark offers a counter: Claude is actually excellent at decomposing a 5k-line PR into a well-structured Graphite stack. The deeper concern is whether human-reviewed AI code or AI-reviewed AI code provides any real safety guarantees.

4. **The human feedback loop and cognitive cost.** trjordan argues that reading AI code all day is agonizing and "melts people's brains." Manual programming had a gratifying read→write→fix feedback loop with a satisfying "click" when things worked. AI-generated code breaks this loop. gavinh adds a pedagogical angle: code review is now substituting for the mental model previously built by writing code, but people recall information they _generated_ far better than information they _read_. Operating with AI-generated code as the only durable artifact may be a dead end.

5. **Documentation-driven and discipline-first AI use.** The engineers reporting genuine success all describe the same pattern: K0balt writes documentation first, then generates code against it — better code, better docs, easier maintenance, 4× speed, ¼ cost. kstenerud: solid design first (else slop), solid plan second (else slop), then set the AI loose but stay alert. msteffen emphasizes going straight for humans and human docs when ramping on a new codebase. The meta-point: AI excels when intent is explicit and requirements are well-specified; it fails on novel domain problems with no prior knowledge.

---

## Notable Takes

- **"We are absolutely drowning in documentation and code that seems legit."** ryandvm describes the fallout from universal AI adoption: the only recourse is to lean on AI to process the sheer volume of AI-generated artifacts — an ouroboros. — u/ryandvm

- **"If it's one prompt, why wouldn't I?"** simonw notes that 25 years of software intuition about how long things take to build is becoming obsolete. An edge-case validation that would previously take 2 hours and be skipped is now one prompt — there's no reason not to add it. — u/simonw

- **"Operating with AI-generated code as the only durable artifact is a dead end."** trjordan argues the interesting artifacts are what humans produce — prompts, markdown plans, decision records — not the generated code itself. The question is how to make those first-class. — u/trjordan

- **"Not X, but Y"** construction saturation: stephbook and keybored both note the article uses a rhetorical style ("it's real, it's not imaginary, it's even existential") common to AI boosterism pieces, and SrslyJosh cuts to the bone: "So, using artificial intelligence requires more expertise than not using it?" — u/SrslyJosh

- **"Big-picture lazy is a virtue; individually lazy is a vice."** AnimalMuppet recovers Larry Wall's Three Virtues of a Programmer to distinguish productive laziness (going to great effort to reduce _overall_ energy expenditure) from the kind of laziness that rubber-stamps AI output, increasing total system cost. — u/AnimalMuppet

---

## Consensus & Dissent

- **Broad agreement:** Undisciplined AI use creates a new class of technical debt — code that looks correct but was never deeply understood. "Vibe coding" at scale is widely treated as obviously bad.
- **Broad agreement:** AI doesn't eliminate the need for domain knowledge, design discipline, or intent. It amplifies both good and bad engineering practices.
- **Split:** Whether the PR size/review problem is solvable in practice. Some (darth_aardvark) say LLMs can decompose large PRs trivially; others (roncesvalles, cmrdporcupine) say management pressure prevents blocking oversized PRs regardless of tooling.
- **Split:** Whether current AI code quality criticism is temporary. sandover argues the author mistakes the current moment for a stable state; capability growth is exponential and critics are consistently proven wrong by the next model. romaniv counters that "you're prompting it wrong / use this model instead" is an unfalsifiable defense that has been deployed since GPT-3.5.
- **Crux of disagreement:** Whether _code_ is still the right artifact to review at all. molsongolden and trjordan argue decisions/structure/requirements should be the reviewed artifacts and code should be regenerable on demand. argee and skydhash counter that code is the only perfect semantic representation of what the computer will actually do — coarser-granularity review guarantees mistakes.

---

## Resources Surfaced

- [stop-reading-prs](https://tern.sh/blog/stop-reading-prs/) — trjordan's post arguing reviewers shouldn't have to read AI-generated code at the same level as human-written code
- [just-send-me-the-prompt](https://blog.gpkb.org/posts/just-send-me-the-prompt/) — referenced by msteffen as context for the article's argument about prompts as first-class artifacts
- [gitsense/gsc-cli](https://github.com/gitsense/gsc-cli) — AI Code Provenance tool: repo where code block headers attribute the model and UUID traces back to the originating conversation
- [tern.sh](https://tern.sh) — product comparing code to prompts and highlighting where the agent made decisions the human wasn't involved in (trjordan's project)
- [saasufy.com](https://saasufy.com) — backend-as-a-service arguing that vibe coders shouldn't manage backend security themselves (socketcluster; context: promotional comment)
