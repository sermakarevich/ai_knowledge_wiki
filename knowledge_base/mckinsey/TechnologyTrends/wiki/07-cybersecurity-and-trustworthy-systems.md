[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Cybersecurity and trustworthy systems
**In one sentence:** AI is compressing the vulnerability-to-exploitation window and enabling autonomous chained attacks at scale, forcing enterprises to shift from perimeter defense to zero-trust continuous runtime inspection, quantum-safe cryptography, and blockchain-based trust layers.
## Key points
- More than three-quarters of all cybersecurity vulnerabilities are classified as "zero day," meaning an exploit already exists by the time of public disclosure.
- Advanced AI agents can autonomously discover and exploit vulnerabilities and chain dozens of separate exploitation steps into one attack path — demonstrated when an agent escalated a single low-severity flaw into complete unauthorized file access in a sanctioned test of 1,060 autonomous attacks.
- Historically weeks-or-months threat cycles have shrunk dramatically: exploitation of public-facing applications surged 44 percent in a single year, fueling a 49 percent increase in active ransomware and extortion groups (IBM 2026 X-Force Threat Intelligence Index).
- Defense is shifting to continuous control-point architectures: continuous runtime inspection, granular data classification, automated containment, and zero-trust (never trust a user, device, or system even inside the network), including custom-integrated security for machine-to-machine and agent identities.
- Machine identities (bots/agents) now outnumber human users by roughly 100 to one, making identity a central security pillar with unified governance, password-free authentication, and context-aware access.
- Investment was $77.5 billion in equity in 2025 and roughly $63.0 billion already by mid-2026 (below 2022 level); searches rose meaningfully, news mentions stayed low, research/patent activity rose modestly — a mature field in sustained deployment.
- "Harvest now, decrypt later" plus NIST finalized post-quantum cryptography standards moved quantum-safe migration from speculative research to active enterprise-planning priority ahead of Q-Day; adoption remains early-stage.
- Consolidation is accelerating around AI-powered platforms bundling identity, cloud, and automated detection: Google completed Wiz acquisition; CrowdStrike→SGNL, Cisco→Astrix Security, Palo Alto Networks→Portkey, Proofpoint→Acuvity, Cyera→Oasis Security ($1 billion), Keyfactor→InfoSec Global.
---
## The trend—and why it matters
**Covers:** Technology Trends Outlook 2026, pp. 57–58, "Cybersecurity and trustworthy systems" intro + "The trend—and why it matters"

Cybersecurity and trustworthy systems help secure computer networks, make digital interactions more verifiable across interconnected environments, and enhance trust in digital systems. Increasingly enabled by AI, they include zero-trust architectures and identity access; other trust-enhancing technologies include blockchain-based ledger systems, tokenization platforms, and quantum-safe cryptography.

When it comes to cybersecurity, AI is both a blessing and a curse: hackers use it to find and exploit vulnerabilities far faster, while companies use it to strengthen and automate defenses. The dynamics are changing beyond break-in prevention — AI alters cyber-defense dynamics while quantum computing is expected to break commonly used cryptography — so cybersecurity is now also the trust layer for AI agents, distributed cloud environments, and machine-to-machine interaction.

Pressures cited:
- Frontier-model capabilities improving rapidly; agents compress time/expertise for offensive activity.
- AI agents chaining multiple exploitation steps into a single coherent attack path, which individual vulnerability scans are not designed to catch.
- Defenders face too much signal, not too little: bottleneck shifts from detecting threats to distinguishing real ones from noise.
- Hackers generate attack tools at massive scale, launching multiple campaigns at once, exploiting flaws before detection/response.
- Models such as Claude Mythos Preview move AI impact into software-security workflows, including finding/exploiting previously unknown vulnerabilities.
- Response: continuous control-point architectures, data security + zero trust, AI-first security protocols, engineering architectures for continuous runtime inspection, granular data classification, automated containment.
- Responsibility expanding beyond IT security to securing agent identities, delegation flows, auditability (who authorized an action, whether an agent stayed in scope, how delegation flowed); more enterprises investing in custom-integrated architectures over off-the-shelf platforms.

> 'As the time between vulnerability identification and exploitation vanishes, bug bounty programs, fraud-analytics-quality incident response, and forward-deployed, engineer-led delivery of just-in-time cybersecurity solutions for enterprise agentic deployments all become more important for providers and customers. Those that get this mix of offerings and capabilities right will put strategic distance between themselves and the competition.'
> — Marc Sorel, partner, Boston

Consolidation: enterprises favor AI-powered platforms bundling identity, cloud security, automated threat detection; Google's acquisition of Wiz underscores hyperscaler/platform race for integrated cloud, AI, and runtime security. Legacy-tool-reliant organizations will be more exposed. For providers, edge may come after the sale: deployment teams learn what an enterprise must protect and derisk agents at machine speed.

## Scoring the trend
**Covers:** p. 59, "Scoring the trend"

Cybersecurity and trustworthy systems continue to draw substantial capital, with $77.5 billion in equity investment in 2025 and roughly $63.0 billion already by mid-2026, though investment remains below its 2022 level. Searches rose meaningfully, reflecting broadening enterprise attention to digital risk management, while news mentions remained low, suggesting less headline attention as the field matures. Research and patent activity rose modestly, consistent with a mature field in sustained deployment rather than breakout growth.

| Vector | 2025 value / note |
|---|---|
| Equity investment | $77.5 billion (+6% shown) |
| Searches | rose meaningfully |
| News | remained low |
| Research | rose modestly |
| Patents | rose modestly |
| Talent demand (job postings 2024–25) | figure shows range bar (value "1" in chunk extraction) |

Note from source: for each vector, a defined set of data sources was used to find keyword occurrences for the 14 trends, screened for valid mentions, indexed 0–1 relative to trends studied. Vectors: News (press reports), Searches (search-engine queries), Research (scientific publications), Patents (patent filings), Equity investment (private- and public-market raises), Talent demand (job postings).

## Latest developments
**Covers:** pp. 59–61, "Latest developments"

- Cybersecurity threat cycles are shrinking as AI accelerates vulnerabilities. Historically weeks or months between identification and active exploitation; today that window has shrunk dramatically because AI lets attackers identify vulnerabilities, develop exploits, and launch attacks much faster. Per IBM's 2026 X-Force Threat Intelligence Index, exploitation of public-facing applications surged by 44 percent in a single year, directly fueling a 49 percent increase in active ransomware and extortion groups. Reporting on Anthropic's Claude Mythos and Glasswing efforts shows frontier-model cyber capabilities accelerating vulnerability discovery.

> 'Cyber and trust are often framed as defensive disciplines, but they also determine how much value technology can create. When people trust a system, they use it more fully, share data more confidently, and build new workflows around it. That is why trust belongs in the value case, not just the risk register.'
> — Roger Roberts, partner, Bay Area

- Offense/defense duality in critical-infrastructure-defense testing: hackers speed up attacks with AI; companies use same capabilities to identify vulnerabilities in critical software and shore up defenses (Project Glasswing: securing critical software for the AI era; Expanding Project Glasswing). New operating reality: defense must leverage AI for detection, triage, containment — plus new frameworks against AI-based attacks. Z.ai's GLM-5.2 inflection: independent cyber benchmarks found the open-weight model competitive on vulnerability detection and cyber-agent tasks — helps defenders but also makes capabilities more accessible to attackers.
- Zero-trust and runtime security architectures are central: unprecedented emphasis on continuous runtime inspection and granular access controls constantly authenticating users, devices, workloads, and AI agents. Vendor moves: CrowdStrike's acquisition of SGNL lets Falcon identity suite make real-time access decisions (grant/deny/revoke for people, machines, AI agents); Cisco's acquisition of Astrix Security brings identity oversight to AI agents and machine credentials; Palo Alto Networks' acquisition of Portkey adds AI gateway and runtime protection to Prisma AIRS. Shift from periodic scanning and perimeter defense toward continuous validation and automated containment.
- Quantum concerns evolving: "harvest now, decrypt later" (capture encrypted data today for future quantum decryption) shifted from speculative research to active enterprise-planning priority. NIST's finalized post-quantum cryptography standards created a practical migration-planning starting point ahead of Q-Day, when quantum computing is expected to break commonly used encryption. Especially relevant for governments, financial institutions, healthcare, critical-infrastructure operators, long-lived-sensitive-data holders. Keyfactor's 2025 acquisition of InfoSec Global illustrates emerging quantum-safe-tool market for inventorying cryptographic exposure before Q-Day.
- Data classification and AI governance controls becoming more important: as gen AI tools and autonomous agents deploy, sensitive data moves across applications, cloud environments, third-party models, internal knowledge systems unpredictably. Data-security platforms now monitor sensitive-information movement through AI-enabled workflows. Cyera's $1 billion acquisition of Oasis Security unifies data security with identity governance for AI agents and nonhuman identities. Proofpoint's acquisition of Acuvity gives visibility/governance over employee and AI-agent use of generative AI and agentic workflows, extending protection across endpoints, browsers, and MCP (model content protocol) servers.
- Identity as security pillar as machine identities outnumber humans: identity can no longer be treated as human-only; software identities (bots/agents) now outnumber human users by roughly 100 to one. Response: unified identity governance, password-free authentication, context-aware access controls instead of static role-based permissions.
- Blockchain as trust-enabling technology: deployed because it provides a shared, auditable record for transactions, ownership, compliance between parties that may not fully trust one another; verifiable digital interactions for tokenized assets, programmable payments, stablecoin settlement, machine-to-machine commerce (see sidebar).

## Sidebar: Blockchain as a trust-enabling technology
**Covers:** p. 61 sidebar

Recent developments suggest movement from broad experimentation toward targeted institutional use cases:
- Stripe completed Bridge acquisition to expand stablecoin infrastructure (faster, lower-cost global payments, programmable financial services).
- Visa supports nine blockchains in its global stablecoin settlement pilot, at a $7 billion annualized run rate; stablecoin-linked card programs growing (Visa operates more than 130 in 50 countries) but still a tiny fraction of overall payment volumes.
- JPMorgan Chase launched a tokenized money market fund using Kinexys Digital Assets.

Momentum signals: interest and innovation largely flat; investment uneven with sharp year-to-year swings, consistent with selective institutional move-in rather than broad scaling. Talent: blockchain hiring runs at roughly 20 percent of cybersecurity's demand but is growing faster; the two share about half their top roles and several core skills; blockchain's distinctive demand reflects commercialization, concentrating in marketing, product, and design roles such as marketing managers and graphic designers (which barely register among cybersecurity's top roles). For enterprises, blockchain-enabled systems may underlie trusted financial flows, proprietary digital assets, compliance workflows; adoption uneven, dependent on regulation, interoperability, privacy, integration — but direction is clearer as a potential element of a broader digital trust stack.

## Talent and labor markets: demand
**Covers:** p. 62, "Demand"

After contracting sharply from a 2022 peak of job postings, hiring stabilized, with 2025 seeing the first year-over-year increase since the post-pandemic pullback. Security analysts remain the dominant role by volume, while hiring strengthened for software engineers and stabilized for security engineers — reflecting demand for technical employees who can build security tooling. Functional mix is more balanced than most other trends, indicating demand extends beyond technical build-out into commercialization, compliance, enterprise operations.

Job postings by title 2022–25 (thousands; chart, top roles): Security analyst, Software engineer, Security engineer, Technician, Solution architect, Machine learning engineer, Software developer, Product manager, Site reliability engineer, Customer service representative.

Job postings by business function, 2025, % share:

| R&D | Sales and marketing | Operations | General and administrative | Other |
|---|---|---|---|---|
| 37 | 12 | 18 | 19 | 14 |

## Talent and labor markets: skills availability
**Covers:** p. 63 top, "Skills availability"

Cloud computing and cybersecurity are the most widely required skills. Cloud supply broadly keeps pace with demand, with strong supply of self-identified cybersecurity talent. Sharpest gaps in AI and continuous integration and continuous delivery (CI/CD), where qualified talent falls well short of demand. Other established capabilities (risk management, crypto, Azure-related) show relatively strong supply.

| Skill | Talent required (% share of postings) | Talent availability (ratio of talent to demand) |
|---|---|---|
| Cloud computing | 65 | 1.0× |
| Cybersecurity | 40 | 3.3× |
| Risk management | 29 | 6.2× |
| Artificial intelligence | 29 | 0.3× |
| Crypto | 26 | 2.0× |
| Azure | 22 | 1.4× |
| CI/CD (continuous integration and continuous delivery) | 20 | 0.1× |

## Adoption developments across the globe
**Covers:** p. 63 middle, "Adoption developments across the globe"

Adoption score: 4 — Scaling in progress. Organizations are scaling deployment across enterprise infrastructure, AI environments, cloud systems, and technology platforms.

- North America remains the largest cybersecurity market globally and accounts for a substantial share of both global cyber incidents and security investment.
- Europe is highly active in digital trust regulation, operational resilience frameworks, privacy governance, and digital sovereignty initiatives.
- Asia continues to expand investment in AI-enabled cybersecurity, semiconductor security, and blockchain infrastructure.
- Worldwide, critical-infrastructure sectors including energy, healthcare, telecommunications, transportation, and financial services are prioritizing zero-trust architectures, runtime observability, infrastructure resilience, and AI-enabled security operations.
- Blockchain-based tokenization adoption remains uneven but accelerating among financial institutions and infrastructure providers.
- Post-quantum security adoption remains early-stage but increasingly a strategic planning priority among governments, financial institutions, and critical-infrastructure operators as Q-Day draws nearer.

## Underlying technologies
**Covers:** p. 64 top, "Underlying technologies"

| Technology | Description in source |
|---|---|
| AI-enabled cyber and observability systems | Combine threat detection, anomaly analysis, runtime monitoring, automated response, and decision-grade audit, allowing organizations to identify unsafe behavior, contain attacks at machine speed, and track authorization and scope across agents and cross-system actions |
| Confidential computing | Protect sensitive data while it is actively being processed |
| Data security and classification systems | Identify, label, monitor, and enforce controls on sensitive information |
| Hardware-based trust mechanisms | Verify device integrity and establish machine-verifiable trust |
| Post-quantum cryptography | Encryption approaches designed to resist future quantum computing threats and protect networks after Q-Day |
| Zero-trust architecture | Security models that continuously verify users, devices, AI agents, and workloads rather than assuming trust |

## Key uncertainties
**Covers:** p. 64 middle, "Key uncertainties"

- AI-enabled offense and defender readiness: whether enterprise defenders can keep pace with attackers increasingly using AI to accelerate vulnerability discovery, exploit generation, phishing, and lateral movement.
- Post-quantum migration timelines: Q-Day timing uncertain, while making legacy cryptographic infrastructure quantum-ready could take years and require significant coordination across vendors, governments, and enterprises.
- Platform consolidation and concentration risk: integrated security control planes may improve visibility and response but could increase dependence on hyperscalers and a small number of dominant cybersecurity vendors.
- Measuring trust and resilience: leaders still lack consistent ways to quantify whether digital-trust investments reduce risk, improve resilience, enable new business models, or strengthen customer confidence.

> 'Cyber defense has to match the speed of AI-enabled attacks. The concern is that attackers can compress discovery, weaponization, and exploitation into much shorter cycles. Continuous run time visibility and automated containment are essential in this era, while leading organizations look to create agentic security operations across their technology stack.'
> — Charlie Lewis, partner, Connecticut

## Big questions about the future / Read more
**Covers:** pp. 64–65, "Big questions about the future" + "Read more"

Companies and leaders may want to consider:
- What is required to secure AI agents, connected devices, operational technology systems, and autonomous infrastructure at enterprise scale?
- How can AI be leveraged to build security systems capable of adapting faster than emerging geopolitical, AI-enabled, and quantum-related threats?
- How can organizations migrate to post-quantum security architectures before quantum decryption capabilities become operationally viable?
- What does a truly trustworthy enterprise look like in a world of AI agents, autonomous infrastructure, fragmented cloud systems, and persistent cyber conflict?

Read more (as listed in source): Knowledge center — Cybersecurity; Blockchain & Digital Assets. Related reading — Securing the agentic enterprise: Opportunities for cybersecurity providers; The board's role in managing emerging AI risks; Taking a business-critical approach to supplier nth-party IT risk management; HackerOne CEO Kara Sprague on how AI is reshaping cybersecurity; Stablecoins in payments: What the raw transaction numbers miss.
