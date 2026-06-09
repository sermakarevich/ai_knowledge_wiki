# Usable Agent Discovery for Decentralized AI Systems

**Paper:** [Usable Agent Discovery for Decentralized AI Systems (Dazzi, Carlini, Mordacchini, Urso, 2026)](https://arxiv.org/abs/2604.23080)

## Human Readable TL;DR

Imagine a city where taxis (AI agents) can be on duty, on a break, or off-shift, and streets (network nodes) randomly close. When you call a taxi, you need to find one AND have it ready to drive -- not just located. This paper studies two different ways of organizing the city's dispatch system (a structured directory vs. word-of-mouth gossip), and figures out which handles streets closing vs. drivers going on break better. The key insight is that "finding" an agent and "using" an agent are two different problems that require different solutions.

## TL;DR

This paper analyzes agent discovery in large-scale distributed AI systems under a two-level churn model -- node failures and agent state transitions (warm/cold). It compares structured overlays (Kademlia DHT) against gossip-based approaches (Cyclon+Vicinity) across four operational regimes, using a new "useful availability" metric (U_Δ) that captures whether a discovered route yields a ready service within a deadline. Kademlia dominates in stable and node-churn regimes, while gossip-based systems compete when agent-level cooling drives cold-start latency overhead.

---

## Problem & Motivation

Large-scale decentralized AI systems (e.g., multi-agent networks) require agents to discover each other at runtime. Existing discovery work focuses on routing correctness but ignores that agents can be warm, cold, or off -- meaning a "successful" route may still fail to deliver a service within a useful time budget. Real deployments face simultaneous disruptions at two levels: physical nodes leaving/failing, and agents suspending (cooling) independently of host availability. No prior work systematically separates these two churn axes or captures the end-to-end cost of cold starts in discovery quality metrics.

---

## Main Original Ideas

1. **Two-level churn model** -- Separates node-level churn (hosts joining/leaving) from agent-level churn (warm/cold/off state transitions). Each axis can be varied independently, yielding four distinct operating regimes for rigorous comparison.

2. **Useful availability metric (U_Δ)** -- A latency-deadline-aware metric defined as: did the discovered route deliver a ready service within deadline Δ? Decomposes end-to-end latency into L_disc (discovery) + L_route (routing) + L_start (cold-start warmup), exposing which term dominates under each regime.

3. **Empirical regime map** -- Systematic comparison of structured (Kademlia) vs. gossip (Cyclon+Vicinity) overlay families across stable, node-churn, cooling, and combined disruption regimes, revealing that no single overlay dominates across all conditions.

4. **Staleness diagnostics** -- Distinguishes stale routing entries from stale host-belief entries as separate failure modes, finding that Kademlia's fragility under combined churn stems primarily from routing-table staleness rather than host-belief errors.

---

## Key Findings

| Regime | Kademlia | Gossip (Cyclon+Vicinity) |
|--------|----------|--------------------------|
| Stable (E1) | **Lower p95 latency, higher success** | Competitive, higher maintenance overhead |
| Node-churn (E2) | **More robust, better U_Δ** | Falls behind; routing degrades faster |
| Agent cooling (E3) | Success advantage compresses | **Competitive**; cold-start dominates both |
| Combined (E4) | Fragile under routing pressure | Neither clearly wins |

- Kademlia background maintenance (index publication + refresh) is substantially cheaper than dense gossip, which costs ~10x more overhead for little latency gain
- Under aggressive cooling, U_Δ drops sharply for Kademlia because cold-start latency erases the routing advantage
- Semantic sparsity (highly specialized skills) only matters at the extremes -- moderately broad skill catalogs see near-full success for both families
- Combined-churn failures are mostly stale-routing driven, not stale-host-belief driven

---

## Suggestions & Future Directions

1. **Hybrid overlays** -- Use structured lookup during stable periods but fall back to unstructured gossip repair when routing tables decay; neither family alone is optimal across all regimes.

2. **Request-aware lifecycle management** -- Align agent warm/cold state with overlay health and predicted demand, turning U_Δ from a passive diagnostic into an active control signal for preemptive warming.

3. **Broader network topologies** -- Current experiments use Erdős–Rényi substrate with zero packet loss; real-world heterogeneous topologies and lossy links need evaluation.

4. **Analytical models** -- The empirical regime map suggests tractable analytical bounds are possible; deriving closed-form transitions between regimes would strengthen theoretical foundations.

---

## Authors & Institutions

Patrizio Dazzi, Emanuele Carlini, Matteo Mordacchini, Saul Urso -- ISTI-CNR (Institute of Information Science and Technologies, National Research Council of Italy)
