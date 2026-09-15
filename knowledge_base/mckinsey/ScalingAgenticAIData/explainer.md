# Explainer — Scaling agentic AI with data transformations

A plain-language companion to the McKinsey article "Building the foundations for agentic AI at scale" (listed as "Scaling agentic AI with data transformations"), for a smart reader outside AI and tech.

## What it is

The article is a playbook for getting AI agents — software assistants that can carry out multi-step jobs on their own, like rebooking a shipment or reconciling an invoice — out of pilot projects and into everyday operation. Its core message is that the obstacle is not smarter AI models but the messy data underneath them: scattered records, conflicting definitions, and weak controls. It lays out seven design principles for data systems, four steps for leaders, and a new way of organizing people around agents.

## Why it matters

Companies are spending heavily on agents, yet almost none see real returns: nearly two-thirds have tried agents while fewer than one in ten has scaled them to real value, and eight in ten blame their data. Every failed scale-up burns budget and trust, while competitors that fix their foundations pull ahead. Because agents act without a human double-checking each step, bad data turns small glitches into cascading mistakes — so data readiness is now a business risk, not an engineering nicety.

## How it works

Think of an agent as a new employee who works at superhuman speed but takes every record literally and never asks clarifying questions. For that employee to succeed, the company must first pick a few high-value jobs worth automating, then tidy each layer of its information systems so facts are consistent and traceable. A shared dictionary of business terms — formalized as ontologies, which define business concepts, and knowledge graphs, which link real records into a network — ensures everyone means the same thing by "customer" or "revenue." Quality control shifts from occasional cleanups to always-on monitoring, a gatekeeper service called an AI gateway polices what models may read and logs every access, and people move from doing the work to supervising the agents that do it, with business teams governing daily use and a central team guarding the shared platform.

## Where it is used

The article illustrates the ideas with online retail, where browsing clicks, wish lists, purchases, and support chats must fuse into one coherent customer picture for agents to personalize and fulfill orders. The same pattern fits banks reconciling payments, hospitals coordinating care records, factories rescheduling supply chains, and any organization where agents juggle structured tables and messy documents under audit scrutiny.

## Takeaways

First, treat data as the product and agents as its customers: invest in shared definitions, reusable data assets, and continuous quality before chasing more use cases. Second, evolve rather than rebuild, but refuse shortcuts that let clever models mask broken architecture. Third, govern agents with the same rules as every other system, enforced automatically, and split accountability so business domains run daily oversight while a central team owns guardrails.

## Jargon decoder

- Agent: software that pursues a goal through multiple steps, using tools and data with limited human input.
- Agentify: redesign a workflow so agents perform it with greater autonomy.
- Data product: a curated data set packaged with an owner, quality guarantees, and a stable way to use it.
- Semantic layer: the shared business dictionary, built from ontologies and knowledge graphs, that gives data machine-readable meaning.
- Medallion architecture: a staged cleanup pipeline that refines raw data step by step into trusted agent-ready records.
- AI gateway: a control point that decides which models may access which unstructured data and records each access.
- Model Context Protocol and agent-to-agent communication: emerging standards letting agents and tools exchange context and coordinate.
- Lineage: the recorded history of where data came from and how it changed.
- Federated governance: business units run daily oversight of their agent workflows while a central team maintains shared platforms and guardrails.
