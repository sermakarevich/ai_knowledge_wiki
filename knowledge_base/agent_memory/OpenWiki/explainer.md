> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# kdsz001/OpenWiki — In Plain Language

## What is this about?

OpenWiki is a desktop app for macOS and Windows that turns things you copy into a personal knowledge base.

The core idea is simple: copy anything — a paragraph, a picture, a link — and a small popup appears. If you choose to keep it, the app saves it. If you ignore it, it disappears after 10 seconds and nothing is stored.

Everything you keep lives in a database on your own computer, not in someone else's cloud. Then built-in AI organizes your saved bits into wiki pages, draws a map of how your ideas connect, answers questions about what you saved, and writes you a weekly summary of what you have been paying attention to.

Think of it as a clipboard with a memory and a librarian: the clipboard catches things, the memory keeps them locally, and the librarian sorts them and reminds you what matters.

## Why does it matter?

Most people copy dozens of things a day — quotes, links, screenshots, article snippets — and then lose them. Browser bookmarks go stale, notes apps fill up with unsorted clutter, and good ideas vanish.

OpenWiki matters for three reasons:

1. **It captures without friction.** You do not have to open an app or file something away. You just copy, as you already do, and decide in one click whether to keep it.

2. **It is private by default.** Notes and research can be sensitive. Keeping the database on your own machine means your reading habits and half-formed ideas are not uploaded somewhere just to be organized.

3. **It organizes for you.** Saving is only half the battle; finding things later is the other half. Automatic wiki pages, a visual graph of connections, search, and a weekly review mean your pile of clippings becomes something you can actually reuse.

In short: less losing things, less manual filing, more trust about where your data lives.

## How does it work?

The system works in five everyday steps:

1. **Copy something.** Whenever you copy text, an image, or a URL, a small popup appears near your work. It knows which app you copied from. You can also summon it by hand with a keyboard shortcut (`Cmd+Shift+C` on Mac, `Ctrl+Shift+C` on Windows).

2. **Decide to keep or ignore.** Click keep and the item is saved; do nothing and the popup closes itself after 10 seconds. Nothing is saved unless you say so.

3. **Everything lands in one local store.** Saved items live in a SQLite database on your computer. You can filter by type (text, image, link) or by time, search across everything, and export to Markdown files when you want to take your notes elsewhere.

4. **AI sorts it into a wiki.** The app groups your captures into pages about concepts, people, and topics, draws a knowledge graph showing how they link together, and flags problems like orphan pages with no links or broken links. An Ask sidebar lets you ask questions and get answers based only on your own saved content.

5. **You get a weekly debrief.** With one click, the app writes a report on what you captured that week, broken into seven angles: a quick glance, what you keep returning to, what you abandoned, what you might be missing, hot topics, a visual heatmap, and suggested next actions. Liking or dismissing items teaches it your tastes over time.

To power the AI features, you connect your own AI account — Anthropic Claude, OpenAI, or Google Gemini — using an API key or login, and pick a model in Settings. The app itself sits in your system tray, supports dark and light themes, and can even connect to Claude Desktop.

Two honest exceptions to "fully local": if you ask it to read a full article from a link, it may send that URL to a reading service (Jina Reader), and the Chinese interface may send foreign-language text to Google Translate. Both are on by default but can be switched off independently in Settings.

## Where can this be used?

- **Personal research.** Students, writers, and curious readers collecting quotes, papers, and articles can keep one searchable place instead of scattered bookmarks and screenshots.
- **Work knowledge.** Product managers, designers, analysts, and developers tracking competitor pages, specs, error messages, and inspiration images can build a shared-with-themselves reference.
- **Reading social feeds.** People who copy threads from X/Twitter, posts from WeChat, or web articles can have the app fetch the full text so the saved copy stays useful.
- **Weekly reflection.** Anyone who wants a Friday-style review — "what did I actually focus on this week?" — can use the attention report to spot obsessions, blind spots, and next steps.
- **Privacy-sensitive notes.** Journalists, researchers, or anyone handling confidential material gets local-first storage instead of pasting everything into a cloud notebook.
- **Building in public.** Because content exports to Markdown, saved research can flow into blogs, docs, or other wiki tools.

Under the hood it is a Tauri 2 desktop app (a lightweight web-frontend-plus-native-shell approach) with a React interface and a Rust backend — but as a user you just see a fast desktop app with a tray icon.

## Conclusions & takeaways

- OpenWiki's bet is that **capture should be effortless but saving should be a choice**. The 10-second popup is the whole philosophy in one interaction: catch everything, keep only what you mean.
- Local-first storage plus optional AI is a practical middle ground: your data stays home, while the heavy thinking is borrowed from a model provider you choose.
- The real value is not saving more — it is **reviewing better**. Wiki pages, the graph, and especially the weekly report turn hoarding into understanding.
- Watch the two network exceptions (link reading and translation) if you need strict offline privacy; they are disclosed and disableable, but they are on by default.
- For anyone drowning in copies, tabs, and screenshots, this is a calm alternative: copy as usual, keep deliberately, and let the app do the filing and the summarizing.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Capture popup | The small window that appears when you copy something, asking if you want to keep it. |
| SQLite database | A simple file-based store on your computer that holds everything you kept; no server needed. |
| Wiki pages | Auto-written summary pages for each topic or person in your captures, like a personal encyclopedia. |
| Knowledge graph | A visual map of dots and lines showing which saved ideas connect to each other. |
| Ask sidebar | A chat panel where you ask questions and get answers drawn from your own saved content. |
| Orphan / broken link | An orphan page is one nothing links to; a broken link points somewhere that no longer exists. |
| Attention analysis | The weekly report's seven-way breakdown of where your focus went and what you ignored. |
| API key / OAuth login | Two ways to connect your AI account: pasting a secret code, or clicking "log in with" your provider. |
| System tray | The corner of your screen where small background apps live so they stay running without a window open. |
| Markdown export | Saving your notes as simple portable text files that any notes app or blog tool can open. |
| MCP integration | A standard plug that lets the app share context with Claude Desktop, an external AI assistant. |
