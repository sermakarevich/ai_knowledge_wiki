# Clio: Privacy-Preserving Insights into Real-World AI Use

**Paper:** [Clio: Privacy-Preserving Insights into Real-World AI Use (Tamkin, McCain et al., 2024)](https://arxiv.org/abs/2412.13678)

## Human Readable TL;DR

Imagine you run a massive library where millions of people come every day to ask questions -- but you're not allowed to read their individual notes. Clio is like a system that groups all those notes into piles by topic ("cooking questions," "homework help," "travel planning") and gives you a summary of each pile, without ever showing you any single person's note. This lets the library understand what people need help with, spot troublemakers, and improve services -- all while keeping everyone's private questions private. It works by having an AI assistant read each note, write a vague-enough summary, then mathematically group similar summaries together and describe the groups.

## TL;DR

Clio is Anthropic's pipeline for analyzing millions of Claude.ai conversations at scale while preserving user privacy. It uses LLMs to extract per-conversation facets (topic summaries, concern scores), embeds them with sentence transformers, applies k-means clustering, generates contrastive cluster descriptions via a stronger LLM, and builds navigable multi-level hierarchies. Validated at 94% end-to-end reconstruction accuracy with a 4-layer privacy defense reducing PII to undetectable levels, it revealed that coding/writing/research dominate usage, identified coordinated misuse patterns (SEO spam, unauthorized reselling), and exposed false positives/negatives in safety classifiers.

---

## Problem & Motivation

AI providers like Anthropic process millions of conversations daily but face a fundamental tension: they need to understand usage patterns (for safety, product improvement, and governance) but cannot ethically or practically review raw user conversations. Existing public datasets (WildChat, LMSYS-Chat-1M) come from specific platforms and don't reflect real production usage. Red-teaming and benchmarks only test for *anticipated* risks -- they cannot discover "unknown unknowns." Clio addresses this gap by enabling bottom-up, privacy-preserving, large-scale analysis of real AI assistant traffic, providing empirically grounded insights for safety, governance, and product development.

---

## Main Original Ideas

1. **LLM-Powered Privacy-Preserving Pipeline** -- Uses AI models themselves as the privacy mechanism: LLMs extract facets from conversations while being prompted to strip PII, then generate cluster-level summaries that further abstract away individual details. This creates a novel "defense in depth" with 4 distinct privacy layers.

2. **Contrastive Cluster Description** -- When generating cluster titles/summaries, the model sees both in-cluster samples AND near-cluster-but-excluded samples, enabling it to identify what is *distinctive* about each cluster rather than just what is common -- a technique that produces much more specific and useful descriptions.

3. **Iterative Hierarchical Clustering** -- Builds multi-level navigable hierarchies by repeatedly embedding cluster descriptions, re-clustering, and using LLMs to propose and assign parent categories. This transforms thousands of flat clusters into a drill-down taxonomy from broad categories to granular sub-topics.

4. **Dual-Use Safety Architecture** -- The same pipeline serves both aggregate analytics (with full privacy layers) and trust & safety investigations (with adjusted privacy layers under strict access controls), enabling detection of coordinated misuse patterns that individual-conversation review would miss.

5. **End-to-End Synthetic Validation Framework** -- Validates the entire pipeline using synthetic multilingual datasets with known ground-truth distributions, measuring reconstruction accuracy (94% regular, 84% concerning content) across 15 languages.

---

## Key Findings

### Pipeline Validation

| Component | Metric | Result |
|---|---|---|
| Conversation summaries | Accuracy (manual review) | **96%** |
| Concern score correlation | Spearman r (vs human) | **0.84** |
| Base cluster titles | Accuracy | **97-99%** |
| Cluster assignment | Misassignment rate | **3%** |
| Hierarchy titles | Accuracy | **97%** |
| E2E reconstruction (regular) | Accuracy | **94%** |
| E2E reconstruction (concerning) | Accuracy | **84%** |
| Multilingual consistency | Min accuracy across 15 langs | **>92%** |
| Privacy (raw -> cluster summary) | PII presence | **10% -> undetectable** |

### Real-World Usage Insights (1M Claude.ai conversations)

- Web/mobile app development alone represents >10% of all conversations
- Top categories: coding, writing assistance, academic research, educational content
- Cross-language variation: Japanese/Chinese conversations show disproportionately more elder care, economic issues, anime/manga content
- Granular discoveries include dream interpretation, D&D game mastering, transportation system optimization

### Safety Applications

- Uncovered coordinated SEO spam networks, explicit content generation rings, and unauthorized Claude access reselling
- Identified safety classifier false positives on job applications, security-adjacent programming, D&D combat stats
- Identified safety classifier false negatives on translated explicit content and requests for uncensored violent/sexual novels
- Used for real-time monitoring during Claude 3.5 Sonnet Computer Use launch and 2024 US elections

---

## Suggestions & Future Directions

1. **Continuous model upgrades** -- As newer, more capable LLMs become available, each pipeline stage (summarization, clustering, description, auditing) should be upgraded to improve accuracy and reduce hallucination.

2. **Cross-provider adoption** -- The authors advocate for other AI providers to adopt similar transparency frameworks, contributing to an "emerging culture of empirical transparency" in the industry.

3. **Improved rare-event detection** -- Clio struggles with rare but high-impact behaviors; future work should develop complementary methods for detecting low-frequency anomalies.

4. **User intent modeling** -- Current analysis captures conversation content but not underlying user intent or downstream real-world actions; bridging this gap is an open challenge.

5. **Balancing privacy and granularity** -- The inherent trade-off between privacy protection and analytical detail requires ongoing calibration, especially as adversarial users develop more sophisticated evasion techniques.

6. **Community engagement** -- Active collaboration with civil society organizations and policymakers to build trust and ensure the system is not misused for surveillance or civil liberties violations.

---

## Authors & Institutions

Alex Tamkin (equal contribution), Miles McCain (equal contribution), Kunal Handa, Esin Durmus, Liane Lovitt, Ankur Rathi, Saffron Huang, Alfred Mountfield, Jerry Hong, Stuart Ritchie, Michael Stern, Brian Clarke, Landon Goldberg, Theodore R. Sumers, Jared Mueller, William McEachen, Wes Mitchell, Shan Carter, Jack Clark, Jared Kaplan, Deep Ganguli -- all at **Anthropic**.
