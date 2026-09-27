---
type: Research
title: AI coding best practices
description: Evidence-backed best practices for using AI coding assistants for writing, debugging, and refactoring code.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-23T20:54:09Z
focus: What are the evidence-backed best practices for using AI coding assistants for writing, debugging, and refactoring code?
topics:
  - code-generation
  - debugging
  - refactoring
lenses:
  - tech
  - ai
sources:
  processed: 20
  in_kb: 0
  unreachable: 0
runs:
  - { at: 2026-09-23, added: 14 }
  - { at: 2026-09-23, added: 6 }
tags:
  - coding-assistants
  - code-generation
  - debugging
  - refactoring
  - best-practices
---

# AI coding best practices

## How to work through this

1. Start with [overview.md](overview.md) for the cross-cutting synthesis, then [digest.md](digest.md) for the five-move picture.
2. Read the sub-topic digest for your task: [topics/01-code-generation/digest.md](topics/01-code-generation/digest.md) for generation speed, verification, security, and prompting; [topics/02-debugging/digest.md](topics/02-debugging/digest.md) for the repair pipeline and benchmarks; [topics/03-refactoring/digest.md](topics/03-refactoring/digest.md) for refactoring dynamics and review-assistant design.
3. Cite shared findings from [agreements.md](agreements.md); check [disagreements.md](disagreements.md) before citing quality or novice/expert claims, and [open_questions.md](open_questions.md) before generalizing beyond the studied envelope.
4. Pick a lens: [lenses/tech.md](lenses/tech.md) for practitioner guidance, [lenses/ai.md](lenses/ai.md) for builder/evaluator guidance.
5. Trace any claim to its source folder via [sources.md](sources.md) and the per-digest contribution tables; all 20 shortlisted sources are processed and contribute evidence.

## Cross-cutting

- Net value is decided by workflow, not raw generation: 40–55% faster routine drafting paired with a verification tax (up to half of assisted time) plus a security tail (~a quarter of committed Copilot-style snippets with confirmed weaknesses across 43 CWE types).
- Prompting and context engineering move outcomes conditionally: security-aware prefixes, self-critique-and-fix, and analyzer-warning-fed repair cut vulnerabilities substantially on newer models, while vague or coercive phrasing hurts or does nothing and effects vary by model and task.
- Debugging rewards evidence and iteration: on-demand static-dynamic context with runtime traces, budgeted question-driven diagnosis distilled into an explicit repair hypothesis, and up to 3 compile-plus-test refinement rounds (89 → 139 correct Defects4J fixes over three rounds) beat one-shot patching.
- Refactoring and review normalize rather than reinvent: iterative readability refactoring converges diverse inputs toward one stable style (with structural drift and comment loss as the cost), and review assistants confirm judgment or catch missed issues only inside human-led, situational use (proactive summary vs on-demand Q&A).
- Guardrails everywhere: human verification plus tests and static analysis, explicit stopping criteria with comment preservation, concise embedded context-aware tooling, and vigilance against over-trust, false positives, and over-refactoring.
- [[agreements|Agreements]] — 8 shared findings

## Lenses

| lens | for |
| [tech](lenses/tech.md) | software engineers using AI coding assistants in daily development |
| [ai](lenses/ai.md) | AI engineers building and evaluating coding assistants |

## Sub-topics

| sub-topic | in one sentence | sources |
| [01-code-generation](topics/01-code-generation/digest.md) | AI code generation reliably accelerates routine coding work but ships insecure or subtly flawed code often enough that prompt wording, verification, and workflow governance determine its net value. | 13 processed, 0 unreachable |
| [02-debugging](topics/02-debugging/digest.md) | LLM-based debugging and repair now work best when static code context is combined with runtime execution dynamics, structured diagnosis, and validation feedback. | 4 processed, 0 unreachable |
| [03-refactoring](topics/03-refactoring/digest.md) | Iterative LLM readability refactoring converges toward a stable, normalized style and LLM review assistance helps most as a situational human-led aid, but both need guardrails and human verification. | 3 processed, 0 unreachable |

## Sources

| source | kind | folder |
| [Benchmarking prompt engineering for secure code](sources.md#src-02) | primary-research | research_topics/coding_agents/BenchmarkingPromptEngineeringTechniquesForSecureCodeGeneration |
| [LLM code refactoring capability](sources.md#src-01) | primary-research | research_topics/coding_agents/LlmCodeRefactoringCapability |
| [Context engineering for multi-agent assistants](sources.md#src-03) | primary-research | research_topics/coding_agents/ContextEngineeringForMultiAgentLLMCodeAssistantsUsingElicitNotebookLMChatGPTAndClaudeCode |
| [Iterative readability refactoring](sources.md#src-04) | primary-research | research_topics/coding_agents/FromRestructuringToStabilization |
| [Human-AI experience in IDEs](sources.md#src-05) | survey | research_topics/coding_agents/HumanAiExperienceInIntegratedDevelopmentEnvironments |
| [TDD governance for multi-agent generation](sources.md#src-06) | primary-research | research_topics/coding_agents/TddGovernanceForMultiAgentCodeGenerationViaPromptEngineering |
| [Copilot productivity and security survey](sources.md#src-07) | survey | research_topics/coding_agents/GithubCopilotProductivitySecurity |
| [Demystifying Copilot practices](sources.md#src-08) | primary-research | research_topics/coding_agents/DemystifyingPracticesChallengesGithubCopilot |
| [APR and code generation survey](sources.md#src-09) | survey | research_topics/coding_agents/AiDrivenAdvancementsAutomatedProgramRepairCodeGeneration |
| [Copilot practices and challenges](sources.md#src-10) | primary-research | research_topics/coding_agents/PracticesAndChallengesOfUsingGitHubCopilot |
| [Copilot at Zoominfo](sources.md#src-11) | primary-research | research_topics/coding_agents/ExperienceWithGithubCopilotForDeveloper |
| [Influence tactics in prompt framing](sources.md#src-12) | primary-research | research_topics/coding_agents/InfluenceTacticsPromptFraming |
| [DebugRepair](sources.md#src-13) | primary-research | research_topics/coding_agents/DebugRepair |
| [LLM assistants and productivity review](sources.md#src-14) | survey | research_topics/coding_agents/ImpactOfLLMAssistantsOnSoftwareDeveloperProductivity |
| [PracRepair](sources.md#src-15) | primary-research | research_topics/coding_agents/PracRepair |
| [Towards practical APR for debugging](sources.md#src-17) | primary-research | research_topics/coding_agents/TowardsPracticalAndUsefulAutomatedProgramRepairForDebugging |
| [Copilot at ANZ Bank](sources.md#src-16) | primary-research | research_topics/coding_agents/ImpactOfAiToolOnEngineeringAtAnzBank |
| [LLM-assisted code review workflows](sources.md#src-18) | primary-research | research_topics/coding_agents/RethinkingCodeReviewWorkflowsWithLLM |
| [Robustness of code generation](sources.md#src-19) | primary-research | research_topics/coding_agents/OnTheRobustnessOfCodeGenerationTechniques |
| [Security weaknesses of Copilot code](sources.md#src-20) | primary-research | research_topics/coding_agents/SecurityWeaknessesOfCopilotGeneratedCodeInGitHubProjects |
