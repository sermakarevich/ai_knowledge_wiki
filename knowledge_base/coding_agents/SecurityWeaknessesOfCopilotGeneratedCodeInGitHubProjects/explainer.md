> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Security Weaknesses of Copilot-Generated Code in GitHub Projects: An Empirical Study — In Plain Language

## What is this about?

This study asks a simple question: when developers paste AI-written code
into real projects on GitHub, how often is that code insecure?

The authors hunted down code that developers themselves said was written
by GitHub Copilot (plus two similar tools, CodeWhisperer and Codeium).
They ended up with 733 real-world snippets: 419 in Python and 314
in JavaScript, mostly from small, little-known projects.

They then scanned every snippet with automated security checkers —
CodeQL for both languages, plus Bandit for Python and ESLint
for JavaScript — and had two people independently verify each warning
so false alarms were thrown out.

The headline result: about one in four snippets had a genuine security
weakness. That is 29.5% of the Python snippets and 24.2% of the
JavaScript snippets, or 200 out of 733 files in total.

Those 200 files contained 628 separate weaknesses, roughly three per
file, spread across 43 different weakness types. The worst single file —
about 1,600 lines long — had 22 weaknesses on its own.

The second half of the study asks: can Copilot Chat fix its own mistakes?
The answer is "partly, and it helps a lot if you show it the warning."

## Why does it matter?

AI assistants are trained on billions of lines of public code, and that
public code already contains bad habits: weak passwords, unchecked
inputs, copy-pasted web code. The assistant learns the habits along
with everything else.

Earlier studies mostly tested assistants with artificial puzzles or
deliberately risky prompts. This study is different because it looks at
code developers actually kept and shipped in GitHub projects.

Three reasons the findings sting:

- The weaknesses are not exotic. Eight of the 43 weakness types sit on
  the MITRE 2023 Top-25 list of the most dangerous software weaknesses,
  accounting for over 200 of the 628 cases.
- The top offenders are everyday bugs: guessable random numbers,
  code injection, cross-site scripting, and operating-system command
  injection. These are the bugs attackers exploit first.
- Over half of the vulnerable snippets had more than one problem, so a
  quick glance would not catch everything. A developer who trusts the
  suggestion without checking inherits the whole bundle.

GitHub itself says users are responsible for the security of Copilot
suggestions. This study measures what that responsibility really costs.

## How does it work?

Think of the study as a four-step pipeline: collect, scan, classify,
then try to repair.

**1. Collect real AI-written code.**
The team searched GitHub with combinations like "by / with / use" plus
"Copilot", "CodeWhisperer", or "Codeium", limited to Python and
JavaScript. After removing duplicates there were 3,589 candidates.
Two authors independently read them over two weeks (agreement score
0.84, which is high) and kept only files the project itself credited
to an AI tool. Practice exercises like LeetCode answers were excluded.

**2. Scan with two checkers per language.**
Every file was scanned twice: CodeQL plus a language specialist (Bandit
for Python, ESLint for JavaScript). Only Warning and Error findings
counted; style-only suggestions were ignored. Each hit was then checked
by hand against the exact line number, and for snippet-style files the
authors confirmed via nearby comments that the flagged lines were
really AI-generated.

**3. Sort each bug into a standard category.**
Two authors independently mapped every confirmed warning to a Common
Weakness Enumeration (CWE) ID over ten days (agreement 0.82), with a
security expert breaking ties. That produced the 43-type catalogue,
averaging about three weaknesses per vulnerable file.

**4. Try to fix a sample with Copilot Chat.**
The team picked 90 files (50 Python, 40 JavaScript) containing 295
weaknesses and tried three repair styles: the built-in `/fix` command,
a plain "please fix this" prompt, and an enhanced prompt that pasted in
the checker's warning message. Each repair was re-scanned to see what
actually went away.

The enhanced prompt won clearly: about 55.5% fixed, versus 31.8% for
the plain prompt and 19.3% for `/fix`. But success varied wildly by bug
type, which leads to the takeaways below.

## Where can this be used?

- **Everyday code review.** If you accept Copilot suggestions in Python
  or JavaScript, run a free checker (CodeQL, Bandit, ESLint) before you
  merge. The study shows one scan catches problems humans miss.
- **Smarter repair prompts.** When the checker complains, paste its exact
  warning plus the surrounding function into Copilot Chat and ask for a
  targeted fix. That one habit roughly tripled the fix rate versus `/fix`.
- **Language-specific checklists.** Python reviewers should watch system
  calls, file paths, and library loading (command injection, uncontrolled
  search path). JavaScript reviewers should watch dynamic code execution
  and web output (code injection, cross-site scripting, path traversal).
- **Team standards.** Use the CWE Top-25 as a shared "most wanted" list
  for auditing AI-generated code, especially in utility tools and web
  apps where the study found the most weaknesses.
- **Teaching and onboarding.** The per-language, per-domain breakdowns
  (for example, Python back ends skew toward SQL injection while
  JavaScript front ends skew toward cross-site scripting) make good
  training examples of how the same assistant fails differently.
- **Knowing when not to trust the bot.** Injection-style bugs such as
  OS command injection barely budged under any prompt. Those need human
  redesign, not another chat retry.

## Conclusions & takeaways

- About 27% of real-world AI-generated snippets in the sample were
  insecure — not a rare edge case but a routine outcome.
- The damage clusters: a few weakness types (weak randomness, injection,
  cross-site scripting) cause most of the trouble, and one bad file can
  carry many bugs at once.
- Context changes the risk. Python utility scripts fail differently from
  JavaScript web apps, so one generic "AI code is fine" rule is unsafe.
- Copilot Chat can repair a bit over half the problems when you feed it
  the checker's warning — easy wins like weak randomness get fixed near
  98% of the time, while command injection and access-control bugs often
  stay at 0%.
- The practical recipe: scan everything, paste warnings into the chat for
  simple fixes, and bring in a human for complex input-handling logic.
  Some Top-25 weaknesses never appeared at all, suggesting the tools
  already filter a few things — but the 30 rarer weakness types outside
  the Top-25 are still exploitable, so vigilance stays necessary.

## Jargon decoder

| Term | What it means in plain language |
| ---- | ------------------------------- |
| Copilot / CodeWhisperer / Codeium | AI assistants that suggest code as you type, trained on public code. |
| Static analysis | Checking code for bugs without running it, like proofreading an essay. |
| CodeQL, Bandit, ESLint | Free automated proofreaders: CodeQL is general-purpose, Bandit covers Python, ESLint covers JavaScript. |
| CWE (Common Weakness Enumeration) | A numbered catalogue of bug types, so everyone means the same thing by "injection flaw". |
| CWE Top-25 | MITRE's yearly "most dangerous bugs" list, used here as a severity yardstick. |
| Cross-site scripting (XSS) | A web bug where attacker input gets shown to other users as live code. |
| Code / command injection | A bug where attacker text gets executed as program or system commands. |
| Copilot Chat / `/fix` | A chat sidebar for asking Copilot to explain or repair code; `/fix` is its one-click repair button. |
| Cohen's Kappa | A 0-to-1 score for how well two reviewers agreed; above 0.8 means strong agreement. |
| False positive | A checker warning about code that is actually fine; the authors filtered these out by hand. |
