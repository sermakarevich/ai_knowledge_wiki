> [[../../index|Research]] | [[../../overview|Overview]] | [[../../digest|Digest]]

# agentic action harnesses

**In one sentence:** The sources jointly establish that durable agent action comes from skill-packaged playbooks executed over a memory substrate, with delegated multi-agent orchestration, checkpointed recovery, provider-routed model calls, and human approval gates — packaged anywhere from file-only markdown plugins to self-hosted runtimes to a user-owned Cloudflare Worker.

## Key points
- Skills-as-executable-markdown is the shared harness idiom: a 33-skill catalog over a versioned Obsidian vault with worker/verifier routing [[research_topics/agent_memory/CogSecondBrain/summary|CogSecondBrain]] and a 20–21-skill plugin where each `SKILL.md` is the executable artifact with no build step [[research_topics/agent_memory/Makerskills/summary|Makerskills]].
- Delegated orchestration separates lead reasoning from cheap data work: Sonnet workers fan out collection/research/file-ops while the Opus lead synthesizes via `/tmp/` handoffs [[research_topics/agent_memory/CogSecondBrain/summary|CogSecondBrain]], parent agents orchestrate scoped required/detached children and join results [[research_topics/agent_memory/RowBot/summary|RowBot]], and one durable Team Run links objective, task DAG, worker executions, and synthesis on a shared board [[research_topics/agent_memory/Mateclaw/summary|Mateclaw]].
- Durability is checkpointed rather than replayed: Goals persist checklist/continuation/leases/artifacts and reconcile after a single-backend restart [[research_topics/agent_memory/Mateclaw/summary|Mateclaw]], thread checkpoints preserve approvals/steering/retries with exactly-once completion while restarts close unanswered tool calls without replay [[research_topics/agent_memory/RowBot/summary|RowBot]], and harness runs append `AC-n`-traced evidence rows to run ledgers [[research_topics/agent_memory/CogSecondBrain/summary|CogSecondBrain]].
- Provider routing favors choice plus failover over a single model: an ordered provider chain with a health tracker that parks failing vendors in cooldown [[research_topics/agent_memory/Mateclaw/summary|Mateclaw]], and side-by-side local Ollama, provider keys, subscription/OAuth sign-ins, and custom OpenAI-compatible endpoints behind explicit provider identity [[research_topics/agent_memory/RowBot/summary|RowBot]] — while the file-only harnesses call no LLM themselves and execute entirely on the host agent [[research_topics/agent_memory/CogSecondBrain/summary|CogSecondBrain]] [[research_topics/agent_memory/Makerskills/summary|Makerskills]].
- Action is gated by verification and approval layers: an opt-in V-model (CP-0–CP-7) with read-only verifiers that observe artifacts but never mutate them [[research_topics/agent_memory/CogSecondBrain/summary|CogSecondBrain]], Tool Guard RBAC with approval flows and path protection over SKILL.md/MCP/ACP tools plus a full audit trail [[research_topics/agent_memory/Mateclaw/summary|Mateclaw]], and ordered steering/approvals with work budgets, delegation limits, and capacity-hard-error compaction [[research_topics/agent_memory/RowBot/summary|RowBot]].
- Memory feeds action rather than sitting beside it: a brain-first read rule (knowledge first, then project, then synthesize) with a citation convention [[research_topics/agent_memory/CogSecondBrain/summary|CogSecondBrain]], LLM Wiki hot-cache injection into the system prompt plus workspace memory files [[research_topics/agent_memory/Mateclaw/summary|Mateclaw]], one Cloudflare Worker memory layer (classify/deduplicate/contradiction-check/relate/index on capture; semantic plus full-text recall) shared by every client over REST and MCP [[research_topics/agent_memory/SecondBrainCloudflare/summary|SecondBrainCloudflare]], and Karpathy-style capture/compile/query/lint/connect vault skills with personal↔team siblings [[research_topics/agent_memory/Makerskills/summary|Makerskills]].
- Deployment splits local-first, self-hosted, and user-cloud: local desktop with OS-credential-store secrets and no account system [[research_topics/agent_memory/RowBot/summary|RowBot]], one JAR/Docker/Electron deployment over PostgreSQL with fail-closed env handling [[research_topics/agent_memory/Mateclaw/summary|Mateclaw]], a single Worker in the user's own Cloudflare account (D1 + Vectorize + Workers AI + KV) [[research_topics/agent_memory/SecondBrainCloudflare/summary|SecondBrainCloudflare]], and zero-server markdown plugins whose personal state lives outside the repo under a config dir or vault [[research_topics/agent_memory/CogSecondBrain/summary|CogSecondBrain]] [[research_topics/agent_memory/Makerskills/summary|Makerskills]].

---
## What the sources agree on
- Memory and action belong in one loop: every source couples a recallable store (vault, wiki, graph, Worker layer) with skills/workflows that act on it, rather than treating memory as passive Q&A.
- Tools must be bounded: skill manifests, per-employee MCP bindings, allowlists, approval gates, and path/workspace protections recur across all five sources.
- Long work needs durable, inspectable state: checkpoints, ledgers, archives with revisit dates, and evidence-backed completion appear in every harness, with human-readable files (markdown, boards, dashboards) over opaque state.
- Human gates are non-optional for outward effects: approvals, verifiers, audit trails, and explicit completion criteria guard sends, publishes, shares, and destructive calls.

## Where they differ
- Who runs the model: the file-only harnesses (CogSecondBrain, Makerskills) execute zero inference and ride the host agent, while MateClaw routes across nine-plus providers with failover, RowBot adds subscriptions/OAuth plus local Ollama, and SecondBrainCloudflare pins inference to Workers AI bindings.
- Verification posture: opt-in and off-by-default (COG's V-model, RowBot's live-provider test lane) versus always-on governance (MateClaw's Tool Guard plus audit, SecondBrainCloudflare's tag/status discipline with contradiction demotion).
- Orchestration weight: heavyweight durable multi-worker runs (MateClaw Team Runs, RowBot parent/child with leases and live joins) versus lightweight skill composition by name with no manifest linking (Makerskills) or single-deliverable harness runs (COG).
- Tenancy and sharing: private-by-default with deliberate canonical moves to one shared team layer (SecondBrainCloudflare), personal↔team skill siblings with sensitivity tagging (Makerskills), multi-user workspaces with channel isolation (MateClaw), versus single owner-operator custody (RowBot, COG).

## Evidence quality
- Strongest on architecture and usage surface: all five summaries ground skill counts, orchestration records, CLI/slash commands, and config shapes in file:line citations from READMEs and root configs.
- No benchmark or outcome claims: none of the five sources reports task-success rates, latency, or recall-precision figures for the action loop; claims are structural (what the harness does), not measured (how well).
- Coverage gaps are explicit: RowBot and SecondBrainCloudflare summaries note truncated wiki chunks and unmapped `src/` internals, and several provider/route details (exact model IDs, full REST tables) are marked as unverified rather than inferred.

## Sources in this sub-topic
| source | kind | what it contributes |
|---|---|---|
| CogSecondBrain | fresh | File-first 33-skill vault harness with Sonnet/Opus worker routing, opt-in V-model checkpoints, and read-only verifiers |
| Mateclaw | fresh | Self-hosted employee runtime with Goals/Team Runs, provider failover, Tool Guard approvals, and workflow/trigger orchestration |
| RowBot | fresh | Local-first desktop agent with parent-led child orchestration, checkpointed threads, metered compaction, and provider-neutral routing |
| SecondBrainCloudflare | fresh | User-owned Cloudflare Worker memory substrate (D1/Vectorize/AI/KV) with capture-organize-recall pipeline and Personal/Shared tenancy |
| Makerskills | fresh | Documentation-first composable skill plugin with structured-input-to-archived-output cadence and public/private data split |
