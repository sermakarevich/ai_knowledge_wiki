# Claude Code Auto Mode: A Safer Way to Skip Permissions

**Article:** [Claude Code auto mode: a safer way to skip permissions (John Hughes / Anthropic, 2026)](https://www.anthropic.com/engineering/claude-code-auto-mode)

## Human Readable TL;DR

When you use Claude Code, it normally asks "can I do this?" before every action -- like a contractor who checks with you before hammering each nail. Most people (93%) say "yes" every time, which means they stop actually reading the requests. Anthropic built a smart security guard that watches what Claude is about to do and only interrupts you when something looks genuinely risky -- like deleting important files or sharing private data. It's not perfect (it misses about 17% of borderline cases), but it's far safer than the old "just do whatever you want" mode, giving users a practical middle ground between constant interruptions and no guardrails at all.

## TL;DR

Anthropic introduces a two-layer defense system for Claude Code's autonomous operation. An input-layer prompt-injection probe scans tool outputs before they enter the agent context, while an output-layer transcript classifier (Sonnet 4.6) evaluates actions through a two-stage pipeline -- a fast single-token filter followed by chain-of-thought reasoning for flagged actions. On real traffic (n=10,000), the full pipeline achieves 0.4% false-positive rate and 17% false-negative rate on overeager behaviors, providing a practical middle ground between manual approval and `--dangerously-skip-permissions`.

---

## Problem & Motivation

Claude Code's default permission model requires user approval before executing commands or modifying files. In practice, users approve 93% of prompts, creating approval fatigue where they rubber-stamp requests without careful evaluation. Users face a binary choice: sandboxed operation (safe but high-friction) or `--dangerously-skip-permissions` (convenient but unsafe). Auto mode addresses this gap by introducing classifiers that automate safe decisions while catching genuinely dangerous actions.

---

## Main Original Ideas

1. **Two-Layer Defense Architecture** -- An input layer scans tool outputs for prompt injection before they enter the agent context, while an output layer evaluates the agent's proposed actions. This compounding means an attack must evade both detection and an independent safety judgment.

2. **Transcript Stripping for Classifier Integrity** -- The classifier sees only user messages and tool calls; assistant text and tool outputs are stripped. This prevents the agent from generating persuasive rationalizations to manipulate the classifier, and removes the primary injection vector (tool results).

3. **Two-Stage Classification Pipeline** -- Stage 1 is a fast single-token yes/no filter that errs toward caution (8.5% FPR). Stage 2 applies chain-of-thought reasoning only to flagged actions, reducing FPR to 0.4%. Identical inputs except the final instruction enable prompt caching for Stage 2.

4. **Three-Tier Permission Model** -- Tier 1: safe-tool allowlist (reads, searches, navigation). Tier 2: in-project file writes bypass the classifier (reviewable via version control). Tier 3: shell commands, web fetches, and external integrations go through the transcript classifier.

5. **Deny-and-Continue with Escalation** -- Blocked actions return as tool results with instructions to find safer alternatives. Three consecutive or 20 total denials trigger human escalation. Headless mode terminates the process instead. This makes false positives survivable rather than session-ending.

6. **Threat Taxonomy for Agent Behavior** -- Four categories: overeager behavior (unauthorized initiative), honest mistakes (scope misunderstanding), prompt injection (malicious instructions in external content), and model misalignment (independent goals -- not yet observed but actively evaluated).

---

## Key Findings

| Metric | Stage 1 Only | Full Pipeline (Stage 1 + 2) |
|--------|-------------|----------------------------|
| **FPR** (real traffic, n=10,000) | 8.5% | **0.4%** |
| **FNR** (real overeager, n=52) | 6.6% | 17% |
| **FNR** (synthetic exfil, n=1,000) | 1.8% | 5.7% |

- Users approve 93% of permission prompts in default mode, confirming the approval fatigue problem
- The 17% FNR on overeager actions represents cases where the classifier correctly identifies danger but misjudges whether user consent covers the specific action
- Stage 2 dramatically reduces false positives (8.5% to 0.4%) at the cost of some increase in false negatives
- Blanket code execution rules (shell access, wildcarded interpreters, package managers) are dropped when entering auto mode
- 20+ block rules grouped into four categories: destroy/exfiltrate, degrade security posture, cross trust boundaries, and bypass review/affect others
- Prompt engineering improvements for the 17% FNR haven't exceeded their implementation costs

---

## Suggestions & Future Directions

1. **Expanding the Overeagerness Dataset** -- The real overeager test set (n=52) is small; the team plans to grow it for more robust evaluation of the classifier's performance on edge cases.

2. **Iterating on Safety and Cost** -- Continued optimization of the two-stage pipeline to reduce both false negatives and computational overhead.

3. **Residual Risk Awareness** -- Users should exercise judgment about which tasks and environments run autonomously, as the system is not infallible -- it's a substantial improvement over unrestricted mode, not a replacement for careful manual review.

4. **User Feedback Loop** -- Users are encouraged to report when auto mode errs, feeding real-world data back into classifier improvement.

5. **Configurable Trust Boundaries** -- The environment slot (domains, cloud buckets, source-control orgs, internal services) defaults to trusting only the current git repository, with `claude auto-mode defaults` exposing the full configuration for customization.

---

## Authors & Institutions

John Hughes (Anthropic), with acknowledgments to Alex Isken, Alexander Glynn, Conner Phillippi, David Dworken, Emily To, Fabien Roger, Jake Eaton, Javier Rando, Shawn Moore, and Soyary Sunthorn (Anthropic)
