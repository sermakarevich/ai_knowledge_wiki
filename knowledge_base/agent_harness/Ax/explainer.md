> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# google/ax — In Plain Language

## What is this about?

AX is a tool for running AI agents the way factories run assembly lines:
you describe what you want, and it runs thousands or millions of copies safely.

Think of it like Kubernetes, but instead of managing web servers,
it manages autonomous agent jobs. Each job runs in its own locked box
(a sandbox) with limited CPU, memory, and internet access.

You tell AX what to run using simple YAML files — the same style
Kubernetes uses. There are four building blocks:

- A **Task** says "run this agent job."
- A **Workspace** prepares the starting materials: Git code, tools, and skills.
- A **Gateway** is the internet firewall: which websites the agent may visit.
- A **Model** says which language model the platform should use.

A tiny example: you write one file that says "clone the Go repository"
and "make sure the Go toolchain builds," then run one command:

```bash
ax apply -f task.yaml
ax watch task test
ax ssh test -- ls -al /workspace
```

AX then starts the job, lets you watch it live, lets you log into
the sandbox to look around, and lets you pause and resume the job later.

## Why does it matter?

Running one AI agent on your laptop is easy. Running a billion of them
safely in production is a completely different problem.

Regular tools fall short in three ways:

1. **Agents are untrusted.** They run code they wrote themselves, browse
   files, and call external tools. Without strict isolation, one bad
   agent can damage everything else.
2. **Agents hold state.** Unlike a simple web request, an agent accumulates
   files, checkpoints, and conversation history. Pausing and resuming
   that state has to work reliably.
3. **Agents need guardrails.** Every agent can spend money (model calls),
   hammer networks, and touch secrets. Those limits must be declared
   up front, not bolted on afterward.

AX matters because it treats all of this as a first-class orchestration
problem. It borrows the proven Kubernetes pattern — declare what you want,
let a control plane make it true — and adapts it to agent workloads:
sandboxing, workspace setup, network fencing, and pause/resume checkpoints.

It is also built for extreme scale from day one: the stated goal is
billions of short-lived agent tasks per cluster, which ordinary
Kubernetes storage was never designed to handle.

## How does it work?

The workflow has five steps, from your laptop to a running sandbox.

**1. You declare what you want.**
You write YAML manifests and submit them with the `ax` command-line tool.
It looks and feels like `kubectl`: `apply`, `get`, `describe`, `watch`,
and `delete`, plus agent-specific verbs like `suspend`, `resume`, and `ssh`.

**2. A server accepts and stores your request.**
A program called `ax-server` receives your manifests over gRPC, checks
that they are valid, and saves them — not in Kubernetes etcd, but in
Redis. Redis acts as both the database (task records) and the work queue
(streams of events). This is a deliberate scale choice: millions of
short-lived tasks would overwhelm etcd storage and write limits.

**3. Workers reconcile reality with your request.**
One or more copies of `ax-controller` read jobs from the Redis queue
and provision real resources on Agent Substrate: a contained area
(atespace), an actor, a worker machine, and firewall rules. Add more
controller copies to handle more tasks — it scales horizontally.

**4. Your agent runs inside a locked sandbox.**
Every task container starts with `ax-task-runner`. It clones the Git
repos from your Workspace, serves metadata about the task to the agent,
and then runs the agent's command under CPU, memory, and network limits.
The default sandbox image is based on Python 3.12 with Git, SSH, and
agent bootstrap tooling preinstalled.

**5. You operate it like a fleet.**
You inspect jobs with `ax get` and `ax describe`, stream live status
with `ax watch`, shell into a debuggable sandbox with `ax ssh`,
and freeze a job with `ax suspend` / thaw it with `ax resume`.
The CLI follows your active Kubernetes context automatically, so
switching clusters with `kubectx` switches what `ax` sees too.

Deployment follows the same story: build container images with `ko`,
install Redis plus the control plane into the `ax-system` namespace,
and try the whole loop with the scripted `demo.sh` (apply, wait for
Ready, poke around over SSH, suspend).

## Where can this be used?

- **Mass code agents:** run thousands of parallel jobs that each clone a
  repo, build it, run tests, or attempt a fix — each in a clean sandbox.
- **Untrusted code execution:** safely run agent-written scripts with CPU,
  memory, and network fences instead of giving agents your laptop or server.
- **Reproducible research runs:** pre-wire datasets, repos, and tool servers
  into a Workspace so every experiment starts from the identical setup.
- **Long-running assistants you can pause:** checkpoint an idle agent with
  `suspend`, free the machine, and `resume` exactly where it left off.
- **Locked-down browsing agents:** give a web agent a Gateway allowlist so
  it can only reach the hosts you approved, nothing else.
- **Multi-cluster agent fleets:** operate staging and production agent
  clusters with the same CLI, switching context the way `kubectl` users do.

Note the warning from the project itself: concepts and file formats are
still changing, so expect breaking changes before any stable release.

## Conclusions & takeaways

- AX is "Kubernetes-style orchestration, but for AI agents": declare Tasks,
  Workspaces, Gateways, and Models in YAML, and a control plane runs them.
- Its headline bet is scale plus safety: Redis instead of etcd for
  billion-task throughput, and sandboxes plus firewall rules by default.
- The developer experience is deliberately familiar: if you know `kubectl`,
  you already know `ax apply`, `ax get`, `ax watch`, and `ax ssh`.
- Pause/resume and SSH inspection are core features, not afterthoughts —
  they reflect how agents really work: long-lived, stateful, debuggable.
- The project is early and explicitly unstable, so treat it as an
  architecture to learn from and experiment with, not a finished platform.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Task | One agent job to run: the command, its limits, and which workspaces it uses. |
| Workspace | A pre-packed starting kit: Git repos, tools, and skills cloned before the agent starts. |
| Gateway | The firewall rulebook: the list of internet hosts an agent is allowed to contact. |
| Model | A settings card saying which language model the platform uses and where its key lives. |
| Sandbox | A locked box the agent runs inside, with capped CPU, memory, and network. |
| Atespace | A named contained area where a group of tasks lives, like a folder for agents. |
| Control plane | The background machinery (server plus controllers) that turns your YAML into running jobs. |
| Redis / Redis Streams | A fast database plus a to-do queue the control plane uses instead of Kubernetes storage. |
| gRPC | A fast machine-to-machine calling system the CLI uses to talk to the server. |
| Suspend / resume | Freezing a running agent (saving its progress) and thawing it later where it stopped. |
