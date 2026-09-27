# TDD Governance for Multi-Agent Code Generation via Prompt Engineering
Source: https://arxiv.org/abs/2604.26615v1
Kind: pdf
Fetched: 2026-09-23T19:54:17.641370+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                           TDD Governance for Multi-Agent Code Generation via Prompt
                                                                 Engineering
                                                            Tarlan Hasanli∗                                               Shahbaz Siddeeq∗                                Bishwash Khanal
                                                         tarlan.h.hasanli@jyu.fi                                       shahbaz.siddeeq@tuni.fi                         bishwash.b.khanal@jyu.fi
                                                         University of Jyväskylä                                         Tampere University                             University of Jyväskylä
                                                           Jyväskylä, Finland                                             Tampere, Finland                                 Jyväskylä, Finland

                                                            Pyry Kotilainen                                              Tommi Mikkonen                                Pekka Abrahamsson
                                                        pyry.kotilainen@jyu.fi                                        tommi.j.mikkonen@jyu.fi                        pekka.abrahamsson@tuni.fi
                                                        University of Jyväskylä                                        University of Jyväskylä                          Tampere University




arXiv:2604.26615v1 [cs.SE] 29 Apr 2026
                                                          Jyväskylä, Finland                                             Jyväskylä, Finland                              Tampere, Finland

                                         Abstract                                                                                        ACM Reference Format:
                                         Large language models (LLMs) accelerate software development                                    Tarlan Hasanli, Shahbaz Siddeeq, Bishwash Khanal, Pyry Kotilainen, Tommi
                                                                                                                                         Mikkonen, and Pekka Abrahamsson. 2026. TDD Governance for Multi-
                                         but often exhibit instability, non-determinism, and weak adher-
                                                                                                                                         Agent Code Generation via Prompt Engineering. In Proceedings of The
                                         ence to development discipline in unconstrained workflows. While                                30th International Conference on Evaluation and Assessment in Software
                                         test-driven development (TDD) provides a structured Red-Green-                                  Engineering (EASE 2026). ACM, New York, NY, USA, 5 pages. https://doi.
                                         Refactor process, existing LLM-based approaches typically use tests                             org/XXXXXXX.XXXXXXX
                                         as auxiliary inputs rather than enforceable process constraints. We
                                         present an AI-native TDD framework that operationalizes classi-
                                         cal TDD principles as structured prompt-level and workflow-level                                1    Introduction
                                         governance mechanisms. Extracted principles are formalized in a                                 The discipline of software engineering is undergoing a major shift
                                         machine-readable manifesto and distributed across planning, gener-                              as autonomous LLM-based agents take on complex coding tasks
                                         ation, repair, and validation stages within a layered architecture that                         [17]. In agentic AI, role-specific agents collaborate to achieve pro-
                                         separates model proposal from deterministic engine authority. The                               gramming goals with limited human intervention [4]. While this
                                         system enforces phase ordering, bounded repair loops, validation                                can improve productivity, LLMs remain non-deterministic. Even
                                         gates, and atomic mutation control to improve stability and repro-                              identical prompts often produce different outputs, and a tempera-
                                         ducibility. We describe architecture and discuss encoding software                              ture of zero does not ensure consistent results [15]. In multi-agent
                                         engineering discipline directly into prompt orchestration, which                                settings, small logic errors can spread across the workflow, which
                                         we think offers a promising direction for reliable LLM-assisted                                 makes automated guardrails essential for code quality and reliability
                                         development.                                                                                    [7, 22].
                                                                                                                                            One potential solution comes from Test-Driven Development,
                                         CCS Concepts                                                                                    introduced through Extreme Programming, where tests are writ-
                                                                                                                                         ten before implementation so correctness is defined in advance
                                         • Software and its engineering → Software development tech-                                     [1]. However, TDD can be demanding because developers must
                                         niques; Automatic programming; • Computing methodolo-                                           maintain both design intent and detailed test logic, which often
                                         gies → Artificial intelligence; Machine learning.                                               reduces productivity during adoption [2, 19]. AI-native engineer-
                                                                                                                                         ing offers a practical complement: TDD provides clear pass or fail
                                         Keywords                                                                                        constraints, and LLMs can generate much of the repetitive test code
                                         Test-Driven Development, Large Language Models, Multi-Agent                                     that developers often find tedious [5].
                                         Systems, Prompt Engineering, Software Engineering Governance                                       This paper presents a prompt-centric multi-agent framework
                                                                                                                                         that turns TDD principles into enforceable rules for LLM-based
                                                                                                                                         code generation. Specialized agents follow explicit guidance, and an
                                         ∗ Both authors contributed equally to this research.
                                                                                                                                         orchestrator controls phase order and checks test outcomes before
                                                                                                                                         transitions. It also limits repair loops. By embedding TDD into the
                                                                                                                                         prompt architecture, the framework aims to reduce instability in
                                         Permission to make digital or hard copies of all or part of this work for personal or           LLM-generated code while preserving the efficiency benefits of
                                         classroom use is granted without fee provided that copies are not made or distributed
                                         for profit or commercial advantage and that copies bear this notice and the full citation
                                                                                                                                         agentic AI
                                         on the first page. Copyrights for components of this work owned by others than the
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission
                                                                                                                                         2    Background and Motivation
                                         and/or a fee. Request permissions from permissions@acm.org.                                     This section reviews the empirical evidence that motivates encod-
                                         EASE 2026, Glasgow, Scotland, United Kingdom                                                    ing TDD as a governed multi-agent protocol. We organize the
                                         © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM                                                              discussion around three themes: classical TDD foundations, LLM
                                         https://doi.org/XXXXXXX.XXXXXXX                                                                 instability factors, and test-guided prompting approaches.
EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom                                                                         Hasanli et al.


    Beck’s formulation of TDD operationalizes development as micro-         implementation, and bounded repair, across multi-agent workflows.
iterations: tests specify behavior before implementation, encourage         Three empirically supported observations summarize this gap:
minimal solutions, and require continuous refactoring after reach-
                                                                               (1) Classical TDD relies on disciplined phase ordering and behavior-
ing a passing state [1]. Fowler’s refactoring catalog complements
                                                                                   preserving refactoring backed by tests [1, 6].
this by defining safe structural transformations and highlighting
                                                                               (2) LLM-based software engineering exhibits instability through
that automated tests are the prerequisite for verifying behavior
                                                                                   hallucinations, non-determinism, and reproducibility gaps
preservation [6]. Together, these sources motivate a process view
                                                                                   [10, 15, 21, 23].
in which tests are not merely evaluation artifacts but an explicit
                                                                               (3) Test-guided and structured prompting approaches improve
control mechanism for incremental design change.
                                                                                   correctness but do not enforce full TDD discipline as a gov-
    Recent advances in large language models have reduced the
                                                                                   erned protocol [3, 5, 8, 14, 16].
cost of code generation, enabling synthesis from natural-language
specifications and interactive debugging. Test-guided prompting                A central open problem therefore remains: how to translate clas-
improves functional correctness and developer confidence in LLM-            sical TDD principles into enforceable, governance-aware prompt
assisted tasks [5, 14], but these systems do not inherently enforce         structures that ensure bounded autonomy and phase discipline
disciplined processes such as phase ordering, minimal implemen-             across multi-agent workflows. The framework presented in Sec-
tation, or bounded repair cycles. Repository-scale analysis shows           tion 3 addresses this gap.
that LLMs produce incorrect or nonsensical code due to contex-
tual dependency errors, insufficient grounding, and overconfident           3 AI-Native TDD
interpolation [23]. Retrieval augmentation reduces hallucinations,
indicating that reliability depends on prompt context quality as
                                                                            3.1 Deriving Enforceable Principles from TDD
well as model capability.                                                       Literature
    Non-determinism further weakens workflows stability: identical          We begin by describing how TDD principles are extracted and
prompts often produce different outputs, with zero equal test out-          formalized as enforceable guidelines. Our goal is not to summarize
puts in up to 75.76% of cases on complex benchmarks [15]. Similar           TDD books or re-document practices. Instead, we distill the key
variability appears in code review tasks [10], and apparently correct       normative rules that early TDD literature treats as correct. We focus
code may still fail in clean environments due to dependency and             on rules that often break down in real teams under time and delivery
configuration issues [21]. These findings suggest that functional           pressure. We therefore focus on principles that were framed as the
correctness alone is insufficient and motivate governed workflows           "right" way to develop, yet were economically fragile for humans
with reproducibility controls.                                              because they demanded continuous attention, constant feedback,
    Interaction-centered evidence shows further failure modes, in-          and non-deferrable cleanup work.
cluding incomplete answers, excessive outputs, missing precondi-               Source scope and selection. We bounded the extraction corpus
tions, and prompt sensitivity, often requiring manual decomposi-            to Kent Beck [1] and Robert C. Martin [12, 13] as a small canon-
tion and iterative steering [20]. Test cases improve performance            ical and practice-oriented source base. These texts were selected
by reducing ambiguity and acting as executable specifications [14].         because they articulate TDD in explicit prescriptive terms, center
WebApp1K similarly finds that when tests serve as both a prompt             the Red-Green-Refactor micro-cycle, and frame rapid, trustwor-
and a verifier, success depends heavily on instruction following and        thy feedback as the core mechanism for reducing development
in-context learning [3].                                                    risk. The objective of this step was not to synthesize all influen-
    Interactive workflows further support test-centric iteration. TiCoder   tial TDD perspectives, but to derive a methodologically consistent
blends TDD-style test refinement with code generation, reporting            set of norms that could be translated into enforceable governance
improved correctness and reduced cognitive load [5]. At repository          rules for AI-assisted development. Other influential perspectives,
scale, TDFlow decomposes workflows into specialized sub-agents              including later design-oriented or object-oriented interpretations of
for patching, debugging, and revising, achieving high pass rates            TDD, were therefore not excluded because they lack relevance, but
with ground-truth tests [8]. Our contribution instead emphasizes            because incorporating them would have required a broader compar-
governed execution under model non-determinism through deter-               ative synthesis across partially heterogeneous formulations of TDD,
ministic validation, bounded repair, and engine-controlled state            which was outside the scope of this study. We accordingly treat the
mutation. Practical guidance for TDD-style LLM use emphasizes               resulting principle set as corpus-bounded rather than exhaustive.
that test-first interaction patterns, descriptive signatures, and fo-       We treated statements as candidates for extraction when they satis-
cused unit tests improve reliability over naive prompting [16].             fied two criteria: (i) the statement is prescriptive (a “must/should”
    Empirical prompt engineering work shows that iterative self-            about how to work), rather than descriptive or tool-specific; and (ii)
evaluation loops (Self-Refine) and structured Chain-of-Thought              violating the statement is a historically common coping strategy
prompting measurably improve code generation quality [11, 18].              under deadline pressure (e.g., batching changes, weakening tests,
Integrating deterministic diagnostics, such as static analysis warn-        or skipping refactoring).
ings as feedback, can further improve non-functional dimensions                Extraction method. We performed a manual, concept-level syn-
like maintainability [9].                                                   thesis rather than a chapter-by-chapter summary. We collected
    These studies establish that structured prompting and determin-         candidate statements and normalized them into a consistent prin-
istic feedback improve outcomes, but they do not specify how to en-         ciple form with: (1) a short label, (2) an "original intent" phrased
force process discipline, specifically TDD phase ordering, minimal          in human-era terms (why this was believed right), and (3) a source
TDD Governance for Multi-Agent Code Generation via Prompt Engineering                                 EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom


reference. We merged them into a single principle in which mul-                        Manifesto representation. The machine-readable manifesto is im-
tiple phrasings expressed the same underlying norm. Conversely,                     plemented as a JSON-based structured1 schema in which each prin-
we split it into separate principles to preserve machine-actionable                 ciple is encoded as a governance object. In addition to bibliographic
semantics when a single passage contained multiple independent                      grounding, each entry includes an identifier, a concise title, the orig-
norms (e.g., phase ordering plus minimality).                                       inal human-oriented intent, an AI-native interpretation, operational
    What qualifies as a "principle." We define a TDD principle as                   constraints, and anti-patterns. This representation is used at two
a constraint on order, granularity, or quality of feedback in the                   levels: interpretation fields guide role-specific prompt construction,
development loop: Order constraints enforce sequencing (e.g.,                       while constraint and anti-pattern fields are mapped to runtime en-
test-first, Red–Green–Refactor), Granularity constraints enforce                    forcement points such as phase gating, scope restriction, proposal
small steps (e.g., one failing test at a time, minimal passing code),               validation, and bounded repair control. Figure 1 illustrates repre-
and Feedback-quality constraints ensure feedback remains fast                       sentative manifesto entries and their translation into enforceable
and trustworthy (e.g., tests must be fast and deterministic; assertions             governance elements.
must be meaningful; refactoring must preserve behavior). Table 1
lists these categories and the typical human-era failure mode that
causes each category to degrade under delivery pressure. (3)


 Category           Canonical principle form       Why humans dropped it un-
                                                   der pressure [2, 19]
 Order              Test-first                and  Front-loads thinking and "just
                    Red→Green→Refactor             code it" feels faster
 Granularity        Minimal failing test, minimal  Batching reduces perceived
                    passing code, and one failing  overhead but increases hid-
                    test at a time                 den risk
 Feedback quality   FAST, independent, repeat-     Slow or flaky suites and weak
                    able, self-validating, and     tests become socially toler-
                    timely tests with meaningful   ated to ship
                    assertions
 Design hygiene     Remove duplication and refac- Benefits are delayed and invis-
                    tor continuously while green ible, so refactor becomes op-      Figure 1: Illustrative manifesto entries and their governance
                                                  tional                            structure.
Table 1: Principle categories and their typical human-era
failure modes.
                                                                                    3.2     Proposed Approach and System Description
                                                                                    We operationalize classical TDD as a governed, multi-phase or-
                                                                                    chestration framework in which TDD principles are encoded as
   Historically "right" but economically fragile. The extracted set
                                                                                    structured constraints distributed across planner, generation, repair,
intentionally over-represents principles that are difficult for humans
                                                                                    and validation stages. Rather than relying on ad hoc prompting or
to sustain. For example, "run tests constantly" and "refactor as
                                                                                    post hoc verification, the system enforces phase ordering, bounded
a required step" are widely accepted, but frequently abandoned
                                                                                    autonomy, and deterministic validation at each step of the develop-
because the short-term cost is salient while the benefit is delayed.
                                                                                    ment loop. Large language models act as proposal generators, while
Similarly, "tests must be self-validating" is accepted in principle, yet
                                                                                    an execution engine maintains authority over state mutation and
humans commonly ship weak tests (or non-assertive tests) because
                                                                                    workflow progression. Unlike TDFlow-style autonomous execu-
they are faster to write. In other words, the extraction targets the
                                                                                    tion, the orchestration engine retains sole authority over workspace
known failure points of human-era TDD: principles that require
                                                                                    mutation.
repeated, immediate investment to preserve long-term optionality.
                                                                                       Phase-Oriented workflow. The system follows a structured ex-
   Outputs and representation. The outcome of this step is a cu-
                                                                                    ecution cycle aligned with the Red-Green-Refactor discipline. A
rated list of principles representing the bounded canonical TDD
                                                                                    specification is first decomposed into ordered steps by a planner
corpus used in this study. Each principle is represented as a struc-
                                                                                    component. These steps explicitly encode expected test outcomes,
tured record containing: a label, a canonical quote (when available),
                                                                                    ensuring that failing tests (red) lead to implementation (Green).
a human-era intent statement, and a bibliographic pointer. This
                                                                                    Code generation is therefore not permitted until a failing test state
representation is designed as the input to the next step: trans-
                                                                                    is established.
lating human-era discipline into AI-native governance rules that
                                                                                       After each proposal, the system executes a review and validation
autonomous or semi-autonomous systems can ingest and enforce.
                                                                                    stage before applying any changes to the project workspace. Only
Figure 1 illustrates three enforceable governance principles: re-
                                                                                    after successful validation are changes applied and tests executed. If
quiring pre-change failing tests (RED) for behavior modifications,
                                                                                    tests fail, the system enters a repair loop; if tests pass, the workflow
treating refactoring as a gated phase with full-suite regression and
                                                                                    proceeds toward completion and optional refactoring (Figure 2).
duplication controls, and operationalizing FIRST test quality via
quantitative checks for speed, determinism, self-validation, and                    1 https://github.com/shahbazsiddeeq/TDD-manifesto/blob/main/tdd_principles_
timeliness.                                                                         manifesto.json
EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom                                                                            Hasanli et al.


    Governance-Centric Architecture. Beyond sequential phase or-                  Prompt Distribution Across Agent Roles. TDD discipline is not
dering, the system is designed around a governance-centric archi-              encoded in a single instruction. Instead, it emerges from coordi-
tecture that separates generative autonomy from state authority.               nated constraints distributed across role-specific prompts. System
Language models never directly write to the file system. Instead,              prompt establishes governance invariants, structured output re-
they return structured patch proposals that are subject to validation          quirements, and phase purity. Planner prompt decomposes the
gates prior to application.                                                    specification into ordered steps with expected test outcomes (e.g.,
    The system incorporates a structured TDD manifesto that en-                FAIL then PASS), thereby encoding test-first progression and con-
codes extracted principles as declarative constraints. These con-              straining phase transitions. Test Generation prompt enforces
straints inform prompt construction, validation rules, and phase               RED-phase constraints, restricting output to the test files and re-
enforcement logic, serving as the conceptual contract between TDD              quiring meaningful assertions aligned with the specification. Imple-
theory and runtime orchestration.                                              mentation prompt restricts synthesis to minimal changes neces-
    Before any mutations occur, outputs undergo:                               sary to satisfy failing tests and forbids unrelated feature additions.
    (1) Structural validation (schema and content checks),                     Failure Repair prompt injects structured failure context (e.g.,
    (2) Policy enforcement (e.g., disallowed paths, directory restric-         failure category and test output) and enforces minimal, localized
        tions),                                                                corrections. Review prompt acts as a quality gate, prohibiting pro-
    (3) Phase consistency checks (ensuring outputs match the ex-               duction edits during test review and preventing over-specification
        pected phase),                                                         or invented requirements.
    (4) Optional human or rule-based approval (in planner mode).                  Through this distribution, classical TDD properties - test-first
    Only after passing these gates are changes applied atomically. All         execution, minimal implementation, and behavior preservation -
file mutations are performed exclusively by the orchestration engine           are enforced at both prompt and engine levels.
after validation, not by the model. This separation ensures that                  Bounded Repair and Loop Control.
generative variability does not directly translate into uncontrolled              Repair is governed by explicit termination policies to ensure con-
state changes (Figure 2).                                                      vergence. Each GREEN step allows at most 𝑁 = 3 repair attempts,
                                                                               chosen as a fixed retry budget to bound cost while preserving itera-
                                       Constraints
                                                                               tive recovery. A failure signature 𝑆 = {exception type, failing tests,
          1
                                                             TDD manifesto     normalized message} is computed per iteration. The loop termi-
              User
          requirements                                              Policy     nates early if:
                                                                                  (1) the same 𝑆 repeats in consecutive iterations,
                                                         Engine Governance        (2) a repair produces no effective code change (detected via
                                                            (authoritative)
        LLM Proposal Layer
                                                                                      patch comparison), or
         (non-authorative)
                                                     5       Checks               (3) proposals are semantically equivalent to prior attempts. Ex-
                                                     schema • policy • phase
              2
                                                       (+ optional human)
                                                                                      ecution also terminates when tests pass or the iteration cap
                  Planner
                                                                                      is reached.
                                                     6
                                                               Test Run        Execution also terminates when tests pass or the iteration cap is
              3
                   Tests
                  (RED)
                                                             (deterministic)   reached. These constraints ensure bounded, reproducible repair
                                   7                                           behavior.
                                  FAIL
              4                                          8
                                                                                  From Principles to Enforceable Mechanisms. The extracted TDD
              Code + Patch                                   Atomic Apply      principles are translated into concrete enforcement mechanisms
               (GREEN)                                       (engine-only)
                                                                               within the orchestration pipeline:
                                                                                   • Test-first development is enforced through planner-ordered
Figure 2: Governed AI-native TDD workflow with separation                            steps and engine-level FAIL gating, preventing code genera-
between non-authoritative proposal generation and authori-                           tion before failing tests exist.
tative execution.                                                                  • Minimal implementation is reinforced by prompt-level
                                                                                     scope restrictions and engine rejection of no-op or unrelated
    Figure 2 illustrates the end-to-end governed workflow. First, user               changes.
requirements and TDD manifesto constraints are provided as in-                     • Behavior preservation is guaranteed by post-apply test
puts. The proposal layer then generates an execution plan through                    execution gates and automatic rollback during refactoring if
the planner. During the RED phase, failing tests are proposed to                     tests fail.
establish the expected behavior. In the GREEN phase, implemen-                     • Controlled refactoring is permitted only after successful
tation proposals (code patches) are generated. All proposals are                     test passes and is subject to validation that forbids feature
routed through the engine governance layer, where schema valida-                     modification or test edits.
tion, policy enforcement, and phase-consistency checks are applied.               Importantly, these guarantees arise from the interaction between
Approved proposals are executed through a deterministic test run.              prompt constraints and deterministic validation rules. TDD is there-
If tests fail, control returns to the proposal layer for bounded repair        fore not advisory but operationalized as a distributed governance
iterations; otherwise, validated changes are atomically committed              protocol.
to the workspace.                                                                 AI-Native TDD as Process Encoding
TDD Governance for Multi-Agent Code Generation via Prompt Engineering                               EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom


   Unlike approaches that treat tests as auxiliary inputs or eval-               [2] Adnan Causevic, Daniel Sundmark, and Sasikumar Punnekkat. 2011. Factors
uation metrics, this framework encodes TDD as a process-level                        Limiting Industrial Adoption of Test Driven Development: A Systematic Review.
                                                                                     In 2011 Fourth IEEE International Conference on Software Testing, Verification and
constraint architecture. Phase ordering, validation gating, bounded                  Validation. 337–346.
repair, and state authority are integrated into the generative loop              [3] Yi Cui. 2025. Tests as Prompt: A Test-Driven-Development Benchmark for LLM
                                                                                     Code Generation. arXiv:2505.09027
itself. As a result, the development discipline shapes the trajectory            [4] Yihong Dong, Xue Jiang, Jiaru Qian, Tian Wang, Kechi Zhang, Zhi Jin, and Ge Li.
of model generation rather than being applied after the fact.                        2025. A Survey on Code Generation with LLM-based Agents. arXiv:2508.00083
   This design positions prompt engineering not merely as task                   [5] Sarah Fakhoury, Aaditya Naik, Georgios Sakkas, Saikat Chakraborty, Madan
                                                                                     Musuvathi, and Shuvendu Lahiri. 2024. Exploring the Effectiveness of LLM based
phrasing but as a mechanism for encoding software engineering                        Test-driven Interactive Code Generation: User Study and Empirical Evaluation.
process invariants within AI-assisted development workflows.                         In Proceedings of the 2024 IEEE/ACM 46th International Conference on Software
                                                                                     Engineering: Companion Proceedings (Lisbon, Portugal) (ICSE-Companion ’24).
                                                                                     Association for Computing Machinery, New York, NY, USA, 390–391.
4    Discussion and Future Work                                                  [6] Martin Fowler. 2018. Refactoring: improving the design of existing code. Addison-
The primary benefit of the AI-native TDD framework is the ex-                        Wesley Professional.
                                                                                 [7] Yuyao Ge, Lingrui Mei, Zenghao Duan, Tianhao Li, Yujia Zheng, Yiwei Wang,
plicit encoding of development discipline within the generative                      Lexin Wang, Jiayu Yao, Tianyu Liu, Yujun Cai, Baolong Bi, Fangda Guo, Jiafeng
workflow. By separating proposal generation from state mutation                      Guo, Shenghua Liu, and Xueqi Cheng. 2025. A Survey of Vibe Coding with Large
                                                                                     Language Models. arXiv:2510.12399
and enforcing phase-ordered execution, the system reduces uncon-                 [8] Kevin Han, Siddharth Maddikayala, Tim Knappe, Om Patel, Austen Liao, and
trolled iteration and mitigates instability common in LLM-driven                     Amir Barati Farimani. 2026. TDFlow: Agentic Workflows for Test Driven Devel-
development. TDD principles are distributed across planner, gener-                   opment. arXiv:2510.23761
                                                                                 [9] E. G. Santana Jr, Gabriel Benjamin, Melissa Araujo, Harrison Santos, David
ation, repair, and validation stages, enabling process-level gover-                  Freitas, Eduardo Almeida, Paulo Anselmo da M. S. Neto, Jiawei Li, Jina Chun,
nance beyond prompt phrasing alone. Bounded repair loops and                         and Iftekhar Ahmed. 2025. Which Prompting Technique Should I Use? An
deterministic validation gates improve reproducibility, while the                    Empirical Investigation of Prompting Techniques for Software Engineering Tasks.
                                                                                     arXiv:2506.05614
structured TDD manifesto operationalizes test-first development as              [10] Eugene Klishevich, Yegor Denisov-Blanch, Simon Obstbaum, Igor Ciobanu, and
a runtime constraint, preserving behavioral safety during iterative                  Michal Kosinski. 2025. Measuring Determinism in Large Language Models for
                                                                                     Software Code Review. arXiv:2502.20747
synthesis.                                                                      [11] Jia Li, Ge Li, Yongmin Li, and Zhi Jin. 2025. Structured chain-of-thought prompt-
   The current implementation has several limitations. Manifesto-                    ing for code generation. ACM Transactions on Software Engineering and Method-
derived constraints are primarily enforced at the prompt level, with                 ology 34, 2 (2025), 1–23.
                                                                                [12] Robert C Martin. 2009. Clean code: a handbook of agile software craftsmanship.
only partial runtime verification, leaving full semantic compliance                  Pearson Education.
as future work. While the bounded autonomy model stabilizes exe-                [13] Robert C Martin. 2011. The clean coder: a code of conduct for professional program-
cution, it may limit exploration in complex refactoring scenarios.                   mers. Pearson Education.
                                                                                [14] Noble Saji Mathews and Meiyappan Nagappan. 2024. Test-Driven Development
Empirical validation remains preliminary, and broader cross-model                    and LLM-based Code Generation. In Proceedings of the 39th IEEE/ACM Interna-
and repository-scale evaluations are needed to assess the robust-                    tional Conference on Automated Software Engineering (Sacramento, CA, USA)
                                                                                     (ASE ’24). Association for Computing Machinery, New York, NY, USA, 1583–1594.
ness. Additionally, scaling to large, multi-module repositories with            [15] Shuyin Ouyang, Jie M. Zhang, Mark Harman, and Meng Wang. 2025. An Empirical
complex dependencies will require more advanced planning and                         Study of the Non-Determinism of ChatGPT in Code Generation. ACM Trans.
invariant enforcement mechanisms.                                                    Softw. Eng. Methodol. 34, 2, Article 42 (Jan. 2025), 28 pages.
                                                                                [16] Sanyogita Piya and Allison Sullivan. 2024. LLM4TDD: Best Practices for Test
   Initial experimentation suggests that explicit phase separation                   Driven Development Using Large Language Models. In Proceedings of the 1st
and validation gating reduce unstable retry cycles compared to                       International Workshop on Large Language Models for Code (Lisbon, Portugal)
baseline prompting. Enforcing test-first ordering and minimal im-                    (LLM4Code ’24). Association for Computing Machinery, New York, NY, USA,
                                                                                     14–21.
plementation appears to limit speculative code generation and un-               [17] Ranjan Sapkota, Konstantinos I. Roumeliotis, and Manoj Karkee. 2025. Vibe
necessary feature expansion. However, manifesto injection must be                    Coding vs. Agentic Coding: Fundamentals and Practical Implications of Agentic
                                                                                     AI. arXiv:2505.19443
carefully balanced against token constraints, highlighting a trade-             [18] Jiho Shin, Clark Tang, Tahmineh Mohati, Maleknaz Nayebi, Song Wang, and Hadi
off between governance strength and prompt compactness.                              Hemmati. 2025. Prompt Engineering or Fine-Tuning: An Empirical Assessment
   Future work will evaluate AI-native TDD in repository-scale in-                   of LLMs for Code. arXiv:2310.10508
                                                                                [19] Daniel Staegemann, Matthias Volk, Maneendra Perera, Christian Haertel,
dustrial settings, including CI/CD integration, to assess stability, de-             Matthias Pohl, Christian Daase, and Klaus Turowski. 2022. A Literature Review on
fect rates, and reproducibility. We also plan to explore configurable                the Challenges of Applying Test-Driven Development in Software Engineering.
governance levels that allow teams to calibrate strictness based                     Complex Systems Informatics and Modeling Quarterly (07 2022), 18–28.
                                                                                [20] Jiessie Tie, Bingsheng Yao, Tianshi Li, Syed Ishtiaque Ahmed, Dakuo Wang, and
on project complexity. The deterministic validation and bounded                      Shurui Zhou. 2024. LLMs are Imperfect, Then What? An Empirical Study on
autonomy model may further support auditable AI-assisted devel-                      LLM Failures in Software Engineering. arXiv:2411.09916
                                                                                [21] Bhanu Prakash Vangala, Ali Adibifar, Ashish Gehani, and Tanu Malik. 2026. AI-
opment, particularly in regulated domains.                                           Generated Code Is Not Reproducible (Yet): An Empirical Study of Dependency
                                                                                     Gaps in LLM-Based Coding Agents. arXiv:2512.22387
Acknowledgments                                                                 [22] Tianxin Wei, Ting-Wei Li, Zhining Liu, Xuying Ning, Ze Yang, Jiaru Zou, Zhichen
                                                                                     Zeng, Ruizhong Qiu, Xiao Lin, Dongqi Fu, Zihao Li, Mengting Ai, Duo Zhou,
This work has been supported by Business Finland (projects GE-                       Wenxuan Bao, Yunzhe Li, Gaotang Li, Cheng Qian, Yu Wang, Xiangru Tang, Yin
NIUS (2545/31/2024) and ANSE (1822/31/2025)). We would also like                     Xiao, Liri Fang, Hui Liu, Xianfeng Tang, Yuji Zhang, Chi Wang, Jiaxuan You,
                                                                                     Heng Ji, Hanghang Tong, and Jingrui He. 2026. Agentic Reasoning for Large
to acknowledge the use of Google’s Nano Banana Pro in generating                     Language Models. arXiv:2601.12538
the visualization for Figure 1.                                                 [23] Ziyao Zhang, Chong Wang, Yanlin Wang, Ensheng Shi, Yuchi Ma, Wanjun Zhong,
                                                                                     Jiachi Chen, Mingzhi Mao, and Zibin Zheng. 2025. Llm hallucinations in practical
                                                                                     code generation: Phenomena, mechanism, and mitigation. Proceedings of the
References                                                                           ACM on Software Engineering 2, ISSTA (2025), 481–503.
 [1] Kent Beck. 2002. Test Driven Development: By Example. Pearson Education,
     Boston.

