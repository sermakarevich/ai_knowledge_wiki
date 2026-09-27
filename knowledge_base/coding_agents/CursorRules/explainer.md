> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Rules | Cursor DocsCursor LogoCursor Logo — In Plain Language

## What is this about?

Cursor Rules are saved instructions that tell Cursor's AI Agent how to behave.

Think of them as house rules pinned to the fridge: instead of repeating
yourself in every chat ("use Tailwind", "validate with zod", "follow our
service template"), you write the instruction once and the Agent reuses it.

There are four kinds of rules:

1. **Project Rules** — live in your repo under `.cursor/rules/` as `.mdc`
   files, checked into git and shared with everyone on the project.
2. **User Rules** — personal, global preferences (e.g. "reply concisely")
   set in Customize → Rules; they follow you across all projects.
3. **Team Rules** — organization-wide rules created in the Cursor dashboard
   on Team/Enterprise plans; they reach every member automatically.
4. **AGENTS.md** — a plain markdown file in your project root (or
   subdirectories) with agent instructions; the simple alternative when
   Project Rules feel like overkill.

## Why does it matter?

Language models have no memory between completions. Without rules, every
new chat starts from zero and the Agent guesses your conventions.

Rules fix three everyday pains:

- **Repetition.** You stop retyping the same standards ("named exports,
  co-located CSS, components under 200 lines") in every conversation.
- **Consistency.** The whole team gets the same guidance: same validation
  library, same error format, same component layout.
- **Fewer repeated mistakes.** The docs' own advice: start simple, and add
  a rule when you notice the Agent making the same mistake repeatedly.

Short version: rules turn tribal knowledge into automatic context.

## How does it work?

When a rule applies, its contents are pasted at the start of the model's
context — the text the AI reads before answering. That is the whole trick:
persistent instructions riding along with each prompt.

Project Rules carry three control knobs in their frontmatter:

- `alwaysApply: true` — include in every chat. Globs and description
  are ignored.
- `globs` set (e.g. `src/**/*.tsx`) — auto-attach only when a matching
  file is in context.
- `description` set — the Agent reads the description and pulls the rule
  in when it judges it relevant ("Apply Intelligently").
- Neither set — the rule sits idle until you `@`-mention it in chat
  ("Apply Manually", e.g. `@my-rule`).

So the four application modes are: Always, Intelligently, Specific Files,
and Manually. A plain `.md` file in `.cursor/rules` is ignored — only
`.mdc` files with frontmatter count.

Team Rules are simpler: free-form text, no folder structure. A glob like
`**/*.py` scopes the rule to matching files; no glob means every
conversation. When rules conflict, they merge in precedence order:
Team Rules beat Project Rules, which beat User Rules.

Two ways to create a rule: type `/create-rule` in Agent chat and describe
what you want (it generates the file), or open Customize → Rules → Add Rule.

Good rules stay focused, actionable, and scoped — under 500 lines, split
into small composable files, with concrete examples. Reference files with
`@filename.ts` instead of pasting their contents, so rules stay short and
do not go stale.

## Where can this be used?

- **Frontend standards.** "Always use Tailwind; animate with Framer Motion;
  follow our component naming conventions."
- **API standards.** "Validate everything with zod; define return types as
  zod schemas; export the generated types."
- **Code templates.** Express services (RESTful shape, error middleware,
  logging, `@express-service-template.ts`) and React components (props
  interface on top, named export, styles at bottom).
- **Workflow automation.** "Analyze the app: run `npm run dev`, fetch
  console logs, suggest performance fixes." Or: "Draft docs from code
  comments plus README into markdown."
- **Org-wide compliance.** Admins enable or enforce Team Rules from the
  dashboard so standards apply to every member and repo.
- **Simple projects.** Drop an `AGENTS.md` in the root instead of setting
  up `.cursor/rules`; nest more `AGENTS.md` files in subdirectories for
  folder-specific guidance (child instructions win).
- **Sharing.** Rules travel with plugins via a marketplace
  (`.cursor-plugin/marketplace.json`), not as standalone imports.

Note the limits: rules feed Agent (Chat) only. They do not affect Cursor
Tab completions, other AI features, or Inline Edit (Cmd/Ctrl+K).

## Conclusions & takeaways

1. Rules exist because the model forgets everything between answers —
   they are persistent prompt-level memory.
2. Start with the lightest tool: User Rules for style, `AGENTS.md` for
   simple projects, Project Rules when you need scoping and versioning.
3. Scope deliberately: always-on for universal truths, globs for
   file-specific standards, descriptions for judgment calls, manual for
   rare migrations.
4. Keep each rule small and concrete — one topic, real examples, links
   (`@`-references) instead of copies.
5. Let Team Rules carry org standards with enforce-on where it matters,
   but do not rely on AI guidance as your only security control.
6. When a rule misfires, check the basics first: right type, description
   present, glob actually matching the files in context.

## Jargon decoder

| Term | What it really means |
|---|---|
| Rule | A saved instruction the Agent reads before answering. |
| Project Rule | A version-controlled rule file (`.mdc`) in `.cursor/rules/`. |
| User Rule | A personal global preference applied in Agent chats everywhere. |
| Team Rule | An org-wide rule pushed from the dashboard to all members. |
| AGENTS.md | A plain markdown instructions file; the no-config alternative. |
| Frontmatter | The settings block (`description`, `globs`, `alwaysApply`) at the top of a rule. |
| Glob | A file-matching pattern (`*` = one level, `**` = any depth). |
| Model context | The text the AI reads before answering; rules get prepended here. |
| Apply Intelligently | The Agent decides from the description whether to use the rule. |
| @-mention | Typing `@rule-name` or `@file` in chat to pull in a rule or file manually. |
