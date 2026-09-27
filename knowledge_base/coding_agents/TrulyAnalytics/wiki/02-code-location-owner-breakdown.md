> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Surviving LoC Stacked by Code Location & Owner
**In one sentence:** Surviving AI code concentrates in `src` Go scaffolding, JSX/JavaScript frontend boilerplate and generated docs, while the human owns the client analytics code, infrastructure/auxiliary directories, most commits, and all significant deletions.
## Key points
- In `src`, surviving Go is close to 50/50, slightly human-led: AI 2,211 lines vs human 2,671 lines of 4,882 total (45.3% AI / 54.7% human).
- HTML is human-led (870 human vs 519 AI surviving lines of 1,389 total, 37.4% AI), described as Codex providing the testing framework and the human tuning it over time.
- JSX (607 AI vs 474 human, 56.2% AI) and JavaScript (683 AI vs 310 human, 67.3% AI) are both AI-led; the simple `app.jsx` is AI-dominant and one of the largest files.
- The `client` analytics code delivered to browsers is almost entirely human-owned: 1,654 human vs 353 AI surviving lines of 2,007 total (82.4% human), effectively refactored by the human post-release.
- Auxiliary directories are human except docs: ansible is human-managed (custom modules read, implemented and tested directly by the human), project root is human boilerplate (Dockerfile, docker-compose.yml, .gitignore), `k8s` is simple human-managed manifests, while `docs` is entirely AI-generated.
- The largest files are all AI-dominated — Go server/routing code (`server.go` / file-17.go), `app.jsx` (file-01.jsx, biggest file), and the database store (file-09.go, ~700 LoC) — versus a human preference for ~300-line files rarely exceeding 500 lines.
- Churn and commits are human-led: human made 107 of 137 commits (78.1%) vs AI 30 (21.9%); the human deletes with abandon (outlier: 0 added / 900+ deleted) while AI dumps code in (outlier: 800 added / 150 deleted), and the biggest human commit added 1,414 lines while deleting over 1,000.
---
## Surviving LoC by code location
Codebase is segregated across root directories; the real codebase is in `src` and `client`, everything else is auxiliary tooling:

- `src` — main codebase: backend exclusively in Go, plus large frontend (HTML, JSX, JavaScript); the `src` frontend is the admin panel and proxy control system UI.
- `client` — frontend analytics code delivered to users.
- `ansible` — custom playbooks and modules for provisioning Google Analytics properties.
- `[root]` — files at project root, usually tooling configuration.
- `html` — locally hosted testing pages for analytics.
- `scripts` — local development scripts.
- `docs` — "documentation I think, Im a senior engineer so I've never looked at the docs".
- `sql` — database schemas and migration code.
- `k8s` — manifests and playbooks for deploying the proxy and admin server to Kubernetes.
- `nginx` — nginx configuration for local testing assets.
- `.vscode` — "no idea, never look at it, probably crap from vscodium".

Ownership by location:

- `src` Go: AI 2,211 vs human 2,671 surviving lines — close to 50/50, slightly human.
- `html` testing suite: 870 human vs 519 AI surviving lines — "Codex gave the framework and the lump of flesh tuned it up over time."
- JS and JSX are both AI-led (per-file breakdown follows in next section).
- `client`: human 1,654 vs AI 353 surviving lines (82.4% human); "Post-release, this entire directory has effectively been refactored by the human, so it's now entirely my problem."
- `ansible`: AI partially contributed to original structure but effectively fully human-managed; "All HTML and Python code in this directory was read, implemented and tested directly by the human"; assisted via web interface "more of a stack overflow than a stand alone agent".
- Project root: "entirely an experienced developer putting together and copying over previously managed code, including Dockerfile, docker-compose.yml, .gitignore and other baggage and boilerplate."
- `docs` is entirely AI-generated "because, frankly, the human did not need to care that much about it"; `k8s` is "very simple and human-managed, it's a few manifests templated and handled with ansible copied from other projects."
- Summary: "That means most AI code went into basic Go structure, UI frontend boilerplate / styling and the majority of the interactive elements of the frontend app."

## Surviving LoC stacked by file type & owner
| Area / language | AI lines | Human lines | Total lines | AI share | Human share |
|---|---|---|---|---|---|
| Go | 2,211 | 2,671 | 4,882 | 45.3% | 54.7% |
| HTML | 519 | 870 | 1,389 | 37.4% | 62.6% |
| JSX | 607 | 474 | 1,081 | 56.2% | 43.8% |
| JavaScript | 683 | 310 | 167 | 67.3% | 32.7% |
| Client analytics code | 353 | 1,654 | 2,007 | 17.6% | 82.4% |

Note: JavaScript total is stated as 167 in the chunk table despite 683 + 310 components; reproduced verbatim.

Mechanisms behind AI survival:

- Two Go files with strong AI presence handle server routing, basic server management, database connectivity and SQL queries.
- No ORM: "it uses SQL code directly in the provisioning, migrations and the queries from the application. The AI generated the boring scaffold code turning the raw SQL rows into the detination Go structs."
- Once retrieved, "the human could do what he wanted across the rest of the codebase so the Go code performing these lookups was mostly written once and left to it" — AI provided "the core replacement mechanic for populating objects, effectively replacing an ORM".
- Kubernetes-job Go code: same scaffold pattern — AI handled "authentication, connection and communication to and from the Kubernetes API" via a standard library (service-account or local client config), while "the data passed to and from these Kubernetes jobs were human-configured".
- HTML upgrade-page styling plus SES email templates: "The AI basically one shot all of this stuff so I didn't need to make changes. Good botto."
- SES Go code persisted for the same reason as Kubernetes — "a standard framework that has a known setup with common conventions".
- Cache Go code (in-memory caching, updates, removals): "A cache is simple to build and Go is pretty much engineered for network connected cache management so once again, it could be copied off the internet basically verbatim using a conventional implementation."

## File size vs ownership
- "All of the largest files are AI-dominated. The top three largest files are about three times the size of the average file or more": Go server code handling web-request mechanics (`server.go` / file-17.go), `app.jsx` (file-01.jsx, currently biggest), and database store (file-09.go, ~700 LoC).
- "The human tends to prefer files around 300 lines long. AI does have some dominant files in that same range, but the human does not really go beyond 500 lines and clearly likes to cluster in a few hundred lines of code."
- "My vscode on my main monitor does 106 lines on screen at once, so generally 2-5 screens per file is what I can tolerate. That is clearly the point where I get sick of scrolling, now it is mathematically quantified."
- "I care. Botto does not care."

## File churn by commit scatter
Each dot maps lines added and deleted per individual commit per file:

- "The human clearly deleted a lot of lines and would make commits that were simply deletions, with no additions. What a chad."
- "AI, by contrast, would make commits that added hundreds of lines without removing anything. What a psychopath."
- "There were more human commits overall, but the behavioural pattern is obvious - AI shoves that code in and hoards what it can. The human deleted things with wild abandon. The graph weighs up and to the left for the human, then down and to the right for AI."
- Outliers: "One human commit added zero lines and deleted more than 900 lines of code. One AI commit added 800 lines and deleted only 150."

## Daily lines added / deleted by human / AI
Per-day added/deleted lines by "the toaster and the petri-dish":

- "At the beginning, AI was dominant. It set up the basic code and smashed in two major commits of more than 1,000 lines"; then "large human spikes, including two commits of around 1,500 lines"; "One large-scale AI commit of around 1,200 lines landed in the middle of those two major human commits but came alongside a huge deletion streak by the fleshbag."
- "AI took a back seat for a while whilst the humie took over the main duties at a calmer pace before the Botto was once again summoned towards the v1 release. Overall things went hard during the first two thirds of May then went through a couple weeks of refinement afterwards."
- "There were more human commits and more human deletions. AI made very few deletions. Its pattern was large swathes of code dumped in, followed by human commits with large additions and, in most cases, healthy ratios of deleted lines."
- "The biggest human commit added 1,414 lines while also deleting more than 1,000 lines. That is behaviour the AI never matched."

## Overwrite heatmap by file type
- "The human overwrote AI code predominantly in Go and JavaScript, but did not touch the JSX much at all. JSX was one of the major surviving AI contributions."
- "The only place where AI did not have human overwrites was Markdown, almost certainly documentation that the human didn't read. The AI claimed this land."
- "AI never touched the Ansible code the human made, any JSON the human wrote or any shell scripts. Every other language in the repository needed human touch-up on AI contributions."

## Share of commits
| Contributor | Commits | Share of commits |
|---|---|---|
| Human | 107 | 78.1% |
| AI / Codex | 30 | 21.9% |
| Total | 137 | 100% |

- "The human made 107 out of 137 commits. That is 78.1% of all commits."
- "AI made 30 out of 137 commits. That is 21.9% of all commits."
- "That ties reasonably closely to the amount of surviving code, but the AI code was not particularly strong in terms of how long it lasted."
- "To understand the real contribution, the non-quantifiable measures matter as well."

**Covers:** Per-directory and per-language AI vs human ownership, AI-dominant areas, file-size pattern (chunk 02-surviving-loc-stacked-by-code-location-owner)
