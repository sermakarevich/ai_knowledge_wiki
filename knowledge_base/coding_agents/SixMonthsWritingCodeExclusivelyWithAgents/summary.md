# Six Months of Writing Code Exclusively With Agents - exe.dev blog

**Article:** [Six Months of Writing Code Exclusively With Agents](https://blog.exe.dev/engineering-with-ai) — exe.dev blog

## Human Readable TL;DR

A programmer who used to carry his whole software system in his head like a chef who has every recipe memorised decided to stop typing code for six months and let AI helpers do all the typing instead. At first it was like sharing one tiny kitchen with a dozen cooks who kept bumping into each other, so he gave every cook their own kitchen — a separate computer in the cloud — and built a phone app to check on them all. He learned the most useful helpers were not the ones writing new dishes but the ones tasting, spotting intruders, and watching the oven during dinner service, while his real job shifted from chopping vegetables to deciding which dishes belonged on the menu at all.

## TL;DR

After models crossed a capability threshold with Claude Code, GPT-5.3 and Opus 4.6, the author adopted a February rule of writing no code by hand for six months and scaled from one agent to around twenty parallel exe.dev Linux VMs managed by a mobile-first tool called botd, with YOLO-mode agents inside disposable VMs, proxied credentials, and agent-run tests, CI, browser checks and peer review. The experiment showed that shipping becomes cheap while deciding what is worth shipping becomes the bottleneck, that up-front system design, contracts, behavior-level tests and hygiene matter more under agents, and that non-coding agents for investigation, red-teaming and deployment watching often deliver the most value — a lesson driven home when botd itself collapsed because it had been vibe-coded without understood architecture, while its SQLite conversation history survived and remained queryable.

---

## Problem & Motivation

The author's long-standing advantage was a deep, hard-earned mental model of the entire system, especially the interfaces between components, unwritten assumptions, and which exact line mattered, maintained by reading every change and by hand-writing multi-layer edits across handlers, schema, tests and docs with asymmetric risk. Hand-writing had become the bottleneck just as agents became capable enough to sustain real work, so the February no-code rule was adopted as a forcing function in the spirit of learning to code itself: rather than finishing stuck work by hand, fix the prompts, tools or environment that left the agent stuck, and build reps until agent-driven development was understood from practice. Parallelism then grew almost accidentally out of idle time between agent turns, which exposed collisions on a shared box, the limits of worktrees and AGENTS.md patches and containers, and finally motivated one VM per task plus botd to preserve off-laptop progress, enable phone-driven supervision, and retain every conversation as a queryable record of how the work was actually done.

## Main Original Ideas

1. **The February no-hand-code rule.** A six-month commitment, broken only once for three minutes, to never finish code by hand but instead repair whatever the agent was missing, turning each failure into an improvement in prompts, tools or environment rather than a reversion to typing.

2. **One VM per task plus botd.** An evolution from a shared dev box through worktrees and container isolation to a dedicated exe.dev Linux VM per task with a scripted dev-environment bootstrap, coordinated by botd under three rules — run off-laptop, be mobile-first, and preserve every conversation — with status tracking, remote inspection, follow-ups and diff review from phone or laptop.

3. **YOLO inside, paranoid outside.** Letting agents run unrestricted bash, installs and services inside disposable VMs to avoid making the human the approval queue, while treating external access as the real risk through read-only defaults, write limits to test environments, credential proxying so secrets never live in the VM, and attention to dangerous tool combinations rather than blind tool minimisation.

4. **Non-coding agents as the highest-leverage roles.** Defining an agent as a model in a loop with tools, where tools determine what the agent can be, and deploying investigators that work from verbatim customer reports against ClickHouse logs and code, a red-team agent tasked simply with breaking in, and Athena the deployment watcher that reads diffs, metrics and logs during wave rollouts and can distinguish infrastructure failures from bad code.

5. **Agentic engineering versus vibe coding.** Insisting on designing architecture, interfaces, constraints and tradeoffs with the agent before accepting code, illustrated by the Shelley async-tools redesign where discussion eliminated edge cases by giving every command the same path into the background after sixty seconds, against the failure mode of inheriting a brand-new legacy codebase whose decisions were never understood.

6. **History as a queryable asset.** Preserving all agent conversations in SQLite so past decisions, discarded designs, effective instructions and recurring failure modes can be searched and reconstructed later, which proved its value when the conversation analysis survived even after the tool that collected it died.

## Key Findings

At peak scale of around twenty simultaneous VMs, manual validation could not keep up, so agents ran tests, triggered full CI, launched the app, drove it in a browser and supplied screenshots, while peer-agent reviews caught occasional real bugs cheaply enough to run repeatedly. Yet the agent was grading its own work and could confidently build and test the wrong thing, diffs arrived whole and unfamiliar so the author still had to load each change into his head before merging, and even green, good-looking changes were discarded because no tool could say whether added complexity was worth carrying given Hyrum's Law and the difficulty of unshipping. Parallel agents amplified both throughput and hygiene effects: more was shipped than in any prior career stretch, but there were also more abandoned tasks, dead-end designs and failures, alongside the finding that good patterns amplify and bad tolerated patterns become templates for the next hundred changes. The sharpest demonstration was botd itself, which delivered enormous work but crumbled under its own weight because driving every model family through its native harness without an understood architecture was exactly the kind of problem where architecture matters, confirming that implementation-mirroring unit tests churn while behavior, contract and property tests, careful migration and state handling, and cheap bespoke tools such as new linters carry the weight under agents.

## Suggestions & Future Directions

The article's direction is to move iteration up a level from code to prompts, designs and whole features, where a rewrite that once cost a week costs a conversation and failures stay cheap enough to afford many of them. It recommends giving agents full developer-grade computers, isolating environments while watching risky combinations of private data, untrusted content and external communication, and investing validation earlier in design discussion, contracts and independent end-to-end checks rather than late-stage peer code review, which the author reports abandoning at exe.dev in favour of merging code deemed worth merging. It further suggests encoding each lesson as tooling and tests that survive code churn, treating migrations and risk management as the enduring hard part of systems work, and keeping complete, searchable conversation history so future agents and humans can recover why a system looks the way it does. The closing stance is that stopping hand-writing did not stop engineering but relocated it: shipping got easy, so deciding what to ship, and understanding what will be owned after the code arrives, got important.

## Authors & Institutions

The wiki materials describe a single practitioner-author associated with exe.dev, working with Claude Code, Codex, Shelley and the in-house botd system on exe.dev Linux VM infrastructure, with acknowledgement of Simon Willison for the lethal-trifecta framing of tool-combination risk. No formal paper authors, affiliations or publication date are stated in the wiki sources, so the attribution rests on the exe.dev blog context and the first-person engineering account synthesised above.
