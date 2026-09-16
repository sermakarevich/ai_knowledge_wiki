# AmuxHarnessGuide summary repair — restore A2 template

## Problem
`summary.md` was written short (no A2 sections). Rewrite it fully from the already-verified wiki pages.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/papers/AmuxHarnessGuide/wiki/*.md` (the verified pages). Never the raw source, never fleet artifacts.
2. Rewrite `/Users/sergii/.ai/knowledge/papers/AmuxHarnessGuide/summary.md` COMPLETELY following this template EXACTLY (all sections, same headers, same order). Keep the existing title line and metadata style; fill every section from the wiki content:
```markdown
# <Title>

**Article:** [Harness Engineering: The Complete Guide](https://amux.io/guides/harness-engineering/) — amux.io, 2026

## Human Readable TL;DR

A 3-5 sentence explanation using everyday analogies that someone outside AI/tech can understand. No jargon.

## TL;DR

A concise technical summary (3-5 sentences) covering the core contribution, method, and key result.

---

## Problem & Motivation

What gap or limitation does this source address? Why does it matter?

---

## Main Original Ideas

Numbered list of the novel contributions. Each item: bold concept name followed by a 2-3 sentence explanation.

---

## Key Findings

- Results table if quantitative comparisons exist
- Bullet points for qualitative findings and ablation insights

---

## Suggestions & Future Directions

Numbered list of proposed next steps, acknowledged limitations, open questions.

---

## Authors & Institutions

Comma-separated authors with affiliations (or site name for articles).
```
3. No git commands (repo auto-syncs). Touch ONLY summary.md.

## Tests
- `wc -l /Users/sergii/.ai/knowledge/papers/AmuxHarnessGuide/summary.md` >= 50; each header present: `grep -c "Human Readable TL;DR\|## TL;DR\|Problem & Motivation\|Main Original Ideas\|Key Findings\|Suggestions & Future\|Authors" /Users/sergii/.ai/knowledge/papers/AmuxHarnessGuide/summary.md` >= 7.

## DoD
1. Tests green.
2. `bd close <own-id> --reason "summary restored"` (own task only).

## Scope & constraints
- No `fleet` commands except `bd close`. No network. No secrets.
