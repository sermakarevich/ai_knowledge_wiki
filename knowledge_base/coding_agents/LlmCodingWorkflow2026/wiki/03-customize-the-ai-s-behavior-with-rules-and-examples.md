> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Customize the AI's behavior with rules and examples

**In one sentence:** Tune the AI like a new hire — with rules files, custom instructions, and examples — and back it with automated tests and continuous learning so its output matches your conventions and gets caught when it doesn't.

## Key points

- Maintain a periodically updated `CLAUDE.md` (and `GEMINI.md` for Gemini CLI) with process rules and preferences — project style, lint rules, banned functions, functional-over-OOP — and feed it at session start to keep the model on track and reduce off-script patterns.
- Configure global project behavior in GitHub Copilot and Cursor with a short style paragraph (e.g. 4-space indent, no arrow functions in React, descriptive names, must pass ESLint) so suggestions match team idioms.
- Prime the model by mimicry: show a similar existing function ("Here's how we implemented X, use a similar approach for Y") or write one comment in the desired style and ask it to continue in that vein.
- Prepend truthfulness rules to prompts, e.g. "If you are unsure about something or the codebase context is missing, ask for clarification rather than making up an answer," plus explanation rules such as "Always explain your reasoning briefly in comments when fixing a bug," yielding reviewable comments like "// Fixed: Changed X to Y to prevent Z (as per spec)."
- Run heavy-AI repos with CI on every commit/PR, enforced style checks (ESLint, Prettier), and a staging deployment, then feed failures back verbatim ("The integration tests failed with XYZ, let's debug this" / paste linter errors plus "please address these issues") and route reviewer comments (e.g. CodeRabbit) back as refactor prompts.
- Treat AI use as a skill amplifier: solid fundamentals, clear specs, tests, and reviews become more powerful, while weak foundations risk "Dunning-Kruger on steroids"; deliberately review AI code, ask it to explain rationale and compare trade-offs, and periodically code without AI.

---

## Customize the AI's behavior with rules and examples

Steer the assistant with style guides, examples, and "rules files" — a little upfront tuning yields much better outputs, rather than accepting the default style.

| Mechanism | Detail from chunk |
|---|---|
| Rules files | `CLAUDE.md` for Claude, `GEMINI.md` for Gemini CLI; contains process rules and preferences, updated periodically |
| Example rules | "write code in our project's style, follow our lint rules, don't use certain functions, prefer functional style over OOP" |
| Custom instructions | Copilot and Cursor global project configuration; short paragraph, e.g. "Use 4 spaces indent, avoid arrow functions in React, prefer descriptive variable names, code should pass ESLint" |
| In-line priming | "Here's how we implemented X, use a similar approach for Y"; write one comment and ask the AI to continue in that style; one or two examples suffice because LLMs mimic well |
| Community rulesets | "Big Daddy" rule; "no hallucination/no deception" clause |

Verbatim prompts/rules quoted in chunk:

- "If you are unsure about something or the codebase context is missing, ask for clarification rather than making up an answer."
- "Always explain your reasoning briefly in comments when fixing a bug."
- Generated comment example: "// Fixed: Changed X to Y to prevent Z (as per spec)."

Attribution noted in chunk: Jesse Vincent noted rules files keep the model "on track"; Ben Congdon was shocked few people use Copilot's custom instructions given how effective they are.

Framing: "don't treat the AI as a black box - tune it"; "akin to onboarding a new hire: you'd give them the style guide and some starter tips, right? Do the same for your AI pair programmer."

## Embrace testing and automation as force multipliers

Use CI/CD, linters, and code review bots — AI works best where mistakes are caught automatically.

- Require automated tests on every commit/PR, style checks (ESLint, Prettier), and ideally a staging deployment for any new branch.
- When AI opens a PR via Jules or GitHub Copilot Agent, let CI report failures, then feed logs back: "The integration tests failed with XYZ, let's debug this," and iterate.
- Paste linter/type-checker output into chat with "please address these issues"; once aware of tool output the model tries hard to correct it — "like having a strict teacher looking over the AI's shoulder."
- Prefer agents that refuse "done" until all tests pass; treat CodeRabbit-style reviewer comments ("This function is doing X which is not ideal") as follow-up prompts: "Can you refactor based on this feedback?"
- Goal going into 2026: more tests, more monitoring, even AI-on-AI code reviews, which have caught things one model missed; without tests/checks, subtle AI bugs slip through until much later.

## Continuously learn and adapt (AI amplifies your skills)

Treat every session as a learning opportunity — expertise plus AI compounds; without fundamentals the AI amplifies confusion.

- LLMs "reward existing best practices": clear specs, good tests, code reviews become even more powerful; operate at design/interface/architecture level while the AI does boilerplate.
- Per Simon Willison (as cited): almost everything that makes someone a senior engineer — designing systems, managing complexity, knowing what to automate vs hand-code — yields the best AI outcomes.
- Learn by reviewing AI code for new idioms, debugging its mistakes, asking it to explain code/rationale "like constantly interviewing a candidate," and using it to enumerate options or compare trade-offs — "an encyclopedic mentor on call."
- Warning: for those without a solid base, "Dunning-Kruger on steroids (it may seem like you built something great, until it falls apart)"; keep honing craft and periodically code without AI to keep raw skills sharp.

## Conclusion

Approach is "AI-augmented software engineering" rather than "AI-automated software engineering": classic discipline — design before coding, tests, version control, standards — matters more when AI writes half the code; the human engineer remains "the director of the show." Notes a new AI-assisted engineering book with O'Reilly with free tips on the book site.

**Covers:** Customize the AI's behavior with rules and examples / Embrace testing and automation as force multipliers / Continuously learn and adapt / Conclusion
