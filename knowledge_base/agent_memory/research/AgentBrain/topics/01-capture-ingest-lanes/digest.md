> [[../../index|Research]] | [[../../overview|Overview]] | [[../../digest|Digest]]

# capture and ingest lanes

**In one sentence:** Capture across these systems is a local-first, provenance-preserving lane from heterogeneous sources (clipboard, chat, platforms, libraries, folder drops) into a typed store, with cloud calls confined to opt-in transcription or enrichment.

## Key points
- Platform capture is subtitle-first and dependency-gated: Bilibili/YouTube via `yt-dlp`, local A/V via on-device transcription, and Markdown/TXT/PDF-text import on stdlib only, landing as frontmatter Markdown with attachments in a vault inbox [[research_topics/agent_memory/Chubbyskills/summary|Chubbyskills]].
- Desktop capture is clipboard-first with an explicit keep-gate: any copy raises a 10-second auto-dismissing popup, only kept text/image/link items persist to local SQLite, and URL copies get full-text fetch including WeChat/X handling [[research_topics/agent_memory/OpenWiki/summary|OpenWiki]].
- Conversational capture needs no commands or categories: Telegram voice, text, photos, documents, and forwards are accepted, voice goes to Deepgram for transcription, and the agent classifies everything into typed vault cards [[research_topics/agent_memory/AgentSecondBrain/summary|AgentSecondBrain]].
- Library ingest reads the owner's store directly instead of re-parsing per query: a resident C++ core indexes `zotero.sqlite` + `storage/` with BM25 passage ranking (~15 ms), while group content arrives via Zotero Web API sync [[research_topics/agent_memory/Docsagent/summary|Docsagent]].
- Bulk-corpus ingest is folder-drop plus staged build: files land in `original_doc/`, then compile into structured multimodal JSON-plus-markdown evidence bundles (layout, notes, chart-text, sheet structure preserved) with incremental rebuild on changes [[research_topics/agent_memory/DocMason/summary|DocMason]].
- Every lane preserves provenance at capture time: source URLs, schema-v1 task IDs with SHA-256 digests, global entry ids, source-app attribution, or exact file-and-page identity, plus Markdown export for portability [[research_topics/agent_memory/Chubbyskills/summary|Chubbyskills]] [[research_topics/agent_memory/OpenWiki/summary|OpenWiki]] [[research_topics/agent_memory/Docsagent/summary|Docsagent]] [[research_topics/agent_memory/DocMason/summary|DocMason]].
- Ingest feeds an incremental retrieval lane, not a dead drop: auto-synced indexes with dedup/queue/retry, token-budgeted ranked search, nightly classification with MOC rebuild, and validation gates that fail bad data instead of publishing it [[research_topics/agent_memory/Chubbyskills/summary|Chubbyskills]] [[research_topics/agent_memory/Docsagent/summary|Docsagent]] [[research_topics/agent_memory/AgentSecondBrain/summary|AgentSecondBrain]] [[research_topics/agent_memory/DocMason/summary|DocMason]].

---
## What the sources agree on
All five keep the capture-to-store path local by default and push network or model calls to explicit opt-in edges (transcription providers, enrichment APIs, Jina Reader/Translate, group sync). All five preserve source identity at ingest time rather than recovering it later. All five treat ingest as the head of a maintained pipeline — index, dedup, sync, or rebuild — rather than one-shot filing.

## Where they differ
The lanes start from different mouths: OS clipboard (OpenWiki), Telegram chat (AgentSecondBrain), platform subtitle/transcription APIs (Chubbyskills), an existing Zotero library (Docsagent), and bulk folder drops (DocMason). The keep-decision differs too: human-gated per item (OpenWiki popup, Chubby queue/retry dedup) versus agent-classified with nothing silently dropped (AgentSecondBrain) versus build-validated publishing (DocMason). Transcription strategy splits between subtitle-first reuse (Chubbyskills), Deepgram cloud calls (AgentSecondBrain), local whisper/FunASR stacks (Chubbyskills), and structure-preserving Office/PDF renderers (DocMason, LibreOffice plus PDF stack).

## Evidence quality
All claims rest on per-source `summary.md`/`digest.md` syntheses grounded in README-level and config-level citations (commands, config keys, tool contracts); Rust/C++ internals, index schemas, and handler-level code were out of scope in several underlying wikis and are not asserted here. Two caveats carry over: OpenWiki's default-on Jina Reader/Google Translate exceptions weaken its local-first framing, and Chubbyskills' PDF import is text-layer only with no OCR, so image-only scans fail at ingest.

## Sources in this sub-topic
| source | kind | what it contributes |
|---|---|---|
| Chubbyskills | fresh | Subtitle-first platform ingest, local transcription/import, vault inbox products, queue/retry/dedup, evidence-brief export |
| OpenWiki | fresh | Clipboard keep-gate capture, URL full-text fetch, local SQLite store, Markdown export |
| AgentSecondBrain | fresh | Telegram voice/text capture, Deepgram transcription, agent classification into typed vault cards |
| Docsagent | fresh | Zotero-native resident BM25 index, 8-tool MCP contract, governed write gate |
| DocMason | fresh | Folder-drop bulk ingest, multimodal evidence bundles, validation-gated incremental publish |
