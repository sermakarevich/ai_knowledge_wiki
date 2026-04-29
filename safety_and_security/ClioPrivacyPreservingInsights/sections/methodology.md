> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Methodology

Clio (Claude Insights and Observations) implements a multi-stage pipeline that transforms raw conversations between users and AI assistants into privacy-preserving, hierarchically organized, interactively explorable insights. The system is analogous to Google Trends for AI assistant usage: it reveals aggregate patterns without exposing individual interactions. The pipeline comprises five major stages -- facet extraction, semantic clustering, cluster description, hierarchy building, and interactive exploration -- each reinforced by four layers of privacy protection.

---

### 1. Facet Extraction

#### What Are Facets?

A **facet** is a specific attribute or characteristic of a conversation. Clio extracts multiple facets per conversation, enabling multi-dimensional analysis and cross-facet exploration (e.g., how use cases vary by language).

Facets range from trivially computable to model-extracted:

| Facet Type | Computation Method | Example |
|---|---|---|
| Programmatic / numeric | Direct computation from raw data | Number of conversational turns |
| Categorical (model-extracted) | Claude classifies into categories | Language of the conversation |
| Open-ended summary (model-extracted) | Claude generates free-text summary | Conversation topic / user request |

#### Extraction Model and Parameters

- **Model:** Claude 3 Haiku (public; claude-3-haiku-20240307)
- **Temperature:** 0.2
- **Input format:** Conversations are preprocessed into a standardized XML-based format. Special handling is applied to function calls, system prompts, multimodal information, and metadata embedded in the conversation.

#### Extraction Prompt Template

The extractor uses a two-turn prompt structure. The conversation is inserted into the first Human turn. The second Human turn poses the facet question and includes explicit privacy instructions (for open-ended facets):

- "Do not include any personally identifiable information (PII), like names, locations, phone numbers, email addresses, and so on."
- "Do not include any proper nouns."
- "Output your answer to the question in English inside answer tags; be clear and concise and get to the point in at most two sentences."

The assistant response is prefilled to steer the output format (e.g., "The user's overall request for the assistant is to").

The privacy language block ("When answering, do not include...") is included **only** for open-ended facets (e.g., user request), not for structured outputs like concern scores.

#### Specific Facets Used

| Facet | Question | Prefill | Notes |
|---|---|---|---|
| **Request** | "What is the user's overall request for the assistant?" | "The user's overall request for the assistant is to" | Primary facet for clustering |
| **Task** | "What task is the model being asked to perform in this conversation?" | "The task is to" | Used in Section 3 (usage analysis) |
| **Language** | "What are the main languages of the conversation?" (excludes programming languages; requires full names, not codes) | Standard prefill only | Validated with `langcodes` and `language-data` Python packages |
| **Concerning** | 1-5 scale rating of how concerning the conversation is from a safety perspective | Standard prefill only | Scale ranges from 1 ("completely benign") to 5 ("explicit threats of violence or illegal activities") |

#### Optional Screener

Before extraction, Clio optionally uses Claude to **screen** the input data to narrow the sample. The screener uses Claude 3 Haiku (claude-3-haiku-20240307) at temperature 0.2 with a Yes/No classification prompt. For example, during election monitoring, the screener question was: "Does this conversation relate to U.S. politics, voting, democratic participation, or the 2024 U.S. election at all (even if only loosely)?"

---

### 2. Semantic Clustering

#### Embedding

For non-categorical or numeric facets (e.g., the request facet), each extracted summary is embedded using **all-mpnet-base-v2** (Reimers and Gurevych, 2022), a sentence transformer model that produces **768-dimensional** embeddings. The choice of summarization prompt controls what information is captured and therefore which conversations land close together in embedding space.

#### Clustering Algorithm

Clio primarily uses the **k-means** algorithm (Lloyd, 1982) to group embeddings into clusters. The authors experimented with other methods but found k-means "works surprisingly well for identifying neighborhoods in what is fundamentally a continuous manifold of conversation types, rather than discrete, well-separated clusters."

#### Choosing k

The number of clusters k is adjusted based on the size of the dataset. In practice, k can be very large -- many thousands of clusters. The exact values of k are not disclosed in the paper; the authors explicitly state that revealing precise k values "could be used to determine the volume at which coordinated behavior would likely not be caught by Clio as a distinct cluster."

#### Privacy-Aware Aggregation

Clusters are subject to a **minimum unique user threshold** -- a cluster is only retained if it contains conversations from a minimum number of distinct accounts. This dual approach (semantic similarity + minimum user count) prevents identification of individuals or small groups within the data.

---

### 3. Cluster Description

#### Model and Parameters

- **Model:** Claude 3.5 Sonnet (June 2024; claude-3-5-sonnet-20240620)
- **Temperature:** 1.0

#### Input to the Describer

For each cluster, the describer receives:

1. **50 summaries** randomly sampled from records within the cluster.
2. **50 contrastive summaries** -- summaries of records that are closest to the cluster's centroid but are *not* assigned to the cluster.

The contrastive examples are the key mechanism: they force the model to identify what makes this cluster *distinctive* rather than generating a generic description.

#### Prompt Strategy

The prompt instructs the model to:

- Summarize the cluster into a "clear, precise, two-sentence description in the past tense."
- Generate a short name of "at most ten words" that is "specific but also reflective of most of the statements."
- Distinguish this group from the contrastive examples.
- "Assume neither good nor bad faith" and "do not hesitate to identify and describe socially harmful or sensitive topics specifically; specificity is necessary for monitoring."

Names must follow facet-specific criteria. For the Request facet, the requirement is: "The cluster name should be a sentence in the imperative that captures the user's request. For example, 'Brainstorm ideas for a birthday party' or 'Help me find a new job.'"

The prompt explicitly prefers actionable, specific names over vague ones. Examples given: "Write fantasy sexual roleplay with octopi and monsters", "Generate blog spam for gambling websites", or "Assist with high school math homework" are preferred over generic terms like "Write erotic content" or "Help with homework."

---

### 4. Hierarchy Building

#### Motivation

A single Clio run can produce thousands of base-level clusters. To make exploration tractable, Clio organizes these into a **multi-level hierarchy** -- from a few dozen top-level categories (e.g., "Explain scientific concepts and conduct academic research") down to thousands of granular leaf clusters (e.g., "Explain and analyze cancer immunology research and treatments").

#### Model and Parameters

- **Model:** Claude 3.5 Sonnet (June 2024; claude-3-5-sonnet-20240620)
- **Temperature:** 1.0

The authors also explored HDBSCAN (McInnes et al., 2017) and agglomerative clustering but found results "inferior to the Claude-based approach."

#### Iterative Algorithm

The hierarchizer transforms base clusters into a multi-level hierarchy through an iterative process. At each level l, it performs these steps:

**Step 1: Embed clusters.** Embed each cluster's name and description using all-mpnet-base-v2 to obtain 768-dimensional vector representations.

**Step 2: Generate neighborhoods.** Group cluster embeddings into k neighborhoods using k-means, where k is chosen so that the **average number of clusters per neighborhood is 40**. This neighborhood grouping is necessary because the names and descriptions for all base clusters may not fit within Claude's context window.

**Step 3: Propose new clusters for each neighborhood.** For each neighborhood, Claude proposes candidate higher-level cluster descriptions by examining both:
- The clusters within the neighborhood
- The nearest m clusters outside it (to ensure boundary clusters are neither overcounted nor undercounted)

The target number of clusters at level l is constrained to n_l +/- 1.5 * n_l, where n_l is chosen so that the ratio between successive levels follows:

    n_l / n_{l-1} = (n_top / n_base)^{1/(L-1)}

for L total levels. This ensures a geometrically smooth reduction across levels.

**Step 4: Deduplicate across neighborhoods.** Claude deduplicates and refines the proposed clusters across all neighborhoods to ensure distinctiveness while maintaining coverage of the underlying data distribution. The deduplication prompt instructs the model to "group similar cluster names together based on their semantic meaning, not just lexical similarity" and to "maintain as much specificity as possible while merging."

**Step 5: Assign each lower-level cluster to its best-fit higher-level parent.** Claude assigns each base/lower-level cluster to the most appropriate parent. The order of higher-level clusters is **randomly shuffled** when sampling from Claude to avoid biasing assignments based on list order. The prompt includes explicit instructions: "You MUST assign the specific cluster to the best higher-level cluster, even if multiple higher-level clusters could be considered."

**Step 6: Rename higher-level clusters.** Once all clusters at level l have been assigned to a higher-level cluster, a new name and description are regenerated for the parent cluster based on the lower-level clusters actually assigned to it. This ensures names continue to accurately reflect their contents after assignment.

This process repeats until reaching the desired number of top-level clusters k_top.

#### Hierarchy Structure (Typical)

For a run of 100,000 conversations, the paper's cost analysis assumes a three-level hierarchy:

| Level | Approximate Count |
|---|---|
| Leaf (base) clusters | ~1,000 |
| Mid-level clusters | ~100 |
| Top-level clusters | ~10 |

---

### 5. Interactive Exploration

Clio presents the hierarchically organized clusters through an interactive interface with multiple complementary views:

#### 5.1 Map View (UMAP Projection)

- **Algorithm:** UMAP (Uniform Manifold Approximation and Projection; McInnes et al., 2020)
- **Input:** The 768-dimensional all-mpnet-base-v2 embedding for each conversation
- **Output:** 2D coordinates for each conversation
- **Hyperparameters:** n_neighbors=15, min_dist=0, metric=cosine

The map view is a zoomable 2D projection where users can visually explore relationships between clusters. Zooming in reveals progressively more granular clusters. Clusters can be colored by various attributes including size, growth rate, and safety classifier scores.

#### 5.2 Tree View

A hierarchical tree representation lets users navigate from broad categories down to specific sub-clusters. Clicking a node displays its summary and children.

#### 5.3 Faceted and Temporal Breakdowns

When a cluster is selected, a sidebar displays:
- **Facet breakdowns:** Distribution of the cluster by other facets (e.g., language, turn length)
- **Temporal trends:** How facet membership has changed over time, enabling identification of emerging trends or shifts in usage patterns

#### 5.4 Facet Overlays

Users can select a facet value (e.g., language=Spanish) and color the entire map to display the prevalence of that feature across all clusters.

#### 5.5 Traces (Restricted Access)

For non-sensitive data (synthetic data, public datasets) or for authorized Anthropic employees (e.g., Trust and Safety), a "traces" feature allows drilling down into representative examples from each cluster.

---

### 6. Privacy Layers

Clio employs a **defense-in-depth** approach with four privacy layers. Because Clio produces rich textual descriptions, formal guarantees such as differential privacy or k-anonymity are difficult to apply. Instead, the system takes a "statistical and empirically validated approach," with multiple layers collectively driving the rate of private information in outputs to undetectable levels.

The paper defines **private information** broadly: any information that could identify not just individual people but also small numbers of individuals or specific organizations (e.g., a small 100-person village or a 15-person business).

#### Layer 1: Conversation Summary Step

**Where:** During facet extraction (Stage 1 of the pipeline).

**Mechanism:** The extraction prompt explicitly instructs the model to answer the summarization question while omitting any private information:
- "Do not include any personally identifiable information (PII), like names, locations, phone numbers, email addresses, and so on."
- "Do not include any proper nouns."
- The assistant response is prefilled with: "Sure, the privacy-preserving answer to the question about the preceding conversation is:"

**Measured effect:** Reduces private information from ~10% of raw conversations down to ~1.5% of summaries (as measured by the automated privacy auditor on a sample of 5,000 conversations).

#### Layer 2: Cluster Aggregation Thresholds

**Where:** After clustering (Stage 2).

**Mechanism:** Clusters are only retained if they exceed minimum size requirements for both:
- **Unique accounts** (number of distinct user accounts)
- **Conversations** (total conversation count)

Clusters composed of a single or small number of accounts are discarded entirely. The exact threshold values are not published.

**Effect:** Prevents the creation of clusters that could be traced back to specific individuals or small groups.

#### Layer 3: Cluster Summary Step

**Where:** During cluster description (Stage 3).

**Mechanism:** When generating cluster summaries, the model is again instructed not to include private information. The contrastive-example approach inherently promotes generalization over specificity.

**Measured effect:** After the cluster summary step, "almost all clusters were rated 5 [fully privacy-preserving], with a few instances rated 4, and none rated 3 or below" on the 5-point privacy scale.

#### Layer 4: Cluster Auditing

**Where:** After cluster description (Stage 3), before results are visible to analysts.

**Mechanism:** A dedicated privacy auditor model reads all cluster summaries and removes any clusters that still contain private information.

**Privacy Auditor Details:**
- **Model:** Claude 3.5 Sonnet (June 2024; claude-3-5-sonnet-20240620)
- **Temperature:** 0.05 (very low, for consistency)
- **Rating scale:** 1-5, where scores of 1-2 are considered privacy violations

| Score | Privacy Level | Example |
|---|---|---|
| 1 | Identifiable to an Individual | "Can you provide advice on improving my resume? [uploads resume]" |
| 2 | Identifiable to a Specific Group | "Help me come up with a jingle for my new startup, Golden Gate Widgets and Gadgets" |
| 3 | Identifiable to Thousands | "Write an email inviting my family to come visit me in Springfield, Ohio" |
| 4 | Identifiable with Significant Context | "I'm looking for recipes that would appeal to regulars at a beachside coffee shop" |
| 5 | Not Identifiable | "Can you come up with an analogy to help explain the difference between lists vs sets in Python?" |

Scores of 3 and above are considered acceptable. Clusters scoring 1 or 2 are removed.

**Auditor validation:** Tested on a curated dataset of 1,237 examples (630 non-privacy-preserving, 607 privacy-preserving), achieving **98% accuracy** as a binary classifier (privacy-preserving vs. not). Non-privacy-preserving examples were created by taking real privacy-preserving clusters and subtly editing them to introduce fictional private information via a combination of models and manual annotation.

#### Cumulative Privacy Effect

Measured across the pipeline on 5,000 Claude.ai conversations:

| Pipeline Stage | % Private Information (scores 1-2) |
|---|---|
| Raw conversations (baseline) | ~10% |
| After summarization (Layer 1) | ~1.5% |
| After cluster summaries (Layers 1-3) | ~0% (no scores below 3) |

At the point where Clio's outputs are visible to analysts (cluster summaries), the amount of private information reaches "very low levels" -- effectively undetectable in the evaluation.

#### Safety Mode Exception

For Trust and Safety enforcement purposes, Layers 2 and 4 (aggregation thresholds and cluster auditing) are **not applied**, so that the safety team can identify and take enforcement action against individual violating accounts. These results are restricted to a small number of authorized staff with strict access controls, and results can be linked back to individual accounts.

---

### Cost Analysis

The paper provides an estimated cost breakdown for processing 100,000 conversations:

| Step | Claude Model | Input Tokens | Output Tokens | Input Cost ($) | Output Cost ($) | Total Cost ($) |
|---|---|---|---|---|---|---|
| Facet Extraction | Claude 3 Haiku | 130.0M | 10.0M | 32.50 | 12.50 | 45.00 |
| Cluster Labeling | Claude 3.5 Sonnet | 1.0M | 50.0K | 3.00 | 0.75 | 3.75 |
| Hierarchy Generation | Claude 3.5 Sonnet | 18.0K | 600 | 0.05 | 0.01 | 0.06 |
| **Total** | | | | | | **48.81** |

Assumptions: average conversation length of 1,000 tokens, facet extraction prompt of 300 tokens, facet summary length of 100 tokens, cluster size of 100 conversations. Cost per conversation: $0.0005.

Pricing: Claude 3 Haiku at $0.25/MTok input and $1.25/MTok output; Claude 3.5 Sonnet at $3/MTok input and $15/MTok output.

---

### Input Sampling Strategies

Two sampling strategies were used across the paper's experiments:

| Strategy | Method | Weighting |
|---|---|---|
| Strategy 1 | Sample model completions, then deduplicate by conversation (keep most recent output per conversation; provide full transcript up to that output) | Weights longer conversations more heavily |
| Strategy 2 | Sample conversations directly at random; provide full transcript up to most recent turn | Weights all conversations equally |

| Analysis | Sample Size | Strategy | Date Range (UTC) |
|---|---|---|---|
| Multilingual Analysis | 2,281,911 | Strategy 1 | Oct 24 -- Nov 13, 2024 |
| Safety Classifier Analysis | 500,000 | Strategy 2 | Oct 31 -- Nov 13, 2024 |
| Privacy Benchmarking | 25,000 | Strategy 1 | Nov 8 -- Nov 14, 2024 |
| General Claude.ai Usage | 1,000,000 | Strategy 2 | Oct 17 -- Oct 24, 2024 |

All data was sampled from Claude.ai Free and Pro tiers, excluding Teams, Enterprise, and Zero Retention customers.

---

### Validation Summary

| Component | Metric | Score |
|---|---|---|
| Conversation summaries (extractor) | Manual accuracy (200 conversations) | 96% overall (93% random, 98% concerning) |
| Concerning content identification | Spearman correlation (human vs. model ratings) | 0.84 |
| Base-level clusterer | Title accuracy (5,904 assignments, 183 clusters) | 97% overall; 3% average misassignment rate |
| Hierarchical clusterer | Title accuracy (1,094 assignments, 183 clusters) | 97% overall (95% random, 99% concerning) |
| End-to-end reconstruction (synthetic) | Category reconstruction accuracy (19,476 transcripts, 20 categories) | 94% (regular), 84% (concerning) |
| Multilingual performance | Accuracy across 15 languages | > 92% on all languages (range: 92.7% Georgian to 95.4% English) |
| Privacy auditor | Binary classification accuracy | 98% on 1,237 curated examples |
