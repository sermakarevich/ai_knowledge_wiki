> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Future of Robotics (and start of Future of Mobility)
**In one sentence:** Robots are moving from scripted demos to RaaS-funded, AI-driven dark-factory deployment, but fine manipulation, real-world reliability, and optimization talent remain the bottlenecks, while mobility is entering selective scaling led by EVs (21M sales in 2025) and repeatable L4 robotaxi service.
## Key points
- Fine manipulation is the bottleneck: the NIST Task Board benchmark notes in-hand manipulation and grasping are among the most difficult capabilities to achieve and measure, limiting moves from demos to dependable production use.
- Robotics-as-a-service (RaaS) shifts humanoids priced at $150,000–$500,000 per unit from capital outlay to per-robot/per-hour/per-task operational expenditure, with Locus Robotics surpassing five billion warehouse picks as a scalability proof point and a feedback loop aligning deployer and operator on uptime.
- Dark factories are accelerating via AI, robotics, and digital twins: Haier, Midea, and Xiaomi expanding in China, Hyundai, LG, and Samsung integrating AI-driven lines in South Korea, though most value will come from brownfield integration, not greenfield showcases.
- Robotics hiring declined from earlier highs with a 2025 uptick tilted to machine learning (largest role), automation, and research; 63% of 2025 postings are R&D, and optimization is scarcest at 0.1× talent-to-demand versus 9.2× for PyTorch and 4.6× for deep learning.
- Adoption score is 2 — Experimentation: China held ~2 million industrial robots in 2024 and 54% of annual installations worldwide and centers robotics in its 15th Five-Year Plan, while manufacturing and logistics lead and construction remains hardest due to dynamic, safety-critical sites.
- Future of mobility is selective scaling: global electric-car sales grew >20% in 2025 to 21 million units (one in four cars sold), China captured >half of sales, Europe grew >30%, the US declined 2% after federal tax credits ended in September, and electric heavy-freight truck sales tripled to >200,000 units.
- Autonomy is narrowing to repeatable domains: Waymo reported >15 million trips in 2025 and >20 million lifetime trips, Baidu Apollo Go reported 3.4 million fully driverless rides in Q4 2025 and >20 million cumulative rides by February 2026, and UNECE adopted the first global automated-driving framework in June 2026; 49% of experts expect mass-market private vehicles to center on L2 through 2035.
- The EV bottleneck is shifting to energy access: >7 million public charging points by end-2025, transformer/switchgear lead times >2 years in some markets, Chinese LFP packs ~€64/kWh and NMC ~€82/kWh with up to 40% lower battery costs than global peers; mobility equity investment was $63.5 billion in 2025 (−11%).
---
## Manipulation bottleneck and RaaS
**Covers:** pp. 96–97

Continuous operation is more feasible but fine manipulation is still the bottleneck. The NIST Task Board benchmark, used to measure manipulation capability, notes in-hand manipulation and grasping are among the most difficult to achieve and measure.

RaaS is accelerating commercial adoption by shifting the $150,000–$500,000 per-unit humanoid cost to operational expenditure (per robot, per hour, or per task). Locus Robotics surpassed five billion warehouse picks. The model creates aligned incentives: deployer gets performance and reliability data, operator gets utilization and failure-mode data.

> ‘For decades, robots could repeat only what they were programmed to do. Physical AI breaks that limit: With foundation models, machines can now perceive, reason, and act in environments no one scripted in advance, and work safely alongside people. The opportunity is vast, but it will be won less by the impressive demo than by making these systems reliable enough for everyday operations.’
> — Christian Jansen, partner, Hamburg

## Dark factories
**Covers:** p. 96

Manufacturers integrate AI, robotics, and digital twins so fleets operate autonomously and maintain themselves. Automotive, electronics, semiconductors, white-goods industries building dark factories with unsupervised robots. China: Haier, Midea, Xiaomi expanding highly automated facilities. South Korea accelerating AI-powered smart factories; Hyundai, LG, Samsung integrating AI-driven lines. Most manufacturers will capture value by integrating robots into existing brownfield plants, not greenfield showcases.

## Talent and labor markets
**Covers:** pp. 97–98

Demand: robotics hiring declined overall from earlier highs, with uptick in 2025. Tilted to machine learning, automation, research. Machine learning engineers now single largest role. Automation engineers and data scientists saw strong growth.

Job postings by title 2022–25 (thousands, chart 0–14): machine learning engineer, software engineer, data scientist, scientist, robotics engineer, software developer, product manager, technician, automation engineer, research engineer.

Job postings by business function, 2025, % share:

| R&D | Sales and marketing | Operations | General and administrative | Other |
|---|---|---|---|---|
| 63 | 6 | 12 | 11 | 8 |

Skills availability: scarcest in optimization (demand clearly outstrips supply, central to real settings); C++, deep learning, machine learning abundant; harder constraint is connecting AI with hardware, controls, deployment.

| Skill | % postings requiring | Talent-to-demand ratio |
|---|---|---|
| Machine learning | 63 | 4.3× |
| Python | 42 | 1.8× |
| Cloud computing | 38 | 1.0× |
| Reinforcement learning | 36 | 1.4× |
| Optimization | 26 | 0.1× |
| PyTorch | 21 | 1.3× |
| C++ | 21 | 9.2× |
| Deep learning | 21 | 4.6× |

## Adoption across the globe
**Covers:** pp. 98–99

Adoption score: 2 — Experimentation. Testing viability with small prototypes; industrial robots scaled, warehouse robots increasingly common; AI-enabled mobile manipulation, humanoids, broader service robots remain early.

- China largest industrial-robot market and most important early humanoid market: ~2 million industrial robots in 2024, 54% of annual installations deployed there; robotics centered in 15th Five-Year Plan toward AI-powered robots.
- United States: major center for start-ups, physical AI models, software, venture-backed humanoids; scaling hardware harder.
- Europe: industrial automation, advanced manufacturing, healthcare; high-precision mechatronics, engineering, safety frameworks.
- Japan: mechatronics, components, industrial automation.
- South Korea: electronics, automotive, conglomerates with robotics ambitions.
- Emerging markets selective: logistics, agriculture, mining, infrastructure inspection.
- Sectors: manufacturing and logistics lead; healthcare, agriculture, hospitality, retail, food service gradual; construction promising but hardest (dynamic, safety-critical) — near-term focus on layout, inspection, repetitive installation.

## Underlying technologies
**Covers:** pp. 99–100

| Technology | Role stated |
|---|---|
| Actuators, motors, dexterous end-effectors | Turn software decisions into movement and manipulation |
| Deterministic controls | Real-time low-latency motion, safety, control loops |
| Fleet software | Coordinate many robots across sites and workflows |
| Physics-aware simulation | High-fidelity physical interactions; learn, test, validate |
| Power and batteries | Determine uptime and untethered operation |
| Safety tools | Collision avoidance, runtime monitoring, fail-safe controls, human oversight |
| Sim-to-real tools | Improve policies in simulation before deployment |
| Tactile sensing | Vision, force, depth, radar, touch to understand environments |
| Teleoperation | Collect data; supervise/manage fleets from afar |
| World models | Simulate environments, predict outcomes, support planning |
| Vision-language models (VLMs) and vision-language-action (VLA) systems | Interpret scenes, reason, convert visual+language inputs into actions |

> ‘The next wave of robotics adoption will be determined less by impressive demonstrations than by measurable business outcomes. Organizations will scale general-purpose robots where they improve safety, productivity, and operational continuity in repeatable workflows. The companies that lead will be those that redesign operations with robotics.’
> — Ani Kelkar, partner, Boston

## Key uncertainties and big questions
**Covers:** pp. 100–101

Uncertainties: real-world reliability (semistructured/unstructured environments); sim-to-real transfer (faster, cheaper); sensor requirements (vision-only VLA vs tactile/other inputs); dexterity and manipulation; humanoid economics vs specialized automation; governance and trust (safety, liability, cybersecurity, insurance).

Big questions: where is ROI clear enough to scale vs pilot; how value splits across hardware vs models, simulation, data, compute, orchestration, integration; what it takes in brownfield vs greenfield; what safety/liability/cybersecurity/software-assurance controls as robots become autonomous and connected.

## Future of mobility — trend and why it matters
**Covers:** pp. 101–103

Trend 11: electric, autonomous, software-defined vehicles plus charging, shared mobility, drones, air taxis, maritime systems making transport more connected and automated. Past decade focused on EVs, autonomous-driving software, micromobility; now challenge is reliable operation inside regulated freeways, rail, aviation.

- Electrification largest/most mature but operationally complex: 21M electric-car sales 2025 (>20% over 2024), one in four cars electric; China largest (>half sales first time 2025); Europe >30% growth on EU emissions standards/incentives/affordability; US −2% on elimination of federal tax credits after September; electric heavy-freight trucks tripled vs 2024 to >200,000 globally.
- Autonomy narrower than early forecasts: L4 robotaxis repeatable in many cities; autonomous trucks moving to driverless freight on select routes; private fully autonomous likely slower; 2025 McKinsey survey (91 decision-makers): L4 robotaxis first commercial L4 at scale, 49% expect mass-market private to center on L2 through 2035; mass-market near-term pathway is advanced driver assistance.
- Novel solutions selective: commercial drone delivery expanding in retail/healthcare; electric air taxis nearing early service but constrained by infrastructure, air-traffic integration, batteries; micromobility (e-scooters/e-bikes) stabilizing and integrating into cities; maritime/industrial advancing via electrified boats/ferries and port integration.
- Software-defined + energy-linked: sensors, AI, over-the-air updates, fleet management, payments; EV/fleet/charging scale depends on grid capacity, interconnection, charging economics, battery supply chains (critical minerals, refining, recycling).

> ‘Mobility is becoming a software-defined system where value comes as much from data, software, and fleet operations as from the vehicle itself. The winners will be those that integrate electrification, autonomy, and digital infrastructure into a seamless customer and operating experience.’
> — Andreas Breiter, partner, Bay Area

## Scoring the trend and latest developments
**Covers:** pp. 103–104

Research publications fallen sharply since 2022 (largest shift); equity investment eased; patent activity increased; search/news edged higher — move from broad experimentation to selective deployment (robotaxis, autonomous freight).

| Vector | Note |
|---|---|
| Equity investment 2025 | $63.5 billion, −11% |
| Job postings 2024–25 | % difference tracked (chart) |
| Score by vector (0–1) | News, Searches, Research, Patents, Equity investment, Talent demand |

Recent developments:
- Robotaxis demonstration → repeatable service, highly localized: Waymo >15M trips in 2025, >20M lifetime; Baidu Apollo Go 3.4M fully driverless Q4 2025, >20M cumulative by Feb 2026 (mostly China), Middle East deployments and Europe pilots early 2026; US city-level deployments, China dense ecosystem, Europe pilot activity; UNECE June 2026 first global automated-driving framework.
- EV adoption growing, regional/affordability-focused: 21M sales (~one-quarter of new-car sales); EU 90% CO₂ reduction target after 2035 pressures shift; Chinese battery costs: LFP ~€64/kWh, NMC ~€82/kWh, up to 40% lower than global peers via pack architecture, LFP chemistry, component costs; China near EV–combustion price parity; high-cost regions adding plug-in hybrids, extended-range EVs, LFP.
- Bottleneck shifting to energy access: >7M public charging points end-2025; large transformer/switchgear lead times >2 years in some markets; freight leapfrog where routes predictable and depot charging plannable; electric heavy-freight tripling to >200,000 concentrated in China, scaling depends on grid, equipment, high-power standards.

**Covers:** Technology Trends Outlook 2026, pp. 96–104 (end of Trend 10 Future of robotics + start of Trend 11 Future of mobility)
