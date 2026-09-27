> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: coreyhaines31/makerskills
*Solo-founder Agent Skills plugin (20–21 skills): judged only on what the digest and wiki evidence, never the source or the web.*

## Claims vs. evidence
- "Documentation-first; the automation is a side effect" — **supported.**
- A `SKILL.md` file IS the skill: markdown workflow logic Claude executes at invocation time, so iterating means editing markdown with no build step (ARCHITECTURE.md:150-161).
- "Skills compose by name instead of reimplementing" — **supported structurally, unproven in operation.**
- Reference counts are concrete (`watch-video` 54 refs, `skillify` 51, `second-brain` 48, `slide-deck` 38, `company-brain` 33, `domain` 32), but they count mentions across sibling docs, not successful invocations.
- "Routes operator intent to the right skill" — **partly supported.**
- The 21-row "I want to..." table plus per-skill trigger phrases and adjacent-skill disambiguation exist (README:88-114), yet FAQ admits cross-refs resolve at invocation time by description match with no manifest linking.
- The documented fix for misrouting is manual: invoke `/skill-name` explicitly (FAQ.md:112-130).
- "Public repo stays generic; personal data stays private" — **supported by design, convention-enforced.**
- The `MAKERSKILLS_CONFIG` split (`git pull` never touches `~/.config/makerskills`) plus `.gitignore` guards (`*.local.*`, archive paths) are real, but enforcement is gitignore plus discipline, not scanning or encryption.
- "Graceful degradation, free fallbacks, no telemetry" — **plausible but thin-evidenced.**
- INSTALL.md lists all API keys as optional with free fallbacks and direct-from-machine calls, yet there are no tests, logs, or failure-mode docs verifying any degradation path.
- Worked examples — **discounted as evidence.**
- EXAMPLES.md states it is "hand-authored illustrations, not literal captures," and the company-brain compile section truncates mid-sentence, so depth claims rest on author narrative.
- Versioning discipline — **documented, not demonstrated.**
- PATCH/MINOR/MAJOR rules for skills and plugin bumps are carefully specified, but no CHANGELOG or release history was present in the digest chunks to confirm they are followed.

## Genuinely new vs. repackaged
- Genuinely useful packaging: the `-ify` trifecta split — `skillify` (new knowledge), `toolify` (new capability), `loopify` (new cadence) — capped by an explicit Rule of 3.
- Compose-by-name with no manifest linking, including cross-plugin refs (`makerskills:paste`) resolved at invocation time, is a real simplification over plugin SDK wiring.
- The two-layer config contract (public repo + private `$MAKERSKILLS_CONFIG` overlay, migrated by copying one dir) and two-level semver (plugin tag plus independent per-skill `metadata.version`) are genuinely disciplined touches.
- Rituals-as-code stand out: revisit-dated decision archives, the `/cb review` culling pass so unreviewed info never poisons answers, idempotent cron with 3-failure bailout, transaction-sum EOM CFO cadence.
- Repackaged core: the intellectual content is attributed borrowing — 37signals decision questions (+house Q39), Karpathy LLM Wiki for second-brain, Gary Vee jab-jab-hook rotation, Eisenhower/kanban for `pm`, Laura Roeder availability-first domain hunting.
- Runtime pipelines are standard ensembles: yt-dlp + ffmpeg + MLX-Whisper for video, Vercel CLI + whois + Domainr + Namecheap + RDAP + USPTO-via-browser for domains, Typefully/Notion/Linear adapters elsewhere.
- Novelty verdict: the contribution is integration and operator ergonomics, not new methods — a well-organised bundle of other people's frameworks wired into Agent Skills conventions.

## Weaknesses and blind spots
- Sources disagree on scope: 21 skills in README/overview vs. 20 in ARCHITECTURE.md/INSTALL.md, which undermines the completeness and versioning story.
- Single-author, Mac-centric operator scope: `watch-video` needs MLX-Whisper, `paste` assumes `pbcopy/pbpaste`; FAQ concedes Linux/Windows need swaps with no matrix of what breaks.
- No evaluation layer: no tests, no success metrics, no telemetry (a privacy plus, an observability minus) — hub-load and multi-tool-ensemble reliability claims have no data.
- Description-based routing is fragile at scale: 20+ skills plus a 46-skill `marketingskills` sibling competing on trigger phrases, with manual invocation as the documented fallback.
- Secrets and multi-author trust rest on convention: keys in `~/.zshenv`, sensitivity tags and trust levels in markdown front-matter, archives in a cloud-synced dir the FAQ recommends but does not provision.
- Heavyweight tails: slide-deck assumes a branded Next.js repo with preview host, company-cfo assumes bank/processor/payroll integrations wired via `toolify` — adoption cost concentrates in the "central" skills newcomers are told to set up first.
- Simulated expertise (`maker-council` with Fried/Musk/Bezos personas, `business-brainstorm` 9-dimension scores) grounds takes in documented frameworks only optionally, so outputs risk confident pastiche without the live-research pass.
- Backlog signals sprawl pressure: eight candidate skills (`weekly-review`, `gh-triage`, `bjj-log`...) plus a productised-service brainstorm sit outside the Rule of 3, with no stated acceptance bar for new additions.
- Eight design principles (voice matters, cite everything, cadence over one-offs) are admirable but unmeasured — none has an associated check, lint, or review gate in the digested material.

## Applicability
- Direct reuse is narrow: domain hunts, Typefully rotation, household CFO, and personal wikis fit founders better than platform teams — but the construction patterns transfer broadly.
- The `/decide`-first onboarding (no config, no deps) is itself a transferable pattern: every skill bundle should have a zero-setup entry point that demonstrates the input → output → archive loop.
- Skills needing no runtime deps (`decide`, `paste`, `pm`, `personal-cfo`) are the realistic pilot set; everything requiring API keys, vault paths, or preview hosts is a second-wave cost.
- **Relevance to my work**
  - *AI/ML engineering:* adopt SKILL.md-as-executable-doc with description triggers + adjacent-skill disambiguation; copy the structured input → structured output → archive-to-disk loop with revisit dates for experiments and evals.
  - *Agentic systems:* copy compose-by-name hubs over reimplementation; keep the `-ify` separation (knowledge vs. capability vs. cadence); enforce `loopify`-style idempotency + bail-out guards on every scheduled agent; run the `unstuck` 10-angle gate before any agent reports a dead end.
  - *Elisity data platform:* mirror the public-generic vs. private-config split (safe defaults in repo, per-tenant overlay, gitignored archives); reuse the personal↔team sibling pattern (`second-brain`/`company-brain`, `personal-cfo`/`company-cfo`) for tenant vs. shared knowledge; require the `/cb review` culling + sensitivity-tagging pass before indexing vault content.

## What this changes
- Lowers my estimate of skill-authoring cost: markdown-only iteration with per-skill semver and cross-skill propagation is a credible lightweight alternative to a plugin SDK.
- Raises the value I place on routing hygiene (trigger phrases, adjacent-skill disambiguation, explicit fallback) and on config-layer separation as a first-class design decision rather than cleanup.
- Does not change my scepticism of scraped-platform skills (`social-fetch` across 10 networks, USPTO-via-browser) and simulated-expert councils — useful draft generators, not sources of truth, without evals.
- Practical takeaway: steal the scaffolding (two-layer config, compose graph, archive + culling cadence), trial two or three skills (`decide`, `skillify`, `second-brain`), and ignore the long tail until a manual workflow justifies each install.
- The strongest single idea to copy is also the smallest: every decision, capture, and research output lands on disk with sources, dates, and a revisit or review hook — memory that compounds instead of chat that evaporates.

## Verdict
- Worth a read for any team standardising agent skills; worth installing only where a founder-operator workflow already hurts.
- Evidence supports the architecture claims, not the reliability or portability ones, and the hand-authored examples plus truncated chunks cap how much can be trusted secondhand.
- Full-catalogue adoption would import Mac-centric deps, scraper brittleness, and trigger-phrase routing debt for workflows a platform team does not run — so the rational move is pattern-level adoption plus a narrow pilot, re-evaluated if evals or a stable MAJOR appear. **trial**
