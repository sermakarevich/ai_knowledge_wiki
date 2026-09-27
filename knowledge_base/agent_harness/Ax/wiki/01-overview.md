> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** AX is a declarative, Kubernetes-like orchestrator for running sandboxed autonomous agent workloads at scale.
## Key points
- Declares agentic tasks via `Workspace` and gateway specifications, then sandboxes execution, wires workspaces, fences networking, and scales runs (README.md:17).
- Targets high-throughput orchestration of billions of autonomous agent tasks per cluster on top of Agent Substrate for sandboxed execution (README.md:19).
- Uses four declarative primitives — `Task`, `Workspace`, `Gateway`, `Model` — plus `ax suspend`/`resume` and `ax ssh` for lifecycle and inspection (README.md:57).
- Expresses everything as `ax.io/v1alpha1` manifests applied with a single command (README.md:68).
- Deploys its control plane (plus Redis) into the `ax-system` Kubernetes namespace via `make deploy` with `ko` and a container registry (README.md:90).
- Exposes a `kubectl`-shaped `ax` CLI over gRPC with `apply`, `get`, `describe`, `watch`, `delete` plus agent-specific verbs (README.md:130).
- Follows the active Kubernetes context (including `kubectx`) and tunnels to that cluster's control plane in the background (README.md:198).
---
## Purpose and positioning
AX runs untrusted agent code as neither stateless microservices nor run-to-completion batch jobs, handling accumulated state, strict isolation, model/tool-server calls, and cost guardrails declaratively (README.md:57).

```yaml
# task.yaml
apiVersion: ax.io/v1alpha1
kind: Workspace
metadata:
  name: golang
spec:
  git:
    - repo: https://github.com/golang/go.git
      branch: "my-fix"
---
apiVersion: ax.io/v1alpha1
kind: Task
metadata:
  name: test
spec:
  workspaces:
    - name: golang
      goal: "Ensure that Go tool chain is available and is built from source"
  debug: true   # lets you `ax ssh` into the sandbox
```

Apply and inspect (README.md:48):

```bash
ax apply -f task.yaml
ax watch task test
ax ssh test -- ls -al /workspace
```

> [!WARNING] Core concepts, protocols, and specifications are still being refined; expect major breaking changes before a stable release (README.md:12).
## Core primitives
| You want to... | AX gives you |
|---|---|
| Run untrusted agent code in an isolated sandbox with CPU/memory limits | **`Task`** |
| Pre-wire Git repos, MCP servers, and skill packages so every agent starts warm | **`Workspace`** |
| Lock outbound traffic down to an explicit host allowlist | **`Gateway`** |
| Configure which LLM the platform itself uses, with credentials from a Kubernetes secret | **`Model`** |
| Pause an idle agent and pick up exactly where it left off | `ax suspend` / `ax resume` |
| Shell into a running agent to see what it is doing | `ax ssh` |

(Table from README.md:59.)
## Getting started
1. Install the CLI (README.md:76):

```bash
go install github.com/google/ax/cmd/ax@latest
```

Binary lands in `$(go env GOPATH)/bin`; that directory must be on `PATH` (README.md:78).
2. Deploy the control plane (README.md:86): requires a Kubernetes cluster, `ko` (`brew install ko`), a container registry the cluster can pull from, and a reachable Agent Substrate Control API (in-cluster default `api.ate-system.svc.cluster.local:443`).

```bash
make deploy AX_IMAGE_REPO=<your-registry>
```

Deploys Redis first, then builds and deploys control plane images with `ko` into the `ax-system` namespace (README.md:90).
3. Run the first task (README.md:97):

```bash
ax apply -f examples/task.yaml       # Task + Workspace + Gateway + Model in one file
ax get tasks
ax watch task task123                # stream phase and condition changes live
ax ssh task123 -- ls -la /workspace  # poke around inside the sandbox
ax suspend task task123              # checkpoint and pause
ax resume task task123               # pick up where it left off
```

Full lifecycle demo: `./demo.sh` applies a custom workspace, waits for readiness, runs commands over `ax ssh`, and suspends the task (README.md:109).
## Documentation map
| Guide | Read it to... |
|---|---|
| [Concepts](docs/concepts.md) | Learn what a `Task`, `Workspace`, `Gateway`, and `Model` each do, and how a task moves through phases and conditions. |
| [Manifests](docs/manifests.md) | Write your own YAML, with an annotated example of every kind. |
| [Sandbox](docs/sandbox.md) | See what the runner does on boot and what your command can rely on: metadata server, guest services, environment. |
| [Runners](docs/runner.md) | Understand the contract between the control plane and the task container, and build your own runner image to replace the default. |
| [Networking](docs/networking.md) | Reach a running task through the atenet router from the cluster, your laptop, or a gRPC client. |
| [Architecture](DESIGN.md) | Understand how the control plane fits together, plus the API reference. |
| [Development](docs/development.md) | Build, test, and ship changes to AX itself. |
| [Roadmap](docs/roadmap.md) | See planned milestones across core specs, actor architecture, agentic environments, and governance. |

(Table from README.md:115.)
## CLI usage
`ax` talks to the control plane over gRPC and is deliberately `kubectl`-shaped: `apply`, `get`, `describe`, `watch`, `delete`, plus agent-specific verbs (README.md:130).

Everyday commands (README.md:136):

```bash
# Apply anything (multi-document YAML, file or stdin)
ax apply -f examples/task.yaml

# Tasks
ax get tasks                          # list
ax get tasks -a my-atespace           # list in another atespace
ax get task task123                   # full spec + live status as YAML
ax describe task task123              # human-readable detail
ax watch task task123                 # stream status and condition transitions
ax suspend task task123               # checkpoint actor state and pause
ax resume task task123                # resume a suspended task
ax delete task task123

# Shell into the running sandbox
ax ssh task123                        # interactive shell (task needs spec.debug: true)
ax ssh task123 -- ls -la /workspace   # one-off command
ax ssh task123 -- python3 main.py

# Gateways, workspaces, models follow the same pattern
ax get gateways
ax describe gateway default-gateway
ax delete gateway default-gateway

ax get workspaces
ax describe workspace default-workspace
ax delete workspace default-workspace

ax get models
ax describe model default-model
ax delete model default-model

# Connection plumbing
ax ctx                                # active kube context and how ax is reaching the control plane
ax tunnel list                        # background tunnels (state lives in ~/.ax/tunnels)
ax tunnel stop
ax version
```

Works with `kubectx` (README.md:198):

```bash
kubectx staging-cluster
ax get tasks

kubectx prod-cluster
ax get tasks

# Or target a context without switching
ax --context=dev-cluster get tasks
```

### Global flags
| Flag | Description | Default |
|---|---|---|
| `-a`, `--atespace` | Atespace scope for the command | `default` |
| `-n`, `--namespace` | Kubernetes namespace where AX is installed | `ax-system` |
| `--context` | Kubernetes context to target | active `kubectx` / `current-context` |
| `--server` | Control plane address, bypassing auto-detection | derived from kube context, or `$AX_SERVER` |

(Table from README.md:217.)
**Covers:** README.md (project purpose, primitives, install/deploy/run, docs index, CLI reference)
