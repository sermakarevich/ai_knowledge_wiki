> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Competitive Landscape

### Market Context

"Cloud browser infrastructure for AI agents" has become a crowded, fast-moving category in 2024--2025. The core value proposition across all players is the same: provide managed, scalable, stealth-capable browser sessions that AI agents can drive remotely via CDP or Playwright, without the operator needing to manage browser infrastructure. Feature parity across the category is high -- stealth fingerprinting, residential proxies, CAPTCHA solving, session recording, and multi-protocol control exist at most competitors. This means differentiation increasingly falls on performance, cost, and architectural choices rather than feature novelty alone.

Kernel (kernel.sh / onkernel.com) is a newer entrant that raised a $22M Series A (SiliconAngle, October 2025) and explicitly targets the incumbent Browserbase as its primary benchmark. Its claimed edge is rooted in a unikernel architecture (see [[sections/architecture-and-performance]]) that allows sub-300ms cold starts and per-second billing without idle surcharges.

---

### Key Competitors

#### Browserbase

Browserbase is the incumbent and market leader. It is the category-defining managed cloud browser platform and the benchmark Kernel explicitly competes against. Its architecture is container-based, which imposes cold-start latency in the seconds range. Session length caps are documented at approximately 6 hours. It is the most widely deployed option in the ecosystem, with broad framework integrations and a mature developer experience.

#### Steel.dev

Steel.dev is a direct competitor to Kernel. Steel publishes a "Steel vs Kernel" comparison on its own blog -- this is an explicitly biased, competitor-sourced document and must be read accordingly. Steel's blog characterizes Kernel as a closed-source, managed-only platform with no self-hosting option (addressed in detail in the [[#Open-Source Discrepancy]] section below). Steel positions itself as open source and self-hostable as a primary differentiator against Kernel.

#### Hyperbrowser

Hyperbrowser is a direct competitor. Kernel publishes a "Kernel vs Hyperbrowser" comparison on its own blog -- this is an explicitly biased, vendor-sourced document. Detailed technical or pricing specifics about Hyperbrowser's architecture are not established from neutral sources in this analysis.

#### Skyvern

Skyvern is an adjacent player -- primarily an AI web-automation agent platform rather than pure browser infrastructure. Skyvern publishes a "Browserbase vs Kernel" comparison on its blog, providing a somewhat more neutral third-party perspective. It is not a direct infrastructure competitor to Kernel in the same way Browserbase and Steel are.

---

### Kernel's Claimed Performance and Cost Advantages

The following figures come from vendor-published benchmarks (Kernel's own blog at kernel.sh/blog/fast) and competitor-sourced comparisons. They are not independently verified and are workload-dependent. A prospective adopter should reproduce these numbers on their own session mix before relying on them for infrastructure decisions.

| Metric | Kernel (vendor claim) | Browserbase (vendor/third-party benchmark) |
|---|---|---|
| Cold start latency | Sub-300--325 ms | Seconds (container startup) |
| Cold start speedup | ~5.8x faster | Baseline |
| End-to-end speedup | ~3.7x faster | Baseline |
| Cost | 50%+ lower | Baseline |
| Max session length | Up to 72 hours | ~6 hours |
| Billing model | Per-second, no idle/proxy surcharges | Not established here |

Root cause of the performance edge: unikernel-based session isolation allows near-instant boot because there is no container or VM runtime to initialize. See [[sections/architecture-and-performance]] for a full treatment.

---

### Comparison Table

The table below compares Kernel against its primary competitors across the dimensions most relevant for AI agent infrastructure decisions. Cells marked "not established here" reflect a deliberate choice not to fabricate specifics from sources unavailable to this analysis. Competitor figures come only from the sources cited.

| Dimension | Kernel | Browserbase | Steel.dev | Hyperbrowser |
|---|---|---|---|---|
| **Architecture** | Unikernel-based session isolation | Container-based | Not established here | Not established here |
| **Cold start** | Sub-300--325 ms (vendor claim) | Seconds -- container startup (vendor/competitor benchmark) | Not established here | Not established here |
| **Max session length** | Up to 72 hours (vendor claim) | ~6 hours (vendor/competitor benchmark) | Not established here | Not established here |
| **Control protocols** | CDP, Playwright (vendor docs) | CDP, Playwright (established, incumbent) | Not established here | Not established here |
| **Stealth / proxies** | Stealth fingerprinting, residential proxies (vendor docs) | Stealth, residential proxies (established) | Not established here | Not established here |
| **CAPTCHA solving** | Yes (vendor docs) | Yes (established) | Not established here | Not established here |
| **Observability / recording** | Session recording, live view (vendor docs) | Session recording, live view (established) | Not established here | Not established here |
| **Serverless agent-loop deploy** | Yes -- `kernel deploy` co-locates agent logic with browser (vendor docs) | Not established here | Not established here | Not established here |
| **Billing model** | Per-second, no idle or proxy surcharges (vendor claim) | Not established here | Not established here | Not established here |
| **Open source posture** | Claimed: open-sourced browser image + open SDKs (vendor docs); CONTESTED -- see below | Not established here | Self-described as open source and self-hostable (Steel blog) | Not established here |
| **Self-hosting** | Claimed possible per vendor docs; CONTESTED by Steel.dev -- see below | Not established here | Self-described (Steel blog) | Not established here |
| **Maturity / market position** | Newer entrant, $22M Series A (Oct 2025) | Incumbent, market leader | Direct competitor | Direct competitor |

---

### Open-Source Discrepancy

**This is the key unresolved point in the competitive picture and deserves explicit attention from any prospective adopter who cares about self-hosting, auditability, or regulated-industry compliance.**

Two directly contradictory claims exist:

**Claim A -- Kernel's own documentation and marketing:** Kernel positions itself as "open source infrastructure." Specifically, it describes an open-sourced browser image and open SDKs, and markets this openness as meaningful for regulated industries that need to self-host or audit the stack.

**Claim B -- Steel.dev's competitor blog ("Steel vs Kernel"):** Steel characterizes Kernel as closed-source and managed-only, with no self-hosting option available to users.

These claims cannot both be true in their strong forms. The tension is real and unresolved.

**How to weight the sources:** Steel.dev is a direct commercial competitor with a financial incentive to portray Kernel negatively on exactly the dimension where Steel claims an advantage. Its blog post should be discounted -- but not dismissed -- as a result. Vendor marketing, conversely, has an incentive to overstate openness. Neither source is neutral.

**Honest resolution:** This discrepancy is **unresolved** pending direct inspection of Kernel's public GitHub repositories and the licenses attached to each component. Possible reconciling explanations include: the browser image is open source but the orchestration layer or session management plane is not; or the SDKs are open but the backend is proprietary; or "open source" is being used loosely to mean "published" rather than "freely self-hostable." Any of these would make both claims technically defensible while being materially misleading to a buyer.

**Recommendation for prospective adopters:** If self-hosting, source auditability, or regulated-industry compliance is a requirement, do not rely on vendor marketing or competitor commentary. Inspect Kernel's public GitHub repositories directly, verify the licenses on each repo, and determine whether the orchestration components -- not just the browser image -- are available for self-deployment before committing to Kernel on this basis.

---

### Differentiation Analysis

The honest competitive take is that Kernel's differentiation is **not** a unique feature list. Feature parity across the category is high: stealth, residential proxies, CAPTCHA solving, observability/recording, and multi-protocol control (Playwright/CDP) are available at Browserbase, Steel, and likely other competitors. A buyer who only needs these table-stakes features has multiple viable options.

Kernel's defensible differentiation comes from two sources:

**1. Performance and cost from the unikernel architecture.** If the vendor benchmarks hold under a buyer's workload, sub-300ms cold starts and 50%+ cost reduction are meaningful advantages for high-volume, latency-sensitive agent pipelines. This is an architectural advantage -- not a feature that can be quickly copied -- because it requires rearchitecting session isolation from the ground up. The caveat: benchmarks are vendor- and competitor-sourced. An adopter should run their own session mix before treating these numbers as guaranteed.

**2. The `kernel deploy` serverless agent-loop platform.** Kernel offers the ability to deploy the agent's own logic (not just the browser) as a serverless function co-located with the browser session. This removes the network round-trip between the agent's compute and the browser, and collapses infrastructure management for both layers. Not all competitors in the category offer this -- it positions Kernel as a platform for agent deployment, not only browser provisioning. This is the more strategically interesting differentiator because it increases switching costs and expands the value delivered beyond raw browser infrastructure.

The open-source posture (if verified) could constitute a third differentiator for regulated industries, but as noted above, this is contested and unverified.

---

### Sources

- https://siliconangle.com/2025/10/09/ -- Kernel $22M Series A coverage
- https://onkernel.com/blog/kernel-vs-hyperbrowser -- Kernel vs Hyperbrowser (vendor-authored, biased)
- https://kernel.sh/blog/fast -- Kernel performance benchmark post (vendor-authored)
- https://steel.dev/blog/steel-vs-kernel -- Steel vs Kernel (competitor-authored, biased)
- https://skyvern.com/blog/browserbase-vs-kernel-which-is-better/ -- Browserbase vs Kernel (Skyvern blog, adjacent third party)
- https://github.com/browserbase/mcp-server-browserbase/issues/127 -- Community discussion reference
