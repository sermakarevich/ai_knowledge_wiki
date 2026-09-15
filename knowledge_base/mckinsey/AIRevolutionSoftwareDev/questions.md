# Retrieval practice — The AI revolution in software development

## Four levels of developer support

1. Name all four levels of developer support and the productivity claim attached to Level 4.
<details><summary>Answer</summary>Level 1: developing without generative artificial intelligence (AI); Level 2: speeding up individual tasks; Level 3: automating entire workflow steps; Level 4: delivering entire applications end to end — with 20 times leverage.</details>

2. Where do most companies sit today, and what does work look like at that level?
<details><summary>Answer</summary>At Level 2: the developer writes a few lines and the AI suggests the next ten, like a super-fast pair programmer; a meaningful boost, but the human drives everything.</details>

3. What model capability shift enabled the spread of Level 3?
<details><summary>Answer</summary>Large language models evolving from simple inline completion tools into systems that autonomously execute long-running multifile refactoring and modernization tasks.</details>

4. Why is Level 4 described as experimental, and why does that matter for the 20x figure?
<details><summary>Answer</summary>Because few organizations run it at scale yet, so 20x is a frontier ceiling demonstrated by pioneers, not a measured average to plan budgets around.</details>

## The night shift and the agent factory

5. In the opening vignette, how many engineers arrive, how many agent teams worked overnight, and on what system?
<details><summary>Answer</summary>Three engineers; nearly a hundred AI agent teams; a cross-border payment system (refined, failure-path tested, shipped overnight).</details>

6. What three artifacts greet the engineers at the daily review, and what changed about review cadence?
<details><summary>Answer</summary>AI-generated pull requests, test evidence, and risk flags; the sprint review moved from every two weeks to every morning.</details>

7. State the global systemically important bank (G-SIB) agent factory result as two numbers.
<details><summary>Answer</summary>Ten times the speed at half the cost.</details>

8. Why would running Level 4 agents on a Level 2 workflow fail to deliver gains?
<details><summary>Answer</summary>Because the coordination layer was never built: without shared persistent context, predefined activity sequences, and output templates, agents produce unreviewable output and the human review bottleneck eats the speedup.</details>

## Humans declare intent, agents do the work

9. Quote (approximately) the article's division of labor between humans and agents.
<details><summary>Answer</summary>Agents run increasingly complex tasks and workflows — evidence provenance, legal and cyber checks, counterfactual testing, suggesting and making decisions — while humans declare high-level intent and boundaries, evaluate outputs, and react to agentic decisions.</details>

10. Name the three structural payoffs of this shift.
<details><summary>Answer</summary>Smaller teams, much lower unit costs for software development, and much faster idea-to-impact cycle times.</details>

11. What breaks if humans abdicate the evaluation step and auto-merge everything agents propose?
<details><summary>Answer</summary>Accountability collapses: plausible-but-wrong code, untested compliance artifacts, and security or legal exposures ship without a signer, and errors compound because downstream agents inherit unverified outputs.</details>

## Context is the input, discipline is the method

12. State the article's maxim about context versus wording.
<details><summary>Answer</summary>"Good AI output comes from good context, not clever wording. You can't 'chat your way' to production-grade software."</details>

13. What two instruments do the article's engineers use to keep agent work predictable?
<details><summary>Answer</summary>Precisely defined workflows with predefined sequences of agent activities, and structured templates for agentic output.</details>

14. What is the "verify the verifier" trap?
<details><summary>Answer</summary>When the same agent writes the code and its tests, a passing suite is weaker evidence than it appears, so a second judge (agent or human) must check that the tests test the right thing.</details>

## Evidence and the organizational moral

15. Arrange these attributed figures on the ladder: 2x tasks, 16–30%, 40–70%, 50% LATAM, 10x at half cost — and say what each rung represents.
<details><summary>Answer</summary>Task rung: up to 2x on some tasks; strong-adopter ceiling: 16–30%; operating-model rung: 40–70% (finserv agent factory) and 50% (LATAM, smaller teams); frontier showcase: 10x speed at half cost (G-SIB). Higher rungs demand more restructuring.</details>

16. Why should a team not plan its next sprint around the 40–70% or 10x figures?
<details><summary>Answer</summary>They are single-organization ceiling cases reported without published methodology — best observed outcomes under full restructuring, not medians a typical team can expect on arrival.</details>

17. Transfer: your team runs AI completion inside an unchanged ticket-and-ceremony process and sees only thin gains. Following this article, name two concrete changes beyond buying more licenses.
<details><summary>Answer</summary>Any two of: turn requirements into machine-usable context with acceptance criteria; predefine agent activity sequences with verification gates; standardize output templates; institute daily evidence-and-risk-flag reviews; add governance for security, privacy, and IP with human sign-off.</details>
