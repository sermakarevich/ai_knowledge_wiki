> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## Memory, State & Retrieval

Agents need three kinds of memory to operate effectively: scratch (in-context), episodic (recent learnings), and semantic (domain knowledge). This section covers memory architecture, RAG design, and grounding agents in facts.

### Three Kinds of Memory

**Scratch:** In-context token budget. Fast, limited, immediate.
**Episodic:** Conversation history and learnings. Slower, larger, per-session.
**Semantic:** Domain knowledge and facts. Structured, searchable, shared across users.

### RAG (Retrieval-Augmented Generation)

RAG grounds the agent in facts by:
1. Converting user query to embeddings
2. Searching vector DB for similar documents
3. Including those documents in the prompt
4. Model generates response grounded in retrieved facts

### Key Concepts

- **Chunking strategy:** How you split documents affects retrieval quality
- **Embedding models:** Different models for different domains
- **Hybrid retrieval:** Combine vector search with keyword matching
- **Memory decay:** Validate facts; don't trust old memory
- **Memory poisoning:** Assume external data may be adversarial
- **Citation & provenance:** Track where facts came from

### Interview Questions

- "Design a RAG system for 100K technical docs. What's your chunking strategy?"
- "A retrieved document is outdated. How do you detect that?"
- "How would you prevent prompt injection through a retrieved document?"

### Future Sections (To be expanded)

- Chunking strategies (token-based, semantic, domain-specific)
- Embedding model selection and fine-tuning
- Hybrid retrieval implementation
- Context window optimization
- Long-context inference strategies
