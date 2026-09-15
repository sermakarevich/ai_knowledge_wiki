> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The three-layer measurement model

**In one sentence:** Lau measures AI transformation in three layers — adoption first, then throughput and process efficiency, then business outcomes — held together by systems thinking that treats the product development life cycle (PDLC) as one flow where a local speedup without pipeline telemetry merely moves the bottleneck.

## Key points

- Layer one is adoption, on the logic that if people are not using the tools transformation cannot happen, tracked both quantitatively and qualitatively.
- Layer two is throughput and process efficiency, using metrics such as pull-request rate, cycle time, and latency, which Lau admits are not perfect but provide a systems-level view.
- Layer three is outcomes, meaning whether business objectives are met, exemplified by road map progress, defect rates, and customer impact.
- The governing metaphor is systems thinking: the PDLC is a flow, so accelerating one stage such as coding while review or compliance lags means the organization has not truly improved.
- Telemetry across the whole pipeline is essential precisely to reveal where bottlenecks appear so they can eventually be fixed, rather than assuming coding speed equals delivery speed.
- Faster coding actively shifts bottlenecks elsewhere — requirements definition, testing, and governance are named — so without holistic change, gains at one point create friction downstream.

---

## Why adoption comes first

Adoption is the gate rather than just a metric: no usage, no transformation, and usage must be tracked quantitatively and qualitatively together. The qualitative half matters because raw activation counts cannot distinguish genuine workflow integration from superficial trial, a distinction the depth finding on the previous page makes economically decisive.

## Throughput metrics with a caveat

Pull-request rate, cycle time, and latency are Lau's chosen process metrics, offered with an explicit imperfection disclaimer. Their value is the systems-level view: they measure flow through the pipeline rather than individual output, which makes them harder to game in isolation and more sensitive to the bottleneck-shifting the model warns about.

## Outcomes as the final arbiter

Road map progress, defect rates, and customer impact move judgment from engineering activity to business objectives actually met. This layer answers the executive question behind the interview — how companies ensure AI is actually effective — by refusing to let faster coding stand in for delivered value.

## Systems thinking and the shifting bottleneck

The passage's core mechanism is conservation of constraint: the PDLC is a single flow, so a coding speedup that outruns review or compliance leaves total throughput unchanged. Telemetry across the pipeline is the instrument that makes the new constraint visible, whether it lands in requirements definition, testing, or governance. The warning is directional — without holistic change, local gains create downstream friction — which turns measurement from scorekeeping into the guide for where to intervene next.

**Covers:** the adoption / throughput-and-efficiency / outcomes layers with their example metrics, the systems-thinking framing, pipeline telemetry, and the bottleneck-shifting mechanism with its three named landing zones.
