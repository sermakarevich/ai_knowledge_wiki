> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Rules
**In one sentence:** Cursor Rules provide persistent, reusable system-level instructions to Agent via four rule types — Project Rules in `.cursor/rules/*.mdc`, User Rules, Team Rules, and `AGENTS.md` — controlled by `alwaysApply`, `description`, and `globs` frontmatter.
## Key points
- Cursor supports four rule types: version-controlled Project Rules in `.cursor/rules`, global User Rules used by Agent (Chat), dashboard-managed Team Rules on Team/Enterprise plans, and `AGENTS.md` markdown instructions as a simple alternative to `.cursor/rules`.
- Rules work because LLMs retain no memory between completions, so applied rule contents are prepended at the start of model context to give consistent guidance.
- Project rules must use the `.mdc` extension — a plain `.md` file in `.cursor/rules` is ignored because it lacks `description`, `globs`, and `alwaysApply` frontmatter; rules can be organized in subfolders such as `frontend/components.mdc`.
- Inclusion is determined by three frontmatter fields: `alwaysApply: true` means always included (globs/description ignored); `alwaysApply: false` + globs means auto-attached on matching file in context; + description only means Agent pulls it when relevant; neither means `@`-mention-only manual invocation.
- Four application modes exist: Always Apply (every chat), Apply Intelligently (Agent decides from description), Apply to Specific Files (glob match), and Apply Manually (e.g. `@my-rule` in chat).
- Glob scoping uses `*` for one path segment and `**` for recursive directories (e.g. `src/**/*.tsx`, `docs/**/*.md, docs/**/*.mdx`), with multiple patterns comma-separated.
- Rules are created via `/create-rule` in Agent chat (generates frontmatter and saves to `.cursor/rules`) or via Customize sidebar → Rules → Add Rule.
- Good rules are focused, actionable, scoped, under 500 lines, split into composable rules, with concrete examples or `@`-referenced files instead of copied contents; Team Rules take precedence over other types and can be enforced so members cannot disable them.
---
## How rules work
Rule contents, when applied, are included at the start of the model context. Verbatim: "Large language models don't retain memory between completions. Rules provide persistent, reusable context at the prompt level." Verbatim: "They bundle prompts, scripts, and more together, making it easy to manage and share workflows across your team."
**Covers:** Covers the Command Palette chunk of the Cursor Rules docs page.
## Project rules
Project rules live in `.cursor/rules` as `.mdc` files, are version-controlled, and are scoped using path patterns, invoked manually, or included based on relevance. Use project rules to: encode domain-specific knowledge; automate project-specific workflows or templates; standardize style or architecture decisions.
## Rule file structure
Each rule is an `.mdc` file with any name. Verbatim: "A plain .md file in .cursor/rules is ignored by the rules system because it has no frontmatter to specify description, globs, and alwaysApply. If you prefer plain markdown, use AGENTS.md instead." Example layout: `react-patterns.mdc` recognized; `api-guidelines.md` (no `.mdc`) ignored; `frontend/components.mdc` shows folder organization.
## Rule anatomy
Each rule is markdown with frontmatter metadata plus content; the type dropdown changes `description`, `globs`, `alwaysApply`.

| alwaysApply | description | globs | Behavior |
|---|---|---|---|
| true | — | — | Always included. Globs and description are ignored. |
| false | — | provided | Auto-attached when a matching file is in context. |
| false | provided | omitted | Agent reads the description and pulls the rule in when relevant. |
| false | omitted | omitted | Included only when you @-mention the rule in chat. |

Examples from chunk: always-applied copyright-header rule (`All source files must include the company copyright header`; never modify generated files in `dist/`/`build/`); glob rule `src/components/**/*.tsx` (named exports, co-located module CSS, keep components under 200 lines, prefer composition over prop drilling); description rule `RPC service conventions and patterns for the backend` (one service per file under `src/services/`, validate at boundary, structured `{code, message}` errors, `@service-template.ts` reference); manual migration rule (every migration needs `up` and `down`, add/backfill/drop instead of in-place type change, `@migration-template.sql` reference).
## Glob pattern examples
Separate multiple patterns with commas.

| Pattern | Matches |
|---|---|
| `*` | Any single file name segment |
| `**` | Any number of directories (recursive) |
| `*.ts` | All .ts files in the root |
| `**/*.ts` | All .ts files in any directory |
| `src/**` | All files anywhere under src/ |
| `src/**/*.tsx` | All .tsx files anywhere under src/ |
| `docs/**/*.md, docs/**/*.mdx` | .md and .mdx files under docs/ (comma-separated) |
| `tailwind.config.*` | tailwind.config with any extension |

## Creating a rule
Two ways: type `/create-rule` in Agent and describe what you want (Agent generates the file with proper frontmatter under `.cursor/rules`); or open Customize in the sidebar → Rules → Add Rule (creates the file; Customize shows all rules and status).
## Best practices
Verbatim: "Good rules are focused, actionable, and scoped." Keep rules under 500 lines; split large rules into multiple composable rules; provide concrete examples or referenced files; avoid vague guidance and write rules like clear internal docs; reuse rules when repeating prompts; reference files instead of copying contents to stay short and avoid staleness.
### What to avoid in rules
Do not copy entire style guides (use a linter; Agent knows common conventions); do not document every command (Agent knows npm, git, pytest); do not add rarely-applicable edge cases; do not duplicate codebase contents (point to canonical examples). Verbatim: "Start simple. Add rules only when you notice Agent making the same mistake repeatedly." Check rules into git; update the rule when Agent errs; you can tag `@cursor` on a GitHub issue/PR to have Agent update the rule.
## Rule file format
Frontmatter controls application; content is the rule. Example frontmatter: `description: "This rule provides standards for frontend components and API validation"`, `alwaysApply: false`. Verbatim: "If alwaysApply is true, the rule will be applied to every chat session. Otherwise, the description of the rule will be presented to the Cursor Agent to decide if it should be applied."
## Examples
Chunk gives four examples: (1) frontend/API standards — Tailwind styling, Framer Motion animations, component naming in components directory; zod validation, zod-schema return types and generated exported types in API directory; (2) Express-service and React-component templates — RESTful principles, error middleware, logging, `@express-service-template.ts`; props interface on top, named export, styles at bottom, `@component-template.tsx`; (3) workflow automation — `npm run dev`, console-log fetch, performance suggestions; doc generation via code comments, `README.md` analysis, markdown output; (4) adding a Cursor setting — toggle property in `@reactiveStorageTypes.ts`, default in `INIT_APPLICATION_USER_PERSISTENT_STORAGE` in `@reactiveStorageService.tsx`, toggle in `@settingsBetaTab.tsx` (beta) or `@settingsGeneralTab.tsx` via `<SettingsSubSection>`, consume via `reactiveStorageService.applicationUserPersistentStorage.myNewProperty`. Verbatim: "Examples are available from providers and frameworks."
## Team Rules
Team/Enterprise plans create and enforce organization-wide rules from the Cursor dashboard; admins configure per-rule required status. Verbatim: "Team Rules work alongside other rule types and take precedence to ensure organizational standards are maintained across all projects."
### Managing Team Rules
Administrators create and manage rules from the dashboard; once created they automatically apply to all members and are visible in the dashboard.
### Activation and enforcement
`Enable this rule immediately`: checked = active on creation, unchecked = saved draft. `Enforce this rule`: enabled = required, cannot be disabled in Customize; disabled = members can toggle off under Team Rules in Customize. Verbatim: "By default, non‑enforced Team Rules can be disabled by users."
**Covers:** Covers the Command Palette chunk of the Cursor Rules docs page.
