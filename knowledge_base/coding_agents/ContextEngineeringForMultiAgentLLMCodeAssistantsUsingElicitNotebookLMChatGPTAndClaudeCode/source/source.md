# Context Engineering for Multi-Agent LLM Code Assistants Using Elicit, NotebookLM, ChatGPT, and Claude Code
Source: https://arxiv.org/abs/2508.08322v1
Kind: pdf
Fetched: 2026-09-23T19:51:32.599073+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                         Context Engineering for Multi-Agent LLM Code Assistants Using
                                                Elicit, NotebookLM, ChatGPT, and Claude Code
                                                                                 Muhammad Haseeb
                                                                               muhammadhaseeb@vt.edu

                                                                                      August 2025




arXiv:2508.08322v1 [cs.SE] 9 Aug 2025
                                                                                         Abstract
                                                  Large Language Models (LLMs) have shown promise in automating code generation and
                                              software engineering tasks, yet they often struggle with complex, multi-file projects due to
                                              context limitations and knowledge gaps. We propose a novel context engineering workflow
                                              that combines multiple AI components—an Intent Translator (GPT-5) for clarifying user
                                              requirements, an Elicit-powered semantic literature retrieval for injecting domain knowledge,
                                              NotebookLM-based document synthesis for contextual understanding, and a Claude Code
                                              multi-agent system for code generation and validation. Our integrated approach leverages in-
                                              tent clarification, retrieval-augmented generation, and specialized sub-agents orchestrated via
                                              Claude’s agent framework. We demonstrate that this method significantly improves the ac-
                                              curacy and reliability of code assistants in real-world repositories, yielding higher single-shot
                                              success rates and better adherence to project context than baseline single-agent approaches.
                                              Qualitative results on a large Next.js codebase show the multi-agent system effectively plans,
                                              edits, and tests complex features with minimal human intervention. We compare our system
                                              with recent frameworks like CodePlan, MASAI, and HyperAgent, highlighting how targeted
                                              context injection and agent role decomposition lead to state-of-the-art performance. Finally, we
                                              discuss the implications for deploying LLM-based coding assistants in production, along with
                                              lessons learned on context management and future research directions.


                                        1    Introduction
                                        Recent advances in large language models (LLMs) have led to powerful code assistant tools capable
                                        of generating code, fixing bugs, and even synthesizing simple programs from natural language
                                        descriptions. Models like OpenAI’s Codex and Anthropic’s Claude have demonstrated that LLMs
                                        can understand and generate human-like code snippets with impressive accuracy. However, as
                                        software engineering tasks grow in complexity, there is an emerging need for more sophisticated
                                        solutions that can handle the intricacies of real-world software development. Repository-level tasks
                                        often involve coordinating changes across multiple files, understanding existing code architecture,
                                        and incorporating domain-specific knowledge that may lie outside the model’s training data. Purely
                                        prompt-driven single-agent solutions struggle with these challenges due to limited context windows
                                        and the risk of hallucinations when confronted with unfamiliar APIs or frameworks.
                                            A key limitation of default code assistants is their reliance on a fixed static context. For example,
                                        Anthropic’s Claude Code allows a repository to include a CLAUDE.md file with project guidelines
                                        and context, but a single prompt cannot capture all relevant details for every possible task. In our
                                        early experiments, a default Claude Code agent with a basic CLAUDE.md prompt often produced
                                        incomplete or incorrect solutions for non-trivial features. It might miss necessary edits in distant


                                                                                             1
files or misuse an unfamiliar library, reflecting insufficient context comprehension. This aligns with
observations by frameworks like CodePlan, which treat repository-level coding as a multi-step plan
rather than a single-step generation [3, 2].
     To address these issues, recent work has explored multi-agent architectures and retrieval aug-
mentation for coding tasks. Systems like MASAI (Modular Architecture for Software Engineering
AI) instantiate specialized sub-agents for different subtasks (planning, localization, code generation,
testing), achieving significantly higher success on repository-level challenges (28.3% resolution on
the SWE-Bench Lite benchmark) than single-agent baselines [2]. Likewise, HyperAgent employs a
team of agents (Planner, Navigator, Code Editor, Executor) to mimic a human developer workflow,
improving issue resolution rates on complex repositories [1]. Another thread of research focuses on
augmenting LLMs with retrieved context: for example, AllianceCoder generates natural-language
descriptions of APIs in a codebase and retrieves relevant API information to guide code generation,
yielding up to 20% higher pass@1 accuracy [5]. These approaches illustrate that providing the right
information and breaking down tasks are crucial to scaling LLMs to complex coding problems.
     Building on these insights, we propose a comprehensive context engineering approach for
LLM-based code assistants. By context engineering, we mean systematically constructing and
supplying all relevant information needed for a coding task—ranging from clarified intent and high-
level plans to external knowledge and repository-specific details—and doing so via a coordinated
multi-agent process. Our contributions are summarized as follows:
   • We design a novel workflow that integrates four components: (1) an Intent Translator using
     GPT-5 to rewrite or elaborate the user request into a structured task specification; (2) an
     Elicit-based semantic paper/document retrieval mechanism to fetch relevant documentation
     or research (e.g., algorithms, API usage guidelines) related to the task; (3) a NotebookLM-
     powered document synthesis module that creates a concise summary or table-of-contents of
     the retrieved materials and can answer follow-up questions for detailed understanding; and
     (4) a Claude Code multi-agent system that orchestrates specialized sub-agents (planner,
     coder, tester, reviewer) along with a vector database for code context, to carry out the coding
     task with iterative refinement.
   • We implement this context-engineered multi-agent assistant on a real-world codebase (the
     RainMakerz Next.js Web application, ∼ 180K lines of code). In qualitative evaluations,
     our system can implement complex features and bug fixes in a single generation cycle. For
     example, it successfully added a new interactive visualization module spanning front-end and
     back-end changes in one try, whereas a baseline single-agent Claude often omitted needed
     steps. We report case studies showing improved code correctness and context adherence.
   • We compare our approach to prior state-of-the-art coding agents. We show that the explicit
     context layering and role decomposition in our system address several failure modes observed
     in earlier methods. The multi-agent Claude pipeline exhibits higher reliability in producing
     working code on the first attempt, matching or exceeding the performance reported for frame-
     works like CodePlan [3] and DARS [4] on similar tasks. We also discuss how our engineering
     decisions (such as using retrieved API descriptions or enforcing agent-specific contexts) are
     informed by these prior works.
   • Finally, we outline a pathway for deploying such an AI assistant in production environments.
     We describe integration with continuous integration (CI) pipelines (e.g., using Claude Code
     in GitHub Actions for automated code reviews) and discuss scalability, cost, and safety con-
     siderations. Our findings suggest that context-engineered multi-agent assistants can be made
     production-ready for team use, given appropriate safeguards and iterative tuning.

                                                  2
    In the remainder of this paper, we first review related work in multi-agent LLM systems and
retrieval-augmented code generation (Section 2). We then describe the design of our context engi-
neering workflow and the architecture of the system in detail (Sections 3 and 4). Section 5 presents
experimental results and case studies on applying the system to a real codebase. We provide anal-
ysis and discussion of the key improvements and remaining challenges in Section 6, and conclude
with future directions in Section 7.


2    Related Work
LLM-based Coding Agents. A number of recent systems have extended LLMs to operate as
autonomous coding agents tackling complex software engineering tasks. Notably, HyperAgent
[1] introduced a centralized multi-agent framework with four specialist agents (Planner, Navigator,
Code Editor, Executor) working in concert. HyperAgent demonstrated state-of-the-art results on
tasks like GitHub issue resolution, achieving a 31.4% success rate on the SWE-Bench Verified bench-
mark – outperforming earlier approaches that focused on single-task agents. Similarly, MASAI
(Arora et al., 2024) proposes a modular architecture of LLM-powered sub-agents, each responsible
for a distinct phase such as test generation, issue reproduction, code editing, or solution ranking.
By dividing the problem and allowing sub-agents to gather information from different parts of the
repository, MASAI attained the highest performance (28.33% resolution rate) on SWE-Bench Lite
at the time of its publication [2]. Our work draws inspiration from these architectures, adopting a
hub-and-spoke orchestration pattern where a central orchestrator (Claude) delegates to specialized
roles (Section 4).

Planning and Iterative Refinement. Another line of work treats complex coding tasks as a
planning problem with iterative feedback. CodePlan [3], while not originally designed for multi-
agent settings, introduced the idea of generating a high-level pseudocode plan that the LLM then
follows step-by-step. This approach improved multi-step reasoning by encouraging the model to
outline dependencies and subgoals before committing to final code. We incorporate a similar
principle via our Intent Translator and Planner agent, which decompose the problem and ensure
that subsequent code generation is guided by an explicit plan. On the execution side, DARS
(Aggarwal et al., 2025) augments an LLM agent with dynamic action re-sampling: at certain
decision points, the agent can branch and try an alternative strategy, using feedback (e.g. test
results) to choose the best outcome [4]. DARS achieved a 47% pass@1 on SWE-Bench Lite with
this method, indicating the value of exploring multiple solution trajectories. While our current
system does not implement full branching, it does incorporate iteration and self-correction (e.g. re-
running tests and adjusting code) within the multi-agent loop, and such adaptive strategies could
further enhance our pipeline in the future.

Retrieval-Augmented Code Generation. Integrating external knowledge via retrieval has
proven crucial for code generation on large codebases. Traditional code search techniques (e.g.
keyword or AST-based searches) can identify relevant code context for a given task, but recent work
has explored semantic retrieval to better utilize unstructured information. AllianceCoder (Gu et
al., 2025) is a representative example: it empirically studied what to retrieve for repository-level
code tasks, concluding that providing in-context code and API documentation yields significant
gains, whereas blindly retrieving similar code examples can sometimes hurt performance [5]. Al-
lianceCoder uses chain-of-thought prompting to break a query into sub-tasks and retrieve pertinent
API descriptions for each. In our system, we similarly retrieve two kinds of context: (1) external


                                                 3
                                  Intent Translator                Semantic Retrieval
                  User Request
                                      (GPT-5)                          (Elicit)




                                 Knowledge Synthesis
                                   (NotebookLM)                     Claude Orchestrator




                                                       backend                             frontend




                                                        devops                             reviewer



                                                                          SubAgents




                                                       VectorDB                           MCP Tools




                                                      Repository                           CI/CD



                                                                            Tools




Figure 1: End-to-end pipeline: intent translation, retrieval and synthesis, orchestrated multi-agent
coding with tools and memory.


knowledge (papers, guides) related to the task via Elicit, and (2) internal codebase knowledge via
a vector database and search tools. Retrieval-Augmented Generation (RAG) approaches have also
been explored in agentic coding assistants; for instance, researchers have proposed agents that
augment prompts with relevant code snippets from the repository and commit history, showing im-
proved bug-fixing accuracy. Our approach extends this idea by not only retrieving static snippets
but also engaging with documents through NotebookLM to extract distilled insights.

Agent Tooling and Debugging. The complexity of multi-agent LLM systems has spurred the
development of tooling to support their operation. Several frameworks (e.g. LangChain Agents,
HuggingGPT) enable LLMs to invoke tools and other models, but tailoring these to software
engineering tasks remains an active area of research. Claude Code provides a built-in mechanism
for defining custom tools (via Model Completion Protocol servers) and multi-agent configurations,
which we leverage for tasks like running tests or analyzing code complexity. Beyond execution,
analyzing the behavior of autonomous coding agents is itself non-trivial. The SeaView tool [6]
was recently proposed to visualize and inspect the trajectories of software-engineering agents. It
highlights the need for better debugging interfaces when agents perform long sequences of actions
(often tens of thousands of tokens of interaction with code and environment). In our work, we
mainly rely on logs and intermediate results for analysis, but incorporating a visualization like
SeaView to trace agent decision-making could greatly aid future development and evaluation of
context-engineered assistants.


3    Methodology: Context Engineering Workflow
Intent Translation with GPT-5. The process begins when a user submits a natural language
query describing a desired code change or feature. This query may be ambiguous or underspecified.

                                                           4
                                            Chroma

          Source    AST                                                                    Agent
                              Embedder                         Query   Rerank   Snippets
           Code    Chunker                                                                  Gen
                                              Zilliz



                                          Vector Index
                                         Unified adapter




Figure 2: Retrieval pipeline: code-aware chunking and dual-index backend with a unified adapter.


To ensure the system accurately grasps the requirements, we employ a high-end LLM (GPT-5,
in our case) to act as an Intent Translator. This agent reformulates the query into a structured
specification that can guide subsequent steps. For example, a user request like ”Add a calendar
view to the scheduling page” might be translated into a more explicit list of tasks (e.g., ”update
UI component X to include a calendar widget; fetch data Y from the backend API; adjust styling
and add unit tests”). The translator prompt is engineered to elicit a step-by-step breakdown,
clarifying any implicit requirements (such as which library to use for the calendar, or what data
needs to be displayed). The output is a well-defined task specification or outline. By front-loading
this clarification step, we reduce the burden on the coding agents to interpret fuzzy instructions,
similar in spirit to the planning step in CodePlan but performed by a distinct, specialized model.

Semantic Literature Retrieval with Elicit. Next, the refined task specification is used to
query external knowledge sources for any domain-specific information that might be relevant. We
integrate Elicit, an LLM-driven research assistant, to perform semantic search over academic papers,
documentation, and Q&A resources. The goal is to retrieve materials such as algorithm descriptions,
API usage examples, or best-practice guidelines that pertain to the task. In our running example,
Elicit might find documentation on a React calendar library or a paper on scheduling UI design.
Unlike keyword search, Elicit’s semantic search helps find conceptually relevant documents even if
they do not share exact keywords with the query. We automate this step by feeding Elicit the key
terms from the task spec (e.g., ”calendar widget React TypeScript library”) and asking for papers
or articles that answer or relate to the query. The top-k results (we used k = 3-5) are fetched as
PDFs or text.

Knowledge Synthesis with NotebookLM. Simply retrieving documents is not enough—the
system must distill them into useful context for coding. We utilize Google’s NotebookLM as a
document analysis agent. All retrieved documents are provided to NotebookLM, which we prompt
to produce a concise table-of-contents (TOC) summary of each and to answer specific questions.
In practice, we instruct NotebookLM to outline the key points of each paper or guide, focusing
on insights that could inform implementation (e.g., ”What are the steps to integrate the chosen
calendar library?”, ”What pitfalls or edge cases are noted?”). This yields a summarized knowledge
base in natural language. We found that structuring the external knowledge as a list of key bullet
points or Q&A pairs makes it much easier to integrate into the code-writing prompt than dumping
long paragraphs. NotebookLM’s ability to handle multiple documents and generate a synthesized
overview was crucial in maintaining a high signal-to-noise ratio in the context.

Repository Context Retrieval. In parallel with external knowledge gathering, the system
prepares relevant context from the codebase itself. Our target repository (RainMakerz) is large,
so providing the entire codebase to the LLM is infeasible. Instead, we built a semantic code
search index using a vector database (we experimented with both ChromaDB and Zilliz for this

                                                           5
                        requirements
      Developer/PO                     Claude Orchestrator                       backend   frontend     devops   reviewer




                                                                                                SubAgents




                     Liveblocks        Supabase       API Routes      Frontend




                           CI/CD          Vector DB       MCP Tools




                                         Runtime & Tooling


Figure 3: System architecture: orchestrator delegates to sub-agents; agents act via tools and
runtime stack.

purpose). We embed code files and fragments into high-dimensional vectors using a code-specialized
embedding model (OpenAI’s code-embedding model). To preserve code structure, we chunk files
by function or class definitions using an AST parser (tree-sitter), as recommended by prior work
on code retrieval. At runtime, given the refined task spec, we query this index for the top relevant
code fragments (e.g., files whose embeddings are closest to the query embedding). Additionally,
Claude’s agents have access to traditional tools like grep and file path search for exact matches of
identifiers. The combination of semantic and lexical search ensures that if the task touches, say,
the SchedulerPage component or a CalendarService class, the pertinent parts of those files will be
retrieved. These code context snippets (with file names and relevant lines) are then available to
the coding agents as supplementary context.


4     System Architecture and Agent Orchestration
4.1    Claude Multi-Agent Design
Our coding workflow is implemented using Claude Code’s multi-agent capabilities. At a high
level, we adopt a centralized orchestrator-worker paradigm (often called a hub-and-spoke pattern):
a primary Claude instance (the ”Manager”) coordinates several specialist sub-agents that each
have their own context and role. Claude’s framework allows defining these agents via simple
YAML/Markdown files. For example, Listing 1 shows a snippet of the configuration for a backend-
architect agent we created. This agent is designated as a senior back-end engineer, with a description
of its expertise and a set of tools it can use (here, file read/write, edit, and bash shell access).
We created similar profiles for a frontend-specialist, devops-engineer, code-reviewer, etc., reflecting
the roles often found in a development team. These definitions reside in the repository under
a .claude/agents/ directory; Claude Code automatically loads them so that the orchestrator can
invoke any agent by name when needed.

                Listing 1: Project-specific Claude Sub-Agent configuration (excerpt).

name : backend−a r c h i t e c t
d e s c r i p t i o n : Design RESTful APIs , m i c r o s e r v i c e b o u n d a r i e s ,

                                                                      6
and d a t a b a s e schemas
model : s o n n e t
t o o l s : Read , Write , Edit , Bash

You a r e a s e n i o r backend a r c h i t e c t s p e c i a l i z i n g i n s c a l a b l e
system d e s i g n
    Each subagent operates with an isolated context window. This means that when the orches-
trator invokes (for example) the backend-architect agent to handle a task, that agent receives only
the information relevant to its task (plus any persistent project context) and does not see the en-
tire dialogue history or unrelated data. This design is intentional: it prevents cross-contamination
between different phases of the workflow and keeps each agent focused. Common background in-
formation that all agents should know (coding conventions, project architecture notes, etc.) is
provided via a persistent context file (CLAUDE.md), which is preloaded into each agent’s context.
The CLAUDE.md for RainMakerz included high-level architectural overviews (such as the system
design shown in Figure 3), coding style guidelines, and a summary of known bugs and previous so-
lutions. Thus, each agent starts with a shared base of project knowledge, and then the orchestrator
augments it with specific instructions and data for the current step.

                                    L1: Task Specification (Intent Translator)



                                 L2: External Knowledge (Elicit & NotebookLM)



                                L3: Project Memory (CLAUDE.md, internal docs)



                                  L4: Retrieved Code Context (Vector DB, grep)



                                 L5: Execution Artifacts (diffs, logs, test results)




                                               Agent Prompt/Input


            Figure 4: Context layering: structured inputs flow into each agent’s prompt.




                                                         7
4.2   Agent Orchestration Flow


                  Plan          Retrieve Context          Delegate           Edit/Implement



                                                             failures
                         Done          Integrate/PR           Review              Run Tests

                                                                        changes




      Figure 5: Claude orchestrator state machine with feedback from tests and code review.

After the intent translation and context retrieval stages (Section 3), the Claude orchestrator enters a
loop of delegating tasks to sub-agents and integrating their outputs. The process can be summarized
as follows:

  1. Planning: The orchestrator first invokes the Planner agent (in our case, we often used the
     backend-architect profile as planner if the task was backend-heavy, or a specialized Planner
     agent) with the structured task specification and the knowledge summary. The Planner agent
     is prompted to produce a concrete implementation plan: a sequence of steps possibly mapped
     to specific files or components. It may output something like: ”1. Update CalendarAPI to
     provide events data; 2. Create CalendarWidget component in frontend; 3. Integrate widget
     into SchedulePage; 4. Write unit tests for new component”. The orchestrator examines this
     plan.

  2. Task Delegation: For each step in the plan, the orchestrator selects an appropriate agent
     and provides it the necessary context. Frontend-related steps are assigned to the frontend-
     specialist agent, server-side tasks to the backend-architect, and so on. Each agent is given: (a)
     the relevant excerpt of the plan (or the whole plan for context), (b) any code snippets retrieved
     that pertain to that step (from the vector DB search), and (c) its specific instructions. The
     agent then executes its task. Most often this involves using the Edit tool to open a file and
     modify or create code. For example, the frontend agent will open SchedulePage.jsx and insert
     the required code for the calendar widget.

  3. Iterative Coding and Validation: As agents make changes, we leverage Claude’s tool
     integration to run validations. After code for a step is written, the orchestrator (or sometimes
     the coding agent itself) can trigger test execution via a shell tool. We configured a test script
     to run the project’s test suite (using npm test for the Node.js environment). If tests or
     build steps fail, the error output is captured. The orchestrator then feeds this back into
     the responsible agent (or a dedicated debugging agent) to prompt a fix. This resembles the
     feedback loop in DARS [4], although in our implementation the branching is simple re-try
     rather than multiple simultaneous trajectories.

  4. Code Review and Refinement: Once all steps are completed and the test suite passes,
     the orchestrator invokes the code-reviewer agent to do a final pass. This agent reads through
     the diff of changes, checking for any style issues, potential bugs, or improvements (it uses a
     comprehensive checklist as shown in its prompt, covering things like type safety, performance,
     and security). The reviewer may suggest minor refactors or additional comments. If so, the

                                                      8
      suggestions are either applied automatically by an editing agent or presented for a human to
      confirm, depending on the confidence level.

    5. Output and Deployment: Finally, the system consolidates the changes. The orchestrator
       can output a summary of what was done along with the unified diff of code changes. In a
       production scenario, these changes could be automatically pushed to a branch or opened as a
       pull request for maintainers. We integrated our system with GitHub Actions for continuous
       integration: after Claude’s changes, the CI pipeline would run again to double-check tests
       and then could auto-merge the changes if all checks passed.

    Throughout this process, the structured layering of context is key (see Figure 4). At any
given time, an agent is working with a manageable slice of information: its role-specific prompt +
CLAUDE.md context + task-specific instructions + relevant code/knowledge snippets. This helps
maintain coherence even for very large tasks. We also observed that dividing the work among
agents reduced prompt tokens per agent, which mitigates context window issues. While our system
currently executes largely in a sequential manner (one sub-task at a time), it is straightforward
to parallelize independent sub-tasks by spawning agents concurrently – an approach suggested by
Anthropic’s experiments with multi-agent research systems [7]. In our case study tasks, parallelism
was less a priority because many steps had inherent dependencies (you can’t test before code is
written, etc.), but as AI agents become more adept at coordination, parallel execution could speed
up complex multi-component feature implementations.


5     Results
We evaluated our context-engineered assistant on several non-trivial development tasks in the
RainMakerz codebase. Table 1 provides a summary of outcomes on a sample of 5 tasks, comparing
our system to a baseline single-agent Claude (with only a CLAUDE.md context and direct user
prompts). In brief, our multi-agent approach succeeded in more tasks and required fewer iterations.
It often produced working solutions on the first attempt, whereas the baseline frequently needed
follow-up prompts or developer intervention to correct mistakes.

Case Study: Adding a New Feature. One test involved implementing a new ”CustomBlock”
in the RainMakerz pitch-deck module (a feature analogous to creating a new content block type in
a presentation). This task spanned front-end and back-end changes: creating a React component
for the block, adding corresponding options UI, updating TypeScript types, and registering the
block in a manager so it could be recognized and saved. Our system handled this end-to-end. The
Planner agent broke the task into 4 steps aligned with these requirements. The Frontend specialist
agent created the new component and its options popup, correctly following the patterns in existing
blocks (likely aided by the retrieved code context of similar blocks). The Backend agent updated
the data model and API endpoints where necessary (though in this case, most logic was front-end,
the agent double-checked if any server changes were needed for persistence). After code generation,
tests were executed; an initial failure occurred because the new block type was not added to a
serialization whitelist. The orchestrator immediately flagged this and tasked the Backend agent
with updating the serialization config. The second test run passed all unit and integration tests.
Finally, the Reviewer agent made a minor suggestion to refactor a hard-coded string into a constant,
which was applied. The entire feature was completed in one automated session. In contrast, when
we tried prompting a single Claude instance for the same task (with the project README and an
excerpt of a similar block as context), the assistant produced only the React component and forgot

                                                 9
to update the registry and type definitions, resulting in runtime errors. This highlights how our
system’s comprehensive approach (particularly, planning and retrieving scattered context) leads to
more thorough solutions.

Improved Context Adherence. We observed that the multi-agent system was far less prone
to hallucinating irrelevant code or inventing functions. Every function or class used by the gen-
erated code existed in the repository, which we attribute to the semantic code retrieval providing
real definitions to the agents. The baseline often guessed function or variable names (e.g. refer-
ring to a non-existent getEvents() API) which then caused failures. By having access to actual
API documentation from AllianceCoder-like retrieval and the code index, our agents stuck to the
truth of the codebase and documentation. For example, in a bug-fix task concerning authentica-
tion, the baseline assistant attempted to use a refreshToken() call that did not exist, whereas our
system consulted the project docs (via CLAUDE.md context) and correctly utilized the existing
renewSession() function.

Single-Shot Success Rate. Out of 5 tasks attempted (including feature additions and bug fixes
of varying complexity), our system achieved a successful outcome (defined by passing all tests and
meeting the acceptance criteria) on 4 tasks (80%) without any human corrections. The single-
agent baseline succeeded on only 2 tasks (40%), with the others requiring significant manual fixes
or additional prompting. While this is a small sample, it aligns with the qualitative improvements
noted in prior multi-agent studies (e.g., DARS and HyperAgent). Notably, even on the one task
where our approach did not fully succeed on the first try, it made partial progress and identified an
environmental issue (a misconfigured library) that a developer then easily fixed before re-running
the agent.

Efficiency and Cost. The richer context and multi-step reasoning come with a cost in LLM
usage. On average, our system exchanged around 30-40 messages across all agents for a single
task and consumed roughly 100k tokens in total (input + output). In contrast, the single-agent
approach might use 10k-20k tokens for a few prompt-response turns. In our evaluation, the multi-
agent method used about 3–5× more tokens on successful tasks. However, the baseline often
needed multiple attempts or lengthy debugging chats which, if counted, push its token count closer
to 50k for a complex task. Thus, the overhead of our approach is justified by getting the job done
largely autonomously. In a team setting, the value of saving developer time by achieving a correct
solution outweighs the additional compute cost. We also note that the modular design allowed us
to parallelize certain steps (though in our tests we ran sequentially); in future, this could further
improve wall-clock efficiency.


6    Discussion
Effect of Context Engineering. The case studies and results illustrate how each element of our
context engineering approach contributes to the overall performance. The intent translation step
(GPT-5) proved particularly useful in breaking down ambiguous requests. We found that when
the initial user query was directly fed to the code agents (baseline approach), the agents sometimes
focused on the wrong sub-problem or skipped a requirement. Having a clarified spec up front led to
more relevant searches and a more coherent plan. Similarly, the use of Elicit and NotebookLM to
inject external knowledge was validated in scenarios where the code change required understanding
concepts outside the codebase. For instance, in one bug fix, the Planner agent suggested using


                                                 10
a debounce mechanism for an API call; the knowledge summary included a brief explanation of
debouncing (from a blog post retrieved by Elicit), which guided the coding agent to implement
it correctly. Without that, the baseline agent attempted a simplistic fix that did not address the
root cause. These observations align with the premise of retrieval-augmented generation: providing
pertinent information at generation time greatly improves correctness.

Lessons on Multi-Agent Orchestration. We adopted multiple specialized agents to mirror
the human software development process (design, coding, testing, reviewing). This division of labor
generally worked well. One lesson was the importance of clearly delineating responsibilities to avoid
both gaps and overlaps. Early in development, we occasionally encountered situations where two
agents would both attempt to modify the same file (e.g., both frontend and backend agents editing
a shared config) or conversely, an agent assumed another would handle a step that got missed.
We mitigated this by refining the Planner’s prompt to explicitly assign sub-tasks to agent roles,
and by implementing a simple lock in the orchestrator to prevent concurrent edits to the same file.
Another insight is that the quality assurance step with a dedicated reviewer agent is invaluable.
The reviewer caught subtle issues (like potential null pointer access and minor security concerns)
that the coding agents overlooked while focusing on feature implementation. This reflects how
human code reviews add value even when code ”works”, and suggests that AI coding agents benefit
from a second pair of eyes as well.

Limitations. Despite its successes, our approach has limitations. First, the dependency on high-
quality external knowledge is a double-edged sword. In one experiment, Elicit returned an irrelevant
research paper due to an ambiguous query, and although NotebookLM summarized it faithfully,
that summary added noise to the context and confused the Planner agent. Robust retrieval ranking
and perhaps filtering by a human or a more advanced AI could be needed to ensure only useful
information is fed into the system. Second, the current orchestrator logic is relatively brittle; it
follows a predetermined sequence (plan → code → test → review). If an unexpected situation arises
(e.g., the plan is flawed or a new requirement emerges mid-way), the system is not yet equipped
to dynamically re-plan from scratch. This is an area where more adaptive, possibly reinforcement
learning-based, agent controllers (as explored in MARL settings) could help in the future. Third,
the computational cost, while acceptable for our use, might become problematic on very large
projects or if many agents run in parallel. Techniques like context compression, caching of vector
search results, or using smaller specialized models for certain agents could help reduce overhead.
    Another limitation is that we relied heavily on the presence of a comprehensive test suite. If
tests are sparse, the system might incorrectly judge a task as complete. Incorporating static analysis
tools (which we did to some extent via linters) and perhaps a ”spec verification” agent to reason
about requirements could partially address this gap. Moreover, error tracing can be challenging in a
multi-agent context; if a final result is wrong, it takes careful log analysis to pinpoint which agent’s
action or which piece of context led to the mistake. Tooling like SeaView [6] could be integrated to
visualize agent interactions and states, making debugging easier for developers overseeing the AI.

Generality and Future Work. While our implementation targeted a specific web application
(Next.js/TypeScript stack), the principles are generalizable. We envision applying the same context
engineering pattern to other domains (e.g., Java microservices, data science notebooks) by swapping
in relevant retrieval sources and agent specializations. The modular design allowed us to add an
additional agent (for example, we introduced a database-migrator agent to handle SQL schema
changes in one case) without altering the core orchestrator logic. This suggests that as long as


                                                  11
tasks can be clearly partitioned, the multi-agent approach can scale to very complex projects by
simply growing the team of AI agents.
    Looking forward, integrating learning mechanisms is an exciting avenue. Currently, our system
does not learn from its mistakes beyond a single session. One could imagine logging all agent in-
teractions and outcomes to fine-tune the agents or a meta-controller, akin to an RL (reinforcement
learning) paradigm. Another direction is improving the Planner agent with more sophisticated algo-
rithms (e.g., search-based planning or using graph representations of the code as in AllianceCoder’s
analysis). Finally, with the rapid progress in LLM capabilities, we anticipate that some components
(like the Intent Translator) could eventually be subsumed by more powerful code-focused models,
but the need to orchestrate multiple steps and use tools will persist. Our work provides a blueprint
for how such orchestration can be done in a robust, context-rich way.


7    Conclusion
We presented a novel context engineering methodology for multi-agent LLM-based code assistants,
combining intent clarification, semantic retrieval, knowledge synthesis, and coordinated sub-agents.
In a case study on a large codebase, this approach substantially outperformed a conventional single-
agent setup, delivering more accurate and complete code solutions with minimal human input. The
results underscore the importance of supplying LLMs with not just more information, but the right
information in the right form, as well as structuring the problem-solving process into manageable
subtasks. By drawing on ideas from recent research (planning, modular agents, RAG, etc.) and
unifying them in a practical workflow, we achieved a system that moves closer to autonomous
software development.
    There are many avenues for further work. Our ongoing efforts include scaling up evaluation
to diverse projects and benchmarks to quantify gains more rigorously, and enhancing the system’s
adaptability (making the planner and orchestrator more dynamic and error-aware). We are also
interested in exploring how human developers and AI agents can best collaborate; for instance,
allowing a human to intervene in the agent loop in a structured way (perhaps to approve a plan or
provide hints) could combine the strengths of both.
    Overall, our findings suggest that the era of multi-agent, context-rich code assistants is on
the horizon. By carefully engineering the context and workflow in which advanced LLMs operate,
we can unlock capabilities that single monolithic prompts alone cannot achieve. We hope this work
provides a foundation and inspiration for building the next generation of AI-assisted development
tools.


References
 [1] Bui, N. D. Q., Phan, H. N., and Nguyen, P. X. (2024). HyperAgent: Generalist Software
     Engineering Agents to Solve Coding Tasks at Scale. arXiv:2409.16299.

 [2] Arora, D., Sonwane, A., Wadhwa, N., Mehrotra, A., Utpala, S., Bairi, R., Kanade, A.,
     and Natarajan, N. (2024). MASAI: Modular Architecture for Software-engineering AI Agents.
     arXiv:2406.11638.

 [3] Wen, J., Guan, J., Wang, H., Wu, W., and Huang, M. (2025). CodePlan: Unlocking Reasoning
     Potential in Large Language Models by Scaling Code-form Planning. In Proceedings of ICLR
     2025.



                                                12
[4] Aggarwal, V., Kamal, O., Japesh, A., Jin, Z., and Schölkopf, B. (2025). DARS: Dynamic
    Action Re-Sampling to Enhance Coding Agent Performance by Adaptive Tree Traversal.
    arXiv:2503.14269.

[5] Gu, W., Chen, J., Wang, Y., Jiang, T., Li, X., Liu, M., Liu, X., Ma, Y., and Zheng, Z. (2025).
    What to Retrieve for Effective Retrieval-Augmented Code Generation? An Empirical Study
    and Beyond. arXiv:2503.20589.

[6] Bula, T., Pujar, S., Buratti, L., Bornea, M., and Sil, A. (2025). SeaView: Software Engineering
    Agent Visual Interface for Enhanced Workflow. arXiv:2504.08696.

[7] Anthropic. (2025). How we built our multi-agent research system. Engineering Blog, published
    June 13, 2025.




                                               13

