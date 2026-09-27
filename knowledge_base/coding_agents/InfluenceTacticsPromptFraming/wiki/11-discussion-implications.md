> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Discussion and Implications
**In one sentence:** Influence-tactic framing does not strongly change correctness or maintainability but can subtly alter code form, with model choice mattering far more, pressure-based phrasing carrying the main correctness/security cost, and overall effects remaining minor but non-negligible.
## Key points
- Prompt framing does not strongly determine correctness or maintainability, but can subtly alter the form of the code, such as its length or explanatory detail.
- LLM choice had a far greater impact than tactic on nearly every metric — correctness, maintainability, security, complexity, and commenting — across both benchmarks.
- Qwen 3 and Llama 4 consistently outperformed others on correctness and Bandit security, while some models were more verbose or produced cleaner PyLint outputs.
- Qualitatively, prompts framed with legitimating or ingratiation tactics more often contained error handling, but the patterns did not conclusively show that tactics alone drive the changes.
- Quantitatively, influence tactics had minimal effects on maintainability, complexity, commenting, and static quality metrics such as PyLint across LiveCodeBench and SWE-Bench Verified.
- Pressure-based phrasing was the main caution: associated with lower correctness, more security warnings, or increased verbosity, and with less secure outputs even in this benign-task setting.
- Prior adversarial/social-engineering work cited shows persuasion tactics can exceed 92% success in jailbreak/manipulation tasks, suggesting the modest effects here reflect benign framings and constrained code-generation tasks rather than inherent LLM insensitivity.
---
## Stylistic effects — Implication 2
> "Prompt framing may modestly influence stylistic features of generated code, such as verbosity or commenting behaviour, though these effects are subtle and context dependent. Developers could cautiously use prompt framing to tailor stylistic features of generated code, which may be beneficial when generating templates, documentation-heavy outputs, or onboarding materials, but should not rely on it as a consistent or reliable method for controlling output style."

## LLM choice matters more than tactic — Implication 3
Across both benchmarks, LLM choice had a far greater impact than tactic on nearly every metric, including correctness, maintainability, security, complexity, and commenting. Qwen 3 and Llama 4 consistently outperformed others on correctness and Bandit security, while some models were more verbose or produced cleaner PyLint outputs.
The chunk attributes this to architectural and training differences overshadowing prompt variations, aligning with literature showing dominant effects of model size, training data quality, and instruction tuning [18]. Influence tactics are described as acting "more like nudges whose effects are only visible in models that are particularly sensitive to linguistic nuance," with robust high-baseline-correctness architectures less affected.
> "Software developers should prioritize model selection over prompt framing when optimizing for correctness or reliability, especially in high-stakes settings. However, prompt style remains a meaningful layer of control, particularly for teams who are locked into specific LLM APIs but need to fine-tune output style or surface-level features."

## Emergent qualitative patterns — Implication 4
Qualitative analysis revealed notable behavioural differences by tactic, suggesting LLMs are somewhat sensitive to influential framing and that tactics may alter completeness, reliability, and verbosity. Prompts framed with legitimating or ingratiation tactics more often contained error handling in the generated responses.
The chunk cautions that the patterns did not conclusively demonstrate tactics alone drive these changes, since temperature settings or dataset context could interact with framing, and future work is needed to isolate causal effects.
> "Researchers studying prompt engineering, human-LLM collaboration, or AI alignment, should consider influence framing as a potentially meaningful dimension in shaping model output."

## Limited overall impact and broader reassurance
Quantitative analysis found minimal effects of influence tactics on maintainability, complexity, commenting, and static code quality metrics (e.g., PyLint) across LiveCodeBench and SWE-Bench Verified. The chunk interprets this as LLMs exhibiting "greater resistance to superficial linguistic manipulation than might be expected," offering reassurance that tactic-like phrasing does not broadly degrade generated code, except for the pressure-based caution above.
Scope caveat: the study covers code generation with non-adversarial framings. Cited adversarial/social-engineering research [13,52] shows social-science persuasion tactics such as logical appeals, impersonation, or emotional urgency can achieve "remarkably high success rates (over 92%) in jailbreak and manipulation tasks." The chunk notes pressure-based framings being linked to less secure outputs aligns with prior work on coercive or emotionally charged language, and that pragmatic-framing effects may be highly task-dependent — stronger in open-ended or adversarial settings than in constrained code generation with strict correctness criteria.

## Conclusion (§6)
The work is presented as "the first empirical investigation into how psychologically inspired influence tactics, when embedded in prompts, affect LLM-generated code," translating organizational-psychology communication strategies into controlled framings and assessing functional, maintainability, stylistic, and security properties across two complementary benchmarks. The mixed-methods evaluation shows a "mixed and context-dependent pattern": most maintainability and static quality metrics were not strongly affected, while pressure-oriented framings were associated with lower correctness and more security warnings in LiveCodeBench and increased verbosity in SWE-bench Verified.
Practical recommendations stated in the chunk:
- Avoid coercive or urgency-based prompt wording when correctness or security is valued.
- Other tactics may shape surface-level or explanatory features, but too modestly to be a reliable improvement method.
- Overall, prompt framing is "a minor but non-negligible factor," with model choice and task difficulty exerting stronger effects; behaviour changes also raise consistency, fairness, and reliability concerns, and future work should isolate causal mechanisms and how influence-based prompting can increase functional correctness and trustworthiness.

## Acknowledgements and declarations (§7–§8)
- Acknowledgements (§7): thanks to Shikari King and Jordi Capdevila Masó for valuable contributions during initial brainstorming and conceptualization.
- Funding (§8.1): partially supported by NSERC 2021 AWD-021280.
- Ethical Approval (§8.2) / Informed Consent (§8.3): not applicable; no human participants, no human or personally identifiable data collected or analyzed.
- Author Contributions (§8.4): Alex Deaconu — conception/design, co-designed and implemented RQ1/RQ2 under Last Author supervision, framework and experimental design, writing/revision; Anubhav Gupta — co-designed/implemented RQ1/RQ2, framework, RQ3 qualitative design/analysis, writing/revision; Manaal Basha — statistical analyses for RQ1/RQ2, writing/revision; Nicholas Haydu — conception/early ideation, validated LLM outputs for RQ1/RQ2; Gema Rodríguez-Pérez — conception/design, supervised RQ1/RQ2, co-designed/participated in RQ3 qualitative analysis, framework, writing/revision; all authors read and approved the final manuscript.
- Data Availability (§8.5): all scripts, datasets, and supplementary materials publicly available in replication package [16].
- Conflict of Interest (§8.6): none declared. Clinical Trial Number (§8.7): not applicable.

**Covers:** Discussion Implications 2–4 and Limited Overall Impact; §6 Conclusion; §7 Acknowledgements; §8.1–§8.7 Declarations (pp. 31–33)
