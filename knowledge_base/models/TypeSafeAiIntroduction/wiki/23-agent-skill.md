> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Agent Skill

**In one sentence:** The TypeSafe agent skill is a drop-in package for Claude Code, Codex, and other agent environments that gives a coding agent full TypeSafe API context — question types, patterns, best practices — installed via plugin, skills CLI, or a pasted prompt, and driven by naming the skill in prompts.

## Key points

- The skill gives an AI coding agent full context on the TypeSafe API: the three question types, the architectural patterns, and best practices for structuring evaluations.
- Three installation paths are documented: the Claude Code plugin (two terminal commands), the skills CLI for other agents (`npx skills add typesafe-ai/skills --skill typesafe-ai`, project-local by default, `-g` for global), and pasting an install prompt into the agent that reads SKILL.md from GitHub.
- Manual installation means copying the entire skills/typesafe-ai directory, including reference files, into the agent's skills directory; only one installation method should be used to avoid duplicate copies.
- Updates run through the same channel: plugin marketplace/plugin update commands plus `/reload-plugins` or auto-update for Claude Code, `npx skills update` for skills.sh installs, or replacing the whole directory for manual copies.
- Three example prompts are given — brainstorming where TypeSafe fits ("explore the project and find opportunities for using intelligent judgement to stand in for complex parsing"), running cheap API experiments with an exported `TYPESAFE_API_KEY`, and checking applicable cookbooks — where naming the skill ("use the TypeSafe skill") works in any agent and the Claude Code plugin also accepts `/typesafe:typesafe-ai`.
- Four good-vibe-coding principles apply: talk it out from the example prompts, review the plan before implementing, keep questions and thresholds as constants in a single reviewable place (agents write poor questions, so edit collaboratively), and don't take assertions at face value — have the agent validate assumptions.
- Five common issues are diagnosed: agent not using the skill (invoke `/typesafe:typesafe-ai` or "use the TypeSafe skill", confirm installer target, restart), routing surprises (check questions and thresholds for false negatives/positives or vague questions), overusing confidence thresholds (highest confidence wins when only the best option matters; probabilities when a statistical algorithm is in mind), review difficulty (questions plus thresholds in one file), and invented request/response fields (stale skill — update and retry).

---

## Installation

Claude Code — run in the terminal:

```bash
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

Other agents:

```bash
npx skills add typesafe-ai/skills --skill typesafe-ai
```

Choose the agent when prompted. Project-local by default; add `-g` for global. Alternatively paste the documented install prompt into the agent (it runs the right installer and reads SKILL.md from GitHub), or copy the whole `skills/typesafe-ai` directory manually. Use one installation method only.

### Updates

```bash
claude plugin marketplace update typesafe-ai
claude plugin update typesafe@typesafe-ai
```

Restart Claude Code or run `/reload-plugins` to load the update; `/plugin` → Marketplaces → typesafe-ai → Enable auto-update turns on automatic updates. Skills.sh installs update with `npx skills update`; manual copies update by replacing the entire skill directory with the latest GitHub version.

## Example prompts

Naming the skill in the prompt — "use the TypeSafe skill" — works in any agent (Claude Code plugin: `/typesafe:typesafe-ai` directly):

1. Brainstorming: "Using the TypeSafe skill, explore the project and find opportunities for using intelligent judgement to stand in for complex parsing or other fragile code."
2. Experiments: create an API key, export it as `TYPESAFE_API_KEY`, and have the agent "run some experiments … Propose changes based on the most promising results."
3. Cookbooks: point at a specific cookbook or the cookbooks index and ask whether any patterns match the project ("analyze my code and see if there are any applicable cookbooks … that show how I could refactor my code to be less fragile or complex").

## Good vibe coding principles

1. Talk it out with the agent from the example prompts.
2. Review the plan and ensure it makes sense before implementing it.
3. Put the constants (questions and thresholds) in a single place so they're easy to review — agents aren't great at writing questions, so expect collaborative editing.
4. Don't take assertions at face value; encourage the agent to validate its assumptions.

## Common issues

- **The agent isn't using the skill:** invoke `/typesafe:typesafe-ai` (Claude Code) or ask to "use the TypeSafe skill"; confirm the installer targeted the agent in use, then restart it.
- **Routing isn't working like you expect:** check questions and thresholds — thresholds too high cause false negatives, too low cause false positives — and make questions more specific.
- **You're using confidence thresholds everywhere:** choosing the best option only needs the highest-confidence option, not a threshold; a specific statistical algorithm probably wants probabilities instead of confidence.
- **It's difficult to review TypeSafe code:** questions and threshold constants belong in a single code file, easy to find without spelunking.
- **The agent invents request or response fields:** the skill is stale — update via the installation method above and retry.

**Covers:** https://docs.typesafe.ai/agent-skill
