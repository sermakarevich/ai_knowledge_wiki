"""Prompt templates adapted from Appendix A of ML-Master 2.0 (arxiv 2601.10402).

Each template references the paper section or appendix it derives from.
"""

# Adapted from Appendix A.1 -- Task Descriptor Prompt.
# Asks the LLM to produce a compact DATA / MODEL summary used as the
# retrieval key for L3 prior wisdom.
TASK_DESCRIPTOR_PROMPT = """You are summarising a machine-learning task for later retrieval.

TASK:
{task_description}

Produce a compact descriptor with two sections. Keep it under 80 words total.

DATA SUMMARY: <one line on the modality, scale, and label type>
MODEL SUMMARY: <one line on the kind of model family that is a reasonable starting point>
"""

# Adapted from Section 3.2.1 -- Hypothesis Generation / Research Plan.
# Uses L3 retrieved wisdom + L2 refined knowledge of prior phases.
PLAN_PROMPT = """You are an ML research agent running phase {phase_index} of a long-horizon task.

TASK: {task_description}

PRIOR WISDOM (retrieved from similar past tasks):
{retrieved_wisdom}

REFINED KNOWLEDGE (lessons from earlier phases of THIS task):
{refined_knowledge}

Propose ONE concrete research direction for trajectory {trajectory_idx} of this phase.
Do not repeat a direction already present in refined knowledge.
Respond in exactly two lines:

HYPOTHESIS: <one-sentence hypothesis>
CODE SKETCH: <two- or three-line pseudocode outline>
"""

# Adapted from Section 3.2.2 -- Code Execution / Observation.
# In the real system the agent runs Python; here we have the LLM
# imagine a plausible observation so the sandbox runs locally.
EXECUTE_PROMPT = """You are simulating the execution of a proposed ML experiment.

HYPOTHESIS: {hypothesis}
CODE SKETCH: {code_sketch}

Imagine running this. Return a short, plausible observation including one
validation-like score between 0 and 1. Bias scores toward 0.4-0.8 so some
directions work and some do not.

OBSERVATION: <2-3 sentences on what happened, including any failure mode>
SCORE: <single float between 0 and 1>
"""

# Adapted from Appendix A.3 -- P1 Prompt (Phase-level Context Promotion).
# Collapses a set of parallel trajectories into one kappa_p refined-knowledge entry.
P1_PROMOTE_PROMPT = """You just completed one research phase of a long-horizon ML task.

TASK: {task_description}

TRAJECTORIES FROM THIS PHASE:
{trajectories_block}

Produce a compact summary of this phase in two parts:

EXECUTION SUMMARY:
- what was tried
- which trajectory performed best and why

STRATEGIC INSIGHTS:
- 2-3 bullets with judgments that should guide the NEXT phase
- only include insights that are validated by the observations above
"""

# Adapted from Appendix A.3 -- P2 Prompt (Task-level Context Promotion).
# Distills all phase-level knowledge into one L3 wisdom entry.
P2_PROMOTE_PROMPT = """The task is complete. Distill durable, cross-task wisdom from the task history.

TASK: {task_description}

REFINED KNOWLEDGE ACROSS ALL PHASES:
{refined_knowledge_block}

Produce an L3 wisdom entry in exactly two sections, targeting reuse on FUTURE
similar tasks. Keep each section under 60 words. Be task-agnostic where possible.

DATA SUMMARY: <generalisable observation about the data pattern>
MODEL SUMMARY: <generalisable modelling strategy, with hyperparameter priors where justified>
"""
