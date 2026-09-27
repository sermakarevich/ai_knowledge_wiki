> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: notoriouslab/vault-curate

## Claims vs. evidence
- Claim: "nothing leaves your machine by default" with a ~110 MB one-download model and no API key (01-overview.md:51). Evidence in digest is strong on intent: AI curation is off until enabled, and cloud exfiltration only happens if the user points it at a cloud service (01-overview.md:51).
- Claim: strong Chinese/CJK handling, including names, proper nouns, colloquial phrases, plus Traditional→Simplified normalization under the hood (01-overview.md:52, 01-overview.md:89). Evidence is assertion-level only: no benchmark, dataset, or precision/recall number appears in the digest or wiki chunks.
- Claim: three-engine search (Keyword + Semantic + Fuzzy title) merged into one ranking over full long notes up to 60,000 characters (01-overview.md:77, 01-overview.md:88). Plausible given the named stack (BM25+, embeddings, RRF k=60, sql.js per 02-top-level-files.md:1057), but no fusion weights, latency figures, or retrieval evals are cited.
- Claim: verdict-gated connections — suggestions only, one click promotes to a real wikilink, ✕ dismisses permanently across renames and rebuilds (01-overview.md:69, 01-overview.md:120). This is the best-evidenced claim: dismissal refill, Hidden-suggestions review, and bidirectional-promotion setting are all documented mechanics.
- Claim: phone reuse — build the index on desktop, sync it over, search on mobile with no re-index or re-download (01-overview.md:54). Conditional evidence: depends entirely on iCloud/Sync/Syncthing working, and mobile search reportedly falls back toward keyword mode where synonyms matter (01-overview.md:91).
- Claim: honest semantic paths — weakest-hop scoring with an explicit "not connected" notice when no strong chain exists (01-overview.md:113). Good sign, but the threshold values and the "actual numbers" shown are not quoted in the digest.
- Claim: relation graphs with typed edges — purple unlinked, gray wikilinked with direction, cyan Cold, green query-relevance — each run writing a fresh timestamped `.canvas` (01-overview.md:104, 01-overview.md:109). The rendering contract is specific; whether scores calibrate to human judgments is unevidenced.
- Claim: tag-fused ranking plus `description`-frontmatter signal and markdown-structure stripping in Find Similar (01-overview.md:89, 01-overview.md:90). Sensible feature engineering, but no ablation (tags on/off) is reported.
- Cross-check: bilingual documentation (English overview plus 307-line Traditional-Chinese README) and a pinned identity (vault-curate 1.11.0, minAppVersion 1.7.2, desktop+mobile) suggest a maintained release, not a demo (02-top-level-files.md:320, 02-top-level-files.md:764).

## Genuinely new vs. repackaged
- Repackaged: BM25 + dense embeddings fused with RRF, HDBSCAN clustering (hdbscan-ts 1.0.17), and Canvas graph export are standard 2023–2025 RAG/PKM practice, not inventions (02-top-level-files.md:363, 02-top-level-files.md:1057).
- Repackaged: Hot/Cold tiering by internal-link count plus recency with a tunable day window is a crude but legible heuristic, closer to a productivity convention than a retrieval breakthrough (01-overview.md:126).
- Genuinely thoughtful: the suggestion-never-edits UX contract — no background AI, every edge awaiting yes/no, dismissals persistent across renames and index rebuilds (01-overview.md:53, 01-overview.md:120).
- Genuinely thoughtful: Traditional→Simplified matching while stored text, keyword search, and snippets stay Traditional — a small localization detail most embedding plugins ignore (01-overview.md:89).
- Genuinely thoughtful: on-device full-note embeddings to 60k characters with tag-fused ranking and frontmatter-description signal, plus shipping workers inlined so Community-store installs still run (01-overview.md:88, 01-overview.md:90, 02-top-level-files.md:216).
- Net: not a research contribution; a well-judged integration of commodity retrieval into an Obsidian-native curation loop.
- Borderline: in-place canvas expansion with orange multi-edge highlighting and slot-into-free-space layout (01-overview.md:115) — nice graph-UX craft, but layout heuristics, not retrieval novelty.
- Borderline: export-results-to-Canvas capped at top 12 with an overflow notice (01-overview.md:92) — a pragmatic truncation rule worth copying, not a new idea.

## Weaknesses and blind spots
- No evaluation anywhere in the covered material: no recall@k, no user study, no Chinese-vs-baseline comparison, no latency or index-size numbers for large vaults.
- Hot/Cold conflates linkedness with value: orphaned but fresh notes read Hot, dense but stale reference notes read Cold; edit-counts-as-use ignores reading, which punishes reference vaults (01-overview.md:126).
- Fresh timestamped `.canvas` per run into a dedicated folder risks canvas sprawl; "never overwrites" is safe but delegates cleanup to the user (01-overview.md:109).
- Coverage gaps in the digest itself: AI-curation actions are truncated mid-list ("Run description…", 01-overview.md:145), and the lockfile body is truncated (02-top-level-files.md:761) — both limit auditability from these sources alone.
- Build fragility signals: worker source inlining, WASM sibling assets, `process.release.name` renaming, sharp stubbing, and node-builtin stripping are a long workaround list for a plugin to carry (02-top-level-files.md:140, 02-top-level-files.md:156, 02-top-level-files.md:182).
- Single-author bus factor (Jacob Mei, vault-curate 1.11.0) and a desktop-first index with mobile-as-reader architecture (01-overview.md:54, 02-top-level-files.md:329).
- Privacy posture is stated but not audited here: "only sends data out if pointed at a cloud service" needs code-level confirmation of what the optional AI-curation path transmits (durations, note bodies, embeddings), which the truncated chunk does not supply.
- Ranking transparency gap: RRF k=60 is named in the tech stack (02-top-level-files.md:1057) without per-engine weights, tie-breaks, or Hot/Cold filter interaction described.
- Test story is thin in these sources: vitest with happy-dom and an Obsidian stub is configured (02-top-level-files.md:1598), but no test count, coverage, or CI signal is quoted.

## Applicability
- Fits: personal Obsidian vaults, especially Traditional-Chinese or mixed CJK vaults where keyword search fails on paraphrase and names (01-overview.md:52).
- Fits: rediscovery workflows — resurfacing Cold notes via current-note and global Discover plus MOC export (01-overview.md:128, 01-overview.md:132).
- Does not fit: team knowledge bases, access-controlled corpora, or server-side search — this is a single-vault desktop plugin, not a service.
- Does not fit: anyone wanting autonomous organization; the plugin explicitly refuses to auto-reorganize notes into a wiki (01-overview.md:38).
- **Relevance to my work**
  - AI/ML engineering: reference pattern for hybrid BM25 + local-embedding retrieval with RRF fusion, tag/frontmatter signal boosting, and weakest-hop path honesty to copy into eval harnesses.
  - Agentic systems: verdict-gated suggestion loop (propose → human yes/no → persistent dismiss) as a safer alternative to agents that auto-edit memory or notes.
  - Elisity data platform: Hot/Cold recency-plus-link heuristic and MOC-style topic grouping as cheap forgotten-data resurfacing; Traditional→Simplified normalization as a reminder to handle script variants in matching layers.
  - Elisity data platform (negative): do not mirror the single-file-index-over-sync distribution model; server-side corpora need access control and audit trails this plugin never promises.
- Adoption cost is low for individuals (no key, local model, off-by-default AI) and high for teams (no multi-user story, no eval to justify rollout).

## What this changes
- Raises the bar for local-first PKM UX: persistent dismissals, per-pair verdicts, and honest "not connected" states should be the default for any suggestion UI I build.
- Confirms small-model on-device retrieval is viable packaging: ~110 MB, no key, syncable index — a template for offline-capable assistants.
- Shifts CJK handling from afterthought to checklist item: script normalization plus synonym lists belong in search settings from day one (01-overview.md:89, 01-overview.md:91).
- Does not change the retrieval state of the art; it changes expectations about how humbly retrieval results should present themselves.
- Reframes "AI curation" as opt-in actions rather than ambient automation — a consent model worth standardizing: manually triggered, never background (01-overview.md:142).
- Suggests the dismissed-pair store (surviving renames and rebuilds) is as valuable as the embedding index for long-lived trust in suggestion systems.

## Verdict
- Useful, narrow, and honest about its boundaries — but unevaluated and single-vault by design, so platform reuse means lifting patterns, not the plugin.
- Cheapest next step is personal: install in a test vault, measure whether Find Similar and Discover surface anything keyword search missed, and steal the verdict/dismiss interaction for agent memory UIs.
- Do not adopt as platform infrastructure; do not depend on its index format or Canvas-folder conventions for anything shared.
- Call: **trial**
