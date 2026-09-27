---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: kdsz001/OpenWiki

### Q1. How does the copy-to-knowledge capture flow work, and what happens if the user does nothing?

> [!tip]- Answer
> > Anything copied on the desktop raises a capture popup supporting text, images, and URLs with automatic source-app detection, plus a manual `⌘⇧C` / `Ctrl+Shift+C` trigger. The popup auto-dismisses after 10 seconds and nothing is saved unless the user actively chooses to keep the item. See [[wiki/01-overview|Overview]].

### Q2. What is OpenWiki's privacy baseline, and what are its two disclosed network exceptions?

> [!tip]- Answer
> > The baseline is privacy-first local storage: all kept data lives in a local SQLite database. The two exceptions are URL reading, which can send the full URL to Jina Reader, and the Chinese UI, which can send foreign-language page text to Google Translate. See [[wiki/01-overview|Overview]].

### Q3. What does the AI knowledge base build from captures, and how can the user interrogate or audit it?

> [!tip]- Answer
> > AI compiles captures into Wiki pages of concepts, entities, and topics, plus a knowledge-graph view of how ideas connect. The user asks questions via the Ask sidebar grounded in their own content, while the system auto-detects orphaned pages, broken links, and structural issues. See [[wiki/01-overview|Overview]].

### Q4. What does the one-click weekly insight report contain, and how does it learn preferences?

> [!tip]- Answer
> > The report summarizes captured content through a 7-dimension attention analysis: At a Glance, Subconscious, Graveyard, Blind Spots, Hot Topics, Heatmap, and Action Items. Liking or dismissing report items trains the AI on the user's preferences for future reports. See [[wiki/01-overview|Overview]].

### Q5. What stack does OpenWiki build on, and what are its entry point, platforms, and key shortcuts?

> [!tip]- Answer
> > It is a Tauri 2 desktop app with a React 19 + Tailwind 4 + Zustand + Framer Motion frontend and a Rust + SQLite (rusqlite) backend built with npm and Vite 6. The Vite entry is `index.html` mounting `<div id="root">` and loading `/src/main.tsx`, shipping for macOS and Windows as a tray-resident app with `⌘⇧C` / `Ctrl+Shift+C` capture and `⌘⇧Y` / `Ctrl+Shift+Y` main-window shortcuts. See [[wiki/02-top-level-files|top-level-files]].

### Q6. What conventions govern secrets, agent workflows, and visual design in the top-level files?

> [!tip]- Answer
> > Secrets are templated by `.env.example` (`GEMINI_CLIENT_ID`, `GEMINI_CLIENT_SECRET`, `OPENAI_OAUTH_CLIENT_ID`) while `.gitignore` excludes real `.env` files but re-allows the example. `AGENTS.md` and `CLAUDE.md` define near-identical agent playbooks (permissions, decision protocol, commit-on-quot phrases, release flow, skill routing), and `DESIGN.md` normatively pins the Brutally Minimal system with warm `#F97316` accent, fixed type scales, and Lucide icons. See [[wiki/02-top-level-files|top-level-files]].

### Q7. Evaluate: should a privacy-sensitive researcher adopt OpenWiki over a cloud note app for a personal knowledge base?

> [!tip]- Answer
> > Recommend OpenWiki when local-only SQLite storage, explicit opt-in capture, and AI wiki/graph/reports over owned content outweigh cloud sync and collaboration needs. Do not recommend it when the workflow requires real-time sharing, managed backups, or zero tolerance for the two default-on network calls (Jina Reader, Google Translate) without first disabling them in Settings. See [[wiki/01-overview|Overview]].
