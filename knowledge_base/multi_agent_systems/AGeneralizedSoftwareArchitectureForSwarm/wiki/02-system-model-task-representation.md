> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# System Model: Task Representation, Network, and Membership
**In one sentence:** The swarm models each sub-task as a tuple `t = ⟨id_t, ρ_t, δ_t, π_t, σ_t⟩` in a shared DAG and executes it over an asynchronous, partially synchronous peer-to-peer network with dynamic membership via recursive decomposition, capability-aware bidding, CRDT-gossip state sync, and gossip-based fault recovery.
## Key points
- Each sub-task is `t = ⟨id_t, ρ_t, δ_t, π_t, σ_t⟩` (Eq. 2), where ρ_t is the required capability descriptor, δ_t is dependency identifiers, π_t is the acceptance predicate, and σ_t is status.
- The network is asynchronous, partially synchronous with delayed, reordered, or dropped (but not corrupted) messages under a non-Byzantine baseline, using a structured peer-to-peer overlay with logarithmic-cost lookup.
- Membership is dynamic with join/departure at any time; failures are silent departures detected via heartbeat timeouts, and later via a SWIM-style probe + gossip + indirect-probe protocol committed to M.
- Goals decompose recursively via `D : G ↦ {t1, ..., tm}` held first by a temporary root holder, inserted as a DAG into the shared state, allowing pipelined progress on tractable sub-tasks.
- Bidding uses `b_i,t = ⟨id_i, u_i,t, e_i,t⟩` (Eq. 3) with utility `u_i,t = α·cap(C_i, ρ_t) + β·(1 − L_i) + γ·κ_i` (Eq. 4), α+β+γ=1, cap in [0,1], awarded after a bounded window with 1−ϵ greedy / ϵ softmax-over-top-k tempering plus deterministic-ID tie-breaking.
- Shared state S = {task DAG T, result store R, membership view M} uses CRDTs (OR-Set + LWW register for T, G-Map for R, delta-state CRDT for M) disseminated by anti-entropy gossip with fan-out each interval τ converging in O(log n) rounds, with vector clocks for staleness.
- Redundant work is avoided by checking σ_t assignment pre-execution plus deterministic conflict resolution, while goal-completion commits use ephemeral on-demand Raft-style quorum consensus; failed agents' orphans return to PENDING with optional bounded shadow agents for fast failover.
---
## Task tuple (Eq. 2)
**Covers:** Sec. IV-B tail – task representation

| Field | Meaning (verbatim / paraphrase from chunk) |
|---|---|
| `id_t` | task identifier |
| `ρ_t` | "the required capability descriptor" |
| `δ_t` | "the set of dependency identifiers" |
| `π_t` | "specifies the acceptance predicate (the conditions under which a result is considered valid)" |
| `σ_t` | status (values seen in chunk: PENDING, ASSIGNED, BIDDING, EXECUTING, COMPLETED) |

> Verbatim: "t = ⟨id_t, ρ_t, δ_t, π_t, σ_t⟩, (2)"

## Network model
**Covers:** Sec. IV-C, Network Model

- "The swarm is assumed to operate over an asynchronous, partially synchronous network in which messages may be delayed, reordered, or dropped, but are not arbitrarily corrupted (a non-Byzantine failure model is adopted in the baseline; Byzantine extensions are discussed in Section VII)."
- "Agents are connected via a structured peer-to-peer overlay that supports logarithmic-cost lookup and neighborhood maintenance."
- "The membership of A is dynamic: agents may join or depart at any time, and failures are modeled as silent departures detected through heartbeat timeouts."

## Dynamic task decomposition and allocation
**Covers:** Sec. IV-C, Dynamic Task Decomposition and Allocation (1–3)

### 1) Recursive Decomposition
- "When a goal G is admitted to the swarm, it is initially held by an arbitrary agent a_i designated as its temporary root holder—an assignment that confers no special authority beyond responsibility for initiating decomposition."
- "The root holder applies a domain-appropriate decomposition function D : G ↦ {t1, ..., tm} implemented within its reasoning module."
- "The resulting sub-tasks, together with their dependency edges, are inserted into the shared task DAG and propagated through the state plane."
- "Decomposition is recursive: any sub-task t may itself be further decomposed by the agent to which it is eventually assigned, producing a hierarchy of refinements."
- Effect: "permits the swarm to begin work on tractable sub-tasks while more abstract sub-tasks are still being broken down, supporting pipelined progress."

### 2) Capability-Aware Bidding
- "For each sub-task t entering status PENDING, the holder publishes a task announcement to the overlay neighborhood relevant to ρ_t, exploiting the structured topology to direct announcements toward agents whose capability profiles are likely matches."
- Bid form (Eq. 3): `b_i,t = ⟨id_i, u_i,t, e_i,t⟩,` "where u_i,t is the agent's self-estimated utility for executing t and e_i,t is its estimated time-to-completion."
- Utility (Eq. 4): `u_i,t = α · cap(C_i, ρ_t) + β · (1 − L_i) + γ · κ_i,` "where cap(·, ·) is a capability-match score in [0, 1], and α, β, γ are tunable weights satisfying α + β + γ = 1."
- "The functional form of cap(·, ·) is task-agnostic at the protocol level: it operates on opaque descriptors interpreted by agent reasoning modules."

### 3) Award and Conflict Resolution
- "After a bounded bidding window, the holder selects the highest-utility bidder."
- Tempered selection: "with probability 1 − ϵ, the highest-utility bidder is selected; with probability ϵ, selection is performed by softmax sampling over the top-k bids" — to "avoid pathological concentration of work and to mitigate adversarial bidding."
- "Ties and conflicting concurrent awards are resolved using deterministic agent identifiers, ensuring that even in the presence of message reordering, the swarm converges to a unique assignment for each sub-task."
- Critical tasks: "redundant assignment is permitted: the top-r bidders execute the sub-task in parallel, and results are reconciled by the acceptance predicate π_t. This trades computational cost for resilience and is configurable on a per-task basis."

## Decentralized state synchronization
**Covers:** Sec. IV-D, Decentralized State Synchronization (1–4)

### 1) Shared State Schema
- "The shared state S maintained across the swarm comprises three principal structures:"
  - "The task DAG T, encoding sub-tasks, dependencies, and statuses."
  - "The result store R, mapping completed sub-task identifiers to their outputs."
  - "The membership view M, listing currently known agents and their capability profiles."
- CRDT encoding: "T employs an OR-Set for vertex membership combined with a last-writer-wins register for status fields; R uses a grow-only map (G-Map) since results, once written, are immutable; M uses a delta-state CRDT to bound metadata overhead under churn."

### 2) Gossip Dissemination
- "State updates are propagated via an anti-entropy gossip protocol. At each gossip interval τ, an agent selects a fixed-fan-out subset of overlay neighbors and exchanges CRDT delta states."
- "Under standard assumptions, gossip dissemination converges in O(log n) rounds with high probability, providing bounded staleness without central coordination."
- "Each agent maintains a vector clock that is used to detect concurrent updates and to bound the age of locally observed state, enabling agents to defer decisions when their view is detected to be unacceptably stale."

### 3) Avoiding Redundant Work
- "The combination of CRDT-encoded task statuses and timely gossip dissemination is the primary mechanism by which redundant work is avoided."
- "Before initiating execution, an agent verifies that σ_t is ASSIGNED to itself in its local replica and that no concurrent assignment has been observed within a synchronization window."
- "When concurrent assignments are detected—which may occur transiently under partition—the deterministic conflict-resolution rule of Section IV-C ensures that, post-merge, a single agent retains responsibility, while the others release their claims."

### 4) Selective Strong Consistency
- "Most coordination operates under eventual consistency, which is sufficient for the bulk of task progression."
- "However, certain transitions—most notably the marking of a goal as completed and the release of dependent downstream computations—benefit from stronger guarantees."
- "For these commitment points, the architecture invokes a lightweight Raft-style consensus among a small quorum of agents drawn from the relevant overlay neighborhood. The consensus group is ephemeral, formed on demand, and dissolved after the commitment is recorded in T."

## Scalability and fault tolerance
**Covers:** Sec. IV-E, Scalability and Fault Tolerance (1–3)

### 1) Membership Dynamics
- "A joining agent contacts a small set of bootstrap peers, retrieves the current membership view via gossip, and announces its capability profile."
- "A departing agent issues a graceful-leave message, allowing its outstanding assignments to be released cleanly."
- "Failures are detected by a SWIM-style protocol in which agents periodically probe random peers; suspected failures are gossiped to the swarm and confirmed through indirect probes before being committed to M."

### 2) Reassignment under Failure
- "The swarm identifies orphaned sub-tasks by inspecting the task DAG for entries whose assignee is no longer in the membership view. Each orphan is returned to the bidding pool with its status reset to PENDING, and the allocation protocol of Section IV-C is reinvoked."
- "To bound the reassignment latency, a bounded number of shadow agents may be designated at award time as standby executors; should the primary assignee fail, a shadow agent assumes the assignment without a fresh bidding round."

### 3) Elastic Scaling
- "The swarm may grow without protocol modification: the structured overlay accommodates new agents at logarithmic routing cost, and the gossip and CRDT layers scale gracefully with n."
- "Individual agents may scale their internal computational resources without disrupting the swarm, since capability profiles and load reports are continuously updated through gossip and consumed by the bidding protocol on the next cycle."

## System architecture (start) and invariants (start)
**Covers:** Sec. V-A layered architecture start; Sec. V-D invariants (partial, truncated in chunk)

- "The software architecture is organized into five layers, ordered from network substrate to agent reasoning:"
  - "1) Transport Layer. Handles authenticated, encrypted point-to-point messaging between agents over the underlying transport (e.g., QUIC or TLS-secured TCP). Provides ordered delivery within a single connection and connection multiplexing."
  - "2) Overlay Layer. Implements the structured peer-to-peer topology, providing peer discovery, routing, and neighborhood maintenance. Exposes primitives for unicast, multicast within a neighborhood, and capability-targeted dissemination."
  - "3) State Synchronization Layer. Hosts the CRDT-encoded shared structures and the gossip dissemination engine,"
- Lifecycle fragment in chunk: agents execute assigned tasks "decomposing as needed, and upon completion publish results into R and update σ_t to COMPLETED. Downstream sub-tasks whose dependencies are satisfied transition from PENDING to BIDDING. The cycle continues until the root sub-task of G reaches COMPLETED, at which point an on-demand consensus quorum confirms goal completion and the result is delivered to the original submitter."
- Invariants (truncated — only what chunk contains):
  - "Eventual assignment uniqueness. For every sub-task t, in the absence of further membership changes affecting t, the swarm converges to a state in which exactly one non-failed agent holds the assignment."
  - "Result immutability. Once a sub-task transitions to COMPLETED with a value in R, that value is not subsequently overwritten by the protocol."
  - "Dependency safety. A sub-task does not enter EXECUT-" [truncated in chunk]
