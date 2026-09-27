> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Format and how Team Rules are applied
**In one sentence:** Team Rules are free-form text applied via optional glob scoping across all team projects in Agent (Chat), merged with Project and User Rules under Team-first precedence.
## Key points
- Team Rules are free-form text and do not use the folder structure of Project Rules.
- A Team Rule with a glob pattern (e.g., `**/*.py`) applies only when matching files are in context.
- A Team Rule without a glob pattern applies to every conversation.
- When enabled (and not disabled by the user, unless enforced), a Team Rule is included in the model context for Agent (Chat) across all repositories and projects for that team.
- Rules merge in precedence order Team Rules → Project Rules → User Rules, with earlier sources winning on conflict.
- Enforced rules are supported in internal compliance workflows, but AI guidance should not be the only security control.
---
## Format
Team Rules are free-form text:

> "Team Rules are free-form text. They do not use the folder structure of Project Rules."

## Glob patterns
Team Rules support glob patterns for file-scoped application:

> "When a glob pattern is set (e.g., **/*.py), the rule only applies when matching files are in context. Rules without a glob pattern apply to every conversation."

| Condition | Behavior |
|---|---|
| Glob set (e.g., `**/*.py`) | Applies only when matching files are in context |
| No glob pattern | Applies to every conversation |

## Where they apply
> "When a Team Rule is enabled (and not disabled by the user, unless enforced), it is included in the model context for Agent (Chat) across all repositories and projects for that team."

## Precedence
> "Rules are applied in this order: Team Rules → Project Rules → User Rules. All applicable rules are merged; earlier sources take precedence when guidance conflicts."

| Order | Source |
|---|---|
| 1 | Team Rules |
| 2 | Project Rules |
| 3 | User Rules |

## Enforced rules note
> "Some teams use enforced rules as part of internal compliance workflows. While this is supported, AI guidance should not be your only security control."

**Covers:** Covers Team Rules format and how Team Rules are applied.
