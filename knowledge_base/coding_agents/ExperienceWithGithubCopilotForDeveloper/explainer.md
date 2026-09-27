> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Experience with GitHub Copilot for Developer — In Plain Language

## What is this about?

This is a real-company story about trying out GitHub Copilot, an AI helper that suggests code while you type.

The company is Zoominfo, a large business-data company with about 4,000 employees, roughly 400 working developers, thousands of code repositories, and teams spread across the US, Europe, India, and Israel.

They did not just turn Copilot on for everyone at once. They tested it in four careful steps over July to September 2023: a tiny 5-person tryout, a signup phase for 126 engineers, a two-week trial with surveys, and then a slow rollout to everyone.

Later they measured what happened in real daily work over 26 days in late 2024: about 6,500 suggestions and 15,000 suggested lines per day.

The headline numbers: developers kept about one-third of suggestions (33%) and about one-fifth of suggested lines (20%), reported saving roughly 20% of their time, and gave 72% satisfaction.

## Why does it matter?

Most claims about AI coding helpers come from small demos, student homework, or short lab tests.

This study is different because it shows what happens with hundreds of professional developers, working on real products, in several programming languages, over months — not just a weekend experiment.

That makes the numbers more trustworthy for other companies asking: "Is this worth buying? Will our developers actually like it? Where does it help, and where does it fail?"

It also matters because the results are honest about limits. Copilot helped a lot with boring, repetitive work but was weaker on company-specific business logic, unusual tasks, and some languages like HTML, CSS, JSON, and SQL.

So the lesson is balanced: real time savings, but you still need human review, security training, and realistic expectations.

## How does it work?

Think of Copilot as a very fast autocomplete trained on billions of lines of public code.

As you type, it looks at the surrounding code and pops up a suggestion — sometimes one line, sometimes a whole small function, usually around 2 to 3 lines at a time.

You can accept it, partly accept and edit it, or ignore it.

Zoominfo judged success mainly with a simple score called "acceptance rate": out of 100 suggestions shown, how many did the developer keep?

They tracked two versions of this score: one for whole suggestions (33% kept) and one for individual lines (20% kept). The line score is lower because people often keep part of a suggestion and rewrite the rest.

To decide whether to roll it out, they also used surveys. The early 5-person group rated experience 8.8 out of 10 and productivity gain 8.6 out of 10. The bigger 126-person trial rated satisfaction 8.0, productivity gain 7.6, and security confidence around 8 out of 10.

Rollout was paced through a ServiceNow request system so licenses, security training, and compliance agreements could be tracked person by person.

## Where can this be used?

The study found Copilot most useful for everyday, repetitive coding chores.

Best uses reported:

- Writing boilerplate — the standard, repeated setup code every project needs.
- Writing unit tests — small automatic checks that verify code behaves correctly.
- Suggesting clear variable names, comments, and short documentation.
- Acting like a second pair of eyes that spots possible bugs and nudges code toward common best practices.
- Helping newcomers and juniors learn a codebase, a new language, or a new library faster.

It worked best in the company's main languages — TypeScript, Java, Python, and JavaScript — which made up about 80% of all suggestions. Those held steady near 30% acceptance.

It was less useful for HTML, CSS, JSON, and SQL, for tasks needing deep knowledge of Zoominfo's own business rules, and for brand-new or highly creative designs.

Both JetBrains and VS Code editors showed similar suggestion acceptance near 30%, so the benefit was not tied to one editor.

## Conclusions & takeaways

Copilot earned its place: about one in three suggestions kept, hundreds of thousands of AI-assisted lines in the codebase, roughly 20% time saved, and nearly three-quarters of developers satisfied.

The phased rollout worked well. Starting small, requiring security training and written policy agreement, surveying honestly, and then expanding slowly avoided big surprises and found no drop in pull-request quality.

But it is not magic. The code is not always right, style and quality can be uneven, and developers still had to edit and double-check suggestions — especially for domain-specific logic.

Other research cited in the paper agrees: results vary widely by task, language, and setup. Some studies show strong speedups; others show many failing tests, shaky answers to reworded questions, or privacy risks.

Bottom line for teams: use Copilot for routine code and tests, keep human review and security checks, train people not to over-trust it, and study long-term effects on quality, maintenance, delivery speed, and learning before calling it a full success.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| AI pair programmer | An AI helper that suggests code beside you, like a junior partner watching your screen. |
| Suggestion acceptance rate | Out of 100 pop-up suggestions, how many the developer kept. Here: 33 out of 100. |
| Line acceptance rate | Out of 100 suggested lines, how many were kept. Here: 20 out of 100. |
| Boilerplate code | Boring, repeated setup code that looks similar in every project. |
| Unit test | A tiny automatic check that makes sure one small piece of code works. |
| Pull request | A packaged set of code changes a teammate reviews before it goes live. |
| DORA metrics | Four standard scores for how fast and reliably a team ships software. |
| Domain-specific logic | Rules unique to one company, like how Zoominfo handles its own customer data. |
| Stratified sampling | Picking trial volunteers so different roles, levels, places, and tools are all represented. |
| Telemetry | Automatic usage data the tool sends back, which can raise privacy questions. |
