> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Vault Curate is an Obsidian plugin for semantic search and connection-finding across local notes, strong on Chinese/CJK, with relation graphs, semantic paths, and Hot/Cold rediscovery, where nothing leaves the machine by default (01-overview.md:22, 01-overview.md:24, 01-overview.md:51).
## Key points
- Vault Curate's whole job is "Find, connect, and rediscover your notes" via semantic search and connection-finding for Obsidian notes (01-overview.md:22, 01-overview.md:24).
- Three capabilities work out of the box with zero setup — Find, Connect, Rediscover — while the fourth, AI curation, is off until turned on (01-overview.md:62).
- Every suggested connection waits for user verdict: one click turns it into a real wikilink, or ✕ dismisses the pair permanently even across renames or index rebuilds (01-overview.md:69).
- The built-in model is about 110 MB, downloads once, needs no API key, and AI curation only sends data out if the user points it at a cloud service (01-overview.md:51).
- Search fuses three engines — Keyword, Semantic, Fuzzy title — into one ranking, and the built-in model reads long notes in full up to 60,000 characters (01-overview.md:77, 01-overview.md:88).
- Relation graphs render as editable Obsidian Canvas files with purple (unlinked), gray (wikilinked), cyan (Cold), and green (query-relevance) edges/nodes, each run writing a fresh timestamped `.canvas` (01-overview.md:102, 01-overview.md:104, 01-overview.md:109).
- Notes are auto-tiered Hot/Cold by internal links plus recency, where editing counts as use but merely opening does not, with the cutoff tunable under Advanced → Hot window (days) (01-overview.md:126).
---
## Principles
Built for three stated problems: keyword-only search failing, scattered related notes requiring manual linking, and years of notes becoming lost memories — explicitly not an AI that auto-reorganizes notes into a wiki (01-overview.md:38, 01-overview.md:40, 01-overview.md:43).
- "**Nothing leaves your machine by default.** Everything runs on your own computer: the model is about 110 MB and downloads once, no API key needed" (01-overview.md:51).
- "**Strong on Chinese.** The built-in Chinese model handles personal names, proper nouns and colloquial phrases especially well. For other languages, switch to Ollama or any OpenAI-compatible service" (01-overview.md:52).
- "**It doesn't think for you.** No AI running in the background, no automatic edits to your notes. Every connection is only a suggestion; you decide yes or no" (01-overview.md:53).
- "**Works on your phone too.** Build the index on desktop, let iCloud, Obsidian Sync or Syncthing carry it over, and search on your phone directly: no re-indexing, no model download" (01-overview.md:54).
## Find: semantic search
"Search by meaning, not just literal characters. Three searches run at once and merge into one ranking" (01-overview.md:77):
| Search | Catches |
|---|---|
| **Keyword** | Exact phrases, keyword combinations (01-overview.md:81) |
| **Semantic** | Different wording, same meaning (01-overview.md:82) |
| **Fuzzy title** | Typos, spelling variants (01-overview.md:83) |
- Entry points: `Vault Curate: Semantic search (modal)` via Cmd/Ctrl+P for quick jump; sidebar **Search** tab for persistent results (01-overview.md:85).
- Results show the matched passage with search words highlighted; clicking opens the note at that passage; in the modal, **Alt+Enter** inserts a link to the selected result at the cursor instead of opening it (01-overview.md:86).
- **Hot / Cold / All** filter: search covers every note by default; buttons narrow to recently touched (Hot) or long-untouched (Cold) notes (01-overview.md:87).
- Long notes read in full up to 60,000 characters so deep passages are findable by meaning (01-overview.md:88).
- **VC: Find similar notes** via right-click on any `.md`; results land in the sidebar and drag to Canvas; markdown structure is stripped before comparison and the note's `description` property joins ranking; Traditional-Chinese vaults convert Traditional→Simplified under the hood for matching while stored text, keyword search, and snippets stay Traditional (01-overview.md:89).
- Ranking fuses frontmatter **tags** with semantic similarity in Find Similar, relation graph, and current-note Discover; with no tags, pure semantic ranking applies (01-overview.md:90).
- Synonyms under Advanced → Synonym list (e.g. `Amy = Amy Chen`): a query with one form silently also searches the others; especially handy on mobile where search runs in keyword mode (01-overview.md:91).
- **Export results to Canvas**: query in the middle, top 12 results around it, each edge labeled with relevance score; past 12 a notice states how many were left out (01-overview.md:92).
## See connections: relation graph / semantic path / expand in place
"Search finds a single note; this layer shows how notes relate, including the links you never drew by hand" (01-overview.md:100).
- **Relation graph (Canvas)**: center note with closest semantic neighbors laid out radially, every edge labeled with similarity score (01-overview.md:102); purple edges = semantically close but not yet linked; gray edges with direction arrows = already wikilinked; cyan nodes = Cold notes; green edges = relevance to a search query on results canvases only, never between two notes (01-overview.md:104, 01-overview.md:107).
- Entry via command palette, right-click **VC: Generate relation graph**, or **Graph** button on Discover sidebar; each run writes a fresh timestamped `.canvas` into the folder set under Advanced → Relation graph folder (default `Vault Curate Canvases`), never overwriting edited graphs (01-overview.md:109).
- **Semantic path (Canvas)**: chain of stepping-stone notes between any two notes, judged by weakest hop; honest "not connected" notice with actual numbers when no strong chain exists; semantic map builds once in background (progress shown, cancellable, UI never freezes) then follows edits in real time (01-overview.md:113).
- **VC: Expand in this graph** via right-click on a canvas node grows the graph in place, slotting the neighborhood into free space, adding connecting edges instead of duplicates; a note pointed at by two or more edges turns **orange**; layout edits and manual colors are never touched (01-overview.md:115).
- Verdict Yes: right-click a generated `.canvas` → checkbox dialog lists every purple edge grouped by source note; Cmd/Ctrl+hover gives native page preview; checked pairs are written into notes' **Related** section as real wikilinks (both notes by default, source-only via **Advanced → Bidirectional promotion**), edges turning gray on the spot (01-overview.md:119).
- Verdict No: per-pair *Don't suggest* button plus hover **✕** on sidebar rows (Find Similar, Discover); dismissed pairs vanish from all suggestion surfaces with slot refilled by next candidate; reviewable under **Settings → Advanced → Hidden suggestions** with open-note link and copy-path button (01-overview.md:120).
## Rediscover: Hot/Cold tiering + Discover
"A good note shouldn't cease to exist just because you forgot it. Notes are auto-tiered by **internal links + recency**" (01-overview.md:126): **Hot** (linked, or created/edited recently; any edit counts as deliberate touch; merely opening does not) vs **Cold** (orphan and untouched for a while); cutoff tunable under Advanced → Hot window (days), applied instantly with tiers derived live at query time (01-overview.md:126).
- Discover works on **notes**, not query strings, surfacing semantically related Cold notes (01-overview.md:128).
- **Current note**: opening a file surfaces related notes ranked by relatedness, Cold ones visually highlighted (01-overview.md:131).
- **Global**: forgotten notes most related to recent focus (recently edited/created notes, their topic tags, semantic centroid), grouped by top-level folder (01-overview.md:131).
- **Generate MOC** exports results to a topic-grouped Map of Content, falling back to flat MOC when results are too few or too similar (01-overview.md:132).
- Every row takes verdict via hover **✕** (in global Discover, the note itself), freed slot refilled (01-overview.md:133).
## Curate (optional, off by default)
Turned on under **Settings → AI Curation → Enable AI curation** to unlock three actions, all manually triggered, never background (01-overview.md:142); the chunk lists "Generate a description + tags into a single note's frontmatter" (01-overview.md:144) followed by a truncated line "Run description" (01-overview.md:145), so the remaining Curate actions are cut in the source and are not described here.
**Covers:** README overview of notoriouslab/vault-curate (Find / Connect / Rediscover / AI curation, Hot-Cold tiering, Canvas relation graph); macro-component stub listing `top-level-files/` (01-overview.md:22, 01-overview.md:62, 01-overview.md:149)
