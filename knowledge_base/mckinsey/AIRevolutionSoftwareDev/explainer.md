# Explainer — The AI revolution in software development

## What it is

Picture a bank in London where three engineers walk in at 8 a.m. and discover that nearly a hundred artificial intelligence (AI) assistants worked all night: polishing a payment system, stress-testing it, and preparing a tidy stack of proposed changes for the humans to approve over morning coffee. That scene opens a McKinsey article arguing that building software is changing the way factory work changed a century ago — from craftsmen hand-making every part to supervisors running machines that do the repetitive work while people handle judgment calls. The authors sort this change into four stages, from writing every line by hand, through autocomplete-style help where most companies sit today, to AI drafting whole features, and finally to small human teams directing fleets of AI agents that build entire applications.

## Why it matters

Software runs everything, yet there are never enough programmers and big projects are slow and expensive. If a handful of people can genuinely do the work of a whole department — the article cites a large bank moving ten times faster at half the cost — the economics of every digital business shift: products reach customers sooner, experiments get cheaper, and small teams can take on ambitious projects. The catch the article keeps repeating is that buying AI tools alone does not deliver this; companies must reorganize how work flows, who reviews what, and where humans stay in charge, or the gains evaporate.

## How it works

The mechanism has two halves. First, humans stop writing routine code and start supplying context and constraints: they describe what should be built, fix the order in which AI agents act, and define templates for what good output looks like. Second, agents execute inside those guardrails overnight or continuously — writing code, generating tests, documenting, running legal and security checks — and return three things for morning review: the proposed change, evidence it works, and flags marking anything risky or uncertain. Humans then approve, adjust priorities, or send work back. The article's memorable rule is that quality comes from good context, not clever phrasing: no amount of witty chatting with the machine substitutes for precise specifications and well-organized background information.

## Where used

The showcase is a global systemically important bank running this agent-factory model with daily human check-ins, plus reported results from a financial services firm at 40–70 percent higher productivity and an airline at 50 percent gains with smaller teams. The pattern generalizes to any organization with large, long-lived software: banks, airlines, retailers, and technology firms modernizing old systems or shipping new products. Early stages are already mainstream — most developers now use AI completion daily — while full end-to-end agent delivery remains experimental frontier practice.

## Takeaways

First, the bottleneck in software is moving from writing code to reviewing machine-made code, so verification capacity matters more than typing speed. Second, context is the real input: teams that write crisp requirements and keep machine-readable knowledge about their systems will outperform teams with better prompts but messier facts. Third, process redesign beats tool purchase — bolting chatbots onto old routines yields shallow gains while restructured teams capture the large ones. Fourth, human accountability grows rather than shrinks, since someone must own safety, legality, and the final call on every release the agents propose.

## Jargon decoder

- **Generative AI:** AI that produces new text, code, or designs from a description rather than just analyzing existing data.
- **Large language model (LLM):** the engine behind tools like coding assistants, trained on vast text and code to predict plausible continuations.
- **AI agent:** an AI setup that does not just answer once but plans and carries out multi-step jobs, using tools like code editors and test runners.
- **Agent factory:** an operating model where coordinated teams of AI agents build software continuously under human supervision, like a production line.
- **G-SIB:** global systemically important bank — one of the world's largest banks, subject to the strictest regulation.
- **Pull request / test evidence / risk flag:** the three review artifacts — a proposed code change, proof it passes tests, and a marker calling out uncertainty or danger.
- **Idea-to-impact cycle time:** how long it takes from having an idea to seeing its effect on customers or the business.
