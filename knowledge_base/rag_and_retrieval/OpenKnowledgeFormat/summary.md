# Introducing the Open Knowledge Format

**Article:** [Introducing the Open Knowledge Format (Sam McVeety, Amir Hormati, 2026)](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

## Human Readable TL;DR

Imagine every team at a company keeps their notes in completely different filing systems -- one uses sticky notes, another uses spreadsheets, and another keeps it all in someone's head. When you bring in a new assistant (like an AI) to help, they have to re-learn everything from scratch because nothing is written in a common language. The Open Knowledge Format (OKF) is like agreeing to write all those notes as simple markdown text files with a small header tag, so any person or AI tool can pick them up and immediately understand them -- no special app required, no translation needed.

## TL;DR

Google Cloud introduces OKF v0.1, a vendor-neutral open specification for representing organizational metadata and context as markdown files with YAML frontmatter. It addresses the fragmentation of knowledge across proprietary catalogs, wikis, and undocumented expert knowledge by defining a minimal, portable format (one required field: `type`) that lives in version control, is human-readable and machine-parseable without any translation layer, and cleanly separates producers from consumers. Google ships three reference implementations: an LLM-powered enrichment agent, a static HTML graph visualizer, and sample bundles for public BigQuery datasets.

---

## Problem & Motivation

Modern AI systems require relevant, accurate context to function well, but organizational knowledge is fragmented across incompatible systems: proprietary metadata catalogs, wikis, code comments, and senior engineers' undocumented expertise. As a result, every agent builder re-assembles context from scratch, every catalog vendor reinvents the same data models, and knowledge cannot travel between products or organizations. There is no lingua franca -- no format that is simultaneously readable by humans, parseable by agents, portable across vendors, and surveyable without proprietary SDKs.

---

## Main Original Ideas

1. **Knowledge as a Living Wiki** -- Rather than repeatedly querying siloed systems, teams maintain a shared markdown library (inspired by Andrej Karpathy's LLM Wiki pattern). Agents -- not humans -- handle bookkeeping: updating cross-references, touching 15 files in one pass, never getting bored or forgetting.

2. **File Path as Concept Identity** -- The directory structure IS the knowledge graph. A table lives at `sales/tables/orders.md`; its path encodes its position in the ontology without requiring a database index.

3. **Minimal Opinionation** -- Only one required YAML frontmatter field (`type`). Producers decide types, additional fields, and body structure. The spec defines the interoperability surface, not the content model, keeping the barrier to adoption near zero.

4. **Producer/Consumer Independence** -- OKF cleanly separates writers from readers. A metadata export pipeline, a human editor, and an LLM enrichment agent can all produce OKF bundles; a graph visualizer, a search index, and an agent reasoning tool can all consume them -- with the format as the only contract.

5. **Format, Not Platform** -- Deliberately not a cloud service, not a database, not a framework. Value comes from adoption, not ownership. Files are shippable as tarballs, hostable in git, mountable on any filesystem.

---

## Key Findings

| Aspect | Detail |
|--------|--------|
| **Spec size** | Full v0.1 conformance spec fits on a single page |
| **Required fields** | Only `type` is mandatory; all others optional |
| **File types** | Markdown + YAML frontmatter; no binary formats |
| **Cross-linking** | Standard markdown links create concept graphs richer than directory hierarchy alone |
| **Special files** | `index.md` (progressive agent navigation), `log.md` (chronological history) |
| **GCP integration** | Knowledge Catalog updated to ingest and serve OKF bundles |

- Reference enrichment agent: walks a BigQuery dataset, drafts an OKF document per table/view, then runs a second LLM pass to add citations, schemas, and join paths from authoritative docs.
- Static HTML visualizer: renders any OKF bundle as an interactive graph with zero backend, zero install, and zero data egress.
- Sample bundles shipped for GA4 e-commerce, Stack Overflow, and Bitcoin public datasets -- produced by the reference agent and committed as living examples.

---

## Suggestions & Future Directions

1. **Write producers** for existing source systems (databases, documentation sites, data catalogs) to generate OKF bundles automatically.
2. **Write consumers** -- viewers, search indexes, agent memory tools -- that treat OKF bundles as first-class input.
3. **Evolve the spec** with backward-compatible extensions as real adoption surfaces edge cases; v0.1 is an explicit starting point, not a finished standard.
4. **Contribute via GitHub** -- file issues, send PRs, propose type extensions, and publish alternative implementations beyond the Google reference code.
5. **Standardize across agent frameworks** -- the emerging AGENTS.md / CLAUDE.md convention files and Obsidian-vault-wired-to-agent patterns suggest OKF could become the de facto convention if adopted by tooling ecosystems early.

---

## Authors & Institutions

Sam McVeety (Tech Lead, Data Analytics Engineering, Data Cloud, Google Cloud), Amir Hormati (Tech Lead, BigQuery Engineering, Data Cloud, Google Cloud)
