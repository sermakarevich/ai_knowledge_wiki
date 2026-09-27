> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[HowAiAgentsSpendYourMoney/summary|How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks]] — same-problem, applies-in-practice: quantifies input-token dominance in agentic coding that Spotify's bulk-read delegation directly attacks, giving the measurement backing for why keeping file contents out of Claude's context saves ~90%.
- [[AgentAsARouter/summary|Agent-as-a-Router: Agentic Model Routing for Coding Tasks]] — same-problem-different-method: both route work to cheaper models, but ACRouter learns routing online as a contextual bandit while Spotify enforces static hook-based routing to a fixed Gemini 2.5 Flash worker.
- [[ContextCompressionInteractionCosts/summary|What Does Context Compression Cost an Agent? Interaction Costs Unrevealed by Task-Completion Metrics]] — shares-technique with a caution: both keep bulk context out of the frontier model, but this paper shows completion-only metrics hide re-query and latency costs, directly relevant to Spotify's unmeasured follow-up re-sends and 10–30s delegation delay.
