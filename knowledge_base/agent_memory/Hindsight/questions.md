---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: vectorize-io/hindsight

### Q1. What is Hindsight's core premise, and how does it position itself against RAG and knowledge graphs?
> [!tip]- Answer
> > Hindsight is an agent memory system built so agents learn over time rather than merely recalling conversation history. It explicitly claims to eliminate the shortcomings of RAG and knowledge-graph techniques on long-term memory tasks. See [[wiki/01-overview|Overview]].

### Q2. What accuracy claim does Hindsight make on LongMemEval, and how is the evidence presented?
> [!tip]- Answer
> > Hindsight claims state-of-the-art accuracy on the LongMemEval long-term memory benchmark, calling itself the most accurate agent memory system ever tested. Live per-model accuracy, latency, and cost are published externally, and the scores were independently reproduced by Virginia Tech's Sanghani Center and The Washington Post. See [[wiki/01-overview|Overview]].

### Q3. How is Hindsight deployed as a server, and which ports do the API and UI use?
> [!tip]- Answer
> > Hindsight deploys as a server via Docker, external PostgreSQL compose, pip bare metal, Helm/Kubernetes, or managed Cloud, with Oracle AI Database supported at feature parity. The API listens on port 8888 and the UI on port 9999. See [[wiki/01-overview|Overview]].

### Q4. What are the three core client operations, and how does the LLM Wrapper change how they are invoked?
> [!tip]- Answer
> > Clients use retain to store information, recall to search memories, and reflect for a disposition-aware response, all scoped to a bank_id across Python, Node.js, Go, CLI, REST, and embedded modes. The LLM Wrapper (wrap_openai, wrap_anthropic via hindsight-litellm) instead stores and retrieves memories automatically on every LLM call with per-call hindsight_* overrides. See [[wiki/01-overview|Overview]].

### Q5. What runtime configuration does `.env.example` define for the LLM and the API server?
> [!tip]- Answer
> > It requires HINDSIGHT_API_LLM_PROVIDER, HINDSIGHT_API_LLM_API_KEY, and HINDSIGHT_API_LLM_MODEL with defaults of openai and gpt-4o-mini, plus slots for VLM, reasoning effort, temperature, timeouts, and multi-LLM failover strategies. The API server defaults are HINDSIGHT_API_HOST=0.0.0.0, HINDSIGHT_API_PORT=8888, and HINDSIGHT_API_LOG_LEVEL=info. See [[wiki/02-top-level-files|Top-level files]].

### Q6. What contributor workflow do CLAUDE.md and AGENTS.md define, including the monorepo map and quality gates?
> [!tip]- Answer
> > AGENTS.md is a 4-line pointer to CLAUDE.md, which defines the world-facts / experience-facts / mental-models memory model, the monorepo package map, and dev/test/lint commands. It mandates dual-dialect migrations via run_for_dialect with _pg_upgrade/_oracle_upgrade and gates changes on lint.sh and /code-review. See [[wiki/02-top-level-files|Top-level files]].

### Q7. (Evaluation) Should a team adopt self-hosted Hindsight or managed Cloud for a production agent needing long-term memory?
> [!tip]- Answer
> > Recommend Cloud when the team wants usage-based billing, dashboards, backups, collaboration, and a 99.9% SLA without operating PostgreSQL, and self-hosting via Docker or Helm when data residency or existing Postgres/Oracle infrastructure matters. Either way, validate the LongMemEval claim against the team's own workload and supported platforms before committing. See [[wiki/01-overview|Overview]].
