---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Why Neighborhoods Matter

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. Why does the paper argue that citation faithfulness should be treated as a "trajectory-level" problem in Agentic GraphRAG, rather than as a property of the final answer and its citations?

> [!tip]- Answer
> Because an agentic system autonomously traverses far more of the knowledge graph than it ends up citing — it inspects neighboring entities, relation patterns, and community structure along the way. If that broader traversal shapes the answer, then judging faithfulness only by whether the cited entities support the answer ignores the rest of the trajectory that may also have contributed. See [[wiki/01-introduction-and-motivation|Introduction and Motivation]].

### Q2. What are the three graph-ablation studies in this paper, and what question does each one test (necessity, sufficiency, or completeness of citations)?

> [!tip]- Answer
> (1) Cited Evidence Ablation removes cited entities (vs. a random-removal control) to test *necessity*. (2) Isolation restricts the system to only cited entities (full isolation) or cited-plus-structure (text-only isolation) to test *sufficiency*. (3) Visited-but-uncited Ablation removes or text-masks entities the agent visited but didn't cite, to test whether uncited navigational context matters. See [[wiki/02-experimental-design-and-studies|Experimental Design and Studies]].

### Q3. In the baseline experiment (Table 1), roughly how many entities do agentic GraphRAG systems visit versus cite, and why does this gap matter for the paper's argument?

> [!tip]- Answer
> Agentic systems visit roughly 10-12 entities on average but cite only about 2 (e.g., Agentic GraphRAG: 11.9 visited vs. 1.9 cited). This gap matters because it is the empirical basis for the paper's core worry: if the agent's real evidence trail is 5-6x larger than its citation list, the citation list alone likely understates what actually shaped the answer. See [[wiki/03-results-and-discussion|Results and Discussion]].

### Q4. Why does the paper compare "cited entity removal" against "random entity removal" of the same size, instead of just measuring the accuracy drop from cited removal alone?

> [!tip]- Answer
> Removing any entities from a knowledge graph will degrade a system's performance somewhat just from losing information. Without a control, a drop after removing cited entities wouldn't prove those entities were specifically important — it might just reflect generic graph damage. Comparing against a matched-size random removal (which shows little or no drop, and sometimes even a rise) isolates the specific importance of the *cited* entities from the generic effect of node removal. See [[wiki/02-experimental-design-and-studies|Experimental Design and Studies]] and [[wiki/03-results-and-discussion|Results and Discussion]].

### Q5. What does it mean that "text-only isolation" recovers more accuracy than "full isolation," and what does this imply about the role of visited-but-uncited entities?

> [!tip]- Answer
> Full isolation removes non-cited entities entirely from the graph; text-only isolation keeps those entities' presence and connectivity in the graph structure but blocks reading their attached text. Since text-only isolation performs better (e.g., GraphRAG: 60.0% vs. 48.0%), the mere structural presence and position of uncited entities — even without their text content — helps the agent navigate and constrain its search. This implies visited-but-uncited entities do real work as *neighborhood context*, not just as potential extra text sources. See [[wiki/03-results-and-discussion|Results and Discussion]].

### Q6. How would you summarize, in one sentence, what "cited entities are necessary but not sufficient" means for someone designing a citation UI for an agentic RAG product?

> [!tip]- Answer
> It means showing users only the final cited sources creates an illusion of complete transparency — the citations are genuinely important (removing them breaks the answer), but they don't contain everything the system used, so a fully honest provenance UI would also need to expose or log the broader traversal trajectory. See [[wiki/04-conclusion-and-limitations|Conclusion and Limitations]].

### Q7. If you wanted to apply this paper's ablation methodology to an agentic RAG system that retrieves from a vector database instead of a knowledge graph, what would need to change?

> [!tip]- Answer
> You would need a way to distinguish "chunks retrieved and considered" from "chunks the answer ultimately cited" (analogous to visited vs. cited entities), then run matched interventions: remove cited chunks vs. randomly removed retrieved-but-uncited chunks, restrict the model to only cited chunks, and remove/mask retrieved-but-uncited chunks. The graph-specific structural argument (position/connectivity mattering, shown via text-only isolation) would need rethinking, since vector retrieval lacks explicit graph connectivity — the closest analogue might be embedding-space proximity or shared-topic clustering. See [[wiki/02-experimental-design-and-studies|Experimental Design and Studies]].

### Q8. The paper's critical analysis flags the 30-question benchmark and single LLM backbone as limitations. Why does this matter for how much weight you should put on the specific accuracy percentages reported (e.g., 76.0% → 36.0%)?

> [!tip]- Answer
> With only 25 non-trivial questions per condition and no reported confidence intervals, a single question flipping correctness moves the reported accuracy by 4 percentage points — so precise numbers carry real sampling noise. The qualitative direction (cited removal hurts far more than random removal; full isolation still hurts) is consistent enough across four different systems to be credible, but the exact magnitudes and cross-system rankings shouldn't be treated as precise estimates that would hold on a larger or different benchmark. See [[critical_thinking|Critical Analysis]].
