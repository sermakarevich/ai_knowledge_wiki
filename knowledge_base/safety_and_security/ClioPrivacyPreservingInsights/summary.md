# Clio: Privacy-Preserving Insights into Real-World AI Use

**Paper:** [Clio: Privacy-Preserving Insights into Real-World AI Use (Tamkin, McCain et al., 2024)](https://arxiv.org/abs/2412.13678)
**Deep dive:** [[details]]
**Code sandbox:** [[sandbox/README]]

## Human Readable TL;DR

Imagine you run a popular help desk where millions of people ask questions every day. You want to understand what people are asking about -- are they mostly asking about cooking, homework, or car repairs? But you also want to protect everyone's privacy and not read their individual messages. Clio is like a smart filing system that automatically sorts all those questions into categories and shows you the big picture ("20% cooking, 15% homework") without ever letting anyone see a specific person's question. It even catches patterns of misuse -- like someone trying to use the help desk for scams -- all while keeping individual conversations private.

## TL;DR

Clio is a privacy-preserving platform from Anthropic that uses LLMs to analyze millions of Claude.ai conversations at scale without human review of raw data. It employs a multi-stage pipeline of facet extraction, semantic clustering, hierarchical organization, and interactive visualization. Applied to one million conversations, it revealed that coding, writing, and research dominate usage, identified cross-language behavioral differences, and detected coordinated misuse patterns including SEO spam and unauthorized API reselling.

---

## Problem & Motivation

Despite widespread deployment of AI assistants, there is remarkably little public data on how these systems are actually used. Understanding real-world usage is critical for AI safety, governance, and product improvement, but is blocked by three barriers: (1) **privacy** -- users share sensitive personal and business information in conversations, (2) **scale** -- millions of daily interactions make manual review impossible, and (3) **competitive pressure** -- providers are reluctant to disclose usage data. Existing public datasets (WildChat, LMSYS-Chat-1M) come from specific platforms and crowdworkers, not representative production traffic. Clio addresses all three barriers simultaneously.

---

## Main Original Ideas

1. **LLM-as-Analyst Pipeline** -- Uses Claude models themselves to extract facets, cluster conversations, generate cluster descriptions, and audit privacy, replacing human review entirely while maintaining 96% summarization accuracy.

2. **Defense-in-Depth Privacy Architecture** -- Four layered privacy protections: PII-free summarization, cluster aggregation thresholds (minimum unique accounts/conversations), privacy-preserving cluster descriptions, and automated privacy auditing (98% accuracy), reducing detectable private information from 10% to undetectable levels.

3. **Bottom-Up Unknown-Unknown Discovery** -- Instead of testing for pre-defined risks (red-teaming), Clio discovers unanticipated usage patterns and novel misuse through unsupervised clustering, enabling detection of threats that no one thought to look for.

4. **Hierarchical Interactive Exploration** -- Multi-level cluster hierarchy with UMAP map view, tree view, faceted breakdowns, and temporal analysis, enabling analysts to navigate from broad categories down to specific behavioral patterns.

5. **Safety Classifier Calibration** -- By cross-referencing automated classifier flag rates with model-generated concern scores, Clio identifies both false positives (over-blocking innocuous content) and false negatives (missed harmful content), enabling targeted classifier improvement.

---

## Key Findings

| Metric | Value |
|--------|-------|
| Conversation summary accuracy | 96% (93% random, 98% concerning) |
| Concern score correlation (Spearman) | 0.84 |
| Base-level cluster title accuracy | 97-99% |
| Cluster misassignment rate | 3% |
| Hierarchical cluster accuracy | 97% |
| Supervised reconstruction (regular) | 94% |
| Supervised reconstruction (concerning) | 84% |
| Multilingual accuracy (15 languages) | >92% all languages |
| Privacy auditor accuracy | 98% |
| Raw PII rate -> final PII rate | 10% -> undetectable |

- **Dominant use cases:** Web/mobile app development (>10%), writing assistance, academic research, educational content
- **Cross-language differences:** Japanese and Chinese conversations showed disproportionately higher rates of elder care, economic issues, and anime/manga content
- **Coordinated misuse detected:** Automated SEO spam networks, explicit content generation rings using identical prompt structures, unauthorized Claude API reselling
- **Classifier insights:** False positives on job advice, security programming questions, D&D combat stats; false negatives on translated explicit content and uncensored novel requests

---

## Suggestions & Future Directions

1. **Continuous refinement** of privacy protections and evaluations using latest Claude models as they improve
2. **Broader adoption** of privacy-preserving monitoring frameworks across the AI industry to foster an "emerging culture of empirical transparency"
3. **Improved rare-event detection** -- Clio currently struggles with low-frequency but high-impact behaviors; future work should address this sensitivity gap
4. **Cross-provider collaboration** -- Sharing methodologies (not raw data) to enable industry-wide understanding of AI usage patterns
5. **Integration with governance frameworks** -- Using empirical usage data to bridge the gap between theoretical ethical frameworks and practical AI policy
6. **User trust calibration** -- Addressing the tension between monitoring necessity and user perception of surveillance through radical transparency and civil society engagement

---

## Authors & Institutions

Alex Tamkin*, Miles McCain* (equal contribution), Kunal Handa, Esin Durmus, Liane Lovitt, Ankur Rathi, Saffron Huang, Alfred Mountfield, Jerry Hong, Stuart Ritchie, Michael Stern, Brian Clarke, Landon Goldberg, Theodore R. Sumers, Jared Mueller, William McEachen, Wes Mitchell, Shan Carter, Jack Clark, Jared Kaplan, Deep Ganguli -- all at **Anthropic**.
