> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[../AutoMem/summary|AutoMem: Automated Learning of Memory as a Cognitive Skill]] — same-problem-different-method: both tackle long-horizon agent memory management, but AutoMem learns it as a trainable skill (scaffold optimizer plus LoRA memory specialist) while Honcho delivers it as a managed service with background reasoning.
- [[../AreWeReadyForAnAgentNativeMemorySystem/summary|Are We Ready For An Agent-Native Memory System?]] — applies-in-practice: Honcho is a production instance of the memory-system class that paper taxonomizes and benchmarks (representation and storage, retrieval and routing, maintenance modules).
- [[../MemoryInTheAgeOfAIAgents/summary|Memory in the Age of AI Agents: A Survey -- Forms, Functions and Dynamics]] — shares-technique: the survey's Forms-Functions-Dynamics taxonomy maps Honcho's design space (session-scoped token memory, Deriver consolidation, peer-scoped retrieval).
- [[../ChatGPTMemoryDreaming/summary|ChatGPT Started Dreaming: How Its Memory Actually Works]] — shares-technique: both rely on async background consolidation to keep memory fresh (ChatGPT's Dreaming profile rewrites versus Honcho's Deriver reasoning over sessions).
