> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# chubbyguan/chubbyskills — In Plain Language

Think of Chubby Skills as a personal clipping service for the AI age.
You save videos, podcasts, articles, and your own notes, and it turns
them into a tidy local library your AI assistant can actually quote from.

## What is this about?

Chubby Skills is a toolkit with 14 ready-made "Agent Skills" plus one
command-line program that ties them together.

In plain terms: instead of bookmarks scattered across YouTube, Bilibili,
Xiaohongshu, WeChat, and your hard drive, you get one local folder — a
"vault" — full of plain Markdown notes with their sources attached.

The basic flow is simple:

1. Point it at a link or a file on your computer.
2. It saves the content as a Markdown note, keeping the title, source
   link, date, and any attachments.
3. You search that library with keywords whenever you need something.
4. You export a "brief": a topic pack with exact quotes, line numbers,
   sources, and checksums, ready for an AI agent to turn into an article,
   video script, or study notes.

The simplest path — importing your own Markdown or text files, searching
them, and exporting a brief — needs nothing extra: just Python, no
add-on packages, no API keys, no AI models.

Heavier jobs need extra tools, installed only when you need them: a
subtitle downloader for YouTube and Bilibili, transcription software for
local video and podcast audio, and a PDF reader for WeChat articles and
reports.

## Why does it matter?

Creators and researchers drown in saved-but-unusable material. A video
you watched last month, a podcast episode, a thread of article
screenshots — none of it is searchable when you sit down to write.

This project solves three everyday pains:

- **Scattered sources.** Six video skills, one podcast skill, and three
  article skills cover the platforms where material actually lives, so
  everything lands in one place in one format.
- **Unverifiable AI help.** When you ask an AI to work from your material,
  it usually paraphrases loosely. Here the brief carries verbatim quotes
  with line numbers and file digests, so every claim traces back to the
  exact source line.
- **Privacy and cost.** The core loop — import, search, export — runs
  entirely on your own machine. Your notes never leave your computer
  unless you explicitly switch on a cloud option.

It also respects platform rules and copyright: the skills are meant for
personal study and research, and the code license grants no rights over
other people's content.

## How does it work?

Picture a small assembly line with five stations, all driven from one
command, `tools/chubby.py`:

**1. Set up the vault.** You run `init --vault` once, which creates your
library folder and a small config file. A typical vault has an inbox for
incoming notes and an output folder for finished briefs.

**2. Collect material.** You `import` local files or `ingest` platform
links and audio. Subtitles are preferred for online video (fast and
accurate); local audio is transcribed on your own machine. PDF import
reads the text layer only — a scanned photo of pages will not work
because there is no text to extract.

**3. Stay organized automatically.** After each import the search index
updates itself. Importing the same file twice reuses the good copy
instead of duplicating it; changed files get a fresh copy while the old
one is kept. A queue file lets you process a whole list of links in
batch, with retry commands for failures.

**4. Find things.** Keyword search works out of the box with no extras.
An optional lightweight semantic search can catch similar wording. An
optional MCP service exposes the same search to AI agents directly,
offering tools like search, read the source, list recent notes, and
show statistics.

**5. Export evidence packs.** You run `brief --topic` with a keyword and
get two files: a readable Markdown brief and a matching data file with
exact excerpts, line numbers, sources, and checksums. A validator script
checks that every output follows the project's schema. The brief never
judges whether the sources are true — it just hands you cited material
so you or your agent can check context before quoting.

Setup comes in layers — light, video, podcast, WeChat, or everything —
so you install only the heavy transcription and parsing software your
material actually needs.

## Where can this be used?

- **Content creators** gathering video subtitles, article graphics, and
  podcast transcripts into reusable material for new videos, posts, or
  newsletter issues.
- **Researchers and students** keeping papers, reports, and their own
  notes in one searchable vault, then exporting cited topic packs with
  flashcards or study notes via the workflow skills.
- **Newsletter and trend writers** running the intelligence-radar skill
  to scan multiple sources and assemble sourced trend briefs.
- **Teams with an AI assistant** that needs grounded answers: the agent
  reads from the local vault through the skill packs or the MCP tools
  instead of guessing from memory.
- **Privacy-conscious users** who want transcription and search to stay
  on-device, switching on cloud transcription or AI enrichment only for
  specific jobs where they accept the cost and data transfer.

It runs on macOS and Linux with Python 3.11 or 3.12, and the project
reports 220 automated tests plus continuous checks on both systems.

## Conclusions & takeaways

Chubby Skills is not another note-taking app or chatbot. It is plumbing
between the messy web and careful AI-assisted writing: platform links
and local files go in, cited evidence packs come out.

Three things to remember:

1. **Markdown first.** Everything becomes ordinary text files you can
   open in any editor — no lock-in, no mystery database.
2. **Evidence, not answers.** It collects and cites; judging truth and
   writing the final piece stays your (or your agent's) job.
3. **Local by default, cloud by choice.** The free, private core covers
   most needs; each cloud feature is opt-in, with credentials you supply
   and costs you can see.

If you save a lot of content and want your AI to quote it back honestly,
this is the kind of boring, reliable infrastructure that makes that
possible.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Agent Skill | A ready-made instruction pack that teaches an AI assistant one job, such as transcribing a video. |
| Vault | Your local library folder where all saved notes and attachments live. |
| Ingest / import | Bringing outside material (a link) or your own files into the vault. |
| Brief (evidence pack) | An export file bundling exact quotes, line numbers, and sources on one topic. |
| Frontmatter | A small header at the top of each note recording title, source, and date. |
| Semantic retrieval | Finding notes by similar meaning, not just exact words. |
| MCP service | A standard plug that lets an AI agent search and read your vault directly. |
| Enrichment | Optional AI extras like auto-summaries, key points, or tags. |
| Transcription | Turning spoken audio or video into written text. |
| Text layer (PDF) | Selectable text inside a PDF; scanned page photos have none, so they cannot be imported. |
