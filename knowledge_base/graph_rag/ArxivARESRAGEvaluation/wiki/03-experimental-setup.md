> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental Setup

**In one sentence:** ARES is evaluated by ranking a battery of mock and real RAG systems built over KILT and SuperGLUE datasets — using a FLAN-T5 XXL synthetic data generator, a DeBERTa-v3-Large fine-tuned judge, gpt-3.5-turbo few-shot baselines, and RAGAS 0.0.18 — to test its ability to score and rank RAG outputs across small accuracy margins.

## Key points

- ARES generates its synthetic judge-training data with FLAN-T5 XXL and uses a fine-tuned DeBERTa-v3-Large as its LLM judge, so RAG systems can be ranked with few-shot prompts on commercial GPUs rather than external APIs.
- The in-context learning baseline uses OpenAI gpt-3.5-turbo-16k (version 10/23) in a zero/few-shot setting.
- Similarity search over in-domain passages is done with FAISS IndexFlatL2 indexing plus OpenAI text-embedding-ada-002 embeddings; it filters out synthetic queries that cannot retrieve the passage from which they were generated.
- RAGAS version 0.0.18 is the external RAG-evaluation baseline used in the experiments.
- All KILT datasets suitable for RAG are used: Natural Questions (NQ), HotpotQA, FEVER, and Wizards of Wikipedia (WoW), each drawing on Wikipedia passages but covering short-answer QA, multi-hop reasoning, fact-verification, and dialogue retrieval respectively.
- From SuperGLUE, MultiRC (direct questions across seven domains) and ReCoRD (placeholder-entity prediction over CNN/Daily Mail news) are used, with open-domain retrieval versions of both tasks.
- Answer faithfulness is not scored on KILT/SuperGLUE because there are no human-annotated hallucinated answers; ARES is instead tested on real attribution datasets in Section 5.2.
- Nine mock RAG systems are created from validation splits ranging from 70% to 90% success rate in 2.5% increments, giving known ground-truth rankings to measure ARES's scoring and ranking accuracy.

---

## Models

For the fine-tuned judges, ARES relies on generating cheap but high-quality synthetic queries and answers using LLMs. FLAN-T5 XXL (Chung et al., 2022) is used to generate the synthetic datasets. DeBERTa-v3-Large (He et al., 2021) is selected as the fine-tuned LLM judge. The design lets ARES rank RAG systems without relying on external APIs, solely using few-shot prompts and deployable LLMs running on commercial GPUs.

The in-context learning baseline uses OpenAI's gpt-3.5-turbo-16k (version 10/23, Brown et al., 2020) in a zero/few-shot setting. For similarity search over in-domain passages, FAISS IndexFlatL2 (Johnson et al., 2019) provides indexing and OpenAI's text-embedding-ada-002 generates the embeddings. This similarity search is also used to filter synthetic queries that cannot retrieve the passage from which they were generated. RAGAS version 0.0.18 (James and Es, 2023) is the external framework benchmarked against.

## Datasets

The experimental goal is to show where ARES can be applied effectively across multiple types of queries, documents, and answers, so all RAG-appropriate datasets from the KILT and SuperGLUE benchmarks are included.

**KILT (Petroni et al., 2021).** Natural Questions (NQ), HotpotQA, FEVER, and Wizards of Wikipedia (WoW) (Kwiatkowski et al., 2019; Yang et al., 2018; Akhtar et al., 2023; Dinan et al., 2018) all use Wikipedia passages but target different applications. NQ and HotpotQA feature direct questions expecting short answers; NQ reasons over single passages while HotpotQA requires multiple. FEVER is fact-verification, deciding whether a passage "SUPPORTS" or "REFUTES" a statement. WoW maps user dialogue to relevant Wikipedia passages before a chatbot generates a paragraph-length response.

**SuperGLUE (Wang et al., 2019).** MultiRC (Khashabi et al., 2018) uses direct questions over seven domains: News, Wikipedia articles, society/law/justice articles, history/anthropology articles, elementary school science textbooks, 9/11 reports, and fiction. ReCoRD (Zhang et al., 2018) involves identifying a placeholder entity in a statement over CNN and Daily Mail news articles. Open-domain versions of both tasks are created: retrieval runs over MultiRC's seven domain passage sets and over ReCoRD's news article passages.

**Mock RAG systems.** To test ARES's ranking ability, mock systems separated by small accuracy margins are built from artificial query-passage-answer triples whose positive and negative examples (for both context relevance and answer relevance) are empirically known. Positive triples use unaltered KILT/SuperGLUE examples; negative query-passage pairs and query-passage-answer triples are sampled from the same Wikipedia document or a random one (Table 7 shows examples). From each KILT and SuperGLUE validation subset, nine splits are created with success rates of 70% to 90% in 2.5% steps (70.0%, ..., 90.0%), each split representing one mock RAG system with a known correct ranking — enabling ARES to be measured on both scoring and ranking across the three evaluation criteria. Answer faithfulness is excluded from KILT/SuperGLUE (no human-annotated hallucinated answers); attribution datasets are covered in Section 5.2.

## Metrics

The correlation between the correct ranking and ARES's ranking is captured by Kendall's rank correlation coefficient (Kendall's τ) = (# concordant pairs − # discordant pairs) / # total pairs, where concordant pairs are two ordinal values with the earlier one lower than the later one and discordant pairs are those with the earlier one greater or equal. A Kendall's τ greater than 0.9 is treated as successful (range 0.0–1.0).

Kendall's τ is chosen because developers compare RAG configurations through pairwise comparisons of model choice, retriever selection, and document preprocessing, and τ is explicitly designed to measure the accuracy of such pairwise comparisons across a range of performance gaps — a standard metric in information retrieval. Together with prediction accuracy it forms the evaluation criterion for ARES as a RAG evaluation system.

**Covers:** Section 4 "Experiments" (4.1-4.3) — arXiv 2311.09476, pages 5-6
