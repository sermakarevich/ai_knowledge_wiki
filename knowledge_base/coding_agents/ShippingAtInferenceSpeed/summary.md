# Shipping at Inference-Speed

**Source:** [Shipping at Inference-Speed (Peter Steinberger, Dec 2025)](https://steipete.me/posts/2025/shipping-at-inference-speed)

## Human Readable TL;DR

Imagine if you had a brilliant intern who could write code almost as fast as you could describe what you want. That's what AI coding tools have become in 2025. The author, a seasoned software developer, explains that he can now build software so fast that the main thing slowing him down is the time it takes the AI to think through his requests -- not the actual typing or coding. The hard parts left for humans are deciding what to build and how to structure it, not the building itself.

## TL;DR

Peter Steinberger documents a fundamental shift in software development productivity in late 2025: AI coding models (primarily GPT-5.2 Codex and Claude Opus) have made implementation near-trivial, moving bottlenecks entirely to architectural decisions, dependency selection, and system design. He describes a workflow of 3-8 concurrent projects, documentation-first conventions, linear commits to main, and visual prompting -- all optimized for agent efficiency rather than human navigation. The core insight is that most software is data transformation and presentation, and AI can now handle that automatically.

---

## Problem & Motivation

The author tracks a personal inflection point: the transition from AI-assisted coding (where working output was a pleasant surprise) to AI-driven coding (where working output is the baseline expectation). The motivation is capturing and systematizing the workflow practices, model preferences, and infrastructure choices that enable "factory-like" building at inference speed.

---

## Main Original Ideas

1. **Inference time as the new bottleneck** -- The limiting factor in software output is no longer typing, debugging, or implementation; it's the time models take to respond and the developer's own architectural thinking. Everything else has been automated away.

2. **Concurrent project queuing** -- Running 3-8 projects simultaneously with one primary focus. Instead of complex multi-agent orchestration, features are queued and tackled iteratively. This maximizes utilization of inference time across projects.

3. **Documentation-first development** -- Each project maintains a `docs/` folder that models read before acting. Well-structured docs act as persistent context, reducing prompt length and improving consistency across long sessions.

4. **Agent-optimized codebases** -- Code and project structure should be designed for agent navigation (clear naming, flat hierarchies, explicit conventions) rather than human aesthetics. Agents work faster with already-loaded file context.

5. **Visual prompting** -- Showing the model a screenshot of what's wrong often replaces paragraphs of text. Prompts have shortened dramatically as visual communication proves more efficient for UI iteration.

6. **Model specialization** -- GPT-5.2 Codex excels at large-scale refactors (reads extensively before writing, handles big context); Claude Opus excels at smaller edits, general automation, and personality-driven applications with a "delightful" quality.

7. **Linear commits to main** -- Feature branches add friction without benefit in solo/small-team AI-assisted development. Committing linearly to main with frequent, small commits keeps context clean for agents.

---

## Key Findings

| Tool / Practice | Best For | Weakness |
|---|---|---|
| GPT-5.2 Codex (`high` mode) | Large refactors, big codebases | Less personality, no system events for file changes |
| Claude Opus | Small edits, automation, personality tasks | Less capable on massive context refactors |
| `high` vs `xhigh` effort | `high` is faster with minimal quality trade-off | `xhigh` rarely worth the latency |
| Git sync (not worktrees) | Dual-machine workflow | Adds sync overhead |
| Local daemon architecture | Chrome extension dev, background tasks | More complex setup |

**Configuration that works:**
```toml
model = "gpt-5.2-codex"
model_reasoning_effort = "high"
tool_output_token_limit = 25000
model_auto_compact_token_limit = 233000
```

- Default token limits are too restrictive -- increasing them significantly improves results.
- Web search enabled, unified execution mode, shell snapshots, and skills support are all on.

**Notable projects built at this speed:**
- *Clawdis* -- AI assistant with screen control, messaging, home automation, voice
- *VibeTunnel* -- Terminal multiplexer rewritten from TypeScript to Zig in a single prompt session
- *Summarize* -- YouTube/video summarization CLI with local processing
- *Oracle* -- Custom GPT-5 Pro research CLI (now mostly superseded by 5.2)

---

## Suggestions & Future Directions

1. Start with model + CLI before expanding to UIs -- CLIs are faster to iterate on and easier for agents to test.
2. Invest in project-level documentation early; it pays compounding returns as context grows.
3. Design codebases for agent navigation: flat structures, explicit naming, minimal magic.
4. Reserve human judgment for dependency selection and data-flow architecture -- these remain genuinely hard.
5. Cross-reference patterns across projects to build a personal library agents can reuse.
6. Monitor AI company competition -- the author expects continued rapid model improvement and maintains multi-model workflows as insurance.

---

## Author & Source

**Peter Steinberger** -- iOS/macOS developer, founder of PSPDFKit (now Nutrient). Blog: steipete.me
