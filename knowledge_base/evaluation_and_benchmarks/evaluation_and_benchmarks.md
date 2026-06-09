# Evaluation & Benchmarks

Research on **benchmarks, evaluation methodologies, verifiers, and empirical head-to-head comparisons** of LLMs and agent systems.

## Papers

- [[AgenticAIEvaluationsSE/summary]] — SE agentic AI papers lack reproducibility; sharing TAR trajectories enables cheap post-hoc behavioral comparison.
- [[AgenticReproductionSocialScience/summary]] — Four-step agentic pipeline reproduces social-science papers' results from text + raw data alone (no original code); best agent (OpenCode + GPT-5.4) hits 91% sign agreement across 48 papers; dominant failure mode is paper underspecification, not agent error.
- [[AgentsLastExam/summary]] — 1,490 real-world professional tasks across 55 digital industries; frontier agents average 2.6% on the hardest tier; model capability matters 3× more than harness choice.
- [[AIPlanningFrameworkForLLMWebAgents/summary]] — Maps LLM web-agent architectures to classical AI planning paradigms (BFS/best-first/DFS); introduces five trajectory metrics beyond binary success and a 794-task human-annotated WebArena dataset.
- [[AiScientistsWithoutReasoning/summary]] — Corral framework analyzes LLM scientific agents' reasoning graphs; base model explains 41% of success variance, scaffold only 1.5%; evidence ignored in 68% of traces.
- [[AlphaEvalEvaluatingAgentsInProduction/summary]] — Production-grounded benchmark of 94 tasks across 6 occupational domains; best agent (Claude Code + Opus 4.6) scores 64.41/100; scaffold impact rivals model choice.
- [[BenchmarkingAgenticSkillsInTheWild]] — Skill benefits degrade under real retrieval; weaker models perform worse with irrelevant skills than none.
- [[DrBencher/summary]] — Synthetic benchmark requiring multi-hop entity ID + numerical computation; Opus 4.6 gets 86% ID but only 20% final answer.
- [[GymAnything]] — Auto-generates 10k+ computer-use tasks across 200 GDP-grounded apps; frontier models achieve only ~23%.
- [[ITestedMetaMuseSparkAgainst4FrontierModels]] — 3-task frontier comparison; Muse Spark wins overall but fails 3D rendering; quality metrics inversely correlate with function.
- [[KnowMeBench/summary]] — Benchmark for evidence-grounded person understanding from long-horizon autobiographies; current memory systems (RAG, Mem0, MemOS) cap at ~22% on psychoanalytic insight tasks.
- [[LLMsCorruptDocumentsDelegation/summary]] — DELEGATE-52 benchmark across 52 professions with Round-Trip Relay Simulation; all 19 tested LLMs degrade documents over time — frontier models corrupt ~25% after 20 interactions.
- [[LOCOMOLongTermConversationalMemory/summary]] — Large-scale benchmark for very long-term conversational memory (~300 turns, 35 sessions); persona-driven event graphs with multimodal turns; observation-based RAG beats raw dialogue, but all models trail humans.
- [[LongHorizonTaskMirage/summary]] — HORIZON benchmark: LLM agents don't degrade linearly on long tasks — they hit a cliff via planning/memory failures.
- [[LongMemEval/summary]] — Benchmark for five long-term memory abilities of LLM chat assistants; commercial systems drop 30–64% accuracy; unified indexing-retrieval-reading framework with fact-expanded keys and time-aware queries substantially recovers performance.
- [[MeasuringAgentsInProduction/summary]] — First large-scale empirical study of production LLM agents: 20 case studies + 306-practitioner survey; successful teams favor simplicity, bounded autonomy, and human oversight over algorithmic complexity.
- [[MemGallery/summary]] — First benchmark for multimodal long-term conversational memory; 3×3 framework across 13 systems; simple multimodal RAG beats complex architectures; all systems fail on knowledge conflict resolution.
- [[MemoryAgentBench/summary]] — Incremental multi-turn benchmark covering four memory competencies (accurate retrieval, test-time learning, long-range understanding, selective forgetting); no current system excels at all four, and selective forgetting remains nearly unsolved (≤7% multi-hop).
- [[MENLOFromPreferencesToProficiency/summary]] — 47-language benchmark (81k annotations) decomposing native-like LLM quality into 4 dimensions; pairwise RL-trained judges outperform frontier APIs and double as generative reward models for policy improvement.
- [[MetaAgentChallenge/summary]] — MAC benchmark evaluates code agents as autonomous agent developers across 5 domains; only proprietary frontier models (5/39 configs) match human-engineered baselines; optimization pressure surfaces emergent reward hacking.
- [[PredictionArenaBenchmarkingAiModelsOnRealWorldPredictionMarkets/summary]] — All Cohort 1 LLMs lost money on real-capital prediction markets; settlement accuracy predicts success.
- [[SkillsBenchBenchmarkingHowWellAgentSkillsWorkAcrossDiverseTasks]] — First agent skills benchmark across 86 tasks; curated skills +16pp, self-generated give no benefit.
- [[TauKnowledgeEvaluatingConversationalAgentsOverUnstructuredKnowledge]] — 700-doc retrieval + tool discovery + policy-compliant action benchmark; best model achieves 25.5%.
- [[TheArtOfBuildingVerifiersForComputerUseAgents/summary]] — Universal Verifier: rubric-based, screenshot-grounded verification with near-zero false positives.
