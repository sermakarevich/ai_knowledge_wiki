> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Example use cases

**In one sentence:** The map groups TypeSafe fits into five capability categories (background automation, 150 ms real-time, 100×-cheaper big-data map-reduce, universal verification of other AIs, harness engineering) plus ~19 automation domains and a 10-row decision-shape table for turning ideas into code-owned workflows.

## Key points

- AI Automation Software means interleaving AI with reliable software runnable a million times in the background with no human co-pilot — code owns control flow (not markdown files) while TypeSafe handles semantic decisions and language understanding.
- Real-time applications use frontier intelligence at ~150 ms (faster than human perception) for games or UI-embedded decisions.
- AI Map Reduce over Big Data exploits ~100× cheaper inference to search, classify, and extract features over giant corpuses, agent traces, and datasets.
- Universal Verification checks prompts, extractions, reasoning traces, tool calls, or any other AI's inputs at a fraction of the LLM call cost — jailbreaks, citation errors, hallucinations, and other error modes.
- Harness Engineering uses Jev queries for model routing, semantic context retrieval, LLM error detection, guardrails, and reasoning-trace classification at lightspeed and a fraction of the cost.
- The automation list spans search/retrieval, scientific discovery, model routing, guardrails, semantic code linting, feature extraction, recruiting, lead gen, support, insurance, financial crime, legal/compliance, marketplaces, moderation, advertising, gaming, risk, forecasting, and knowledge graphs.
- The decision-shape table maps ten shapes (classification, detection, scoring, routing, search, retrieval, ranking, verification, ML feature extraction, structured extraction) to when to reach for each, e.g. routing when a category selects the next code path.
- Usage recipe: open the closest industry, scan the example decisions, and adapt them to the documents and actions in your own workflow.

---

## Example use case categories

| Category | Claim |
|---|---|
| AI Automation Software | Interleave AI with reliable software runnable a million times in the background without a human co-pilot; code owns control flow (not markdown files) while TypeSafe handles semantic decisions and language understanding. |
| Real-time applications | Frontier intelligence at real-time speeds (150 ms) — faster than human perception; programmable for games or embedded into a UI. |
| AI Map Reduce over Big Data | 100× cheaper means giant datasets are processable: search corpuses, classify agent traces, extract features for predictions. |
| Universal Verification | Verify input prompts, extractions, reasoning traces, tool calls, or any other AI's inputs; detect jailbreaks, citation errors, hallucinations, mistakes at a fraction of the LLM call cost. |
| Harness Engineering | Jev queries make harnesses smarter — model routing, semantic context retrieval, LLM error detection and guardrails, reasoning-trace classification at lightspeed and a fraction of the cost. |

## Example automation use cases

- **Search and retrieval:** replace/supplement RAG embeddings with semantic search, scoring, ranking; score query-to-candidate relevance; pairwise rerank; cross-encode queries and candidates; select useful downstream context.
- **Scientific discovery:** screen papers against inclusion/exclusion criteria; label transcript/survey/field-note passages with themes; check cited passages support manuscript claims; flag missing methods (controls, datasets, settings); link entities into research knowledge graphs.
- **Model routing:** custom router choosing which LLM gets each prompt; per-workflow rules/thresholds; intent/domain classification; difficulty/risk estimation; escalation to pricier models.
- **LLM guardrails:** semantic checks on every LLM input, output, and tool call at a fraction of the LLM cost; jailbreak/prompt-injection, policy-violation, sensitive-data, tool-call-error, and response-quality detection; structured logging for traceability.
- **Semantic code linting:** Jev queries as automated semantic lints for code and writing; team conventions as checks run in CI and flagged for review.
- **Feature extraction for predictive modeling:** probabilistic features from natural language combined with structured data for ground-truth tasks; autoresearch workflows propose and evaluate features on held-out truth.
- **Recruiting:** resumes/applications/feedback against explicit job criteria; experience, competencies, role match, routing, uncertain-case escalation.
- **Lead generation:** match profiles/bios/inbound to ideal customer profile; industry fit, maturity, buyer relevance, pain, intent; prioritize and route.
- **Customer support:** classify tickets by issue/product/intent; mine transcripts for issues/commitments/actions; urgency/frustration/churn/refund detection; routing; response-vs-policy verification.
- **Insurance claims:** classify first-notice-of-loss/adjuster notes; complexity, missing-info, fraud detection; straight-through vs specialist prioritization; uncertain/high-risk escalation.
- **Financial crime:** transaction-narrative/KYC/alert-history evaluation; entity matching across inconsistent records; alert prioritization by risk/relevance/evidence; ambiguous-case routing to investigators.
- **Legal and compliance:** classify contracts/policies/filings/marketing claims; missing-clause/prohibited-claim/violation detection; verification against explicit requirements; escalation to counsel.
- **E-commerce marketplaces:** listing classification/normalization across seller catalogs; attribute extraction; prohibited/counterfeit/review-abuse detection; ranking plus human review routing.
- **Moderation and trust & safety:** company-specific nuanced criteria; toxicity/harassment/spam/fraud/unsafe-advice/PII/opt-out detection; severity × confidence → allow/warn/review/block.
- **Advertising:** creative/copy/landing/placement evaluation; brand safety, audience suitability, regulatory compliance, creative quality, ad-to-page alignment.
- **Gaming:** player reports/chat/reviews/support evaluation; abuse/toxicity moderation; frustration/engagement scoring; churn detection and support routing.
- **Risk assessment:** reports/notes/descriptions into probabilistic risk indicators for insurance/underwriting; type classification, severity scoring, review prioritization, risk-model features.
- **Demand forecasting:** semantic signals (intent, urgency, interest, supply/competitive/demand themes) from inquiries/notes/reviews/tickets/reports fed with time-series into forecasting models.
- **Graphs and knowledge graphs:** typed semantic annotation/verification; relationship/entity classification; contradiction detection; probabilistic traversal and hierarchical classification.

## Example task categories

| Decision shape | Reach for it when | Examples |
|---|---|---|
| **Classification** | One known category should win | Intent, topic, department, risk type, entity type |
| **Detection** | You need a probability that one property is present | Spam, fraud, urgency, jailbreaks, sensitive data |
| **Scoring** | The answer belongs on an ordered rubric | Severity, relevance, quality, frustration, suitability |
| **Routing** | A category selects the next code path | Tool use, escalation, model routing, support queues |
| **Search** | You need to find items that match a natural-language query | Semantic search, document discovery, candidate generation |
| **Retrieval** | A workflow needs the most relevant context or records | RAG context, evidence retrieval, knowledge lookup |
| **Ranking** | Items need to be ordered by semantic relevance or quality | Search results, recommendations, candidate prioritization |
| **Verification** | An artifact must be checked for specific failure modes | Citation support, policy violations, tool-call errors, response quality |
| **ML Feature Extraction** | A downstream classical ML model needs semantic signals | Purchase intent, product interest, competitive pressure, churn signals |
| **Structured Data Extraction** | Known fields must be recovered from unstructured input | Candidate attributes, order fields, document labels |

**Covers:** Example use cases by industry and decision shape (source/topics/concepts_use-case-map.md)
