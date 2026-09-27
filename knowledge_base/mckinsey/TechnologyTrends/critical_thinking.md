> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: Technology Trends

This is a critical read of the digest and wiki notes (not the source report or the web).
The report's big idea: technology moved "off the screen into the physical world," with
AI as the accelerant and energy, chips, talent, and trust as the brakes.

## Claims vs. evidence

- Strongest claim pair: agentic software development could unlock almost $1 trillion, yet only
  one-quarter of adopters get real acceleration (twofold gains in 25%+ of teams). The wiki backs
  this with skewed gains (top 20% of engineers +55%, rest ~+3%) and cases where output rose 180%
  but shipped releases rose only 30%. Claim and evidence agree: tools are real, transformation is rare.
- Same honesty on agentic AI: 89% of firms use AI, majority test agents, but only 37% report any
  positive EBIT (Earnings Before Interest and Taxes, a profit measure). A single agentic workflow can
  cost 5–30x the tokens of one chatbot query, and 93% exceed AI budgets. Value story is plausible;
  profit story is not yet proven.
- Physical-limits claims are the best supported: data centers heading for ~14% of US power by 2030
  (from 3% in 2022), transformer lead times over two years, 2,500+ gigawatts stuck in grid queues,
  inference becoming most of AI compute. Multiple independent signals (investment, talent, shortages)
  point the same way.
- Security claims are striking and specific: over three-quarters of vulnerabilities are "zero day"
  (exploit exists at disclosure), public-app exploitation +44%, ransomware groups +49%, machine
  identities outnumber humans ~100 to 1. The sanctioned test (1,060 autonomous attacks chaining a
  low-severity flaw into full file access) is concrete, though single-test evidence should not be
  treated as a base rate.
- Weakest evidence: 2026 investment "doublers" extrapolated from H1 run rates. The 12.8x multiple for
  agentic development rests heavily on one $60 billion Cursor deal; space (5.3x) and robotics (2.1x)
  are similarly megadeal-sensitive. Direction is likely right; exact multiples are fragile.

## Genuinely new vs. repackaged

- Genuinely new this edition: two trends split out — agentic software development (Trend 01) and AI
  for scientific discovery and engineering (Trend 03). Both reflect real shifts: async agent fleets and
  the "agentic factory" across the PDLC (Product Development Life Cycle), plus closed-loop labs where
  AI proposes hypotheses and robots run experiments.
- Reframed, not new: "AI infrastructure and model architectures" (old AI trend), "cybersecurity and
  trustworthy systems" (old digital trust), "life sciences and bioengineering" (old bioengineering).
  The content moved with the market (inference economics, zero-trust runtime, scale-up focus), but the
  categories are continuity with new labels.
- Retired: cloud and edge computing, judged mature. That is a fair call given the wiki evidence —
  hiring there shifted from build-out to sales, support, and operations.
- Repackaged pattern to watch: "physical AI" and "world models" appear across robotics, mobility,
  and infrastructure. The shared tech (VLA — vision-language-action — models, simulation, digital twins)
  is real, but the report sometimes counts the same advance under several trends.

## Weaknesses and blind spots

- Investment is used as conviction, but capital follows hype too. Patent, search, and hiring signals
  are indexed 0–1 relative to the 14 trends, so "high innovation" means high versus this set, not
  versus all technology. Private-company innovation (semiconductors, models) is undercounted in papers.
- Talent data leans on English-speaking postings; China-heavy execution (54% of robot installs,
  EV and battery scale, 12,000-km quantum network) is described but structurally underweighted.
- Costs and who pays are thin: token budgets, fab economics vs. obsolescence, grid interconnection,
  green premiums, and reimbursement (diagnostics, cultivated meat) decide deployment, yet get less
  space than capability stories.
- Missing or light: environmental cost of the AI build-out beyond power access; labor displacement and
  junior-engineer pipelines as agents take implementation work; small-business and public-sector paths
  (everything reads enterprise/hyperscaler); evaluation science — the report says "invest in evals"
  but offers no shared yardstick for agent reliability across vendors.
- Security advice (zero trust — "never trust, always verify" — plus quantum-safe migration) is sound
  but vendor-deal-heavy (Wiz, SGNL, Astrix, Portkey, Acuvity); concentration risk in a few platforms
  gets one paragraph when it deserves a chapter.

## Applicability

- Most transferable now: inference economics (cost per token, performance per watt/dollar), CI/CD
  (Continuous Integration / Continuous Delivery — getting code safely to production) discipline, agent
  evaluations tied to business goals, knowledge graphs plus enterprise context for brownfield codebases,
  zero-trust identity for machine users, and MRV-style (Measurement, Reporting, Verification) observability.
- Least transferable now: quantum computing, orbital compute, humanoids, eVTOL (electric vertical
  takeoff and landing) air taxis, D2D (direct-to-device) satellite-to-phone. Track the adjacent usable
  parts: post-quantum cryptography inventory, RaaS (Robotics-as-a-Service) contracting lessons, LEO
  (Low Earth Orbit) backhaul for remote sites, smart glasses for field service.
- **Relevance to my work**
  - AI/ML engineering: treat inference as the operating cost — prefer SLMs (Small Language Models),
    compression, and routing/orchestration over biggest-model-default; fix the CI/CD and orchestration
    bottleneck (0.1–0.2x availability) before buying more model; measure release throughput and defect
    escape rate, not coding activity.
  - Agentic systems: pilot human–agent pods (small human team supervising agent fleets) on 4+ PDLC
    stages with harness/guardrail controls, MCP (Model Context Protocol) interfaces to legacy systems,
    and token budgets per workflow; expect 5–30x chatbot cost and govern nonhuman identities from day one.
  - Elisity data platform: scientific-data and enterprise-context lessons apply directly — lineage,
    permissions, and searchable proprietary knowledge decide agent quality; federated access plus
    data-classification and continuous runtime inspection fit a trust-layer positioning; workflow
    integration (not raw imagery/data volume) is where space, EO (Earth Observation), and MRV notes
    say the value sits.

## What this changes

- Operating model first, tools second: async delegation, after-hours agents, smaller leveraged teams,
  and verification at the edges (what to build, whether it works). Without rewiring PDLC, agents add
  code faster than review, test, and deploy can absorb — the "brittle code" trap.
- Build-vs-buy shifts: codesigned silicon, orchestration middleware (LangGraph-style), and identity
  platforms concentrate power in hyperscalers and a few vendors. Default to buying the substrate and
  building the thin layer that encodes your data, workflows, and evals.
- Energy and hardware join the planning stack: time-to-power rivals time-to-market. Any AI roadmap
  without power, memory/packaging, and supply-chain assumptions is fiction past pilot scale.
- Security posture must assume near-zero defense windows: continuous runtime inspection, automated
  containment, and quantum-safe inventory move from backlog to roadmap.

## Verdict

Useful as a planning lens, weak as a playbook: it diagnoses constraints well but underprices cost,
concentration, and evaluation gaps. For our work, pilot the agentic factory with strict evals and
budgets, harden identity and runtime security, and design for inference cost — monitor quantum,
immersive, space, and humanoids without staffing them. Overall call: **trial**.
