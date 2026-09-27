[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Not all agents write code
**In one sentence:** The most useful agents often don't write code at all — investigation, red-teaming, and deployment-watching agents plus up-front system engineering matter more than the code itself, as the vibe-coded collapse of botd proves.

## Key points
- An agent is just a model in a loop with tools, so the loop never changes and the tools decide what the agent can be — a dev agent needs a full computer (shell, compilers, browsers, install freedom).
- Tool risk comes from combinations, not single tools: private data + untrusted content + external communication together is Simon Willison's "lethal trifecta," so the author isolates environments and watches combinations rather than minimizing tools blindly.
- Investigation agents work from the customer's verbatim report queried against ClickHouse logs plus code reading, and the output is evidence for a human decision — sometimes the fix is a doc or email, not code.
- The red-team agent ("try to break into our systems") found open network paths thought to be restricted and showed exactly how they were reachable, so they were patched before outsiders noticed.
- The deploy-watcher Athena reads diff, metrics, and logs during wave rollouts and once correctly continued deploying to other machines after diagnosing a failure as infrastructure, not the new code.
- Agentic engineering means designing architecture, interfaces, constraints, and tradeoffs before accepting code, otherwise you inherit a brand-new legacy codebase — "that's vibe coding."
- Engineering hygiene amplifies under agents: behavior/contract/property tests beat implementation-mirroring unit tests, migrations/state handling is the hard part, tolerated bad patterns become templates, and cheap bespoke tools (e.g. a new linter) should encode lessons.

---
## Not all agents write code
**Covers:** agent definition, tool philosophy, investigation / red-team / deploy-watch roles

An agent is "a model in a loop with tools. Send the model a message; if it asks for a tool call, run the tool and send the result back; repeat. That's the whole thing." The model supplies capability (given bash on a real computer it installs what's missing, adapts to different grep flags, keeps going); the tools decide what the agent can be.

| Principle | Claim (verbatim/paraphrase) |
|---|---|
| Starting point | "Give the agent whatever I'd give a developer. Good developer tools have turned out to be good agent tools." |
| Tool risk | "The thing to fear isn't any single tool. It's combinations. Private data, untrusted content, external communication: any two are manageable. All three in one agent is how your secrets walk out the door." — Simon Willison's "lethal trifecta"; response is isolate the environment and watch combinations, not minimize tools blindly |

Non-coding roles:

- **Investigate.** Prompt is "embarrassingly simple": `"Customer reports: <their report, verbatim>. Please figure out what happened using the ClickHouse logs."` Verbatim matters — summarizing injects the author's interpretation and blind spots. The agent queries logs, reads relevant code, reconstructs what happened; then the human decides (pick among options, or accept working-as-intended with a doc/email fix).
- **Attack.** Red-team agent with one instruction: "try to break into our systems." It found open network paths believed restricted and demonstrated exactly how they were still reachable; patched before anyone outside noticed. Value: tested a relied-upon assumption against the running system instead of listing theoretical vulnerabilities.
- **Watch.** "Deployments are scary, but not deploying is worse. We deploy in waves, and writing perfect rules for when to continue is basically impossible: production fails in weird ways." Athena babysits every deployment (diff + metrics + logs); in one rollout it investigated a problem, diagnosed an infrastructure issue rather than bad new code, and continued deploying to the other machines instead of blindly halting. "Athena is more diligent than I can be. It doesn't get distracted, doesn't get impatient, and never stops paying attention. It is tireless."

## Engineer the system before the agent writes the code
**Covers:** agentic engineering vs vibe coding, testing, migrations, hygiene, Shelley async-tools example, conversation history

An agent can design and build a whole system almost instantly and the design "might even be good" — but accepting it blind means not knowing how it works, where it breaks, which corners were cut, which tradeoffs were agreed to. "At that point, I've inherited a legacy codebase that happens to be brand new. That's vibe coding." The alternative: "Agentic engineering is working with the agent on the system first: the architecture, interfaces, constraints, and tradeoffs. When the code arrives, I understand what I'm about to own." No single method — "reps: do a lot, ask a lot, throw away a lot."

| Engineering lesson | Detail from chunk |
|---|---|
| Testing | Implementation-mirroring unit tests churn with agent rewrites; behavior, contract, and property tests matter more — define invariants that stay true while code changes freely |
| Migrations | "Code changes are cheap, but systems carry state: data, running processes, users mid-flight. Getting from one design to the next without dropping any of that is the part that's still hard. The job is risk management and migrations." |
| Hygiene | "The agent copies what it finds in the codebase. Good patterns amplify. Bad patterns amplify faster." Every tolerated pattern becomes the template for the next hundred changes |
| Personalized tools | "You don't have to be a domain expert to write a new linter. So write a new linter. Enforce the pattern, encode the lesson, make the mistake impossible. The marginal cost of a bespoke tool has collapsed." |
| Code review | "Peer code review is dead. We don't do code reviews at exe.dev: we merge code we deem should be merged. The review that matters happens earlier: in the design discussion, the contracts, the validation." |

Worked example — Shelley (the coding agent shipped in exe.dev VMs) async tools: the first design made the agent decide which commands run in the background, creating edge cases (large outputs, long-running tasks, blocked agents, predicting ahead of time). Discussion removed most edge cases instead: every command follows the same path and automatically moves into the background after sixty seconds. The author didn't recall this offhand — an agent searched all agent conversations and returned the original request, first design, objections, design change, final commit, and session links, which is why preserving every conversation mattered: "The history wasn't just an archive. I could query it to understand how I worked."

## botd is dead; long live botd
**Covers:** botd collapse, SQLite history survival, iteration loop

- botd "died this month. It crumbled under its own weight." Cause: "botd was entirely vibe coded. I didn't read a single line of its code, nor did I really pay attention to how it was architected." Its core was genuinely hard — driving every model family through its native harness (Claude Code, Codex, and the rest) while papering over differences — "exactly the kind of problem where architecture matters."
- It delivered enormous work but became "a brand-new legacy codebase that I had inherited without understanding all of the decisions inside it"; exploratory architecture meant modest changes required redoing large parts; the author also wanted to build on Shelley to control the harness, so "botd was living on borrowed time. It just died before I could retire it."
- Twist: the conversation-search analysis was never sent to botd — "All the history was in SQLite, so I pointed another agent at it and got the analysis anyway. The tool died; the data didn't."
- Closing ledger: "When I started, my advantage was that the system lived in my head. Six months later… I've lost some of that depth. I don't have the same line-by-line familiarity with every system. But I can ask agents detailed questions and use them to dig into whatever I need." More shipped than in any career stretch, but also more failures (abandoned VMs, dead-end designs, a collapsed tool) — "The failures were cheap, so I could afford a lot of them." Same loop moved up a level: "write, run, fail, fix. I used to iterate on code. Now I iterate on prompts, designs, whole features. A rewrite that used to cost a week costs a conversation." Final line: "I stopped writing code by hand. I didn't stop engineering."
