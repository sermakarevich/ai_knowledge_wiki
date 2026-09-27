# mateaix/mateclaw
> PDF location (no local source.pdf): https://github.com/mateaix/mateclaw
Source: https://github.com/mateaix/mateclaw
Kind: repo
Fetched: 2026-09-26T13:43:57.968490+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# mateaix/mateclaw

Commit: 6bbd3ac4dac0c04f00f6a95bde6689766f1c51e5

## README

# MateClaw

<p align="center"><b>Your second brain</b></p>

<p align="center"><sub><b>Pluggable Agent Runtime · Native + DSH · Spring Boot inside</b></sub></p>

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black.svg?logo=github)](https://github.com/mateaix/mateclaw)
[![Documentation](https://img.shields.io/badge/Docs-Website-green.svg?logo=readthedocs&label=Docs)](https://claw.mate.vip/docs)
[![Live Demo](https://img.shields.io/badge/Demo-Online-orange.svg?logo=vercel&label=Demo)](https://claw-demo.mate.vip)
[![Website](https://img.shields.io/badge/Website-claw.mate.vip-blue.svg?logo=googlechrome&label=Site)](https://claw.mate.vip)
[![Java Version](https://img.shields.io/badge/Java-21+-blue.svg?logo=openjdk&label=Java)](https://adoptium.net/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-brightgreen.svg?logo=springboot)](https://spring.io/projects/spring-boot)
[![Vue](https://img.shields.io/badge/Vue-3-4FC08D.svg?logo=vuedotjs)](https://vuejs.org/)
[![Last Commit](https://img.shields.io/github/last-commit/mateaix/mateclaw)](https://github.com/mateaix/mateclaw)
[![License](https://img.shields.io/badge/license-Apache--2.0-red.svg?logo=opensourceinitiative&label=License)](LICENSE)

[[Website](https://claw.mate.vip)] [[Live Demo](https://claw-demo.mate.vip)] [[Documentation](https://claw.mate.vip/docs)] [[中文](README_zh.md)]

</div>

<p align="center">
  <img src="assets/images/preview.png" alt="MateClaw Preview" width="800">
</p>

---

> **v2.3.0 (released 2026-09-20) — JSON acceptance and execution evidence for persistent Goals.** Users can configure required JSON fields and bind checks to current requirements and immutable artifact versions. This release also adds controlled worker intervention and skill document/folder uploads, with fixes for DSH history and output budgets, vLLM reasoning, and SSE framing. [Read the release notes](https://claw.mate.vip/docs/en/releases/2.3.0).

---

> **Other personal AI agents are built for one person. MateClaw is the one your IT department can actually sign off on.**
>
> Multi-user workspaces. Approval-gated sensitive actions. Full audit trail. Spring Boot Actuator health monitoring. Per-channel error isolation so one chat platform's outage doesn't take down the rest. One JAR in your environment; you control persisted data, and task content is sent only to model, channel, or tool services you explicitly configure.
>
> **And underneath, a real Agent Runtime.** An employee is no longer welded to one reasoning loop. Choose the native StateGraph runtime for ReAct, Plan-and-Execute, Goals, and Team Runs, or run DeepSeek Harness as a managed external loop over authenticated JSON-RPC. Both paths converge on the same conversations, workspace boundaries, Tool Guard, event projection, and lifecycle controls.

Most AI tools die when their vendor has a bad day. Most forget you the moment the tab closes. Most give you a chatbox and call it a product.

**MateClaw is the whole widget.** One deployment. Reasoning, knowledge, memory, tools, channels — built together, not bolted on. And when your primary model is unavailable, the next healthy provider retries the current request.

---



### 1 · Your AI doesn't die when a model does

Primary key expired. Vendor returns 401. Network blip. Quota drained.

Other tools hand you a red error card. MateClaw tries the next healthy provider in configured order — including built-in and OpenAI-compatible options such as DashScope, OpenAI, Anthropic, Gemini, DeepSeek, Kimi, Ollama, LM Studio, and MLX — and attempts to recover the current request. It returns an error only when the available chain is exhausted. A provider health tracker parks bad vendors in a cooldown window so they don't waste seconds on every turn.

You don't write a retry script. You drag providers into priority order in **Settings → Models** and watch the health dashboard fill with green dots as requests route around failures in real time.



### 2 · Knowledge that links itself

Upload a PDF, a batch of markdown, a scraped page — raw material in.

MateClaw's **LLM Wiki** digests it into structured pages, builds `[[links]]` between them, and preserves traceable citations for generated content. Open the citation drawer to inspect the corresponding source chunk and verify page or answer references.

This is the difference between a warehouse and a library.



### 3 · One product, five surfaces

| Surface | What it is |
|---|---|
| **Web Console** | Full admin — digital employees, models, skills, knowledge, security, cron, **runtime console** (see what every employee is doing, force-recycle in one click) |
| **Desktop** | Electron app with a bundled JRE 21. Double-click, run. No Java install |
| **Webchat Widget** | One `<script>` tag embed. Drop it on any site |
| **IM Channels** | DingTalk · Feishu · WeChat Work · WeChat · Telegram · Discord · QQ · Slack |
| **Plugin SDK** | Java module for third-party capability packs |

Same brain. Same memory. Same tools. Different doors.

<p align="center"><b>$0 · No tokens metered. No seats billed. Your server. Your data. Your keys.</b></p>

---



### Digital employees, not chatbots
You hire coworkers, not chat boxes. Each one has a **Role**, a **Goal**, a **Backstory**, a runtime, a pixel-art avatar, and a color of their own — six built-in templates ship ready (General Assistant · Product Assistant · Research Analyst · Customer Support · Data Analyst · Code Reviewer). Employee identity and governance stay stable even when the execution engine changes.



### Agent Runtime: native or DSH (2.2.0+)
The `AgentRuntimeProvider` contract separates an employee from the engine that runs its turn. The **native runtime** keeps ReAct, Plan-and-Execute, persistent Goals, and Team Runs inside MateClaw. The **DSH runtime** manages `dsh-jsonrpc-agent` as an authenticated child process and streams thinking, text, tool calls, usage, completion, and cancellation back as normalized runtime events. DSH owns the external Agent loop; MateClaw still owns the session, workspace, credentials, tools, approvals, messages, and UI projection. Runtime availability and capabilities are validated before startup, and DSH can be installed, verified, connection-tested, enabled, or disabled from the console. [Configure DeepSeek Harness →](https://claw.mate.vip/docs/en/deepseek-harness)



### Durable long tasks: checkpoint, restart, continue (2.2.0+)
Persistent Goals turn work that takes hours into bounded, recoverable segments. The database preserves the goal checklist, continuation state, attempts, cooldowns, leases, and user input accepted while the worker is busy. After a single backend instance restarts, the supervisor reconciles the interrupted attempt, reads persisted checkpoints and artifacts, and schedules the next safe segment instead of asking you to repeat the task.

For file-producing work, ask the employee to keep a progress ledger, append small verifiable units, inspect the existing tail after recovery, and complete the Goal only after reproducible acceptance checks pass. The runtime does not promise exactly-once behavior for arbitrary external side effects; payments, sends, publishes, and destructive calls still need provider idempotency or review. [Run and verify durable Goals →](https://claw.mate.vip/docs/en/goals)

> Prompt pattern: “Create a persistent Goal first. Save the plan and progress in the workspace, write in small checkpoints, resume from existing evidence after errors or restart, and call `completeGoal` only after every criterion has verifiable evidence.”



### Team Runs (2.1.0+)
One request, one durable **Team Run**. A stable `runId` links the user's objective, task DAG, worker executions, final synthesis, and deliverables. Chat is the outcome surface, Agents Live groups the workers for real-time observation, and Teams owns history and governance — all three consume the same server projection. Worker conversations no longer flood the normal sidebar; summaries and files lead, while tasks, evidence, approvals, and read-only worker records drill down on demand. Underneath, the 2.0 shared board still provides dependency orchestration, parallel dispatch, prerequisite hand-off, execution leases, cancel-interrupt, and human approval gates.



### Knowledge & memory
- **LLM Wiki** — raw materials digest into linked pages with citations; the **hot cache** auto-injects into every employee's system prompt. **Transformations engine** (1.3.0+) turns the Wiki from a search index into a processing pipeline
- **Workspace memory** — `AGENTS.md`, `SOUL.md`, `PROFILE.md`, `MEMORY.md`, daily notes
- **Memory lifecycle** — post-conversation extraction, scheduled consolidation, Dreaming workflows. Workflows can also write directly into an employee's `MEMORY.md` via the `write_memory` step



### Skills · MCP · ACP — three ways to extend capability
- **SKILL.md packages** — manifest + prompt + tool list + **LESSONS.md**. In 2.1, reflection and cross-session recurring-request mining can produce reusable improvements; routine promotion, constrained auto-binding, curator handover/governance, origin policy, snapshots, and restore points keep evolution observable, workspace-scoped, and reversible. Eight starter templates plus a five-step creation wizard, with **Pre-flight checks** before install
- **MCP** — stdio / SSE / Streamable HTTP, plug into any external tool server. **Per-employee binding** (1.3.0+) means a tool you install for one employee doesn't bleed into another's toolbox
- **ACP** — bring top-tier coding agents like Claude Code and Codex in as employees, auto-bridged to skill cards with wrapper tools
- **Tool Guard** — RBAC + approval flow + path protection. Capability needs boundaries



### Business orchestration (1.3.0+)
- **Workflow** — compose multiple employees plus system actions (approval / channel dispatch / write-memory) into a publishable, triggerable, replayable linear DSL. Seven step modes (`sequential` / `fan_out` / `collect` / `conditional` / `await_approval` / `dispatch_channel` / `write_memory`). JSON-first authoring with Monaco + schema validation, or natural-language → draft generation
- **Triggers** — wire system events to workflows or to employee conversations. Six pattern types (`cron` / `webhook` / `channel_message` / `agent_lifecycle` / `content_match` / `workflow_completion`). Default-on event governance: dedup, per-trigger rate limit, bot-self filter, recursion guard, fail-closed unknown patterns
- **Wiki Transformations** — Wiki stops being retrieval-only. User-authored templates run against raw materials or existing pages, with cross-material map-reduce aggregation, reverse-citation extraction, JSON output mode, and per-template model picker



### You see what every employee is doing
**Admin Runtime Console** (`Settings → System → Runtime`) — who's running, which runtime provider owns the turn, what step it is on, how many tokens it uses, and one-click force-recycle when stuck. Native and DSH events enter the same thinking / tool / answer projection; completion, failure, usage, and cancellation retain consistent lifecycle semantics. Per-event SSE IDs make reconnects safe, and Team Runs group member work under one live execution.



### Multimodal creation
Text-to-speech · Speech-to-text · Image · Music · Video · 3D. First-class, not add-ons. **Sidecar routing** (1.3.0+) means a text-only main model + an image attachment no longer dead-ends — a configured vision model describes the image, and the main model answers. **Image edit** lands too: refer to an earlier conversation attachment by `msg:<id>:<idx>` and ask the model to recolor or restyle it. Four **document-generation tools** (`DocxRenderTool` / `XlsxRenderTool` / `PptxRenderTool` / `PdfRenderTool`) render Markdown straight to Office files insi

... (truncated, 17038 more characters)

## pom.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>vip.mate</groupId>
    <artifactId>mateclaw</artifactId>
    <version>${revision}</version>
    <packaging>pom</packaging>

    <name>MateClaw</name>
    <description>MateClaw monorepo reactor and Maven parent</description>

    <!-- Reactor modules. Keep plugin-api before consumers for predictable local builds. -->
    <modules>
        <module>mateclaw-plugin-api</module>
        <module>mateclaw-server</module>
        <module>mateclaw-plugin-sample</module>
        <module>mateclaw-plugin-search-sample</module>
        <module>mateclaw-plugin-mem0</module>
    </modules>

    <properties>
        <!-- MateClaw release version shared by all Maven modules. -->
        <revision>2.4.0-SNAPSHOT</revision>

        <!-- Java -->
        <java.version>21</java.version>
        <maven.compiler.release>${java.version}</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

        <!-- Spring ecosystem -->
        <spring-boot.version>3.5.16</spring-boot.version>
        <spring-ai.version>1.1.8</spring-ai.version>
        <spring-ai-alibaba.version>1.1.2.3</spring-ai-alibaba.version>
        <springdoc.version>2.8.16</springdoc.version>

        <!-- Persistence and core utilities -->
        <mybatis-plus.version>3.5.16</mybatis-plus.version>
        <hutool.version>5.8.26</hutool.version>
        <jjwt.version>0.12.6</jjwt.version>
        <slf4j.version>2.0.16</slf4j.version>
        <jackson.version>2.18.3</jackson.version>

        <!-- Channel and platform SDKs -->
        <dingtalk-stream.version>1.3.12</dingtalk-stream.version>
        <lark-oapi.version>2.7.1</lark-oapi.version>
        <jda.version>6.4.1</jda.version>
        <slack.version>1.48.1</slack.version>

        <!-- Browser automation and WebSocket runtime -->
        <zxing.version>3.5.4</zxing.version>
        <playwright.version>1.62.0</playwright.version>
        <tyrus.version>2.2.2</tyrus.version>

        <!-- Document, wiki, and rendering toolchain -->
        <!-- POI must stay aligned with the POI version tika-parser-microsoft-module
             pulls in transitively (poi-ooxml-full / poi-scratchpad). A skew between
             poi-ooxml-lite and poi-ooxml-full silently breaks XSSF (xlsx) parsing. -->
        <poi.version>5.5.1</poi.version>
        <batik.version>1.19</batik.version>
        <jsoup.version>1.22.2</jsoup.version>
        <tika.version>3.3.0</tika.version>
        <flying-saucer.version>10.2.0</flying-saucer.version>
        <commonmark.version>0.28.0</commonmark.version>
        <archunit.version>1.3.0</archunit.version>
        <shedlock.version>7.7.0</shedlock.version>
        <jgrapht.version>1.5.3</jgrapht.version>
        <pdfbox.version>3.0.7</pdfbox.version>
        <pebble.version>4.1.1</pebble.version>

        <!-- Build plugin versions -->
        <maven-compiler-plugin.version>3.14.1</maven-compiler-plugin.version>
        <maven-dependency-plugin.version>3.8.1</maven-dependency-plugin.version>
        <maven-surefire-plugin.version>3.5.5</maven-surefire-plugin.version>
        <flatten-maven-plugin.version>1.7.3</flatten-maven-plugin.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <!-- ==================== BOM Imports ==================== -->
            <!-- Spring Boot replaces spring-boot-starter-parent while this root POM stays the project parent. -->
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>org.springframework.ai</groupId>
                <artifactId>spring-ai-bom</artifactId>
                <version>${spring-ai.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>org.springdoc</groupId>
                <artifactId>springdoc-openapi-bom</artifactId>
                <version>${springdoc.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>

            <!-- ==================== MateClaw Modules ==================== -->
            <!-- Internal module dependencies share the same revision-controlled version. -->
            <dependency>
                <groupId>vip.mate</groupId>
                <artifactId>mateclaw-plugin-api</artifactId>
                <version>${revision}</version>
            </dependency>
            <dependency>
                <groupId>vip.mate</groupId>
                <artifactId>mateclaw-server</artifactId>
                <version>${revision}</version>
            </dependency>
            <dependency>
                <groupId>vip.mate</groupId>
                <artifactId>mateclaw-plugin-sample</artifactId>
                <version>${revision}</version>
            </dependency>

            <!-- ==================== Spring AI Alibaba ==================== -->
            <dependency>
                <groupId>com.alibaba.cloud.ai</groupId>
                <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
                <version>${spring-ai-alibaba.version}</version>
            </dependency>
            <dependency>
                <groupId>com.alibaba.cloud.ai</groupId>
                <artifactId>spring-ai-alibaba-graph-core</artifactId>
                <version>${spring-ai-alibaba.version}</version>
            </dependency>

            <!-- ==================== Persistence ==================== -->
            <dependency>
                <groupId>com.baomidou</groupId>
                <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
                <version>${mybatis-plus.version}</version>
            </dependency>
            <dependency>
                <groupId>com.baomidou</groupId>
                <artifactId>mybatis-plus-jsqlparser</artifactId>
                <version>${mybatis-plus.version}</version>
            </dependency>

            <!-- ==================== Utilities and Security ==================== -->
            <dependency>
                <groupId>cn.hutool</groupId>
                <artifactId>hutool-all</artifactId>
                <version>${hutool.version}</version>
            </dependency>
            <dependency>
                <groupId>io.jsonwebtoken</groupId>
                <artifactId>jjwt-api</artifactId>
                <version>${jjwt.version}</version>
            </dependency>
            <dependency>
                <groupId>io.jsonwebtoken</groupId>
                <artifactId>jjwt-impl</artifactId>
                <version>${jjwt.version}</version>
            </dependency>
            <dependency>
                <groupId>io.jsonwebtoken</groupId>
                <artifactId>jjwt-jackson</artifactId>
                <version>${jjwt.version}</version>
            </dependency>
            <dependency>
                <groupId>org.slf4j</groupId>
                <artifactId>slf4j-api</artifactId>
                <version>${slf4j.version}</version>
            </dependency>
            <dependency>
                <groupId>com.fasterxml.jackson.core</groupId>
                <artifactId>jackson-databind</artifactId>
                <version>${jackson.version}</version>
            </dependency>

            <!-- ==================== Channel and Automation SDKs ==================== -->
            <dependency>
                <groupId>com.dingtalk.open</groupId>
    

... (truncated, 13725 more characters)
```

## Top-level layout

- .dockerignore (~28 lines)
- .env.example (~165 lines)
- .gitattributes (~19 lines)
- .github/ (dir, 5 files, ~238 lines)
- .gitignore (~135 lines)
- assets/ (dir, 5 files, ~648 lines)
- docker/ (dir, 3 files, ~113 lines)
- docker-compose.yml (~194 lines)
- docs/ (dir, 3 files, ~1549 lines)
- LICENSE (~201 lines)
- mateclaw-desktop/ (dir, 33 files, ~9714 lines)
- mateclaw-plugin-api/ (dir, 11 files, ~665 lines)
- mateclaw-plugin-mem0/ (dir, 11 files, ~1323 lines)
- mateclaw-plugin-sample/ (dir, 3 files, ~104 lines)
- mateclaw-plugin-search-sample/ (dir, 3 files, ~198 lines)
- mateclaw-server/ (dir, 3571 files, ~570824 lines)
- mateclaw-ui/ (dir, 461 files, ~126646 lines)
- mateclaw-webchat/ (dir, 6 files, ~1204 lines)
- pom.xml (~499 lines)
- README.md (~337 lines)
- README_zh.md (~337 lines)
- rfcs/ (dir, 1 files, ~851 lines)

