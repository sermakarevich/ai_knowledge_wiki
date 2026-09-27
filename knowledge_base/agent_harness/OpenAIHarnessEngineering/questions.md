---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Harness Engineering

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What was the hard constraint of the experiment, and what scale did the team reach under it?

> [!tip]- Answer
> Zero manually-written lines of code for five months on a real internal-beta product; roughly one million lines and about 1,500 merged PRs from a team growing 3 to 7 engineers, at an estimated 1/10th the hand-written time. See [[wiki/01-zero-hand-written-code-experiment|The Zero-Hand-Written-Code Experiment]].

### Q2. How did the engineer's job change once humans stopped writing code?

> [!tip]- Answer
> From writing code to designing environments, specifying intent, and building feedback loops; engineers work depth-first, turning each agent failure into a missing capability (tool, guardrail, abstraction, doc) that Codex itself encodes. See [[wiki/01-zero-hand-written-code-experiment|The Zero-Hand-Written-Code Experiment]].

### Q3. How does a pull request get driven to completion in this system, and what role do humans play in review?

> [!tip]- Answer
> Codex reviews its own changes, requests additional agent reviews locally and in the cloud, responds to feedback, and iterates until all agent reviewers are satisfied (a Ralph Wiggum loop); humans may review but are not required, with most review effort agent-to-agent. See [[wiki/01-zero-hand-written-code-experiment|The Zero-Hand-Written-Code Experiment]].

### Q4. Why did the team make the running application directly operable by Codex, and what three capabilities did that include?

> [!tip]- Answer
> Human QA became the bottleneck, so Codex got per-worktree bootable instances, CDP browser control (DOM snapshots, screenshots, navigation), and an ephemeral per-worktree observability stack queried with LogQL/PromQL, enabling multi-hour autonomous verification runs. See [[wiki/02-application-legibility|Making the Application Legible to Agents]].

### Q5. Give an example of a quantitative prompt that becomes tractable once observability is agent-legible, and explain why.

> [!tip]- Answer
> "Service startup under 800ms" or "no span over two seconds in four critical user journeys": the agent can check them against its isolated copy's real logs and metrics instead of guessing, turning an aspiration into a measured acceptance test. See [[wiki/02-application-legibility|Making the Application Legible to Agents]].

### Q6. Why did the "one big AGENTS.md" fail, and what replaced it?

> [!tip]- Answer
> It crowded out task context, saturated into non-guidance, rotted into stale rules, and resisted mechanical verification; replaced by a ~100-line AGENTS.md map pointing into a structured, CI-validated docs/ system of record with progressive disclosure and a doc-gardening agent. See [[wiki/03-repository-knowledge-system-of-record|Repository Knowledge as the System of Record]].

### Q7. What is the "anything Codex can't reach in-context doesn't exist" rule, and what does it imply for team habits?

> [!tip]- Answer
> Only repository-local versioned artifacts are visible to the agent, so Slack decisions, Google Docs, and tacit knowledge must be encoded into the repo or they stay illegible, exactly like onboarding a future hire; it also favors boring, modelable dependencies and occasional reimplementation over opaque libraries. See [[wiki/03-repository-knowledge-system-of-record|Repository Knowledge as the System of Record]].

### Q8. Describe the enforced layered architecture: the layer order, the Providers rule, and how violations are caught.

> [!tip]- Answer
> Each domain stacks Types to Config to Repo to Service to Runtime to UI with forward-only dependencies, and cross-cutting concerns enter only via a single Providers interface; Codex-generated custom linters and structural tests enforce it, with lint errors carrying remediation instructions. See [[wiki/04-architecture-taste-throughput|Enforcing Architecture and Taste]].

### Q9. When is the permissive merge philosophy (minimal gates, flakes via follow-up runs) justified, and when would it be irresponsible?

> [!tip]- Answer
> Justified when agent throughput far exceeds human attention so corrections are cheap and waiting is expensive, with agent-to-agent review absorbing verification; irresponsible at low throughput where each bad merge is costly and slow to fix. See [[wiki/04-architecture-taste-throughput|Enforcing Architecture and Taste]].

### Q10. What are the golden principles, how does garbage collection work, and what is the weakest link in the article's evidence for it?

> [!tip]- Answer
> Opinionated mechanical rules (shared utilities over hand-rolled helpers; validate at boundaries with typed SDKs, never YOLO-probe) enforced by recurring background Codex tasks opening sub-minute-review refactor PRs; the weakest link is that effectiveness is asserted from one self-reported codebase with no control comparison or long-term drift metrics, so transferability is unproven. See [[wiki/05-autonomy-entropy-learnings|Autonomy, Entropy, and What Comes Next]] and [[critical_thinking|Critical Analysis]].
