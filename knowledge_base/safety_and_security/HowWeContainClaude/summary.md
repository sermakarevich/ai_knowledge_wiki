# How We Contain Claude Across Products

**Paper:** [How We Contain Claude Across Products (McGuinness, Grace, De Jonghe, Eaton, Ribbink -- 2026)](https://www.anthropic.com/engineering/how-we-contain-claude)

## Human Readable TL;DR

Imagine giving a very capable but unpredictable assistant access to your entire computer. You'd want a series of safety cages: the assistant's work area is sealed off, the doors have locks, and a guard watches what comes in and out. This article describes exactly how Anthropic built those cages for three different Claude products -- a web chat tool, a developer coding assistant, and a workplace productivity tool -- and what broke along the way.

## TL;DR

Anthropic describes a three-layer containment architecture (environment, model, external-content controls) applied across claude.ai, Claude Code, and Claude Cowork. Each product uses isolation primitives matched to its risk profile: ephemeral gVisor containers, OS-level sandbox (Seatbelt/bubblewrap), and full VMs respectively. Two critical incidents -- a prompt-injection phishing bypass and credential exfiltration through approved endpoints -- showed that custom components fail more often than battle-tested primitives, and that environmental controls consistently outperform model-layer behavioral classifiers.

---

## Problem & Motivation

As AI agents gain access to filesystems, shells, and APIs, the blast radius of both misuse and accidental harm grows substantially. Three distinct threat vectors emerge: users directing harmful actions (intentionally or carelessly), model misbehavior (unintended actions from agentic systems), and external attackers exploiting tool and network access. No single defense layer is sufficient; products require containment strategies calibrated to user expertise, capability scope, and trust model.

---

## Main Original Ideas

1. **Three-layer containment model** -- Environment-layer controls (sandboxes, VMs, egress filters) form the primary defense; model-layer controls (system prompts, classifiers, training) supplement but cannot substitute. External-content controls limit what tools and connectors can do.

2. **Approval fatigue as a measurable failure mode** -- Claude Code users approved ~93% of permission prompts, with experienced users auto-approving twice as frequently as novices. This quantifies how human-in-the-loop oversight degrades with familiarity, motivating OS-level sandbox to cut prompt frequency by 84%.

3. **Ephemeral-container pattern (claude.ai)** -- Code execution in gVisor containers on isolated server infrastructure. Short-lived filesystem scope limits blast radius while accepting a narrow capability envelope.

4. **Local-OS sandbox pattern (Claude Code)** -- Seatbelt (macOS) and bubblewrap (Linux) applied to a developer-machine agent with full shell and filesystem access. Configuration files executing before trust prompts appeared was an identified gap.

5. **Full-VM pattern with external agent loop (Claude Cowork)** -- Non-technical users get a VM with selective workspace mounting. The agent loop was moved outside the VM for reliability, keeping the security boundary intact while avoiding in-VM stability issues.

6. **MitM proxy for credential exfiltration defense** -- After discovering credentials embedded in workspace files could be exfiltrated via approved api.anthropic.com endpoints, Anthropic deployed an in-VM man-in-the-middle proxy to validate credentials before any outbound call.

---

## Key Findings

| Scenario | Outcome |
|---|---|
| Claude Code permission prompts before sandbox | Users approved ~93% of requests |
| OS-level sandbox introduction | Permission prompts reduced ~84% |
| Prompt injection phishing test | Succeeded 24 of 25 attempts |
| Custom proxy incidents | Both major incidents traced to custom components, not standard isolation primitives |

- Environmental controls outperform model-layer defenses when exfiltration occurs through legitimate, approved channels -- classifiers have no signal to act on.
- Experienced users interrupt execution more often than novices even while auto-approving more, creating an inconsistent oversight model.
- Both critical incidents (phishing bypass, credential exfiltration) involved Anthropic-built custom components rather than standard hypervisors, syscall filters, or container runtimes.

---

## Suggestions & Future Directions

1. **Persistent memory poisoning** -- Agent context surviving across sessions creates new injection-persistence vectors that current per-session isolation doesn't address.
2. **Multi-agent trust escalation** -- Structured outputs from sub-agents may receive unwarranted credibility; trust hierarchies for agent-to-agent communication need formal treatment.
3. **Agent identity standardization** -- Open question whether agents should have independent principals vs. operating purely as extensions of user permissions.
4. **Prefer established primitives** -- Battle-tested hypervisors, syscall filters, and container runtimes have survived more adversarial attention than anything custom-built; avoid reinventing them.
5. **Match isolation to oversight capacity** -- Containment strength should track user expertise and how reliably they exercise active oversight (vs. passive approval).

---

## Authors & Institutions

Max McGuinness, Mikaela Grace, Jiri De Jonghe, Jake Eaton, Abel Ribbink -- Anthropic (2026)
