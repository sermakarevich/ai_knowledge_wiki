---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Rules | Cursor DocsCursor LogoCursor Logo

### Q1. What are the four Cursor rule types and where does each one live?
> [!tip]- Answer
> Project Rules are version-controlled `.mdc` files in `.cursor/rules`, User Rules are global preferences in Customize → Rules, Team Rules are managed from the Cursor dashboard, and `AGENTS.md` is plain markdown in the project root or subdirectories. Project Rules suit domain knowledge and templates, User Rules suit style preferences, and Team Rules suit org-wide standards. See [[wiki/01-command-palette|Rules]].

### Q2. How do the `alwaysApply`, `description`, and `globs` frontmatter fields determine when a Project Rule is included?
> [!tip]- Answer
> With `alwaysApply: true` the rule is always included and globs/description are ignored. With `alwaysApply: false` plus globs it auto-attaches when a matching file is in context, with description only the Agent pulls it in when relevant, and with neither it applies only via `@`-mention. A plain `.md` file in `.cursor/rules` is ignored for lacking this frontmatter. See [[wiki/01-command-palette|Rules]].

### Q3. What glob syntax, creation flows, and best practices govern Project Rules?
> [!tip]- Answer
> `*` matches one path segment and `**` matches recursively (e.g. `src/**/*.tsx`), with comma-separated multiples like `docs/**/*.md, docs/**/*.mdx`. Rules are created via `/create-rule` in Agent chat or Customize sidebar → Rules → Add Rule. Good rules stay focused, actionable, scoped, under 500 lines, use `@`-references instead of copied contents, and are split into composable rules. See [[wiki/01-command-palette|Rules]].

### Q4. How are Team Rules formatted, scoped with globs, and merged with other rule types?
> [!tip]- Answer
> Team Rules are free-form text without the Project Rules folder structure. A globbed rule (e.g. `**/*.py`) applies only when matching files are in context, while one without a glob applies to every conversation. Enabled rules enter Agent (Chat) model context across all team repos, merging Team Rules → Project Rules → User Rules with earlier sources winning conflicts. See [[wiki/02-format-and-how-team-rules-are-applied|Format and how Team Rules are applied]].

### Q5. How do Team Rule activation controls and enforced compliance rules work?
> [!tip]- Answer
> Admins create Team Rules from the dashboard where they apply automatically to all members. `Enable this rule immediately` checked means active on creation, unchecked means saved draft; `Enforce this rule` means members cannot disable it in Customize. Enforced rules support compliance workflows, but AI guidance should not be the only security control. See [[wiki/02-format-and-how-team-rules-are-applied|Format and how Team Rules are applied]].

### Q6. What alternatives to Project Rules exist — `AGENTS.md`, User Rules, and plugin imports — and what limits apply to each?
> [!tip]- Answer
> `AGENTS.md` is plain markdown without frontmatter, supported in root and nested subdirectories whose instructions combine with more specific ones winning. User Rules are global Customize → Rules preferences used only by Agent (Chat), not Cursor Tab or Inline Edit (Cmd/Ctrl+K). External rules arrive only inside a plugin published via a marketplace (repo needs `.cursor-plugin/marketplace.json`), imported with From GitHub Repository. See [[wiki/03-examples|Examples]].

### Q7. A 20-person team needs React/Tailwind component standards, Python backend conventions, and a non-bypassable compliance notice. What rule setup should you recommend and why?
> [!tip]- Answer
> Put the React standards in a glob-scoped Project Rule (`src/**/*.tsx`) with Tailwind, naming, and `@component-template.tsx` references, and the Python conventions in an enforced glob-scoped Team Rule (`**/*.py`). Make the compliance notice an enforced no-glob Team Rule so it fires every conversation and members cannot disable it. This matches mechanism to scope: versioned project specificity, org-wide consistency, and Team-first precedence where it matters most. See [[wiki/03-examples|Examples]].
