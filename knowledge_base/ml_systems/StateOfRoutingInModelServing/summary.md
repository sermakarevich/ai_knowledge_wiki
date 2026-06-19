# State of Routing in Model Serving

**Paper:** [State of Routing in Model Serving (Nipun Kumar, Rajat Shah, Peter Chng, 2026)](https://netflixtechblog.com/state-of-routing-in-model-serving-16e22fe18741)

## Human Readable TL;DR

Imagine a massive phone switchboard operator whose job is to connect callers to the right department. At Netflix, every personalized recommendation you see is powered by an ML model, and "getting you to the right model" is surprisingly hard at scale. This post explains how Netflix built a smart traffic director called Switchboard that routes every ML request to the correct model version -- and then how they replaced it with a leaner system called Lightbulb when Switchboard became a bottleneck. Instead of one centralized operator handling every call, Lightbulb just whispers the routing instructions into each caller's ear and lets them connect directly.

## TL;DR

Netflix's ML serving platform handles 1M+ requests/second across hundreds of model types. They built **Switchboard** -- a centralized context-aware routing proxy that decoupled clients from model sharding, enabled A/B experimentation, and supported canary deployments. At scale, Switchboard introduced 10--20ms latency overhead and became a single point of failure. They evolved to **Lightbulb**: a lightweight metadata-resolution sidecar that pushes routing config to clients and delegates actual request routing to Envoy, eliminating the centralized hop while preserving all abstraction benefits.

---

## Problem & Motivation

ML models at Netflix are self-contained workflows (not just scorers): they encapsulate pre/post-processing, feature computation, and optional trained components. Clients only provide request context (userId, country, device) and domain context (titles to rank, payment details). The platform must:

1. Route each request to the correct model version based on A/B allocation
2. Isolate clients from frequent VIP address changes as models shift between cluster shards
3. Support shadow testing, canary rollouts, and instant rollbacks without client code changes

Standard API gateways (AWS API Gateway, service mesh proxies) lacked first-class A/B experimentation integration, gRPC support, and rich domain-context routing.

---

## Main Original Ideas

1. **Objective Abstraction** -- Each business use case (e.g., `ContinueWatchingRanking`) is assigned an `Objective` enum. Clients address requests to an Objective, never to a concrete model ID. This single contract enables model iteration to be fully opaque to calling services.

2. **Switchboard: Centralized Context-Aware Router** -- A custom proxy handling 1M+ RPS that translates Objective + request context → model selection + cluster VIP routing. Integrates with Netflix's experimentation platform for A/B cell allocation and supports shadow mode, canary splits, and instant rollback.

3. **Switchboard Rules (JavaScript DSL)** -- Researchers define routing logic as JavaScript configs that compile to JSON rules. Rules specify default models, A/B experiment → model mappings, and traffic-shift percentages. Published via Netflix's Gutenberg pub-sub system with independent versioning from code deployments.

4. **Lightbulb: Decoupled Routing Metadata Service** -- Separates routing concerns from the request path. Lightbulb resolves request context to a `routingKey` (placed in HTTP headers) and an `ObjectiveConfig` (injected into the request body). Envoy reads the `routingKey` header to select the target VIP -- no large payload deserialization required.

5. **Control Plane / Data Plane Separation** -- The control plane handles model-to-shard assignment, validation, and VIP mapping. The data plane (Envoy + Lightbulb) handles per-request routing without touching the payload body, removing serialization overhead.

---

## Key Findings

| Issue with Switchboard | Impact | Lightbulb Solution |
|---|---|---|
| Single point of failure in request path | Full platform outage risk | Moved routing metadata out of request path; Envoy does actual routing |
| 10--20ms latency from payload deserialization | Unacceptable for latency-sensitive clients | `routingKey` in header only; payload untouched |
| Noisy neighbor / tenant isolation | Error cascades across use cases | Per-tenant isolation via Envoy routing rules |
| Client origin visibility lost | Training data contamination | Clients connect directly to clusters; origin preserved |

**Scale:** 1M requests/second, hundreds of model types and versions, 30+ service clients, as of 2025.

---

## Suggestions & Future Directions

1. Future posts in the series will cover **inference and feature fetching** in depth and how they interact with the routing architecture.
2. The Lightbulb architecture is positioned to support further ML growth -- implication is continued investment in control plane tooling for fast experimentation config propagation and client-side caching/fallback.

---

## Authors & Institutions

Nipun Kumar (Netflix), Rajat Shah (Netflix), Peter Chng (Netflix)
