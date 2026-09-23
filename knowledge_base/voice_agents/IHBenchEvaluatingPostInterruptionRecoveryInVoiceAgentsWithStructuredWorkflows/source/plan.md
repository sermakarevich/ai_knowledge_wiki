# Plan — IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows

Source: https://arxiv.org/abs/2606.19595 (kind pdf, fetched via pdftotext 2026-09-22)
Paper dir: /Users/sergii/.ai/knowledge/research/IHBenchEvaluatingPostInterruptionRecoveryInVoiceAgentsWithStructuredWorkflows

Chunk slug → planned wiki page. Covers notes are inferred from chunk index/slug/title only (bodies not read).

| Chunk slug | Wiki page | Covers |
|---|---|---|
| 01-ihbench-evaluating-post-interruption-recovery-in | 01-overview.md | Paper abstract, benchmark goal, and contributions |
| 02-1-introduction-these-benchmarks-answer-an | 02-introduction.md | Motivation, voice-interruption problem, good vs bad recovery examples |
| 03-2-prerequisites-conversation-synthesis | 03-benchmark-design-overview.md | Data-generation pipeline overview, prerequisites and synthesis stages |
| 04-spoken-task-success-across-enterprise-domains | 04-related-work.md | Related full-duplex, voice-agent, and synthetic-benchmark work |
| 05-3-correction-the-user-corrects-something | 05-interruption-types.md | Six interruption types and their type-specific recovery requirements |
| 06-gpt-realtime-2-medium-728-03-624-04 | 06-evaluation-methodology.md | Two-axis scoring: comparative task fulfillment and absolute recovery quality |
| 07-5-figure-3-plots-the-per-model | 07-overall-results.md | 27-model results, TF win rate and RQ pass rate with judge comparison |
| 08-0-i-i-ral-ni-i | 08-judge-agreement.md | Inter-judge robustness and human-annotator agreement validation |
| 09-1-sided-tests-tost-procedure-34 | 09-statistical-analysis.md | Significance testing, degradation with conversation depth, modality gap |
| 10-7-post-interruption-recovery-is-a | 10-findings-discussion.md | Key findings, recovery quality as a distinct capability axis |
| 11-8-17-kimiteam-ding-ding-zeqian | 11-references.md | References and cited models, benchmarks, and systems |
| 12-other-rater-table-2-dataset-statistics | 12-dataset-statistics.md | Dataset statistics, domain coverage, interruption-type distribution |
| 13-dered-as-audio-in-the-task | 13-audio-pipeline.md | Audio synthesis pipeline, TTS normalization and ASR verification |
| 14-rq-pass-rate-our-27-model | 14-per-type-results.md | Per-interruption-type breakdowns, closed vs open-weight comparison |
| 15-14-skip-conditions | 15-workflow-structure.md | State-machine workflows, stages, skip/failure and termination conditions |
| 16-1-fresh-start-the-response-does | 16-rubric-design.md | Per-interruption rubrics, task-fulfillment and recovery-quality criteria |
| 17-16-you-are-writing-a-system | 17-system-prompts.md | Simulator system prompts and knowledge-base construction details |
| 18-17-user-plan-should-reveal-hidden-info | 18-user-simulation.md | User intent profiles, round planner, hidden-information handling |
| 19-i-4-user-simulator-the-normal-branch | 19-simulator-branches.md | Normal vs interruption simulator branches and utterance generation |
| 20-20-1-apply-only-the-changes | 20-verification-modifier.md | Post-hoc verifier checks, modifier fix loop, discard policy |
