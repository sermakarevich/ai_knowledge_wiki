PDF: https://github.com/notoriouslab/vault-curate
# notoriouslab/vault-curate
Source: https://github.com/notoriouslab/vault-curate
Kind: repo
Fetched: 2026-09-26T13:46:54.926623+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# notoriouslab/vault-curate

Commit: 3eeb21c7fa2f7ceaa1200650ef0f7875d5c59fd9

## README

<div align="center">



# Vault Curate

[![Website](https://img.shields.io/badge/website-notoriouslab.github.io-7C3AED?style=flat-square)](https://notoriouslab.github.io/vault-curate/)
[![Release](https://img.shields.io/github/v/release/notoriouslab/vault-curate?style=flat-square)](https://github.com/notoriouslab/vault-curate/releases)
[![Downloads](https://img.shields.io/badge/dynamic/json?style=flat-square&logo=obsidian&color=7C3AED&label=downloads&query=%24%5B%22vault-curate%22%5D.downloads&url=https%3A%2F%2Fraw.githubusercontent.com%2Fobsidianmd%2Fobsidian-releases%2Fmaster%2Fcommunity-plugin-stats.json)](https://obsidian.md/plugins?id=vault-curate)
[![License](https://img.shields.io/github/license/notoriouslab/vault-curate?style=flat-square)](LICENSE)
[![Obsidian Desktop + Mobile](https://img.shields.io/badge/Obsidian-Desktop%20%2B%20Mobile-7C3AED?style=flat-square&logo=obsidian)](https://obsidian.md/)
[![WebGPU Accelerated](https://img.shields.io/badge/WebGPU-Accelerated-FF6A00?style=flat-square)]()
[![Ollama Optional](https://img.shields.io/badge/Ollama-Optional-000?style=flat-square)](https://ollama.com/)
[![Last Commit](https://img.shields.io/github/last-commit/notoriouslab/vault-curate?style=flat-square)](https://github.com/notoriouslab/vault-curate)

**Find, connect, and rediscover your notes.**

Semantic search and connection-finding for your Obsidian notes, strong on Chinese/CJK · semantic search · relation graph · semantic paths · Hot/Cold rediscovery · desktop builds, mobile searches · nothing leaves your machine by default

[繁體中文](https://github.com/notoriouslab/vault-curate/blob/main/README.zh-TW.md)

![Vault Curate](./docs/vault-curate.png)

</div>

---



## Why I built Vault Curate

As my notes piled up, I kept running into the same problems:

- I roughly remember writing something, but without the exact keyword I used back then, I can't find it
- Several notes are really about related things, but they're scattered around, and linking them one by one by hand is tedious
- Years of notes turn into lost memories: written once, never opened again
- I don't want an AI to mindlessly reorganize all my notes into a wiki. That would be the AI's memory, not mine

Vault Curate is built for exactly these.



### A few things I insist on

- **Nothing leaves your machine by default.** Everything runs on your own computer: the model is about 110 MB and downloads once, no API key needed. AI curation only sends data out if you point it at a cloud service, and that choice is yours.
- **Strong on Chinese.** The built-in Chinese model handles personal names, proper nouns and colloquial phrases especially well. For other languages, switch to Ollama or any OpenAI-compatible service.
- **It doesn't think for you.** No AI running in the background, no automatic edits to your notes. Every connection is only a suggestion; you decide yes or no.
- **Works on your phone too.** Build the index on desktop, let iCloud, Obsidian Sync or Syncthing carry it over, and search on your phone directly: no re-indexing, no model download.

---



## What it does

Three things work out of the box with zero setup; the fourth (AI curation) is off until you turn it on.

1. **Find**: semantic search that finds notes even when you phrase it differently, and shows the passage that matched.
2. **Connect**: draws related notes you never linked onto an Obsidian Canvas relation graph.
3. **Rediscover**: notes you haven't touched in a long time come back into view.
4. **AI curation** (optional): writes descriptions and tags for notes, and groups results into topic tables of contents.

**Every connection waits for your call.** Like one? Turn it into a real wikilink in one click. Don't? Hit **✕** and that pair is never suggested again, even after renames or index rebuilds. Hot/Cold follows what you do, too: *editing* a note counts as using it again, merely opening it doesn't.

![Semantic relation overview](./docs/concept-graph.png)



### 🔍 Find: semantic search

Search by meaning, not just literal characters. Three searches run at once and merge into one ranking:

| Search | Catches |
|---|---|
| **Keyword** | Exact phrases, keyword combinations |
| **Semantic** | Different wording, same meaning |
| **Fuzzy title** | Typos, spelling variants |

- Cmd/Ctrl+P → `Vault Curate: Semantic search (modal)` for a quick jump; the sidebar **Search** tab for persistent results.
- **See where it matched**: search results show the passage that matched, with your search words highlighted, and clicking it opens the note right at that passage. In the search modal, **Alt+Enter** inserts a link to the selected result at your cursor instead of opening it.
- **Hot / Cold / All**: search covers every note by default, forgotten ones included. The buttons under the search box narrow it to recently touched (Hot) or long-untouched (Cold) notes.
- **Long notes are read in full**: the built-in model reads every part of a long note (up to 60,000 characters), not just its opening, so a passage deep inside a note can be found by meaning too.
- **Find similar notes**: right-click any `.md` → **VC: Find similar notes**; results land in the sidebar and drag straight to Canvas. Similarity ranks **content**, not templates: markdown structure is stripped before comparison and the note's `description` property joins the ranking, so even when dozens of notes share the same template, what surfaces is the handful actually about the same thing, not a row of identical-looking template mates. On Traditional-Chinese vaults, text is converted Traditional→Simplified under the hood before semantic matching (stored text, keyword search, and snippets stay Traditional) to sharpen ranking.
- Ranking is also keyword-aware: Find Similar, the relation graph, and current-note Discover fuse your frontmatter **tags** with semantic similarity, so notes that merely share your writing style stop crowding out notes that share the topic. No tags? Pure semantic ranking.
- **Your own synonyms**: under Advanced → Synonym list you can teach the search your private vocabulary: nicknames, org shorthand, domain terms no model could know (`Amy = Amy Chen` and the like). A query containing one form silently also searches the others. Especially handy on mobile, where search runs in keyword mode.
- **Export the results to a Canvas**: the **Export results to Canvas** button on the Search tab lays your current results out on an editable Canvas: the query in the middle, the top 12 results around it, each edge labeled with that result's relevance score. This is the *result space of one search*, where the relation graph below is the *neighborhood of one note*. Past 12 results a notice tells you how many were left out; nothing is cut silently.

![Search results + Canvas drag](./docs/search-canvas.png)



### 🕸 See connections: relation graph / semantic path / expand in place

Search finds a single note; this layer shows how notes relate, including the links you never drew by hand.

**Relation graph (Canvas)**: generate an editable Obsidian Canvas around any note: the note in the center, its closest semantic neighbors laid out radially, every edge labeled with its similarity score.

- **Purple edges** = semantically close but **not yet linked**: invisible connections the native graph view can't show you
- **Gray edges** (with direction arrows) = notes you've already wikilinked
- **Cyan nodes** = Cold notes
- **Green edges** = relevance to a search query. They appear on the results canvases exported from the Search tab, never between two notes

Entry points: the command palette, right-click **VC: Generate relation graph**, or the **Graph** button on the Discover sidebar. Each run writes a fresh timestamped `.canvas` into the folder set under Advanced → Relation graph folder (default `Vault Curate Canvases`), so your edited graphs are never overwritten.

![Relation graph: semantic neighborhood on Canvas](./docs/relation-graph.png)

**Semantic path (Canvas)**: pick any two notes and get the **chain of stepping-stone notes** that connects them. The chain is judged by its weakest hop, so one far-fetched link can't hide behind strong ones; if no consistently strong chain exists, you get an honest "not connected" notice with the actual numbers. That's information, not an error. The underlying semantic map builds once **in the background** (progress shown, cancellable, UI never freezes) and then follows your edits in real time, so queries stay instant no matter how large your vault grows.

**Expand in this graph**: right-click any node inside a generated canvas → **VC: Expand in this graph** grows the graph *in place*: the clicked note's neighborhood slots into free space around it, notes already on the canvas get connecting edges instead of duplicates, and a note pointed at by two or more edges turns **orange** (several expansions independently converged on it, which usually means it matters). Your layout edits and manually applied colors are never touched.

**Your verdict on every pair**: the graph suggests, you decide, and both answers are one click:

- **Yes → Apply purple edges as wikilinks.** Right-click a generated `.canvas` (or run the command) → a checkbox dialog lists every purple edge grouped by source note; Cmd/Ctrl+hover any name for a native page preview. Checked pairs are written into the notes' **Related** section as real wikilinks (both notes by default, source-only via **Advanced → Bidirectional promotion**), and the edges turn gray with direction arrows on the spot. Nothing is written unchecked, and accepted pairs never come back as suggestions: they're real links now.
- **No → Don't suggest this again.** The same dialog carries a per-pair *Don't suggest* button, and every suggestion row in the sidebar (Find Similar, Discover) has a hover **✕**. A dismissed pair vanishes from all suggestion surfaces, its slot refilled by the next candidate, so rejecting never shrinks your results. Changed your mind? Everything is reviewable and restorable under **Settings → Advanced → Hidden suggestions**, each entry with an open-note link and a copy-path button.



### ♻️ Rediscover: Hot/Cold tiering + Discover

A good note shouldn't cease to exist just because you forgot it. Notes are auto-tiered by **internal links + recency**: **Hot** (linked, or created/edited recently; any edit counts as a deliberate touch; merely opening a note does not), **Cold** (orphan and untouched for a while). The cutoff is tunable under Advanced → Hot window (days) and applies instantly: tiers are derived live at query time.

Discover works on **notes**, not query strings: it actively surfaces semantically related Cold notes you haven't touched recently:

- **Current note**: opening a file surfaces related notes ranked purely by relatedness, with Cold ones visually highlighted ("you haven't read this one")
- **Global**: forgotten notes most related to your **recent focus** (the notes you've recently edited or created, their topic tags, and their semantic centroid), grouped by top-level folder so each corner of your vault surfaces its own best forgotten notes. Intentional blind-spot mining
- Results export to a topic-grouped Map of Content via **Generate MOC** (falls back to a flat MOC when results are too few or too similar)
- Every row takes your verdict: hover **✕** dismisses a suggestion for good (in global Discover, the note itself), with the freed slot refilled (see *Your verdict on every pair* above)
- Also on a Canvas: the Search tab's **Export results to Canvas** button does the same for a query's results, so a search's result space and a note's neighborhood can sit side by side

![Discover sidebar: current note](./docs/discover-current-note.png)



### ✨ Curate (optional, off by default)

Turn it on under **Settings → AI Curation → Enable AI curation** to unlock three actions, all manually triggered, never running in the background:

- Generate a description + tags into a single note's frontmatter
- Run description 

... (truncated, 12471 more characters)

## package.json

```
{
  "name": "vault-curate",
  "version": "1.11.0",
  "description": "Find, connect, rediscover your notes. Local semantic search (BM25 + embeddings), relation graph + semantic paths for unlinked related notes, Hot/Cold surfacing of forgotten ones, strong Chinese/CJK. Mobile reads your desktop-built index. No API keys.",
  "main": "main.js",
  "scripts": {
    "dev": "node esbuild.config.mjs",
    "build": "node esbuild.config.mjs production",
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "keywords": [
    "obsidian",
    "semantic-search",
    "embeddings"
  ],
  "author": "Jacob Mei",
  "license": "MIT",
  "devDependencies": {
    "@huggingface/transformers": "^4.0.1",
    "@types/node": "^22.0.0",
    "@types/sql.js": "^1.4.11",
    "esbuild": "^0.28.0",
    "happy-dom": "^20.9.0",
    "obsidian": "^1.13.1",
    "sql.js": "^1.14.1",
    "typescript": "^5.7.0",
    "vitest": "^4.1.6"
  },
  "dependencies": {
    "hdbscan-ts": "1.0.17"
  }
}

```

## Top-level layout

- .github/ (dir, 2 files, ~80 lines)
- .gitignore (~39 lines)
- CHANGELOG.md (~282 lines)
- docs/ (dir, 20 files, ~15874 lines)
- esbuild.config.mjs (~265 lines)
- LICENSE (~21 lines)
- manifest-beta.json (~10 lines)
- manifest.json (~10 lines)
- package-lock.json (~3010 lines)
- package.json (~33 lines)
- README.md (~306 lines)
- README.zh-TW.md (~306 lines)
- scripts/ (dir, 7 files, ~758 lines)
- src/ (dir, 96 files, ~16409 lines)
- styles.css (~491 lines)
- test/ (dir, 82 files, ~8692 lines)
- tsconfig.json (~19 lines)
- vitest.config.ts (~18 lines)

