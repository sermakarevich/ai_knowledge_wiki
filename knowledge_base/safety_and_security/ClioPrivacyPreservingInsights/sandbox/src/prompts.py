"""Prompt templates for each LLM-powered stage of the Clio pipeline.

Each prompt mirrors a specific section of the paper and is designed to
produce structured, PII-free output.
"""

# Section 3.1 -- Facet Extraction
# The LLM reads a full conversation and distills it into a short topic
# summary that contains zero personally-identifiable information.
FACET_EXTRACTION_PROMPT = """\
You are a privacy-preserving conversation analyst.

Given the following conversation between a user and an AI assistant,
extract a concise topic summary (1-2 sentences) that captures what the
conversation is about.

CRITICAL RULES:
- Do NOT include any names, locations, organizations, or other identifying info.
- Do NOT quote the user directly.
- Focus on the general topic, task type, and domain.

Conversation:
{conversation}

Respond with ONLY the topic summary, nothing else."""

# Section 3.3 -- Cluster Description
# Given a batch of facet summaries that landed in the same cluster,
# produce a single title and description that represents the group.
CLUSTER_DESCRIPTION_PROMPT = """\
You are a privacy-preserving analyst. You are given topic summaries from
a cluster of similar AI assistant conversations.

Generate:
1. A short TITLE (3-6 words) for this cluster.
2. A DESCRIPTION (1-2 sentences) summarizing the common theme.

CRITICAL RULES:
- Do NOT include any personally-identifiable information.
- Generalize across all summaries -- do not single out individual conversations.

Topic summaries:
{facets}

Respond in this exact format:
TITLE: <your title>
DESCRIPTION: <your description>"""

# Section 3.4 -- Privacy Audit
# A separate LLM pass checks whether a cluster description accidentally
# leaks PII. This is one layer of the defense-in-depth approach.
PRIVACY_AUDIT_PROMPT = """\
You are a privacy auditor. Your job is to check whether the following
cluster description contains any personally-identifiable information (PII).

PII includes: names, email addresses, phone numbers, physical addresses,
organization names, account numbers, specific dates of birth, or any
information that could identify a specific individual.

Cluster title: {title}
Cluster description: {description}

Respond in this exact format:
PASSED: true or false
REASON: <brief explanation>"""

# Section 3.4 -- Hierarchy Building
# Groups existing cluster descriptions into higher-level categories,
# building the multi-level taxonomy the paper describes.
HIERARCHY_PROMPT = """\
You are a taxonomy builder. Given the following cluster titles and
descriptions, group them into 2-4 higher-level categories.

Clusters:
{clusters}

For each category, provide:
1. A CATEGORY name (2-4 words).
2. Which cluster numbers belong to it (comma-separated).
3. A one-sentence SUMMARY of the category.

Respond in this exact format (one block per category):
CATEGORY: <name>
CLUSTERS: <comma-separated cluster numbers>
SUMMARY: <one sentence>"""
