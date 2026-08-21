> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# RQ1: Existing Attacks Fail Under GraphRAG

**In one sentence:** Conventional RAG poisoning attacks (represented by POISONEDRAG) are measurably less effective against graph-based RAG systems (GraphRAG and LightRAG) because GraphRAG's indexing pipeline — LLM-based extraction and merging of entity/relation descriptions — inherently filters, omits, or counteracts the injected poisoning text, motivating the need for the new GRAGPOISON attack.

## Key points

- Attack success rate (ASR) is defined as ASR = (1/|X|) · Σ_{(x,y)∈X} 1[ŷ ≠ y], i.e. the fraction of target queries for which the attacked system returns an answer different from the correct one, with |X| the number of target queries and 1p an indicator returning 1 if p is true and 0 otherwise.
- The systems evaluated are NaiveRAG as the conventional RAG baseline, and GraphRAG and LightRAG as the graph-based implementations, with GPT-4o-mini as the underlying LLM for GraphRAG and LightRAG.
- The representative poisoning attack POISONEDRAG generates poisoning text for each query by directly providing an incorrect answer by concatenating the query subject to a wrong response.
- POISONEDRAG's performance degrades on both GraphRAG and LightRAG compared to NaiveRAG across all settings; on the Geographical dataset the ASR against NaiveRAG is over 10% higher than against GraphRAG or LightRAG.
- Concrete example: for the multi-hop query "How to mitigate the malware Stuxnet?", the correct reasoning involves intermediate steps "Stuxnet utilizes DLL Injection" and "DLL Injection can be mitigated by Behavior Prevention on End-point"; POISONEDRAG's poisoning text "Stuxnet can be mitigated by Network Intrusion Prevention and User Training" is highly query-similar, so NaiveRAG would retrieve it and generate an incorrect answer, while GraphRAG is more resilient.
- First resilience mechanism: during the indexing phase, GraphRAG's use of LLMs to extract entity and relation descriptions can negatively impact poisoning effectiveness, because the LLM may omit critical information from the poisoning text during extraction.
- Second resilience mechanism: even under controlled conditions (zero temperature and explicit prompting), the LLM tends to generate accurate descriptions when it encounters both the original corpus statements and the poisoning statements introduced by POISONEDRAG, thereby undermining the attack's effectiveness.
- The chunk ends by introducing GRAGPOISON, a novel attack designed specifically for GraphRAG that innovates in two ways: (a) higher effectiveness by poisoning relations rather than answers to exploit GraphRAG's graph-based retrieval, and (b) improved scalability by generating poisoning text that compromises multiple queries simultaneously.

---

## 3.1 Experimental Setting

- **RAG.** The conventional baseline is NaiveRAG; the graph-based implementations are GraphRAG and LightRAG. For GraphRAG and LightRAG, GPT-4o-mini is used as the underlying LLM.
- **Attacks.** POISONEDRAG is used as the representative poisoning attack. It generates poisoning text for each query by directly providing an incorrect answer — e.g. for the query "How to mitigate the malware Stuxnet?" the poisoning text can be "Stuxnet can be mitigated by Network Intrusion Prevention and User Training."
- **Metric.** Attack success rate (ASR): ASR = (1/|X|) Σ_{(x,y)∈X} 1[ŷ ≠ y], where |X| is the number of total target queries and 1p is the indicator function returning 1 if p is true and 0 otherwise.

## 3.2 Experimental Results

POISONEDRAG's performance degrades on both GraphRAG and LightRAG compared to NaiveRAG across all settings. For instance, on the Geographical dataset, the ASR against NaiveRAG is over 10% higher than against GraphRAG or LightRAG.

**Table 1: Attack effectiveness of POISONEDRAG on NaiveRAG and two Graph-based RAG (i.e., GraphRAG and LightRAG)**

| Dataset | NaiveRAG | GraphRAG | LightRAG |
|---|---|---|---|
| MuSiQue | 88.4% | 57.6% | 59.6% |
| Geographical | 71.6% | 59.3% | 61.9% |
| Medical | 69.5% | 58.9% | 56.8% |
| Cyber-Security | 97.4% | 68.4% | 63.2% |

**Why existing poisoning attacks degrade under GraphRAG.** To illustrate the observed ASR gap between GraphRAG and NaiveRAG, the paper considers the multi-hop query "How to mitigate the malware Stuxnet?". The correct reasoning involves intermediate steps "Stuxnet utilizes DLL Injection" and "DLL Injection can be mitigated by Behavior Prevention on End-point". POISONEDRAG directly concatenates the subject to an incorrect mitigation (e.g. "Stuxnet can be mitigated by Network Intrusion Prevention and User Training"). Against NaiveRAG, this poisoning text, with high textual similarity to the query, would likely be retrieved and passed to the generator LLM, leading to an incorrect answer. However, GraphRAG's processes inherently provide resilience, through two mechanisms:

1. **Extraction-time omission.** During the indexing phase, GraphRAG's use of LLMs to extract entity and relation descriptions during indexing can negatively impact poisoning effectiveness — specifically, the LLM may omit critical information from the poisoning text during extraction.
2. **Accurate description generation.** Further, even under controlled conditions (zero temperature and explicit prompting), the LLM tends to generate accurate descriptions when encountering both original statements introduced by POISONEDRAG, thereby undermining its effectiveness.

**4. GRAGPOISON (introduced at the end of the chunk).** Next, the chunk introduces GRAGPOISON, a novel attack designed specifically for GraphRAG that addresses the key limitations of existing attacks. The attack innovates in two ways: it achieves higher effectiveness by poisoning relations rather than answers to exploit GraphRAG's graph-based retrieval, and it improves scalability by generating poisoning text that compromises multiple queries simultaneously.

As illustrated in Figure 3, GRAGPOISON operates in three phases:

- **i) Relation Selection (§4.1).** It employs an LLM to extract and identify critical relations shared across target queries from inferred query-related subgraphs, using the LLM's chain-of-thought reasoning.
- **ii) Relation Injection (§4.2).** It generates poisoning text to inject deceptive competing relations (r*) that substitute the selected shared relations, concealed within logical "covering narratives" through semantically crafted textual descriptions (d*r).
- **iii) Relation Enhancement (§4.3).** It generates additional poisoning text to create supporting textual narratives (d+r) that strengthen the injected relations, boost their centrality and retrieval priority by GraphRAG.

Unlike traditional graph poisoning attacks that assume explicit graph knowledge and directly manipulate structures or node/edge features/embeddings, GRAGPOISON must first infer relevant graph portions (i.e. Relation Selection) and then generate poisoning textual narratives targeting the source corpus (i.e. Relation Injection, Relation Enhancement).

**Covers:** Sec 3 (RQ1: Performance of Conventional RAG poisoning attacks), Sec 3.1-3.2
