> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Conclusion and Limitations

**In one sentence:** Final citations in Agentic GraphRAG are necessary but not sufficient to explain a generated answer's evidence basis, so citation faithfulness must be evaluated as a trajectory-level property that includes graph context and the retrieval path, not just the final outputs.

## Key points

- Final citations in Agentic GraphRAG are not sufficient to explain the evidence basis of generated answers: cited entities play a necessary role, but accurate answering depends on more than the entities ultimately cited.
- Removing cited entities substantially changes answers and reduces accuracy, confirming their necessity, while removing visited-but-uncited entities and altering traversal/neighborhood structure can also influence how the agent discovers, selects, and interprets evidence.
- A correct citation set can still omit parts of the retrieval trajectory that were relevant to producing the answer, so evaluating citations only by checking whether cited sources support the answer or were visited by the agent is insufficient.
- Faithful citation mechanisms should account for the graph context and retrieval path that shape the final response; provenance in agentic graph-based retrieval should be treated as a trajectory-level property rather than only a final-output property.
- The study is limited by its small benchmark size and by using a controlled knowledge graph built from 2WikiMultiHopQA rather than a large real-world knowledge graph.
- Future work should repeat the interventions on larger datasets, richer graph structures, and domain-specific knowledge bases, and develop citation mechanisms that expose not only final supporting entities but also the relevant traversal context.

---

## Conclusion

The paper examined whether final citations in Agentic GraphRAG are sufficient to explain the evidence basis of generated answers and found that they are not. Cited entities often play a necessary role — removing them substantially changes answers and reduces accuracy — but the experiments also show that accurate answering depends on more than the entities ultimately cited. Graph traversal, neighborhood structure, and visited-but-uncited entities can all influence how the agent discovers, selects, and interprets evidence.

The authors argue that citation faithfulness in Agentic GraphRAG therefore requires a broader notion of provenance: a citation set may correctly identify supporting evidence yet still omit parts of the retrieval trajectory that were relevant to producing the answer. Consequently, evaluating citations only by checking whether the cited sources support the answer, or whether they were visited by the agent, is insufficient. Faithful citation mechanisms should also account for the graph context and retrieval path that shape the final response. Overall, the results indicate that provenance in agentic graph-based retrieval should be treated as a trajectory-level property rather than only a final-output property.

## Limitations

The study is limited by its small benchmark size and by its use of a controlled knowledge graph built from 2WikiMultiHopQA rather than a large real-world knowledge graph. The authors note that future work should evaluate the same interventions on larger datasets, richer graph structures, and domain-specific knowledge bases, and should develop citation mechanisms that expose not only final supporting entities but also the relevant traversal context.

Future work will focus on expanding the experiments across all dimensions — larger datasets, diverse benchmarks, and real-world knowledge bases — while investigating how graph structure influences Agentic AI performance and the interplay between parametric knowledge, cited knowledge, and knowledge acquired through traversal.

---

**Covers:** Sections 4-5 (Conclusion, Limitations), source/full.txt lines 330-363
