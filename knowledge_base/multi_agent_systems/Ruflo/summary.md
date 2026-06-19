# Technical Analysis: ruflo

**Repository:** https://github.com/ruvnet/ruflo
**Version analyzed:** 3.6.12 (npm: `claude-flow`)
**Date:** 2026-05-03

---

## 1. Overview / What Problem It Solves

Claude Code ships as a single-agent CLI. When a task requires parallel work — reviewing security while writing tests while updating docs — users must orchestrate that by hand. Ruflo (formerly Claude Flow) adds a coordination layer that makes Claude Code operate as a swarm: multiple specialized agents run concurrently, share memory, route tasks by capability, and learn from prior sessions.

The primary users are AI engineers and power developers who want to automate complex, multi-step software workflows using Claude Code as the execution substrate. Ruflo installs via a native Claude Code plugin (`/plugin install ruflo-core@ruflo`) or as an MCP server (`npx @claude-flow/cli`) and then hooks into Claude Code's session lifecycle invisibly — users keep writing code, and Ruflo handles routing, memory, and parallelism in the background.

Ruflo also ships a hosted web UI at `flo.ruv.io` that exposes the same MCP tools over HTTP to any OpenRouter-compatible model, enabling multi-model agent orchestration without local install.

---

## 2. High-Level Architecture

```
User / Claude Code / Web UI (flo.ruv.io)
          │
          ▼
  CLI / MCP Server (@claude-flow/cli)
          │
     ┌────┴────────────────┐
     ▼                     ▼
 Swarm Coordinator     Memory Service
 (unified-coordinator)  (HNSW + AgentDB)
     │                     │
     ▼                     ▼
 Agent Pool            Smart Retrieval
 (15 agents, domains)   (RRF + MMR + recency)
     │                     │
     ▼                     ▼
 Federation Hub        SQLite / AgentDB
 (cross-machine)       (persistent store)
     │
     ▼
 LLM Providers (Claude, GPT, Gemini, Ollama)
```

**Data flow — user task to agent output:**

1. User issues a task via CLI (`npx ruflo@latest swarm run`) or MCP tool call from Claude Code.
2. The CLI parses the command and calls `callMCPTool` which forwards to the running MCP server (`v3/@claude-flow/cli/src/mcp-server.ts`).
3. The MCP server routes to `UnifiedSwarmCoordinator`, which selects a domain (queen / security / core / integration / support) using capability matching.
4. The coordinator spawns agents from the `AgentPool` and distributes sub-tasks via the `MessageBus`.
5. Agents query `SmartRetrieval` for relevant prior context (multi-query fan-out → RRF fusion → MMR re-ranking), then call the configured LLM provider.
6. Results are written back to AgentDB (SQLite + HNSW) and returned to the caller; successful patterns are recorded to the `LearningBridge` for future trajectory optimization.

**Persistent state:** SQLite files at `.claude/memory.db` (default) and `.swarm/state.json` for swarm status. The HNSW graph is kept in memory and rebuilt from SQLite on startup.

---

## 3. The Swarm Coordination Model

The repo's central abstraction is a **15-agent hierarchical mesh** organized into five domains:

| Domain | Agent numbers | Roles |
|--------|--------------|-------|
| Queen | 1 | Top-level coordinator, task delegation |
| Security | 2–4 | security-architect, security-auditor, test-architect |
| Core | 5–9 | core-architect, type-modernization, memory-specialist, swarm-specialist, mcp-optimizer |
| Integration | 10–12 | integration-architect, cli-modernizer, neural-integrator |
| Support | 13–15 | test-architect, performance-engineer, deployment-engineer |

**Key types** (`v3/@claude-flow/swarm/src/types.ts`):

- `AgentType` — union of `'coordinator' | 'researcher' | 'coder' | 'analyst' | 'architect' | 'tester' | 'reviewer' | 'optimizer' | 'documenter' | 'monitor' | 'specialist' | 'queen' | 'worker'`
- `TopologyType` — `'mesh' | 'hierarchical' | 'centralized' | 'hybrid'`; default is `'hierarchical-mesh'` per `swarm.config.ts:21`
- `TaskPriority` — determines which `TaskId.priority` slot a task enters and which domain receives it.
- `ConsensusResult` — output of the `ConsensusEngine` used for multi-agent agreement before committing architectural decisions.

**Key knobs** (`v3/swarm.config.ts`):

| Config field | Default | Purpose |
|---|---|---|
| `maxAgents` | 15 | Hard cap on the pool |
| `messageTimeout` | 30 000 ms | Message bus round-trip timeout |
| `retryAttempts` | 3 | Per-task retry budget |
| `healthCheckInterval` | 5 000 ms | Agent heartbeat interval |
| `loadBalancingStrategy` | `'capability-match'` | How tasks map to agents |

Ephemeral agents (short-lived, task-specific) are managed by `FederationHub` (`v3/@claude-flow/swarm/src/federation-hub.ts`), which also handles cross-machine swarm registration, heartbeats, and zero-trust authentication between installations.

---

## 4. LLM / External Service Integration

Ruflo does call LLMs itself when agents execute tasks. The integration is provider-agnostic:

- **Providers:** Claude (Anthropic), OpenAI/GPT, Gemini, Cohere, Ollama (local). Configuration is via environment variables and the `providers` CLI command.
- **Local LLMs:** `ruflo-ruvllm` plugin routes to Ollama and other OpenAI-compatible endpoints. The `ruvLLM` layer (from `ruvnet/RuVector`) supports MicroLoRA adapters and SONA trajectory learning on-device.
- **Web UI (flo.ruv.io):** Uses OpenRouter to proxy six frontier models (Qwen 3.6 Max default, Claude Sonnet 4.6, Claude Haiku 4.5, Gemini 2.5 Pro, Gemini 2.5 Flash, OpenAI). Users can add any OpenAI-compatible endpoint via the UI.
- **MCP exposure:** Ruflo exposes ~210+ tools over MCP (stdio, HTTP, or WebSocket transport). Claude Code and the web UI are the MCP clients; Ruflo is the server.
- **Frameworks used:** No LangChain or LangGraph — the `agentic-flow` npm package (ADR-001) provides the agent lifecycle primitives. MCP protocol is implemented directly in `mcp-server.ts`.

Required env vars for LLM calls: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY` (each optional depending on which provider is active). None are hardcoded.

---

## 5. The Agent Execution Pipeline

**Init → Swarm → Task → Memory → LLM → Store:**

1. **Init** (`v3/@claude-flow/cli/src/commands/init.ts`): `npx ruflo init --wizard` writes `.claude/settings.json`, registers MCP tools, seeds `.swarm/` directory, and optionally installs git hooks. Supports `minimal | default | full | enterprise` templates.

2. **Swarm spawn** (`v3/@claude-flow/swarm/src/unified-coordinator.ts`): `UnifiedSwarmCoordinator.createSwarm()` instantiates an `AgentPool`, a `TopologyManager` (sets mesh or hierarchical connections), and a `MessageBus`. The queen agent registers first; domain agents follow.

3. **Task routing** (`unified-coordinator.ts:~120`): Incoming `TaskDefinition` is scored against each domain's `capabilities[]`. Best-scoring domain receives the task; if all busy, it queues. Parallel execution is enabled per domain (`parallelExecution: true` in `swarm.config.ts`).

4. **Memory query** (`v3/@claude-flow/memory/src/smart-retrieval.ts`): Before calling the LLM, each agent runs `SmartRetrieval.search()`:
   - Expands the query into 2–3 variants (template-based, no LLM cost).
   - Fan-out fetches from HNSW, merges via Reciprocal Rank Fusion (RRF constant k=60).
   - Applies recency boost (half-life 30 days, max multiplier ×1.2).
   - MMR diversity re-ranking (λ=0.7, token-Jaccard proxy) to avoid redundant results.
   - Session round-robin for multi-session coverage.

5. **LLM call**: Agent sends assembled context + task to the configured provider. Tool calls from the model are handled and fed back in the same turn.

6. **Store + learn** (`v3/@claude-flow/memory/src/learning-bridge.ts`): Successful outputs are embedded (via `@ruvector/core`) and upserted into AgentDB. `PersistentSona` records the trajectory for future pattern matching.

**Input → output shapes:** `TaskDefinition` → `ParallelExecutionResult[]` (one per domain), each containing `{ taskId, domain, success, result, durationMs }`.

---

## 6. Key Files

| File | Lines (approx) | What It Does |
|------|---------------|--------------|
| `v3/@claude-flow/swarm/src/unified-coordinator.ts` | ~600 | Core swarm orchestrator: domain routing, agent pool management, parallel dispatch |
| `v3/@claude-flow/swarm/src/federation-hub.ts` | ~500 | Ephemeral agents, cross-swarm registration, zero-trust federation protocol |
| `v3/@claude-flow/swarm/src/types.ts` | ~400 | All canonical swarm types: AgentId, TaskId, TopologyType, ConsensusResult |
| `v3/@claude-flow/memory/src/hnsw-index.ts` | ~500 | HNSW vector index with BinaryMinHeap/BinaryMaxHeap for O(log n) ops |
| `v3/@claude-flow/memory/src/smart-retrieval.ts` | ~400 | LongMemEval-derived RAG pipeline: multi-query, RRF, recency, MMR, session diversity |
| `v3/@claude-flow/memory/src/agentdb-backend.ts` | ~300 | AgentDB adapter: SQLite persistence, HNSW integration, namespace isolation |
| `v3/@claude-flow/cli/src/mcp-server.ts` | ~400 | MCP server lifecycle: stdio/HTTP/WebSocket transport, PID management, health checks |
| `v3/@claude-flow/cli/src/commands/init.ts` | ~400 | Wizard init: template selection, hook registration, Codex dual-mode support |
| `v3/@claude-flow/cli/src/commands/swarm.ts` | ~350 | `swarm` CLI subcommands: status, run, stop, agent management |
| `v3/@claude-flow/cli/src/mcp-tools/index.ts` | ~200 | MCP tool registry: 28 tool files, ~210+ exposed tools |
| `v3/swarm.config.ts` | ~150 | Default 15-agent swarm config: domains, phases, topology, load balancing |
| `v3/index.ts` | ~120 | V3 barrel re-export: security, memory, swarm, integration, shared, cli, neural |
| `ruflo/src/` | ~600 | Legacy V2 source: chat UI, MCP bridge, ruvocal integration |
| `plugins/ruflo-*/` | varies | 32 native Claude Code plugins (one directory each) |
| `agents/*.yaml` | 5 files | YAML agent definitions: architect, coder, reviewer, security-architect, tester |

---

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `semver` | `^7.6.0` | Version comparison for plugin compatibility |
| `zod` | `^3.22.4` | Runtime schema validation for MCP tool inputs |
| `@ruvector/core` | `^0.1.30` | WASM-accelerated embeddings and vector ops (optional) |
| `@ruvector/router` | `^0.1.30` | Intelligent LLM provider routing (optional) |
| `@ruvector/sona` | `^0.1.5` | SONA self-learning neural patterns (optional) |
| `@ruvector/attention` | `^0.1.3` | Flash Attention implementation in WASM (optional) |
| `agentdb` | `^3.0.0-alpha.9` | AgentDB: vector-capable SQLite store (optional) |
| `agentic-flow` | `^2.0.7` | Agent lifecycle primitives, ADR-001 foundation (optional) |
| `@claude-flow/codex` | `^3.0.0-alpha.8` | OpenAI Codex integration for dual-mode init (optional) |
| `@claude-flow/plugin-gastown-bridge` | `^0.1.3` | Plugin gateway bridge (optional) |
| `typescript` | `^5.0.0` | Dev — compilation |
| `tsx` | `^4.21.0` | Dev — watch mode |
| `vitest` | `^1.0.0` | Dev — test runner (ADR-008: Vitest over Jest) |
| `@openai/codex` | `^0.98.0` | Dev — Codex SDK for dual-mode development |
| `hono` | `>=4.11.4` | Overridden — CVE/incompatibility pin on web framework dependency |

All `@ruvector/*` and `agentdb` packages are `optionalDependencies` — the system degrades gracefully when they are absent, falling back to the `sql.js` in-memory SQLite backend.

---

## 8. CLI / Usage Surface

**Entry points** (`package.json:bin`):

```json
{ "claude-flow": "./bin/cli.js" }
```

Also callable as `npx ruflo@latest` (npm package name `claude-flow`, binary aliased).

**Primary commands:**

```bash
# Initialize project
npx ruflo@latest init [--wizard] [--minimal | --full] [--force]
npx ruflo@latest init --codex   # OpenAI Codex dual-mode

# Swarm operations
npx ruflo@latest swarm run <task>
npx ruflo@latest swarm status [--swarm-id <id>]
npx ruflo@latest swarm stop

# Agent management
npx ruflo@latest agent spawn --type coder --task "refactor auth module"

# Memory
npx ruflo@latest memory store <key> <value> [--namespace <ns>]
npx ruflo@latest memory search <query> [--limit 10]

# MCP server
npx ruflo@latest mcp start [--transport stdio|http|websocket] [--port 3000]
npx ruflo@latest mcp status

# Autopilot
npx ruflo@latest autopilot start --goal "improve test coverage to 80%"

# Plugin management
/plugin marketplace add ruvnet/ruflo
/plugin install ruflo-core@ruflo
```

**Environment variables:**

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Claude API access |
| `OPENAI_API_KEY` | — | OpenAI/GPT provider |
| `GEMINI_API_KEY` | — | Google Gemini provider |
| `OPENROUTER_API_KEY` | — | OpenRouter multi-model proxy |
| `RUFLO_MCP_PORT` | `3000` | HTTP/WebSocket MCP server port |
| `RUFLO_MCP_TRANSPORT` | `stdio` | MCP transport mode |
| `RUFLO_LOG_LEVEL` | `info` | Logging verbosity |

**Configuration files:**

| Path | Purpose |
|---|---|
| `.claude/settings.json` | Claude Code hooks, permissions, MCP server config |
| `.swarm/state.json` | Live swarm state snapshot |
| `.swarm/agents/*.json` | Per-agent state files |
| `.claude/memory.db` | SQLite AgentDB backing store |
| `v3/swarm.config.ts` | Compiled swarm topology defaults |

---

## 9. Extensibility Points

- **New agent types:** Add entries to `DOMAIN_CONFIGS` in `v3/@claude-flow/swarm/src/unified-coordinator.ts` (around the `DomainConfig[]` declaration). Each entry requires a `name`, `agentNumbers`, `priority`, and `capabilities` array. The load balancer automatically considers new domains in capability matching.

- **New MCP tools:** Create a new file in `v3/@claude-flow/cli/src/mcp-tools/` following the existing convention (e.g. `agentdb-tools.ts`). Register it in `mcp-tools/index.ts`. The MCP server picks up all exports that conform to the tool schema in `types.ts`.

- **New LLM provider:** Implement the provider interface in `v3/@claude-flow/providers/` (the directory exists under `v3/@claude-flow/`). Wire it into the `router` (uses `@ruvector/router`) with a priority score and capability flags.

- **New Claude Code plugin:** Use the `ruflo-plugin-creator` plugin (`/plugin install ruflo-plugin-creator@ruflo`), which scaffolds the `.claude-plugin/` structure. Alternatively, mirror any directory under `plugins/ruflo-*/` — each plugin is a self-contained directory with a `plugin.json` manifest.

- **New memory backend:** Implement the `SearchFn` interface in `v3/@claude-flow/memory/src/smart-retrieval.ts` and register it in the `DatabaseProvider` (`database-provider.ts`). Existing backends: `AgentDBBackend`, `SqliteBackend`, `SqlJsBackend` (in-memory), `RVFBackend`.

- **WASM extensions:** The `ruflo-wasm` plugin provides a sandboxed WebAssembly runtime. Drop a `.wasm` module into the designated plugin path and it registers as an agent tool. The WASM policy engine (Rust-compiled) runs capability checks without exposing host APIs.

---

## 10. Limitations and Gotchas

- **Alpha optionalDependencies:** Core performance features (`@ruvector/core`, `agentdb`, `agentic-flow`) are `optionalDependencies` at alpha versions (`^3.0.0-alpha`). Installations that fail to pull these silently fall back to slower in-memory or sql.js backends with no visible warning to the user.

- **npm name mismatch:** The published package name is `claude-flow`, not `ruflo`. `npx ruflo@latest` works because the npm registry has a `ruflo` package that delegates, but the internal package.json, bin entry, and GitHub URLs still reference `claude-flow` / `ruvnet/claude-flow`. This creates confusion navigating issues and changelogs.

- **15-agent ceiling is configuration, not enforcement:** `maxAgents: 15` in `swarm.config.ts` is a default; the `UnifiedSwarmCoordinator` does not enforce it at the type level. Passing a higher count in custom config will not throw but is untested.

- **HNSW graph is in-memory only:** `hnsw-index.ts` builds the graph at startup by replaying SQLite records. Large memory stores (>100K entries) will have slow cold starts; there is no incremental persistence of the HNSW graph itself.

- **No WebSocket client in V3 CLI:** `mcp-server.ts` declares `websocket` as a supported transport but the CLI client (`mcp-client.ts`) only implements stdio and HTTP. WebSocket server-side code exists; client-side does not (per README: "not verified in source").

- **Dual v2/v3 source tree:** The repo ships both `ruflo/src/` (V2 legacy) and `v3/` (V3 rewrite). The published npm package ships V3 artifacts only, but the presence of two parallel source trees increases maintenance burden and confuses contributors about the canonical path.

- **Security scan caveat:** `AIDefence` (`ruflo-aidefence` plugin) claims prompt injection detection, but it is a plugin installable on request — it is not active by default. Users who install Ruflo without the plugin have no built-in input sanitization.

- **CLAUDE.local.md present in repo root:** A `CLAUDE.local.md` file is committed to the repository root, which typically contains machine-local or developer-specific overrides and should be gitignored.

---

## 11. How It Compares to Alternatives

**LangGraph / LangGraph Cloud** — graph-based agent orchestration from LangChain. LangGraph gives fine-grained control over state machines and branching conditions; Ruflo trades that explicitness for a higher-level "domain swarm" abstraction that requires less graph-design upfront. LangGraph has a mature checkpoint/persistence story; Ruflo's HNSW memory is faster but lacks LangGraph's built-in resumable state graph.

**AutoGen (Microsoft)** — conversation-based multi-agent framework. AutoGen centers on agent-to-agent dialogue with structured turn-taking; Ruflo centers on capability-matched task dispatch with parallel execution. AutoGen is provider-agnostic by design; Ruflo is Claude-first with other providers as add-ons.

**CrewAI** — role-based agent crews with sequential and parallel task execution. CrewAI's `Crew` concept maps closely to Ruflo's swarm, but CrewAI is Python-only and has no native Claude Code plugin system. Ruflo's integration with Claude Code hooks gives it a tighter developer-experience loop for users already in that ecosystem.

**Dify / Flowise** — low-code/no-code agent builders with visual workflows. These target non-developer users; Ruflo targets engineers who want code-native control. Ruflo's CLI and MCP surface are significantly more powerful for programmatic use but have no visual workflow editor.

**Positioning:** Ruflo is the only multi-agent framework with native Claude Code plugin integration and a self-learning memory layer, making it the least-friction choice for teams already using Claude Code who want to move from single-agent to swarm-scale automation.

---

## Appendix: Selected Code Snippets

**15-Agent Domain Configuration (`v3/@claude-flow/swarm/src/unified-coordinator.ts:~90`)**

```typescript
const DOMAIN_CONFIGS: DomainConfig[] = [
  {
    name: 'queen',
    agentNumbers: [1],
    priority: 100,
    capabilities: ['coordination', 'planning', 'delegation', 'monitoring'],
    description: 'Top-level coordinator for the entire swarm',
  },
  {
    name: 'security',
    agentNumbers: [2, 3, 4],
    priority: 90,
    capabilities: ['security-audit', 'vulnerability-scan', 'cve-remediation', 'penetration-testing'],
    description: 'Security domain: architect, auditor, test-architect',
  },
  {
    name: 'core',
    agentNumbers: [5, 6, 7, 8, 9],
    priority: 80,
    capabilities: ['architecture', 'type-system', 'memory', 'swarm-coordination', 'mcp-optimization'],
    description: 'Core domain: architect, type-modernization, memory-specialist, swarm-specialist, mcp-optimizer',
  },
];
```

**HNSW BinaryMinHeap for O(log n) candidate selection (`v3/@claude-flow/memory/src/hnsw-index.ts:~30`)**

```typescript
class BinaryMinHeap<T> {
  private heap: Array<{ item: T; priority: number }> = [];

  insert(item: T, priority: number): void {
    this.heap.push({ item, priority });
    this.bubbleUp(this.heap.length - 1);
  }

  extractMin(): T | undefined {
    if (this.heap.length === 0) return undefined;
    const min = this.heap[0].item;
    const last = this.heap.pop()!;
    if (this.heap.length > 0) {
      this.heap[0] = last;
      this.bubbleDown(0);
    }
    return min;
  }

  private bubbleUp(index: number): void {
    while (index > 0) {
      const parent = Math.floor((index - 1) / 2);
      if (this.heap[parent].priority <= this.heap[index].priority) break;
      [this.heap[parent], this.heap[index]] = [this.heap[index], this.heap[parent]];
      index = parent;
    }
  }
}
```

**SmartRetrieval pipeline options (`v3/@claude-flow/memory/src/smart-retrieval.ts:~55`)**

```typescript
export interface SmartSearchOptions {
  query: string;
  namespace?: string;
  limit?: number;          // final results (default 10)
  threshold?: number;      // similarity floor (default 0.3)
  multiQuery?: boolean;    // fan-out 2-3 variants + RRF (default true)
  recencyBoost?: boolean;  // timestamp-based score boost (default true)
  diversityMMR?: boolean;  // MMR re-ranking (default true)
  sessionDiversity?: boolean; // round-robin by session_id (default true)
  fanOutK?: number;        // candidates per variant (default limit × 3)
  rrfK?: number;           // RRF constant (default 60)
  recencyHalfLifeDays?: number; // decay half-life (default 30)
  mmrLambda?: number;      // relevance/diversity tradeoff (default 0.7)
}
```

**Swarm default configuration (`v3/swarm.config.ts:~65`)**

```typescript
export const defaultSwarmConfig: V3SwarmConfig = {
  topology: 'hierarchical-mesh',
  maxAgents: 15,
  messageTimeout: 30000,
  retryAttempts: 3,
  healthCheckInterval: 5000,
  loadBalancingStrategy: 'capability-match',
  name: 'claude-flow-v3-swarm',
  version: '3.0.0',
  description: '15-agent hierarchical mesh swarm for V3 implementation',
  // ...
};
```
