> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** Top-level files define the repo's build, runtime, architecture, and demo entry points for the AX task orchestrator.
## Key points
- `.dockerignore` excludes local tooling and build outputs (`.git`, `.idea`, `.vscode`, `.claude`, `*.log`, `tmp/`, `bin/`, `ax`, `ax-server`, `ax-task-runner`, `ax-controller`) from Docker build context (`.dockerignore:1-12`).
- `.gitignore` excludes built binaries (`bin/`, `/tmp/`, `*.exe`, `*.test`, `/ax`, `/ax-server`, `/ax-task-runner`, `/ax-controller`) plus a Python cache artifact at `cmd/ax-task-runner/__pycache__/antigravity_bootstrap.cpython-313.pyc` (`.gitignore:1-12`).
- `.ko.yaml` configures `ko` image builds with `defaultBaseImage: cgr.dev/chainguard/static:latest`, an `alpine/git:latest` override for `github.com/google/ax/cmd/ax-task-runner`, and two `CGO_ENABLED=0` / `-trimpath` / `-s -w` builds for `ax-controller` and `ax-task-runner` (`.ko.yaml:55-74`).
- `demo.sh` scripts the full single-task lifecycle in about two minutes: declare Workspace + Task YAML and `ax apply`, watch until `Running`/`Ready`, inspect via `ax ssh`, then `ax suspend` with workspace checkpoint (`demo.sh:95-104`, `demo.sh:193-250`).
- `demo.sh` is parameterized by `AX_BIN` (default `./bin/ax`), `ATESPACE` (default `default`), and `NO_COLOR`, and defines `ax()`, `run()`, `in_sandbox()`, `task_field()`, and polling `wait_for PHASE [READY]` helpers (`demo.sh:102-178`).
- `DESIGN.md` states AX keeps state in Redis with Redis Streams as the work queue instead of Kubernetes CRDs/etcd, flowing `ax-server` (gRPC API + `/healthz`) → Redis (hashes + streams + pubsub) → `ax-controller` (`XREADGROUP`) → Agent Substrate (atespace/actor/worker/egress) (`DESIGN.md:66-97`).
- `DESIGN.md` defines four binaries (`ax`, `ax-server`, `ax-controller`, `ax-task-runner`) and the `ax.v1alpha1.AX` gRPC service with Task/Gateway/Workspace/Model `Get`/`List`/`Update`/`Delete` RPCs plus `SuspendTask`, `ResumeTask`, and streaming `WatchTask` (`DESIGN.md:299-351`).
- `Dockerfile.task-runner` builds the task image `FROM python:3.12-slim` with `git`, `curl`, `ca-certificates`, `openssh-client`, `procps`, `bash`, `pip install google-antigravity`, copies in `ax-task-runner` and `antigravity_bootstrap.py`, and sets `ENTRYPOINT ["/usr/local/bin/ax-task-runner"]` (`Dockerfile.task-runner:11-32`).
---
## .dockerignore
Excludes editor, VCS, log, temp, and built-binary paths from the Docker context (`.dockerignore:1-12`):

```
.git
.idea
.vscode
.claude
*.log
tmp/
bin/
ax
ax-server
ax-task-runner
ax-controller
```

## .gitignore
Excludes build outputs and one generated Python artifact from version control (`.gitignore:1-12`):

```
# Binaries
bin/
/tmp/
*.exe
*.test
/ax
/ax-server
/ax-task-runner
/ax-controller

cmd/ax-task-runner/__pycache__/antigravity_bootstrap.cpython-313.pyc
```

## .ko.yaml
`ko` container-build config (`.ko.yaml:55-74`):

| Key | Value |
|---|---|
| `defaultBaseImage` | `cgr.dev/chainguard/static:latest` |
| `baseImageOverrides["github.com/google/ax/cmd/ax-task-runner"]` | `alpine/git:latest` |
| `builds[0].id` / `main` | `ax-controller` / `./cmd/ax-controller` |
| `builds[1].id` / `main` | `ax-task-runner` / `./cmd/ax-task-runner` |
| `env` (both builds) | `CGO_ENABLED=0` |
| `flags` (both builds) | `-trimpath` |
| `ldflags` (both builds) | `-s -w` |

Verbatim excerpt (`.ko.yaml:55-74`):

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

## demo.sh
End-to-end demo script, `set -euo pipefail`, about-two-minute lifecycle (`demo.sh:95-113`):

```bash
AX_BIN="${AX_BIN:-./bin/ax}"
ax() { "${AX_BIN}" "$@"; }
ATESPACE="${ATESPACE:-default}"
TASK_NAME="demo-task"
WORKSPACE_NAME="demo-workspace"
REPO_URL="https://github.com/chalk/chalk.git"
```

Environment (`demo.sh:102-105`):

| Variable | Default | Purpose |
|---|---|---|
| `AX_BIN` | `./bin/ax` | path to the ax CLI |
| `ATESPACE` | `default` | atespace to run the demo in |
| `NO_COLOR` | unset | set to disable colored output |

Helpers (`demo.sh:128-178`): `step()` numbers presentation steps; `run()` echoes `$ <cmd>` then runs it; `in_sandbox()` runs a snippet via `ax ssh "${TASK_NAME}" -a "${ATESPACE}" -- sh -c`; `task_field()` parses `ax describe task`; `wait_for PHASE [READY] [timeout=180]` polls `Phase:`/`Ready` every 2s with elapsed-time output.

Applied manifest (`demo.sh:196-223`):

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

Flow (`demo.sh:187-256`): clean up old `demo-task`/`demo-workspace`; `ax apply -f` the YAML; `wait_for "Running" "True"`; `ax get tasks`; `ax describe task`; `ax ssh` checks (`ls -la /workspace`, `ls -la /workspace/chalk`, `DEMO_ENV`/`AX_METADATA_URL`, `curl "$AX_METADATA_URL/metadata/v1alpha1/ax/task"`); `ax suspend task` then `wait_for "Suspended"`; ends with `ax resume` / `ax ssh` / `ax delete` hints.

## DESIGN.md
Architecture rationale (`DESIGN.md:66`): millions of short-lived tasks as Kubernetes CRDs would push etcd past single-digit-GB storage and write-rate limits, so AX uses Redis plus Redis Streams between API server and scaled controllers.

Data path (`DESIGN.md:68-97`):

```
ax apply -f task.yaml → ax-server (gRPC API + /healthz) → store & publish event → Redis (Task Hashes + Event Streams + PubSub) → XREADGROUP → ax-controller (Horizontally Scaled Workers) → gRPC (Control API) → Agent Substrate (Atespace Provisioning, Actor Creation & Activation, Worker Assignment, Egress Policy Filtering)
```

Component table (`DESIGN.md:301-306`):

| Binary | Role |
|---|---|
| `ax` | Developer CLI. Applies manifests, inspects and watches resources, tunnels to the cluster. |
| `ax-server` | Stateless gRPC API on port 8080. Validates manifests, persists to Redis, publishes events. |
| `ax-controller` | Reconciliation workers. Consume the Redis stream, provision atespaces and actors on Agent Substrate, apply egress policy, and drive tasks toward desired state. Scale by adding replicas. |
| `ax-task-runner` | Entrypoint inside every task container. Bootstraps the workspace, serves metadata, and runs the agent command. A thin wrapper over the `runner` package, which custom images can embed directly. |

API reference (`DESIGN.md:310-351`): control plane exposes `ax.v1alpha1.AX` gRPC service; health is plain HTTP `GET /healthz` returning `200 OK` on the same port. Request/response types follow `<Method>Request` / `<Method>Response`; generated Go types live in `pkg/apis/v1alpha1`.

| Group | RPCs |
|---|---|
| Tasks | `GetTask`, `ListTasks`, `UpdateTask`, `DeleteTask`, `SuspendTask`, `ResumeTask`, `WatchTask` (server-streaming status/condition transitions) |
| Gateways | `GetGateway`, `ListGateways`, `UpdateGateway`, `DeleteGateway` |
| Workspaces | `GetWorkspace`, `ListWorkspaces`, `UpdateWorkspace`, `DeleteWorkspace` |
| Models | `GetModel`, `ListModels`, `UpdateModel`, `DeleteModel` |

## Dockerfile.task-runner
Task-container image definition (`Dockerfile.task-runner:11-32`):

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

## go.sum
Pinned Go module checksums, 76 lines (`go.sum:1-76`); notable entries include `github.com/agent-substrate/substrate`, `github.com/agent-substrate/env`, `github.com/redis/go-redis/v9 v9.22.0`, `google.golang.org/grpc v1.83.2`, `google.golang.org/protobuf v1.36.12`, `go.opentelemetry.io/otel v1.44.0`, and `github.com/stretchr/testify v1.12.1`. No truncated files were noted in the chunk.

**Covers:** `.dockerignore`, `.gitignore`, `.ko.yaml`, `demo.sh`, `DESIGN.md`, `Dockerfile.task-runner`, `go.sum`
