# Notebook: ontology-in-AI concept tutorial (runs after research epic)

## Problem
The `research` workflow run `wfr-2l1rhkdh` (epic `fleet-grfzs`) builds
`/Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai/` (digests, lenses, sources)
but no runnable tutorial. The user wants 1 concept notebook explaining ontology
in AI. This bead creates it from the finished research aggregates.

## Fix
Create ONE file (plus its output dir):
`/Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai/notebooks/ontology_in_AI.ipynb`
(nbformat 4, 8-12 cells), teaching: what an ontology is (classes, properties,
individuals, axioms) vs taxonomy vs knowledge graph; tiny hand-built ontology
in plain Python dicts (stdlib only, simulated I/O, never network/keys);
RDF-triple / OWL idea in 5 lines; a toy ontology-alignment + consistency-check
demo; how LLMs use ontologies (constrained decoding, KG grounding, eval);
failure case (ambiguous term) with fix; closing quiz cell (assert-based).
Every factual claim must trace to the research leaves — cite
`../../../<Name>/summary.md` (papers, three levels up from `notebooks/`) and `../digest.md` in markdown cells (relative links).
Style: simple language for non-experts; expand EVERY abbreviation on first use
in the notebook (e.g. OWL (Web Ontology Language, a formal vocabulary format));
flowing paragraphs, not one sentence per line.

STOP-IF-MISSING: before writing anything, check these exist:
`/Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai/index.md`,
`/Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai/digest.md`,
and >= 5 `summary.md` files under
`/Users/sergii/.ai/knowledge/research_topics/ontology_ai/*/summary.md` (the paper folders sit in the topic folder, next to `research/`).
If any check fails, exit 1 WITHOUT creating files and WITHOUT closing the bead
(the research run is not finished yet; the supervisor will retry).

## Tests
Exact commands (cwd `/Users/sergii/.ai`):
1. `ls /Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai/notebooks/ontology_in_AI.ipynb`
2. `python3 -c "import nbformat; nb=nbformat.read('/Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai/notebooks/ontology_in_AI.ipynb', as_version=4); print(len(nb.cells), 'cells'); assert 8 <= len(nb.cells) <= 14"`
3. `jupyter nbconvert --to notebook --execute /Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai/notebooks/ontology_in_AI.ipynb --to notebook --stdout > /dev/null`
   (must exit 0; if `jupyter` is missing use `python3 -m nbconvert` same args;
   if neither exists, `pip install --quiet nbconvert nbformat` first — never
   touch `pyproject.toml`/`uv.lock`)
All three green.

## DoD
1. Listed tests green.
2. Stage ONLY the notebook by explicit path:
   `git add knowledge/research_topics/ontology_ai/research/ontology-ai/notebooks/ontology_in_AI.ipynb`
   then `git commit -m "ontology-ai: concept tutorial notebook"`.
   NEVER `git add -A`/`.`, `-a`, reset, checkout, stash, or restore.
3. Verify it landed:
   `git show HEAD:knowledge/research_topics/ontology_ai/research/ontology-ai/notebooks/ontology_in_AI.ipynb | grep -c ontology`
   prints >= 1.
4. `bd close fleet-ontonb1 --reason "ontology concept notebook landed and executes green"`.
   Never exit rc=0 without closing; close ONLY your own task.

## Scope & constraints
- cwd: `/Users/sergii/.ai`. Do NOT run `fleet serve restart` / `fleet run`.
- Touch ONLY the notebook path above. Never rewrite research aggregates,
  sources, or sibling folders. No new packages, no lockfile changes.
- Recipe: plain task, no `ai show` recipe needed; contracts above are complete.
