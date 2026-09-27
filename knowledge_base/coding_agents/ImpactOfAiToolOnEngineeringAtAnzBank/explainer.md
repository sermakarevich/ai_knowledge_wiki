> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# THE IMPACT OF AI TOOL ON ENGINEERING AT — In Plain Language

## What is this about?

This paper asks a simple question: does giving bank engineers an AI
coding assistant actually help them work better?

The setting is ANZ Bank, which employs more than 5,000 engineers.
Before rolling GitHub Copilot out to everyone, its Architecture and
Engineering team ran a careful six-week experiment in mid-June to
end-July 2023 with just over 100 volunteer engineers.

The experiment had two phases. In the first two weeks, engineers used
Copilot on everyday tasks and reported how it felt. In the next phase,
they were split into two groups — one with Copilot switched on, one
with it switched off — and both groups solved the same short Python
coding puzzles.

The team measured four things: how fast people worked, how good the
code was, whether the code was secure, and how engineers felt about
the tool.

The headline finding: Copilot users finished tasks about 42% faster,
their code had fewer bugs and quality warnings, security results were
too thin to judge, and engineers felt mildly positive about the tool.

## Why does it matter?

Banks run on software, and 5,000 engineers writing code is expensive.
If an AI assistant makes them meaningfully faster without hurting
quality, that is a big deal — more features shipped, less time spent
on repetitive typing.

But there are real risks. AI-generated code could leak secrets, break
intellectual-property rules, introduce security holes, or look right
while being subtly wrong. A bank cannot simply hand a new tool to
everyone and hope for the best.

That is why this study matters: it is a methodical "try before you
buy" guide. It shows how a large, regulated organisation can test an
AI pair-programmer under controlled conditions, weigh the numbers
against the risks, and only then decide to roll it out — which ANZ
did, reaching 1,000+ users by the time the paper was written.

It also matters because it is honest about limits: small puzzles are
not real banking software, participation wobbled over six weeks, and
security could not really be tested this way.

## How does it work?

Think of the experiment as a fair race with a mid-race shoe swap.

First, everyone answers a background survey (role, Python skill), and
legal and security teams set ground rules for safe Copilot use.
Everyone uses the same editor (VS Code) so usage statistics stay
comparable.

Then comes the crossover race. In week 3, Group A gets Copilot and
Group B does not. In week 4, they swap: Group B gets Copilot and
Group A loses it. Each week has six short algorithmic challenges —
12 in total — all in Python so grading stays uniform. The group
without Copilot may still use Google and Stack Overflow, just like
normal work.

After each puzzle, each engineer reports how many minutes it took.
Their code is also graded by the experiment team, run against unit
tests, and scanned by a static-analysis tool (SonarQube) that flags
bugs, suspicious patterns, and security holes. Separately, GitHub
itself reports how often Copilot suggestions were shown and accepted.

Because finishing times are lopsided (a few people take very long),
the team cannot use textbook bell-curve statistics. After cleaning
200 data points down to 172 valid ones, they use a non-parametric
paired test (the Wilcoxon signed-rank test) that compares the same
people with and without Copilot, asking: is the Copilot time reliably
lower?

The same style of test is applied to bugs and quality warnings.
Security gets special planted questions — one about hashing passwords
safely, one about a web endpoint that could let attackers inject
commands — but the short puzzles produce almost no security findings
at all.

## Where can this be used?

The most direct use is the one ANZ chose: rolling Copilot out to
thousands of engineers for everyday coding, documentation, unit
tests, and understanding unfamiliar code.

More broadly, any large software organisation can copy the playbook:
pilot with volunteers, survey sentiment every couple of days, then run
a short crossover A/B on standard tasks before buying licences for
everyone.

The results suggest the biggest wins are on speed and toil reduction:
beginners gained the most (about 52% faster), but intermediate and
advanced engineers also gained about 40% each, and the hardest puzzles
showed the largest time savings. Teams drowning in boilerplate,
tests, and docs are the natural first candidates.

What this approach should not be used for is proving security. Short
puzzles barely produce vulnerabilities, so a team that cares about
secure password handling or injection attacks needs longer,
project-style tasks and dedicated security review — which the authors
flag as future work.

## Conclusions & takeaways

- Copilot made ANZ engineers about 42% faster on short Python tasks
  (average 31 minutes down to 18; median 20 down to 10), a result the
  statistics call significant.
- Code quality improved too: fewer bugs and fewer "code smells" with
  Copilot, both statistically significant; unit-test scores were about
  13% higher but not significantly so.
- Security is the open question. Only one scan found anything, so no
  conclusion could be drawn — the data merely showed no major new
  security problems.
- Engineers liked the tool but did not love it: median ratings were
  "somewhat helpful," "a bit less" debugging, "well" aligned with
  standards — positive everywhere, strongly positive nowhere.
- Caveats are real: ~100 fluctuating volunteers are not 5,000
  engineers, times were self-reported, and tiny puzzles leave little
  room for bugs or hacks to appear.
- The bottom line the authors draw: subject to more security analysis,
  productionise Copilot at the bank, and keep studying its effect on
  real operational efficiency.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| GitHub Copilot | An AI assistant inside the code editor that suggests the next lines of code as you type. |
| Pair-programmer | Working with a partner who watches, suggests, and catches mistakes; here the partner is the AI. |
| Control vs Copilot group | The group with the AI switched off versus the group with it switched on, solving identical tasks. |
| Crossover design | Halfway through, the groups swap who gets the AI, so everyone is tested both ways. |
| Null hypothesis (H0) | The default assumption: "Copilot makes no real difference"; statistics try to disprove it. |
| Wilcoxon signed-rank test | A statistical check for paired, lopsided data that asks whether one condition is reliably better. |
| SonarQube | An automated code checker that flags bugs, messy patterns, and security holes. |
| Code smell | Code that runs but is messy or fragile — a hint that it will be hard to maintain. |
| Unit-test success ratio | The share of small automatic correctness checks that the submitted code passes. |
| Vulnerability / injection attack | A weakness an attacker could exploit, e.g. tricking an app into running a malicious command. |
