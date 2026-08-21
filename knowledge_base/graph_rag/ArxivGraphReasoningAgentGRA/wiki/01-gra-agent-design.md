[[../index|Wiki]] | [[../summary|Summary]]

# GRA agent design: code agents applied to knowledge graphs, and the three tested systems

**In one sentence:** The paper argues that a knowledge graph admits the same generic navigation interface as an unfamiliar codebase, and presents GRA — a graph reasoning agent using seven unix-style tools — against two controls (RSA, the same loop without the graph, and SQA, a full-context serialized baseline) on the UFK-M benchmark.

## Key points

- Tool-calling code agents (ls, cat, grep over files) navigate repositories they have never seen; a labeled property graph admits structurally equivalent operations — listing neighbours, reading node content, searching node descriptions.
- The authors present GRA (Graph Reasoning Agent) for hybrid knowledge graphs, whose nodes are either textual concepts or relational tables, discovering everything domain-specific at run time via seven generic tools.
- Headline result (from the abstract): on UFK-M, an industrial benchmark of 258 analytical questions whose gold answers come from executing validated SQL programs, GRA beats a full-context agent by 5.1 pp (88.4% vs. 83.3%) while reading under a third of its input tokens.
- The abstract frames the two competing philosophies this paper measures: serialize everything into the prompt, versus give the model a bounded context plus tools to fetch what it needs.
- A graph-free control (RSA) shows the gain comes chiefly from selective agentic access rather than graph topology, and the effect depends on a model able to drive tools reliably.
- The assumed substrate contract is minimal: each node has an identifier, natural-language description, labels, optional properties; relations are directed subject–predicate–object triples; some nodes are data tables backed by real DuckDB tables queryable with SQL.
- The design descends from ReAct (interleaving reasoning and tool calls) and SWE-agent (showing a few file-system commands suffice for an unfamiliar repo); prior graph-agent work assumes the vocabulary is known and that traversal alone answers the question — neither holds on a hybrid substrate.
- GRA hard-codes nothing domain-specific: no concept list, no label strings, no table names in tools or system prompt.
- RSA ("fairness enforced by construction") shares the identical execution loop and strategy prompt blocks verbatim with GRA, differing only in substrate (flat text chunks + table schemas) and navigation tools.
- SQA is the serialize-everything baseline: full text description plus fully rendered schema (~17k tokens) up front, answering within at most six turns with no navigation.

## Detail

### Framing: from code agents to graph agents

The paper (Dragic, Rio, Ifrah — R&D at Oplit, July 2026, arXiv:2608.15834v1) opens with a correspondence argument: tool-calling agents work effectively inside repositories they have never seen using a small set of generic primitives — list a directory, read a file, search for a string. None of these tools knows anything about the project; the agent reconstructs it by navigating. A labeled property graph admits the same interface: listing the neighbours of a node, reading a node's content, and searching node descriptions are structurally equivalent operations on a different substrate, so the navigation competence of code agents should transfer to knowledge graphs at little cost.

The substrate contract assumed is minimal, and it defines what "hybrid" hybrid knowledge graph means:

- Every node carries an identifier, a natural-language description, labels, and optional properties.
- Relations are directed subject–predicate–object triples.
- Some nodes are data tables, backed by a real DuckDB table that can be queried with SQL.

Textual and relational knowledge thus coexist in one graph, and answering a question may require either or both. The paper explicitly measures the trade-off between two competing philosophies: (1) serialize everything (documentation and schema) into the prompt and ask for an answer, and (2) give the model a bounded context and a toolset and let it fetch what it needs — with controls designed to attribute the outcome to its cause.

The abstract previews the headline numbers: on UFK-M (Unified Factory Knowledge Model), an industrial benchmark of 258 analytical questions whose gold answers are produced by executing validated SQL programs, GRA beats a full-context agent by 5.1 pp (88.4% vs. 83.3%) while reading under a third of its input tokens. A graph-free control shows the gain comes chiefly from selective agentic access rather than graph topology, and that the effect depends on a model able to drive tools reliably. In the paper's words: "Seeing less, the agent answers better: selective navigation over a structured substrate beats exhaustive context."

The paper's opening figure (rendered as text in the source) illustrates the substrate and systems: a semantic layer (Rule R8, Concept Customer, KPI Lateness) is bridged to a data layer (tbl_customers with customer_id (pk), segment/market; tbl_orders with order_id (pk), cust_id (fk), promised/delivered) via edges CONSTRAINS, REPRESENTS, JOINS, MEASURED_ON. GRA reads graph slices with its seven tools; RSA, the flat agent (search_text, describe_table, query, think, answer), retrieves chunks + schemas in "the same loop, graph removed"; SQA serializes the founding text + full schema (~17k tokens up front) into its prompt and runs ≤6 turns with no navigation.

### Related work

- **ReAct [1]** — GRA's interface descends from it: ReAct introduced the interleaving of reasoning and tool calls now common to LLM agents, but left open which tools a given substrate should expose.
- **SWE-agent [2]** — answered that question for source code: its agent–computer interface showed that a few file-system commands suffice to work over an unfamiliar repository. A knowledge graph is much like a codebase in this respect — a large connected structure explored by following links, not by reading it whole — so the strategy transfers directly; only the substrate differs.
- **Graph retrieval-augmented generation surveys [3]** — a parallel line giving LLMs an interface to structured knowledge directly: these systems read over graphs, tables, and databases [4], follow relation paths [5–7], or expose primitives for node lookup and neighbour listing [8, 9]. All share GRA's premise — navigate the graph rather than read a flat dump of it — but assume that the graph's vocabulary is known and that traversal alone answers the question. The paper argues neither assumption holds on a hybrid substrate: the deciding fact often sits in a table reached through the graph, and a question's words must first be matched to a node. Aligning the two is itself hard, as work on natural-language-to-graph-query translation shows [10].
- **GraphRAG [11]** — instead builds a graph and summaries offline and retrieves over them. That suits broad questions but fixes the retrieval structure in advance, whereas GRA gathers evidence per question over a graph that keeps changing.

The paper's synthesis: each of these provides part of what GRA needs, but none provides all of it at once — (a) operation without per-schema tuning, (b) a substrate that unites a semantic graph with relational tables, and (c) the ability to compute a quantity no node stores. Section 8 (overview of the industrial-intelligence examples, per the table of contents) puts that combination to work, where turning an operator's plain-language rule into a grounded feasibility verdict depends on all three together.

### Three agents, one substrate

#### GRA: Graph Reasoning Agent

GRA explores the graph with seven unix-style tools. Nothing domain-specific is hard-coded in the tools or the system prompt: no concept list, no label strings, no table names. The agent orients with `ls`, reads nodes with `cat`, searches literally with `grep` and semantically with `sems`, and reads values with a read-only `query`.

**Table 1 — The GRA toolkit: seven generic primitives for navigating and querying a hybrid knowledge graph**

| Tool | Role |
|------|------|
| `ls` | List nodes, tables, and edges to orient in the graph. |
| `cat` | Read a single node in full; for tables, shows columns, keys, joins, and a 3-row sample. |
| `grep` | Literal search over ids, text, properties, edges, and columns. |
| `sems` | Semantic search (dense + BM25, top 10 results). |
| `query` | Read-only SQL (SELECT/WITH), capped at 50 rows. |
| `think` | Scratchpad for planning and checking, no side effects. |
| `answer` | Submit the final answer, with optional citations and confidence. |

**Worked example (UFK-M):** Question — "How many orders were late for each customer segment last quarter?" The agent starts cold: no schema, no table names, no vocabulary. Trace: `ls(labels)` → `ls(tables)` → `grep("orders")` → `grep("customer segment")` → `cat(tbl_customer_orders)` → `cat(Customer)` → `cat(tbl_customers)` → `query(...)` → `think` → `answer`. The KG and the definition of "late" are discovered on the way, and only a few thousand unique tokens are ever read.

#### RSA: Retrieval SQL Agent

RSA is GRA with the graph removed: it retrieves over chunks of the flat textual documentation and over table schemas (`search_text`, `list_tables`, `describe_table`) and keeps the identical `query`, `think`, and `answer` tools. Fairness is enforced by construction: both agents run the very same execution loop, share their strategy prompt blocks verbatim, and differ only in substrate and toolset.

**Worked example, same question:** Trace: `search_text("customer segment")` → `list_tables()` → `describe_table(tbl_customer_orders)` → `describe_table(tbl_customers)` → `query(...)` → `think` → `answer`. The same loop reaches the same answer, but the link between the segment concept and the table that stores it must be inferred from retrieved text chunks rather than read off an edge, and candidate tables are scanned by name instead of followed.

#### SQA: SQL Agent

SQA follows the serialize-everything approach: it receives a prompt containing the complete text description of the graph and the fully rendered schema (typed columns, key relations, categorical vocabularies, date ranges), totaling approximately 17k tokens, and produces SQL answers within at most six turns.

**Worked example, same question:** The prompt already contains the founding text and every table schema (≈17k tokens). Turn 1: a single SQL statement joining `tbl_customer_orders` and `tbl_customers`. Turn 2: the answer. There is no search and no navigation — the join path is visible in the prompt from the start. The whole corpus is read before the first word, whether or not the question needs it, and the remaining turns serve only to repair a failed query.

The exact distinction the paper draws: GRA navigates a structured substrate and reads graph slices on demand; RSA is the same agent and loop with the graph removed, retrieving chunks and schemas instead; SQA gets everything serialized up front and simply writes SQL. The three-way design isolates, by construction, whether the benefit comes from graph structure or from selective agentic access itself (and, per the abstract, from a model reliable enough to drive tools).
