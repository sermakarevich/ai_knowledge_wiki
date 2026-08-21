import json

BASE = "/Users/sergii/.kb/papers/ArxivSAGEGraphMemory"
manifest = json.load(open(f"{BASE}/source/chunks.json"))

FORMAT_CONTRACT = """## Wiki page format contract (follow exactly)

The output file is one page of an LLM-wiki. Structure it exactly like this:

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# <Topic Title>

**In one sentence:** <the section's whole argument, in one sentence>

## Key points

- <complete-claim bullet 1, with real numbers/mechanisms/conclusions>
- <complete-claim bullet 2>
- ... (5-8 bullets total, each a standalone claim, not a topic label)

---

<Full detail below, mirroring the source's internal structure with ## subsections.
Use tables for numeric results. Quote exact numbers, prompts, or equations where
the source gives them. Embed any named figure exactly where it is discussed:
![<caption>](images/<file>.png) using the image file(s) listed below, if any.>

**Covers:** <line/section range given below>
```

Rules:
- The page must cover the WHOLE chunk given to you, including the last topic near the end of the chunk — do not stop after the opening subsection.
- Write for a technical reader already familiar with RAG / knowledge graphs / RL — no need to re-explain basics, but do explain this paper's own notation and mechanisms.
- Do not invent numbers, citations, or claims not present in the chunk text.
- If the chunk is mostly proofs/derivations, summarize the setup, the key lemma/proposition statements, and their informal implication — do not transcribe full equation derivations line by line, but do keep the final stated bounds/results verbatim.
"""

RETRY_NOTE = """
## If this is a retry

If the output file already exists (a retry), overwrite it completely — do not
try to merge with the previous attempt.

Context is tight on this worker model: read ONLY the chunk file (and the figure
description file(s), if listed) referenced below — nothing else. Do NOT read this
task's own fleet artifacts/log/event files, and do NOT read sibling wiki pages for
style reference; the format contract above is the only convention you need. On a
retry, do not try to diagnose the prior failure by reading logs — just re-read the
chunk and write the page directly.
"""

DOD = """
## Definition of done

1. Write the full page to the output path below.
2. `bd close <own-id> --reason "chunk {n} extracted"`

Scope: touch ONLY the one output file listed below. Do not run any fleet/bd
commands other than the final `bd close`. No git commands — this repo auto-syncs.
"""

for c in manifest["chunks"]:
    n = c["chunk"].split(".")[0]
    chunk_path = f"{BASE}/source/chunks/{c['chunk']}"
    out_path = f"{BASE}/wiki/{c['wiki_page']}"
    img_lines = ""
    if c["images"]:
        img_lines = "\n## Figure description file(s) for this chunk\n\n"
        for img in c["images"]:
            desc_path = f"{BASE}/wiki/images/{img.rsplit('.',1)[0]}-description.md"
            img_lines += f"- Image: `{BASE}/wiki/images/{img}` (embed as `![...](images/{img})`)\n"
            img_lines += f"- Vision description (read this to write the caption/discussion): `{desc_path}`\n"

    spec = f"""# Extract task — SAGE paper, chunk {n}

Topic: {c['topic']}
Source paper: SAGE: A Self-Evolving Agentic Graph-Memory Engine for Structure-Aware
Associative Memory (Wang et al., 2026), https://arxiv.org/abs/2605.12061

## Input

Read exactly this file — it is a plain-text excerpt of the paper (source lines {c['source_lines']}):

`{chunk_path}`
{img_lines}
## Output

Write the wiki page to:

`{out_path}`

{FORMAT_CONTRACT}
{RETRY_NOTE}
{DOD.format(n=n)}
"""
    spec_path = f"{BASE}/source/specs/{n}-extract.md"
    open(spec_path, "w").write(spec)
    print("wrote", spec_path)
