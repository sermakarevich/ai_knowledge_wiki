> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Event-Driven Orchestration and Integrations

**In one sentence:** Conductor starts workflows from API (Application Programming Interface) calls, schedules, webhooks, and broker messages, pauses and resumes them with wait and signal primitives, publishes results back to brokers, and connects both directions through managed broker integrations, an integration task catalog, and API/MCP (Model Context Protocol) gateways.

## Key points

- Triggers are uniform but independent: direct API/SDK (Software Development Kit) start, cron (scheduled) start, verified incoming webhook, broker message via event handler, and signal into a waiting execution all create or advance the same workflow execution model.
- Publishing is a workflow task (`EVENT`, or `KAFKA_PUBLISH` for Kafka-specific producer controls) and consumption is a separate control-plane object (event handler); webhooks are a third path that only starts workflows or resumes `WAIT_FOR_WEBHOOK` tasks, never a general action dispatcher.
- Delivery is at-least-once everywhere, so idempotency keys with strategies `FAIL`, `RETURN_EXISTING`, and `FAIL_ON_RUNNING`, plus idempotent workers and tool calls keyed on business identity, are the correctness mechanism rather than an option.
- Broker support splits by distribution: OSS (open-source software) Conductor covers the internal `conductor` queue, Kafka, SQS (Simple Queue Service), NATS variants, and AMQP (Advanced Message Queuing Protocol); Orkes adds managed Azure Service Bus, GCP (Google Cloud Platform) Pub/Sub, IBM MQ (Message Queue), Confluent Kafka, and Amazon MSK (Managed Streaming for Apache Kafka).
- Outward exposure reverses the direction: API gateway maps HTTP (Hypertext Transfer Protocol) routes to workflows, MCP gateway maps the same routes to callable AI-agent tools, and remote services register external HTTP/gRPC (gRPC Remote Procedure Calls) endpoints with circuit breakers for use inside workflows.
- Credentials stay out of definitions: signing secrets and API keys live in the secrets store or environment variables and are referenced symbolically, while the managed integration catalog surfaces each external system as prebuilt task operations.

---

## Triggers into workflows

Five trigger types start or advance executions. They differ in source and deduplication, not in the execution they produce.

Direct start via API or SDK creates an execution from a named workflow definition and input. The Start Workflow API accepts `idempotencyKey` and `idempotencyStrategy` as headers (`X-Idempotency-key`, `X-on-conflict`); SDKs in Java, Python, JavaScript, C#, and Go expose the same two fields on the start request. Nested starts use the `START_WORKFLOW` and sub-workflow tasks, which also accept idempotency settings.

Scheduled start uses the scheduler service. The legacy form is one Spring six-field cron expression (`second minute hour day-of-month month day-of-week`, macros such as `@daily` accepted) plus an IANA (Internet Assigned Numbers Authority) `zoneId` defaulting to UTC (Coordinated Universal Time). The multi-expression form `cronSchedules` carries per-entry expressions and zones and takes precedence when non-empty. Creation is by CLI (Command Line Interface) for the simple case (`conductor schedule create/get/list/pause/resume/delete`) and by REST (Representational State Transfer) (`POST /api/scheduler/schedules`, search and execution-history endpoints) for the complete model. Each run injects `_startedByScheduler`, `_scheduledTime`, `_executedTime`, `_executionId`, and `_schedulerCron` into workflow input; `correlationId` is copied literally and is not templated. `runCatchupScheduleInstances: true` replays missed slots after downtime and can burst, so targets must be idempotent; `false` resumes from current time. Bounds are epoch-millisecond `scheduleStartTime`/`scheduleEndTime`. There is no native overlap policy, no run-now endpoint, and preview is capped at five times evaluated in the server scheduler timezone rather than the schedule zone.

Incoming webhooks accept HTTP callbacks from providers such as Stripe, Slack, SendGrid, GitHub, or any custom sender. Routes are `POST /webhook/{id}` for the callback body, query, and headers, `GET /webhook/{id}` for provider URL-verification or ping, and `/metadata/webhook` CRUD (Create, Read, Update, Delete) for configuration. Each request is verified before processing, then recorded durably so restarts do not lose it. One verified callback can start receiver workflows, resume matching `WAIT_FOR_WEBHOOK` tasks, or both. Verification types are `HEADER_BASED`, `SIGNATURE_BASED` (`sha256=` HMAC-SHA-256 (Hash-based Message Authentication Code, Secure Hash Algorithm 256) of raw body), `HMAC_BASED` (Base64-decoded secret), `SLACK_BASED` (signature plus timestamp replay check, returns `challenge`), `STRIPE`, `TWITTER` (returns signed `response_token` on `crc_token`), and `SENDGRID` (ECDSA (Elliptic Curve Digital Signature Algorithm) public key). Webhook starts accept dynamic idempotency keys derived from input, for example `${workflow.input.order_id}`.

Broker-message start uses event handlers, described below: a handler subscribes to `provider:destination`, tests a JavaScript condition against the payload, and runs a `start_workflow` action with input mapped from payload fields.

Signals into running workflows address a known waiting execution directly. A signal completes the current `WAIT` in a targeted workflow, which is the narrower alternative when the caller already knows the workflow ID rather than broadcasting over a broker or webhook.

## Eventing primitives inside executions

Publishing, pausing, routing, and status emission are four distinct primitives.

The `EVENT` task publishes a provider-neutral message to an enabled event-queue provider. Its `sink` is `provider:provider-specific-destination`; OSS provider keys include `conductor`, `kafka`, `sqs`, `nats`, `jsm`, `nats_stream`, `amqp_queue`, and `amqp_exchange`. The `conductor` provider namespaces short sinks by workflow, so `conductor:order-status` in workflow `order_workflow` expands to `conductor:order_workflow:order-status`, and handlers must subscribe to the expanded name. Conductor resolves `inputParameters`, then appends `workflowInstanceId`, `workflowType`/`workflowVersion`, `correlationId`, and `taskToDomain` to the broker message; task output adds `event_produced` (not sent on the wire). The task ID serves as the broker message identity for duplicate detection. With `asyncComplete: false` a successful publish completes the task; with `true` the task stays `IN_PROGRESS` until an external update or a handler `complete_task`/`fail_task` resolves it. `KAFKA_PUBLISH` is reserved for contracts needing Kafka keys, headers, serializers, or producer controls; the docs direct all other Kafka destinations to `EVENT`.

`WAIT_FOR_WEBHOOK` pauses a workflow mid-execution until a matching verified webhook callback arrives, at which point the callback payload resumes the task. It is the webhook-side counterpart of the generic `WAIT` plus signal pattern.

Event handlers route broker messages to actions. A handler names `event`, a JavaScript `condition` rooted at the delivered payload (for example `$.status == 'READY'`; missing means true), `evaluatorType` (`javascript` or a registered evaluator), placeholder-mapped `actions`, and `active` (defaults to `false`). Placeholders use `${fieldName}` with dot notation for nesting; `expandInlineJSON: true` is only for fields that are intentionally JSON-encoded strings. Supported actions are `start_workflow`, `complete_task`, `fail_task`, `terminate_workflow` (Orkes only), `update_workflow_variables` (Orkes only), and `start_agent`. Task-targeting actions require an exact target -- `taskId`, or `workflowId` plus `taskRefName` -- and a business correlation key alone does not resolve. On Kafka, ordering behavior follows the partition and handler configuration rather than workflow order. Handler execution is monitored via `event_execution_success`/`event_execution_error` plus queue-depth and message counters; broker acknowledgement alone does not prove the downstream action landed.

Workflow status events and CDC (Change Data Capture) are outbound feeds rather than tasks. Status events notify external systems as executions change state; CDC emits workflow state changes for downstream indexing or mirroring. Both are configured at platform level and consumed outside any single execution.

## Supported message brokers

The event name grammar is `provider:provider-specific-destination`, split at the first colon, and the provider must be enabled on the server. On Orkes the provider segment is the configured managed integration name, which is not interchangeable with OSS provider keys.

Documented coverage by distribution:

- Internal `conductor` queue: OSS yes, Orkes not listed as a managed broker (used as namespaced intra-cluster channel in OSS examples).
- Kafka (Apache Kafka, including Confluent Kafka and Amazon MSK as managed variants): both.
- SQS (Amazon Simple Queue Service): both.
- NATS (Neural Autonomic Transport System) core, JetStream, and Streaming: OSS yes; Orkes yes for NATS messaging (JetStream/Streaming matrix entries are OSS-only).
- AMQP queue and exchange, including RabbitMQ: both.
- Azure Service Bus: Orkes only.
- GCP Pub/Sub: Orkes only.
- IBM MQ: Orkes only.

Handler event strings on Orkes use the form `message-broker-type:integration-name:topic-or-queue`, with broker types `amqp`, `sqs`, `azure`, `kafka`, `nats`, `gcp_pubsub`, and `ibm_mq`. The UI lists only integrations actually configured on the cluster; the topic or queue name must be appended or the payload has no valid destination. Operational signals are broker queue depth (`event_queue_depth`), processed/handled/error counters, and handler action outcomes.

## Exposing workflows outward

API gateway exposes workflows as REST endpoints. The documented sequence is: create one workflow per endpoint; create an Orkes application (the service-account identity) with `EXECUTE` permission on those workflows; create a reusable auth config (`API Key` or `No Authentication`, bound to the application so the gateway inherits its permissions via access-key/JWT (JSON Web Token)); define a service (logical group of routes sharing base path, auth config, and CORS (Cross-Origin Resource Sharing) policy with allowed origins, methods, and headers); then define each route as method plus path mapped to a workflow name and version, with request/response mapping and optional transforms. Routes are testable from the console (test request, execution link, endpoint detail) and monitored by request, latency, and error statistics.

MCP gateway follows the same five steps with `MCP Enabled` on the service, then adds a sixth: connect the service to AI agents as an MCP tool. Each route becomes a tool definition the agent can discover and call; the gateway executes the backing workflow under the bound application identity and returns its output as the tool result. An MCP Workbench verifies tool listing and invocation.

Remote services go the opposite direction: they register external systems for use inside workflows. An HTTP service is defined by a Swagger (OpenAPI) URL plus optional extra hosts and authorization key/value; a gRPC service by host, port, and either server reflection or an uploaded compiled proto descriptor (`protoc --descriptor_set_out`). Endpoints are discovered automatically or added manually with resource name, path, method type, and accept/content types. Tested endpoints generate a sample execution. In workflows, HTTP and HTTP Poll tasks (and separately gRPC tasks) use `Populate from remote services` to fill host, method, and parameters from the registry entry. Per-service circuit breakers short-circuit failing or slow calls with thresholds for failure rate, slow-call rate and duration, half-open wait, and automatic open-to-half-open transition; status and manual open/close are API-accessible. Hedging (parallel duplicate requests, first success wins) reduces tail latency but is restricted to idempotent operations. Schemas register automatically from discovery for contract validation.

## Managed integrations catalog

Beyond brokers and gateways, the catalog provides prebuilt connectors grouped by domain. Counts change over time; the structure is stable:

- AI/LLM (Large Language Model): OpenAI, Azure OpenAI, Anthropic Claude, Google Vertex AI and Gemini, AWS Bedrock variants (Anthropic, Cohere, Titan), Cohere, Mistral, Hugging Face, Ollama, Perplexity, Grok.
- Vector databases for RAG (Retrieval-Augmented Generation): Pinecone, Weaviate, Postgres Vector, MongoDB Vector.
- Cloud storage and functions: AWS S3 (Simple Storage Service) and Lambda, Google Cloud Storage and Cloud Functions, Azure Storage and Azure Functions; plus generic AWS and GCP provider entries.
- Productivity and collaboration: Slack, Google Docs, Sheets, Drive, Calendar, Slides, Notion, Discourse.
- Project and source management: Jira, GitHub and generic Git repository.
- Data: PostgreSQL, MySQL, Redis, generic relational-database (JDBC (Java Database Connectivity)) access.
- Commercial and content: Stripe (payments), HubSpot (CRM (Customer Relationship Management)), SendGrid (email), WordPress (CMS (Content Management System)), Common Room (community).

Each connector documents its operations separately (for example Slack operations, GitHub operations, S3 operations). The catalog is distinct from message-broker integrations and from remote-service registrations, though all three end up invoked as tasks.

## Secrets, environment variables, and task surfacing

Secrets hold signing keys, HMAC keys, private keys, API keys, and service credentials. Webhook verifiers, gateway auth configs, and remote-service authorization reference secrets symbolically (for example `${workflow.secrets.PAYMENT_WEBHOOK_SECRET}`); literals must never appear in workflow definitions or examples. Environment variables carry non-secret per-environment configuration and have their own CRUD and tagging API. Applications bind identity to permissions, so a gateway or integration caller receives only the workflows and operations its application grants.

In workflow definitions, integrations appear as tasks. Catalog operations are selected as task types with operation-specific inputs; remote-service endpoints populate HTTP, HTTP Poll, and gRPC task parameters; broker interaction uses `EVENT`/`KAFKA_PUBLISH` for output, event handlers or `WAIT_FOR_WEBHOOK`/`WAIT` plus signals for input, and LLM/MCP tasks (`LIST_MCP_TOOLS`, `CALL_MCP_TOOL`) for agent tool use. Task-level retries, timeouts, and rate limits sit above service-level circuit breakers, and both layers assume at-least-once delivery with idempotent side effects.

**Covers:** https://orkes.io/content/devguide/integrations, https://orkes.io/content/devguide/how-tos/event-bus, https://orkes.io/content/event-driven-orchestration/publish-events, https://orkes.io/content/event-driven-orchestration/receive-events, https://orkes.io/content/developer-guides/event-handler, https://orkes.io/content/developer-guides/webhook-integration, https://orkes.io/content/developer-guides/scheduling-workflows, https://orkes.io/content/developer-guides/api-gateway, https://orkes.io/content/developer-guides/mcp-gateway, https://orkes.io/content/remote-services, https://orkes.io/content/idempotency
