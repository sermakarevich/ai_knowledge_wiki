# React synth questions (worker)

## Problem
Write retrieval-practice `questions.md` from the digest only — one question per wiki section (3 sections), answers collapsed.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/papers/HarnessEngineeringCourse/digest.md`. Never the source, wiki pages, or fleet artifacts.
2. Write `/Users/sergii/.ai/knowledge/papers/HarnessEngineeringCourse/questions.md` COMPLETELY (overwrite on retry): front-matter (`type: Retrieval Prompts`, `last_reviewed: null`, `review_count: 0`), then ≥3 questions (6), each with the answer inside a collapsed `<details>` block. Mix: half core recall with numbers, a third elaboration (why / what breaks if), rest transfer. Leave OUT the final evaluation question (finalize-synth adds it).
3. No git. Touch ONLY questions.md.

## Tests
- `test -f /Users/sergii/.ai/knowledge/papers/HarnessEngineeringCourse/questions.md; grep -c "<details>" /Users/sergii/.ai/knowledge/papers/HarnessEngineeringCourse/questions.md` >= 3.

## DoD
Tests green, then `bd close <own-id> --reason "questions done"` (own task only).

## Scope & constraints
- No fleet commands except `bd close`. No network.
