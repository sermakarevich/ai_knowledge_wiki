> [[index|Research]] | [[overview|Overview]] | [[digest|Digest]]

# Agreements — AgentBrain / agent_memory

Focus: which of these 20 agent second-brain GitHub projects are worth using
for a system that captures sources, connects ideas, remembers context, and
helps agents act on it, and how they compare across capture, linking,
memory/recall, and agentic action.

Scope note: every claim below is supported by two or more *independent*
sources (different repos). All underlying evidence is README- and
config-level documentation synthesis from fresh `summarise` runs — no source
pair ran a controlled experiment or measured the same outcome metric, so
"strength" here means breadth and independence of architectural convergence,
not replicated measurement. Vendor-reported benchmark figures (LoCoMo,
LongMemEval, R@5/token claims) appear in single sources only and are
excluded. Ordered strongest to weakest.

## Plain Markdown files are the human-readable store; the graph or index is a derived companion layer

Backed by: [[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]]
[[research_topics/agent_memory/Swarmvault/summary|Swarmvault]]
[[research_topics/agent_memory/SageWiki/summary|SageWiki]]
[[research_topics/agent_memory/VaultCurate/summary|VaultCurate]]
[[research_topics/agent_memory/AgentSecondBrain/summary|AgentSecondBrain]]
[[research_topics/agent_memory/Chubbyskills/summary|Chubbyskills]]
[[research_topics/agent_memory/OpenViking/summary|OpenViking]]
[[research_topics/agent_memory/MemU/summary|MemU]]
[[research_topics/agent_memory/OpenSecondBrain/summary|OpenSecondBrain]]
[[research_topics/agent_memory/CogSecondBrain/summary|CogSecondBrain]]
[[research_topics/agent_memory/DocMason/summary|DocMason]]

All four linking sources keep the vault as ordinary interlinked
(Obsidian-compatible) Markdown with the graph as a companion machine layer
(ledgers, `graph.json`, ontology, ephemeral Canvas suggestions) rather than a
replacement. The same file-first shape recurs independently: AgentSecondBrain
files typed cards into a plain-markdown vault, Chubbyskills lands frontmatter
Markdown plus attachments in a vault inbox, OpenViking extracts
inspectable/editable Markdown memories, MemU's whole store is an
agent-maintained Markdown skill wiki, OpenSecondBrain stores `Brain/*.md`
with git history and no daemon, CogSecondBrain runs numbered vault folders
with no database, and DocMason publishes JSON-plus-markdown evidence
bundles. Joint evidence is strong: 11 independent repos, same file-first
representation, documented in store layouts and CLI/config surfaces. The
agreement covers the *human-readable layer*, not graph weight — Swarmvault
and SageWiki persist a typed graph artifact while VaultCurate keeps only
ephemeral suggestions, which is a design choice, not a dispute. Holds for
Obsidian-compatible personal/team vaults; does not extend to the
relational-bank (Hindsight) or Cloudflare-D1 (SecondBrainCloudflare) stores,
which keep Markdown only at the edges.

## Local-first by default; network and model calls sit at explicit opt-in edges

Backed by: [[research_topics/agent_memory/Chubbyskills/summary|Chubbyskills]]
[[research_topics/agent_memory/DocsAgent/summary|DocsAgent]]
[[research_topics/agent_memory/DocMason/summary|DocMason]]
[[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]]
[[research_topics/agent_memory/Swarmvault/summary|Swarmvault]]
[[research_topics/agent_memory/SageWiki/summary|SageWiki]]
[[research_topics/agent_memory/VaultCurate/summary|VaultCurate]]
[[research_topics/agent_memory/Agentmemory/summary|Agentmemory]]
[[research_topics/agent_memory/MemU/summary|MemU]]
[[research_topics/agent_memory/OpenSecondBrain/summary|OpenSecondBrain]]
[[research_topics/agent_memory/RowBot/summary|RowBot]]
[[research_topics/agent_memory/OpenWiki/summary|OpenWiki]]

Chubbyskills runs its core path on stdlib with no keys or models;
DocsAgent retrieves lexically with zero exfiltration; DocMason sends no
document content over the network and delegates reasoning to the host agent;
ClaudeObsidian core makes no network requests; Swarmvault's default
`heuristic` provider is offline; VaultCurate's Find/Connect/Rediscover run
fully on-device behind a ~110 MB local model; Agentmemory runs keyless BM25
with no external service; MemU's service makes no LLM/chat calls;
OpenSecondBrain's Markdown path needs no external service; RowBot makes no
call by default and bans surprise network use. Joint evidence is strong: 12
independent repos converging on the same boundary, each documented via
dependency tables and provider matrices. Condition: "local-first" means the
capture→store→retrieve core, while transcription, enrichment, embeddings, or
group sync are declared opt-in edges (provider keys, flags, settings).
Known qualifier: OpenWiki's Jina Reader/Google Translate exceptions are on
by default, so its local-first claim is weaker than the rest. Holds for
self-hosted/personal deployments; team-cloud variants (TencentDB service
mode, Hindsight Cloud, SecondBrainCloudflare Workers AI) move inference into
operated infrastructure by design.

## Provenance is captured at ingest time and kept visible, not reconstructed later

Backed by: [[research_topics/agent_memory/Chubbyskills/summary|Chubbyskills]]
[[research_topics/agent_memory/OpenWiki/summary|OpenWiki]]
[[research_topics/agent_memory/DocsAgent/summary|DocsAgent]]
[[research_topics/agent_memory/DocMason/summary|DocMason]]
[[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]]
[[research_topics/agent_memory/Swarmvault/summary|Swarmvault]]
[[research_topics/agent_memory/SageWiki/summary|SageWiki]]
[[research_topics/agent_memory/OpenSecondBrain/summary|OpenSecondBrain]]

Capture lanes preserve source identity up front: schema-v1 task IDs with
SHA-256 digests (Chubbyskills), source-app attribution (OpenWiki), global
entry ids (DocsAgent), exact file-and-page identity (DocMason). Linking
sources keep that provenance visible through use: source/claim ledgers with
authority, support, contradiction, and confidence (ClaudeObsidian),
`extracted`/`inferred`/`ambiguous` edge tags plus contradiction flags
(Swarmvault), evidenced edges carrying span, confidence, and asserting
document (SageWiki), and attributable writes with write records and
before-images (OpenSecondBrain). Joint evidence is strong: 8 independent
repos, same "tag it, don't hide it" rule, grounded in frontmatter schemas,
ledger files, and edge vocabularies. The mechanism differs (digests vs
ledgers vs edge tags vs write records), but no source recovers provenance
after the fact. Holds where answers must cite sources (creator briefs,
research corpora, cited Q&A); weakest for pure chat-memory stores that keep
only session text.

## Recall fuses lexical, vector, and graph/structure signals instead of relying on one method

Backed by: [[research_topics/agent_memory/TencentDBAgentMemory/summary|TencentDBAgentMemory]]
[[research_topics/agent_memory/Hindsight/summary|Hindsight]]
[[research_topics/agent_memory/Agentmemory/summary|Agentmemory]]
[[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]]
[[research_topics/agent_memory/Swarmvault/summary|Swarmvault]]
[[research_topics/agent_memory/SageWiki/summary|SageWiki]]
[[research_topics/agent_memory/VaultCurate/summary|VaultCurate]]
[[research_topics/agent_memory/SecondBrainCloudflare/summary|SecondBrainCloudflare]]

BM25 + vector + RRF (TencentDB), four-strategy fan-out with fusion and
cross-encoder reranking (Hindsight), BM25/vector/graph fusion weights
(Agentmemory), BM25 with optional cosine rerank (ClaudeObsidian), SQLite FTS
plus embeddings with bounded traversal (Swarmvault), three-channel
lexical/vector/graph-proximity fusion (SageWiki), fused
keyword/semantic/fuzzy-title ranking (VaultCurate), and semantic plus
full-text relevance with connection expansion (SecondBrainCloudflare) all
attest the same hybrid core. Joint evidence is strong: 8 independent repos
across the memory and linking groups, each naming the same channel set in
retrieval configs and tool contracts. Every source also keeps a
deterministic fallback (BM25/FTS/keyword) when models are unavailable.
Condition: fusion weights, rerankers, and traversal bounds differ per repo —
the agreement is on combining similarity with structure, not on any single
formula. No two sources measured recall quality on the same benchmark, so
this is a design convergence, not a measured superiority claim.

## Flat chat history and single-method vector retrieval are insufficient on their own

Backed by: [[research_topics/agent_memory/TencentDBAgentMemory/summary|TencentDBAgentMemory]]
[[research_topics/agent_memory/OpenViking/summary|OpenViking]]
[[research_topics/agent_memory/Agentmemory/summary|Agentmemory]]
[[research_topics/agent_memory/Hindsight/summary|Hindsight]]
[[research_topics/agent_memory/MemU/summary|MemU]]
[[research_topics/agent_memory/OpenSecondBrain/summary|OpenSecondBrain]]

All six memory-substrate sources add structure on top of raw history or
embeddings: layered distillation (TencentDB L0→L3, OpenViking L0/L1/L2),
banks with ACLs (Hindsight, TencentDB), subtree scoping
(OpenViking `viking://`), skill-wiki distillation (MemU), vault files with
visibility boundaries (OpenSecondBrain). Hindsight states the position
explicitly ("learn, not just remember") against conversation-history recall,
RAG, and graph-only extraction. Joint evidence is moderately strong: 6
independent repos in one sub-topic plus the hybrid-retrieval consensus
above, all documented at the architecture/API level. What replaces the flat
store differs (layers, files, banks, wikis), so the claim holds only in its
negative form — *something* structural must sit above transcripts and pure
vectors. No source tested flat-vs-structured recall head-to-head on shared
data.

## Memories must be inspectable and editable by humans, not opaque embeddings

Backed by: [[research_topics/agent_memory/OpenViking/summary|OpenViking]]
[[research_topics/agent_memory/MemU/summary|MemU]]
[[research_topics/agent_memory/OpenSecondBrain/summary|OpenSecondBrain]]
[[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]]
[[research_topics/agent_memory/TencentDBAgentMemory/summary|TencentDBAgentMemory]]

Session commits extract editable Markdown memories (OpenViking), the
agent-maintained skill wiki is the whole readable store (MemU), `Brain/*.md`
files are greppable, git-versioned, and hand-editable with no daemon
(OpenSecondBrain), vault lint reports dead links, orphans, and staleness
against a declared date (ClaudeObsidian), and team assets are reviewed and
permissioned in a Hub panel (TencentDB). Joint evidence is moderate: 5
independent repos, same inspectability norm, grounded in file layouts,
CLI surfaces, and review flows. Condition: the audit surface suits
file-shaped stores; relational/vector internals (banks, chunks, embeddings)
remain machine-readable only, with human review happening at the
Markdown/panel layer. Holds for single-owner and small-team vaults where a
human curates; less applicable to fully automatic server-side pipelines.

## Graph and link writes are gated — staging, approval, or verdict stands between proposal and canon

Backed by: [[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]]
[[research_topics/agent_memory/Swarmvault/summary|Swarmvault]]
[[research_topics/agent_memory/SageWiki/summary|SageWiki]]
[[research_topics/agent_memory/VaultCurate/summary|VaultCurate]]
[[research_topics/agent_memory/DocsAgent/summary|DocsAgent]]
[[research_topics/agent_memory/DocMason/summary|DocMason]]

One inspected transaction bundle applied by a single orchestrator
(ClaudeObsidian), `compile --approve` with `candidates/` staging and
`lint --conflicts` (Swarmvault), review-gated entity-resolution proposals
and quarantined outputs (SageWiki), suggestion-only Canvas links requiring an
accept/dismiss verdict (VaultCurate), preview-then-confirm with a per-hour
rate limit on writes (DocsAgent), and validation gates that fail bad data
instead of publishing it (DocMason) all enforce the same rule: no silent
auto-linking into canonical state. Joint evidence is moderate: 6
independent repos across linking and capture groups, documented via
CLI flags, staging directories, and gate specs. The gate mechanism differs
(transaction inspect/apply vs approval bundles vs verdict dialogs vs rate
limits); the agreement is that *a* gate exists, not on its form. Holds for
shared or long-lived vaults where bad links compound; single-use scratch
indexes may skip gating.

## Recall is scoped and budgeted rather than loading everything

Backed by: [[research_topics/agent_memory/OpenViking/summary|OpenViking]]
[[research_topics/agent_memory/Hindsight/summary|Hindsight]]
[[research_topics/agent_memory/TencentDBAgentMemory/summary|TencentDBAgentMemory]]
[[research_topics/agent_memory/Agentmemory/summary|Agentmemory]]

Subtree-scoped `find`/`search`/`grep` with L0-first scan-before-read tiers
(OpenViking), `bank_id` tenancy over every call (Hindsight),
`private`/`team`/`restricted` visibility plus User/Role/Agent ACLs with
count/char/timeout budgets (TencentDB), and token budgets with per-session
observation caps (Agentmemory) converge on bounded, permissioned recall.
Joint evidence is moderate: 4 independent repos, documented in query CLIs,
config keys, and recall-path descriptions. Scoping axis differs (directory
subtree vs bank vs visibility boundary) and budget units differ (tokens,
chars, counts, tiers), so the claim holds at the principle level only.
Applies to multi-user or large-corpus deployments where unbounded recall
wastes tokens or leaks across boundaries; single-user scratch vaults in
these sources often skip it.

## Capture and recall are separate seams: one path records experience, a later path injects it

Backed by: [[research_topics/agent_memory/MemU/summary|MemU]]
[[research_topics/agent_memory/Hindsight/summary|Hindsight]]
[[research_topics/agent_memory/OpenViking/summary|OpenViking]]
[[research_topics/agent_memory/Agentmemory/summary|Agentmemory]]
[[research_topics/agent_memory/AgentSecondBrain/summary|AgentSecondBrain]]

Record/inject split with a scheduled bridging task (MemU), retain vs
recall/reflect operations (Hindsight), session commit vs find/search/grep
(OpenViking), `memory_save` vs `memory_recall`/`memory_smart_search`
(Agentmemory), and Telegram capture vs vault-and-graph question answering
(AgentSecondBrain) all separate the write path from the read path, often
across agents and sessions. Joint evidence is moderate: 5 independent repos,
grounded in CLI verbs, API triples, and pipeline stage names. Condition:
capture is frequently agent- or hook-mediated (bridging tasks, proxies,
persistent sessions) rather than direct user filing — the seam exists
whether or not a human sits in it. Holds for cross-session and cross-agent
reuse; single-turn Q&A over static files does not need the split.

## Memory feeds action in one loop: skills-as-markdown act on the store under bounded tools, durable state, and human gates

Backed by: [[research_topics/agent_memory/CogSecondBrain/summary|CogSecondBrain]]
[[research_topics/agent_memory/Makerskills/summary|Makerskills]]
[[research_topics/agent_memory/Mateclaw/summary|Mateclaw]]
[[research_topics/agent_memory/RowBot/summary|RowBot]]
[[research_topics/agent_memory/SecondBrainCloudflare/summary|SecondBrainCloudflare]]

Every action harness couples a recallable store (vault, wiki, graph, Worker
layer) with skills/workflows that act on it rather than treating memory as
passive Q&A; the file-only harnesses make each `SKILL.md` the executable
artifact with no build step (CogSecondBrain, Makerskills). Tools are bounded
everywhere: skill manifests, per-employee MCP bindings, allowlists,
approval gates, path/workspace protections. Long work persists as
inspectable state: checkpoints with exactly-once completion (RowBot), Goals
with checklist/continuation/leases reconciled after restart (Mateclaw),
`AC-n`-traced evidence rows in run ledgers (CogSecondBrain). Outward effects
are human-gated: Tool Guard RBAC with audit (Mateclaw), ordered
steering/approvals with budgets (RowBot), read-only verifiers (CogSecondBrain).
Joint evidence is moderate: 5 independent repos in one sub-topic, documented
at the structural level (skill counts, orchestration records, CLI/slash
commands, config shapes). No source reports task-success rates, latency, or
recall-precision for the action loop, so this is a structural convergence,
not an effectiveness claim. Holds across deployment shapes (file-only,
desktop, self-hosted, user-cloud); who runs inference, verification
strictness, and orchestration weight all differ and are excluded from this
claim.
