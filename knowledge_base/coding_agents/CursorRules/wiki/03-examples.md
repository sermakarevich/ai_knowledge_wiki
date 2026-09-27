> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Examples
**In one sentence:** The chunk gives concrete rule examples (frontend/API standards, Express/React templates, workflow automation, adding a Cursor setting) and then documents Team Rules administration and precedence, repository import via plugins, AGENTS.md usage with nesting, User Rules scope, and FAQ limits.
## Key points
- Frontend component rules require Tailwind for styling, Framer Motion for animations, and component naming conventions; API rules require zod for all validation, zod schemas for return types, and exported schema-generated types.
- Express service rules prescribe RESTful principles, error handling middleware, proper logging, and `@express-service-template.ts`; React component rules prescribe a props interface at top, component as named export, styles at bottom, and `@component-template.tsx`.
- Automation rules define app analysis as running the dev server with `npm run dev`, fetching console logs, and suggesting performance improvements, and documentation drafting as extracting code comments, analyzing README.md, and generating markdown documentation.
- Adding a new Cursor setting requires creating a property in `@reactiveStorageTypes.ts`, adding a default in `INIT_APPLICATION_USER_PERSISTENT_STORAGE` in `@reactiveStorageService.tsx`, placing beta toggles in `@settingsBetaTab.tsx` versus `@settingsGeneralTab.tsx`, and reading the flag via `reactiveStorageService.applicationUserPersistentStorage.myNewProperty`.
- Team Rules are created and managed from the Cursor dashboard, apply automatically to all team members, can be required via "Enforce this rule", work alongside other rule types, and merge in precedence order Team Rules → Project Rules → User Rules with earlier sources winning conflicts.
- Team Rules are free-form text without Project Rules folder structure, support glob scoping (e.g. `**/*.py`, only applying when matching files are in context), apply to every conversation when no glob is set, and are included in model context for Agent (Chat) across all repositories and projects for the team.
- Rules are not imported standalone but arrive with a plugin published through a marketplace (repository needs `.cursor-plugin/marketplace.json`, imported via From GitHub Repository or team marketplace); `AGENTS.md` is a plain-markdown alternative in project root and subdirectories with nested files combined and more specific instructions taking precedence, while User Rules are global Customize → Rules preferences used only by Agent (Chat), not Cursor Tab or Inline Edit (Cmd/Ctrl+K).
---
## Standards for frontend components and API validation
| Area | Requirements stated in chunk |
|---|---|
| Components directory | Always use Tailwind for styling; use Framer Motion for animations; follow component naming conventions |
| API directory | Use zod for all validation; define return types with zod schemas; export types generated from schemas |

## Templates for Express services and React components
| Template | Requirements stated in chunk |
|---|---|
| Express service | Follow RESTful principles; include error handling middleware; set up proper logging; `@express-service-template.ts` |
| React component layout | Props interface at top; component as named export; styles at bottom; `@component-template.tsx` |

## Automating development workflows and documentation generation
| Workflow | Steps stated in chunk |
|---|---|
| Analyze the app | Run dev server with `npm run dev`; fetch logs from console; suggest performance improvements |
| Draft documentation | Extract code comments; analyze README.md; generate markdown documentation |

## Adding a new setting in Cursor
Sequence stated in chunk:
1. Create a property to toggle in `@reactiveStorageTypes.ts`.
2. Add default value in `INIT_APPLICATION_USER_PERSISTENT_STORAGE` in `@reactiveStorageService.tsx`.
3. For beta features add toggle in `@settingsBetaTab.tsx`, otherwise in `@settingsGeneralTab.tsx`, as `<SettingsSubSection>` for general checkboxes.
4. Read it in the app via `reactiveStorageService` property `myNewProperty`.

Verbatim toggle sketch from chunk:
> `<SettingsSubSection  label="Your feature name"  description="Your feature description"  value={    vsContext.reactiveStorageService.applicationUserPersistentStorage      .myNewProperty ?? false  }  onChange={(newVal) => {    vsContext.reactiveStorageService.setApplicationUserPersistentStorage(      "myNewProperty",      newVal,    );  }}/>`

Verbatim usage sketch from chunk:
> `const flagIsEnabled =  vsContext.reactiveStorageService.applicationUserPersistentStorage    .myNewProperty;`

Chunk note: "Examples are available from providers and frameworks. Community-contributed rules are found across crowdsourced collections and repositories online."

## Team Rules
- "Team and Enterprise plans can create and enforce rules across their entire organization from the Cursor dashboard."
- "Admins can configure whether or not each rule is required for team members."
- "Team Rules work alongside other rule types and take precedence to ensure organizational standards are maintained across all projects."

## Managing Team Rules
- "Team administrators can create and manage rules directly from the Cursor dashboard."
- "Once team rules are created, they automatically apply to all team members and are visible in the dashboard."

## Activation and enforcement
- "Enable this rule immediately: When checked, the rule is active as soon as you create it. When unchecked, the rule is saved as a draft and does not apply until you enable it later."
- "Enforce this rule: When enabled, the rule is required for all team members and cannot be disabled in Customize. When not enforced, team members can toggle the rule off under Team Rules in Customize."
- "By default, non‑enforced Team Rules can be disabled by users. Use Enforce this rule to prevent that."

## Format and how Team Rules are applied
- "Content: Team Rules are free‑form text. They do not use the folder structure of Project Rules."
- "Glob patterns: Team Rules support glob patterns for file-scoped application. When a glob pattern is set (e.g., **/*.py), the rule only applies when matching files are in context. Rules without a glob pattern apply to every conversation."
- "Where they apply: When a Team Rule is enabled (and not disabled by the user, unless enforced), it is included in the model context for Agent (Chat) across all repositories and projects for that team."
- "Precedence: Rules are applied in this order: Team Rules → Project Rules → User Rules. All applicable rules are merged; earlier sources take precedence when guidance conflicts."
- "Some teams use enforced rules as part of internal compliance workflows. While this is supported, AI guidance should not be your only security control."

## Importing rules from a repository
- "Rules aren't imported on their own. To bring rules in from a GitHub repository, package them in a plugin and publish that plugin through a marketplace: import the repository in Customize with From GitHub Repository (the repository needs a .cursor-plugin/marketplace.json), or add it as a team marketplace, then install the plugin. The rules arrive with the plugin and appear in Customize alongside your other rules."

## AGENTS.md
- "AGENTS.md is a simple markdown file for defining agent instructions. Place it in your project root as an alternative to .cursor/rules for straightforward use cases."
- "Unlike Project Rules, AGENTS.md is a plain markdown file without metadata or complex configurations."
- "Cursor supports AGENTS.md in the project root and subdirectories."

## Improvements — Nested AGENTS.md support
- "Nested AGENTS.md support in subdirectories is now available. You can place AGENTS.md files in any subdirectory of your project, and they will be automatically applied when working with files in that directory or its children."
- Example tree from chunk: `project/  AGENTS.md              # Global instructions  frontend/    AGENTS.md            # Frontend-specific instructions    components/      AGENTS.md          # Component-specific instructions  backend/    AGENTS.md            # Backend-specific instructions`
- "Instructions from nested AGENTS.md files are combined with parent directories, with more specific instructions taking precedence."

## User Rules
- "User Rules are global preferences defined in Customize → Rules that apply across all projects. They are used by Agent (Chat) and are perfect for setting preferred communication style or coding conventions:"
- Verbatim example: "Please reply in a concise style. Avoid unnecessary repetition or filler language."

## FAQ
| Question | Answer stated in chunk |
|---|---|
| Why isn't my rule being applied? | "Check the rule type. For Apply Intelligently, ensure a description is defined. For Apply to Specific Files, ensure the file pattern matches referenced files." |
| Can rules reference other rules or files? | "Yes. Use @filename.ts to include files in your rule's context. You can also @mention rules in chat to apply them manually." |
| Can I create a rule from chat? | "Yes, you can ask the agent to create a new rule for you." |
| Do rules impact Cursor Tab or other AI features? | "No. Rules do not impact Cursor Tab or other AI features." |
| Do User Rules apply to Inline Edit (Cmd/Ctrl+K)? | "No. User Rules are not applied to Inline Edit (Cmd/Ctrl+K). They are only used by Agent (Chat)." |

## Related
Chunk lists under Related: "Rules help" and language options "English", "English", "简体中文", "Русский", "日本語", "Português", "Español".

**Covers:** Covers the Examples chunk of the Cursor Rules docs page.
