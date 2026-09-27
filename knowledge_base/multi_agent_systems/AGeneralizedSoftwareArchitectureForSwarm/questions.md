---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: A Generalized Software Architecture for Swarm

### Q1. Why does the paper reject centralized orchestrator–worker topologies, and what does it propose instead?

> [!tip]- Answer
> Centralized orchestrators are diagnosed as a single point of failure, a throughput bottleneck as swarm size grows, and a carrier of task-specific assumptions that hurt generalization. The paper proposes a fully decentralized swarm where peer agents coordinate through local interactions and collective capacity is a function of protocol design rather than central control. See [[wiki/01-generalized-swarm-architecture-overview|Generalized Swarm Architecture Overview]].

### Q2. What are the three logical planes of the swarm and the five design principles behind them?

> [!tip]- Answer
> The task plane governs the sub-task lifecycle (decomposition, advertisement, bidding, execution, result integration), the state plane holds eventually consistent shared context and dependencies, and the membership plane tracks composition and reallocates work on join, departure, or failure. The five principles are locality of decision, protocol–semantics separation, redundancy by default, graceful degradation, and composable primitives built from standard distributed-systems mechanisms. See [[wiki/01-generalized-swarm-architecture-overview|Generalized Swarm Architecture Overview]].

### Q3. How is a sub-task represented as a tuple, and how does recursive decomposition with capability-aware bidding work?

> [!tip]- Answer
> Each sub-task is `t = ⟨id_t, ρ_t, δ_t, π_t, σ_t⟩`, where ρ_t is the required capability descriptor, δ_t the dependency identifiers, π_t the acceptance predicate, and σ_t the status. A goal G is first held by a temporary root holder that applies decomposition D into a DAG of sub-tasks, and any assignee may recursively decompose further so tractable work pipelines early. Pending sub-tasks are announced to the overlay neighborhood and awarded from bids `b_i,t` scored by utility `u_i,t = α·cap(C_i, ρ_t) + β·(1 − L_i) + γ·κ_i` with tempered greedy/softmax selection. See [[wiki/02-system-model-task-representation|System Model: Task Representation, Network, and Membership]].

### Q4. How does the swarm keep shared state consistent without a central node, and when does it use strong consensus?

> [!tip]- Answer
> Shared state S = {task DAG T, result store R, membership view M} is encoded as CRDTs (OR-Set + LWW register for T, G-Map for R, delta-state CRDT for M) and spread by anti-entropy gossip with fixed fan-out each interval τ, converging in O(log n) rounds with vector clocks bounding staleness. Redundant work is avoided by checking the local σ_t assignment plus deterministic-ID conflict resolution after merges. Stronger linearizability via an ephemeral on-demand Raft-style quorum is reserved only for irreversible commitments such as goal completion. See [[wiki/02-system-model-task-representation|System Model: Task Representation, Network, and Membership]].

### Q5. How do the coordination and reasoning layers (and the five internal agent components) preserve task-agnosticism?

> [!tip]- Answer
> Layer 4 (coordination) implements allocation, membership, failure detection, and on-demand consensus with interfaces for goal submission, announcement, bidding, award, and result publication, while layer 5 (reasoning) holds the decomposition function, capability evaluation, execution, and acceptance-predicate checks and talks only through those interfaces. Inside each agent, a coordination client, bidding engine, task executor, state observer, and health monitor mirror this split. Because domain semantics never leak downward and the reasoning layer is insulated from the network, the same substrate hosts research, code synthesis, or document analysis unchanged. See [[wiki/03-decentralized-state-synchronization|Layers, Lifecycle, Analysis, Discussion and Conclusion]].

### Q6. What scalability, consistency, and fault-tolerance guarantees does the architecture claim?

> [!tip]- Answer
> Per-agent overhead stays sub-linear into the thousands: overlay routing O(log n), gossip O(log n) rounds with constant per-agent cost, CRDT merge O(|Δ|) bounded by recent activity, and allocation O(k) solicited bidders independent of n. Routine state is eventually consistent with staleness bounded by gossip period and fan-out, while critical commits get linearizability via lightweight consensus. The swarm tolerates any minority failure in the consensus quorum and broader failures while the overlay stays connected, reassigning orphans to PENDING (instantly via shadow agents) and reconciling partitions through CRDT merge plus deterministic resolution. See [[wiki/03-decentralized-state-synchronization|Layers, Lifecycle, Analysis, Discussion and Conclusion]].

### Q7. (Evaluation) Your team must coordinate hundreds of heterogeneous LLM agents across research and code tasks with frequent churn and partitions — should you adopt this architecture, and what caveats demand attention first?

> [!tip]- Answer
> Yes, recommend it when you need one reusable, partition-tolerant substrate without a central scheduler, since only the reasoning layer changes per domain and progress degrades gracefully under churn. Before committing, weigh the stated limits — non-Byzantine baseline, scalar capability utility, no economic incentives — plus the open gaps in learned decomposition quality, gossip/bidding tuning, and missing large-scale empirical validation, so plan a simulation pilot reusing existing overlay, CRDT, and Raft libraries. See [[wiki/03-decentralized-state-synchronization|Layers, Lifecycle, Analysis, Discussion and Conclusion]].
