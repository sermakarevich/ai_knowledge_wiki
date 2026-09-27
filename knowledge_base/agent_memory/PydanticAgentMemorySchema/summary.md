# Pydantic Fixed My Agent's Memory

**Source:** [Akshay Pachaar (@akshay_pachaar) on X, May 25, 2026](https://x.com/akshay_pachaar/status/2058976178908885210)

## Human Readable TL;DR

Imagine your AI assistant has a filing cabinet for memory, but every folder is just labeled "stuff" and every item inside is called "thing." When you ask "which big-budget clients have urgent open tickets?", it can't answer -- not because it forgot the information, but because nothing was organized in a way that lets you filter or search. This post shows how to give your AI a proper filing system upfront by defining categories like "Project," "Technology," and rules like "a User can Work On a Project" -- so the AI stores information in a way it can actually use later.

## TL;DR

Unguided LLM extraction for knowledge graph memory produces generic node/edge types ("Topic," "Object," "RELATES_TO") that make structured querying impossible. The fix is defining a domain ontology upfront using Pydantic `EntityModel`/`EdgeModel` subclasses (via Zep), which constrains extraction to typed entities, typed edges with source/target rules, and structured attributes. This transforms agent memory from a glorified vector store into a traversable, filterable knowledge graph that supports multi-hop reasoning.

---

## Problem & Motivation

**Vector memory breaks on multi-hop queries.** Semantic similarity retrieval only returns chunks that match query terms. If bridging fact "Project Atlas runs on PostgreSQL" doesn't share tokens with "Alice" or "Tuesday", it won't surface -- even though it's the key link for answering "was Alice's project affected by Tuesday's outage?"

**Knowledge graphs solve traversal, but extraction is uncontrolled.** Most frameworks let the LLM decide entity types, relationship labels, and attributes during extraction. The result is generic, unfiltered noise: every customer becomes an "Object," every ticket becomes a "Topic," every relationship becomes "RELATES_TO." The graph has the data but can't be queried by type, severity, or plan tier.

**The gap:** Nobody told the agent what to pay attention to.

---

## Main Original Ideas

1. **Ontology as a memory schema** -- An ontology defines valid entity types, edge types, and the attributes each carries -- analogous to a database schema but for agent memory. Defining it upfront constrains LLM extraction so it produces structured, queryable results instead of ad-hoc labels.

2. **Pydantic `EntityModel` for entity types** -- Custom entity types subclass `EntityModel` (itself a Pydantic `BaseModel`). Field descriptions and class docstrings act as extraction instructions -- they teach the extraction model domain vocabulary it may not have seen in training.

3. **Pydantic `EdgeModel` with source/target constraints** -- Edge types subclass `EdgeModel` and carry typed attributes (e.g., `role`, `proficiency`). `EntityEdgeSourceTarget` rules enforce that, e.g., `WORKS_ON` can only connect `User → Project` -- preventing invalid relationships from being stored at all.

4. **Zep's five-step extraction pipeline** -- On ingestion, Zep runs: entity extraction → entity resolution (dedup) → fact extraction → fact resolution (contradiction invalidation, history preserved) → temporal extraction (validity windows on edges). The Pydantic schema guides steps 1 and 3; the rest is automatic.

5. **Context templates for structured prompt injection** -- Templates select which edge/entity types to include and how many, then format them with temporal annotations into a single string injected into the agent's prompt. Defined once, referenced by ID.

6. **10/10/10 constraint as a forcing function** -- Zep enforces a hard cap of 10 entity types, 10 edge types, and 10 fields per type. This is intentional: it forces domain modeling discipline rather than trying to capture everything. Schema defines the space of valid memories -- what's outside the schema cannot be stored as a typed edge.

---

## Key Findings

- Without a schema, agents using knowledge graphs effectively behave like vector stores -- graph construction cost, no structured retrieval benefit
- Docstring and field descriptions in `EntityModel` are not just documentation -- they are extraction prompts that carry domain vocabulary directly into the LLM extraction step
- Source/target constraints act as guardrails: if `Project → Competitor` isn't a defined edge type, it won't be created even if the conversation mentions both
- The same pattern already used everywhere in AI stacks (FastAPI response models, function calling tool schemas) applies directly to agent memory

**Before schema:**
| Node | Type | Queryable? |
|------|------|-----------|
| Customer A | Object | No |
| Ticket #42 | Topic | No |
| Relationship | RELATES_TO | No |

**After schema:**
| Node | Type | Attributes | Queryable? |
|------|------|-----------|-----------|
| Nexus | Project | status: active, type: web app | **Yes** |
| Python | Technology | category: language | **Yes** |
| Alice→Nexus | WORKS_ON | role: lead developer | **Yes** |

---

## Suggestions & Future Directions

1. **Start small** -- Begin with 3-4 entity types and 3-4 edge types covering 80% of domain logic, then add complexity incrementally
2. **Schema-first for domain-specific apps** -- General LLM extraction works on common knowledge; internal product names, jargon, and acronyms require explicit schema definitions to avoid nonsense extraction
3. **Zep open-source** -- Full implementation available on Zep's GitHub repo (referenced in the post)

---

## Author & Source

**Akshay Pachaar** (@akshay_pachaar) -- X/Twitter thread, May 25, 2026  
Tools referenced: [Zep](https://github.com/getzep/zep) (open-source), Pydantic
