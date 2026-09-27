# [Hypothesis] Cory House — personal Spec Kit + Claude Code run
- Source: https://x.com/housecor/status/1970666878797258990
- Status: fetched 2026-09-24
## Content
- Ran GitHub Spec Kit (spec-driven development toolkit) with Claude Code (Anthropic's agentic coding CLI) on a personal restaurant app.
- Task: greenfield admin feature; Spec Kit generated and executed a 32-task plan, checking tasks off as it progressed.
- Pipeline observed: feature branch creation, high-level plan, quickstart doc, research docs on decisions/alternatives, detailed spec, task list, failing-first tests (Test-Driven Development, TDD), implementation, then lint/build/test validation with self-fixes.
- Worked: thorough, organized, highly opinionated flow; self-corrected minor mistakes during final validation; Large Language Model (LLM) portable (works with many models, not Claude-only).
- Friction 1: generates a large number of files — feels excessive, opposite of casual vibe coding.
- Friction 2: heavy token use from verbose, detailed, specific artifacts.
- Friction 3: mid-flow mind changes are costly — many files to update, unclear revision path.
- Friction 4: review burden replaces authoring burden — easy to rubber-stamp specs and code without real review.
- Friction 5: despite full pipeline, the feature did not work quite right; open question whether to fix specs or patch code directly with Claude's help.
## Why it was kept
- Real hands-on run, but n=1 on a personal codebase — practitioner datapoint, not team evidence.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
