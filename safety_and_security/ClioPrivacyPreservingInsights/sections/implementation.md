> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Implementation Details

This section catalogs every concrete implementation choice reported in the paper: models, prompts, parameters, datasets, validation protocols, cost estimates, and the interactive visualization interface.

---

### 1. Models Used at Each Pipeline Stage

| Pipeline Stage | Model | Model ID | Temperature |
|---|---|---|---|
| Screener (input filtering) | Claude 3 Haiku (public) | `claude-3-haiku-20240307` | 0.2 |
| Facet Extraction (summaries) | Claude 3 Haiku (public) | `claude-3-haiku-20240307` | 0.2 |
| Concern-score Extraction | Claude 3.5 Sonnet (June 2024) | `claude-3-5-sonnet-20240620` | (uses extractor template) |
| Base-level Cluster Labeling | Claude 3.5 Sonnet (June 2024) | `claude-3-5-sonnet-20240620` | 1.0 |
| Hierarchy Generation (all sub-steps) | Claude 3.5 Sonnet (June 2024) | `claude-3-5-sonnet-20240620` | 1.0 |
| Privacy Auditor | Claude 3.5 Sonnet (June 2024) | `claude-3-5-sonnet-20240620` | 0.05 |
| Synthetic Data Generation | Helpful-only Claude (version unspecified) | -- | -- |
| Embedding | all-mpnet-base-v2 (sentence-transformers) | `all-mpnet-base-v2` | N/A |

Key observations:
- The cheapest model (Haiku) handles the highest-volume work: screening and per-conversation facet extraction.
- The most capable model (Sonnet) is reserved for cluster labeling, hierarchy construction, and the safety-critical privacy auditor.
- The privacy auditor uses an unusually low temperature (0.05), favoring deterministic, conservative judgments.

---

### 2. Embedding Model and Configuration

- **Model:** `all-mpnet-base-v2` (Reimers & Gurevych, 2022), a sentence-transformer based on MPNet, trained on over 1 billion training pairs.
- **Embedding dimensionality:** 768 dimensions.
- **Usage points:**
  1. Embedding each conversation's extracted summary facet for base-level clustering.
  2. Embedding each cluster's name and description for hierarchical clustering.
- **Projection to 2D:** UMAP with parameters `n_neighbors=15`, `min_dist=0`, `cosine` metric.

---

### 3. Clustering Parameters

#### Base-level Clustering

- **Algorithm:** k-means in 768-dimensional embedding space.
- **k selection:** Varies with dataset size. The authors explicitly state they cannot publish exact k values because doing so would reveal the volume threshold below which coordinated abuse would escape detection as a distinct cluster.
- **Privacy constraint on clusters:** Each cluster must exceed minimum thresholds for both unique accounts and unique conversations. Clusters composed of only a single or small number of accounts are discarded.

#### Cluster Labeling

For each cluster, Claude 3.5 Sonnet receives:
- A random sample of **50 summaries** from records within the cluster.
- **50 summaries** of records closest to the cluster centroid but *not* assigned to the cluster (contrastive examples).

The contrastive examples are critical: the model must generate a name and description that distinguishes this cluster from neighboring clusters, not just describes it generically.

#### Hierarchical Clustering

The hierarchy is built iteratively, level by level, from base clusters up to the desired number of top-level clusters. At each level *l*:

1. **Embed clusters** using `all-mpnet-base-v2` on cluster name + description.
2. **Generate neighborhoods** via k-means, choosing k so the average neighborhood size is **40 clusters**.
3. **Propose higher-level clusters per neighborhood** using Claude, including the nearest *m* clusters outside the neighborhood for boundary coverage.
4. **Deduplicate** proposed clusters across all neighborhoods using Claude.
5. **Assign** each lower-level cluster to its best-fit parent using Claude. Higher-level clusters are randomly shuffled when presented to avoid order bias.
6. **Rename** each parent cluster based on its actual assigned children.

**Scaling formula for number of clusters per level:**

The number of clusters at level *l* is constrained to n_l +/- 1.5 * n_l. The target ratio between successive levels follows:

    n_l / n_{l-1} = (n_top / n_base)^(1/(L-1))

for *L* total levels. This produces a geometric progression from base clusters to the desired top-level count.

**Hierarchy structure in practice:** Three levels -- e.g., 10 top-level categories, 100 mid-level categories, 1,000 leaf clusters (for the cost estimate scenario).

**Alternatives considered and rejected:** HDBSCAN (McInnes et al., 2017) and agglomerative clustering methods were explored but found inferior to the Claude-based hierarchical approach.

---

### 4. Prompt Templates and Strategies

All prompts below are reproduced verbatim or near-verbatim from the paper's appendices (G.3--G.8). The system uses a consistent two-turn dialogue format with XML-tagged outputs.

#### 4.1 Screener Prompt

Used to filter input conversations to a specific subset (e.g., election-related). Forces binary Yes/No output:

> **Turn 1 (Human):** Presents the full conversation transcript.
> **Turn 2 (Assistant):** "I understand."
> **Turn 3 (Human):** Poses the screening question in `<question>` tags, demands "Yes" or "No" in `<answer>` tags.
> **Turn 4 (Assistant prefill):** "Sure, the answer to the question is: `<answer>`"

Example screening question for election monitoring:

> "Does this conversation relate to U.S. politics, voting, democratic participation, or the 2024 U.S. election at all (even if only loosely)? Answer either 'Yes' or 'No' with no other commentary."

#### 4.2 Extractor Prompt (Facet Extraction)

The core extraction prompt follows the same two-turn structure, but with richer instructions for open-ended facets:

> **Turn 1 (Human):** Presents the conversation.
> **Turn 2 (Assistant):** "I understand."
> **Turn 3 (Human):** Asks the facet question. For open-ended facets, appends privacy instructions:
>
> "When answering, do not include any personally identifiable information (PII), like names, locations, phone numbers, email addresses, and so on. When answering, do not include any proper nouns. Output your answer to the question in English inside `<answer>` tags; be clear and concise and get to the point in at most two sentences."
>
> Includes few-shot examples:
> - "The user asked for help with a trigonometry problem."
> - "The user asked for advice on how to fix a broken dishwasher. It took several attempts to get the right answer."
> - "The user asked how to make Anthrax and the AI system refused the requests."
>
> **Turn 4 (Assistant prefill):** "Sure, the privacy-preserving answer to the question about the preceding conversation is: `<answer>` {prefill}"

The privacy instruction block ("When answering, do not include...") is included **only** for open-ended facets, not for numeric or categorical ones (e.g., concern scores).

#### 4.3 Specific Facets and Their Prompts

| Facet | Question | Prefill |
|---|---|---|
| **Request** | "What is the user's overall request for the assistant?" | "The user's overall request for the assistant is to" |
| **Language** | "What are the main languages of the conversation? Do not mention programming languages and do not provide only language codes; only the full names for human languages... Only consider languages in or after the human's first request. Output each language as a single full word with no other commentary." | (standard prefill only) |
| **Task** | "What task is the model being asked to perform in this conversation?" | "The task is to" |
| **Concerning** | A detailed rubric from 1 (not concerning) to 5 (extremely concerning), with example anchors for each level -- see below | (standard prefill only) |

**Concern-score rubric (verbatim):**

| Score | Description | Example Anchor |
|---|---|---|
| 1 | Not concerning at all. Completely benign conversation. | A friendly chat about favorite books or movies. |
| 2 | Slightly concerning, but likely harmless. | A heated but civil debate about politics. |
| 3 | Moderately concerning. May warrant a closer look. | Discussion of controversial topics that could escalate. |
| 4 | Very concerning. Likely needs review. | Conversations involving potential self-harm or harmful ideation. |
| 5 | Extremely concerning. Immediate review needed. | Explicit threats of violence or illegal activities. |

Language facet outputs were validated using the `langcodes` and `language-data` Python packages (Speer, 2024a, 2024b).

#### 4.4 Base-level Cluster Labeling Prompt

The cluster labeling prompt instructs Claude to generate both a two-sentence summary and a short name (max 10 words). Key design choices:

- **Contrastive framing:** The model receives both in-cluster summaries (`<answers>`) and nearby-but-excluded summaries (`<contrastive_answers>`), forcing the label to be discriminative.
- **Safety-first specificity:** The prompt explicitly states: "Do not hesitate to identify and describe socially harmful or sensitive topics specifically; specificity is necessary for monitoring."
- **Actionable names preferred:** Examples given include "Write fantasy sexual roleplay with octopi and monsters", "Generate blog spam for gambling websites", "Assist with high school math homework" -- contrasted against vague alternatives like "Write erotic content" or "Help with homework."
- **Per-facet criteria:** A `<criteria>` block is injected per facet. For the Request facet: "The cluster name should be a sentence in the imperative that captures the user's request."

#### 4.5 Hierarchizer Prompts

The hierarchy construction uses four distinct prompts, each with Claude 3.5 Sonnet at temperature 1.0:

1. **Proposing cluster names per neighborhood:** Given a list of clusters with descriptions, generate roughly `{desired_names}` higher-level categories. Output range constrained to `[0.5 * desired_names, 1.5 * desired_names]`. Uses a `<scratchpad>` for chain-of-thought reasoning before the final `<answer>`.

2. **Deduplicating across neighborhoods:** Merges similar proposed clusters from different neighborhoods. Same output range constraint. Instructions emphasize semantic (not lexical) similarity and maintaining specificity during merges.

3. **Assigning to higher-level clusters:** For each lower-level cluster, selects the single best-fit parent. Uses a `<scratchpad>` step, then outputs the exact parent name in `<answer>` tags. The list of candidate parents is randomly shuffled to avoid order bias.

4. **Renaming higher-level clusters:** After assignment, regenerates each parent's name and description based on its actual children. Same format as base-level labeling (two-sentence summary + max-10-word name).

All four prompts include explicit instructions about safety specificity: "clusters that clearly describe harmful behavior are slightly preferred" and "specificity is necessary for effective monitoring and enforcement."

#### 4.6 Privacy Auditor Prompt

The auditor classifies cluster names/descriptions on a 1-5 privacy scale with 12 hand-crafted examples spanning the full range. Key design details:

- **Temperature:** 0.05 (nearly deterministic).
- **Classification threshold:** Scores of 3 ("might narrow down identification to the order of a few thousand people") and above are considered acceptable.
- **Output format:** `<justification>` tags for reasoning, then `<rating>` tag for the score.
- **Explicit guidance:** The prompt lists five specific checks (names of individuals/organizations, locations, unique identifiers, specific events/dates, general vs. specific information).
- **Notable example calibrations:**
  - "The user asked for advice setting up their boba shop's marketing website, named Spindle Boba." scores **2** (identifies a specific business).
  - "The conversation centers on the Zebb Quinn case, a well-known long-running missing persons investigation." scores **5** (public knowledge, no private info).
  - "The user asked several direct questions about Donald Trump and Kamala Harris." scores **5** (public figures).
  - "The discussion is about the user's severe suicidal thoughts and self-harm behaviors." scores **5** (no identifying details despite sensitivity).

The paper notes a typo in an earlier version of the prompt: "scontentummary" instead of "content" -- preserved as-is in the published appendix.

---

### 5. Dataset Details

#### 5.1 Production Datasets (Claude.ai)

All production analyses used Claude.ai Free and Pro tier consumer conversations. Teams, Enterprise, API, and Zero Retention customers were **excluded**.

| Analysis | Sample Size | Sampling Strategy | Date Range (UTC) |
|---|---|---|---|
| General Claude.ai Usage (Section 3, Fig 6) | 1,000,000 | Strategy 2 (sample conversations directly) | Oct 17--Oct 24, 2024 |
| Multilingual Analysis (Section 3.3, Fig 7) | 2,281,911 | Strategy 1 (sample completions, deduplicate) | Oct 24--Nov 13, 2024 |
| Safety Classifier Analysis (Section 4, Fig 8) | 500,000 | Strategy 2 | Oct 31--Nov 13, 2024 |
| Privacy Benchmarking (Section D, Fig 5) | 25,000 | Strategy 1 | Nov 8--Nov 14, 2024 |

**Sampling strategies:**

- **Strategy 1 (sample completions, then deduplicate):** Take a random sample of Claude.ai model outputs. Deduplicate by keeping only the most recent output per conversation. Provide Clio the full transcript up to and including that output. *Biases toward longer conversations.*
- **Strategy 2 (sample conversations directly):** Sample conversations at random, provide full transcript up to the most recent turn. *Weights short and long conversations equally.*

#### 5.2 Synthetic Evaluation Datasets

Generated via a hierarchical process using a helpful-only Claude model:

1. **Manually specify** high-level categories (e.g., "financial planning and investment" for regular; "inquiries about illegal drug manufacturing" for concerning).
2. **Claude generates** more specific subcategories within each category.
3. **Claude generates** individual prompts within each subcategory, with randomly varied length, tone, and language.
4. **Claude continues** the conversation as if responding to a real user.

| Dataset | Conversations | Top-level Categories | Languages |
|---|---|---|---|
| Regular synthetic | 19,476 | 20 | 15 |
| Concerning synthetic | 19,488 | 18 | 15 |

Languages tested: English, Ukrainian, Spanish, Japanese, Mandarin Chinese, French, Russian, Hindi, Portuguese, Catalan, Armenian, Arabic, Afrikaans, Turkish, Georgian.

#### 5.3 External Datasets Analyzed

- **WildChat** (Zhao et al., 2024): ~1M conversations collected by offering free GPT-3.5-Turbo and GPT-4 access via HuggingFace Spaces. Used for public demonstration of the Clio interface.
- **LMSYS-Chat-1M** (Zheng et al., 2023): ~1M queries from the Chatbot Arena platform. Analyzed for comparative distribution of use cases.

---

### 6. Privacy Auditor Implementation and Accuracy Metrics

#### 6.1 Four Privacy Layers

The system employs defense-in-depth with four sequential privacy barriers:

| Layer | Mechanism | Effect |
|---|---|---|
| 1. Conversation summary step | Model instructed to omit PII, proper nouns | Private info drops from ~10% (raw) to ~1.5% |
| 2. Cluster aggregation thresholds | Minimum unique accounts and conversations per cluster; small clusters discarded | Prevents small-group identification |
| 3. Cluster summary step | Model again instructed not to include private information | Further reduction |
| 4. Cluster auditing | Privacy auditor model reads cluster summaries, removes any with private info | Drives to undetectable levels |

#### 6.2 Privacy Scale (1-5 Rubric)

| Score | Level | Description |
|---|---|---|
| 1 | Identifiable to an Individual | Contains easily identifiable information that could single out an individual or small group |
| 2 | Identifiable to a Specific Group | Details that could identify specific organizations, communities, or institutions |
| 3 | Identifiable to Thousands | Specifics that narrow identification to several thousand people |
| 4 | Identifiable with Significant Context | Mostly general; identification possible only with substantial additional context |
| 5 | Not Identifiable | Entirely general information without any specific identifying details |

Scores of 1 or 2 are considered privacy failures. Score 3 and above is the acceptable threshold.

#### 6.3 Auditor Validation

- **Test set:** 1,237 examples (630 non-privacy-preserving, 607 privacy-preserving).
- **Construction:** Privacy-preserving examples curated from real Clio clusters. Non-privacy-preserving examples created by taking privacy-preserving clusters and subtly editing them to introduce fictional private information, using a combination of models and manual annotation.
- **Accuracy:** **98%** on this binary classification task (rated 3+ = privacy-preserving; rated 1-2 = not).

#### 6.4 Privacy Progression Through Pipeline (5,000 Conversations)

- **Raw conversations:** ~10% contain private information (scores 1 or 2).
- **Post-summary:** Private information drops to ~1.5%.
- **Post-cluster summary (analyst-visible output):** Almost all clusters rated 5, a few rated 4, **none rated 3 or below**.

---

### 7. Validation Methodology

#### 7.1 Manual Review Protocols

A small number of employees with authorized access reviewed conversation data under strict privacy controls. Two types of data were manually reviewed:

- **Random sample:** Randomly sampled from Claude.ai Free and Pro.
- **Concerning sample:** Random conversations whose last turn was flagged by automated Trust and Safety tooling.

| Component | Combined Accuracy | Random Data | Concerning Data |
|---|---|---|---|
| Extractor (Summaries) | 96% | 93% | 98% |
| Extractor (Concerning Content ID) | 0.84 (Spearman's rho) | -- | -- |
| Base-level Clusterer | 97% | 99% | 96% |
| Hierarchical Clusterer | 97% | 95% | 99% |

**Conversation summaries (200 conversations):**
- 96% accurately summarized overall.
- Main failure mode: long multi-topic conversations where summary omitted some requests (model tended to focus on more harmful requests if present).

**Concern scores (200 conversations):**
- Spearman correlation of 0.84 between human and model scores (strong directional agreement).

**Base-level clusters (5,904 assignments across 183 clusters):**
- 99% of clusters on random data had accurate titles; 96% on T&S-flagged data.
- Average 3% of conversations per cluster were misassigned (typically subtle errors, e.g., "analyze business case studies" cluster incorrectly including a stock analysis conversation).

**Hierarchical clusters (1,094 assignments across 183 clusters):**
- 97% overall title accuracy (95% random, 99% T&S-flagged).

#### 7.2 End-to-End Synthetic Data Evaluation

**Supervised reconstruction (ground-truth labels known):**
- Clio summarizes and clusters unsupervised, then assigns base clusters to known higher-level categories.
- **94% accuracy** on 20 regular categories.
- **84% accuracy** on 18 concerning categories. Performance drop attributed to model evasiveness on harmful content and some overlap between concerning categories (e.g., "fringe conspiracy theories" vs. "pseudoscientific health practices").

**Multilingual performance (regular synthetic data):**

| Language | Accuracy | Macro F1 | Weighted F1 | Samples |
|---|---|---|---|---|
| English | 0.954 | 0.954 | 0.955 | 1,354 |
| Ukrainian | 0.952 | 0.956 | 0.952 | 1,243 |
| Spanish | 0.950 | 0.952 | 0.950 | 1,283 |
| Japanese | 0.944 | 0.943 | 0.945 | 1,297 |
| Mandarin Chinese | 0.942 | 0.942 | 0.943 | 1,296 |
| French | 0.942 | 0.946 | 0.942 | 1,260 |
| Russian | 0.941 | 0.938 | 0.941 | 1,261 |
| Hindi | 0.941 | 0.937 | 0.941 | 1,330 |
| Portuguese | 0.941 | 0.947 | 0.942 | 1,343 |
| Catalan | 0.941 | 0.946 | 0.942 | 1,299 |
| Armenian | 0.939 | 0.934 | 0.939 | 1,302 |
| Arabic | 0.939 | 0.940 | 0.939 | 1,294 |
| Afrikaans | 0.937 | 0.936 | 0.938 | 1,295 |
| Turkish | 0.935 | 0.940 | 0.935 | 1,357 |
| Georgian | 0.927 | 0.933 | 0.927 | 1,262 |

All languages maintain accuracy above 92%. Range: 92.7% (Georgian) to 95.4% (English).

**Unsupervised reconstruction:**
- Fully unsupervised Clio runs on synthetic data were qualitatively compared to ground truth via confusion matrices.
- Results were "quite sensible" -- e.g., software development questions mapped to "provide expert guidance on software development and troubleshooting."
- Acknowledged weaknesses: some valid-but-suboptimal groupings (e.g., geopolitics placed under "explain complex topics and troubleshoot technology issues").

#### 7.3 Safety Classifier Correlation

- **Method:** Per-cluster comparison of Clio's mean concern score vs. Anthropic's Trust & Safety classifier flag rate.
- **Result:** Pearson correlation r = 0.71.
- **Use:** Divergences identify false positives (high flag rate, low concern score) and false negatives (low flag rate, high concern score).

---

### 8. Computational Costs and Infrastructure

#### 8.1 Cost Breakdown for 100,000 Conversations

| Step | Claude Model | Input Tokens | Output Tokens | Input Cost ($) | Output Cost ($) | Total Cost ($) |
|---|---|---|---|---|---|---|
| Facet Extraction | 3 Haiku | 130.0M | 10.0M | 32.50 | 12.50 | 45.00 |
| Cluster Labeling | 3.5 Sonnet | 1.0M | 50.0K | 3.00 | 0.75 | 3.75 |
| Hierarchy Generation | 3.5 Sonnet | 18.0K | 600 | 0.05 | 0.01 | 0.06 |
| **Estimated Total** | | | | | | **$48.81** |

**Pricing basis:** Claude 3 Haiku at $0.25/MTok input, $1.25/MTok output. Claude 3.5 Sonnet at $3/MTok input, $15/MTok output.

**Assumptions:**
- Average conversation length: 1,000 tokens.
- Facet extraction prompt: 300 tokens.
- Facet summary length: 100 tokens.
- Average cluster size: 100 conversations.
- Hierarchy: three levels (10 top-level, 100 mid-level, 1,000 leaf clusters).

**Cost per conversation:** ~$0.0005 (roughly $0.50 per 1,000 conversations).

Note: Embedding costs (all-mpnet-base-v2) and UMAP projection are not included in this table, as these are run locally and are computationally trivial compared to the LLM inference costs. The paper does not mention specific hardware or cloud infrastructure details.

---

### 9. Interactive Visualization Interface

The Clio interface supports four complementary exploration modalities:

#### 9.1 Map View (Figure 3)

- **Projection:** Clusters projected to 2D via UMAP (768-dim -> 2D, cosine metric, n_neighbors=15, min_dist=0).
- **Interaction:** Zoomable -- zooming in reveals progressively more granular (lower-level) clusters. Zooming out shows high-level categories.
- **Coloring:** Clusters can be colored by various attributes: size, growth rate, safety classifier scores, or any other facet value.
- **Use case:** Serendipitous discovery and rapid identification of concerning clusters. Example: an analyst might zoom into the "Writing" cluster, notice a large sub-cluster titled "Formulaic content generation for SEO," and flag it for review.

#### 9.2 Tree View (Figure 9)

- **Structure:** Hierarchical representation of clusters. Users navigate from broad categories down to specific sub-clusters.
- **Sidebar:** Clicking a cluster shows its summary and children.
- **Complementary to Map View:** Offers structured navigation vs. the spatial exploration of the map.

#### 9.3 Faceted and Temporal Breakdowns

- When a cluster is selected, a sidebar shows breakdowns by other facets (e.g., language distribution, turn-length distribution).
- Temporal dimension: shows how facet membership has changed over time, enabling detection of emerging trends or shifts.

#### 9.4 Facet Overlays

- Users select a facet value (e.g., language=Spanish) and the map recolors to show prevalence of that feature across all clusters.
- Enables cross-dimensional analysis: e.g., which coding clusters have disproportionately high Japanese usage.

#### 9.5 Traces Feature

- **Restricted access:** Only available when underlying data is non-sensitive (public datasets, synthetic data) or to authorized Anthropic employees (e.g., Trust & Safety).
- **Function:** Drill down into representative examples from each cluster, providing concrete context for abstract patterns.

---

### 10. Preprocessing and Data Handling

- **Preprocessing algorithm:** Raw conversation transcripts standardized into an XML-based format before model analysis.
- **Special handling for:** Function calls, system prompts, multimodal information, and metadata that may be embedded in conversations.
- **No geographic analysis:** Clio explicitly does not support analysis based on geography (mentioned as a privacy safeguard).
- **Data retention:** All data managed according to Anthropic's established privacy and retention policies. Raw conversations processed in a secure private environment with restricted access; only aggregate clusters are made available outside this environment.

---

### 11. Safety-Specific Implementation Variations

When Clio is used for safety purposes (Section 4), the implementation differs from the standard privacy-preserving mode:

- **Cluster aggregation thresholds are removed** to enable identification of coordinated abuse even from small groups of accounts.
- **Results can be linked back to individual accounts** for enforcement actions.
- **Strict access controls** limit viewing of safety-focused results to a small number of authorized Trust & Safety staff.
- **No automated enforcement:** Actions are never taken based solely on Clio clusters. Suspicious clusters are manually reviewed by designated T&S team members in a secure environment.
- **API traffic:** For safety investigations, Clio is also run on a subset of first-party API traffic (not just Claude.ai consumer). Results are restricted to authorized staff. Certain accounts (trusted organizations with Zero Retention agreements) are excluded.

---

### 12. Key Quantitative Findings from Implementation

| Metric | Value |
|---|---|
| Synthetic dataset reconstruction accuracy (regular) | 94% across 20 categories |
| Synthetic dataset reconstruction accuracy (concerning) | 84% across 18 categories |
| Conversation summary accuracy | 96% (200 conversations) |
| Concern-score Spearman correlation (human vs. model) | 0.84 |
| Base-level cluster title accuracy | 97% (183 clusters) |
| Hierarchical cluster title accuracy | 97% (183 clusters) |
| Average misassignment rate per cluster | 3% |
| Privacy auditor accuracy | 98% (1,237 test examples) |
| Raw conversations with private info | ~10% |
| Post-summary private info rate | ~1.5% |
| Post-cluster-summary private info (analyst-visible) | 0% at scores 1-3 |
| Safety classifier vs. concern score correlation | Pearson r = 0.71 |
| Multilingual accuracy range | 92.7%--95.4% |
| Cost per 100K conversations | $48.81 |
| Cost per conversation | ~$0.0005 |
