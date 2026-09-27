
	1	Arize AX
	2	Phoenix OSS
	3	Docs Docs Arize AX  Managed AI engineering platform Phoenix OSS  Open-source observability and evals    
	4	Learn Start here Blog  AI engineering best practices Video tutorials  Hands-on product walkthroughs   Build your playbook Resources  Guides, templates, and reports Glossary  Learn AI engineering terminology Courses & certifications  Build practical AI engineering skills   See it in production Customers  How teams ship production AI Events  Live and on-demand events Community  Connect with AI engineers    
	5	Company Company About  We power the future of AI Careers  Join a world class team Partners  Partner with us    Press  Updates from the newsroom Security  We take your trust seriously    
	6	Pricing
Sign in Try Arize AX Book a Demo
	1	Arize AX
	2	Phoenix OSS
	3	Docs
	4	Learn
	5	Company
	6	Pricing
Sign up Book a demo
Resources
Learn Blog Resources Customers Events


	1	Resources
	2	/
	3	LLM Evaluation
The definitive guide to LLM evaluations
A practical guide to building and implementing evaluation strategies for AI applications and agents.
	•	
	•	
	•	

Chapters
	1	What is LLM evaluation?
	2	LLM evaluation metrics: correctness, groundedness, RAG & agent scores
	3	Pre-production LLM evaluation: datasets, synthetic data & benchmarks
	4	CI/CD for LLM apps: experiments, regression tests & release gates
	5	Production LLM evaluation: guardrails, online evals & monitoring
	6	Self-improving LLM evaluation: feedback loops & eval iteration
Contents
	•	TL;DR
	•	Getting started with LLM evaluation
	•	Quick answer: AI and agent evaluation vs. LLM evaluation
	•	Why is LLM evaluation important?
	•	Explore the LLM evaluation guide
	•	Where to go next
	•	How to debug AI agents: tracing, observability & evals
	•	From unit and integration testing to LLM evaluation
	•	LLM evaluation methods
	•	How to choose an LLM evaluation approach
	•	What should you evaluate in an LLM application?
	•	Agent evaluation and agent-as-a-judge
	•	LLM evaluation techniques comparison chart
	•	Retrieval-augmented generation (RAG) evaluation
	•	LLM benchmarks vs. application-specific evaluation
	•	Choosing between online and offline LLM evaluation
	•	Evaluation across the LLM application lifecycle
	•	Regulatory and governance evaluation
	•	Multimodal evaluation
	•	How to build an LLM evaluation strategy
	•	Get started with LLM evaluation
Learn more
Book a demo
Talk to our experts in agent observability to see Arize AX up close.
Learn more
LLM-as-a-Judge
Learn more about LLM as a judge
Watch — 3:17
Code Evaluations


Put it in Production
Instrument your first eval in Arize with an engineer.
Book a demo
CHAPTER SUMMARY
Overview: The introduction provides an overview of LLM evaluation, and emphasizes the importance of evaluating LLM applications to ensure they meet user expectations and perform reliably. It highlights the shift from traditional software testing to dynamic, context-sensitive evaluations that account for LLMs’ non-deterministic nature. This was last updated on August 31, 2026. 
Get started with LLM evaluation by following our product documentation, which provides step-by-step guidance to begin implementing effective evaluation strategies.
TL;DR
	•	LLM evaluation measures whether an application answers correctly, uses the right evidence, calls the right tools, and completes tasks under realistic conditions.
	•	Combine code checks, LLM-as-a-Judge, human review, and production sampling — no single method covers every failure mode.
	•	A tutorial that applies that mix to a financial research agent, starting from traces, is How to build agent evals from traces.
	•	Connect offline datasets, CI/CD release gates, and production monitoring so every change is testable before and after deployment.
Getting started with LLM evaluation
Large language model (LLM) evaluation is the process of measuring whether an LLM-powered application behaves as intended across realistic inputs, workflows, and operating conditions. It covers the quality of the final response and the steps that produced it, including retrieval, routing, tool calls, model calls, guardrails, latency, cost, and end-to-end task success.
LLM applications change constantly. Teams revise prompts, swap models, adjust retrieval, add tools, change orchestration, and respond to new production failures. Without evaluation, it is difficult to know whether a change improved the application, introduced a regression, or only made the demo look better.
Evaluation turns those changes into testable questions. Instead of asking, “Does this response look good?” teams can ask whether the application answered correctly, used the right evidence, selected the right tool, followed policy, stayed within latency and cost limits, and completed the user’s task.
Get started with LLM evaluation in the Arize AX documentation, or explore the Phoenix evaluation documentation for an open-source workflow.
TRY ARIZE AX
Build better agents with Arize
Trace, evaluate, and learn. Build agents that work with Arize AX and start tracing your runs today.
Get started
View AX docs
Prefer open source? Try Arize Phoenix for self-hosted, open source agent observability.

Quick answer: AI and agent evaluation vs. LLM evaluation
AI and agent evaluation is the broader practice of measuring whether an AI system performs its intended task reliably, safely, and efficiently. The system may be a predictive machine-learning model, a generative model, a retrieval-augmented generation application, an agent, or a workflow combining several models, tools, and business rules. The evaluation design should match both the unit of behavior the team can change and the outcome the user cares about.
For a traditional predictive model, AI evaluation may focus on accuracy, precision, recall, calibration, drift, fairness, and performance across important segments. For an LLM-powered application, the relevant unit is often larger than the model. Teams may need to evaluate the prompt, retrieved context, model response, routing, tool calls, guardrails, latency, cost, and final task outcome. A strong foundation model can still produce a weak application when the surrounding system supplies poor context, selects the wrong workflow, or fails to complete the requested action.
LLM evaluation is therefore a major category within AI evaluation. It combines deterministic tests, reference-based scoring, LLM-as-a-Judge, human review, and production signals to measure behaviors that do not have one exact correct output. The same evaluator may be used before release on a curated dataset and after release on sampled production traces, although production evaluation introduces additional requirements around latency, cost, privacy, monitoring, and incident response.
Agent evaluation extends the scope further. An agent may select tools, plan across several steps, retrieve information, update state, recover from failures, and interact with a user over a complete session. Evaluating only the final answer can miss a wrong tool call, an invented parameter, or a failed action hidden behind a plausible response. Agent evals therefore measure the observable path and final system state as well as the response.
This guide is the canonical Arize starting point for evaluating LLM-powered applications. Use the agent evaluation guide for autonomous, multi-step workflows, the LLM evaluation metrics guide for choosing quality measures, and the LLM evaluation platform comparison when selecting software.
Evaluation scope
What it measures
Typical methods
AI model evaluation
Model performance across known tasks or datasets
Accuracy, recall, calibration, benchmarks
LLM application evaluation
Prompts, retrieval, responses, tools and workflows
Code checks, LLM judges, reference data, human review
Agent evaluation
Multi-step decisions, tool calls, trajectories and task completion
Span, trace, trajectory and session evals
Business outcome evaluation
Whether the application creates the intended user or operational result
Resolution, conversion, completion and downstream signals
Now, let’s jump in.
Why is LLM evaluation important?
LLMs make it possible to build useful applications without defining every valid input and output in advance. A prompt can generate content, extract structured data, summarize documents, answer questions, call tools, or coordinate a multi-step workflow.
That flexibility is also what makes these applications difficult to test. Outputs are probabilistic, user inputs are open-ended, and a response can be fluent while still being wrong, unsupported, unsafe, or operationally expensive. A workflow can also return the right final answer for the wrong reason, such as using an irrelevant document, inventing a tool argument, or retrying until it happens to succeed.
A practical evaluation system helps teams:
	•	Track whether prompts, models, retrieval strategies, tools, or orchestration changes improve the application.
	•	Catch regressions before they reach users.
	•	Measure quality across dimensions such as correctness, relevance, groundedness, safety, latency, cost, and task completion.
	•	Debug failures by identifying which step in a workflow went wrong.
	•	Compare models, prompts, agent architectures, and retrieval configurations on the same examples.
	•	Monitor production behavior and turn real failures into future test cases.
	•	Preserve evidence for release reviews, audits, and governance processes.
The dataset matters as much as the evaluator. A narrow or overly clean test set can produce strong scores that do not generalize to real traffic. Useful eval datasets represent the application’s supported tasks, common requests, difficult edge cases, policy boundaries, and known production failures.
Explore the LLM evaluation guide
This page provides the broad framework for evaluating LLM applications. The chapters below go deeper on the parts of the workflow that require their own implementation guidance:
	•	LLM evaluation metrics: Choose metrics for correctness, relevance, hallucination, safety, fluency, and other quality dimensions.
	•	Pre-production LLM evaluation: Build and validate curated, synthetic, and human-annotated datasets before release.
	•	CI/CD for LLM apps: Run experiments, compare application changes, and add evaluation to release workflows.
	•	Production LLM evaluation: Use real-time checks and guardrails to reduce risk in deployed applications.
	•	Self-improving LLM evaluation: Use feedback loops, evaluator iteration, and production examples to improve the application over time.
The rest of this page explains how these pieces fit together, including newer evaluation patterns for RAG systems, agents, multimodal applications, benchmarks, and governance.
Where to go next
This guide covers evaluation for LLM applications generally. Four companion resources go deeper on specific problems.
	•	Evaluating agents rather than single responses. Agents fail along a path, not only in a final answer. The agent-native evaluation framework covers outcome, path, decision quality, and reliability.
	•	Implementing the workflow. For the engineering process — datasets, evaluator selection, experiments, regression cases, and release gates — see how to evaluate AI agents in production.
	•	Instrumenting the system first. Evaluation needs evidence to score. AI agent tracing and evaluation covers spans, trace structure, and how instrumentation shapes what you can measure.
	•	Choosing tooling. If you are comparing platforms, LLM and agent evaluation platforms covers selection criteria and includes an RFP checklist.
Budgeting the work is a separate question from designing it. LLM evaluation costs covers the cost model, formulas, and sample budgets.
How to debug AI agents: tracing, observability & evals

From unit and integration testing to LLM evaluation
LLM evaluation extends familiar software testing principles rather than replacing them. Traditional unit tests isolate functions and verify deterministic behavior. Integration tests check whether services and components work together. Those tests remain essential for an LLM application: APIs still need to return valid responses, schemas still need to parse, and tools still need to update the correct records.
The difference is that many important LLM behaviors cannot be expressed as one exact expected string. A useful answer may have several valid forms. The right response may depend on retrieved context, conversation history, user intent, policy, or the result of a tool call. Evaluation therefore combines conventional tests with datasets, rubrics, model-based judges, human labels, and production signals.
For example, a customer support agent may need to:
	•	Classify the user’s request correctly.
	•	Select the right support workflow.
	•	Extract an order number without inventing missing information.
	•	Call the right tool with valid parameters.
	•	Follow refund and escalation policies.
	•	Use the tool result in the final response.
	•	Resolve the user’s issue without unnecessary steps.
A single pass/fail check on the final message cannot show which of those behaviors succeeded or failed. Effective LLM evaluation tests both the components and the end-to-end task.
In traditional software engineering:
	•	Unit Testing isolates individual components of the code, ensuring that each function works correctly on its own.
	•	Integration Testing focuses on how different modules or services work together, validating the correctness of their interactions.
In the world of LLM applications, these goals remain, but the complexity of behavior increases due to the non-deterministic nature of LLMs.
	•	Dynamic Behavior Evaluation: Rather than testing isolated code components, LLM evaluations focus on how the application responds to various inputs in real-time, examining not just accuracy but also context relevance, coherence, and user experience.
	•	Task-Oriented Assessments: Evaluations are now centered on the application’s ability to complete user-specific tasks, such as resolving queries, generating coherent responses, or interacting seamlessly with external systems (e.g., function calling).
Both paradigms emphasize predictability and consistency, with the key difference being that LLM applications require dynamic, context-sensitive evaluations, as their outputs can vary with different inputs. However, the underlying principle remains: ensuring that the system (whether it’s traditional code or an LLM-driven application) performs as designed, handles edge cases, and delivers value reliably.
LLM evaluation methods
LLM evaluation works best as a layered system. Different methods are reliable for different behaviors, and most production applications need more than one type of evaluator.
LLM-as-a-judge
LLM-as-a-judge uses a language model to evaluate another model’s output against a written rubric. The judge can return a categorical label, a score, an explanation, or a structured combination of those outputs.
This approach is useful for semantic or open-ended qualities that are difficult to express in code, such as answer correctness, relevance, groundedness, helpfulness, tone, policy adherence, conversation quality, or whether an agent completed a task. The evaluator should receive the evidence it needs. A hallucination evaluator for a RAG response, for example, needs the model response and the retrieved context, not only the response.
An LLM judge is not ground truth by itself. Judge outputs can change with the model, prompt, label definitions, input order, and examples provided. Teams should validate important evaluators against a human-labeled dataset, inspect disagreements, and version evaluator changes just as they version application changes.
Learn more about LLM-as-a-judge.
Code-based evaluation
Code-based evaluators use deterministic logic to check conditions that have clear, machine-verifiable answers. They are often the best choice for JSON validity, schema compliance, exact matches, required fields, numeric ranges, regex checks, tool argument validation, executable code tests, latency limits, token budgets, and API status.
Code-based checks are fast, reproducible, and do not add judge-model token costs. Their limitation is scope: they can verify that a field exists, but they usually cannot determine whether an open-ended answer is genuinely helpful or whether a summary preserves the meaning of a source document.
Ground truth comparison and human review
Ground truth comparison measures an output against a trusted reference answer or label. It works well for classification, extraction, question answering, and tasks with a known expected state. For agents, ground truth can also describe the correct tool, parameters, database state, or acceptable task outcome.
Human review remains important when the task requires subject-matter expertise, policy judgment, or interpretation that automated evaluators have not yet demonstrated reliably. Human labels are especially useful for discovering failure modes, creating benchmark datasets, calibrating LLM judges, and reviewing uncertain or high-risk cases.
The goal is not to have humans label every production output. It is to use targeted human judgment to define what good looks like and verify that automated evaluators approximate it closely enough for their intended use.
User feedback and production signals
User feedback reveals whether the application works in the environment that matters most. Explicit signals such as thumbs-up ratings, corrections, escalations, or survey responses can be useful, but they are often sparse and biased toward unusually good or bad experiences.
Behavioral signals can add context. Repeated questions, abandoned sessions, manual overrides, unresolved tickets, tool retries, and downstream task completion may all indicate quality problems. These signals should be interpreted carefully because they can have causes outside the model.
How to choose an LLM evaluation approach
No single evaluator can reliably measure every dimension of an LLM application. Choose the simplest method that can verify the behavior in question, then combine methods where one signal is insufficient.
Evaluation need
Start with
Add when needed
Schema validity, exact values, tool arguments or latency limits
Code-based evaluation
Property-based tests and production monitors
Correctness, relevance, groundedness or helpfulness
LLM-as-a-Judge
Human-labeled examples for calibration
Known correct answers, labels or final states
Ground-truth comparison
Semantic scoring for acceptable variations
Specialized, ambiguous or high-risk decisions
Human review
Automated evaluators after agreement is established
RAG performance
Separate retrieval and generation evals
End-to-end task and citation evaluation
Agent workflows
Span-, trace-, trajectory- and session-level evals
Repeated-run reliability and final-state checks
Production quality and emerging failures
Online evaluation and user signals
Monitoring, alerts and regression datasets
Most mature evaluation systems combine several of these approaches. Code-based checks catch structural failures quickly. LLM judges assess semantic quality. Reference data tests known cases. Human review defines and validates the quality bar. Production signals reveal behaviors the original dataset did not anticipate.
Choosing an evaluation approach is different from choosing an evaluation platform. This guide covers the methodology. For a buyer-oriented comparison of Arize AX, Phoenix, LangSmith, Braintrust and Langfuse, see Comparing LLM Evaluation Platforms.
For a deeper treatment of individual quality dimensions and scoring approaches, see LLM evaluation metrics.

What should you evaluate in an LLM application?
The right evaluation target depends on the application architecture and the user task. A simple text-generation feature may only require output checks. A RAG application or agent usually needs evaluation at several levels.
Common evaluation targets include:
	•	Final response quality: Is the answer correct, relevant, complete, grounded, useful, and appropriate for the user?
	•	Retrieval quality: Did the system retrieve documents or passages that were relevant, sufficient, and ranked well for the query?
	•	Routing: Did the application select the right model, workflow, skill, or function?
	•	Tool selection and parameters: Did the agent choose the correct tool and pass complete, valid arguments derived from the user’s request?
	•	Tool result handling: Did the application detect tool errors, interpret the result correctly, and avoid claiming success when the operation failed?
	•	Agent path quality: Did the workflow take a reasonable sequence of steps without loops, redundant calls, or premature completion?
	•	Safety and policy adherence: Did the application follow business, legal, privacy, and safety requirements, including escalation rules?
	•	Operational performance: Did the system stay within acceptable latency, cost, token, throughput, and error-rate limits?
	•	Session and task outcomes: Did the application resolve the user’s goal across the full interaction, not only produce a locally plausible response?
These checks can run at different scopes. Span-level evals assess an individual model call, retrieval step, or tool invocation. Trace-level evals assess one end-to-end run. Session-level evals assess a sequence of interactions, which is often necessary for conversational systems and long-running agents.
Agent evaluation and agent-as-a-judge
Agent evaluation measures whether an AI agent completes a task correctly across a multi-step workflow. The agent may need to interpret the request, plan, retrieve context, select a skill, call a tool, update state, recover from errors, and decide when the task is complete.
Because the workflow is stateful and non-deterministic, agent evaluation needs to look beyond the final response. A polite, confident answer can hide a wrong tool call, an invented parameter, a failed write, or an inefficient path.
Why final-answer evaluation is not enough
Suppose an order-support agent tells a user that an address was updated successfully. The message may look correct, but several different failures can sit behind it:
	•	The agent selected the tracking tool instead of the order-management tool.
	•	It extracted a tracking number where the API required an order ID.
	•	The tool returned an error that the agent ignored.
	•	The update applied to the wrong order.
	•	The agent never called the tool and only described what it intended to do.
A final-answer judge might miss these failures unless it can inspect the observable workflow and resulting state. Agent evaluation should therefore test the decisions and actions that produced the response.
LLM evaluation techniques comparison chart
We’ve reviewed various LLM eval methodologies here to assess different aspects of their capabilities and real-world effectiveness. This table provides a comparison of several key evaluation methods, including those leveraging the power of other LLMs for judgment, automated code-based assessments, and the distinct perspectives offered by online and offline evaluation strategies.
(Click to expand)

Evaluate agent workflows step by step
Common agent checks include:
	•	Skill or function selection: Did the agent choose the workflow that matches the user’s intent?
	•	Parameter extraction: Did it extract the right values without omitting required information or inventing unsupported values?
	•	Tool-call accuracy: Did the call match the tool schema and the user’s request?
	•	Retrieval quality: If the agent used retrieval, did it find the evidence needed for the task?
	•	Result interpretation: Did it use the returned data correctly and recognize errors or empty results?
	•	Path quality: Did it take a valid and reasonably efficient sequence of steps?
	•	Recovery behavior: Did it respond appropriately to missing information, ambiguous requests, tool failures, or conflicting evidence?
	•	Task completion: Did the environment reach the expected state, and did the final response accurately describe what happened?
The evaluator does not need access to private hidden reasoning. It can assess observable plans, actions, tool calls, intermediate outputs, state changes, and the final result.
Use traces to diagnose agent failures
Traces expose the sequence of spans behind an agent run. Depending on the application, a trace may include routing, retrieval, model calls, tool calls, custom logic, evaluator results, and user feedback.
This makes evaluation more diagnostic. If task success drops, teams can determine whether the source is a router regression, a tool-description change, parameter extraction, retrieval quality, a backend error, or final-response generation. Without traces, those failure modes can collapse into one generic “bad answer” label.
Trace data also helps build better datasets. Teams can select examples from specific paths, tool failures, low-confidence decisions, long sessions, or repeated user corrections, then add those cases to regression tests.
Agent-as-a-judge
Agent-as-a-judge uses a model-based evaluator to inspect an agent workflow rather than only a single response. The judge can evaluate whether the selected tools were appropriate, whether the path was coherent, whether evidence supported the outcome, and whether the agent recovered correctly from problems.
For reliable results, define the judge’s scope precisely. A tool-selection evaluator should judge tool choice, not overall helpfulness. A path evaluator should know the available tools and the task goal. A task-completion evaluator should receive the final observable state when that state is the real success criterion.
Read the Arize guide to agent evaluation.
Retrieval-augmented generation (RAG) evaluation
RAG evaluation measures both retrieval and response generation. A RAG application can fail because it retrieved the wrong documents, selected weak passages, constructed poor context, ignored the available evidence, or generated claims that the evidence did not support.
Evaluating only the final response hides where the failure originated. A fluent answer can be wrong because the retriever never found the necessary source. An apparently poor answer can also be the correct refusal when the retrieved context does not contain enough information.
Evaluate retrieval
Retrieval evaluation asks whether the system found useful evidence for the query. Common checks include:
	•	Document relevance: Do the retrieved documents match the user’s question or task?
	•	Context relevance: Do the selected passages contain information that helps answer the question?
	•	Coverage or sufficiency: Is the context complete enough to support a correct response?
	•	Ranking quality: Are the most useful results placed where the generator is likely to use them?
	•	Retrieval diversity: When the task requires multiple sources or perspectives, did the system avoid returning redundant passages?
Ground truth document IDs are useful when they exist. LLM judges can help when relevance is semantic and several documents may be acceptable. Retrieval metrics should be interpreted in the context of the generator, because more retrieved text is not always better: irrelevant context can increase latency, cost, and hallucination risk.
LLM benchmarks vs. application-specific evaluation
Public benchmarks measure broad model or agent capability on a shared test suite. They are useful for comparing systems under a common protocol and for identifying whether a model is capable of the general kind of work an application requires.
Different benchmarks test different environments:
	•	SWE-bench evaluates repository-level software engineering tasks.
	•	Terminal-Bench evaluates agents completing tasks in terminal environments.
	•	tau-bench evaluates tool-using agents interacting with simulated users under domain policies.
	•	WebArena evaluates autonomous agents in realistic web environments.
	•	OSWorld evaluates computer-use agents across real desktop applications and operating systems.
	•	GAIA evaluates general assistants on tasks involving reasoning, tools, browsing, and multimodal information.
A benchmark score is not evidence that an application is ready for production. Public benchmarks do not contain a company’s prompts, retrieval corpus, APIs, policies, user distribution, latency requirements, or failure costs. They can also become less representative as systems optimize specifically for them.
Task-specific evaluation tests the components the team controls. Useful application datasets combine representative examples, human-labeled cases, synthetic edge cases, real production traces, and known failures. The strongest evaluation strategy uses public benchmarks as a broad capability signal and application-specific evals as the acceptance criteria for the system that will actually ship.
Evaluate response generation
Generation evaluation asks whether the final response used the retrieved evidence correctly. Common checks include:
	•	Answer correctness: Did the response answer the user’s question accurately?
	•	Faithfulness or groundedness: Are the response’s claims supported by the retrieved context?
	•	Citation quality: Do citations point to sources that support the associated claims?
	•	Completeness: Did the response address the important parts of the request that the context could support?
	•	Abstention behavior: Did the application avoid inventing an answer when the evidence was insufficient?
	•	End-to-end task success: Did the system complete the user’s actual task, not merely produce a relevant passage?
Diagnose the pipeline, not just the score
Separate retrieval and generation evals make RAG failures actionable:
	•	If retrieval relevance is low, investigate the query transformation, embeddings, chunking, filters, or reranker.
	•	If the context is relevant but the answer is unsupported, investigate the generation prompt, model, context formatting, or instruction hierarchy.
	•	If the answer is correct but citations are wrong, investigate the attribution and citation-mapping layer.
	•	If both stages score well but users remain dissatisfied, revisit the task definition, response format, latency, and dataset coverage.
Choosing between online and offline LLM evaluation
While it may seem advantageous to apply online evaluations universally, they introduce additional costs in production environments. The decision to use online evaluations should be driven by the specific needs of the application and the real-time requirements of the business. AI engineers can typically group their evaluation needs into three categories: offline evaluation, guardrails, and online evaluation.
	•	Offline evaluation: Offline evaluations are used for checking LLM application results prior to releasing to production. Use offline evaluations for CI/CD checks of your LLM application. Example: Customer service chatbot where you want to make certain changes to a prompt do not break previously correct responses.
	•	Guardrail: AI engineers want to know immediately if something isn’t right and block or revise the output. These evaluations run in real-time and block or flag outputs when they detect that the system is veering off-course. Example: An LLM application generates automated responses for a healthcare system. Guardrails check for critical errors in medical advice, preventing harmful or misleading outputs from reaching users in real time.
	•	Online evaluation: AI engineers don’t want to block or revise the output, but want to know immediately if something isn’t right. This approach is useful when it’s important to track performance continuously but where it’s not critical to stop the model’s output in real time. Example: An LLM application generates personalized marketing emails. While it’s important to monitor and ensure the tone and accuracy are correct, minor deviations in phrasing don’t require blocking the message. Online evaluations flag issues for review without stopping the email from being sent.
Evaluation across the LLM application lifecycle
LLM evaluation should continue from development through production. Offline and online evaluation are not necessarily different evaluator designs; they describe where the data comes from and when the evaluation runs. The same correctness or groundedness evaluator can often score a curated test dataset before release and sampled production traces after release.
Pre-production evaluation
Pre-production evaluation uses curated examples to test expected behavior before deployment. The dataset may include hand-written cases, human annotations, synthetic examples, benchmark data, and failures collected from an earlier version of the application.
This stage is where teams define task coverage, create ground truth, calibrate evaluators, compare model or prompt candidates, and stress-test edge cases. Dataset quality matters more than raw size. A smaller set that covers the application’s important paths and failure modes is often more useful than a large set of near-duplicate examples.
For detailed guidance on golden datasets, annotations, synthetic data, and evaluator benchmarking, see pre-production LLM evaluation.
CI/CD and release evaluation
Evaluation becomes part of CI/CD when teams run the same dataset and evaluators against proposed application changes. An experiment can compare a new prompt, model, retriever, tool definition, routing policy, or orchestration graph with the current baseline.
Release criteria should reflect product risk. A team may require no regression on critical policy cases, a minimum task-success rate, bounded latency and cost, and manual review of newly failing examples. Because LLM evals can be noisy, release decisions should consider confidence intervals, repeated runs where appropriate, and the severity of individual failures rather than relying on one aggregate score.
For experiments and deployment workflows, see CI/CD for LLM apps.
Production evaluation
Production evaluation runs on real traces and user interactions. It reveals changes in user behavior, data, tool responses, traffic mix, and failure modes that a pre-production dataset may not capture.
Not every production eval belongs in the request path. Guardrails run synchronously when an unsafe or invalid input or output must be blocked, transformed, or escalated before it reaches the user. Other online evals can run asynchronously on all traffic or a sample, providing monitoring and alerting without adding user-facing latency.
For the guide’s deeper treatment of real-time safeguards, see production LLM evaluation.
Continuous improvement
Production evaluation should feed the next development cycle. Teams can review failed traces, identify recurring patterns, add representative cases to a dataset, update evaluators when the rubric is incomplete, test candidate fixes, and monitor the released change against the same measures.
A practical loop is:
	1	Observe production behavior.
	2	Identify and categorize failures.
	3	Add failures and boundary cases to an eval dataset.
	4	Update the prompt, model, retrieval, tools, or orchestration.
	5	Run an experiment against the baseline.
	6	Release the change when it meets the quality bar.
	7	Continue monitoring for new failures.
For evaluator iteration, feedback loops, and improvement patterns, see self-improving LLM evaluation.
Regulatory and governance evaluation
In regulated or high-impact environments, evaluation is also part of the evidence layer for governance. Teams may need to show what the application was designed to do, how it was tested, which version produced an output, what data and tools it used, whether it followed policy, and how failures are detected after release.
Evaluation alone does not make an AI system compliant. Requirements depend on the jurisdiction, industry, use case, system role, and risk classification. Legal, risk, security, privacy, and subject-matter experts should help define the controls and evidence the organization needs.
Common governance-oriented evaluation checks include:
	•	Accuracy and performance: Does the system meet the approved quality threshold for the task and population?
	•	Robustness: Does it behave reliably across edge cases, ambiguous inputs, adversarial inputs, and changing production data?
	•	Traceability: Can reviewers reconstruct the prompt, model version, retrieved context, tool calls, evaluator outputs, annotations, and final result?
	•	Policy adherence: Did the application follow business, legal, safety, and domain-specific rules?
	•	Privacy and data leakage: Did the workflow expose sensitive information or send data to an inappropriate component or provider?
	•	Human oversight and escalation: Did the system defer, abstain, or escalate when the request exceeded its authority or confidence?
	•	Release comparison: Did a prompt, model, retrieval, tool, or orchestration change introduce a new governance failure?
	•	Post-release monitoring: Can the team detect, review, and document failures after deployment?
The EU AI Act, for example, uses a risk-based framework. For high-risk systems, the European Commission describes obligations that include risk management, data quality, logging, documentation, human oversight, robustness, cybersecurity, and accuracy. Evaluation and observability can help produce evidence for several of those controls, although the required compliance process is broader than model scoring.
In financial services, SR 11-7 model risk management guidance emphasizes model validation, ongoing monitoring, benchmarking, and outcomes analysis. Teams applying similar governance principles to LLM applications need to understand whether the full workflow performs as intended and whether changes introduce new risks.
In healthcare and life sciences, the FDA’s work on AI-enabled medical devices reflects the importance of lifecycle controls, transparency, safety, and effectiveness for AI-enabled device software. The applicable requirements depend on the product and intended use.
For any governed application, preserve the evidence used for both debugging and review: representative datasets, evaluator versions, experiment results, traces, human annotations, release decisions, and post-release monitoring.
Multimodal evaluation
Multimodal evaluation applies the same principles to applications that work with images, screenshots, PDFs, charts, tables, audio, video, or combinations of those inputs. The system may need to retrieve the correct source, interpret it accurately, generate a grounded answer, or take an action based on visual or audio evidence.
Common multimodal evaluation checks include:
	•	Visual grounding: Is the response supported by the image, screenshot, chart, or page it references?
	•	Document understanding: Did the application extract the correct fields, entities, relationships, and sections from the document?
	•	Table and chart interpretation: Did it understand labels, rows, columns, units, legends, and trends correctly?
	•	Audio and video understanding: Did it identify the relevant speaker, event, timestamp, or sequence without losing important context?
	•	Multimodal retrieval: Did the system retrieve the correct document, page, image region, slide, or media segment before generating the response?
	•	Cross-modal consistency: Does the generated text agree with the non-text source and with other provided modalities?
	•	Output format and action: Did the application return the required schema or take the correct downstream action?
Multimodal workflows often combine deterministic and model-based checks. Code can validate schemas, field presence, numeric constraints, bounding boxes, timestamps, or exact values. Vision-language or multimodal judges can evaluate whether a summary or claim is supported by the source.
The evaluation record should retain enough source context to reproduce the judgment. For a document workflow, that may include the file version, page number, extracted text, image region, model inputs, and final output. Without that lineage, a reviewer may know that an eval failed but not which source evidence the application saw.
How to build an LLM evaluation strategy
A useful evaluation program can start small. The goal is not to create every possible metric before the application ships; it is to measure the most important behaviors with enough coverage to guide decisions.
1. Define the task and quality bar
Write down what the application is expected to accomplish, what it must never do, and which outcomes matter to the user. Separate product requirements from vague goals such as “be helpful.” A support agent, for example, may need explicit criteria for resolution, policy compliance, escalation, and record updates.
2. Identify failure modes
Inspect development runs, early traces, user research, and domain risks. List the ways the system can fail at each component: retrieval, routing, tool use, generation, safety, latency, and task completion. Evaluators should map to these concrete failure modes.
3. Instrument the workflow
Capture traces and the metadata needed to reproduce behavior. At minimum, record relevant inputs and outputs, model and prompt versions, retrieved context, tool calls and results, errors, latency, token usage, and application version. Evaluation is far less useful when the underlying run cannot be inspected.
4. Build a representative dataset
Start with the application’s important paths and known boundaries. Include normal cases, edge cases, adversarial or ambiguous requests where relevant, policy-sensitive cases, and examples that should trigger abstention or escalation. Add production failures as they appear.
5. Match evaluators to behaviors
Use code for deterministic checks, reference comparisons for known outcomes, LLM judges for semantic rubrics, and humans for calibration or high-risk review. Avoid asking one broad evaluator to judge unrelated qualities. Separate correctness, style, safety, tool accuracy, and task completion when different failures require different fixes.
6. Validate the evaluators
Compare automated results with trusted human labels. Review false positives and false negatives, clarify label definitions, provide the evaluator with the right context, and test whether small prompt or model changes alter results unexpectedly. Version the evaluator and its benchmark dataset.
7. Run the same quality system before and after release
Use datasets and experiments to compare changes before deployment. In production, run the same core evaluators on real traces where practical, then add operational signals and guardrails that are specific to live traffic. Comparable measurements make it easier to identify whether production behavior has moved away from the pre-release baseline.
8. Turn failures into regression tests
Every meaningful failure is a candidate test case. Add the example or a privacy-safe representation of it to the dataset, confirm the evaluator detects the problem, test a fix, and keep the case in future release runs. Over time, the dataset becomes a record of the application’s real quality requirements.
Get started with LLM evaluation
LLM evaluation is a repeatable workflow: define expected behavior, instrument the application, test critical failure modes, compare changes, and learn from production. Start with one representative user journey, then follow the Arize AX evaluation quickstart or Phoenix evaluation documentation to implement the workflow.
Next chapter LLM evaluation metrics: correctness, groundedness, RAG & agent scores
Get the latest on AI & Observability
Sign up for our newsletter, The Evaluator—and stay in the know with updates and new resources:
Newsletter Signup Form

SUBSCRIBE

Related articles
Keep building the quality bar.
See all
Agent Engineering
How Coinbase Wallet built an agent-first product development lifecycle
By redesigning planning, validation, and risk review around AI agents, Coinbase Wallet dramatically shortened the path from product idea to working software.
7 min read
Agent Engineering
Agent cost management is about more than the model
Every LLM call your application makes costs money, and agentic applications make a lot of LLM calls. Arize AX now ships a Cost Agent that reads traces, ranks…
8 min read
AI Engineering
How to reduce LLM costs without sacrificing quality
Trace where your AI budget goes, identify the requests that do not justify their spend, and validate lower-cost alternatives with Arize AX.
11 min read
Don’t ship vibes.
Arize gives AI teams observability and evals to understand and improve agent performance.
Get started Book a demo
 
Platform
	•	Arize AX
	•	Alyx
	•	adb
	•	Self-hosted Arize AX
	•	Phoenix Open Source
	•	Arize AX Docs
	•	Phoenix Docs
	•	Pricing
Learn
	•	Blog
	•	Guides, templates, and reports
	•	A Guide to Agent Evals
	•	Customers
	•	Events
	•	Community
	•	Glossary
Topics
	•	LLM Evaluations
	•	Agent Evaluation Metrics
	•	LLM Evals: Proving AI ROI
	•	AI Agent Analytics: A Buyer’s Guide
	•	LLM-as-a-Judge
	•	Arize vs. Braintrust
	•	Arize vs. Langsmith
	•	Arize vs. Langfuse
	•	AI Observability Tools (2026)
	•	What Is an Agent Observability Platform?
	•	LLM & Agent Evaluation Platforms
Company
	•	About
	•	Careers
	•	Press
	•	Partners
	•	Security
	•	Try Arize AX
	•	Book a Demo
	•	Sign In
	•	Contact
	•	AX Platform Status
	•	Privacy Policy
	•	LLMs.txt
	•	Linkedin Twitter YouTube

Copyright © 2026 Arize AI, Inc Privacy Policy
Subscribe to The Evaluator
We’ll send you the latest news, expertise, and product updates from Arize. Your inbox is sacred, so we’ll only curate and send the best stuff.
Subscribe to The Evaluator

Submit
*We're committed to your privacy. Arize uses the information you provide to contact you about relevant content, products, and services. You may unsubscribe from these communications at any time. For more information, check out our privacy policy.
