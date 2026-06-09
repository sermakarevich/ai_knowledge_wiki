# Every Agentic Engineering Hack I Know (June 2026)

**Paper:** [Every Agentic Engineering Hack I Know (June 2026) (Van Horn, 2026)](https://x.com/mvanhorn/status/2061877533885473181)

## Human Readable TL;DR

A veteran startup engineer shares 22 tricks for "agentic engineering" -- directing AI coding agents through written plans rather than typing code yourself. Think of it like being a film director: you describe what you want, the AI actors execute it, and you react and redirect. The author claims this workflow let him ship multiple popular open-source tools (tens of thousands of GitHub stars) after years of shipping nothing notable. The secret is making a plan file first, letting agents do the work in parallel, and using your judgment to steer rather than execute.

## TL;DR

A practitioner's guide to running multiple AI coding agents (Claude Code + OpenAI Codex) in parallel using the plan.md → /ce-plan → /ce-work workflow from the Compound Engineering plugin. Key operational hacks: bypass permission prompts, run 4-6 sessions simultaneously in cmux tabs, use voice input (Monologue/Wispr Flow), and maintain a personal knowledge base as agent memory. Supplementary tooling covers remote control, email-triggered sessions (AgentMail), pre-plan research (last30days), raw transcript injection (Granola), video generation (HyperFrames), and real-world errand automation (Printing Press + Agent Cookie).

---

## Problem & Motivation

Traditional software development requires heavy manual coding and cognitive overhead. Agentic engineering promises to flip the 80/20 coding-to-planning ratio by having AI agents handle execution while humans focus on planning and taste. The gap is knowing how to configure and operate the agent stack efficiently -- which tools, which settings, which workflows. This article closes that gap with 22 actionable hacks drawn from daily practice shipping real software.

---

## Main Original Ideas

1. **Plan-First Loop** -- Always start with `/ce-plan` before touching code. The plan.md becomes a checkpoint that survives context resets. Traditional dev is 80% coding, 20% planning; this flips it. Compound Engineering fans out parallel research agents (codebase, past solutions, external docs) before writing the plan.

2. **Don't Read the Plan** -- Plans are for agents, not humans. Skim the title, run `/ce-work`, ask inline questions ("eli5 this plan"). The plan enforces rigor on the agent, not on you. It is the leash that stops agents from cutting corners.

3. **Plan the Plan for Deep Work** -- For non-code knowledge work (strategy docs, competitive analysis, book synthesis), ask the agent to first produce a plan for how it will produce the deliverable. Then execute that plan. Forces deep research instead of lazy shortcuts; works with PDFs and meeting transcripts as input.

4. **Parallel cmux Sessions** -- Run 4-6 terminal tabs simultaneously: one planning, one building, one debugging, one on a bug. While `/ce-plan` spins up research in tab 1, run `/ce-work` on a ready plan in tab 2, paste a new bug in tab 3. Cycle asynchronously.

5. **YOLO Permission Mode** -- Bypass all Claude permission prompts: `skipDangerousModePermissionPrompt: true` and `defaultMode: bypassPermissions` in `~/.claude/settings.json`. Git is the safety net. Codex equivalent: `approval_policy = "never"` / `sandbox_mode = "danger-full-access"`.

6. **Claude Plans, Codex Builds** -- Use Claude Code for planning and taste; delegate heavy parallel builds to Codex (reasoning xhigh + fast mode on). Hand off via Codex IDE extension, `/ce-work --codex`, or Printing Press Codex mode. Claude fast mode skipped to avoid per-token billing on top of Max plan.

7. **Voice Input** -- Monologue or Wispr Flow on Mac; Apple built-in dictation on iOS. LLMs tolerate imperfect transcription, so mumbles and restarts still parse. A gooseneck mic recommended for desk use. Open-office voice remains an unsolved challenge.

8. **Default Terminal into Agent** -- Configure every new terminal tab to open directly into Claude Code (via `~/.local/bin/claude-launcher.sh`), not a shell. Zero-cost session start means you start more sessions. Works with both Ghostty and cmux.

9. **Remote Control + AgentMail** -- Enable `remoteControlAtStartup: true` to reach any session from the Claude mobile app. Give Claude an email address via AgentMail: emailing it from your phone opens a fresh Claude session on your Mac and starts working the subject/body as a task.

10. **Pre-Plan Research with last30days** -- Before `/ce-plan`, run `/last30days <topic>` to search Reddit, X, YouTube, HN, GitHub in parallel. The output grounds the plan in current community knowledge rather than stale training data. Key for library/tool selection decisions.

11. **Raw Transcript Injection** -- Drop full Granola meeting transcripts (unedited, including off-topic tangents) into `/ce-plan`. Let the agent extract signal and ignore noise against your codebase and prior strategy plans. Do not pre-summarize -- the LLM handles extraction better than you do.

12. **Personal Knowledge Base as Agent Memory** -- Point agents at Bear notes (Bear CLI), Obsidian vaults, or gbrain/supermemory. Every session compounds on a decade of decisions, strategies, and half-baked ideas. The more you put in, the smarter each session gets.

13. **Printing Press + Agent Cookie** -- A fleet of agent-native CLIs (Tesla, Instacart, Alaska Airlines, ESPN) authenticated via real browser sessions delivered by Agent Cookie. Agents run real-world errands while you do something else. Build your own with Printing Press for any API or service you live in.

14. **Write Reusable Skills** -- Any workflow done more than twice becomes a skill command. Point the agent at an existing working skill and say "make one like this for X." It reads the structure, scaffolds a new one. This is the author's primary open source contribution loop.

15. **HyperFrames for Video** -- Build launch reels as HTML (write `script.md` scene by scene, agent renders to MP4). Same plan→build loop as code; output is a video. Cost of a video drops to a conversation.

---

## Key Findings

- With this stack the author shipped last30days (27K+ stars), Printing Press (4K+ stars), Agent Cookie, and became a top OSS contributor to Python, Go, GStack, Paperclip, Compound Engineering, Vercel's agent-browser, and Camoufox -- after years of shipping nothing notable.
- M5 Max 64GB lasts as little as 1 hour on battery under 6 agent sessions + Codex; carry an Anker brick.
- Voice in open offices remains an unsolved personal challenge (author explicitly requests community input).
- Primary psychological risk: "AI psychosis" -- addiction to the build loop at the expense of shipping to real users or maintaining personal relationships.
- The rare valuable input in the agentic loop is human judgment (taste, direction, react-and-redirect), not typing.

---

## Suggestions & Future Directions

1. **Crack voice in open offices** -- author explicitly notes this as his weak spot and asks for community advice.
2. **Evaluate supermemory** -- author is currently investigating it as a cross-session agent memory layer; verdict pending.
3. **Build personal skills for any repeated workflow** -- the compounding value grows with every skill added.
4. **Contribute to open source projects you use daily** -- community relationships compound beyond the merged PRs.
5. **Avoid AI psychosis** -- validate that someone actually wants what you're building; take breaks; talk to loved ones.
6. **Unfreeze from IDE habits** -- no Zed, no IDE, no typing code; voice + plan + agent is the full workflow.

---

## Authors & Institutions

Matt Van Horn (@mvanhorn), independent engineer and founder; contributor to Compound Engineering (with @kieranklaassen and @trevin), Printing Press (@ppressdev, with @trevin), and numerous open source projects.
