> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Results & Evaluation

This section covers all quantitative results reported in the paper, organized by evaluation type: pipeline validation (manual review), end-to-end synthetic data reconstruction (supervised and unsupervised), multilingual performance, privacy evaluation, real-world usage analysis, and safety applications.

---

### 1. Pipeline Validation -- Manual Review

Each stage of the Clio pipeline was evaluated independently through manual review. A combined dataset of 200 conversations was used for summarization and concern scoring evaluations: half randomly sampled from Claude.ai Free and Pro, half from conversations flagged by Anthropic's Trust and Safety tooling. Teams, Enterprise, and Zero Retention accounts were excluded.

#### 1.1 Conversation Summary Accuracy

| Data Subset | Accuracy |
|---|---|
| Combined | 96% |
| Random conversations | 93% |
| Concerning conversations | 98% |
| Total conversations reviewed | 200 |

The main failure mode was long, multi-topic conversations where the summary omitted a subset of user requests. In these cases, the model typically focused on the more harmful requests if any existed.

#### 1.2 Concerning Content Identification

The model (Claude) rated conversations on a 1--5 concern scale and was compared against manual human ratings.

| Metric | Value |
|---|---|
| Spearman's rank correlation (model vs. human) | 0.84 |
| Conversations evaluated | 200 |
| Scale | 1 (not concerning) to 5 (extremely concerning) |

The downstream use of concern scores is as a comparative indicator (relative ranking), so correlation is the appropriate metric.

#### 1.3 Base-Level Clusterer Accuracy

| Metric | Random Data | T&S-Flagged Data | Combined |
|---|---|---|---|
| Cluster title accuracy | 99% | 96% | 97% |
| Clusters reviewed | 100 | 83 | 183 |
| Total cluster assignments reviewed | -- | -- | 5,904 |
| Average misassignment rate per cluster | -- | -- | 3% |

The most common error for Trust and Safety-flagged conversations was that cluster titles were overly generic in referring to the type of harm. Misassignments were typically subtle (e.g., "analyze business case studies" incorrectly including a stock analysis conversation that was not part of a business case study).

#### 1.4 Hierarchical Clusterer Accuracy

| Metric | Random Data | T&S-Flagged Data | Combined |
|---|---|---|---|
| Title accuracy | 95% | 99% | 97% |
| Clusters reviewed | 100 | 84 | 183 (higher-level) |
| Total assignments reviewed | -- | -- | 1,094 |

#### 1.5 Pipeline Accuracy Summary Table

Reproduced from the paper (Table 4):

| Component | Combined Accuracy | Random Data | Concerning Data |
|---|---|---|---|
| Extractor (Summaries) | 96% | 93% | 98% |
| Extractor (Concerning Content ID) | 0.84* | -- | -- |
| Base-level Clusterer | 97% | 99% | 96% |
| Hierarchical Clusterer | 97% | 95% | 99% |

*Spearman's Rank Correlation

---

### 2. End-to-End Synthetic Data Reconstruction

Two synthetic datasets were generated with known ground-truth topic distributions to test Clio holistically. The generation process was hierarchical: manually specified high-level categories, Claude-generated subcategories, then Claude-generated prompts with varied length, tone, and language. A helpful-only version of Claude was used for generation.

#### 2.1 Dataset Specifications

| Dataset | Synthetic Conversations | High-Level Categories | Languages |
|---|---|---|---|
| Regular (non-concerning) | 19,476 | 20 | 15 |
| Concerning | 19,488 | 18 | 15 |

#### 2.2 Supervised Reconstruction

In supervised reconstruction, Clio performed unsupervised summarization and base-level clustering, then assigned base-level clusters to known ground-truth high-level categories (equivalent to the assignment step of the hierarchical clusterer).

| Dataset | Accuracy | Baseline (random) |
|---|---|---|
| Regular synthetic data | 94% | 5% (1/20 categories) |
| Concerning synthetic data | 84% | ~5.6% (1/18 categories) |

The performance drop on concerning data is attributed to two factors: (1) Claude's evasiveness when handling harmful content reduces both generation and analysis quality, and (2) overlap between some concerning categories (e.g., "Questions about fringe conspiracy theories" vs. "Discussions promoting pseudoscientific health practices").

Figure 4 in the paper shows the ground-truth vs. reconstructed distributions for regular data are closely aligned. Figure 10 shows the concerning data reconstruction, which still closely tracks the underlying distribution despite lower overall accuracy.

#### 2.3 Unsupervised Reconstruction

In fully unsupervised mode, Clio generates its own cluster hierarchy from scratch. Evaluation is qualitative, comparing Clio's emergent categories to known ground truth.

**Regular data findings:**
- Clio categorized the majority of software development questions into "provide expert guidance on software development and troubleshooting"
- Health and fitness questions mapped to "provide personalized health and fitness advice for diverse needs"
- "Book discussions and literary analysis" split sensibly into "analyze complex global issues in politics, culture, and society" and "analyze literary works and assist with literature-related tasks"
- Suboptimal case: significant fraction of "questions about geopolitics" went to "explain complex topics and troubleshoot technology issues" -- technically correct but not monosemantic

**Concerning data findings:**
- "Requests for advice on academic cheating" mapped primarily to "assist with academic cheating and avoiding detection," followed by "conduct unethical scientific research or falsify results"
- "Glorifying violence and extremism" mapped to clusters about extremist, racist, and terrorist organizations

---

### 3. Multilingual Performance

Clio was tested across 15 languages using the regular synthetic dataset with supervised reconstruction. Performance is consistently high across all tested languages.

#### 3.1 Per-Language Reconstruction Accuracy

Reproduced from Table 5 in the paper:

| Language | Accuracy | Macro Avg. F1 | Weighted Avg. F1 | Samples |
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

**Key observations:**
- All 15 languages achieve accuracy above 92%
- Range: 92.7% (Georgian) to 95.4% (English)
- Spread is narrow (~2.7 percentage points between best and worst)
- Non-Latin script languages (Armenian, Arabic, Georgian) perform only marginally lower

---

### 4. Privacy Evaluation Results

Privacy was evaluated using an automated privacy auditor (a prompted model) that scores content on a 1--5 scale (Table 6 in the paper). Scores of 1--2 are considered privacy-violating; 3+ is considered acceptable.

#### 4.1 Privacy Auditor Validation

| Metric | Value |
|---|---|
| Test set size | 1,237 examples |
| Privacy-preserving examples | 607 |
| Non-privacy-preserving examples | 630 |
| Auditor accuracy (binary: score >= 3 vs. < 3) | 98% |

Non-privacy-preserving examples were created by taking real privacy-preserving clusters and subtly editing them to introduce fictional private information via a combination of models and manual annotation.

#### 4.2 PII Rates at Each Pipeline Layer

Evaluated across a sample of 5,000 Claude.ai conversations:

| Pipeline Stage | PII Rate (scores 1 or 2) | Notes |
|---|---|---|
| Raw conversations (baseline) | ~10% | Before any processing |
| Post-summary | ~1.5% | After conversation summarization with PII-removal prompt |
| Post-cluster summary | 0% (undetectable) | No clusters rated 3 or below; a few rated 4, most rated 5 |

The four privacy layers that achieve this reduction:
1. **Conversation summary step** -- model prompted to omit private information (10% -> ~1.5%)
2. **Cluster aggregation thresholds** -- minimum unique accounts and conversations per cluster
3. **Cluster summary step** -- model again instructed not to include private information
4. **Cluster auditing** -- model reads cluster summaries and removes any with private information

At the analyst-visible stage (cluster summaries), the amount of private information reaches undetectable levels.

#### 4.3 Privacy Scale Definitions

| Score | Level | Description |
|---|---|---|
| 1 | Identifiable to an Individual | Contains easily identifiable information that could single out an individual or small group |
| 2 | Identifiable to a Specific Group | Includes details that could identify specific organizations, communities, or institutions |
| 3 | Identifiable to Thousands | Contains specifics that narrow identification to several thousand people |
| 4 | Identifiable with Significant Context | Mostly general information; identification possible only with substantial additional context |
| 5 | Not Identifiable | Entirely general information without any specific identifying details |

---

### 5. Real-World Usage Analysis Results

Analysis was conducted on 1,000,000 Claude.ai Free and Pro conversations sampled between Oct 17--24, 2024 (Strategy 2: sample conversations directly). Teams, Enterprise, and Zero Retention customers were excluded.

#### 5.1 Top 10 High-Level Task Categories (Claude.ai)

From Figure 6, the top 10 categories on Claude.ai (1M conversations):

| Rank | Category | Approximate Share |
|---|---|---|
| 1 | Web and mobile application development | >10% |
| 2--4 | Writing assistance, Academic research, Educational content | 6--10% each |
| 5--10 | Various business, coding, and creative tasks | Remaining shares |

Key finding: coding-related tasks dominate, with "Web and mobile application development" representing over 10% of all conversations. Writing, research, and educational use cases each comprise 6--10% of usage.

#### 5.2 Cross-Dataset Comparison (Claude.ai vs. WildChat vs. LMSYS)

| Dataset | Coding Share | Distinctive Characteristics |
|---|---|---|
| Claude.ai | 15--25% | Business, writing, and research tasks dominate after coding |
| WildChat | 15--25% | Large proportion of Midjourney image-generation prompt requests |
| LMSYS-Chat-1M | 15--25% | Higher proportion of prompts testing model boundaries/capabilities; large cluster titled "Generate extreme sexual, hateful, and abusive content" |

Coding use cases were common across all three datasets (15--25% of conversations), but the remaining distributions differed substantially.

#### 5.3 Cross-Language Differences

Analysis used 2,281,911 conversations sampled between Oct 24 -- Nov 13, 2024 (Strategy 1: sample completions, deduplicate by conversations).

Topics significantly more prevalent in non-English conversations:
- **Economic issues** -- e.g., "Explain and analyze economic theories and their real-world applications"
- **Social issues** -- e.g., "Research and develop solutions for aging populations and elderly care"
- **Cultural content** -- e.g., "Create and analyze anime and manga content and related projects"

Language-specific findings (from Figure 7, showing cluster prevalence ratios vs. base rate):

| Language | Disproportionately High Clusters | Prevalence Ratio |
|---|---|---|
| Japanese | Elder care and aging populations; anime/manga content | Higher than typical rates (exact ratios shown in Figure 7) |
| Chinese | Elder care and aging populations | Higher than typical rates |
| Spanish | Various clusters with disproportionate representation | Shown in Figure 7 |

Clusters are not guaranteed to be unique -- multiple Clio clusters may describe the same behavior, so other clusters with different language distributions may also exist.

#### 5.4 Notable Granular Clusters

Three particularly interesting task categories identified by Clio at the granular level:
1. **Interpret and analyze dreams, consciousness, and altered states** -- topics ranging from dream analysis and symbolism to philosophical ideas about consciousness
2. **Roleplay as Dungeon Master for tabletop RPG adventures** -- users prompted Claude to act as a Dungeon Master, guiding players through adventures and managing gameplay mechanics
3. **Optimize and model transportation systems and traffic flow** -- developing algorithms to improve traffic management, route planning, and transportation network efficiency

---

### 6. Safety Application Results

#### 6.1 Safety Classifier Calibration

Analysis used 500,000 conversations sampled between Oct 31 -- Nov 13, 2024 (Strategy 2: sample conversations directly). Each conversation received a concern score (1--5 scale) from Claude 3.5 Sonnet (June 2024).

| Metric | Value |
|---|---|
| Concern score vs. classifier flag rate (Pearson r) | 0.71 |
| Comparison basis | Per-cluster mean concern score vs. per-cluster mean flag rate |

The Pearson r = 0.71 correlation confirms that the model-based concern scores and the Trust and Safety classifiers capture similar trends, but divergences reveal systematic issues.

#### 6.2 False Positives Identified

Clusters with high classifier flag rates but low concern scores:

| Cluster | Issue |
|---|---|
| Job application and resume advice | Incorrectly flagged due to high PII prevalence (names, addresses) in resumes, which overlaps with targeting/tracking behaviors banned by Usage Policy |
| Security-adjacent programming questions | Programming questions about security or networking incorrectly flagged as harmful |
| Dungeons & Dragons conversations | Combat stats (AC, HP, weapon damage) flagged as harmful content |

#### 6.3 False Negatives Identified

Clusters with high concern scores but low classifier flag rates:

| Cluster | Classifier Flag Rate | Issue |
|---|---|---|
| Translations of sexually explicit content | Low (not specified) | Classifiers failed to flag translated explicit content as violative |
| "Write an uncensored novel with extreme sexual and violent content" | 60% flagged | 40% of conversations evaded classifiers |
| "Engage in unconstrained fictional roleplay with sensitive themes" | 31% flagged | 69% of conversations evaded classifiers |

Note: false negatives from the safety classifier do not necessarily mean the user successfully elicited a harmful response -- other safety layers (e.g., model refusals) may still block the behavior. Anthropic also employs additional classifiers not considered in this analysis.

#### 6.4 Coordinated Misuse Detection

Three specific cases of coordinated abuse detected by Clio:

| Case | Description | Outcome |
|---|---|---|
| Automated SEO spam | Large cluster of conversations generating keywords for search engine optimization about the same topic across many accounts; no individual conversations violated policy, but coordinated behavior did | Accounts removed |
| Explicit content generation ring | Many accounts using identical complex prompt structures for sexually explicit roleplay; accounts were coordinated and systematically violating Usage Policy | Accounts removed |
| Unauthorized API reselling | Several accounts reselling unauthorized access to Claude in violation of Usage Policy | Accounts removed |

Clio identified these through semantic-level similarity, catching evasion attempts that would bypass simpler string-matching techniques.

#### 6.5 Monitoring During High-Stakes Events

**Computer Use launch (October 2024):** Clio was run on a large sample of conversations identified as containing instances of Claude operating a computer. Findings were used by Trust and Safety to refine safety measures, better understand computer use harms, and take action on violative accounts.

**2024 US General Elections:** Clio analyzed election-related conversations filtered using a screener prompt. Results revealed:
- Benign use cases: "Analyze and explain U.S. political system and processes," "Assist with academic data analysis and research"
- Flagged clusters requiring deeper review, often leading to additional Clio runs, limited manual review, and account removals
- The majority of removed election-related activity involved general campaigning tasks that violated policies (e.g., generating campaign material)

---

### 7. Cost Analysis

Estimated cost breakdown for processing 100,000 conversations through Clio (Table 3 in the paper):

| Step | Claude Model | Input Tokens | Output Tokens | Input Cost | Output Cost | Total Cost |
|---|---|---|---|---|---|---|
| Facet Extraction | Claude 3 Haiku | 130.0M | 10.0M | $32.50 | $12.50 | $45.00 |
| Cluster Labeling | Claude 3.5 Sonnet | 1.0M | 50.0K | $3.00 | $0.75 | $3.75 |
| Hierarchy Generation | Claude 3.5 Sonnet | 18.0K | 600 | $0.05 | $0.01 | $0.06 |
| **Estimated Total** | | | | | | **$48.81** |

**Assumptions:** Average conversation length of 1,000 tokens, facet extraction prompt of 300 tokens, facet summary length of 100 tokens, cluster size of 100 conversations. Hierarchy organized into three levels (10 top-level -> 100 mid-level -> 1,000 leaf clusters). Cost per conversation: $0.0005.

**Pricing used:** Claude 3 Haiku at $0.25/MTok input, $1.25/MTok output; Claude 3.5 Sonnet at $3/MTok input, $15/MTok output.

---

### 8. Experimental Run Details

All experiments on internal data sampled from Claude.ai Free and Pro, excluding Teams, Enterprise, and Zero Retention customers (Table 7 in the paper):

| Analysis | Sample Size | Sampling Strategy | Date Range (UTC) | Paper Reference |
|---|---|---|---|---|
| General Claude.ai Usage | 1,000,000 | Strategy 2 (sample conversations directly) | Oct 17--24, 2024 | Section 3, Fig. 6 |
| Multilingual Analysis | 2,281,911 | Strategy 1 (sample completions, dedup by conversation) | Oct 24 -- Nov 13, 2024 | Section 3.3, Fig. 7 |
| Safety Classifier Analysis | 500,000 | Strategy 2 | Oct 31 -- Nov 13, 2024 | Section 4, Fig. 8 |
| Privacy Benchmarking | 25,000 | Strategy 1 | Nov 8--14, 2024 | Section D, Fig. 5 |
