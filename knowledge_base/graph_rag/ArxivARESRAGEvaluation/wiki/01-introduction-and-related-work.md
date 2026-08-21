> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction & Related Work

**In one sentence:** RAG evaluation is hard because it traditionally demands expensive, domain-specific human annotations (or fixed, unadaptable heuristic prompts), whereas ARES sidesteps both by fine-tuning lightweight LLM judges on self-generated synthetic data and correcting their predictions with a small human-annotated set via prediction-powered inference, yielding statistically guaranteed, low-annotation evaluation that substantially exceeds RAGAS.

## Key points

- ARES evaluates RAG systems along exactly three dimensions — context relevance, answer faithfulness, and answer relevance — and reports them as three separate scores computed by three distinct judge models.
- ARES is presented as the first automated RAG evaluation system to generate tailored LLM judges for each component of the RAG pipeline, achieving large precision and accuracy gains over existing approaches like RAGAS.
- ARES's human effort is sharply bounded: it needs an in-domain passage set, a human preference validation set of ~150 annotated datapoints or more, and only a few (e.g., five or more) in-domain few-shot query/answer examples — requiring 78% fewer annotations than the annotation-based baseline.
- On the six knowledge-intensive KILT and SuperGLUE datasets, ARES beats RAGAS by an average of 59.3 percentage points on context relevance evaluation accuracy and 14.4 points on answer relevance accuracy.
- ARES also accurately estimates answer hallucination rates on the AIS attribution dataset (Rashkin et al., 2022), predicting within 2.5 percentage points of the ground-truth average hallucination rate.
- Prediction-powered inference (PPI; Angelopoulos et al. 2023) is the mechanism that both corrects the lightweight judges' prediction errors and supplies statistical confidence intervals for ARES's RAG scores — a property the paper emphasizes prior systems lack.
- The two most-related prior works, EXAM and RAGAS, are directly contrasted: EXAM requires each query to carry associated sub-questions (a burden ARES avoids), and RAGAS's handful of heuristic hand-written prompts offer little adaptability to new corpora and substantially underperform ARES.
- A judge's generality is a feature, not just a component-level gain: ARES judges remain effective across domain shifts, staying accurate even after the query and/or document types in the evaluated RAG systems change.

---

## The RAG evaluation problem

Retrieval-augmented generation has become a dominant way to build user-facing NLP applications such as question answering, fact-checking, and customer support. The core idea is to combine an LLM with a retrieval system so the model can gather domain-specific knowledge, ground its generation in factual information, and even offer a degree of transparency or interpretability by citing sources (Lewis et al., 2020; Khattab et al., 2021; Izacard et al., 2022). A given RAG system is typically a retriever plus a downstream LM: the retriever finds relevant passages from a corpus and the LM uses them to generate the answer.

The design space around that skeleton is wide, however. Even the simplest choices — what retrieval model to use, how to divide the corpus into retrieval chunks, and how to prompt or fine-tune the LM to leverage retrieved information — are non-trivial. The "best" design is not universal: it shifts with data domain, corpus size, and cost/latency budget. That is precisely what makes evaluation hard — there is no single, domain-agnostic reference point to compare systems against.

Traditionally, tuning a RAG system therefore requires hand annotations in the target domain: test questions, passages to retrieve (to score the retriever), and responses to generate (to score the LM). A practitioner can alternatively A/B-test candidate systems in production by collecting human preference comparisons. Both routes are costly and expertise-heavy.

The cheap alternative — model-based evaluation (Zheng et al., 2023) — already exists in the open-source RAGAS framework (James and Es, 2023), which prompts an LM to judge the relevance of retrieved information and the faithfulness/accuracy of the generated response. But such strategies rely on a fixed set of heuristically hand-written prompts, offering little adaptability to different evaluation contexts and no guarantees about quality.

## ARES: the proposed framework

To close this gap, the paper introduces ARES (Automated RAG Evaluation System, Saad-Falcon et al., NAACL 2024). ARES is positioned as the first automated RAG evaluator to generate *tailored* LLM judges for each pipeline component, and — unlike prior systems — to provide *confidence intervals* through prediction-powered inference (PPI; Angelopoulos et al. 2023), a technique that converts a small set of human annotations into statistically valid scoring.

Operationally, ARES requires only three inputs: an in-domain passage set, a human preference validation set of approximately 150 annotated (positive + negative) datapoints covering all three dimensions, and a handful of in-domain few-shot query/answer examples, which it uses for prompting the LM in synthetic data generation. The authors designate this small annotated set as the human preference validation set, composed of positive and negative examples for each of context relevance, answer faithfulness, and answer relevance. From the passages ARES: (1) builds a synthetic question–answer dataset by prompting an LM; (2) fine-tunes three lightweight judge models — one for each classification task (context relevance, answer faithfulness, answer relevance) — against a contrastive-learning objective; and (3) scores the candidate RAG systems using PPI, which both boosts the accuracy of the model-based evaluation and yields confidence intervals by correcting the judges' residual prediction errors. In this framing, a good RAG system finds relevant contexts and generates answers that are both faithful and relevant.

The empirical results are strong: across the six KILT and SuperGLUE knowledge-intensive datasets, ARES wins over RAGAS by 59.3 and 14.4 percentage points (average) on context relevance and answer relevance accuracy; on AIS it estimates the average hallucination rate within 2.5 percentage points of ground truth; and it is 78% more annotation-efficient than the annotation-based baseline. The paper also notes that ARES can separate RAG systems whose true metrics are only a few points apart — the precision needed to guide configuration choices — and that ARES judges stay effective across domain shifts (changing query and/or document types). The code and datasets are released on GitHub.

## Related evaluation frameworks

Multiple LLM-based evaluation techniques have emerged to gauge LLM systems, which the paper says is essential for rapid deployment in new settings where building a traditional benchmark dataset from scratch is difficult. Early attempts used LLMs out of the box as judges, as in MT-Bench and Chatbot Arena (Zheng et al., 2023). AutoCalibrate (Liu et al., 2023b) seeks to align an LLM judge with human preferences with a self-refinement prompt, but — a point the paper singles out — offers no statistical guarantees for the accuracy of its predictions, which ARES's PPI step does provide.

Other work has used LLM prompting to evaluate system quality across natural-language generation tasks such as translation, summarization, and dialogue (Kocmi and Federmann, 2023; Fu et al., 2023; Liu et al., 2023a; Wang et al., 2023). In the context of knowledge-intensive NLP tasks, LLMs have been explored for assessing attribution and factuality (Min et al., 2023; Gekhman et al., 2023; Yue et al., 2023), and new guidelines like LongEval (Krishna et al., 2023) plus datasets like Hagrid (Kamalloo et al., 2023) and ALCE (Gao et al., 2023) provide resources for analyzing knowledge-intensive LLM pipelines. None of these, however, is an end-to-end evaluator of a full RAG system that also returns statistically valid scores.

Two systems are identified as most closely related. EXAM (Sander and Dietz, 2021) gauges a response by estimating how many exam-style sub-questions a simulated QA reader can answer from it; doing this requires every query to come bundled with a set of associated sub-questions, "a burden that ARES does not bring." RAGAS (James and Es, 2023) relies on a handful of hand-written heuristic prompts, which the paper says offers little adaptability to new RAG evaluation settings (e.g., new corpora) and, per ARES's own evaluation, substantially underperforms ARES.

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Work) — arXiv 2311.09476, pages 1-3
