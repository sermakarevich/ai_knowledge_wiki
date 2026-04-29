# Build a More Secure, Always-On Local AI Agent with OpenClaw and NVIDIA NemoClaw

**Source:** [NVIDIA Developer Blog (Patrick Moorhead, Edward Li, Apr 17 2026)](https://developer.nvidia.com/blog/build-a-secure-always-on-local-ai-agent-with-nvidia-nemoclaw-and-openclaw/)

## Human Readable TL;DR

Think of this like setting up a personal AI assistant that lives entirely inside your own computer -- it can read your files, message you on Telegram, and run tasks for you, but it never phones home to any cloud service. NVIDIA packaged three tools (NemoClaw, OpenClaw, OpenShell) together so you can install this private assistant in about half an hour on a compatible machine. Before the assistant reaches out to the internet for anything, it has to ask you for permission, like a child asking before leaving the yard. The whole point is keeping your data on your desk instead of sending it to someone else's computer.

## TL;DR

NemoClaw is an open-source reference stack that bundles NVIDIA OpenShell (sandboxing runtime), OpenClaw (multi-channel agent framework), and the Nemotron 3 Super 120B model into a turnkey local agent deployment. All inference runs on-device via Ollama on a DGX Spark (GB10 GPU), with network/filesystem isolation and interactive policy approval preventing uncontrolled external access. It supports Telegram/Slack/Discord front-ends, persistent memory, and custom tools, targeting enterprise use cases where data cannot leave the device. Reported inference latency is 30--90 s per response for the 120B model; setup takes 20--30 minutes plus a ~87 GB model download.

---

## Problem & Motivation

Autonomous agents have outgrown simple Q&A -- they now execute code, call APIs, and drive multi-step workflows. Running these agents against third-party cloud inference creates two problems: sensitive data leaves the device, and the agent's tool-use surface is unbounded by default. Organizations handling regulated or confidential data need an agent stack that (a) runs entirely on-prem, (b) sandboxes tool invocations, and (c) exposes network/filesystem access through auditable, approvable policies rather than blanket trust.

---

## Main Original Ideas

1. **NemoClaw reference stack.** A single orchestrated bundle -- installer, lifecycle manager, and versioned blueprints -- that wires OpenShell + OpenClaw + Nemotron 3 Super together so operators don't assemble the pieces themselves.
2. **OpenShell network/filesystem isolation.** Sandbox boundaries restrict agents to whitelisted network endpoints and filesystem paths. By default the sandbox cannot even reach the host's Ollama on `localhost:11434` unless explicitly permitted.
3. **Interactive policy approval.** When the agent tries to hit an external endpoint, operators approve or deny in real time through the TUI/Web UI, without editing base policies or restarting the sandbox.
4. **Fully local inference path.** Nemotron 3 Super 120B is served via Ollama on local GPU (DGX Spark GB10); no runtime dependency on NVIDIA cloud services, preloaded into GPU memory to avoid cold starts.
5. **Messaging-first agent surface.** OpenClaw natively integrates Telegram/Slack/Discord plus persistent memory, turning the sandbox into an always-on assistant reachable from any messaging client rather than a one-off chat session.

---

## Key Findings

| Metric | Value |
|---|---|
| Model | NVIDIA Nemotron 3 Super 120B (120B params) |
| Model download size | ~87 GB |
| Inference latency (per response) | **30--90 seconds** (local, 120B) |
| Active setup time | 20--30 min |
| Full setup (incl. download) | 35--60 min depending on bandwidth |
| Hardware target | DGX Spark (GB10 GPU), Ubuntu 24.04 LTS |
| Docker | ≥28.x with NVIDIA container runtime |
| Web UI port | 18789 (tokenized auth) |

- No comparative benchmarks (vs. cloud agents or other sandboxing stacks) are reported -- claims are qualitative.
- Model preloading into GPU memory is called out as the reason subsequent interactions avoid cold-start cost.
- Default sandbox is network-isolated strongly enough that `OLLAMA_HOST=0.0.0.0` binding is required for the agent container to reach the host Ollama.

---

## Suggestions & Future Directions

1. **Prompt-injection caveat.** Authors explicitly state: "no sandbox offers complete protection against advanced prompt injection. Always deploy on isolated systems when testing new tools."
2. **Alternative inference backends.** Beyond Ollama, the stack supports NVIDIA NIM and vLLM for non-Spark hardware.
3. **Extensibility via CLI.** Custom tools and policies can be added through the `nemoclaw` CLI.
4. **Policy evolution.** Interactive approvals are expected to graduate into persistent endpoint allowlists as operators converge on stable policy sets.
5. **Multi-sandbox scaling.** Implied direction toward running concurrent sandboxes/agent instances on the same host.
6. **Community contribution** invited via the GitHub repo and Discord.

---

## Authors & Institutions

Patrick Moorhead (Technical Marketing Engineering, NVIDIA; Data Science student, Baylor University); Edward Li (Technical Marketing Engineer, NVIDIA Enterprise Computing; BS/MS CS -- Data Science, University of Pennsylvania).

---

## Key Resources

- GitHub: <https://github.com/NVIDIA/NemoClaw>
- Docs: <https://docs.nvidia.com/nemoclaw/>
- OpenShell docs: <https://docs.nvidia.com/openshell/latest/get-started>
- DGX Spark setup: <https://build.nvidia.com/spark/nemoclaw/instructions>
- Model card: <https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b>
- No-hardware starter: <https://build.nvidia.com/nemoclaw>
