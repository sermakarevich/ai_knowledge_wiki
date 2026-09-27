> [[index|Wiki]] | [[summary|Summary]]

# Rules | Cursor DocsCursor LogoCursor Logo — Digest

## 1. [[wiki/01-command-palette|Rules]]

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

## 2. [[wiki/02-format-and-how-team-rules-are-applied|Format and how Team Rules are applied]]

**In one sentence:** Team Rules are free-form text applied via optional glob scoping across all team projects in Agent (Chat), merged with Project and User Rules under Team-first precedence.

## Key points

- Team Rules are free-form text and do not use the folder structure of Project Rules.
- A Team Rule with a glob pattern (e.g., `**/*.py`) applies only when matching files are in context.
- A Team Rule without a glob pattern applies to every conversation.
- When enabled (and not disabled by the user, unless enforced), a Team Rule is included in the model context for Agent (Chat) across all repositories and projects for that team.
- Rules merge in precedence order Team Rules → Project Rules → User Rules, with earlier sources winning on conflict.
- Enforced rules are supported in internal compliance workflows, but AI guidance should not be the only security control.

## 3. [[wiki/03-examples|Examples]]

**In one sentence:** The chunk gives concrete rule examples (frontend/API standards, Express/React templates, workflow automation, adding a Cursor setting) and then documents Team Rules administration and precedence, repository import via plugins, AGENTS.md usage with nesting, User Rules scope, and FAQ limits.

## Key points

- Frontend component rules require Tailwind for styling, Framer Motion for animations, and component naming conventions; API rules require zod for all validation, zod schemas for return types, and exported schema-generated types.
- Express service rules prescribe RESTful principles, error handling middleware, proper logging, and `@express-service-template.ts`; React component rules prescribe a props interface at top, component as named export, styles at bottom, and `@component-template.tsx`.
- Automation rules define app analysis as running the dev server with `npm run dev`, fetching console logs, and suggesting performance improvements, and documentation drafting as extracting code comments, analyzing README.md, and generating markdown documentation.
- Adding a new Cursor setting requires creating a property in `@reactiveStorageTypes.ts`, adding a default in `INIT_APPLICATION_USER_PERSISTENT_STORAGE` in `@reactiveStorageService.tsx`, placing beta toggles in `@settingsBetaTab.tsx` versus `@settingsGeneralTab.tsx`, and reading the flag via `reactiveStorageService.applicationUserPersistentStorage.myNewProperty`.
- Team Rules are created and managed from the Cursor dashboard, apply automatically to all team members, can be required via "Enforce this rule", work alongside other rule types, and merge in precedence order Team Rules → Project Rules → User Rules with earlier sources winning conflicts.
- Team Rules are free-form text without Project Rules folder structure, support glob scoping (e.g. `**/*.py`, only applying when matching files are in context), apply to every conversation when no glob is set, and are included in model context for Agent (Chat) across all repositories and projects for the team.
- Rules are not imported standalone but arrive with a plugin published through a marketplace (repository needs `.cursor-plugin/marketplace.json`, imported via From GitHub Repository or team marketplace); `AGENTS.md` is a plain-markdown alternative in project root and subdirectories with nested files combined and more specific instructions taking precedence, while User Rules are global Customize → Rules preferences used only by Agent (Chat), not Cursor Tab or Inline Edit (Cmd/Ctrl+K).

## The argument in five moves

1. Rules exist because LLMs retain no memory between completions, so persistent instructions are prepended to model context.
2. Project Rules carry those instructions as version-controlled `.mdc` files whose `alwaysApply`, `globs`, and `description` frontmatter selects among always, glob-matched, intelligent, and manual application.
3. Team Rules extend the same mechanism org-wide from the dashboard, with enable/enforce controls and automatic application to all members.
4. Team Rules stay free-form, gain optional glob scoping, and merge Team-first over Project and User Rules inside Agent (Chat) context.
5. Concrete examples (frontend/API standards, service/component templates, workflow automation, settings changes) show the pattern in practice, while `AGENTS.md`, User Rules, and plugin imports offer simpler or broader alternatives.
6. FAQ limits bound the system: rules need correct type/description/globs to fire, can `@`-reference files and be created from chat, and do not affect Cursor Tab or Inline Edit.
