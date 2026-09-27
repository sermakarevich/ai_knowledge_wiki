> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluation and Quality Defects
**In one sentence:** A `max(1, v)` guard on integer env vars silently truncated 37,542 source chars to 1 and zeroed per-chunk relationship extraction, and six post-extraction cleaning fixes corrected title duplication, type inconsistency, self-loops, misassignment, ID chaos, and abbreviation false positives.
## Key points
- The `_env_int()` guard rewrote the `REL_EXTRACTION_MAX_SOURCE_CHARS = 0` (unlimited) sentinel via `g(0) = 1`, so `S[:1]` reduced 37,542 chars to the single letter "P" and per-chunk relationships fell to 0 versus 22–38 expected.
- Removing the guard restored sentinel semantics `g(v) = v` and immediately recovered 22–38+ relationships per chunk (0 → 500+ total), with no other caller affected since all other integer defaults are ≥ 1.
- Title-prefix duplication created 91 duplicate pairs inflating Person count from ~224 to 315 (~30% inflation); dynamic prefix-stripping normalisation merges them while preserving the titled variant as alias.
- Context-aware duplicate detection flagged 66 of 91 title pairs but classified all as "different_people_different_contexts" because SequenceMatcher similarity (e.g. 0.75) fell below the 0.95 auto-merge threshold and 25 pairs fell below the 0.75 detection threshold.
- Relationship-type variants (e.g. INFILTRATED 7 / INfiltrated 15 / infiltrated 4; SURVEILLED 64 / surveilled 1 / surveiled typo 1) collapsed via `t' = τ(Upper(Snake(t)))` with typo table `τ(SURVEILED) = SURVEILLED`, deduplicating ~30 relations.
- Self-loop filtering removed 114 relationships (21% of 540) where source == target via `ρ' = {(u,v,t) ∈ ρ : u ≠ v}`; type correction reclassified 42 Person-typed entities by indicator words; ID reassignment unified 7 formats and removed 9 dangling references.
- Net impact on IR-001.pdf (45 pages): entities 579 → ~400 (−31%), self-loops 114 → 0, broken references 9 → 0, type variants 39 → ~28, false-positive dedup candidates 79 → ~0, ID patterns 7 → 1.
---
## Observation point: expected vs observed
| Observation point | Expected | Observed |
|---|---|---|
| Source chars passed by caller | 37,542 | 37,542 |
| Source chars seen inside extraction | 37,542 | 1 |
| Entities provided to the LLM | 23 | 23 |
| Relationships returned | 22–38 | 0 |

**Covers:** §7.3 intro, observation table (p. 31)

## Root cause: `g(v) = max(1, v)` sentinel bug
The configuration reader applied `g(v) = max(1, v)` to every integer environment variable to prevent division-by-zero in unrelated callers, but `REL_EXTRACTION_MAX_SOURCE_CHARS` uses `v = 0` to mean unlimited; the guard silently rewrote it to `g(0) = 1`, and `S[:g(0)] = S[:1]` reduced the evidence to one character. The relationship model "asked to find relations in a one-character document, correctly returned none, which made the failure look like a model deficiency rather than an infrastructure bug."

Fix: guard removed, restoring `g(v) = v` (non-numeric values fall back to default); no other caller affected since every other integer default is ≥ 1. Impact: per-chunk relationship extraction recovered to 22–38+ relationships per chunk.

**Covers:** §7.3 root cause, fix, impact (p. 31)

## Fix 1: cross-chunk title-based entity duplication
Same entity appeared as distinct entities with different title prefixes across chunks.

Table 12: Title-Based Entity Duplication Examples from IR-001.pdf

| Chunk A Entity | Chunk B Entity | Chunk C Entity |
|---|---|---|
| per_087: "Mario Chavez" | per85_3: "Colonel Mario Chavez" | — |
| per48_2: "Nicole Trujillo" | per47: "Dr. Nicole Trujillo" | per80: "Agent Dr. Nicole Trujillo" |
| per5: "Bianca Knapp" | per2_2: "General Bianca Knapp" | — |

Scale: 91 duplicate pairs detected, inflating Person count from ∼224 to 315 (∼30% inflation).

Why Fig. 10 did not catch it: flagged 66 of 91 pairs but classified every one as "different_people_different_contexts" with low confidence because (1) SequenceMatcher similarity e.g. 0.75 below 0.95 auto-merge threshold, (2) full-string comparison without title-prefix awareness, (3) 25 pairs below 0.75 detection threshold.

Why chunk merging did not catch it: canonical key compared verbatim, `("person", "colonel mario chavez") ≠ ("person", "mario chavez")`.

Fix: dynamic normalisation stripping leading prefix tokens until a two-word core remains, where `prefixlike(w)` holds when `w` ends in a period ("Dr.") or is a short alphabetic token (|w| ≤ 12, covering "Colonel", "General", "Agent"); e.g. "Agent Dr. Nicole Trujillo" → "Dr. Nicole Trujillo" → "Nicole Trujillo"; merge preserves titled variant as alias with base name primary.

**Covers:** §7.3.2 (pp. 31–32)

## Fix 2: relationship type inconsistency
Table 13: Relationship Type Variants from IR-001.pdf

| Variant 1 | Variant 2 | Variant 3 |
|---|---|---|
| INFILTRATED (7) | INfiltrated (15) | infiltrated (4) |
| REPORTED_TO (22) | reported to (5) | — |
| SURVEILLED (64) | surveilled (1) | surveiled (1, typo) |

Root cause: Fig. 11 deduplicates by key (u, v, t) but compared type t as raw string without normalization. Fix: canonicalise via `t' = τ(Upper(Snake(t)))` where Snake collapses whitespace/hyphen runs to underscores and τ is a typo-correction table (τ(SURVEILED) = SURVEILLED, τ(TRANSFERED) = TRANSFERRED).

**Covers:** §7.3.3 (p. 32)

## Fix 3: self-referencing relationships
114 relationships (21% of all 540) had source == target; one entity ("Dr. Nicole Trujillo") had nine self-loops including SURVEILLED, FUNDED, MONITORED, DEPLOYED_TO. Root cause: when the LLM cannot resolve the correct target it reuses the source entity ID, "a known hallucination pattern observed more frequently with smaller local models than with the cloud-hosted alternative." Fix: `ρ' = {(u, v, t) ∈ ρ : u ≠ v}`, discarding all 114 self-loops on IR-001.pdf.

**Covers:** §7.3.4 (p. 32)

## Fix 4: entity type misassignment
42 entities with non-person names were typed "Person". Table 14 examples: "Bank" → Organization; "Leviathan Submarine LS-6720" (submarine) → Equipment; "Christopherchester Camp" (camp) → Location; "Agency" (agency) → Organization. Root cause: typing accuracy degrades in later chunks of long documents ("consistent with reported positional degradation in long contexts [34]", "Person" as default). Fix: post-extraction inference checking indicator words (camp, laboratory → Location; agency, institute → Organization; submarine, drone → Equipment), applied only to Person-typed entities with strong indicators.

**Covers:** §7.3.5 (pp. 32–33)

## Fix 5: inconsistent entity ID scheme
At least seven patterns (per1, per1_2, per_001, org_020, e_local_5, etc.) because each chunk's LLM call generated IDs independently plus collision suffixes. Fix: final-stage reassignment to uniform `{prefix}_{number}` (per_001, org_001, loc_001, eqp_001) with relationship remapping, plus filtering 9 dangling references to nonexistent entity IDs on IR-001.pdf.

**Covers:** §7.3.6 (p. 33)

## Fix 6: false positive abbreviation similarity matches
Fig. 9's abbreviation signal produced 79 nonsensical matches at hardcoded 0.92, e.g. "Michael Cruz" vs "Mario Chavez" flagged abbreviation_variant via shared initials M/C. Root cause: `match_buggy(p,q) ⟺ p = q ∨ p₁ = q₁`. Fix: `match(p,q) ⟺ p = q ∨ (|p| = 1 ∧ p = q₁) ∨ (|q| = 1 ∧ q = p₁)`, accepted only if at least one part-pair used the single-letter clause; "E. Petrov" vs "Elena Petrov" still matches, "Michael Cruz" vs "Mario Chavez" rejected.

**Covers:** §7.3.7 (p. 33)

## Summary of quality fixes
Table 15: Summary of Post-Extraction Data Cleaning Fixes

| # | Fix | Root Cause | Entities | Rels |
|---|---|---|---|---|
| 0 | _env_int() bug | max(1,0) truncated source text | 0 | All (0→500+) |
| 1 | Title normalization | Verbatim name comparison | 91 merged | Refs remapped |
| 2 | Rel type normalization | No case normalization | 0 | ∼30 deduped |
| 3 | Self-loop filtering | LLM hallucination | 0 | 114 removed |
| 4 | Entity type correction | LLM accuracy degradation | 42 reclassified | 0 |
| 5 | ID reassignment | Independent per-chunk IDs | All renumbered | 9 dangling removed |
| 6 | Abbreviation fix | First-letter-only match | 0 | 0 (dedup fixed) |

Fixes operate at Stages 2–3 of the pipeline (Fig. 15), before core deduplication (Stage 5).

Table 16: Net Quality Impact on IR-001.pdf (45 pages)

| Metric | Before Fixes | After Fixes | Change |
|---|---|---|---|
| Total entities | 579 | ∼400 | −31% (dedup) |
| True Person count | 315 (inflated) | ∼224 | −29% (accurate) |
| Per-chunk relationships | 0 | 500+ | Restored |
| Self-loop relationships | 114 (21%) | 0 | −100% |
| Broken entity references | 9 | 0 | −100% |
| Relationship type variants | 39 | ∼28 | −28% (normalized) |
| False positive dedup candidates | 79 | ∼0 | −100% |
| Entity ID format patterns | 7 | 1 | Uniform |

**Covers:** §7.3.8, Tables 15–16 (p. 33)
