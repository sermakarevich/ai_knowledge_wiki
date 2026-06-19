# Kernel -- Browser Infrastructure for AI Agents

**Paper:** [Kernel Documentation (Kernel / onkernel.com, 2025)](https://www.kernel.sh/docs)
**Deep dive:** [[details]]

## Human Readable TL;DR

When an AI agent needs to "use the web" -- log into a site, click around, fill a form, scrape a dashboard -- it needs a real browser running somewhere in the cloud, not just an API call. Kernel rents you those browsers on demand: you ask for one and it boots in a fraction of a second, already equipped to dodge bot-detection, solve CAPTCHAs, remember logins, and record everything it does so you can watch it like a screen-share. Think of it as the "cloud browser as a utility" -- the same way you rent a server instead of buying a PC, you rent a disposable, fully-loaded Chrome that your agent drives, pay only for the seconds it runs, and never manage the messy plumbing yourself. Kernel's pitch is that it does this faster and cheaper than the incumbents because of an unusual engineering choice (unikernels) that strips the browser's operating system down to almost nothing.

## TL;DR

Kernel is a managed cloud-browser platform purpose-built for AI agents and web automation. It provisions sandboxed Chromium instances (claimed sub-second cold starts, "<30ms" warm spin-up from reserved pools) that agents drive via Playwright, raw CDP, WebDriver BiDi, or computer-use (vision) control, with stealth (CAPTCHA solving + residential proxies), auth/session persistence, and built-in observability (live view, MP4 recording, screenshots) included by default. Beyond raw browsers, it offers a serverless app platform to deploy long-running agent loops co-located with the browser. The core differentiator is a unikernel-based architecture that strips OS overhead to deliver browsers that are materially faster and cheaper than container-based competitors -- third-party and vendor benchmarks cite ~5.8x faster cold starts and ~50% lower cost versus Browserbase. Backed by a $22M Series A (Accel, Oct 2025), YC, and used by Cash App, Framer, and 3,000+ teams.

---

## Problem & Motivation

AI agents increasingly need to operate the live web -- not call clean APIs, but drive a real browser through login walls, JavaScript-heavy SPAs, CAPTCHAs, and stateful multi-step flows. Doing this yourself is a deep infrastructure problem: you must run and scale headless Chromium, keep it from being fingerprinted and blocked, manage cookies/sessions across runs, supply proxies, and observe what the agent actually did when something breaks. Traditional cloud-browser providers solve this with container- or VM-based browsers that are slow to start (often 3-5 seconds cold), expensive to keep warm, and bill for idle time -- a poor fit for agent workloads that spawn many short-lived, bursty browser sessions. Kernel's thesis is that browser infrastructure is the bottleneck for agentic web automation, and that a faster, cheaper, "batteries-included" primitive -- billed per second and deployable serverless -- is what lets agent builders ship instead of babysitting browser fleets.

---

## Main Original Ideas

1. **Unikernel-based cloud browsers** -- Rather than running Chromium inside a full Linux container or VM, Kernel packages each browser as a unikernel: a minimal machine image containing only the OS components the browser actually needs. Stripping the OS surface yields lighter, faster-booting, lower-overhead browsers, which is the root cause of its claimed cold-start and cost advantages over container-based providers.

2. **"Batteries-included" browser primitive** -- A single provisioned browser ships with four capabilities on by default rather than as add-ons: (i) sandboxed Chromium with optional GPU, (ii) auth/credential and session management, (iii) stealth mode (CAPTCHA solving + residential proxies to evade bot detection), and (iv) observability (live view, MP4 recording, screenshots). The agent builder gets anti-blocking and debugging for free instead of stitching together separate services.

3. **Protocol-agnostic control surface (Create / Control / Observe)** -- Kernel organizes its product around three pillars and deliberately does not lock you into one control method. The same browser can be driven by high-level Playwright, raw Chrome DevTools Protocol (CDP), WebDriver BiDi, or computer-use (vision-based) control -- so existing automation code and frontier computer-use agents both work without rewrites.

4. **Serverless agent-loop deployment co-located with the browser** -- Beyond renting browsers, Kernel provides an app platform (`kernel deploy`) to host the agent's own logic serverlessly, running on-demand or scheduled, co-located with the browser to cut network latency. This collapses "where does the agent code run" and "where does the browser run" into one managed surface, with scaling handled via reserved browser pools.

5. **Session persistence and standby for bursty agent workloads** -- Browsers support long sessions (documented up to 72 hours vs. a typical 6-hour ceiling elsewhere), pause/resume with a live view, and a standby mode that idles a browser cheaply instead of tearing it down -- matched with per-second billing and no idle/proxy surcharges. The economic model is explicitly shaped around the spiky, many-short-sessions pattern of agent traffic.

---

## Key Findings

| Aspect | Detail |
|--------|--------|
| **Category** | Managed cloud-browser infrastructure for AI agents / web automation |
| **Warm spin-up (vendor claim)** | "<30ms" from reserved browser pools |
| **Cold start (benchmark)** | sub-300--325ms vs. 3-5s typical container-based |
| **vs. Browserbase (cold start)** | ~5.8x faster (third-party/vendor benchmark) |
| **vs. Browserbase (end-to-end)** | ~3.7x faster |
| **vs. Browserbase (cost)** | 50%+ lower |
| **Max session length** | up to 72 hours (vs. ~6h on Browserbase) |
| **Control protocols** | Playwright, CDP, WebDriver BiDi, computer-use (vision) |
| **Billing** | per-second; no idle or proxy surcharges; generous free tier |
| **Funding** | $22M Series A led by Accel (Oct 2025); YC-backed |
| **Adoption** | Cash App, Framer, 3,000+ teams |
| **Open source** | browser image + SDKs open-sourced (per Kernel) -- see caveat below |

- **Two different "speed" numbers measure different things.** The "<30ms spin-up" figure almost certainly refers to grabbing an already-warm browser from a reserved pool, while the "sub-300ms" cold-start figure refers to booting a fresh unikernel. Both can be true; they are not the same metric, and the writeup presents them as such rather than collapsing them.
- **Open-source claim is contested.** Kernel's own docs position it as "open source infra" (open browser image + SDKs), which it markets as important for regulated industries that need to self-host or audit. A competitor (Steel.dev) characterizes Kernel as closed-source and managed-only with no self-hosting. Steel is a biased source; treat the discrepancy as unresolved pending direct inspection of Kernel's repos.
- **Differentiation is performance + economics, not features.** Most listed capabilities (stealth, proxies, observability, multi-protocol control) also exist at Browserbase/Steel/Hyperbrowser. Kernel's defensible edge, if the benchmarks hold, is the unikernel-driven cold-start/cost advantage plus the serverless agent-loop platform -- not a unique feature checklist.

---

## Suggestions & Future Directions

_(Open questions and considerations for a prospective adopter -- this is a product/docs analysis, not a research paper, so these are evaluation notes rather than author proposals.)_

1. **Verify the open-source claim directly** -- Inspect Kernel's GitHub for the browser image and SDK licenses before relying on self-hosting or audit guarantees, given the Steel contradiction.
2. **Benchmark on your own workload** -- The 5.8x / 50% figures are vendor/competitor-sourced. Cold-start and cost advantages are workload-dependent; validate against your actual session mix (many short vs. few long).
3. **Probe the stealth/CAPTCHA terms** -- Residential proxies and CAPTCHA solving carry legal/ToS considerations per target site; confirm acceptable-use boundaries before scaling scraping use cases.
4. **Test the serverless platform's limits** -- Co-located agent-loop deployment is the stickiest differentiator; evaluate cold-start, runtime limits, and observability of the deployed app layer (not just the browser).
5. **Compare total cost at steady state** -- Per-second billing and standby mode favor bursty traffic; model the cost against always-on alternatives if your agents run continuously rather than in bursts.

---

## Company & Funding

Kernel (kernel.sh / onkernel.com). Y Combinator-backed; $22M Series A led by Accel (announced Oct 2025). Customers cited include Cash App, Framer, and 3,000+ teams. Primary competitors: Browserbase (incumbent), Steel.dev, Hyperbrowser, Skyvern.
