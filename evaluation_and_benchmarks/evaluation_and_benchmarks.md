# Evaluation & Benchmarks

Research on **benchmarks, evaluation methodologies, verifiers, and empirical head-to-head comparisons** of LLMs and agent systems.

## Papers

- [[AgenticAIEvaluationsSE/summary]] — SE agentic AI papers lack reproducibility; sharing TAR trajectories enables cheap post-hoc behavioral comparison.
- [[AiScientistsWithoutReasoning/summary]] — Corral framework analyzes LLM scientific agents' reasoning graphs; base model explains 41% of success variance, scaffold only 1.5%; evidence ignored in 68% of traces.
- [[BenchmarkingAgenticSkillsInTheWild]] — Skill benefits degrade under real retrieval; weaker models perform worse with irrelevant skills than none.
- [[DrBencher/summary]] — Synthetic benchmark requiring multi-hop entity ID + numerical computation; Opus 4.6 gets 86% ID but only 20% final answer.
- [[GymAnything]] — Auto-generates 10k+ computer-use tasks across 200 GDP-grounded apps; frontier models achieve only ~23%.
- [[ITestedMetaMuseSparkAgainst4FrontierModels]] — 3-task frontier comparison; Muse Spark wins overall but fails 3D rendering; quality metrics inversely correlate with function.
- [[LongHorizonTaskMirage/summary]] — HORIZON benchmark: LLM agents don't degrade linearly on long tasks — they hit a cliff via planning/memory failures.
- [[PredictionArenaBenchmarkingAiModelsOnRealWorldPredictionMarkets/summary]] — All Cohort 1 LLMs lost money on real-capital prediction markets; settlement accuracy predicts success.
- [[SkillsBenchBenchmarkingHowWellAgentSkillsWorkAcrossDiverseTasks]] — First agent skills benchmark across 86 tasks; curated skills +16pp, self-generated give no benefit.
- [[TauKnowledgeEvaluatingConversationalAgentsOverUnstructuredKnowledge]] — 700-doc retrieval + tool discovery + policy-compliant action benchmark; best model achieves 25.5%.
- [[TheArtOfBuildingVerifiersForComputerUseAgents/summary]] — Universal Verifier: rubric-based, screenshot-grounded verification with near-zero false positives.
