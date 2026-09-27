[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Productivity Literature Context
**In one sentence:** Follow-up studies find Copilot boosts perceived and measured productivity — high acceptance rates, faster tasks, and more merged pull requests — but results are mixed on code quality, depend strongly on task complexity, and acceptance rate alone is a misleading proxy.
## Key points
- Sobania et al. [14] found Genetic Programming better suited for tasks requiring numerous input/output examples, while Copilot performs well for problems defined through textual descriptions; their study was limited to Python and a small set of files.
- Productivity and code-quality results are mixed [15]: Copilot can generate large portions of code but output quality often falls short and requires extensive debugging, so productivity must be balanced with code quality.
- Acceptance rate correlates strongly with perceived productivity but does not fully reflect developer experience [16], and Copilot does not always shorten task completion time because AI-generated code often needs additional debugging [17].
- Mozannar et al. [18], using data from 535 programmers, proposed a utility-theoretic framework to optimize displaying versus withholding suggestions, found a substantial portion of likely-rejected suggestions could be avoided, stressed the programmer's latent unobserved state, and warned that using acceptance as a reward signal can lead to lower quality suggestions.
- Baralla et al. [19] found Copilot generates functional code and helps routine smart-contract tasks (generation, debugging, testing), excelling at simpler contracts and standard token implementations but weakening on complex contracts with intricate blockchain-specific logic and advanced security considerations.
- ANZ Bank experiment (Chatterjee et al. [20], six weeks): Copilot group completed tasks 42.36% faster than control — beginners 52.27%, intermediates 41.6%, advanced users 40.48%; ZoomInfo evaluation (Bakal et al. [21], 400+ developers): consistent 33% suggestion and 20% lines-of-code acceptance rates with 72% satisfaction, useful for boilerplate but struggling with domain-specific logic.
- GitHub internal experiment (95 participants): Copilot users completed tasks 55% faster; survey of 2,000+ developers: 88% felt more productive, 77% spent less time searching for information, 87% experienced less mental effort on repetitive tasks, 74% could focus on more satisfying work; GitHub–Accenture study [23]: 8.69% increase in pull requests, 15% increase in merge rate, 84% increase in successful builds, ~30% of suggestions accepted, 90% committing Copilot-recommended code, 91% reporting teams merged PRs containing Copilot-suggested code.
---
## Sobania et al.: Copilot vs Genetic Programming
Sobania et al. [14] compared GitHub Copilot with Genetic Programming (GP) for program synthesis in Python. Verbatim finding: "GP is better suited for tasks requiring numerous input/output examples, whereas Copilot performs well for problems defined through textual descriptions." Limitation stated in chunk: study was limited to Python and a small set of files.
## Mixed results on productivity and quality
- General trade-off [15]: "While it can significantly boost productivity by generating large portions of code, the quality of its outputs often falls short, requiring extensive debugging. This underscores the need to balance productivity with code quality [15]."
- Acceptance-rate caveat [16]: "Researchers have observed a strong correlation between Copilot's acceptance rate and perceived productivity but caution that this metric alone does not fully reflect the complexity of developer experiences [16]."
- Completion-time caveat [17]: "While Copilot can improve overall programming efficiency, it does not always shorten task completion time, as AI generated code often requires additional debugging [17]."
## Mozannar et al.: utility-theoretic display framework
Mozannar et al. [18] analyzed data from interactions with GitHub Copilot, proposing a utility theoretic framework to optimize decisions on displaying or withholding suggestions. Based on data from 535 programmers:
- A substantial portion of suggestions likely to be rejected by developers could be avoided.
- Significance of considering a programmer's latent, unobserved state when determining when to present suggestions.
- Using suggestion acceptance as a reward signal for guiding display decisions can lead to lower quality suggestions.
## Baralla et al.: smart contracts on blockchain
Baralla et al. [19] examined Copilot's potential to enhance developer productivity in smart contract development on the blockchain, highlighting capacity to generate functional code, improve efficiency, and assist routine tasks such as code generation, debugging, and testing [19]. Copilot excelled at simpler smart contracts and standard token implementations, accelerating development; performance weakened with more complex contracts, particularly intricate blockchain-specific logic and advanced security considerations — effective for basic tasks but requiring significant human oversight for complicated, security-sensitive scenarios.
## ANZ Bank productivity experiment
Chatterjee et al. [20] reported productivity improvements after Copilot adoption at ANZ Bank. During a six-week experiment, the Copilot group completed tasks 42.36% faster than the control group.

| Group | Improvement vs control |
|---|---|
| Overall | 42.36% faster |
| Beginners | 52.27% improvement |
| Intermediates | 41.6% improvement |
| Advanced users | 40.48% improvement |

## ZoomInfo evaluation
Bakal et al. [21] evaluated Copilot's impact at ZoomInfo with over 400 developers:

| Metric | Value |
|---|---|
| Suggestion acceptance rate | 33% |
| Lines-of-code acceptance rate | 20% |
| Developer satisfaction | 72% |

Copilot proved useful for boilerplate code generation but struggled with domain specific logic [21].
## GitHub internal study: speed and satisfaction
Experiment with 95 participants: developers using Copilot completed tasks 55% faster than those without it. Survey of over 2,000 developers:

| Survey statement | Agreement |
|---|---|
| Felt more productive | 88% |
| Spent less time searching for information | 77% |
| Less mental effort on repetitive tasks | 87% |
| Able to focus on more satisfying work | 74% |

Chunk summary: "This analysis highlights how Copilot enhances speed and improves overall job satisfaction among developers [22]."
## GitHub–Accenture workflow study
Study by GitHub in partnership with Accenture explored daily-workflow integration [23], treating pull-request volume as a value indicator and merge rate as a code-quality measure from maintainers'/coworkers' perspective:

| Metric | Value |
|---|---|
| Increase in pull requests (Accenture developers) | 8.69% |
| Increase in pull request merge rate | 15% |
| Increase in successful builds | 84% |
| Suggestions accepted | ~30% |
| Reported committing Copilot-recommended code | 90% |
| Teams merged PRs containing Copilot-suggested code | 91% |

Chunk conclusion: "This study demonstrated a strong adoption and growing influence within the developer community."
## B. Reflections on literature
- Task Complexity Matters: "Studies suggest that the productivity benefits of Copilot are more noticeable in simpler tasks, whereas complex or domain specific challenges often require additional developer intervention to maintain code quality."
- Quality vs. Speed Trade off: "While accelerated code generation is frequently cited as a key advantage, research indicates that AI generated code often requires extra debugging and validation. This highlights an ongoing need to refine AI tools to better balance speed and code quality."
**Covers:** Follow-up productivity literature (GP comparison, acceptance rates, ANZ/ZoomInfo/GitHub studies) plus Section B reflections on task complexity and quality-vs-speed.
