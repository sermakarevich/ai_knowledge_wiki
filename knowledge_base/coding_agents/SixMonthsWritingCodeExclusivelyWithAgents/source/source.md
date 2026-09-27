> PDF location (no source.pdf bundled; article source): https://blog.exe.dev/engineering-with-ai
# Six Months of Writing Code Exclusively With Agents - exe.dev blog
Source: https://blog.exe.dev/engineering-with-ai
Kind: article
Fetched: 2026-09-25T05:41:13.143762+00:00
Tool: urllib
Topic: coding_agents

Six Months of Writing Code Exclusively With Agents - exe.dev blog

In February of this year, I made a rule for myself: I wasn’t going to write code by hand anymore. I’ve been living by that rule for six months.

## The system lived in my head

Back in 2024, before AI, my superpower was knowing how the entire system worked, especially the interfaces between its different components.

If someone came to me with a feature they wanted to build or a bug they were trying to fix, I could usually point them to the exact line of code that mattered and tell them what needed to change. I also remembered why the strange-looking decisions existed and which assumptions were never written down.

This was knowledge I’d built over months and years of working in the codebase. It was hard-earned and invaluable. It let me build features quickly and, more importantly, safely.

The cost was that I had to keep up with everything. As more people contributed, I spent more and more time reading changes just to maintain that mental model.

The bigger cost was the typing. Every time I wanted to build something, I could see the code in my head. I just couldn’t type it out fast enough.

Typing speed was only part of the problem: a feature was almost never one edit. Even a small change spanned multiple layers and touched handlers, schema, tests, and docs. And those edits weren’t equal: a bad handler could be reverted, but a bad migration could leave a mess behind. So writing the code by hand meant carrying one decision safely through every place it touched.

Copilot autocomplete helped immediately: a doc comment became a first draft, often wrong, but beats editing a blank file. Cursor’s tab complete helped more. The models were clearly improving fast.

Claude Code changed a ton. I could describe the change once, and the agent would edit a bunch of files at once.

As a result, I typed a lot less. But typing less didn’t mean working less: I read every change the model generated to match it against the desired state I had in my head. Agents would still be wrong quite a lot and make changes that weren’t required. Working incrementally kept them on track. This meant hand editing some of the generated code. After all, I was still responsible for every line that merged. The model wasn’t going to be held accountable.

Then, early this year, the models got really good, almost all at once. GPT-5.3 and Opus 4.6 could suddenly handle larger changes with much less steering, and the results were finally good enough to build on.

So in February I made the rule: no more code by hand. If an agent got stuck, I wasn’t allowed to finish the code myself. I had to figure out what the agent was missing - and fix that instead.

I didn’t get good at coding by reading about coding. I got good by writing a lot of code, running it, seeing it fail, fixing it, and doing it again.

AI agents are just software, after all. I wasn’t going to understand them by reading prompt guides. I had to use them for real work, see where they failed, change the prompts, tools, or environment, and try again.

The rule forced me to get those reps.

I broke it once, for three minutes. I opened the code and wrote a few lines, and it felt great. I had missed this. Right up until I realized how much I still had to type. I noped out.

## One agent became a dozen

Once I stopped typing the code myself, I started finding these pockets of free time. I would give an agent a task, and then there was nothing for me to do while it worked.

Instead of waiting, I spun up another agent to do something else. Then I did it again.

I wasn’t intentionally building a parallel system. I was just filling the time between tasks. I have ADHD. I got distracted.

It’s easy to imagine what would happen if you shared a single dev box between colleagues. Now imagine they don’t talk to each other and they’re all working at the same time.

That was my first parallel setup. The agents changed the same files and Git state, installed dependencies, fought over ports, and left processes running. I also had to coordinate when each agent could test, push, or deploy. Worse, I often ended up waiting for the longest-running agent before the others could move forward. I had started more agents to avoid waiting and somehow created a new way to wait.

I asked friends and colleagues how they dealt with this, and everyone had a workaround.

Worktrees came up first. Each agent got its own checkout and branch, and the source collisions mostly went away, but worktrees only solved the Git part. The agents still shared databases, ports, processes, and the rest of the machine.

So people patched around that with AGENTS.md: use a random port, create an ephemeral database, don’t touch another agent’s process. Every conflict became another instruction, and the agents burned context figuring out how not to step on each other instead of doing the task.

Containers got closer: separate ports, processes, and local state. But the boundary was leaky: whatever my laptop could reach, the container could potentially reach too. The blast radius of a bad command wasn’t contained, so I was still approving commands. And worst of all, my laptop had to stay awake. If I closed it, all of the work stopped.

## I closed my laptop. The work kept going.

By this point, I had joined exe.dev. We make Linux VMs that come up in a couple of seconds with SSH and HTTPS already set up, so moving the agents off my laptop was the natural next step.

Each task got its own machine. I could close my laptop, walk away, and the work kept running.

But now I had a new problem: how do I reliably bring up a complete development environment for whatever I want the agent to work on?

So, staying true to not writing code, I asked Claude to write a startup script. I told it what I wanted and instructed it to loop until things worked. It installed our toolchains, cloned the repositories, configured Claude Code and Codex, and did everything needed to turn a fresh VM into a development environment. Then it ran the validation loop: bring up a fresh box, run the script, see what broke, fix the script, and try again.

The agent boxes worked, but each agent still had its own tmux session. I ended up keeping a dozen terminal windows open just to see what each agent was doing. I had to jump between them to find which agent had finished, which one was stuck, and which one needed something from me. I needed one place to manage all of them.

So I built botd.

I gave it three rules. First, it had to run somewhere other than my laptop (the agents should keep working when I closed it). Second, mobile had to be first-class. Managing agents shouldn’t require sitting in front of a terminal. Third, it had to preserve every conversation so I could look back across agents and understand where they got stuck, which instructions worked, and which problems kept repeating.

botd provisioned and deprovisioned the agent boxes, drove the agents underneath, and kept track of every task. It showed me which agents were working, which were stuck, and which were waiting for me. From my phone or laptop, I could inspect the conversation, send follow-up instructions, and review the diff.

Instead of managing a dozen terminal sessions, I had one place to manage the work.

None of this worked if I had to approve every tool call. That would just turn me into the queue again. Each agent was running inside an isolated, disposable VM, so I let it run in YOLO mode. It could run bash commands, install packages, start services, and change whatever it needed. A trashed environment cost me nothing but the VM.

But an agent that can only touch its own VM isn’t very interesting. I still wanted agents to read logs, pull from Git, call Anthropic or OpenAI, and inspect things in Stripe.

That access is where the real risk lived, and the VM did nothing to bound it. An agent reads untrusted content and can be prompt-injected by it; whatever it can reach, an injected agent can leak or corrupt. There were holes I knew I hadn’t filled. So every piece of external access got the same question: what’s the worst that can happen through this? Reading mostly passed: agents got read-only access. Writing didn’t, so write access was limited to test environments, where the worst case was corrupted test data.

I also didn’t want the credentials inside the VM. With exe.dev integrations, the agent sends its request through a proxy, the proxy adds the credential, and the agent receives the response without ever seeing the secret.

## Everything passed. I still didn’t want it.

At peak I was running about twenty VMs at a time. Not all of them were active. Some tasks got started, sat untouched for weeks, and were eventually abandoned because the cognitive overhead was too much and the work was never urgent or important enough to survive.

Validation sucked at that scale. I couldn’t manually rebuild every branch, rerun its tests, and check the application myself. But inside their isolated boxes, agents could run the tests, trigger the full CI suite, start the application, and drive it through a browser. They would send me screenshots of the completed work.

But the agent was still grading its own work. If it misunderstood what I wanted, it could build the wrong thing, write tests for the wrong thing, and then confidently tell me that everything passed.

That’s why being able to open the running environment mattered. I could use it myself, drive the new UI end to end, and make sure it worked the way I wanted, not just the way the agent said it worked.

Then there was the reviewing. When I wrote the code myself, I understood the change by the time it was ready for review. After all, I had made the decisions along the way. With an agent, the whole diff appeared at once. It might have passing tests and screenshots, but it was still unfamiliar code. And when several agents finished around the same time, I had a queue of complete changes to load into my head before I could merge any of them.

Having other agents review the code worked surprisingly well. They occasionally caught real bugs, and it was cheap enough to run several reviews. But I couldn’t merge something just because the agents approved it. I still had to understand the change. I was still responsible for the code that got merged.

And sometimes I understood it. The tests were green, the screenshots looked good, the UI did what I had asked for, even the schema looked good and the code was approved by all the review agents.

I threw it away anyway.

Maybe nobody needed it. Maybe it introduced a second way to do something we already supported. Maybe a small convenience added complexity we would carry for years.

The tools could tell me that the change worked. They couldn’t tell me whether it was worth adding to the system.

Unshipping something is so much harder than shipping it. Hyrum’s Law kicks in: once enough people use a system, someone depends on every observable behavior, even behavior you never intended to be a contract. Removing something breaks users, scripts, and workflows you didn’t know existed.

Shipping got easy. Deciding what to ship got important.

## Not all agents write code

Everything so far has been about shipping code. But some of the most useful agents we run don’t ship code at all.

It’s worth pausing on what an agent actually is, because the word sounds heavier than it deserves. An agent is a model in a loop with tools. Send the model a message; if it asks for a tool call, run the tool and send the result back; repeat. That’s the whole thing.

The model is what makes the loop capable. Give it bash on a real computer, and it can install what’s missing, adapt when your grep has different flags, and keep going until the job is done.

The loop never changes. The tools decide what an agent can be. A development agent needs a full computer: shell, compilers, browsers, the freedom to install things. Hold those back and the agent is useless, and you’re back to approving every action.

My starting point: give the agent whatever I’d give a developer. Good developer tools have turned out to be good agent tools. Whether the best agent tools end up being developer tools at all, time will tell.

And the thing to fear isn’t any single tool. It’s combinations. Private data, untrusted content, external communication: any two are manageable. All three in one agent is how your secrets walk out the door. That’s what Simon Willison calls the lethal trifecta. So I don’t minimize tools blindly: I isolate the environment and I watch the combinations.

Here’s the first example: investigation. When a customer reports a problem, I have a prompt I use, and it’s embarrassingly simple:

“Customer reports: <their report, verbatim>. Please figure out what happened using the ClickHouse logs.”

Verbatim matters. If I summarize the report, the agent inherits my interpretation - and my blind spots. Given the customer’s own words, it queries the logs, reads the relevant code, and reconstructs what actually happened.

Then the decision is mine. Sometimes I ask for options and pick one. Sometimes the evidence says working-as-intended, and the fix is a doc or an email, not code. Either way I’m deciding from evidence, not guessing from a bug report.

The second job: attack. Our red-team agent has one instruction: try to break into our systems.

And it worked. It found open network paths we thought we had restricted, and showed us exactly how they were still reachable. We patched them before anyone outside ever noticed.

That’s more useful than a list of theoretical vulnerabilities. It took an assumption we were relying on and tested it against the running system, and the assumption was wrong.

The third job: watch. Deployments are scary, but not deploying is worse. We deploy in waves, and writing perfect rules for when to continue is basically impossible: production fails in weird ways.

So Athena babysits every deployment. It reads the diff, the metrics, and the logs, and watches the rollout. During one deployment it noticed a problem, investigated, and realized it was an infrastructure issue, not the new code. Instead of blindly halting everything, it continued deploying to the other machines.

Could I do a better job? I’m not sure anymore. Athena is more diligent than I can be. It doesn’t get distracted, doesn’t get impatient, and never stops paying attention. It is tireless.

## Engineer the system before the agent writes the code

An agent can now design and build an entire system almost instantly. The design might even be good. But if I simply accept it, do I know how it works? Where it breaks? Which corners it cut? Which tradeoffs I agreed to?

At that point, I’ve inherited a legacy codebase that happens to be brand new. That’s vibe coding.

Agentic engineering is working with the agent on the system first: the architecture, interfaces, constraints, and tradeoffs. When the code arrives, I understand what I’m about to own.

There is no one answer to agentic engineering. Everyone works differently; every model is good at different things. The key here is reps: do a lot, ask a lot, throw away a lot. You’ll learn what works for you.

Everything we knew about running software teams is amplified now. Start with testing. When agents write and rewrite the implementation, unit tests that mirror the implementation just churn with it. Behavior, contract, and property tests matter so much more now: define the system’s invariants and pin down what must stay true while the code underneath changes freely.

So much of the game is migrations now. Code changes are cheap, but systems carry state: data, running processes, users mid-flight. Getting from one design to the next without dropping any of that is the part that’s still hard. The job is risk management and migrations.

The agent copies what it finds in the codebase. Good patterns amplify. Bad patterns amplify faster. Engineering hygiene is more important than ever: every pattern you tolerate becomes the template for the next hundred changes.

And it’s the golden age of personalized tools. You don’t have to be a domain expert to write a new linter. So write a new linter. Enforce the pattern, encode the lesson, make the mistake impossible. The marginal cost of a bespoke tool has collapsed.

Peer code review is dead. We don’t do code reviews at exe.dev: we merge code we deem should be merged. The review that matters happens earlier: in the design discussion, the contracts, the validation. By the time the diff exists, the decisions are already made.

Here’s a recent example. Shelley is the coding agent we ship in exe.dev VMs. I wanted its tools to be asynchronous.

The first design put the onus on the agent to decide which commands should run in the background. That introduced a ton of edge cases: large outputs, long-running tasks, blocked agents, and the agent having to predict all of this ahead of time.

If I were vibe coding, I would have accepted that design and let the agent deal with those edge cases. Maybe it would have handled them. Maybe it wouldn’t have. I wouldn’t really know.

Instead, we kept discussing the problem and found a design that removed most of the edge cases entirely. Every command follows the same path and automatically moves into the background after sixty seconds.

I didn’t remember this example off the top of my head. I asked an agent to search across all of my agent conversations for a case where my questions had materially changed the architecture. It returned the original request, the first design, the objections I raised, how the design changed, the final commit, and links to the original sessions.

This is why preserving every conversation mattered. The history wasn’t just an archive. I could query it to understand how I worked.

## botd is dead; long live botd

There’s one more part of this story. botd died this month. It crumbled under its own weight.

That probably shouldn’t be surprising. botd was entirely vibe coded. I didn’t read a single line of its code, nor did I really pay attention to how it was architected. And at its core was a genuinely hard problem: driving every model family through its own native harness (Claude Code, Codex, and the rest) while papering over their differences. That is exactly the kind of problem where architecture matters, and I was not paying attention to it.

It helped me deliver an enormous amount of work, but it eventually became the exact thing I described earlier: a brand-new legacy codebase that I had inherited without understanding all of the decisions inside it. The architecture was exploratory, and some of the decisions buried in it made even modest changes mean redoing large parts of the system. And I wanted to build on top of Shelley so that I could control the harness better; botd was living on borrowed time. It just died before I could retire it.

But here’s the twist: that search I described earlier was never sent to botd. All the history was in SQLite, so I pointed another agent at it and got the analysis anyway. The tool died; the data didn’t.

When I started, my advantage was that the system lived in my head. Six months later, the honest answer is that I’ve lost some of that depth. I don’t have the same line-by-line familiarity with every system.

But I can ask agents detailed questions and use them to dig into whatever I need to understand. Work no longer waits for me to finish one thing before starting another.

I’ve shipped more in these six months than in any stretch of my career. I’ve also failed more: abandoned VMs, dead-end designs, a whole tool that collapsed. The failures were cheap, so I could afford a lot of them - that’s most of how I learned what works.

It’s the same loop that taught me to code, moved up a level: write, run, fail, fix. I used to iterate on code. Now I iterate on prompts, designs, whole features. A rewrite that used to cost a week costs a conversation. And understanding is iterative too: every conversation helps me understand and internalize the system more.

I stopped writing code by hand. I didn’t stop engineering.
