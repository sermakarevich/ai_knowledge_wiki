# google/ax
> PDF location (no local source.pdf): https://github.com/google/ax
Source: https://github.com/google/ax
Kind: repo
Fetched: 2026-09-24T02:58:11.879734+00:00
Tool: git-clone

# google/ax

Commit: ace03604a60167d111589c6db8c1c7f88aa8e6b5

## README

<h1>
  <img src="assets/axolotl.svg" width="70" align="absmiddle" alt="AX axolotl">
  AX
</h1>

> [!WARNING]
> We are still actively refining our core concepts, protocols,
> and specifications. We will likely to introduce major breaking
> changes prior to a stable release.

**Declare an agentic task with workspaces and gateway specifications. AX sandboxes it, wires up its workspace, fences its network, and helps running it at scale.**

AX is a high-throughput, declarative orchestrator to run billions of autonomous agent workloads in a cluster. It runs on top of [Agent Substrate](https://github.com/agent-substrate/substrate) for sandboxed execution and is built to run billions of tasks per cluster. If you have used Kubernetes, `ax` will feel similar.

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

Then apply it, watch it come up, and look over the agent's shoulder:

```bash
ax apply -f task.yaml
ax watch task test
ax ssh test -- ls -al /workspace
```



## Why?

Agents are a new kind of workload. They are neither stateless microservices nor run-to-completion batch jobs. They accumulate state, need strict isolation, call out to model APIs and tool servers, and can burn money in a loop if nobody is watching. AX gives you four small primitives that handle all of that declaratively:

| You want to... | AX gives you |
|---|---|
| Run untrusted agent code in an isolated sandbox with CPU/memory limits | **`Task`** |
| Pre-wire Git repos, MCP servers, and skill packages so every agent starts warm | **`Workspace`** |
| Lock outbound traffic down to an explicit host allowlist | **`Gateway`** |
| Configure which LLM the platform itself uses, with credentials from a Kubernetes secret | **`Model`** |
| Pause an idle agent and pick up exactly where it left off | `ax suspend` / `ax resume` |
| Shell into a running agent to see what it is doing | `ax ssh` |

Everything is expressed as `ax.io/v1alpha1` manifests and applied with a single command.



### 1. Install the CLI

```bash
go install github.com/google/ax/cmd/ax@latest
```

This puts the `ax` binary in `$(go env GOPATH)/bin`. Make sure that directory is on your `PATH`.



### 2. Deploy the control plane

You need a Kubernetes cluster, [`ko`](https://ko.build/) (`brew install ko`), a container registry your cluster can pull from, and a reachable Agent Substrate Control API (in-cluster default: `api.ate-system.svc.cluster.local:443`).

```bash
make deploy AX_IMAGE_REPO=<your-registry>
```

This deploys Redis, then builds and deploys the control plane images with `ko`. Everything lands in the `ax-system` namespace.



### 3. Run your first task

```bash
ax apply -f examples/task.yaml       # Task + Workspace + Gateway + Model in one file
ax get tasks


# task123   default    Running   task123         10.20.3.67   1m

ax watch task task123                # stream phase and condition changes live
ax ssh task123 -- ls -la /workspace  # poke around inside the sandbox
ax suspend task task123              # checkpoint and pause
ax resume task task123               # pick up where it left off
```

Want to see the whole lifecycle end to end? Run [`./demo.sh`](demo.sh). It applies a custom workspace, waits for readiness, runs commands over `ax ssh`, and suspends the task.



## Documentation

| Guide | Read it to... |
|---|---|
| [Concepts](docs/concepts.md) | Learn what a `Task`, `Workspace`, `Gateway`, and `Model` each do, and how a task moves through phases and conditions. |
| [Manifests](docs/manifests.md) | Write your own YAML, with an annotated example of every kind. |
| [Sandbox](docs/sandbox.md) | See what the runner does on boot and what your command can rely on: metadata server, guest services, environment. |
| [Runners](docs/runner.md) | Understand the contract between the control plane and the task container, and build your own runner image to replace the default. |
| [Networking](docs/networking.md) | Reach a running task through the atenet router from the cluster, your laptop, or a gRPC client. |
| [Architecture](DESIGN.md) | Understand how the control plane fits together, plus the [API reference](DESIGN.md#api-reference). |
| [Development](docs/development.md) | Build, test, and ship changes to AX itself. |
| [Roadmap](docs/roadmap.md) | See planned milestones across core specs, actor architecture, agentic environments, and governance. |



## CLI usage

`ax` talks to the control plane over gRPC. It is deliberately `kubectl`-shaped: `apply`, `get`, `describe`, `watch`, `delete`, plus a few agent-specific verbs.



### Everyday commands

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


# default-gateway   default    8494/gRPC,8080/HTTP   *
ax describe gateway default-gateway
ax delete gateway default-gateway

ax get workspaces


# default-workspace   default    1           1
ax describe workspace default-workspace
ax delete workspace default-workspace

ax get models


# default-model   default    google     gemini-3.8-flash
ax describe model default-model
ax delete model default-model



# Connection plumbing
ax ctx                                # active kube context and how ax is reaching the control plane
ax tunnel list                        # background tunnels (state lives in ~/.ax/tunnels)
ax tunnel stop
ax version
```



### Works with `kubectx`

`ax` follows your active Kubernetes context. Switch clusters and `ax` resolves and tunnels to that cluster's control plane in the background.

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

## go.mod

```
module github.com/google/ax

go 1.27.1

require (
	github.com/agent-substrate/env v0.0.11-0.20260912052224-4468a200b170
	github.com/agent-substrate/substrate v0.0.0-20260911232748-672533541dbf
	github.com/redis/go-redis/v9 v9.22.0
	google.golang.org/grpc v1.83.2
	google.golang.org/protobuf v1.36.12
	gopkg.in/yaml.v3 v3.0.1
)

require (
	github.com/cespare/xxhash/v2 v2.3.0 // indirect
	github.com/kr/pretty v0.3.1 // indirect
	github.com/rogpeppe/go-internal v1.14.1 // indirect
	go.uber.org/atomic v1.11.0 // indirect
	golang.org/x/net v0.58.0 // indirect
	golang.org/x/sys v0.47.0 // indirect
	golang.org/x/text v0.41.0 // indirect
	google.golang.org/genproto/googleapis/rpc v0.0.0-20260720211330-0afa2a65878a // indirect
	gopkg.in/check.v1 v1.0.0-20201130134442-10cb98267c6c // indirect
)

```

## Top-level layout

- .dockerignore (~11 lines)
- .github/ (dir, 2 files, ~94 lines)
- .gitignore (~11 lines)
- .ko.yaml (~35 lines)
- assets/ (dir, 2 files, ~45 lines)
- cmd/ (dir, 5 files, ~1708 lines)
- CONTRIBUTING.md (~122 lines)
- demo.sh (~177 lines)
- deploy/ (dir, 3 files, ~260 lines)
- DESIGN.md (~90 lines)
- Dockerfile.task-runner (~31 lines)
- docs/ (dir, 8 files, ~536 lines)
- examples/ (dir, 2 files, ~131 lines)
- go.mod (~24 lines)
- go.sum (~75 lines)
- internal/ (dir, 22 files, ~6854 lines)
- LICENSE (~202 lines)
- Makefile (~97 lines)
- pkg/ (dir, 5 files, ~5582 lines)
- README.md (~186 lines)
- runner/ (dir, 2 files, ~550 lines)

