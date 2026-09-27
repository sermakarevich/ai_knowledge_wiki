> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Context Engineering for Multi-Agent LLM Code

**In one sentence:** Single-agent LLM coders fail on repository-level tasks for lack of task-specific context, so the paper proposes context engineering — a four-component workflow (GPT-5 intent clarification, Elicit retrieval, NotebookLM synthesis, Claude Code multi-agent execution) that improves single-shot accuracy and project-context adherence on a large real codebase.

## Key points

- Single-agent prompt-driven coders struggle on multi-file, repository-level tasks because of limited context windows and hallucinations on unfamiliar APIs or frameworks outside training data.
- A fixed static context such as one `CLAUDE.md` file cannot cover every task; in early experiments a default Claude Code agent with basic `CLAUDE.md` produced incomplete or incorrect solutions, missing distant-file edits or misusing unfamiliar libraries.
- Prior multi-agent and retrieval systems prove the mechanism: MASAI's specialized sub-agents reached 28.3% resolution on SWE-Bench Lite, HyperAgent's Planner/Navigator/Editor/Executor team reached 31.4% on SWE-Bench Verified, and AllianceCoder's retrieved API descriptions yielded up to 20% higher pass@1 accuracy.
- The proposed workflow has four components: (1) GPT-5 Intent Translator rewriting the request into a structured task specification, (2) Elicit-based semantic retrieval of documentation/research, (3) NotebookLM synthesis into a concise summary/table-of-contents with follow-up Q&A, and (4) a Claude Code multi-agent system (planner, coder, tester, reviewer) plus a vector database for code context with iterative refinement.
- Context engineering is defined as systematically constructing and supplying all relevant information for a task — clarified intent, high-level plans, external knowledge, repository-specific details — via a coordinated multi-agent process.
- The system was implemented on the RainMakerz Next.js application (~180K lines of code), where it implemented complex features in a single generation cycle — e.g. a new interactive visualization module spanning front-end and back-end — while a baseline single-agent Claude often omitted needed steps.
- The authors claim explicit context layering plus agent role decomposition fixes failure modes of earlier methods, matching or exceeding CodePlan and DARS on similar tasks, and outline a production path via CI integration (Claude Code in GitHub Actions for automated reviews) with cost, scalability, and safety safeguards.

---

## Abstract

The chunk is the paper front matter and abstract (arXiv:2508.08322v1 [cs.SE] 9 Aug 2025, Muhammad Haseeb, muhammadhaseeb@vt.edu):

> "Large Language Models (LLMs) have shown promise in automating code generation and software engineering tasks, yet they often struggle with complex, multi-file projects due to context limitations and knowledge gaps."

The abstract states the integrated approach "leverages intent clarification, retrieval-augmented generation, and specialized sub-agents orchestrated via Claude's agent framework," and claims it "significantly improves the accuracy and reliability of code assistants in real-world repositories, yielding higher single-shot success rates and better adherence to project context than baseline single-agent approaches."

Qualitative evidence cited: "a large Next.js codebase" where "the multi-agent system effectively plans, edits, and tests complex features with minimal human intervention," compared against "CodePlan, MASAI, and HyperAgent."

## 1. Introduction — why single agents fail

Repository-level tasks require coordinating changes across multiple files, understanding existing architecture, and incorporating domain knowledge outside training data. Verbatim:

> "Purely prompt-driven single-agent solutions struggle with these challenges due to limited context windows and the risk of hallucinations when confronted with unfamiliar APIs or frameworks."

> "A key limitation of default code assistants is their reliance on a fixed static context."

The concrete failure case: "a default Claude Code agent with a basic CLAUDE.md prompt often produced incomplete or incorrect solutions for non-trivial features. It might miss necessary edits in distant files or misuse an unfamiliar library, reflecting insufficient context comprehension." This is linked to CodePlan's framing of repository coding as multi-step planning, not single-step generation [3, 2].

Prior-work numbers given in the introduction:

| System | Mechanism | Reported result (per chunk) |
|---|---|---|
| MASAI (Modular Architecture for Software Engineering AI) | Specialized sub-agents for planning, localization, generation, testing | 28.3% resolution on SWE-Bench Lite |
| HyperAgent | Planner, Navigator, Code Editor, Executor mimicking human developer workflow | Improved issue resolution on complex repositories |
| AllianceCoder | Generates natural-language API descriptions, retrieves relevant API info to guide generation | Up to 20% higher pass@1 accuracy |

Claim: "providing the right information and breaking down tasks are crucial to scaling LLMs to complex coding problems."

## Contributions — the four-component workflow

By context engineering the authors mean:

> "systematically constructing and supplying all relevant information needed for a coding task — ranging from clarified intent and high-level plans to external knowledge and repository-specific details — and doing so via a coordinated multi-agent process."

The four contributions as listed:

1. Workflow design: (1) Intent Translator using GPT-5; (2) Elicit-based semantic paper/document retrieval (e.g. algorithms, API usage guidelines); (3) NotebookLM document synthesis (concise summary or table-of-contents plus follow-up questions); (4) Claude Code multi-agent system (planner, coder, tester, reviewer) with a vector database and iterative refinement.
2. Real-world implementation on the RainMakerz Next.js Web application (~180K lines of code), with single-generation-cycle features/bug fixes; example: "successfully added a new interactive visualization module spanning front-end and back-end changes in one try, whereas a baseline single-agent Claude often omitted needed steps."
3. Comparison to prior state of the art (CodePlan [3], DARS [4]): "explicit context layering and role decomposition" address observed failure modes; "higher reliability in producing working code on the first attempt, matching or exceeding the performance reported for frameworks like CodePlan [3] and DARS [4]"; decisions "such as using retrieved API descriptions or enforcing agent-specific contexts" are informed by prior work.
4. Production pathway: integration with CI pipelines "e.g., using Claude Code in GitHub Actions for automated code reviews," plus scalability, cost, and safety considerations; claim the assistant "can be made production-ready for team use, given appropriate safeguards and iterative tuning."

Paper roadmap stated in chunk: Section 2 related work; Sections 3–4 workflow design and architecture; Section 5 experiments/case studies; Section 6 analysis; Section 7 conclusion.

## 2. Related Work (beginning) — coding agents

Chunk covers only the opening of Section 2 ("LLM-based Coding Agents"):

- HyperAgent [1]: "centralized multi-agent framework with four specialist agents (Planner, Navigator, Code Editor, Executor) working in concert," with "state-of-the-art results on tasks like GitHub issue resolution, achieving a 31.4% success rate on the SWE-Bench Verified benchmark."
- MASAI (Arora et al., 2024): "modular architecture of LLM-powered sub-agents, each responsible for a distinct phase such as test generation, issue reproduction, code editing, or solution ranking"; "By dividing the problem and allowing sub-agents to gather information from different parts of the repository, MASAI attained the highest performance (28.33% resolution rate) on SWE-Bench Lite at the time of its publication [2]."
- The authors draw from these a "hub-and-spoke orchestration pattern where a central orchestrator (Claude) delegates to specialized roles (Section 4)."

**Covers:** Abstract + Section 1 Introduction + opening of Section 2 (LLM-based Coding Agents: HyperAgent, MASAI); arXiv:2508.08322v1, August 2025.
