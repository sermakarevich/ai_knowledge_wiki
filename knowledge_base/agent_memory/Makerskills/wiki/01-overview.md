> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** makerskills is a plugin of 21 documentation-first AI agent skills for founder/operator workflows (decisions, research, knowledge bases, content, CFO, domains) that run on Claude Code, Codex, Cursor, and other Agent Skills hosts.
## Key points
- The repo's job is "AI agent skills for the personal operator's craft" covering decisions, research, second-brain workflows, content rotation, scenario modeling, CFO cadence, domain hunts, and meta-skills for authoring more skills (README:11).
- It targets founders and indie operators and works with Claude Code, Codex, Cursor, and other Agent Skills hosts, with site maker-skills.com (README:13, README:15).
- Installation is via `/plugin marketplace add coreyhaines31/makerskills` + `/plugin install makerskills@makerskills`, or a symlink for local dev (`git clone ... ~/code/makerskills` + `ln -s ... ~/.claude/plugins/makerskills`), with env/personal-config details deferred to INSTALL.md (README:26-38).
- The first-touch pattern is structured input → structured output → written to disk, exemplified by `/decide` picking questions from the 37signals framework and archiving with a revisit date (README:56-62).
- Each skill is a workflow doc invocable as `/decide` or by reading `skills/decide/SKILL.md` and running steps by hand; "the plugin is documentation-first; the automation is a side effect" (README:64-70).
- A 21-row routing table maps operator intents ("I want to...") to skills, and each skill's SKILL.md description carries trigger phrases plus disambiguation from adjacent skills (README:88-114).
- Skills compose by calling each other by name instead of reimplementing, with central hubs `watch-video` (54 refs), `skillify` (51), `second-brain` (48), `slide-deck` (38), `company-brain` (33), `domain` (32) (README:173-186).
- The repo is "public + generic" with personal data kept out of the repo — but the Architecture section is truncated mid-sentence in this chunk so the full separation mechanism is not visible here (README:194-199).
---
## Install
Verbatim setup (README:26-38):
```bash
# In Claude Code
/plugin marketplace add coreyhaines31/makerskills
/plugin install makerskills@makerskills
```
Local-dev alternative:
```bash
git clone https://github.com/coreyhaines31/makerskills ~/code/makerskills
ln -s ~/code/makerskills ~/.claude/plugins/makerskills
```
Details on env vars, personal-config setup, and runtime dependencies live in `INSTALL.md` (README:38).
## Getting started — 5-minute path
Ordered path for newcomers (README:46-80):
1. Install plugin, then set base env var in `~/.zshenv` (README:48-52):
```bash
export MAKERSKILLS_CONFIG="$HOME/.config/makerskills"
```
then reload shell.
2. Run `/decide` first — no config required; it asks what decision is faced, triages questions from the 37signals framework, archives with a revisit date (README:56-62).
3. Read one `SKILL.md` to see the pattern, e.g. `open ~/code/makerskills/skills/decide/SKILL.md` (README:64-68).
4. Try `/paste twitter` — reads clipboard, strips formatting, warns over 280 chars, copies back cleaned output; pure utility, no config file (README:72-78).
5. Skim the 21-skill list and adopt the skill mapping to an already-manual workflow (README:80).
## Which skill do I invoke when?
Full routing table, intent → skill (README:90-112):
| I want to... | Skill |
|---|---|
| Think through a decision with a real fork | `decide` |
| Break through a wall ("this seems impossible") | `unstuck` |
| Get a board of famous founders to weigh in | `maker-council` |
| Pressure-test a new business or product idea | `business-brainstorm` |
| Research a topic with citations | `deep-research` |
| Find an available `.com` for a new project | `domain` |
| Capture / query / lint my personal knowledge base | `second-brain` |
| Same but for a team-shared knowledge base | `company-brain` |
| Extract notes / highlights / summaries from a book | `read-book` |
| Extract a transcript or key moments from a video | `watch-video` |
| Turn a call transcript or client message into issues + reply | `ingest` |
| Fetch any social post by URL as structured data | `social-fetch` |
| Plan / draft social content rotation across a portfolio | `jab-hook` |
| Draft, update, convert, or export a slide deck | `slide-deck` |
| Clean terminal output for Slack / LinkedIn / X / Notion etc. | `paste` |
| Manage projects across businesses (kanban) | `pm` |
| Model personal financial scenarios (house, cash flow, etc.) | `personal-cfo` |
| Run monthly / weekly CFO for a company or agency | `company-cfo` |
| Create, adapt, or update a skill | `skillify` |
| Wire up an integration / API / MCP into a project | `toolify` |
| Set up an agent loop or scheduled task | `loopify` |
## Meta — extend Claude Code (the `-ify` trifecta)
| Skill | What (README:122-125) |
|---|---|
| `skillify` | Create, adapt, or update a skill in any sibling repo. Three modes: CREATE (from-chat / from-video / from-dump / from-scratch), ADAPT (port external skill with license check + attribution), UPDATE (improve existing skills with cross-skill propagation + semver discipline). |
| `toolify` | Wire up an integration, API, MCP server, or third-party service into a Next.js or Rails project. Interactive wizard for auth, env vars, client wrapper, webhook handling, and smoke-test. |
| `loopify` | Set up an agent loop, cron-scheduled task, or recurring workflow. Judgment layer on top of `ScheduleWakeup` / `CronCreate` / `/loop` — picks pattern (dynamic / cron / one-shot), tunes delay for cache windows, enforces idempotency + bail-out conditions. |
## Decision & strategy
| Skill | What (README:132-137) |
|---|---|
| `decide` | 37signals decision framework (38 questions + house additions like Q39 opportunity cost, triaged to 6–8 per decision). Archives with revisit dates. |
| `business-brainstorm` | Pressure-test a new business or product on 9 dimensions. Composes with `deep-research` + `domain`. |
| `domain` | 11-step .com domain hunt on Laura Roeder's "availability-first, never fall in love with a name" methodology. Multi-tool ensemble: Vercel CLI + whois (per-TLD) + Domainr API + Namecheap API + `rdap.org` (modern TLDs) + `agent-browser` for USPTO trademark screening + aftermarket click-throughs (HugeDomains / Afternic / Sedo / Dan). Handles bare-word + prefix/suffix brainstorming, budget filtering, negotiation guidance, and social handle checks. |
| `deep-research` | Multi-source research with citations + archive. WebSearch, WebFetch, `agent-browser`, `/last30days`, memory. |
| `unstuck` | The roadblock antidote. Classifies what kind of "no" you hit (assumption / framing / gatekeeper / tool / resource / physics), runs targeted lateral-thinking techniques from a 10-technique inventory, 10-angle minimum before evaluating. Agents run it on themselves before reporting any dead end. Upstream of `decide`. |
| `maker-council` | Simulated personal board of advisors — Fried, Musk, Bezos, Jensen, Iger, Graham, Naval, Blakely. Seats 3–5 by question type with a designated dissenter, grounds takes in documented frameworks (optional live-research pass), maps the disagreements, synthesizes a call. Custom members via config dir. |
## Knowledge & content consumption
| Skill | What (README:144-148) |
|---|---|
| `second-brain` | Karpathy LLM Wiki workflow over any markdown vault. Capture / compile / query / lint / connect / search. Personal-scope. |
| `company-brain` | Team-scope sibling to second-brain. Structured raw dirs (people / companies / meetings / sops / decisions / customer-language / recurring-questions / sales-objections), multi-author attribution, sensitivity tagging, trust levels + a `/cb review` culling pass so unreviewed or deprecated info never poisons answers, optional auto-sync from Fathom / Gong / Granola / CRM. |
| `read-book` | PDFs, EPUBs, MOBI, markdown — chapter-by-chapter notes, quotes, summaries, or spaced-rep study mode. |
| `watch-video` | YouTube, Loom, Vimeo, Riverside, Zoom, MP4. Transcript / visual / multimodal (Gemini-native) modes. |
| `ingest` | Raw human input — call transcripts (Grain/Zoom/Granola/Fathom), client texts, emails, voice notes — extracted into decisions, action items (yours vs theirs), filed GitHub issues, vault captures, and a drafted-never-sent reply. Person→project routing via private `people.yaml`. |
## Output & creative; Operations & utilities
Output & creative (README:155-156): `jab-hook` applies Gary Vee's jab-jab-jab-right-hook rhythm to portfolio rotation on X + LinkedIn via Typefully; `slide-deck` builds branded React decks (Next.js) with "show, don't tell" narrative pitching, density modes, PPT conversion, Playwright export.
Operations & utilities (README:163-167): `pm` is kanban (5-column) + Eisenhower across portfolio with tool-agnostic adapters (Notion, GitHub, Plane, Linear, Obsidian, manual); `personal-cfo` covers household-scope scenarios (house purchase + rental forecasting, monthly cash flow, big-purchase decisions); `company-cfo` covers team scope (monthly snapshots, weekly cash pulse, scenario projector; transaction-sum EOM methodology; pulls from bank + payment processor + payroll + expense-mgmt via `toolify`-wired integrations); `paste` cleans terminal output for 9 destinations with secret-detection first; `social-fetch` pulls any social post by URL across 10 platforms (X, LinkedIn, IG, TikTok, Bluesky, Reddit, Mastodon, Threads, HN) with free + paid fallback chain.
## Skills compose
Skills route to each other by name rather than reimplementing adjacent jobs; the most-referenced ("central") skills are adoption entry points (README:175-186):
| Most referenced by siblings | Composes with... |
|---|---|
| **`watch-video`** (54 refs) | `second-brain` (capture summary), `skillify from-video`, `social-fetch` (X/IG/TikTok metadata), `pm` (action items), `decide` (flagged decisions) |
| **`skillify`** (51 refs) | `watch-video` (record → skill), `second-brain` (capture source), `compound-engineering:*` (Anthropic-official skill authoring) |
| **`second-brain`** (48 refs) | `deep-research` (external gaps), `read-book` (highlights → wiki), `watch-video` (summaries → raw), `paste` (clean captures) |
| **`slide-deck`** (38 refs) | `business-brainstorm` (pitch decks), `watch-video` (talk-recording → outline), `second-brain` (wiki as content) |
| **`company-brain`** (33 refs) | `toolify` (wire auto-sync), `loopify` (schedule sync), `deep-research` (external gaps), `decide` (structured archive) |
| **`domain`** (32 refs) | `business-brainstorm` (name after idea passes filter), `toolify` (wire Domainr + Namecheap), `decide` (candidate fork) |
Full dependency lists live in each skill's `## Composes with` section (README:186).
## Architecture (truncated in chunk)
Chunk ends mid-sentence at "The repo is **public + generic**. Your personal data (Typefully workspace IDs, portfolio properties, voice" (README:194-195) and the macro-component list cuts off after `top-level-files/` (README:196-199). No further Architecture content is present in this chunk, so it is not summarised here.
**Covers:** README (makerskills repo overview: tagline, hosts, site, install, 5-minute path, 21-skill routing table, category tables, compose graph, truncated Architecture lead-in); INSTALL.md (referenced only for env vars / personal-config / runtime deps, not excerpted in this chunk); skills/*/SKILL.md (referenced by routing/compose tables, not excerpted in this chunk)
