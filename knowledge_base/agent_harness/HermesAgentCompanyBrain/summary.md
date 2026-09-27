# Hermes Agent Full Guide: Give Hermes a Company Brain

**Source:** [Hermes Agent FULL GUIDE (Box Developers / Chris Kim, 2026)](https://x.com/boxplatform/status/2067668340831850964)
**Type:** Developer tutorial (X long-form article)
**Author:** Chris Kim (@chriskim_dev) for Box Developers (@BoxPlatform)
**Date:** 2026-06-18

## Human Readable TL;DR

Imagine a smart assistant that only ever sees its own private copy of your team's files, so it never knows which version is the "real" one and can't see your coworkers' notes. This guide gives that assistant its own employee badge and a shared filing cabinet (Box) that the whole team uses too. Now the assistant and your teammates all read and write from the same drawer, so nobody works off a stale copy and the robot only touches the folders you let it into.

## TL;DR

Step-by-step tutorial for connecting NousResearch's Hermes Agent to Box cloud storage so an AI agent shares the same files, comments, and versions as a human team. The agent runs 24/7 on a VPS (DigitalOcean Droplet) with Slack as its gateway, and talks to Box through the Box CLI. The key design choice: authenticate the agent with a Box Client Credentials Grant (CCG) **service account** instead of a personal user, giving the agent its own identity scoped to only the folders explicitly shared with it.

---

## Problem & Motivation

AI agents like Hermes are strong for individual productivity but **siloed** — they operate from their own local copy of a project. Agent-to-human and agent-to-agent handoffs break because everyone (human and machine) works from different context. Typical failure: ZIPs dropped in Slack, version sprawl (`video_project_v2_FINAL.zip`, `final_final_revised.mov`), buried feedback, edits to the wrong file. An agent in that loop makes it worse by confidently acting on a stale local copy.

Fix: give agents the same shared workspace the team already uses — one source of truth they all draw from. Box is that workspace.

---

## Main Original Ideas

1. **Service-account identity, not personal account** — Create a Box CCG app so Hermes authenticates with its own server-side identity (`AutomationUser_...@boxdevedition.com`), not the developer's personal Box user. Clean security boundary: Hermes sees only folders explicitly shared with it.

2. **Box as the "company brain"** — A single shared project folder becomes the durable source of truth for humans and agents alike. The agent reads current truth on every run, never last week's copy.

3. **Headless Box via Box CLI** — Installing `@box/cli` on the VPS makes Box fully headless. Hermes performs all Box operations (read, upload, create, organize) by issuing CLI commands.

4. **Self-improvement loop** — Rather than hand-authoring every command, you give Hermes a task and let it learn the Box CLI from the environment, building its own reusable `box-cli` skill. Demonstrated in the video: Hermes created the skill itself.

5. **Multi-agent / multi-interface convergence** — "Different teams. Different agents. Different interfaces. Same shared workspace." A second agent on a teammate's machine can later pull the same folder and continue the work.

---

## Key Findings

What you build by the end:

- Hermes Agent running on a VPS with **Slack as the gateway**
- **Box CLI** installed on the same server
- A Box app using **Client Credentials Grant (CCG)** auth
- A dedicated Box **service account** for Hermes
- A shared project folder = workspace for humans + agents
- A repeatable pattern for agentic workflows (upload, read, analyze, organize in Box)

Build steps:

| Step | Action |
|------|--------|
| 1 | Create a DigitalOcean Droplet (Ubuntu 24.04, 1 vCPU, 2 GB RAM, SSH key, monitoring) |
| 2 | Install Hermes Agent; `hermes setup`, pick a model provider, verify with "Hello" |
| 3 | Create Slack app + configure Hermes Gateway (install as system service so it survives reboot) |
| 4 | Install Box CLI: `npm install --global @box/cli` |
| 5 | Create Box CCG app; write `box-ccg-config.json`; add + set CLI environment; verify with `box users:get` |
| 6 | Share project folder with the automation user email (the security boundary) |

Suggested guardrail instructions for Hermes:

- Always use the Box CLI service environment.
- Only operate inside the approved project folder.
- Ask before deleting or overwriting content.
- Preserve version history whenever possible.
- Treat Box as the durable source of truth.

---

## Suggestions & Future Directions

Real-world scenarios the author proposes once the shared brain exists:

1. **Content & marketing** — editor drops final cut, writer comments, Hermes generates captions/YouTube description/thumbnail concepts and saves to the launch folder.
2. **Product launch coordination** — Hermes reads spec + mockups + QA notes, drafts a go/no-go checklist and one-page launch brief; re-run when the spec changes.
3. **Engineering** — summarize open issues + design doc in an Auth-Service folder, draft release notes for a deploy. Doubles as onboarding (new engineer + their agent read the same folder).
4. **Personal side projects** — workout logs + recipes → meal-and-training plan dropped in a Side Projects folder; start on phone, finish on laptop, hand to another agent tomorrow.
5. **Legal & contract work** — compare redlined V2 of a vendor MSA against V1, list changed clauses, flag liability/termination changes; everyone pulls the latest signed version.

Prereqs noted: free Box developer account, DigitalOcean (or any VPS), Slack workspace, Hermes Agent with a model provider, basic terminal familiarity. Author assumes prior experience setting up Hermes Agent Gateway on a VPS.

---

## Authors & Institutions

Chris Kim (@chriskim_dev), writing for Box Developers (@BoxPlatform). Integrates NousResearch Hermes Agent with Box. 45.6K views; published Jun 18, 2026.
