# Unleashing developer productivity with generative AI

**Article:** [Unleashing developer productivity with generative AI](https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/unleashing-developer-productivity-with-generative-ai)

## Human Readable TL;DR

Imagine giving every programmer a tireless junior helper that drafts routine work in seconds. In McKinsey's experiment, coding chores got done up to twice as fast, programmers felt happier and more focused, and quality held steady — like a kitchen where prep cooks handle all the chopping so chefs can concentrate on the actual cooking. The catch is that the helper knows nothing about your business and sometimes makes confident mistakes, so experts must still taste every dish before it goes out.

---

## TL;DR

McKinsey's June 2023 lab study assigned more than 40 developers to perform code generation, refactoring, and documentation tasks with and without two generative Artificial Intelligence (AI) tools, rotating each developer through both conditions. Assisted developers finished standard tasks up to twice as fast — documentation in half the time, new code in nearly half, refactoring in nearly two-thirds — with no quality loss and more than double the reported happiness and flow. Gains collapsed below 10 percent on highly complex tasks and reversed for developers with under a year of experience, leading the authors to prescribe training, broader use cases, skill planning, and risk governance.

---

## Problem & Motivation

Technology leaders face intense pressure to ship software faster with scarce engineering talent, and generative AI assistants arrived with bold vendor claims but almost no controlled evidence about where they actually help. Without measurements, companies risk either underinvesting in a genuine lever or deploying tools naively and harvesting errors at higher speed. McKinsey built an ongoing developer lab to supply that evidence, quantifying speed, quality, and experience effects and identifying what leadership must do to convert time savings into real productivity without amplifying privacy, legal, ethical, and security risks.

---

## Main Original Ideas

1. **Controlled lab measurement of AI-assisted coding.** Rather than relying on satisfaction surveys, the study ran a test/control experiment with within-subject rotation across three task types, combining self-recorded timing, judge-evaluated demos, and automated readability, maintainability, and bug checks.
2. **Skill-gated productivity gains.** The study showed the same tools that doubled expert speed on routine tasks delivered under 10 percent savings on complex tasks and slowed junior developers by 7 to 10 percent, framing AI as a multiplier of existing skill rather than a substitute.
3. **Dual-tool compounding.** Developers using both a general prompt-driven model and a code-tuned model on one task gained an extra 1.5 to 2.5 times improvement over single-tool use, motivating combined deployments beyond plain code generation.
4. **Developer experience as a business outcome.** The finding that assisted developers were more than twice as likely to report happiness, fulfillment, and flow turned morale into a retention argument for adoption, not a side benefit.
5. **Four-priority rollout playbook.** Training and coaching, advanced use cases, skill-shift planning, and risk controls translate the lab results into an actionable leadership agenda tied to four named governance risks.

---

## Key Findings

| Task / outcome | Result with generative AI |
|---|---|
| Code documentation | Completed in half the time |
| Writing new code | Completed in nearly half the time |
| Code refactoring | Completed in nearly two-thirds the time |
| High-complexity tasks | Under 10 percent time saved, but 25–30 percent more likely to finish on time |
| Junior developers (< 1 year) | 7–10 percent slower on some tasks |
| Code quality | No sacrifice when collaborating; readability marginally better |
| Developer experience | More than 2x reports of happiness, fulfillment, flow |
| Dual-tool versus single-tool use | Extra 1.5–2.5x time improvement |

- The tools excelled at repetitive work, first drafts from a blank screen, faster edits to existing code, and ramp-up on unfamiliar code bases, languages, and frameworks.
- Human oversight stayed essential for hunting AI-introduced bugs, where participants had to "spoon-feed" the tool, and for supplying project context such as interfaces, data, and security requirements through prompting.
- Effective prompting gated the gains: developers who prompted well made larger, faster changes, while those lacking foundations could not steer or verify outputs.

---

## Suggestions & Future Directions

1. Train every developer in prompt engineering with hands-on exercises, plus workshops on data privacy, intellectual-property issues, and reviewing AI-assisted code for design, functionality, complexity, standards, and quality.
2. Give developers with under a year of experience extra coursework in syntax, data structures, algorithms, design patterns, and debugging, sustained by senior coaching and community channels for sharing examples.
3. Pursue combined and advanced use cases beyond single-tool code generation, exploiting the compounding effect of general and code-tuned models together.
4. Plan deliberately for skill shifts by redirecting freed capacity toward business expansion and frequent product updates while building design and architecture skills.
5. Install governance for four risks: privacy and third-party exposure via prompts, regulatory change including the General Data Protection Regulation, ethics and reputation around contested code ownership, and security vulnerabilities in generated code.
6. Treat the lab as ongoing: keep measuring new tools and long-term effects on production codebases, team coordination, and junior skill formation, which the short study could not observe.

---

## Authors & Institutions

Begum Karaci Deniz, McKinsey Digital, Chandra Gnanasambandam, McKinsey Digital, Martin Harrysson, McKinsey Digital, Alharith Hussin, McKinsey Digital, Shivam Srivastava, McKinsey Digital.
