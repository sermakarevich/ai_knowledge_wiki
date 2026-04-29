> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Applications & Practical Implications

### 1. When to Use Clio-Like Systems (and When NOT To)

**Appropriate use cases:**

- **Post-deployment monitoring at scale.** Clio is designed for situations where millions of conversations need to be analyzed and manual review is infeasible. It excels at surfacing aggregate patterns and trends across large corpora of AI interactions.
- **Bottom-up discovery of unknown unknowns.** Unlike benchmarks or red-teaming that test for predefined threats, Clio enables exploratory search where analysts start with broad questions and iteratively discover patterns they did not anticipate.
- **Complementing top-down safety approaches.** Pre-deployment evaluations (red-teaming, benchmarks) inherently can only test for issues that have been thought of in advance. Clio fills the gap by providing empirical, data-driven observation of what actually happens in production.
- **Cross-language usage analysis.** Clio maintains above 92% reconstruction accuracy across 15 tested languages, making it suitable for understanding how multilingual communities use AI differently.

**Inappropriate or insufficient use cases:**

- **Detecting rare, one-off misuse events.** Clio identifies patterns across many conversations. A single instance of extreme misuse (however consequential) will not form a cluster and will escape detection. Clio is fundamentally a statistical tool, not a per-conversation monitor.
- **Automated enforcement.** The authors explicitly state that they do not take automated enforcement actions based solely on Clio clusters. The system's outputs are "preliminary and require additional validation before being used as the basis for decision-making." Human review of flagged clusters is required before any account-level action.
- **Capturing user intent.** Clio analyzes conversational content and can infer topics, but it cannot definitively determine what a user actually intended, especially when intent is encoded subtly across multiple sessions or differs from how the user presents it.
- **Measuring downstream real-world impact.** Clio only analyzes what happens within conversations. It cannot observe whether a user actually acted on advice received, whether generated code was deployed, or what societal effects resulted from a conversation.
- **Formal privacy guarantees.** Because Clio produces rich textual descriptions rather than numerical outputs, formal guarantees like differential privacy or k-anonymity cannot be directly applied. The system relies on empirically validated, layered defenses rather than mathematical proof.

---

### 2. Real-World Applications Described in the Paper

#### 2.1 Understanding Broad Usage Patterns

Clio was run on one million Claude.ai Free and Pro conversations to produce the first large-scale, in-depth analysis of direct traffic on a major AI assistant. Key findings:

- **Top use cases:** Coding-related tasks dominate, with "Web and mobile application development" alone accounting for over 10% of all conversations. Writing, research, and educational use cases each comprise 6--10%. Business data analysis and professional email drafting are also prominent.
- **Granular clusters:** Beyond high-level categories, Clio surfaced thousands of fine-grained clusters, including "Interpret and analyze dreams, consciousness, and altered states," "Roleplay as Dungeon Master for tabletop RPG adventures," and "Optimize and model transportation systems and traffic flow."
- **Cross-language variation:** Japanese and Chinese conversations disproportionately discuss elder care and aging populations. Non-English conversations are more likely to involve economic theories, social issues, and anime/manga content creation. These findings demonstrate that AI usage is not culturally uniform and that safety and product decisions should account for linguistic community differences.

#### 2.2 Safety Monitoring

Clio was deployed for three distinct safety purposes:

1. **Identifying patterns of violative behavior** (coordinated misuse invisible at the single-conversation level). See detailed case studies below.
2. **Monitoring for unknown unknowns during high-stakes periods** (new capability launches and major world events).
3. **Calibrating safety classifiers** (finding false positives and false negatives in existing automated safety systems).

#### 2.3 Classifier Calibration

Clio was used to systematically evaluate Anthropic's safety classifiers against a model-generated "concern score" (1--5 scale, Spearman r = 0.71 with classifier flag rates). By examining clusters where these two signals diverge, Clio identified:

**False positives (classifier over-triggers):**
- Job application and resume advice -- flagged due to high PII density, which pattern-matches behaviors banned by the Usage Policy.
- Security-adjacent programming questions -- networking and security topics incorrectly flagged as harmful.
- Dungeons & Dragons combat stats -- character sheets with damage descriptions ("4-24+4 slashing + 2-12 fire") triggered violence classifiers.

**False negatives (classifier under-triggers):**
- Translations of sexually explicit content often evaded classifiers, despite violating the Usage Policy.
- A cluster titled "write an uncensored novel with extreme sexual and violent content" was only flagged by classifiers 60% of the time.
- A cluster titled "engage in unconstrained fictional roleplay with sensitive themes" was only flagged 31% of the time.

These findings directly feed back into classifier improvement, creating a continuous refinement loop.

#### 2.4 Election Monitoring (2024 US General Elections)

In the months preceding the 2024 US elections, Clio was used to monitor Claude.ai traffic for election-related risks. The process:

1. Claude screened conversations for relevance to U.S. politics, voting, and democratic participation.
2. Clio clustered the resulting conversations.
3. Trust and Safety team members reviewed clusters to identify emerging or unknown harms.

Results were mixed: most election-related activity was benign (e.g., "Analyze and explain U.S. political system and processes," "Assist with academic data analysis and research"), but some clusters were flagged for deeper review. The majority of removed election-related activity involved general campaigning tasks that violated Anthropic's policies, such as generating campaign material.

#### 2.5 New Capability Launch Monitoring (Computer Use)

After launching the refreshed Claude 3.5 Sonnet with computer-use capabilities in October 2024, Anthropic used Clio to monitor a large sample of conversations where Claude was identified as operating a computer. Despite pre-launch red-teaming, this monitoring was motivated by the impossibility of anticipating all potential risks for a novel capability. Trust and Safety used the results to refine safety measures, better understand computer-use-specific harms, and take action on violative accounts.

---

### 3. Case Studies of Misuse Detection

These three cases illustrate Clio's core strength: detecting coordinated abuse that is invisible at the individual conversation level.

#### 3.1 SEO Spam Network

**What Clio found:** A large cluster of conversations where Claude was asked to generate keywords for search engine optimization, all about the same topic, across many different accounts.

**Why it mattered:** No individual conversation violated the Usage Policy -- each was a normal-looking SEO request. Only the cross-account pattern revealed coordination.

**What evaded simpler tools:** The accounts used formats that would have evaded string-matching techniques. Clio's semantic clustering grouped them by meaning rather than exact phrasing.

**Action taken:** After investigation, accounts were determined to be engaged in coordinated abuse and were removed from the system.

#### 3.2 Explicit Content Generation Ring

**What Clio found:** A large cluster of conversations from many different accounts using an identical complex prompt structure to engage Claude in sexually explicit role-play.

**Why it mattered:** While the Usage Policy prohibits sexually explicit content, Anthropic generally does not off-board accounts for a single violation. These accounts were removed specifically because of their coordinated behavior -- systematic, multi-account orchestration rather than isolated incidents.

**Key nuance:** The enforcement action was based on the coordination pattern, not the content per se. This demonstrates Clio's value for detecting organized misuse campaigns.

#### 3.3 Unauthorized Reselling of Access

**What Clio found:** A large volume of traffic from several accounts whose usage patterns suggested violations of certain policies.

**Investigation outcome:** The accounts were reselling unauthorized access to Claude, violating the Usage Policy.

**Action taken:** Violative accounts were removed.

**Common thread across all three cases:** Clio targets semantic similarity, enabling it to catch abuse that uses varied surface-level phrasing but shares underlying intent. In all cases, suspicious clusters were first identified by Clio, then reviewed by authorized Trust and Safety team members in a secure environment under strict privacy controls before any enforcement action was taken.

---

### 4. Practical Limitations and Failure Modes

#### 4.1 Operational Limitations (Potentially Fixable)

These arise from imperfections in each pipeline stage and could improve as models and techniques advance:

| Pipeline Stage | Failure Mode |
|---|---|
| **Facet extraction** | Hallucination, misinterpretation of slang or sarcasm, missing implicit information, failure to capture new developments |
| **Semantic clustering** | Suboptimal groupings for conversations that span multiple categories or represent rare outlier topics; k-means assumes roughly spherical clusters |
| **Cluster labeling** | Overly broad labels that obscure important subtopics; labels that overemphasize certain within-cluster topics |
| **Hierarchization** | Oversimplified relationships between topics; incorrect placement of clusters within the hierarchy |

The main failure mode for conversation summarization identified in manual review was long, multi-topic conversations where the summary omitted some user requests (the model tended to focus on more harmful requests when present).

#### 4.2 Fundamental Limitations (Inherent to Design)

1. **Inability to fully capture intent.** Misuse can be encoded subtly across multiple requests to different models, or a user's true intent may differ from what they present.
2. **Limited to conversational data.** No visibility into real-world downstream actions or societal effects.
3. **Privacy vs. granularity trade-off.** Robust privacy measures inherently limit the detail that can be extracted. Some potentially important clusters -- including discussions about specific public figures or small organizations -- may be filtered out.
4. **Model-specific insights.** Findings from Claude.ai may not generalize to other AI systems with different capabilities, user bases, and use patterns.
5. **Inability to detect rare events.** Clio only surfaces patterns across many conversations. A single catastrophic misuse event will not form a cluster.
6. **Cannot prove absence of harm.** Pipeline imperfections or adversarial actions could allow harmful behavior to escape detection. Clio should never be treated as a comprehensive audit.

---

### 5. Privacy Risks and Mitigation Strategies

#### 5.1 The Four-Layer Privacy Defense

Clio employs defense in depth rather than formal privacy guarantees:

1. **Conversation summary step.** The model is prompted to answer summarization questions while omitting any private information and all proper nouns.
2. **Cluster aggregation thresholds.** Clusters must exceed minimum size requirements for both unique accounts and conversations. Single-user or small-group clusters are discarded.
3. **Cluster summary step.** When generating cluster-level summaries, the model is again instructed not to include private information.
4. **Cluster auditing.** A separate model reads cluster summaries and removes any that contain private information (auditor achieves 98% accuracy on a curated hard test set).

**Empirical validation:** In a 5,000-conversation audit, raw conversations contained ~10% private information (rated 1--2 on a 5-point privacy scale). After summarization, this dropped to ~1.5%. After cluster summarization, no clusters were rated below 4 (i.e., zero detectable private information in final outputs).

#### 5.2 Residual Privacy Risks

- **Correlated failures across layers.** If the same type of PII consistently survives summarization, it might also survive cluster summarization. Layered defenses reduce but cannot eliminate correlated failure modes.
- **Group privacy violations.** Aggregated data could reveal sensitive information about specific communities (e.g., a small religious group's distinctive patterns) without revealing any individual. This is an area of acknowledged but not fully resolved risk.
- **Unforeseen forms of privacy infringement.** The privacy scale and auditor are designed for known categories of private information. Novel or indirect identifiers may not be caught.

#### 5.3 Mitigation Approach

- Regular privacy audits and evaluations.
- Continuous model upgrades (using the latest Claude models to improve privacy safeguards).
- Data minimization: only conversation summaries (not full conversations) are retained in Clio's pipeline.
- Clio does not support analysis based on geography.
- Strict aggregation and access controls throughout.

---

### 6. Risks of Misuse of the System Itself

The paper explicitly acknowledges that Clio-like systems could be turned to harmful purposes:

- **Surveillance and civil liberties.** Any tool that provides insights into how people use technology could potentially be repurposed for surveillance. The paper notes this risk directly: "a potential risk is misuse in ways that interfere with privacy or civil liberties."
- **False positive enforcement at scale.** If Clio's clusters were used for automated enforcement (which Anthropic explicitly does not do), innocent users could be swept up in false positive clusters. The paper notes the specific risk: "If particular clusters are flagged as problematic and that signal is used to automatically ban or restrict accounts, some non-violating users might be included."

**Mitigations described:**
- Strict access controls, data minimization, and retention policies within Clio and across Anthropic.
- No automated enforcement based solely on Clio clusters.
- Only a small number of authorized staff can view safety-focused Clio results.
- Safety-focused runs that link back to individual accounts have strict access controls.
- Multilingual performance evaluations to ensure fairness across language groups (Table 5 in the paper).

---

### 7. User Trust Implications

The paper identifies a core tension: the mere existence of a system like Clio -- even with strong privacy protections -- might be perceived as invasive and could erode user trust in AI assistants.

**The authors' approach to this tension:**

1. **Radical transparency.** Publishing the paper itself is framed as a deliberate trust-building measure. The alternative -- building such a system and not disclosing it -- is presented as worse for trust.
2. **Public good framing.** Usage data insights (e.g., the top-10 use case breakdown in Figure 6) are shared publicly despite being commercially sensitive, because "it is in the best interest of society to know how AI systems are being used in the world."
3. **Civil society engagement.** Feedback from privacy, safety, and civil liberties experts shaped multiple aspects of the system, including expanded multilingual validation methods, clarified privacy mechanisms, and identification of priority research areas.
4. **Commitment to ongoing disclosure.** The authors state plans to share further Clio insights and contribute to a culture of empirical transparency.

**Unresolved tension:** The paper's justification rests on the argument that the pro-social benefits (safety improvements, public knowledge about AI use, governance insights) outweigh the risks. This is a value judgment that not all stakeholders will share. Users who consider any analysis of their conversations invasive may not be persuaded by aggregate-level privacy protections.

---

### 8. Future Directions and Open Problems

The paper identifies several areas for further work, both explicitly and implicitly:

**Explicitly stated:**
- **Comprehensive cross-lingual analysis.** The multilingual findings are preliminary; a deeper investigation of how different linguistic communities use Claude is flagged as "an important direction for future work."
- **Continuous model improvement for privacy.** Using the latest Claude models in Clio to improve the performance of privacy safeguards over time.
- **Ongoing public disclosures.** The authors commit to sharing further Clio insights to support empirical transparency in AI governance.

**Implicitly raised by the paper's limitations:**
- **Formal privacy guarantees for textual outputs.** The paper acknowledges the difficulty of applying differential privacy to rich textual descriptions. Developing methods that provide formal guarantees while preserving the richness of Clio's outputs is an open research problem.
- **Group privacy protections.** Preventing aggregated patterns from revealing sensitive information about specific communities, without overly restricting the system's analytical power.
- **Intent detection.** Moving beyond content analysis to understand user intent would significantly strengthen Clio's safety value but raises even more difficult privacy and ethical questions.
- **Cross-platform generalizability.** Clio's findings are specific to Claude.ai. Whether similar systems at other providers would reveal consistent or divergent patterns remains unknown.
- **Rare event detection.** Complementary methods are needed for catching the low-frequency, high-consequence misuse events that Clio by design cannot surface.
- **Adversarial robustness.** Sophisticated actors who understand Clio's clustering methodology could potentially craft prompts that evade semantic grouping. The paper does not extensively discuss adversarial attacks on the pipeline itself.
- **Temporal dynamics.** While Clio supports temporal breakdowns in its interface, the paper does not deeply explore how usage patterns evolve over time or how quickly Clio can detect emerging threats.

---

### 9. Broader Implications for AI Governance and Transparency

#### 9.1 Clio as a Governance Tool

The paper positions Clio as a bridge between top-down AI governance frameworks and bottom-up empirical observation. Most existing governance frameworks (Jobin et al. 2019, Weidinger et al. 2021, 2022, Gabriel et al. 2024) "typically identify risks or provide guidelines for responsible AI development and deployment, but often lack empirical grounding in real-world usage patterns." Clio provides the empirical grounding that these frameworks need.

#### 9.2 The Case for Empirical Transparency

The paper makes an argument for a new norm in the AI industry: model providers should systematically analyze and publicly share aggregate usage data, even when doing so is commercially disadvantageous. This is framed as analogous to how Google Trends provides aggregate insights about web search behavior -- a comparison the paper returns to repeatedly.

The argument is that the public interest in understanding how AI systems are being used outweighs providers' competitive interests in keeping usage data private. By publishing commercially sensitive data (like the top use case breakdown), Anthropic is trying to establish a precedent.

#### 9.3 Post-Deployment Monitoring as Essential Complement

The paper argues that pre-deployment testing (red-teaming, benchmarks, evaluations) is necessary but fundamentally insufficient: it "can only test for issues we think to look for." Post-deployment monitoring provides the empirical complement by surfacing "real-world usage patterns and risks that may not be captured by predetermined scenarios -- insights that can in turn inform future pre-deployment tests and safeguards." This creates a feedback loop where production observations improve future pre-deployment assessments.

#### 9.4 The Technology is Not Novel -- The Application Is

The authors note that the underlying technologies (clustering, embedding, summarization, visualization) are not new. Similar embed-cluster-summarize systems have been applied to general text data (Nomic 2024, Lam et al. 2024). The distinctive contribution is applying these techniques to AI assistant conversations at production scale with a layered privacy-preservation approach. This means other model providers could build similar systems using existing methods -- the barrier is not technical but organizational and ethical.

#### 9.5 Dovetailing with Industry-Wide Efforts

Clio complements abuse disclosures from other providers (e.g., OpenAI's covert influence operations report, Nimmo 2024) and responds to civil society calls for greater transparency into AI usage data (Nicholas 2024). The paper explicitly frames Clio as contributing to an "emerging culture of empirical transparency" rather than a standalone initiative.

#### 9.6 The Cost Question

A full Clio run on 100,000 conversations costs approximately $48.81 ($0.0005 per conversation), making it affordable even at large scale. This low cost means the barrier to deploying similar systems is not economic -- it is primarily one of institutional will, privacy engineering, and governance design. The affordability also means that smaller AI providers, not just well-resourced labs, could implement similar monitoring.
