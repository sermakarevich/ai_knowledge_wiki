---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Rethinking Code Review Workflows with LLM

### Q1. What is the full title, author team, and institutional setting of this study?

> [!tip]- Answer
> The full title is "Rethinking Code Review Workflows with LLM Assistance: An Empirical Study" by Adalsteinsson, Magnússon, Milicevic, Davidsson, and Cheng. It is a field study plus field experiment at WirelessCar Sweden AB with Chalmers University of Technology and University of Gothenburg. The abstract frames code review as critical yet time-consuming and motivates LLM assistance. See [[wiki/01-rethinking-code-review-workflows-with-llm|Rethinking Code Review Workflows with LLM]].

### Q2. What are RQ1 and RQ2, and how do they differ in purpose?

> [!tip]- Answer
> RQ1 is diagnostic: it asks what practices, challenges, and expectations characterize modern code review and where developers see AI helping. RQ2 is exploratory: it asks how developers perceive LLM-assisted review tools and which interaction mode they prefer. RQ1 covers current practice and the automation–human balance, while RQ2 covers trust, satisfaction, barriers, and usability. See [[wiki/02-background-and-research-questions|Background, Related Work, and Research Questions]].

### Q3. What gap in prior LLM-for-review work does this study claim, and what is its support-not-replace stance?

> [!tip]- Answer
> Prior work covered replicating reviewer changes, issue-detection experiments, emotional responses to AI feedback, standards enforcement, fine-tuning, and multi-agent autonomous review. The stated gap is the preferred human–AI collaboration interaction during review, which RQ2 targets. The study takes a support-not-replace stance because LLMs remain prone to hallucinations. See [[wiki/02-background-and-research-questions|Background, Related Work, and Research Questions]].

### Q4. Who participated in Phase 1, and how was the sample constructed?

> [!tip]- Answer
> Phase 1 listed ten participants (P1, P2, P3, P5, P7, P8, P9, P10, P11, P12) spanning QA, application development, security, and software engineering roles. P1 is the Quality Assurance Specialist on Team A, P2 the Application Developer on Team A, and P5 the Security Engineer on Team B. Team A held the largest group (P1, P2, P3, P9), with the rest spread across Teams B, D, E, F, and G. See [[wiki/03-phase1-participants-and-setup|Phase 1 Participants and Setup]].

### Q5. How did Mode A (Co-Reviewer) and Mode B (Interactive Assistant) differ in the Phase 2 experiment?

> [!tip]- Answer
> Mode A proactively auto-generated an up-front summary of major changes and concerns before the reviewer started, plus follow-up Q&A. Mode B gave no proactive summary and answered only when explicitly prompted with targeted questions. Ten developers each reviewed two matched WirelessCar PRs, one per mode, with rotated assignment, think-aloud observation, and post-session interviews. See [[wiki/04-phase2-experiment-design|Phase 2 Experiment Design]].

### Q6. How did the RAG tool and the Mode A `start_review` sub-agent handle PR context?

> [!tip]- Answer
> The tool used a RAG pipeline where `search_requirements` supplied the motivating Jira ticket for the PR. In Mode A a fourth tool, `start_review`, added a sub-agent that performed a structured initial review from the full PR data injected into its context. Injection rather than query-engine retrieval was chosen so every file change would be considered in the complete review. See [[wiki/05-tool-implementation-rag-pipeline|Tool Implementation: RAG Pipeline and Agentic Structure]].

### Q7. What did developers expect from AI assistance, and what accuracy and trust concerns did they raise?

> [!tip]- Answer
> Developers expected AI to catch defects "borderline impossible to catch on the fly," such as race conditions missed in a three-minute review. They warned that false positives erode trust and divert attention from real issues, and feared over-reliance especially in Mode A. Trust was framed as necessary but not blind, acceptable when use is optional but costly when it sends reviewers chasing impossible suggestions. See [[wiki/06-phase1-findings-challenges-and-ai-use-cases|Phase 1 Findings: Challenges and AI Use Cases]].

### Q8. What efficiency gains and what integration and output limitations emerged in Phase 2?

> [!tip]- Answer
> The assistant sped up reviews, cut codebase searching, surfaced missed issues like deadlocks on large PRs, and could suggest documentation updates. Limits included missing broader context such as architecture docs, Jira tickets, and conventions, plus overly long hard-to-scan output and slow responses. Developers wanted embedding in GitHub, Slack, or IDEs with precise file and line references. See [[wiki/07-phase2-findings-trust-and-integration|Phase 2 Findings — Trust and Integration]].

### Q9. When did developers prefer Mode A versus Mode B, and what extra usage patterns did they propose?

> [!tip]- Answer
> Mode A was valued for orientation in unfamiliar or complex codebases, for large PRs needing a manual breakdown, and for low-risk PRs where AI could do most of the work. Preference was often situational ("50/50"), with Mode B favored where reviewers knew the codebase or wanted full control. Proposed extras included Mode A as an author pre-review aid and a human-first-then-validate pattern. See [[wiki/08-interaction-modes-and-design-implications|Interaction Modes and Design Implications]].

### Q10 (Evaluation). A team lead asks whether to roll out a proactive AI co-reviewer as the default for all reviews — what should you recommend?

> [!tip]- Answer
> Recommend against a single default: deploy dual modes with AI-led summaries defaulting on for large, unfamiliar, low-risk, or newcomer reviews and on-demand assistance elsewhere. Justify this by the situational preference finding plus trust, false-positive, latency, and integration risks. Require embedding in existing tools, concise file/line-specific output, fast responses, and deeper requirements and codebase context. See [[wiki/08-interaction-modes-and-design-implications|Interaction Modes and Design Implications]].
