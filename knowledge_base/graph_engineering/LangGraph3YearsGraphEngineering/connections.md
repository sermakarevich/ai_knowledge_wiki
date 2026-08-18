> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[GraphEngineeringVsLoopEngineering/summary|Graph Engineering vs. Loop Engineering]] — makes the same-problem-different-source argument that graph engineering sits above loop engineering in a layered stack (prompt → context → harness → loop → graph); worth reading alongside this article's own claim that loops are simply a cyclic special case of graphs, since the two sources frame the loop/graph relationship slightly differently (a layer above vs. a special case of).
- [[LoopEngineeringAnthropicPlaybook/summary|Loop Engineering: The Anthropic Playbook]] — shares-technique: covers the loop-engineering discipline this article explicitly treats as nested inside graph engineering (a loop is "merely a directed, cyclic graph"), useful for the more detailed treatment of loop design (routing, escalation, memory) that this article only gestures at.
- [[LoopEngineeringClearlyExplained/summary|Loop Engineering Clearly Explained]] — same-problem-different-method: another loop-engineering framing that this article's Lesson 2 (loops are simple graphs) directly subsumes; useful for contrasting how differently "loop" is scoped across sources.
- [[TrizAgents/summary|TrizAgents]] (in [[multi_agent_systems/multi_agent_systems|Multi-Agent Systems]]) — applies-in-practice: a concrete LangGraph-based multi-agent system (a supervised 6-step TRIZ workflow) that exercises exactly the fixed-structure-plus-model-judgment pattern this article argues for, in a real domain outside LangChain's own docs-agent example.
