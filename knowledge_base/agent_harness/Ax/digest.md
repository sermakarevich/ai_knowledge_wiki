> [[index|Wiki]] | [[summary|Summary]]
# google/ax — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** AX is a declarative, Kubernetes-like orchestrator for running sandboxed autonomous agent workloads at scale.
## Key points
- Declares agentic tasks via `Workspace` and gateway specifications, then sandboxes execution, wires workspaces, fences networking, and scales runs (README.md:17).
- Targets high-throughput orchestration of billions of autonomous agent tasks per cluster on top of Agent Substrate for sandboxed execution (README.md:19).
- Uses four declarative primitives — `Task`, `Workspace`, `Gateway`, `Model` — plus `ax suspend`/`resume` and `ax ssh` for lifecycle and inspection (README.md:57).
- Expresses everything as `ax.io/v1alpha1` manifests applied with a single command (README.md:68).
- Deploys its control plane (plus Redis) into the `ax-system` Kubernetes namespace via `make deploy` with `ko` and a container registry (README.md:90).
- Exposes a `kubectl`-shaped `ax` CLI over gRPC with `apply`, `get`, `describe`, `watch`, `delete` plus agent-specific verbs (README.md:130).
- Follows the active Kubernetes context (including `kubectx`) and tunnels to that cluster's control plane in the background (README.md:198).
## 2. [[wiki/02-top-level-files|top-level-files]]
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
## The system in five moves
1. Declare the desired agent workload as `ax.io/v1alpha1` Task/Workspace/Gateway/Model manifests and apply them with the kubectl-shaped `ax` CLI.
2. Serve the API from stateless `ax-server` over gRPC, persisting state and publishing events to Redis rather than etcd/CRDs for billion-task scale.
3. Reconcile via scaled `ax-controller` workers consuming Redis Streams and provisioning atespaces, actors, workers, and egress policy on Agent Substrate.
4. Execute inside the `python:3.12-slim` task-runner sandbox that bootstraps git workspaces, serves metadata, and runs the agent command under CPU/memory and network fencing.
5. Operate and inspect the live system with `get`/`describe`/`watch`, `ssh` into debuggable sandboxes, and `suspend`/`resume` checkpointed tasks, following kube contexts with background tunnels.
6. Build, deploy, and demo the whole loop with `ko` images into `ax-system`, Redis, and the scripted `demo.sh` lifecycle from apply to suspend.
