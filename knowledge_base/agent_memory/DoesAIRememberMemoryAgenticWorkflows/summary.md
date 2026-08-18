# Does AI Remember? The Role of Memory in Agentic Workflows

**Article:** [Does AI Remember? The Role of Memory in Agentic Workflows (Ksenia Se, 2025)](https://huggingface.co/blog/Kseniase/memory)
**Also published at:** [Turing Post](https://www.turingpost.com/p/aia9)

## Human Readable TL;DR

Imagine if every time you went to sleep, you woke up with no memory of anyone you had ever met. That's roughly how most AI chatbots work today -- each conversation starts fresh. This article explores why memory is such a hard problem for AI systems, what kinds of memory (short-term, long-term, skill-based) researchers are trying to build in, and how agents that can actually remember past experiences behave more like believable, helpful companions. It also raises a deeper question: if AI starts reconstructing our past for us, what happens to human memory itself?

## TL;DR

This article -- part 9 of Ksenia Se's "AI Agent" series -- surveys the role of memory in agentic AI workflows, tracing its roots from the 1987 SOAR cognitive architecture through modern LLM-based generative agents. It categorizes memory into declarative (semantic, episodic) and procedural forms, maps them onto short-term (context window, working memory) and long-term storage, and analyzes how OpenAI's ChatGPT memory mode implements selective retrieval via vector embeddings. The article concludes with a philosophical provocation: AI's memory capabilities are beginning to reshape and potentially erode human agency over our own remembered past.

---

## Problem & Motivation

Current AI systems -- including frontier LLMs -- lack stable, structured memory that persists reliably over time. They can retrieve information or summarize past interactions within a session, but have no consistent mechanism for retaining and using prior experiences across interactions. This gap limits agents' ability to build relationships, learn from experience, and behave coherently over long task horizons. The article frames this as one of the central unresolved challenges in agentic AI system design.

---

## Main Original Ideas

This is a synthesizing survey article rather than a primary research contribution. Its key intellectual moves are:

1. **SOAR as the ancestor of modern agent memory** -- The 1987 SOAR architecture (Newell, Rosenbloom, Laird) is positioned as the foundational template: it unified working memory, long-term memory, and learning in a single framework via chunking (compressing solved problems into reusable production rules) and subgoaling (automatic hierarchical decomposition). Modern techniques -- RAG, fine-tuning, hierarchical planning -- are characterized as echoes of SOAR's original design.

2. **Cognitive taxonomy applied to LLM agents** -- The article maps classical cognitive science memory categories onto AI agent components:
   - *Semantic memory* → knowledge bases and world-fact retrieval
   - *Episodic memory* → logs of past interactions and context-aware adaptation
   - *Procedural memory* → implicit skill learning through training
   - *Working memory* → active reasoning over the current context window
   - *Short-term memory* → the bounded context window itself

3. **Generative Agents as the state-of-the-art exemplar** -- The 2023 Stanford/Google paper "Generative Agents" (Park et al.) is analyzed in depth. Its memory stream architecture -- continuous natural-language logging, scored retrieval by recency + importance + relevance, and periodic reflection into higher-level insights -- is presented as the most complete implementation of human-like memory in AI agents to date.

4. **ChatGPT memory mode as a production case study** -- Rather than storing full transcripts, ChatGPT extracts key facts into vector embeddings stored server-side. These are selectively retrieved on new sessions to simulate continuity. The article highlights user controllability (review, update, delete) as an important design choice.

5. **AI as a reconstructor of human memory** -- Drawing on Andrew Hoskins' 2024 Cambridge paper "AI and Memory", the article argues AI is not merely a memory aid but creates a "third way of memory" -- ongoing reconstruction of pasts never actually lived, through LLM generation. This raises concerns about consent, authenticity, and erosion of human agency over personal and collective historical narratives.

---

## Key Findings

| Memory Type | Cognitive Analog | AI Implementation |
|---|---|---|
| Semantic | General world knowledge | Knowledge bases, retrieval |
| Episodic | Personal past events | Memory streams, conversation logs |
| Procedural | Implicit skills | Training, fine-tuning |
| Working | Active reasoning scratchpad | In-context processing |
| Short-term | Immediate session | Context window |

**Qualitative findings:**

- SOAR's *chunking* mechanism directly anticipates modern in-context learning and RAG: both compress experience into reusable, retrievable units.
- In Generative Agents, three-factor retrieval (recency, importance, relevance) produces emergent social behaviors -- information diffusion, relationship formation, coordinated activities -- that single-session LLMs cannot replicate.
- ChatGPT's memory is not stored in model weights; it is external summarized state retrieved at session start, making it inspectable and editable but also fragile and limited in scope.
- Known failure modes of memory-augmented agents: retrieval failures, hallucinations about past events, and biases inherited from the base model.
- AI-generated "deadbots" (interactive simulations of deceased persons) represent an extreme manifestation of AI memory reconstruction, raising unresolved ethical questions about consent and digital legacy.

---

## Suggestions & Future Directions

The article does not present explicit experimental future work (it is a survey/commentary), but the open questions it surfaces are:

1. How do we build memory that is both persistent and reliable across long agent lifetimes, beyond the current context window?
2. How should agents differentiate learned experience from AI-generated reconstruction of the past?
3. What governance and transparency mechanisms are needed so users retain agency over what AI systems remember about them?
4. How can the SOAR-era insight of unified working + long-term + learning memory be more fully instantiated in modern neural architectures?
5. How do agentic systems maintain coherence in long-horizon tasks without memory retrieval failures or hallucinated recollections?

---

## Authors & Institutions

**Ksenia Se** -- Independent AI researcher and writer, Hugging Face Community; also publishes as Turing Post newsletter author.

**Referenced works:**
- Allen Newell, Paul S. Rosenbloom, John E. Laird -- Carnegie Mellon University (SOAR, 1987)
- Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein -- Stanford University / Google Research (Generative Agents, 2023; arXiv:2304.03442)
- Andrew Hoskins -- University of Glasgow (AI and Memory, 2024, Cambridge journals)
