> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Benchmarks and the 90% Saving
**In one sentence:** On a Java monorepo across four scenarios, delegating bulk reads to the worker mode cut the tokens Claude consumes by about 90% on average.
## Key points
- The test setup was a Java monorepo with four scenarios that compared tokens Claude would use when reading files directly against tokens Claude used when receiving the bulk-reader summary or using the code-writer path.
- Mean saving for bulk reads was around 90%, meaning Claude consumed only about one tenth of the tokens it would have used by reading the full files itself.
- The code-write case was harder to measure because without delegation Claude both reads the reference files and produces the new code as costly output tokens.
- With delegation for code-write, the new code goes straight to disk and Claude never sees it, so both the reference reads and the output tokens are avoided.
- The saving happens because the large set of files goes to the cheap worker model, and only a short summary comes back into Claude's context.
- The article did not publish a per-scenario table, so individual results for each of the four scenarios are not known.
- These are author-run benchmarks on one single repo, so they show what is possible in that setup rather than a promise for every codebase.
---
## Setup
The article tested the approach on a Java monorepo. A monorepo is one large shared code store for many parts of a project. There were four scenarios. In each scenario, the comparison was simple: how many tokens Claude would consume by reading the files directly, against how many tokens Claude consumed when the work went through the bulk-reader summary or through the code-writer.
## The 90% number
The headline number is a mean saving of around 90% for bulk reads. In plain words, when Claude needed an answer that required reading several large files, letting the worker read them and return a short summary used about one tenth of the Claude tokens. The article states this as an average and does not give exact numbers for each scenario.
| Scenario | What was compared | Per-scenario saving |
| --- | --- | --- |
| Scenario 1 of 4, not named in the article | Direct reads by Claude vs short summary for Claude | Not published in the article |
| Scenario 2 of 4, not named in the article | Direct reads by Claude vs short summary for Claude | Not published in the article |
| Scenario 3 of 4, not named in the article | Direct reads by Claude vs short summary for Claude | Not published in the article |
| Scenario 4 of 4, code-write case | Reading references plus writing code vs code straight to disk | Harder to measure, no separate number published |
## Why code-write is measured differently
Bulk reads are easy to compare because the input is the main cost. Code-write is different because it has two costs at once. Without delegation, Claude reads the reference files and then writes out the new code, and writing output tokens is costly. With delegation, the worker writes the new file directly to disk. Claude never reads the references in full and never produces the output, so both kinds of cost disappear. That makes a single clean percentage harder to give.
## Where the saving comes from
The mechanism is simple. The large files still get read, but they are read by the cheaper worker model instead of by Claude. Only the short answer or summary enters Claude's context. For code-write there is a second saving: Claude avoids producing the long new file token by token. So Claude spends tokens only on the small question, the small summary, and the next reasoning step.
## What the benchmarks do not show
The benchmarks do not show a detailed breakdown per scenario, so we cannot say which kind of question saved most. They do not show results on other languages or other repos, since only one Java monorepo was used. They were run by the article author, not by an outside lab, so treat them as a field report rather than an independent test. They also do not measure reasoning quality, edit accuracy, or time delay, only the drop in tokens Claude consumes.
**Covers:** article section "The benchmarks".
