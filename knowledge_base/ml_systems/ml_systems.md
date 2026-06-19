# ML Systems & Serving

Research on **ML infrastructure** — model serving, request routing, deployment patterns, traffic management, and production system design for large-scale ML.

## Papers

- [[EfficientLLMInference/summary]] — Full-stack reference on LLM inference optimization: GPU memory-bandwidth bottleneck, KV cache mechanics, quantization, speculative decoding, FlashAttention, and production serving (vLLM, continuous batching).
- [[EfficientRetrievalScalingHILL/summary]] — Jointly trains a hierarchical tree index with a retrieval model via residual quantization for fast beam-search; +2.57% ads gain at Meta at 3.9x vs. 24.6x infra cost.
- [[StateOfRoutingInModelServing/summary]] — Netflix replaced Switchboard (centralized routing proxy) with Lightbulb (metadata sidecar + Envoy) to eliminate 10–20ms latency and SPOF while preserving A/B and canary abstractions at 1M+ RPS.
