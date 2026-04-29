# Claude Ecosystem

Research and documentation on **Anthropic's Claude models and Claude Code** — system cards, best practices, migration guides, leaked/reverse-engineered internals, and Mythos.

## Papers

- [[ClaudeCodeAutoMode]] — Two-layer classifier (prompt-injection + transcript) enables safe autonomous Claude Code; 0.4% false-positive rate.
- [[ClaudeCodeMemory]] — Analysis of Claude Code's 6-layer memory hierarchy; MEMORY.md is a pointer index, not storage.
- [[ClaudeCodeSourceAnalysis]] — Deep reverse-engineering of Claude Code's leaked source; 50-line TAOR loop + deterministic scaffolding.
- [[ClaudeMigrationGuide/summary]] — Official Anthropic migration guide for Opus 4.7/Sonnet 4.6/Haiku 4.5 with adaptive thinking + new `effort` param.
- [[ClaudeOpus47BestPractices/summary]] — Opus 4.7 uses adaptive (not fixed-budget) thinking; `xhigh` effort level recommended default.
- [[ClaudeOpus47SystemCard/summary]] — Opus 4.7 leads SWE-bench at 87.6%; no new ASL tier; improved prompt-injection robustness.
- [[ClaudeOpus47SystemPrompt/summary]] — Leaked 1,408-line operational prompt: search-first behavior, copyright constraints, refusal tripwires.
- [[DiveIntoClaudeCode/summary]] — Source-level analysis of Claude Code v2.1.88: only 1.6% AI logic, 98.4% deterministic infrastructure.
- [[SystemCardClaudeMythosPreview]] — Anthropic's most capable model restricted to defensive cybersecurity partners; best-aligned yet highest-risk.
