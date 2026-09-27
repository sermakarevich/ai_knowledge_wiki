> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The system lived in my head

**In one sentence:** After models got good enough, the author stopped writing code by hand in February and scaled from one agent to ~20 parallel VMs managed by botd — which made shipping easy but made deciding what was worth shipping the hard part.

## Key points

- Before AI, the author's superpower was a hard-earned mental model of the whole system, especially interfaces between components, unwritten assumptions, and which line of code mattered — maintained by constantly reading others' changes.
- Hand-writing was the bottleneck: typing speed plus the fact that even small features spanned handlers, schema, tests, and docs with unequal blast radius (a bad handler reverts cleanly, a bad migration leaves a mess).
- The February rule — no code by hand for six months, broken once for three minutes — forced reps with agents: when an agent got stuck, fix what it was missing (prompts, tools, environment) instead of finishing the code.
- The trigger was Claude Code plus a step-change in models (GPT-5.3 and Opus 4.6 handling larger changes with less steering); earlier Copilot autocomplete and Cursor tab-complete only helped with first drafts.
- Parallelism grew accidentally from idle time between agent tasks (one agent became a dozen): sharing one dev box caused file/Git collisions, dependency/port/process fights, and waiting on the longest-running agent.
- Isolation evolved worktrees (fixed only Git) → AGENTS.md patches (random ports, ephemeral databases, burned context avoiding collisions) → containers (separate ports/processes/state but leaky boundary, laptop must stay awake) → one exe.dev Linux VM per task (SSH/HTTPS in seconds, work survives closing the laptop).
- Botd (three rules: off-laptop, mobile-first, preserve every conversation) provisioned/deprovisioned boxes, showed working/stuck/waiting status, and enabled phone/laptop inspection, follow-ups, and diff review; agents ran YOLO mode inside disposable VMs with credentials proxied (never in-VM) and write access limited to test environments.
- Validation at scale (~20 VMs peak, some abandoned for weeks) relied on agents running tests, full CI, browser-driven screenshots, and multi-agent code review — but the agent graded its own work, the author still had to load each full diff into his head, and good-looking passing changes were thrown away because tools can't say whether complexity is worth adding (Hyrum's Law makes unshipping harder than shipping).

---

## The system lived in my head

In 2024 the author's advantage was knowing the entire system and its interfaces: pointing others at the exact line to change, remembering why strange decisions existed, and carrying unwritten assumptions. That let him build fast and safely, at the cost of reading every change to keep the model current and of typing multi-layer edits (handlers, schema, tests, docs) with asymmetric risk.

Early tooling progression from the chunk:

| Tool | What it did |
|---|---|
| Copilot autocomplete | Doc comment became a first draft — often wrong, but better than a blank file |
| Cursor tab-complete | Helped more; models visibly improving fast |
| Claude Code | Describe the change once, agent edits many files at once |
| GPT-5.3 and Opus 4.6 (early this year) | Suddenly handled larger changes with much less steering; results good enough to build on |

Key mechanism after Claude Code: the author typed less but read every generated change against the desired state in his head, working incrementally and hand-editing output because agents were "still wrong quite a lot" and he remained responsible for every merged line. The February rule's logic is stated as a parallel to learning to code:

> "I didn't get good at coding by reading about coding. I got good by writing a lot of code, running it, seeing it fail, fixing it, and doing it again."

> "AI agents are just software, after all. I wasn't going to understand them by reading prompt guides. I had to use them for real work, see where they failed, change the prompts, tools, or environment, and try again."

Verbatim on the single lapse: *"I broke it once, for three minutes. I opened the code and wrote a few lines, and it felt great. I had missed this. Right up until I realized how much I still had to type. I noped out."*

## One agent became a dozen

Idle time while an agent worked led to spinning up more agents ("I have ADHD. I got distracted"), producing the equivalent of colleagues sharing one dev box without talking to each other: same-file/Git edits, dependency installs, port fights, stray processes, and coordination over testing/pushing/deploying — plus a new wait on the slowest agent.

| Isolation attempt | What it fixed | What still broke |
|---|---|---|
| Single shared box | Nothing (baseline) | File/Git collisions, ports, processes, deploy coordination |
| Worktrees (own checkout + branch each) | Source collisions mostly gone | Shared databases, ports, processes, rest of machine |
| AGENTS.md patches (random port, ephemeral DB, don't touch others' processes) | Some conflicts avoided | Every conflict became another instruction; agents burned context avoiding each other |
| Containers | Separate ports, processes, local state | Leaky boundary (whatever the laptop could reach, the container could potentially reach); still approving commands; laptop had to stay awake |

## I closed my laptop. The work kept going.

After joining exe.dev (Linux VMs up in seconds with SSH/HTTPS), each task got its own machine so work survived closing the laptop. The new problem was reliably bringing up full dev environments, so the author had Claude write a startup script (toolchains, repo clones, Claude Code/Codex config) via a validation loop: fresh box → run script → fix → retry.

The dozen tmux sessions / terminal windows for a dozen agents then became the bottleneck (finding who finished, who was stuck, who needed input), so he built botd with three rules:

1. Run somewhere other than the laptop (agents keep working when it's closed).
2. Mobile first-class (no terminal required).
3. Preserve every conversation (look back across agents at where they got stuck, which instructions worked, which problems repeated).

Botd provisioned/deprovisioned boxes, drove agents, tracked tasks, and exposed status plus conversation inspection, follow-up instructions, and diff review from phone or laptop.

Safety model:

- YOLO mode (bash, installs, services, any local change) was acceptable because each agent sat in an isolated, disposable VM — "A trashed environment cost me nothing but the VM" — and because approving every tool call would make the author the queue again.
- External access was the real risk (agents read untrusted content and can be prompt-injected; whatever the agent can reach, an injected agent can leak or corrupt), so each integration faced: *"what's the worst that can happen through this?"* Reads mostly passed with read-only access; writes were limited to test environments where the worst case was corrupted test data.
- Credentials never lived in the VM: the agent's request goes through a proxy that adds the secret, and the agent sees only the response.

## Everything passed. I still didn't want it.

At peak ~20 VMs ran at once (not all active; some tasks sat untouched for weeks then were abandoned as cognitively too costly and never urgent/important enough). Manual validation didn't scale, so agents ran tests, triggered full CI, started the app, drove it in a browser, and sent screenshots — but the agent was grading its own work and could build and test the wrong thing confidently. Opening the live running environment to drive the UI end-to-end mattered as an independent check.

Review bottleneck: hand-written code was understood by review time, but agent diffs arrived whole and unfamiliar, queuing up when several agents finished together. Peer-agent reviews "worked surprisingly well," occasionally catching real bugs and cheap enough to run several times — but the author still had to understand each change before merging because he was responsible for it.

Even with green tests, good screenshots, good schema, and agent approvals, changes were discarded for product reasons: nobody needed it, it duplicated an existing path, or a small convenience added years of complexity. Verbatim:

> "The tools could tell me that the change worked. They couldn't tell me whether it was worth adding to the system."

> "Unshipping something is so much harder than shipping it. Hyrum's Law kicks in: once enough people use a system, someone depends on every observable behavior, even behavior you never intended to be a contract."

Closing claim: *"Shipping got easy. Deciding what to ship got important."*

**Covers:** chunk sections "The system lived in my head" through "Everything passed. I still didn't want it" (pre-agent workflow → February no-code rule → one agent to a dozen → worktrees/containers/VMs → botd/YOLO/security → validation/review/worth-shipping)
