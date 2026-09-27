> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Operators and System Tasks

**In one sentence:** Conductor distinguishes control-flow OPERATORS (evaluated by the server to route, fan out, loop, nest, pause, or stop execution) from SYSTEM TASKS (standard integrations and transforms the server executes itself) and AI TASKS (server-executed LLM (Large Language Model), embedding, retrieval, and media operations), leaving only proprietary or heavy logic to WORKER tasks (SIMPLE -- custom code run by your own workers).

## Key points

- Operators never do business work -- they decide which tasks run, in what order, how many times, and when the workflow continues.
- Every operator and system task runs on the Conductor server, so it needs no worker deployment; only SIMPLE (worker) tasks require you to run polling workers.
- Static parallelism (FORK_JOIN + JOIN) fixes branches at design time, while DYNAMIC_FORK (FORK_JOIN_DYNAMIC) and DYNAMIC decide branches or task names at runtime from upstream outputs.
- Pausing has three grades: WAIT (fixed duration or timestamp), WAIT_FOR_WEBHOOK/HUMAN (indefinite wait for an external signal or a person completing a form), and YIELD (park execution until externally resumed).
- SUB_WORKFLOW is a synchronous subroutine call (parent blocks and receives outputs); START_WORKFLOW is an asynchronous fire-and-start (parent continues without waiting).
- TERMINATE ends the workflow immediately with an explicit status and output, and is the standard way to short-circuit out of a SWITCH branch.
- System tasks replace workers for commodity operations: HTTP/HTTP_POLL for REST (Representational State Transfer -- the standard HTTP API style) calls, INLINE for small JS (JavaScript)/Python snippets, JSON_JQ_TRANSFORM for jq reshaping, EVENT/KAFKA_PUBLISH for publishing, JDBC/gRPC/BUSINESS_RULE/SENDGRID for database, RPC (Remote Procedure Call), rules, and email.
- AI tasks form a full RAG (Retrieval-Augmented Generation -- answering with an LLM grounded in retrieved documents) and agent loop kit: generate text/chat, embed/store/search vectors, index/search documents, chunk/parse inputs, call MCP (Model Context Protocol -- the standard for exposing tools to LLMs) tools, and generate image/audio/video/PDF -- each requiring a configured LLM or vector-database integration.

---

## Part A -- control-flow operators (server-evaluated)

### SWITCH -- conditional branching

- What: if/else or switch/case over task sequences. Evaluates one expression, matches its value against `decisionCases` keys, runs that branch; otherwise runs `defaultCase`.
- Key inputs: `evaluatorType` (`value-param` -- plain reference to an input key; `javascript`/`graaljs` -- JS expression evaluated server-side), `expression` (the key name or the script; inside scripts inputs are addressed as `$.key`), `decisionCases` (map from case string to task list), `defaultCase` (task list, may be empty), `inputParameters` (must contain the key named in `expression` when using `value-param`).
- Output: `selectedCase` records which branch ran; branch tasks return their own outputs normally.
- Vs worker: use SWITCH instead of routing inside worker code whenever branches are known upfront -- branches stay visible in the UI and each branch can use different task types. Use DYNAMIC (below) when case options are unbounded or unknown at design time.

### FORK_JOIN + JOIN + EXCLUSIVE_JOIN -- static parallelism

- What: FORK_JOIN (`FORK_JOIN`) runs a fixed list of branches in parallel; JOIN (`JOIN`) blocks until the required branches finish and aggregates their outputs. EXCLUSIVE_JOIN covers the case where only one of several alternative branches (e.g. out of a SWITCH) will complete.
- Key inputs: FORK_JOIN takes `forkTasks` (list of lists; each inner list is one branch executed in order, branches execute concurrently). JOIN takes `joinOn` (task reference names that must complete; a subset may be listed to make remaining branches optional) and optional `expression` (join script for custom completion logic).
- Constraint: a FORK_JOIN task must be immediately followed by its JOIN task or registration fails.
- Vs worker: use for independent I/O-bound calls (e.g. three enrichment HTTP calls at once). Do not fan out CPU-heavy work this way unless the downstream tasks are workers scaled for it.

### DYNAMIC_FORK + DYNAMIC -- runtime-determined parallelism and dispatch

- What: DYNAMIC_FORK (`FORK_JOIN_DYNAMIC`) fans out to N branches where N and per-branch inputs are known only at runtime (e.g. one branch per cart item). DYNAMIC executes a single task whose name/type is resolved at runtime, like a function pointer.
- Key inputs, three shapes: (1) different task per fork -- `dynamicForkTasksParam` + `dynamicForkTasksInputParamName` (names of input keys holding the task-definition list and the per-task input map, typically produced by an upstream INLINE task); (2) same task per fork -- `forkTaskType` (`HTTP`, `SIMPLE`, ...) + `forkTaskName` (when SIMPLE) + `forkTaskInputs` (list, one entry per branch); (3) same sub-workflow per fork -- `forkTaskWorkflow` + `forkTaskWorkflowVersion` + `forkTaskInputs`. Follow with a JOIN (usually empty `joinOn`). DYNAMIC takes `dynamicTaskNameParam` pointing at the input key carrying the resolved task name.
- Constraint: one fork runs exactly one task; for multiple tasks per dynamic branch, fork a SUB_WORKFLOW instead.
- Vs worker: use when fan-out width comes from data. Preceding INLINE task usually builds the task/input lists; no worker fleet changes needed when N grows.

### DO_WHILE -- loops

- What: repeats `loopOver` task list sequentially; body always runs at least once, then `loopCondition` is checked (do..while semantics). Supports counter loops and list iteration.
- Key inputs: `loopOver` (task list), `loopCondition` (JS boolean expression; wire the loop's own output back into `inputParameters`, e.g. `"loop_ref": "${loop_ref.output}"`, so `$.loop_ref['iteration']` is readable; always include an iteration cap), `items` (expression evaluating to a list; per iteration exposes `${loop_ref.output.loopItem}` and `${loop_ref.output.loopIndex}`), `evaluatorType: graaljs` (required on recent clusters or the condition fails).
- Outputs: `iteration` (final count), `loopItem`/`loopIndex` (list mode), per-iteration outputs keyed by iteration number.
- Vs worker: use for polling loops, paginated API walks, and agent plan-act-observe cycles (each iteration is a durable checkpoint). Move the per-iteration heavy work into worker tasks; keep only the condition in the loop header.

### SUB_WORKFLOW + START_WORKFLOW -- composition

- What: SUB_WORKFLOW runs another workflow synchronously as a subroutine: parent blocks, child outputs return to the parent. START_WORKFLOW launches another workflow asynchronously as an entry point: parent continues immediately without waiting.
- Key inputs: `subWorkflowParam.name` + `subWorkflowParam.version` (pre-registered child; version optional, defaults to latest), `subWorkflowParam.workflowDefinition` (inline full WorkflowDef object or a `${ref.output.field}` expression resolving to one -- lets a planner/LLM task generate the child plan at runtime, no prior registration), `subWorkflowParam.taskToDomain` (domain routing), plus `inputParameters` carrying the child's inputs. Child-to-parent data flows through the child's `outputParameters`, read as `${sub_ref.output.someKey}`.
- Vs worker: use to reuse a task sequence across parents (fix once, all callers inherit), to nest DO_WHILE loops, or to give each DYNAMIC_FORK branch multiple steps. Prefer START_WORKFLOW for fire-and-forget side workflows.

### WAIT + WAIT_FOR_WEBHOOK + HUMAN -- pausing

- WAIT: pauses until `duration` (e.g. `10m20s`; units d/h/m/s) or `until` (datetime, e.g. `2025-06-15 09:00 GMT+00:00`) passes; completes automatically. With neither parameter it waits indefinitely until completed via the Task Update API or an event handler. Overridable early via Task Update API.
- WAIT_FOR_WEBHOOK (`WAIT_FOR_WEBHOOK`): pauses indefinitely until a matching incoming webhook signal arrives; for event-driven resumes rather than clocks.
- HUMAN (`HUMAN`): pauses for a person. Links a user form (`__humanTaskDefinition.userFormTemplate.name/version`, `displayName`); form fields come from `inputParameters` (empty/default = filled by assignee; preset = read-only context). Assignment policy (`assignments`: user/group assignee, `slaMinutes`, escalation chain; `assignmentCompletionStrategy` LEAVE_OPEN or TERMINATE; `autoClaim`) controls who acts; trigger policy (`taskTriggers`: PENDING/ASSIGNED/IN_PROGRESS/COMPLETED/TIMED_OUT/ASSIGNEE_CHANGED/CLAIMANT_CHANGED) can start workflows on state changes. Completed via UI claim/submit or Human Task APIs (claim, reassign, release, skip, update).
- Vs worker: WAIT vs HUMAN -- fixed clock vs external human trigger. Never hold a worker thread polling for approval; HUMAN parks the workflow with zero resource use. For machine signals prefer WAIT_FOR_WEBHOOK or EVENT-driven resume.

### SET_VARIABLE + GET_WORKFLOW -- workflow variables and lookups

- SET_VARIABLE: writes key-value pairs into `workflow.variables`, readable downstream as `${workflow.variables.name}`. Used to accumulate loop/agent state or share values across branches without threading outputs.
- GET_WORKFLOW (`GET_WORKFLOW`): reads the state of a workflow execution (e.g. by ID) for inspection or branching decisions.
- Vs worker: use variables for small scalar state; do not stash large payloads (use the payload/file APIs or pass references).

### TERMINATE + YIELD -- completion semantics

- TERMINATE (`TERMINATE`): ends the current workflow immediately with `terminationStatus` (COMPLETED or FAILED) and `workflowOutput`. Standard pattern: inside a SWITCH branch (e.g. FAILED branch of a polled job) to short-circuit. Must be a terminal step -- nothing after it in that path runs. Distinct from TERMINATE_WORKFLOW, which targets a (sub-)workflow execution.
- YIELD (`YIELD`): suspends the workflow, yielding control until externally resumed; for cooperative pause points in long-lived executions.
- Vs worker: prefer TERMINATE over returning a failure code from a worker and adding sentinel checks downstream.

## Part B -- system tasks (executed by the server)

No worker needed for any of these. Reach for a SIMPLE worker only when logic is proprietary, needs private libraries/heavy CPU, or speaks a protocol no system task covers.

### HTTP + HTTP_POLL -- REST calls

- HTTP (`HTTP`): calls any REST endpoint. Key inputs under `http_request`: `uri`, `method` (GET/POST/PUT/DELETE), `headers`, `body`, `accept`/`contentType`, `connectionTimeOut`/`readTimeOut`, `encode`, `acceptedStatusCodes`, `outputFilter`, plus hedging (`hedgingConfig.maxAttempts` -- parallel duplicate requests, first success wins; idempotent services only) and OAuth/bearer/api-key/basic header patterns. Output: `response.body`, `response.headers`, `response.statusCode`.
- HTTP_POLL (`HTTP_POLL`): same `http_request` plus `terminationCondition` (JS evaluated after each poll; truthy stops; can return 1/0/-1 for complete/re-poll/fail), `pollingInterval` (seconds; server-side floor ~60s), `pollingStrategy` (FIXED, LINEAR_BACKOFF, EXPONENTIAL_BACKOFF), `maxPollCount` (default 1000). Match every terminal state in the condition or dead jobs poll until the count runs out.
- Vs worker: use for service-to-service calls and long-job status polling; use a worker only for custom auth flows, streaming, or non-HTTP protocols.

### INLINE -- server-side scripting

- What (`INLINE`): evaluates a small expression in the server JVM (Java Virtual Machine -- the runtime Conductor runs on) and returns `output.result` for downstream wiring.
- Key inputs: `evaluatorType` (`graaljs` recommended for modern JS, `python` via GraalVM polyglot, legacy `javascript`, `value-param` passthrough), `expression` (must return a value; extra inputs referenced as `$.key`), plus arbitrary input keys.
- Vs worker: for deterministic glue -- validation, calculation, unit conversion, building DYNAMIC_FORK lists, categorizing before a SWITCH. Move to a worker when scripts grow long, need libraries, or do heavy compute.

### JSON_JQ_TRANSFORM -- JSON reshaping

- What (`JSON_JQ_TRANSFORM`): transforms JSON with jq (a JSON query/transform language) syntax.
- Key inputs: the data fields plus `queryExpression` (jq program, e.g. `[.items[] | select(.created_at > "...") | {title: .title}]`). Outputs: `result` (first result), `resultList` (all results), `error`.
- Vs worker: use to trim verbose API responses, merge arrays, or reshape payloads between tasks. Prefer over INLINE when the job is pure JSON projection/filtering.

### EVENT + KAFKA_PUBLISH -- publishing messages

- EVENT (`EVENT`): provider-neutral publish of a JSON message. Key inputs: top-level `sink` (`provider:destination`; OSS providers include `conductor`, `kafka`, `sqs`, `nats`, `amqp_queue`, `amqp_exchange`; short `conductor` sinks expand to `conductor:<workflow>:<event>` and handlers must subscribe to the expanded name), `inputParameters` (payload fields), `asyncComplete` (false = complete on publish; true = stay IN_PROGRESS until an external update or event-handler complete/fail action). Server stamps `workflowInstanceId`, `workflowType`/`workflowVersion`, `correlationId`; output carries `event_produced`; task ID serves as broker message identity for dedupe.
- KAFKA_PUBLISH (`KAFKA_PUBLISH`): direct Kafka publish with Kafka-specific controls (topic, key, headers, serializers, producer settings).
- Vs worker: prefer EVENT unless the contract needs Kafka-specific keys/headers/serializers -- then KAFKA_PUBLISH. Never write a worker just to publish a queue message.

### JDBC, gRPC, BUSINESS_RULE, SENDGRID, UPDATE_SECRET, GET_SIGNED_JWT

- JDBC (`JDBC`): runs SQL queries/updates against relational databases (MySQL, PostgreSQL, Oracle) via the configured RDBMS (Relational Database Management System) integration, with pooling/transaction handling. Inputs: query/statement plus connection parameters.
- gRPC (`GRPC`): invokes a gRPC service method. Inputs: `method`, `host`, `port`, `request` (JSON payload), `methodType`, `useSSL`, `trustCert`, `headers`, `inputType`/`outputType`, `hedgingConfig.maxAttempts`. Output is the method response. Parameters can be auto-populated from a registered remote service.
- BUSINESS_RULE (`BUSINESS_RULE`): evaluates spreadsheet-like business rules over inputs; for analyst-editable decision tables without code deploys.
- SENDGRID (`SENDGRID`): sends email through the SendGrid integration (to/from/subject/body or template).
- UPDATE_SECRET (`UPDATE_SECRET`): creates or updates a secret stored in the Conductor cluster.
- GET_SIGNED_JWT (`GET_SIGNED_JWT`): mints a signed JWT (JSON Web Token -- a short-lived signed credential) for authenticating downstream calls.
- Related server-side tasks worth knowing: WAIT_FOR_WEBHOOK (pause for webhook), UPDATE_TASK (change another running task's status), QUERY_PROCESSOR (query Conductor search/metrics), OPSGENIE (alerting), NOOP (no-op placeholder).

## Part C -- AI tasks family (server-executed, integration-backed)

All require a configured integration (LLM provider such as OpenAI/Anthropic/Bedrock/Vertex, or a vector store such as Pinecone/Weaviate/Postgres-pgvector/Mongo). They run on the server; use workers only for custom model hosting, private frameworks, or pre/post-processing the tasks cannot express.

### Generation and chat

- LLM_TEXT_COMPLETE (`LLM_TEXT_COMPLETE`): single-prompt text completion. Inputs: `llmProvider`, `model`, `prompt`, `maxTokens`, `temperature`, optional stop sequences.
- LLM_CHAT_COMPLETE (`LLM_CHAT_COMPLETE`): multi-turn chat completion. Inputs: `messages` (system/user/assistant roles), `llmProvider`, `model`, `jsonOutput` (force JSON for tool-routing loops), temperature/token limits. This is the think-step of plan-act agent loops (pair with DO_WHILE + SWITCH + CALL_MCP_TOOL).

### Embeddings and vector search

- LLM_GENERATE_EMBEDDINGS (`LLM_GENERATE_EMBEDDINGS`): text to embedding vector.
- LLM_STORE_EMBEDDINGS (`LLM_STORE_EMBEDDINGS`) / LLM_GET_EMBEDDINGS (`LLM_GET_EMBEDDINGS`) / LLM_SEARCH_EMBEDDINGS (`LLM_SEARCH_EMBEDDINGS`): write, fetch, and similarity-search vectors in the configured vector store (namespace/index parameters select the collection).

### Document indexing and RAG

- LLM_INDEX_DOCUMENT (`LLM_INDEX_DOCUMENT`) / LLM_INDEX_TEXT (`LLM_INDEX_TEXT`): index a stored document or raw text chunk stream into a searchable index. GET_DOCUMENT fetches a stored document; LLM_SEARCH_INDEX (`LLM_SEARCH_INDEX`) queries the index. Together with LLM_CHAT_COMPLETE this is the standard RAG pipeline (index once, retrieve top-k, stuff into chat context).
- CHUNK_TEXT (`CHUNK_TEXT`): splits long text into overlapping chunks (size/overlap parameters) before embedding/indexing.
- PARSE_DOCUMENT (`PARSE_DOCUMENT`): extracts text from binary documents (PDF/DOC); LIST_FILES lists files available in the cluster.

### Tool use and media generation

- LIST_MCP_TOOLS (`LIST_MCP_TOOLS`) / CALL_MCP_TOOL (`CALL_MCP_TOOL`): discover tools on an MCP server and invoke one (`mcpServer`, `method`, `arguments`). This is the act-step of agent loops; route the LLM's chosen action through SWITCH or DYNAMIC first.
- GENERATE_IMAGE (`GENERATE_IMAGE`) / GENERATE_AUDIO (`GENERATE_AUDIO`) / GENERATE_VIDEO (`GENERATE_VIDEO`) / GENERATE_PDF (`GENERATE_PDF`): synthesize media artifacts from a prompt plus format parameters.

## Comparison table

| Operator / task | Purpose | Runs where |
|---|---|---|
| SWITCH | Conditional branch on one expression | Server |
| FORK_JOIN | Fixed parallel branches | Server |
| JOIN | Barrier + output aggregation for forks | Server |
| EXCLUSIVE_JOIN | Join when one alternative branch completes | Server |
| DYNAMIC_FORK (FORK_JOIN_DYNAMIC) | Runtime-count parallel fan-out | Server |
| DYNAMIC | Runtime-resolved single task dispatch | Server |
| DO_WHILE | Counter or list loop with JS exit condition | Server |
| SUB_WORKFLOW | Synchronous nested workflow call | Server |
| START_WORKFLOW | Asynchronous workflow launch | Server |
| TERMINATE_WORKFLOW | Stop a workflow execution | Server |
| WAIT | Pause for duration or timestamp | Server |
| WAIT_FOR_WEBHOOK | Pause until webhook signal | Server |
| HUMAN | Pause for human form completion/approval | Server |
| SET_VARIABLE | Write workflow variables | Server |
| GET_WORKFLOW | Read a workflow execution | Server |
| TERMINATE | End current workflow with explicit status/output | Server |
| YIELD | Suspend until externally resumed | Server |
| HTTP | REST call | Server |
| HTTP_POLL | Poll REST until termination condition | Server |
| INLINE | Small JS/Python expression evaluation | Server |
| JSON_JQ_TRANSFORM | jq JSON reshaping | Server |
| EVENT | Provider-neutral message publish | Server |
| KAFKA_PUBLISH | Direct Kafka publish with producer controls | Server |
| JDBC | SQL query/update | Server |
| GRPC | Remote gRPC method invocation | Server |
| BUSINESS_RULE | Spreadsheet/rule-table evaluation | Server |
| SENDGRID | Email via SendGrid | Server |
| UPDATE_SECRET | Create/update cluster secret | Server |
| GET_SIGNED_JWT | Mint signed JWT | Server |
| UPDATE_TASK | Change another running task status | Server |
| QUERY_PROCESSOR | Query Conductor search/metrics | Server |
| LLM_TEXT_COMPLETE | Single-prompt LLM completion | Server |
| LLM_CHAT_COMPLETE | Multi-turn LLM chat | Server |
| LLM_GENERATE_EMBEDDINGS | Text to vector | Server |
| LLM_STORE_EMBEDDINGS | Write vectors to vector store | Server |
| LLM_GET_EMBEDDINGS | Fetch stored vectors | Server |
| LLM_SEARCH_EMBEDDINGS | Similarity search over vectors | Server |
| LLM_INDEX_DOCUMENT | Index a document for retrieval | Server |
| LLM_INDEX_TEXT | Index raw text for retrieval | Server |
| LLM_SEARCH_INDEX | Search text index (RAG retrieval) | Server |
| CHUNK_TEXT | Split text for embedding/indexing | Server |
| PARSE_DOCUMENT | Extract text from binary documents | Server |
| LIST_MCP_TOOLS | Discover MCP server tools | Server |
| CALL_MCP_TOOL | Invoke an MCP tool | Server |
| GENERATE_IMAGE / AUDIO / VIDEO / PDF | Media synthesis | Server |
| SIMPLE (worker task) | Custom proprietary/heavy logic | Worker (your code) |

**Covers:** https://orkes.io/content/category/reference-docs, https://orkes.io/content/category/reference-docs/operators, https://orkes.io/content/reference-docs/operators/switch, https://orkes.io/content/reference-docs/operators/fork-join, https://orkes.io/content/reference-docs/operators/dynamic-fork, https://orkes.io/content/reference-docs/operators/do-while, https://orkes.io/content/reference-docs/operators/sub-workflow, https://orkes.io/content/reference-docs/operators/wait, https://orkes.io/content/reference-docs/operators/human, https://orkes.io/content/reference-docs/operators/set-variable, https://orkes.io/content/reference-docs/operators/terminate, https://orkes.io/content/category/reference-docs/system-tasks, https://orkes.io/content/reference-docs/system-tasks/http, https://orkes.io/content/reference-docs/system-tasks/inline, https://orkes.io/content/reference-docs/system-tasks/jq-transform, https://orkes.io/content/reference-docs/system-tasks/event, https://orkes.io/content/category/reference-docs/ai-tasks
