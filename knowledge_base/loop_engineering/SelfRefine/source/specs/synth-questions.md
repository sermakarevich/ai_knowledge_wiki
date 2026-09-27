# SelfRefine synth questions (worker)

## Problem
Write retrieval-practice `questions.md` from the digest only — one question per wiki section (4 sections), answers collapsed.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/research/SelfRefine/digest.md`. Never the source, wiki pages, or fleet artifacts.
2. Write `/Users/sergii/.ai/knowledge/research/SelfRefine/questions.md` COMPLETELY (overwrite on retry): front-matter (`type: Retrieval Prompts`, `last_reviewed: null`, `review_count: 0`), then ≥4 questions (7), each with the answer inside a collapsed `<details>` block. Mix: half core recall with numbers, a third elaboration (why / what breaks if), rest transfer. Leave OUT the final evaluation question (finalize-synth adds it).
3. No git. Touch ONLY questions.md.

## Tests
- `test -f /Users/sergii/.ai/knowledge/research/SelfRefine/questions.md; grep -c "<details>" /Users/sergii/.ai/knowledge/research/SelfRefine/questions.md` >= 4.

## DoD
Tests green, then `bd close <own-id> --reason "questions done"` (own task only).

## Scope & constraints
- No fleet commands except `bd close`. No network.
