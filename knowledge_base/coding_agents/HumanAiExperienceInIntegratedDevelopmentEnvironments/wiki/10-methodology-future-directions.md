[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Methodology, Validity, and Future Directions
**In one sentence:** Across 90 studies with a median of 17 participants, the review finds in-IDE HAX research underpowered and short-term, and recommends justified sample sizes, preregistration, open sharing, and industry collaboration alongside broader tool, lifecycle, and longitudinal coverage.
## Key points
- Sample sizes are often underpowered and rarely justified, with a median of 17 participants across the corpus.
- HCI benchmarks cited (Caine, 2016): most common sample size 12 and median 18; in-person median 15, remote median 77 — many quantitative studies at these sizes will be underpowered and benefit from replication.
- Recommended rigor: a priori power analysis for confirmatory comparisons, saturation arguments for qualitative designs, and explicit reporting of recruitment constraints.
- Recommended openness: versioned repositories with study materials and data where feasible — codebooks, prompts, task descriptions, analysis scripts, deidentified datasets with metadata and data dictionary — plus preregistration, blinding, randomization when appropriate, and transparency checklists recording methodology, exclusion criteria, and data-sharing plans.
- Academic–industry collaboration is recommended to improve recruitment and enable longitudinal, ecologically valid evaluations, balancing industrial 1–2 month feedback horizons with academic standards.
- Research to date concentrates on a small set of tools (most often GitHub Copilot) and the implementation SDLC stage, leaving requirements, testing, and deployment underexplored; future work should diversify assistants, cover earlier and later lifecycle stages, and prioritize longitudinal and comparative designs.
- Review-level threats acknowledged: sampling bias (recall-oriented query biased toward professional contexts), temporal bias (2022–2024 window), source reliability (including non-peer-reviewed ArXiv papers), interpretation bias in categorizing a large corpus, and industry time-factor constraints on statistical significance.
---
## Methodological and open science recommendations
**Covers:** Methodological and open science recommendations section

Sample sizes "are often underpowered and rarely justified. The median is seventeen participants." Context from prior studies: "for HCI practice, the most common sample size is twelve and the median is eighteen; in-person studies have a median of fifteen, while remote studies have a median of seventy-seven (Caine, 2016)." Consequence stated verbatim: "Although many quantitative studies at these sizes will be underpowered and therefore benefit from replication."

Recommendations, verbatim in substance:
- "We recommend a priori power analysis for confirmatory comparisons and saturation arguments for qualitative designs, with explicit reporting of recruitment constraints."
- "Collaboration between academia and industry can improve recruitment and enable longitudinal assets."
- "To support replication, we recommend sharing versioned repositories with study materials and data where feasible, including codebooks, prompts, task descriptions, analysis scripts, and deidentified datasets with clear metadata and a data dictionary."
- "We also recommend using preregistration, blinding, and randomization when appropriate, and embedding transparency checklists that record methodology, exclusion criteria, and data sharing plans."

## Takeaways
**Covers:** Takeaways section

Verbatim takeaways:
- "Treat verification as a main part of the interaction with AI assistants, keeping tests, static analysis, and reference examples inside the editor and by surfacing runtime evidence to support calibrated acceptance decisions."
- "Evaluate the effect beyond time spent on the task by reporting acceptance, edits, and verification effort."
- "Design AI assistance as a hybrid of autocompletion and conversation that shares context, offers brief explanations, and scope controls at decision time."
- "Structure educational use of AI in IDEs with staged contribution of AI, stepwise reveal of its suggestions, and controls for their quick checks."
- "For studies, report the SDLC stage and expand coverage of tasks completed with AI to early and late stages."
- "Strengthen methodological rigor through justified sample sizes, preregistration where appropriate, transparent reporting, and collaboration with industry for larger, ecologically valid, and longitudinal evaluations."

## Threats to validity (§4.1)
**Covers:** §4.1 Threats to the Validity

- Sampling Bias: "Despite efforts to include well-known libraries and refine the search string, the possibility of sampling bias remains." Recall-oriented query "can bias the pool toward professional contexts, since educational deployments do not always occur inside full IDEs or are indexed under alternative platforms." Mitigations: "including multiple synonyms where supported and by manually screening every record for the inclusion criterion" and "we provide our search protocol to mitigate this threat."
- Temporal Bias: "The chosen time frame (papers published between 2022 and 2024) introduces a potential temporal bias, excluding earlier works." Rationale: "driven by the intention to focus on contemporary developments following the advent of LLMs."
- Source Reliability: "Inclusion of non-peer-reviewed papers from ArXiv introduces concerns regarding the reliability of findings, given the absence of a formal peer-review process." Justification: "deemed it necessary to consider insights from ArXiv due to the dynamic and rapidly evolving nature of the field"; screening via "examining titles, abstracts, and full texts ensured that all included works contributed meaningfully"; plus "the open publication environment of ArXiv encourages the publication of negative or null results, contributing to a more balanced representation."
- Interpretation Bias: "Analyzing a large amount of information can introduce interpretation bias and impact the way studies are categorized." Transparency response: "we emphasize transparency and provide the entire dataset (Sergeyuk et al., 2025) for the readers."
- Industry-related challenges: in-IDE HAX research "faces unique challenges due to its close ties with the industry and professional context"; the "time factor" — "Industrial sponsors and participants often have short time horizons. They expect valuable feedback within 1-2 months of research, so that they could make timely business decisions." Practical constraint: "sometimes make it challenging to prioritize statistical significance. Analyzing immediate trends and patterns can be sufficient for them." Prescription: "By fostering a collaborative environment, we can develop strategies that balance the demands of industrial collaboration with the standards of academic research."

## Conclusion (§5)
**Covers:** §5 CONCLUSION (pp. 28–29)

"This review offers a structured synthesis of current research on AI-powered assistance in integrated development environments. Drawing on 90 studies, we identified dominant trends, conceptual gaps, and methodological characteristics of the emerging field of in-IDE HAX."

Findings restated: research "focuses heavily on a small set of tools, most often GitHub Copilot, and concentrates primarily on the implementation stage of the SDLC," producing "early insights into how developers engage with AI assistance during code writing and modification" but leaving "requirements analysis, testing, and deployment underexplored."

Future directions stated: "investigate diverse AI assistants across varied development environments, extend coverage to earlier and later lifecycle stages, and prioritize longitudinal and comparative designs that capture how practices and their impact evolve over time"; "support personalization and trust calibration, reduce validation burden, and address broader quality and governance concerns"; methodological note: "studies tend to prioritize short-term evaluations, often with underpowered samples and limited contextual variation" and "advancing cumulative evidence will require the adoption of robust empirical practices and closer collaboration across research groups."

Closing: "the reviewed literature demonstrates growing interest in the integration of AI into developer tools but also highlights the need for deeper empirical grounding, broader tool coverage, and stronger methodological foundations."

Context notes from chunk (no new claims): work conducted as part of the AI for Software Engineering (AI4SE) collaboration between JetBrains and Delft University of Technology, supported by JetBrains Research; ethical approval / informed consent / clinical trial number "Not applicable"; "All data are available in our supplementary materials (Sergeyuk et al., 2025)"; authors declare no conflict of interest.
