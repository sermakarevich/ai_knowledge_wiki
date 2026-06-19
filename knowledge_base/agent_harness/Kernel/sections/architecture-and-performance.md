> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Architecture & Performance

### The Unikernel Architecture

The technical foundation that differentiates Kernel from container- and VM-based cloud browser providers is its use of **unikernels** to run each browser instance.

A unikernel is a specialized, single-purpose machine image compiled to include only the OS components the target application actually requires. For Kernel, the application is Chromium. Rather than booting a full Linux userland with a general-purpose kernel, init system, unused drivers, and background services, a unikernel strips the image down to the exact OS surface Chromium needs -- nothing more. The result is a dramatically smaller image, lower memory and CPU footprint per browser instance, and far less initialization work at boot time.

This is the root cause of Kernel's claimed cold-start and cost advantages. There is simply less to boot and less to run. Competing platforms that run browsers inside standard Linux containers or VMs must initialize a fuller OS userland per instance, which is why their cold-start times are measured in seconds rather than milliseconds.

#### Unikernel vs Container/VM: What Changes

| Dimension | Container / VM approach | Kernel unikernel approach |
|---|---|---|
| OS surface per browser | Full (or near-full) Linux userland | Only what Chromium requires |
| Image size | Larger; general-purpose OS layers | Minimal; application-specific |
| Boot initialization | Full OS init path | Minimal; purpose-built entrypoint |
| Cold-start latency | Seconds (3-5s typical) | Sub-300ms (see benchmarks below) |
| Per-browser overhead | Higher; unused OS components present | Lower; no extraneous processes |

The unikernel approach is not a deployment optimization layered on top of a conventional browser runtime -- it is a fundamental architectural choice that affects every downstream performance and cost characteristic.

---

### Performance Benchmarks

The figures below are drawn from Kernel's documentation and third-party benchmarks. They have not been independently reproduced here and should be treated as vendor-reported or benchmark-context numbers pending independent verification.

#### Startup Latency

| Metric | Kernel | Typical container-based provider | Notes |
|---|---|---|---|
| Warm spin-up | < 30 ms | Not applicable (no equivalent warm-pool primitive) | Browser acquired from a standing reserved pool; no boot required |
| Cold start | Sub-300 ms -- sub-325 ms | 3-5 seconds | Genuine boot of a fresh unikernel from nothing |

#### Comparison with Browserbase (benchmark figures)

| Dimension | Kernel vs Browserbase |
|---|---|
| Cold-start speed | ~5.8x faster |
| End-to-end task speed | ~3.7x faster |
| Cost | 50%+ lower |

---

### Critical Nuance: Warm Spin-Up vs Cold Start

The "< 30 ms spin-up" and the "sub-300 ms cold start" are **two distinct metrics measuring two different things**. They can both be simultaneously true, and conflating them produces a misleading picture of Kernel's actual startup behavior.

**Warm spin-up (< 30 ms):** This figure almost certainly refers to acquiring a browser that is already running in a reserved standby pool. No boot occurs -- the browser process exists and is handed to the caller. The latency here is scheduling and handoff overhead, not OS initialization. A workload that consistently draws from a warm pool will observe sub-30 ms session acquisition.

**Cold start (sub-300 ms -- sub-325 ms):** This figure refers to booting a fresh unikernel from scratch with no pre-warmed instance available. Even at sub-300 ms this is roughly 10-16x faster than container-based alternatives, but it is categorically different from the warm-pool path.

**Practical implication for benchmarkers:** A team evaluating Kernel should determine which path their workload actually hits. Workloads with predictable concurrency that fit within a pre-provisioned pool will see warm-pool latencies. Workloads with sudden burst traffic that exhausts the pool, or one-off invocations with no prior warm state, will hit the cold-start path. The architecture supports both, and the warm-pool size is configurable -- but the two numbers should not be averaged or treated as interchangeable in capacity planning.

---

### Session and Resource Model

Kernel's resource model is directly shaped by its unikernel architecture and is worth treating as a coherent system rather than a list of independent features.

**Session duration:** Documented support for sessions up to 72 hours. Browserbase documents approximately 6 hours. For agents that must maintain persistent browser state across long-running tasks -- authenticated sessions, multi-step workflows, stateful scraping -- this is a structural advantage rather than a tuning parameter.

**Pause and resume:** Sessions can be paused and resumed with a live view of the session state. A paused session holds its browser state without consuming full active-session compute.

**Standby mode:** An idle browser instance can be placed on standby -- kept alive cheaply -- rather than torn down entirely. Resuming from standby is fast because no boot is required. This is distinct from a cold start and distinct from a fully active session. The three states (active, standby, terminated) map to three distinct cost and latency profiles, giving operators fine-grained control over the trade-off between resume latency and idle cost.

**Billing model:**

| Dimension | Kernel |
|---|---|
| Billing granularity | Per-second |
| Idle surcharge | None |
| Proxy surcharge | None (built-in; no separate line item) |
| Free tier | Generous (see current pricing page for current limits) |
| GPU | Optional; available on sandboxed Chromium instances |

Per-second billing with no idle surcharge is particularly consequential for bursty agent workloads -- see [[#Why the Architecture Matters for Agents]] below.

**Reserved browser pools:** Configurable pools of pre-warmed browser instances. These are the mechanism behind the < 30 ms warm spin-up figure. Pools also serve as a scaling primitive: provisioning a pool ahead of a known traffic spike ensures warm-pool hits rather than cold starts during the burst.

---

### Deployment Topology

Kernel exposes two deployment modes that correspond to different stages of the development and production lifecycle.

**Development -- `kernel create`:** The CLI command `kernel create` spins up a single browser instance on demand. This is the interactive, iterative path for building and debugging agent logic.

**Production -- `kernel deploy`:** The `kernel deploy` command deploys a serverless application platform that hosts the agent's own loop code. Critically, this platform runs **co-located** with the browser infrastructure -- agent logic and the browser it drives execute in the same network environment.

Co-location is architecturally significant. Every Playwright command, every CDP (Chrome DevTools Protocol) message, and every browser interaction is a network round-trip. In a conventional setup where the agent process runs on the developer's infrastructure and the browser runs in a cloud provider's data center, each of those round-trips crosses the public internet or at minimum a wide-area network path. At high interaction density -- hundreds of commands per session -- this latency accumulates. Co-locating agent logic and browser eliminates that path, collapsing network latency to intra-data-center levels. `kernel deploy` also supports on-demand invocation and scheduled execution, making it suitable for both event-driven agent pipelines and periodic automation.

---

### Why the Architecture Matters for Agents

The design choices above form a coherent whole when examined against the actual traffic shape of AI agent workloads.

Agent-driven browser usage is characteristically **bursty and short-lived**. An agent fleet may need zero browsers for minutes, then need fifty simultaneously, then drop back to near-zero. Individual sessions may be brief -- a task completes, the browser is discarded. Or sessions may be long and stateful -- a research or workflow agent that must hold authenticated context for hours.

This traffic shape is the worst-case scenario for platforms optimized around conventional web-scraping or RPA workloads:

- **Slow cold starts** (3-5 seconds) introduce per-session latency that dominates short tasks and degrades burst responsiveness.
- **Idle-time billing** penalizes the gap between task end and the next task arrival -- unavoidable in bursty workloads unless every browser is torn down immediately (which then incurs cold-start cost on the next burst).
- **Session duration caps** force architectural workarounds for long-running agents.
- **Network-separated agent and browser** multiplies latency across every interaction.

The Kernel architecture addresses each of these directly:

| Agent workload problem | Kernel mechanism |
|---|---|
| Slow cold starts on burst | Unikernel boot (sub-300 ms) + reserved warm pools (< 30 ms) |
| Idle billing between tasks | Standby mode + per-second billing with no idle surcharge |
| Short-session overhead | Low per-session cost; no minimum billing unit beyond per-second |
| Long-running stateful sessions | 72-hour session limit; pause/resume |
| Interaction latency | Co-located agent + browser via `kernel deploy` |

The substantive version of Kernel's "built for agents" claim is this: the unikernel architecture, the warm-pool model, the standby primitive, the per-second billing, and the co-located deployment platform are all design choices that specifically address the failure modes of conventional cloud browser infrastructure when subjected to agent-shaped traffic. The performance numbers are a consequence of architectural fit, not incidental optimization.
