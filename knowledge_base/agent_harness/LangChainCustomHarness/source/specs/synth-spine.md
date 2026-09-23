# React synth spine (worker)

## Problem
Add the argument spine to digest.md — touch nothing else in the file.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/research/LangChainCustomHarness/digest.md`.
2. Replace ONLY the block between `<!-- FIVE_MOVES_START -->` and `<!-- FIVE_MOVES_END -->` with `## The argument in five moves` — 5-7 numbered steps, one clause each, the paper's whole arc. Do NOT touch any other line (the rest is verbatim copy). Keep the marker comments.
3. No git. Touch ONLY digest.md.

## Tests
- `grep -c "five moves" /Users/sergii/.ai/knowledge/research/LangChainCustomHarness/digest.md` >= 1; markers still present.

## DoD
Tests green, then `bd close <own-id> --reason "spine done"` (own task only).

## Scope & constraints
- No fleet commands except `bd close`. No network.
