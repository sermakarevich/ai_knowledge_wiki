> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Benchmarking Prompt Engineering Techniques for — In Plain Language

## What is this about?
This paper asks a simple question: can you get AI coding assistants to write
safer code just by wording your request differently?

The authors test this on three OpenAI models — GPT-3.5-turbo, GPT-4o-mini,
and GPT-4o. They feed each model 202 risky Python programming tasks (things
like handling passwords, SQL queries, or file uploads) and try out different
prompt tricks: adding a security reminder before the request, appending a
"make it secure" note after it, or asking the model to review and fix its own
answer afterwards.

Every generated program is then checked automatically for known security
flaws, so the tricks can be compared fairly.

## Why does it matter?
AI-generated code often looks correct but hides vulnerabilities. Earlier
studies cited in the paper found roughly a quarter to 40% of AI-assisted
snippets had security issues, and one test saw GPT-3.5 write secure programs
in only 5 of 21 tasks.

Worse, programmers tend to trust the assistant's output and even rate insecure
code as safe. If a one-line reminder or an automatic self-review can cut the
number of vulnerable programs in half, that is a cheap win — no retraining of
the model, no new tools to install.

This study is one of the first to measure that idea systematically, with
multiple samples per prompt and realistic model settings, instead of a single
try at zero randomness.

## How does it work?
Think of the benchmark as an assembly line with six stations:

1. **Risky prompts.** The team collects 202 Python tasks chosen to tempt the
   model into mistakes, drawn from two existing research datasets
   (LLMSecEval and SecurityEval). Each task is tagged with the weakness it
   might trigger, such as SQL injection.
2. **Prompt augmentation.** Each task is copied many times, each copy with a
   different trick applied. The simplest tricks add one sentence: for
   example, the prefix "You are a developer who is very security-aware and
   avoids weaknesses in the code." Others append "make sure every line is
   secure." The fancier trick is RCI — Recursive Criticism and Improvement —
   where the model is shown its own code and asked to critique it, then to
   rewrite it based on that critique. As a sanity check, one "adversarial"
   prompt deliberately asks for vulnerable code.
3. **Response generation.** Each modified prompt is sent to the model 10
   times (simulating 10 different developers), using the normal default
   settings rather than forcing deterministic output.
4. **Code extraction.** Chat answers mix explanation with code, so a script
   pulls out the code blocks and checks they are valid Python, asking the
   model to reformat if needed.
5. **Security scan.** Every sample is scanned by two independent static
   checkers, Semgrep and CodeQL. A sample only counts as vulnerable if both
   agree it contains the suspected weakness — a strict rule that filters out
   many false alarms.
6. **Scoring.** The headline score, SAFVS, is the percentage of samples both
   scanners flag. Repeating the whole run gives a spread of scores (OFVP),
   showing how much results wobble by chance.

The team also spot-checks that safer prompts do not break functionality,
using the standard HumanEval coding test.

## Where can this be used?
- **Everyday prompting.** If you use an AI coding assistant, starting your
  request with a security-aware role ("you are a security-aware developer…")
  measurably reduces flaws on the newer GPT-4o-family models — free and
  instant.
- **Coding-assistant products.** The authors build a demo "Prompt Agent" on
  top of a chat interface that silently adds that prefix before sending your
  request to the model, plus an optional self-review pass. Tool vendors could
  ship the same idea: a "secure mode" toggle.
- **Automated repair loops.** RCI-style review-then-fix passes catch flaws
  the first draft missed. That pattern fits CI pipelines or IDE plugins that
  re-check generated code before it is committed — at the cost of extra model
  calls and waiting time (over 10 seconds per snippet in the demo).
- **Benchmarking other models.** The open-source harness (prompt sets,
  extraction, scanning, scoring) can be reused to test new models, new
  prompt wordings, or other languages beyond Python.

## Conclusions & takeaways
- A single well-chosen sentence is the best cheap trick: the security-aware
  prefix cut vulnerable samples by about 47% on GPT-4o-mini and 56% on
  GPT-4o.
- Asking the model to review and fix its own code (RCI) is the strongest
  trick overall: one round fixed roughly 25% of flawed snippets on
  GPT-3.5-turbo, 50% on GPT-4o-mini, and 65% on GPT-4o. Combining the prefix
  with RCI reached nearly 69% fewer vulnerabilities on GPT-4o.
- Older and newer models behave differently. On GPT-3.5-turbo, most proactive
  security reminders backfired and made things worse; only after-the-fact
  review helped. Newer models are far more responsive to wording — for better
  (secure prefix) and for worse (the adversarial prompt pushed GPT-4o to
  153% more vulnerabilities).
- There are trade-offs: RCI costs extra calls, adds latency, can be overly
  verbose, and slightly lowered first-try correctness in the functionality
  check. Returns also diminish after a couple of review rounds.
- Caveats: results rest on two automated scanners (which miss things), on
  short isolated Python snippets, on OpenAI models only, and without formal
  statistical significance tests. Treat the percentages as strong signals,
  not guarantees.

## Jargon decoder
| Term | What it means in plain language |
|---|---|
| Prompt engineering | Changing the wording of your request to get better answers, without changing the model itself. |
| Prefix / suffix | An extra sentence added before (prefix) or after (suffix) your task, e.g. "write secure code". |
| RCI (Recursive Criticism and Improvement) | Asking the model to critique its own code for security holes, then rewrite it — repeatable over rounds. |
| Chain-of-thought (CoT) | Asking the model to reason step by step before giving the final code. |
| CWE (Common Weakness Enumeration) | A numbered catalogue of known software weakness types, e.g. SQL injection. |
| Semgrep / CodeQL | Automated tools that scan code for bug and security patterns without running it. |
| SAFVS | The study's strict score: share of samples where both scanners agree a flaw is present. |
| Temperature | A randomness dial for the model; the study uses the normal default (1), not forced-deterministic output. |
| AST (Abstract Syntax Tree) | The model's internal map of code structure; used here just to check the extracted code is valid Python. |
| HumanEval (pass@1 / pass@10) | A standard test of whether generated code actually runs correctly, on the first try or within 10 tries. |
