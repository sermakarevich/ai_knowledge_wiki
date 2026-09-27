# Future Work Directions: Audit, Personalization, Verification, and IDE Redesign

> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

**In one sentence:** The reviewed papers propose larger and longer evaluations, stronger audit and verification assets, broader life-cycle coverage, and adaptive assistance that is explainable and under user control.

## Key points
- Productivity proposals connect gains to interface and workflow choices, calling for concrete design changes and controls plus accounting for project and environment factors.
- Audit proposals seek wider security coverage over time: expanded vulnerability categories and language coverage, longitudinal tracking, targeted test suites and benchmarks, and more unit tests and quality metrics.
- Prompting proposals center on structured conversational prompting with refinement aids, comparative evaluation of prompt-engineering strategies, multi-modal channels, and prompt sanitization with privacy-aware feedback.
- Personalization proposals call for user models keyed to profile, expertise and task state, including frequency/snooze controls, adaptive strategies responding to real-time performance, and style- and context-matched results.
- Verification proposals concentrate on checking outputs before adoption via automatic test generation, reference-example retrieval, post-processing/filtering layers, and multi-alternative comparison interfaces.
- Explainability, trust, and control proposals ask for rationales and code-level explanations, studies of community trust recalibration and interface-driven trust shifts, and richer controls over generation and automation levels.
- IDE and life-cycle proposals argue for AI-aware environments (non-linear input, sketch merging, chat control, edit propagation, memory management and dynamic prompts) and tooling beyond implementation across requirements, design, debugging, testing, deployment, and search.

---

## Fig. 7: co-occurrence of future-work Topic by Method

Paper IDs are plotted for co-occurrence between Topic on the y-axis and Method on the x-axis for suggested future work. Topics on the y-axis include: Productivity; Audit of AI code; Design of AI; Skill-building; Prompting; Trust; Personalization; IDE redesign; Verification; SDLC stages; Explainability; Education with AI; Proactivity; Context enrichment; Mental models; User control.

**Covers:** Fig. 7 caption and axes (future-work Topic × Method co-occurrence)

## Productivity and workflow design

Several papers connect productivity to interface and workflow choices and propose concrete design changes and controls (Ziegler et al., 2022; Angert et al., 2023; Rasnayaka et al., 2024; Ságodi et al., 2024; Pandey et al., 2024; Amoozadeh et al., 2024; Nam et al., 2023; Jiang and Coblenz, 2024). Papers also call to account for project and environment factors (Peng et al., 2023; Feldman and Anderson, 2024; Zhou et al., 2025b).

**Covers:** pp. 22–23, productivity future-work paragraph

## Audit of AI-generated code

Future work on auditing AI-generated code seeks wider security coverage, longitudinal observation, and stronger assets for evaluation. Proposals include expanding vulnerability categories and language coverage and tracking change over time (Pearce et al., 2022; Asare et al., 2023, 2024), building targeted test suites and benchmarks (Liu et al., 2024), and increasing unit tests and quality metrics to stress code quality (Yetistiren et al., 2022; Liu et al., 2024). Some papers extend audits to SDLC touchpoints and to interfaces that surface risk at decision time (Liang et al., 2024; Asare et al., 2024; Liu et al., 2024; Kruse et al., 2024; Pearce et al., 2022; Vasconcelos et al., 2025).

**Covers:** p. 23, audit future-work paragraph

## Prompting support

Prompting support centers on guided interactions and safe practice. Suggestions include structured conversational prompting and refinement aids (Jiang et al., 2022; Angert et al., 2023), prompt engineering strategies with comparative evaluation (Pearce et al., 2022; Denny et al., 2023; Mastropaolo et al., 2023; Fagadau et al., 2024), multi-modal prompt channels for tasks that are not purely textual (Angert et al., 2023), and prompt sanitization with privacy-aware feedback (Li et al., 2024). Authors also ask for generalization across tools and settings (Fagadau et al., 2024).

**Covers:** p. 23, prompting future-work paragraph

## Personalization

Personalization proposals focus on adapting assistance to user profiles, expertise, and task state. Examples include user models to personalize initial prompts and responses (Ross et al., 2023a; Chopra et al., 2024), frequency and snooze controls to manage attention (Vaithilingam et al., 2023), adaptive strategies that respond to real time performance and needs (Kazemitabaar et al., 2025), and results that better match the intended coding context and style (de Moor et al., 2024; Liu et al., 2024; Sahoo et al., 2024; Cheng et al., 2024b; Mozannar et al., 2024c; Vasconcelos et al., 2025). Several papers request tailored documentation and scaffolds for specific roles such as data analysts (Wang et al., 2022; Gu et al., 2024).

**Covers:** p. 23, personalization future-work paragraph

## Explainability and transparency

Explainability and transparency aim to help users understand, validate, and teach the assistant. Suggested mechanisms include rationales, annotations, and code level explanations (Vaithilingam et al., 2022; Hu et al., 2022; McNutt et al., 2023), interpretability features that support accurate mental models and calibrated expectations (Weisz et al., 2022; Jiang et al., 2022; Sun et al., 2022; Bird et al., 2022), internal deliberation to improve reasoning quality (Ross et al., 2023b), and presentation of validation evidence such as testing suite results or multi model checks (Omidvar Tehrani et al., 2024; Yan et al., 2024).

**Covers:** p. 23, explainability future-work paragraph

## Verification support

Verification support concentrates on tools that help users check and repair outputs before adoption. Proposals include automatic test generation and retrieval of reference examples (Vaithilingam et al., 2022; Ferdowsi et al., 2024), post processing and filtering layers that repair or block risky outputs (Pearce et al., 2022; Al Madi, 2022; Ferdowsi et al., 2024), interface patterns that present multiple alternatives for comparison (Weisz et al., 2022), and study designs that measure how learners verify AI suggestions and develop durable checking habits (Kazemitabaar et al., 2023b,a).

**Covers:** p. 23, verification future-work paragraph

## Coverage beyond implementation (SDLC stages)

Coverage beyond the implementation stage remains a consistent request. Papers propose research and tooling for requirements, design, evolution, debugging, testing, deployment, and code search across the life cycle (Nguyen and Nadi, 2022; Liu et al., 2024; OBrien et al., 2024; Chopra et al., 2024; Ferdowsi et al., 2024; Vasconcelos et al., 2025). Many of these suggestions pair life cycle scope with deeper integration into the developer workspace (Chopra et al., 2024; Ferdowsi et al., 2024).

**Covers:** pp. 23–24, SDLC-coverage future-work paragraph

## Trust and reliability

Trust and reliability suggestions examine individual and community factors as well as interface effects. Authors ask for studies of how communities and organizations form and recalibrate trust over time (Cheng et al., 2024a; Prather et al., 2024), for quantification of interface-driven trust shifts (Wang et al., 2024), for evaluations that measure the impact of assistant behavior changes on acceptance (Feldman and Anderson, 2024), and for approaches that foster appropriate trust with clear boundaries (Ferdowsi et al., 2024). Inclusion of diverse developer groups appears throughout (Vaithilingam et al., 2022; Hu et al., 2022; Ross et al., 2023a).

**Covers:** p. 24, trust future-work paragraph

## IDE redesign and context enrichment

Proposals on IDE redesign and context enrichment argue for AI-aware environments. Suggestions include non-linear input and new interaction media (McNutt et al., 2023), improved error handling and better merging of sketch-like artifacts (Angert et al., 2023), chat or dialogue interfaces for automation control (Shlomov et al., 2024), and consistent propagation of edits and assumptions (Kazemitabaar et al., 2024a). For context, papers recommend memory management, dynamic prompts that reflect project artifacts, and search-based integrations (Ross et al., 2023b; Wang et al., 2023b; Ross et al., 2023a; Shlomov et al., 2024).

**Covers:** p. 24, IDE-redesign and context-enrichment paragraph

## Mental models, proactivity, user control, governance

Less frequent but important themes include user mental models, proactivity, user control, and governance. Future work asks for theory building on how developers form and use mental models of assistants and for longitudinal observation of expectation change (Nguyen and Nadi, 2022; Lau and Guo, 2023; Asare et al., 2023; Zhu et al., 2024; Amoozadeh et al., 2024). Proactivity-related suggestions seek predictive models of user state and careful study of long-term effects on quality of code and productivity (de Moor et al., 2024; Mozannar et al., 2024a,b). User control-oriented suggestions call for clearer and richer controls over generation and automation levels (Yen et al., 2023; Feng et al., 2024; Wang et al., 2024). Governance suggestions raise questions about fairness, access, and alignment, including alignment toward helpful and harmless behavior and possible career impacts for different demographic groups (Ross et al., 2023a; Feldman and Anderson, 2024; Peng et al., 2023).

**Covers:** p. 24, cross-cutting-themes paragraph

## Synthesis and discussion framing

> "Taken together, these directions indicate the need for larger and longer evaluations, stronger audit and verification assets, broader life cycle coverage, and adaptive assistance that is explainable and under user control."

The discussion of the systematic literature review of 90 in-IDE HAX studies is organized around topics coverage and gaps (RQ1), implications for practice and research (RQ2), and a future work agenda (RQ3).

**Covers:** p. 24, synthesis sentence + Section 4 Discussion opening
