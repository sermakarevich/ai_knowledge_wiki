# Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems

**Paper:** [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems (Liu, Zhao, Shang, Shen, 2026)](https://arxiv.org/abs/2604.14228)

## Human Readable TL;DR

Imagine a self-driving taxi. Everyone assumes the "smart" part is the AI driver, but when you look under the hood, only about 2% of the car is the AI brain -- the rest is seatbelts, brakes, emergency stop buttons, a locked steering wheel when kids climb in the backseat, a dashboard that only shows the driver what's relevant right now, and a dispatch system that forgets old rides so the memory stays fresh. This paper tears apart Claude Code (the actual shipping software engineers use) to show that the AI is a small passenger in a huge, carefully engineered vehicle, and that all the boring-sounding safety rails, memory hygiene, and permission gates are where the real design work lives. The authors argue that as AI models become equally smart, the winners will be the teams who build the better vehicle around them -- not the teams with the smartest passenger.

## TL;DR

The paper provides a source-grounded architectural analysis of Claude Code v2.1.88 (~1,900 TypeScript files, ~512K LOC), mapping five human values through thirteen design principles to concrete implementation choices. Its headline finding is that only ~1.6% of the codebase is AI decision logic; the remaining 98.4% is deterministic infrastructure for permissions, context management, tool routing, and recovery. The work introduces a 7-component / 5-layer subsystem model, analyzes the deny-first permission pipeline and its seven modes, documents a five-stage context compaction pipeline, and contrasts Claude Code against OpenClaw to expose how deployment context reshapes the same six recurring design questions. A secondary contribution is introducing long-term human-capability preservation as a sixth evaluative lens -- surfacing a "sustainability gap" the authors treat as the most consequential open problem for production agent systems.

---

## Problem & Motivation

Anthropic ships user-facing documentation for Claude Code but no detailed architectural description of the system itself. Despite rapid adoption of agentic coding tools, recurring design questions -- safety posture, context management, extensibility, delegation -- have not been systematically analyzed at the source-code level of any production agent. Prior literature describes ideas for agent frameworks; this paper examines what a shipped, widely used agent actually does and why.

The broader motivation: as frontier models converge in raw coding capability, the operational harness around them becomes the principal differentiator. Understanding that harness -- its costs, its trade-offs, and the values it encodes -- is essential for anyone building or evaluating production agent systems.

---

## Main Original Ideas

1. **Five-value / thirteen-principle framework.** The paper identifies five human values driving Claude Code's architecture (Human Decision Authority, Safety/Security, Reliable Execution, Capability Amplification, Contextual Adaptability) and traces each through 13 named design principles (deny-first, graduated trust, defense-in-depth, graduated context cost, etc.) down to specific TypeScript files. This is the first such systematic value-to-code mapping for a production coding agent.

2. **7-component / 5-layer subsystem model.** A source-grounded decomposition consisting of seven high-level components (user, interfaces, agent loop, permission system, tools, state/persistence, execution environment) arranged across five subsystem layers (surface, core, safety/action, state, backend). Every component is traced to concrete files, making the model verifiable rather than aspirational.

3. **The 1.6% / 98.4% ratio.** Quantifies that only ~1.6% of the codebase is AI decision logic while 98.4% is deterministic operational infrastructure. This challenges the common framing of agents as "LLM + thin scaffolding" and reframes agent engineering as harness engineering.

4. **Permission system anatomy.** Full documentation of the deny-first permission pipeline with seven modes, a two-stage ML auto-mode classifier (fast filter + chain-of-thought), seven independent safety layers that must all pass, and a detailed adversarial analysis including disclosed CVEs (CVE-2025-59536, CVE-2026-21852) exposing pre-trust initialization vulnerabilities.

5. **Four-mechanism extensibility ordered by context cost.** Argues that Claude Code's four extension surfaces -- hooks (zero context cost), skills (low), plugins (medium), MCP servers (high) -- are deliberately arranged along a cost gradient. Graduated context cost is framed as a first-class architectural principle, not incidental.

6. **Five-layer context compaction pipeline.** Documents five sequential strategies (budget reduction → snip → microcompact → context collapse → auto-compact) applied before every model call, each at a different cost-benefit tradeoff. Notable finding: in a January 2026 fleet experiment, the non-cache-reuse compaction path had a ~98% cache-miss rate, costing ~0.76% of fleet `cache_creation` tokens.

7. **Six-dimension contrast with OpenClaw.** A structured comparison (scope, trust model, runtime, extensibility, memory, multi-agent routing) showing that the same recurring design questions produce opposite answers when deployment context shifts from a CLI coding tool to a multi-channel persistent gateway -- making the design space itself visible.

8. **Long-term human capability as a sixth evaluative lens.** Introduces capability preservation as a cross-cutting concern absent from Anthropic's stated design values, supports it with independent empirical evidence (EEG studies, comprehension deltas, hiring data), and uses it to surface a "sustainability gap" in the architecture.

---

## Key Findings

### Architectural composition (Claude Code v2.1.88)

| Quantity | Value |
| --- | --- |
| Total codebase | ~1,900 TypeScript files / ~512K LOC |
| **AI decision logic share** | **~1.6%** |
| **Deterministic infrastructure share** | **~98.4%** |
| Built-in tools | up to 54 (19 unconditional, 35 feature-gated) |
| Hook event types | 27 (5 safety, 22 lifecycle/orchestration) |
| Permission modes | 7 (plan, default, acceptEdits, auto, dontAsk, bypassPermissions, internal "bubble") |
| Tool subdirectories in `src/tools/` | 42 |
| Context window | 200K tokens (older models) / 1M tokens (Claude 4.6 series) |
| Compaction pipeline depth | 5 sequential layers |

### Empirical findings on permission and safety behavior

- Users approve **~93%** of permission prompts (approval fatigue, Hughes 2026).
- Auto-approve rates climb from ~20% at <50 sessions to **>40%** by 750 sessions (McCain et al., 2026).
- Sandboxing reduced permission prompt frequency by **~84%** (Dworken & Weller-Davies, 2025).
- Commands with **>50 subcommands** fall back to a single generic approval -- a documented defense-in-depth failure (Adversa.ai, 2026).

### Human side-effects of agentic coding (external studies synthesized)

- **+27%** of Claude Code-assisted tasks were work "that would not have been attempted without the tool" (Huang et al., 2025, N=132 Anthropic engineers/researchers).
- Developers using AI tools were **19% slower** in an RCT while perceiving a 20% speedup (Becker et al., 2025).
- Cursor adoption caused **+40.7%** code complexity increase (p<0.001); velocity +281% in month one, back to baseline by month three (He et al., 2025, N=807 repos).
- **~25%** of AI-introduced issues persist to latest revision across 304K AI-authored commits; security issues persist at substantially higher rates (Liu et al., 2026).
- AI-assisted developers scored **17% lower** on comprehension tests; EEG connectivity weakened and persisted after AI removal (Shen & Tamkin 2026; Kosmyna et al., 2025).
- Only **13.3%** of indexed agentic systems publish agent-specific safety cards (MIT AI Agent Index, 2026).

### Qualitative architectural insights

- Extensibility mechanisms are strictly ordered by context cost -- a design axis most agent frameworks leave implicit.
- Session persistence is append-only JSONL with resume/fork/rewind, but permission state is **not restored** on resume -- a deliberate safety/usability trade.
- The `queryLoop()` / `StreamingToolExecutor` pairing implements ReAct with explicit error-recovery paths rather than relying on the model to self-correct.
- Subagent delegation uses sidechain transcripts with scoped permissions, keeping parent context clean -- the graduated-trust principle applied at the orchestration layer.

---

## Suggestions & Future Directions

1. **Close the observability-evaluation gap.** ~78% of AI failures are estimated to be silent; observability is adopted by ~89% of teams but offline evaluation by only 52.4%. Open question: should evaluation scaffolding (generator-evaluator separation, sprint contracts, post-hoc checks) live inside the harness as new hook events, or outside as a separate layer?

2. **Design a durable cross-session memory layer.** A gap exists between static `CLAUDE.md` and ephemeral JSONL transcripts. Candidates proposed: paged memory (LLM-as-OS framing), production memory stores, self-reflection traces, and verbal RL across attempts.

3. **Evolve the harness boundary along four axes:** *where* (virtualized session/harness/sandbox as swappable interfaces), *when* (proactive tick-based architectures), *what* (VLA models extending tool use to physical actions), and *with whom* (role-differentiated multi-agent coordination beyond parent/subagent hierarchies).

4. **Scale the work horizon from sessions to scientific programs.** Current turn/session/subagent primitives are untested for work spanning weeks. METR's 50%-time-horizon metric is suggested as an empirical frame; progress likely requires both cross-session memory and new coordination primitives.

5. **Prepare for external governance.** EU AI Act full applicability (August 2026), the GPAI Code of Practice, and emerging copyright jurisprudence (Bartz v. Anthropic) will require externally auditable logging and transparency interfaces. Current session transcripts are internally auditable but not in forms regulators contemplate.

6. **Treat long-term human capability as a first-class design requirement.** Proposed directions: comprehension-preserving surfaces, session-level cognitive-offloading probes, and mechanism analogues to generator-evaluator separation applied to the *human* learning loop -- not just the agent's output loop.

---

## Authors & Institutions

Jiacheng Liu (VILA Lab, Mohamed bin Zayed University of Artificial Intelligence -- MBZUAI); Xiaohan Zhao (VILA Lab, MBZUAI); Xinyi Shang (VILA Lab, MBZUAI & University College London); Zhiqiang Shen (VILA Lab, MBZUAI -- corresponding author).
