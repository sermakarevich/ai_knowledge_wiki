# Technical Analysis: google/ax

**Repository:** https://github.com/google/ax
**Version analyzed:** unknown
**Date:** 2026-09-24
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Agent workloads are neither stateless microservices nor run-to-completion batch jobs: they accumulate state, execute untrusted code, call models and tool servers, require strict network isolation, and need cost guardrails (README.md:57). Running millions to billions of such short-lived tasks per cluster exceeds what Kubernetes CRDs/etcd can store and reconcile at acceptable write rates (DESIGN.md:66).

AX addresses this as a declarative, Kubernetes-like orchestrator for sandboxed autonomous agent workloads (01-overview.md:3). Users declare `Task`, `Workspace`, `Gateway`, and `Model` manifests under `ax.io/v1alpha1` and apply them with a single command; the control plane sandboxes execution, pre-wires workspaces, fences outbound networking, and scales runs on top of Agent Substrate (README.md:17, README.md:19, README.md:57, README.md:68). Lifecycle operations (`suspend`/`resume`, `ssh`) are first-class (README.md:57).

Primary user: a developer or platform operator running many untrusted agent tasks on a Kubernetes cluster with access to an Agent Substrate Control API.

## 2. High-Level Architecture

```
ax CLI ──► ax-server (:8080 gRPC + /healthz) ──► Redis (hashes + streams + pubsub)
 │                        │                              │
 │                        ▼                              ▼
 │              persist + publish event          XREADGROUP consume
 │                                                       │
 └─► tunnel / kube-context ──► ax-system ──► ax-controller (scaled workers) ──► Agent Substrate
                                                                                 │ (atespace / actor / worker / egress)
                                                                                 ▼
                                                                    ax-task-runner (in-task container)
```

Control-plane binaries are `ax` (CLI), `ax-server` (stateless gRPC API), `ax-controller` (reconciliation workers), and `ax-task-runner` (in-container entrypoint); the gRPC service is `ax.v1alpha1.AX` with Task/Gateway/Workspace/Model `Get`/`List`/`Update`/`Delete` RPCs plus `SuspendTask`, `ResumeTask`, streaming `WatchTask` (DESIGN.md:299-351). `ax-server` validates manifests, persists to Redis, and publishes events; controllers consume the Redis Stream via `XREADGROUP`, provision atespaces and actors on Agent Substrate, apply egress policy, and drive tasks toward desired state (DESIGN.md:68-97, DESIGN.md:301-306). Task containers boot via `ax-task-runner`, which bootstraps the workspace, serves metadata, and runs the agent command (DESIGN.md:301-306). The CLI follows the active kube context (including `kubectx`) and maintains background tunnels to that cluster's control plane (README.md:198).

Data-flow narrative:

1. `ax apply -f task.yaml` sends multi-document YAML over gRPC; `ax-server` validates, writes Task hashes, and publishes to Redis Streams (DESIGN.md:68-97, README.md:48).
2. `ax-controller` replicas consume events via `XREADGROUP` and reconcile: provision atespace, create/activate actor, assign worker, install egress policy (DESIGN.md:68-97).
3. `ax-task-runner` boots inside the sandbox: clones workspace git repos, serves the metadata endpoint, exposes guest services and environment to the agent command (docs/sandbox.md per README.md:115; Dockerfile.task-runner:11-32).
4. Operator observes via `ax get/describe/watch` and inspects via `ax ssh` (requires `spec.debug: true`); `ax suspend` checkpoints actor state and pauses, `ax resume` continues from checkpoint (README.md:136, demo.sh:187-256).
5. Networking to running tasks goes through the atenet router from cluster, laptop, or gRPC client (docs/networking.md per README.md:115).
6. Deploy path is `make deploy AX_IMAGE_REPO=<registry>`: Redis first, then `ko`-built control-plane images into `ax-system` (README.md:90).

Persistent state lives in Redis (Task hashes, Event Streams, PubSub), explicitly chosen over Kubernetes CRDs/etcd (DESIGN.md:66). Local CLI tunnel state lives in `~/.ax/tunnels` (README.md:136). Kubernetes itself holds only the deployment (`ax-system` namespace) and `Model` credential secrets, not per-task objects.

## 3. Task, Workspace, Gateway, and Model — The Core Abstraction

Everything is a declarative `ax.io/v1alpha1` manifest with `apiVersion`, `kind`, `metadata`, `spec`, applied in one file (README.md:68). The four named kinds (README.md:59):

- `Task` (README.md:59): an isolated sandbox with CPU/memory limits running untrusted agent code; references workspaces by name with per-task `goal`; supports `spec.debug: true` for `ax ssh` access.
- `Workspace` (README.md:59): pre-wired starting state — Git repos, MCP servers, skill packages — so every agent starts warm. Example spec (`demo.sh:196-223`): `git: [{name: chalk, repo, branch: main, depth: 1}]`.
- `Gateway` (README.md:59): outbound network policy; an explicit host allowlist enforced as egress filtering on Agent Substrate.
- `Model` (README.md:59): which LLM the platform itself uses, with credentials sourced from a Kubernetes secret.

Task-to-workspace binding representation (README.md:16):

```yaml
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

Key queries are CLI-shaped, `kubectl`-style (README.md:130, README.md:136): `ax get tasks`, `ax get tasks -a my-atespace`, `ax get task task123` (full spec plus live status as YAML), `ax describe task task123` (human-readable), `ax watch task task123` (stream phase/condition transitions), with `gateways`, `workspaces`, `models` following the same `get/describe/delete` pattern.

## 4. LLM / External Service Integration

- `Model` resource: configures the LLM the platform uses; credentials come from a Kubernetes secret (README.md:59). Wiki excerpts do not name specific model providers, model IDs, or secret keys.
- Agent runtime: the task-runner image installs `google-antigravity` via pip (`Dockerfile.task-runner:11-32`), and `cmd/ax-task-runner/antigravity_bootstrap.py` is copied into the image; no provider endpoint or auth flow is documented in the covered pages.
- Mandatory external service: Agent Substrate Control API (default in-cluster `api.ate-system.svc.cluster.local:443`) for atespace/actor/worker/egress operations; deployment requires a Kubernetes cluster, `ko`, a pullable container registry, and Redis (README.md:86, README.md:90, DESIGN.md:68-97).
- In-sandbox service surface: a metadata server at `$AX_METADATA_URL` (e.g. `curl "$AX_METADATA_URL/metadata/v1alpha1/ax/task"` in `demo.sh:187-256`), guest services, and environment variables (`DEMO_ENV` example in `demo.sh:196-223`).
- Env vars observed: `$AX_METADATA_URL` (injected into sandbox), `$AX_SERVER` (CLI control-plane override). No LLM API keys are documented in the covered wiki pages.

No direct LLM provider call signatures, required/optional call graphs, or model-specific env vars can be grounded from the two wiki pages; the repo's own external calls center on Agent Substrate gRPC, Redis, and the atenet router.

## 5. Task Lifecycle — The Main Pipeline

1. **Declare manifests** (`README.md:48`, `demo.sh:196-223`): author multi-document YAML (`Workspace` with `spec.git`, `Task` with `spec.workspaces`, `spec.image`, `spec.env`, `spec.debug`). Example image pin: `gcr.io/ax-substrate/ate-images/ax-task-runner@sha256:3a0d…` (`demo.sh:196-223`).
2. **Apply** (`README.md:48`, `README.md:136`): `ax apply -f task.yaml` (file or stdin) → `ax-server` validates manifests, persists to Redis hashes, publishes stream event (DESIGN.md:68-97).
3. **Reconcile** (`DESIGN.md:68-97`, `DESIGN.md:301-306`): `ax-controller` workers `XREADGROUP` the event, provision the atespace, create and activate the actor, assign a worker, and install Gateway egress policy via the Substrate Control API.
4. **Bootstrap and run** (`Dockerfile.task-runner:11-32`, `demo.sh:187-256`): `ax-task-runner` entrypoint clones repos, sets up `/workspace`, serves metadata, and executes the agent command (default image `FROM python:3.12-slim` with `git curl ca-certificates openssh-client procps bash`).
5. **Observe and inspect** (`README.md:97`, `README.md:136`): `ax get tasks`, `ax describe task task123`, `ax watch task task123` (phase/condition stream); `ax ssh task123 -- <cmd>` for interactive or one-off inspection; `./demo.sh` polls `Phase:`/`Ready` every 2 s via `wait_for PHASE [READY]` (`demo.sh:128-178`) until `Running`/`True`.
6. **Suspend / resume / delete** (`README.md:97`, `README.md:136`, `demo.sh:187-256`): `ax suspend task task123` checkpoints actor state and pauses (demo waits for `Suspended`); `ax resume task task123` picks up where it left off; `ax delete task task123` (plus workspace/gateway/model deletes) removes resources.

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | — | Project purpose, four primitives, install/deploy/run, docs index, full CLI reference |
| `DESIGN.md` | — | Architecture rationale (Redis over etcd), data path, component table, gRPC API reference |
| `docs/concepts.md` | — | Task/Workspace/Gateway/Model semantics, task phases and conditions |
| `docs/manifests.md` | — | Annotated YAML for every kind |
| `docs/sandbox.md` | — | Runner boot behavior: metadata server, guest services, environment |
| `docs/runner.md` | — | Control-plane ↔ task-container contract; guide to custom runner images |
| `docs/networking.md` | — | Reaching tasks via the atenet router |
| `docs/development.md` | — | Building, testing, and shipping AX itself |
| `docs/roadmap.md` | — | Milestones: core specs, actor architecture, environments, governance |
| `cmd/ax` | — | `ax` CLI: apply/get/describe/watch/delete, suspend/resume, ssh, tunnel, ctx |
| `cmd/ax-server` | — | Stateless gRPC API (`ax.v1alpha1.AX`) on :8080 plus `GET /healthz` |
| `cmd/ax-controller` | — | Redis-stream reconciliation workers driving Substrate provisioning |
| `cmd/ax-task-runner` (+ `antigravity_bootstrap.py`) | — | In-sandbox entrypoint: workspace bootstrap, metadata, agent exec |
| `pkg/apis/v1alpha1` | — | Generated Go request/response types for the gRPC service |
| `demo.sh` | ~256 | End-to-end lifecycle demo: apply, poll to Running/Ready, ssh checks, suspend |
| `Dockerfile.task-runner` | ~32 | Task image: `python:3.12-slim`, tooling, `google-antigravity`, entrypoint |
| `go.mod` / `go.sum` | `go.sum` 76 lines | Module pins incl. substrate, go-redis, grpc, protobuf, otel, testify |
| `.ko.yaml` | ~74 | `ko` image builds for controller and task-runner (`CGO_ENABLED=0`, `-trimpath`, `-s -w`) |
| `examples/task.yaml` | — | Single-file Task + Workspace + Gateway + Model example |

Line counts marked `—` are not stated in the covered wiki pages; ranges given elsewhere are the cited excerpts (e.g. `.dockerignore:1-12`, `.ko.yaml:55-74`, `demo.sh:95-256`, `DESIGN.md:66-97, 299-351`).

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `github.com/agent-substrate/substrate` | pinned in `go.sum` (exact version not quoted) | Agent Substrate client: atespace/actor/worker provisioning |
| `github.com/agent-substrate/env` | pinned in `go.sum` (exact version not quoted) | Substrate environment support library |
| `github.com/redis/go-redis/v9` | `v9.22.0` | Redis hashes, Streams work queue, PubSub |
| `google.golang.org/grpc` | `v1.83.2` | `ax-server` gRPC API and Substrate Control API transport |
| `google.golang.org/protobuf` | `v1.36.12` | Protobuf codegen for `ax.v1alpha1` types |
| `go.opentelemetry.io/otel` | `v1.44.0` | Observability/tracing |
| `github.com/stretchr/testify` | `v1.12.1` | Test assertions |
| `google-antigravity` (pip) | unpinned (`pip install --no-cache-dir google-antigravity`) | Agent runtime inside task-runner image |
| `cgr.dev/chainguard/static:latest` | `latest` (ko `defaultBaseImage`) | Default base image for control-plane builds |
| `alpine/git:latest` | `latest` (ko override for `ax-task-runner`) | Base image override for task-runner build |
| `python:3.12-slim` | `3.12-slim` (Dockerfile `FROM`) | Task-container base image |
| `git, curl, ca-certificates, openssh-client, procps, bash` | distro-latest via `apt-get` | Tooling inside task image (clone, ssh, introspection) |
| `ko` | install via `brew install ko` (version unpinned) | Container image builder for `make deploy` |
| Redis | deployed before control plane via `make deploy` | Durable state + work queue + event bus |
| Kubernetes cluster + pullable registry | operator-provided | Deploy target (`ax-system`) and image distribution |

Required first (runtime): Kubernetes, Redis, Agent Substrate Control API, container registry. Build-time: Go toolchain, `ko`. Test-only: `testify`.

## 8. CLI / Usage Surface

Entry points: `ax` (developer CLI, `go install github.com/google/ax/cmd/ax@latest` into `$(go env GOPATH)/bin`, README.md:76), `ax-server`, `ax-controller`, `ax-task-runner` (cluster-side binaries, DESIGN.md:301-306).

| Command | Effect |
|---|---|
| `ax apply -f <file\|->` | Apply multi-document YAML (Task/Workspace/Gateway/Model) |
| `ax get tasks [-a ATESPACE]` | List tasks (optionally in another atespace) |
| `ax get task NAME` | Full spec + live status as YAML |
| `ax describe task NAME` | Human-readable task detail |
| `ax watch task NAME` | Stream status/condition transitions |
| `ax suspend task NAME` | Checkpoint actor state and pause |
| `ax resume task NAME` | Resume a suspended task |
| `ax delete task\|gateway\|workspace\|model NAME` | Delete a resource |
| `ax ssh NAME [-- cmd]` | Interactive shell or one-off command (needs `spec.debug: true`) |
| `ax get/describe/delete gateways\|workspaces\|models` | Same pattern for the other three kinds |
| `ax ctx` | Show active kube context and control-plane reachability |
| `ax tunnel list\|stop` | Manage background tunnels |
| `ax version` | Print CLI version |
| `./demo.sh` | Full lifecycle demo (apply → wait Running/Ready → ssh checks → suspend) |

Global flags (README.md:217):

| Flag | Description | Default |
|---|---|---|
| `-a, --atespace` | Atespace scope | `default` |
| `-n, --namespace` | Kubernetes namespace where AX is installed | `ax-system` |
| `--context` | Kubernetes context to target | active `kubectx` / `current-context` |
| `--server` | Control-plane address, bypassing auto-detection | derived from kube context, or `$AX_SERVER` |

Env vars and config:

| Variable | Default | Purpose |
|---|---|---|
| `AX_BIN` | `./bin/ax` | CLI path used by `demo.sh` |
| `ATESPACE` | `default` | Atespace used by `demo.sh` |
| `NO_COLOR` | unset | Disable colored demo output when set |
| `AX_SERVER` | unset | Control-plane address override for `ax` |
| `AX_IMAGE_REPO` | (required arg) | Container registry for `make deploy` |
| `AX_METADATA_URL` | injected in sandbox | Metadata server base URL inside task container |
| `~/.ax/tunnels` | — | Local background-tunnel state |

## 9. Extensibility Points

- Custom runner image: implement the `runner` package contract and replace the default image — set `Task.spec.image` (cf. `gcr.io/.../ax-task-runner@sha256:…` in `demo.sh:196-223`); contract and packaging in `docs/runner.md`, `cmd/ax-task-runner`, `Dockerfile.task-runner`.
- Workspace content: add `spec.git` entries (repo/branch/depth), MCP servers, and skill packages via `Workspace` manifests (`docs/manifests.md`, `demo.sh:196-223`).
- Network policy: define `Gateway` allowlists to scope task egress (`docs/networking.md`, `README.md:59`).
- Platform model: add/replace `Model` manifests with secret-backed credentials (`README.md:59`, `docs/manifests.md`).
- Controller scale-out: add `ax-controller` replicas consuming the Redis Stream group; no per-task CRDs to migrate (DESIGN.md:66-97).
- API evolution: extend `ax.v1alpha1.AX` RPCs and generated types in `pkg/apis/v1alpha1` (DESIGN.md:310-351).
- Multi-cluster targeting: `--context` / `kubectx` switching plus `ax tunnel` management in `cmd/ax` (README.md:198).

## 10. Limitations and Gotchas

- **Pre-stable API — expect breaking changes.** Core concepts, protocols, and specifications are still being refined (README.md:12); manifests written today may not apply tomorrow.
- **Heavy deploy prerequisites.** Needs a Kubernetes cluster, `ko`, a registry the cluster can pull from, and a reachable Agent Substrate Control API (default `api.ate-system.svc.cluster.local:443`) — there is no local-only quickstart in the covered pages (README.md:86).
- **`ax ssh` requires opting in.** Shell access only works when the Task sets `spec.debug: true` (README.md:16, README.md:136); forgetting the flag means no interactive inspection.
- **Redis is the single durable store.** Avoiding etcd removes the CRD write bottleneck but concentrates task hashes, streams, and PubSub in Redis (DESIGN.md:66); Redis sizing/HA is load-bearing and undocumented in the covered pages.
- **Task image is pinned by digest in examples.** The demo pins `gcr.io/ax-substrate/ate-images/ax-task-runner@sha256:3a0d…` (`demo.sh:196-223`); stale pins silently lag runner fixes, and the narrow `demo.sh` polling (`Phase:`/`Ready` string parse, 180 s default timeout, `demo.sh:128-178`) is brittle for slow image pulls or large clones.

## 11. How It Compares to Alternatives

- **Kubernetes Jobs / CronJobs + Kueue:** the default for run-to-completion batch work with etcd-backed CRDs and queueing; AX deliberately avoids per-task CRDs in favor of Redis Streams to reach far higher task churn, at the cost of operating a second durable store.
- **E2B (sandbox API):** hosted Firecracker micro-VMs with SDK-driven code execution; AX instead offers self-hosted, declarative, `kubectl`-shaped orchestration with Git/MCP workspace pre-wiring and Gateway egress policy on the user's own cluster.
- **Modal:** serverless containers with fast cold starts aimed at data/ML functions; AX targets long-lived stateful agents with checkpoint suspend/resume and in-sandbox `ssh` inspection rather than function invocation.
- **Daytona / DevZero style dev sandboxes:** SSH-able ephemeral dev environments; AX overlaps on `ax ssh` debuggability but adds the Task/Workspace/Gateway/Model control plane, atenet routing, and billion-task-scale controller design.

Positioning: AX is the Kubernetes-native, declarative option for operators who want agent-task orchestration (sandboxing, workspace wiring, egress fencing, suspend/resume) on their own cluster and Substrate backend, rather than a hosted sandbox API or generic batch scheduler.

## Appendix: Selected Code Snippets

`README.md:16` — minimal Workspace + Task declaration:

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

`demo.sh:196-223` — demo manifest with pinned runner image and env:

```yaml
apiVersion: ax.io/v1alpha1
kind: Workspace
metadata:
  name: ${WORKSPACE_NAME}
  atespace: ${ATESPACE}
spec:
  git:
    - name: chalk
      repo: "${REPO_URL}"
      branch: "main"
      depth: 1
---
apiVersion: ax.io/v1alpha1
kind: Task
metadata:
  name: ${TASK_NAME}
  atespace: ${ATESPACE}
spec:
  debug: true
  image: "gcr.io/ax-substrate/ate-images/ax-task-runner@sha256:3a0dea6ad8b55278685db58aca6e37dc4ba04056831d45bef3aaeafdca43cac6"
  workspaces:
    - name: ${WORKSPACE_NAME}
      path: "/workspace"
  env:
    - name: DEMO_ENV
      value: "active"
```

`Dockerfile.task-runner:11-32` — task-container image:

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    openssh-client \
    procps \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir google-antigravity

COPY bin/linux_amd64/ax-task-runner /usr/local/bin/ax-task-runner
COPY cmd/ax-task-runner/antigravity_bootstrap.py /usr/local/bin/antigravity_bootstrap.py

ENTRYPOINT ["/usr/local/bin/ax-task-runner"]
```

`.ko.yaml:55-74` — container build configuration:

```yaml
defaultBaseImage: cgr.dev/chainguard/static:latest
baseImageOverrides:
  github.com/google/ax/cmd/ax-task-runner: alpine/git:latest
builds:
  - id: ax-controller
    main: ./cmd/ax-controller
    env:
      - CGO_ENABLED=0
    flags:
      - -trimpath
    ldflags:
      - -s -w
  - id: ax-task-runner
    main: ./cmd/ax-task-runner
    env:
      - CGO_ENABLED=0
    flags:
      - -trimpath
    ldflags:
      - -s -w
```
