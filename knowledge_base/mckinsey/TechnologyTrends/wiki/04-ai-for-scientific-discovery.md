[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# AI for scientific discovery and engineering
**In one sentence:** AI — from AlphaFold-style deep learning through LLMs (large language models, AI systems trained on massive text to understand and generate language), agentic workflows, and robotics — is moving from prediction and simulation into closed-loop discovery systems that accelerate drug, materials, and engineering R&D, though economics, validation, and scale-up bottlenecks remain.
## Key points
- Deep learning models solved long-standing challenges in protein structure prediction (e.g., AlphaFold) and established AI as a credible scientific tool; attention now shifts to physical AI, LLMs, and autonomous experimentation.
- Bringing a new drug to market still takes more than ten years and costs $1.3 billion to $2.6 billion with high clinical failure rates, so firms deploy AI across experiment design, molecular optimization, toxicity prediction, candidate generation/evaluation, and clinical-trial design.
- Dozens of AI-discovered or AI-assisted candidates are reportedly in development globally; Anthropic launched Claude Science (beta AI workbench) plus an internal AI drug-discovery program focused on neglected diseases.
- In materials and engineering, AI searches large pools for batteries, semiconductors, and catalysts; physics-informed AI and deep learning surrogates approximate costly fluid-dynamics and structural simulations but still require high-fidelity validation and physical testing.
- Momentum is capital-led: equity investment rose from nearly $8 billion ($7.9B) in 2025 to $12.5 billion through H1 2026; talent demand +18% (2024–25); headline rounds include Isomorphic Labs $2.1B Series B, Earendil Labs $787M, Fathom $47M Series A, PhysicsX $300M at $2.4B valuation, Periodic Labs $300M seed (2025).
- R&D organizations use LLMs as orchestration/coordination layers over simulations and tools (MCP-SIM memory-coordinated physics-aware simulation example), and shift toward closed-loop labs where AI proposes hypotheses and robots run experiments (Berkeley A-Lab; Ginkgo + GPT-5: 6 cycles, 40% cost reduction in cell-free protein synthesis).
- Scientific data is the strategic bottleneck: biobanks (e.g., 490,640 UK Biobank whole genomes), consortium pooling, federated learning (e.g., Lilly TuneLab, built on $1B+ research investment), and proprietary data generation (e.g., Recursion) expand training data.
---
## The trend — and why it matters
AI for scientific innovation is a nascent field; R&D organizations that adopted AI for prediction and modeling now experiment with autonomous, agentic AI-enabled research workflows. AI optimizes molecules, prioritizes product candidates, and explores engineering design spaces feeding real-world pipelines. AI could dramatically boost R&D productivity in some discovery steps, including expanding the number of hypotheses. Although AI-discovered medicines so far have limited clinical outcomes, life sciences companies bet heavily on this pathway. Engineering uses AI across life sciences, materials science, chemistry, physics, climate science, energy, geoscience, astronomy, and engineering: models, simulations, and agentic workflows help generate hypotheses, design experiments, and automate work.

**Covers:** pp. 28–29, "The trend—and why it matters"

## AI in life sciences and the drug pipeline
AI is embedded in life sciences R&D from discovery through clinical trials. Applications span the discovery value chain — generating/optimizing therapeutic candidates; evaluating safety, efficacy, manufacturability before physical testing; experiment design, literature review, data analysis; toxicity prediction; clinical-trial design — aiming to improve discovery speed and probability of success. Protein-engineering and generative-chemistry foundation models move toward commercial deployment; advances including Boltz-2 and Evo 2 demonstrated how large-scale models support antibody engineering, protein optimization, and pharma research. Caveat stated in chunk: antibody prediction remains difficult because therapeutic antibodies are engineered to bind targets in highly specific ways possibly unrepresented in natural protein training data; Boltz-2 can help prioritize antibody designs to test but still requires experimental validation.

**Covers:** pp. 28–30, life-sciences R&D and foundation models

## Materials science and engineering design
AI models search large materials pools for batteries, semiconductors, and industrial catalysts, seeking compounds stable and practical to manufacture; traditional cycles take years of iterative experimentation. Transformer-based architectures (attention-mechanism models effective for language, protein analysis, drug discovery) now search massive design spaces across batteries, catalysts, semiconductors, alloys, carbon materials, and manufacturing systems — with the goal shifting from theoretically viable compounds to synthesizable, scalable, economical ones. Examples in chunk: Berkeley Lab A-Lab (AI proposes compounds, robots prepare/test them for batteries/electronics); Microsoft Discovery platform supported the Majorana 2 quantum-chip materials stack, with agentic AI improving qubit reliability (reported as 1,000x more reliable); MIT generative model trained on more than 23,000 synthesis recipes to guide synthesis pathways. Physics-informed AI and deep learning surrogates accelerate engineering design by approximating costly simulations (fluid dynamics, structural performance, e.g., NeuralDEM particulate flows; interleaved physics-deep-learning fatigue-crack simulations), subject to high-fidelity and physical-test validation.

**Covers:** pp. 29–31, materials and engineering design

## Investment signal
Investment is described as the clearest momentum signal. AI-native drug discovery continued attracting major capital in 2026: Isomorphic Labs $2.1 billion Series B; Earendil Labs $787 million for AI-driven biologics; Fathom Therapeutics (formerly Atommap) $47 million oversubscribed Series A for physics- and AI-enabled small-molecule design. Broader signal: PhysicsX reported $300 million financing at $2.4 billion valuation (June); Periodic Labs $300 million seed (2025), called one of the largest early-stage scientific-AI investments. Economics context: discovery remains capital- and labor-intensive with declining R&D productivity ("Eroom's Law" in biopharma — discovery slower and more expensive over time).

| Metric | Value (chunk) |
|---|---|
| Equity investment 2025 | $7.9 billion (text: "nearly $8 billion") |
| Equity investment H1 2026 | $12.5 billion |
| Job postings change 2024–25 | +18% |

**Covers:** pp. 29–31, investment and scoring box

## Scoring the trend
News and searches are the strongest vectors (rising interest); patents and research publications specific to the category remain limited. Investment is the clearest momentum signal, rising from a low base to nearly $8 billion in 2025 and $12.5 billion through H1 2026. Score-by-vector chart (0–1 scale, relative to trends studied) covers News, Searches, Research, Patents, Equity investment, Talent demand for 2022 vs 2025. Note in source: each vector used defined sources/keywords, screened for valid mentions, indexed 0–1 relative to trends studied.

**Covers:** p. 30, "Scoring the trend" box

## Latest developments
- Protein-engineering and generative-chemistry foundation models toward commercial deployment (Boltz-2, Evo 2), with validation caveats above.
- Materials science as commercially important frontier (transformers; synthesizability/manufacturability focus; Periodic Labs $300M seed).
- LLMs as orchestration layers: adopted not as replacements for deterministic simulators but as coordination layers managing workflows and tools (Anthropic Claude Science announcement). Vendors cited: PhysicsX, BeyondMath (€8.4M raise to expand generative physics research), Luminary Cloud with nTop (cut design time from months to hours with NVIDIA technology). Research example: MCP-SIM (memory-coordinated physics-aware simulation) translates incomplete natural-language prompts into validated simulations while coordinating with scientific tools; organizations must codify proprietary data, know-how, expertise, and validation routines into agentic workflows.
- Shift from isolated models to closed-loop discovery: AI plus automated labs/robotics/real-world experiments across drugs, batteries, catalysts, semiconductors, advanced materials; loop = AI generates hypotheses, automated systems execute, orchestration feeds data back. Partnerships: Insilico Medicine deals worth billions with Eli Lilly, SK Biopharmaceuticals (up to $2.5B, neuroimmune), Takeda (up to $600M); Insilico assets cited: Rentosertib (pulmonary fibrosis) and Garutadustat (inflammatory bowel disease). Autonomous/cloud labs: China autonomous-lab infrastructure; Emerald Cloud Lab "rent lab in the cloud"; Ginkgo Bioworks gave GPT-5 cloud-lab access in Boston — after six cycles, 40% cost reduction in cell-free protein synthesis vs state-of-the-art.
- Agents replacing parts of custom scientific analytics pipelines (multimodal data analysis, literature synthesis, experiment tracking, biomarker discovery, knowledge retrieval), with humans retained for approval/verification.
- Scientific data as strategic asset: consortium pooling, public–private biobanks (Iceland, UK, US; e.g., 490,640 UK Biobank whole genomes), federated learning (Lilly TuneLab platform, $1B+ research investment, toxicity/molecular analysis without centralizing sensitive data), proprietary data generation (Recursion via automated labs/high-throughput testing).

> 'Scientific AI is no longer just about computational prediction. It is about tightening the feedback loop between generative models and physical labs. Algorithms can help us explore vast chemical and biological spaces, but it is the seamless integration with rapid experimental validation that actually drives R&D productivity.'
> — Alex Devereson, senior partner, London

> 'Drug discovery is moving from isolated AI models toward orchestrated research systems. Models are being connected to workflows that design experiments, optimize molecules, assess toxicity, and evaluate candidates. That breadth improves speed of discovery and probability of scientific success.'
> — David Champagne, senior partner, London

**Covers:** pp. 30–33, "Latest developments" + quotes

## Talent and labor markets
Demand: talent market contracted sharply from 2022 peak, postings down by more than half; scientist roles (largest category) down roughly two-thirds since 2022; past year shows early recovery with machine-learning engineers among fastest-growing roles and scientists bouncing back — field reorienting toward AI-enabled research. Functional mix heavily R&D-weighted: 2025 shares — R&D 80%, Sales and marketing 3%, Operations 7%, General and administrative 1%, Other 9%. Titles tracked (2022–25, thousands): Scientist, Bioinformatics scientist, Data scientist, Postdoctoral researcher, Biologist, Machine learning engineer, Professor, Research technician, Software engineer, Product manager. Skills: most required are computational biology (82% of postings) and machine learning (74%), both well supplied; Python 50%, cloud computing 40%, programming 31%, data science 28%, statistics 21%, with supply roughly keeping pace (availability ratios: computational biology 4.6x, machine learning 4.3x, Python 1.8x, cloud 1.0x, programming 1.5x, data science 1.7x, statistics 6.4x). Finding: domain scientists and technologists are available; people combining both are harder to find.

**Covers:** pp. 34–35, talent demand and skills availability

## Adoption across the globe
Adoption score: 2 — Experimentation. Most organizations remain in initial stages of deploying AI-native scientific-discovery systems, though investment and experimentation accelerated sharply over the past year. North America holds a large share of AI-enabled drug discovery, computational biology, and foundation-model investment (frontier AI firms, pharma, hyperscalers, research universities). China builds autonomous-lab infrastructure and industrial-scale automation integrating robotics, AI, and physical experimentation. Europe is highly active in scientific-AI research (pharma, chemistry, industrial materials), with adoption shaped by regulatory/governance considerations. Most active adopters: pharma, biotech, battery developers, chemicals, materials science organizations.

**Covers:** p. 35, adoption developments

## Underlying technologies
| Technology | Role (per source) |
|---|---|
| Agentic orchestration systems | Coordinate workflows, tools, experiments, knowledge sources to plan, execute, optimize research |
| Laboratory automation systems | Robotics/orchestration platforms automating experimental workflows, testing, data collection, iterative discovery |
| Multimodal scientific data platforms | Integrated biological, chemical, genomic, imaging, sensor, experimental data for AI-driven analysis |
| Protein-engineering models | Analyze, predict, design proteins, antibodies, enzymes, biological sequences with targeted functions |
| Scientific foundation models | Large-scale models/deep-learning surrogates trained on molecules, proteins, sequences, materials, literature to generate predictions, insights, designs |

**Covers:** p. 36, underlying technologies table

## Key uncertainties
- Scientific reliability and reproducibility (consistency/validation of AI outputs).
- Data availability and ownership (fragmented, uneven access to high-quality data sets).
- Regulatory evolution (standards for AI-generated discoveries, drug development, autonomous experimentation).
- Laboratory integration complexity (robotics + AI + simulation + infrastructure).
- Economic scalability (autonomous labs expensive to deploy/maintain at scale).
- Downstream bottlenecks/translation constraints (clinical trials, manufacturing scale-up limit how fast discoveries reach market).

**Covers:** p. 36, key uncertainties

## Big questions about the future
- How autonomous can scientific discovery systems realistically become over the next decade?
- How should organizations balance open scientific collaboration with proprietary data and competitive advantage?
- How should regulators validate and govern AI-generated scientific outputs and experimentation?
- What new infrastructure, data-sharing models, and partnerships are required to scale AI-enabled discovery globally?

**Covers:** p. 37, big questions; related reading list omitted (out of chunk scope for this page's claims)

**Covers:** Trend 03, Technology Trends Outlook 2026 pp. 28–37 (chunk 04-engineering-demonstrated-how-deep-learning-model)
