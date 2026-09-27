---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: google/ax

### Q1. What is AX in one sentence, and what workload shape does it target?
> [!tip]- Answer
> AX is a declarative, Kubernetes-like orchestrator for running sandboxed autonomous agent workloads at scale. It runs untrusted agent code that fits neither stateless microservices nor run-to-completion batch jobs, handling accumulated state, strict isolation, model/tool-server calls, and cost guardrails declaratively. It targets billions of autonomous tasks per cluster on top of Agent Substrate. See [[wiki/01-overview|Overview]].

### Q2. What are the four declarative primitives in AX, and what are `suspend`/`resume` and `ssh` for?
> [!tip]- Answer
> The four primitives are `Task` (isolated sandbox with CPU/memory limits), `Workspace` (pre-wired Git repos, MCP servers, skill packages), `Gateway` (egress host allowlist), and `Model` (platform LLM with credentials from a Kubernetes secret). `ax suspend`/`resume` checkpoints an idle agent and picks up exactly where it left off, while `ax ssh` shells into a running sandbox for inspection. Everything is expressed as `ax.io/v1alpha1` manifests applied with a single command. See [[wiki/01-overview|Overview]].

### Q3. How do you install, deploy, and operate AX with the `ax` CLI across clusters?
> [!tip]- Answer
> Install with `go install github.com/google/ax/cmd/ax@latest`, then deploy with `make deploy AX_IMAGE_REPO=<registry>` into the `ax-system` namespace with Redis via `ko`. The `kubectl`-shaped CLI offers `apply`, `get`, `describe`, `watch`, `delete` plus `suspend`, `resume`, and `ssh` over gRPC with global flags for atespace, namespace, context, and server. It follows the active kube context including `kubectx` and tunnels to that cluster's control plane in the background. See [[wiki/01-overview|Overview]].

### Q4. Why does AX keep state in Redis instead of Kubernetes CRDs/etcd, and what is the data path?
> [!tip]- Answer
> Millions of short-lived tasks as CRDs would push etcd past single-digit-GB storage and write-rate limits, so AX uses Redis hashes plus Redis Streams as the work queue. The path is `ax-server` (gRPC API plus `/healthz`) writing to Redis (hashes, streams, pubsub), then scaled `ax-controller` workers consuming via `XREADGROUP` and provisioning atespaces, actors, workers, and egress policy on Agent Substrate. Controllers scale horizontally by adding replicas. See [[wiki/02-top-level-files|top-level-files]].

### Q5. What are the four AX binaries and the `ax.v1alpha1.AX` gRPC service groups?
> [!tip]- Answer
> The binaries are `ax` (developer CLI), `ax-server` (stateless gRPC API on port 8080 that validates and persists to Redis), `ax-controller` (reconciliation workers driving tasks toward desired state), and `ax-task-runner` (in-container entrypoint bootstrapping workspaces and running the agent command). The gRPC service exposes Task, Gateway, Workspace, and Model `Get`/`List`/`Update`/`Delete` RPCs, with Tasks adding `SuspendTask`, `ResumeTask`, and streaming `WatchTask` for status transitions. Health is plain HTTP `GET /healthz` on the same port. See [[wiki/02-top-level-files|top-level-files]].

### Q6. What do `demo.sh`, `.ko.yaml`, and `Dockerfile.task-runner` each define?
> [!tip]- Answer
> `demo.sh` scripts the full single-task lifecycle in about two minutes: apply Workspace plus Task YAML, poll until `Running`/`Ready`, inspect via `ax ssh`, then `suspend` with workspace checkpoint, parameterized by `AX_BIN`, `ATESPACE`, and `NO_COLOR`. `.ko.yaml` configures `ko` builds with a Chainguard static base, an alpine/git override for the task-runner, and `CGO_ENABLED=0`/`-trimpath`/`-s -w` builds for controller and runner. `Dockerfile.task-runner` builds `FROM python:3.12-slim` with git, curl, ssh client, `pip install google-antigravity`, and `ENTRYPOINT ["/usr/local/bin/ax-task-runner"]`. See [[wiki/02-top-level-files|top-level-files]].

### Q7. Should a team adopt AX today for production agent workloads, and why or why not?
> [!tip]- Answer
> Recommend against production adoption today because core concepts, protocols, and specs are explicitly still being refined with major breaking changes expected before stable release. Recommend it only for experiments where declarative sandboxed orchestration at scale, Redis-backed throughput, and suspend/resume plus ssh debuggability outweigh API instability. Revisit once the manifests, controller semantics, and runner contract stabilize. See [[wiki/01-overview|Overview]].
