> [[index|Wiki]] | [[digest|Digest]]

# Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs

**Paper:** [Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs (Dragic et al., 2026)](https://arxiv.org/abs/2608.15834)

## The idea in one paragraph

Coding agents (SWE-agent, and the ReAct loop behind them) navigate repositories they have never seen using a handful of generic commands — list a directory, read a file, grep for a string. The paper argues a hybrid knowledge graph — one that mixes free-text concept nodes with relational data tables — admits the exact same interface. GRA (Graph Reasoning Agent) is that agent: seven unix-style tools (`ls`, `cat`, `grep`, `sems`, `query`, `think`, `answer`), nothing domain-specific hard-coded, discovering the schema, vocabulary, and join paths of whatever graph it's dropped into at run time.

## The headline result

On UFK-M — a synthetic-but-realistic industrial benchmark of 258 questions whose gold answers come from validated, executed SQL — GRA beats SQA, a full-context baseline that serializes the entire schema (~17k tokens) into the prompt, by 5.1 percentage points (88.4% vs. 83.3%) while reading under a third of SQA's unique input tokens. A third agent, RSA, is GRA with the graph stripped out (flat text + table schemas, identical loop) — it comes within 0.3–1.9pp of GRA, which tells the authors that most of the win comes from *selectively fetching only what's needed* rather than from graph topology per se. That advantage depends on the backbone model being a reliable tool-caller: with weaker tool-callers (Qwen3-Coder-Flash, GPT-5 Nano), the full-context baseline wins instead.

## Why it matters

Beyond QA, the paper shows GRA embedded in a real factory deployment loop, where it judges whether an operator's plain-language scheduling rule is feasible by navigating the graph for evidence — refusing one rule for two independent reasons found only at question time, and accepting another with a quantified seasonal risk — before a companion agent (ORA) compiles the accepted rule into solver code. The result is a case for treating structured-but-heterogeneous enterprise data the way code agents treat a codebase: don't flatten it into a prompt, give the model tools and let it look.

**Caveat worth carrying forward:** the benchmark's full schema (17k tokens) still fits in every tested model's context window, so the regime where serialization becomes truly infeasible — where structured navigation should matter most — is not yet tested here.

---
See [[digest|the digest]] for a section-by-section version, or jump straight into the [[wiki/01-gra-agent-design|wiki]].
