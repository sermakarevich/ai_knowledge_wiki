> [[index|Wiki]] | [[summary|Summary]]
# Harness — In Plain Language
## What is this about?
Think of Harness as the foreman on a construction site.
On this site, all the workers are artificial intelligence (AI) helpers that write computer programs.
Each helper is fast but forgetful.
Each helper takes instructions very literally.
Each helper is sometimes overconfident.
Left alone, ten helpers would trip over each other.
They might fix the same wall twice.
They might knock down something important.
Harness is the system around them that keeps the site orderly.
It hands out jobs.
It sets safety rules.
It checks the finished work.
It keeps a full logbook.
It cleans up when something stalls or fails.
It does not write the programs itself.
It manages the workers who do.
## Why does it matter?
One AI helper is easy to watch.
Ten or fifty working at once are not.
Without coordination, familiar problems appear.
Two helpers edit the same piece at the same time.
A helper deletes something it should never touch.
Nobody notices bad work until much later.
There is no record of who did what or what it cost.
Harness matters because it answers four basic management questions at scale.
Who should do what next.
What is each worker allowed to touch.
Is the result actually good.
What exactly happened along the way.
That turns a crowd of fast but unreliable helpers into something closer to a dependable crew.
## How does it work?
Picture a construction site.
Harness is the foreman in the site office, plus a team of independent building inspectors.
1. A job arrives at the office.
A customer request, such as "fix this reported problem," comes in through a single front desk.
The foreman writes it down as a work order.
The foreman decides whether it first needs a plan or can go straight to building.
The plan is filed separately, so the idea stays distinct from the day-to-day tasks.
2. The foreman checks capacity and budget.
Before assigning anything, the foreman asks if this crew is qualified.
The foreman asks if there is a free spot on this part of the site.
The foreman asks if too much time or money has already been spent today.
The foreman asks if the safety setup is available.
If the answer is no, the job waits politely in line instead of overloading the site.
3. Each worker gets a separate workspace and a timed permit.
Every job gets its own fenced-off copy of the work area, so workers do not collide.
Each job also gets a timed permit slip.
The slip has the holder's name on it, an expiry time, and a version number.
While working, the holder keeps renewing the slip.
If a worker disappears, the slip expires.
The foreman can then safely hand the same job to someone else.
4. Rules limit what workers may do.
Some actions are freely allowed.
Some need a supervisor nod.
Some are flatly forbidden.
The rules are written down as simple lists, such as "commands starting with these words need approval."
Workers are also fenced in physically.
Some may only look but not change anything.
Some may build only inside their own plot.
Internet access is controlled separately from building access.
5. Workers from different companies speak through one interpreter.
Harness can hire different brands of AI helpers.
Each brand talks differently.
So Harness puts a standard interpreter in front of each one.
The foreman always gives orders in the same format.
The foreman always receives progress reports in the same format.
It does not matter who is actually swinging the hammer.
6. Finished work goes to independent inspectors.
A first inspector writes up findings.
Then a second, different inspector must confirm, dispute, or add to each finding.
This runs for a few bounded rounds.
The same helper is never allowed to inspect its own work.
Only when no agreed problems remain does the work pass.
7. Automatic quality checks do the measuring and testing.
Formatting is checked.
Automated tests are run.
Proof that the promised delivery actually exists is verified.
If outside feedback arrives, such as failed tests or requested changes, a limited repair loop tries to fix it.
It does not loop forever.
8. Patterns of mess trigger a cleanup crew.
If the logbook shows repeated warnings, stuck jobs, over-edited files, slow sessions, or many small rule breaks, a separate crew steps in.
That crew proposes a fix to the rulebook or the shared instructions.
The proposal sits as a draft.
It is applied only after a human or a strict automatic check approves it.
9. Everything is written in a permanent logbook.
Every decision, warning, block, token count, and cost is stored in one central record book.
Optional standard telemetry exports let outside monitoring tools read traces, counts, and logs.
This is how you later answer what happened, how long it took, and what it cost.
## Where can this be used?
Fixing reported software problems at scale.
Turn a long list of bug reports into planned, assigned, built, reviewed, and merged fixes.
No single manager has to hand-hold every step.
Running several AI helpers in parallel safely.
Give each helper its own isolated copy of the project.
Give each helper its own budget of turns.
Give clear "do not touch what your neighbor owns" instructions.
Enforcing safety for powerful automated tools.
Keep helpers away from sensitive files unless explicitly permitted.
Keep helpers away from dangerous commands unless explicitly permitted.
Keep helpers away from open internet access unless explicitly permitted.
Any review pipeline that needs a second pair of eyes.
For example writing, legal drafting, lesson plans, or grant proposals.
One AI drafts, and a different AI must confirm or challenge each flagged issue.
Any team that needs a paper trail.
For example customer support automation, document processing, or research assistance.
You must later show each step, each cost, and each approval.
Self-improving operations.
Detect repeated friction, such as the same warning fifty times.
Turn it into a proposed rule or checklist update instead of tribal knowledge.
## Conclusions & takeaways
Harness treats AI helpers like strong but junior workers.
Useful in numbers, unsafe without supervision.
Its core trick is separation.
A central office plans and records.
Isolated plots prevent collisions.
Written rules prevent accidents.
Independent inspectors prevent self-praise.
Timed permits make crashes recoverable.
The result is less about any single clever helper.
It is more about making a whole fleet boringly reliable: bounded, checkable, and traceable.
If you remember one image, remember the foreman plus the inspectors plus the logbook.
That is the whole idea.
## Jargon decoder
| Term | Plain meaning |
|---|---|
| Control plane | The site office: the central manager that assigns jobs and keeps records, separate from the workers |
| Policy engine | The written safety rulebook plus the clerk who checks actions against it |
| Worktree | A separate fenced-off copy of the work area for one job, so workers do not collide |
| Reconcile | Walking the site and comparing the paperwork with reality, then fixing mismatches |
| Lease | A timed permit slip for a job: who holds it, when it expires, renewed while work continues |
| Sandbox | The fence and locked gates around a worker: what ground it may touch and whether it may reach the internet |
| Adapter | The interpreter that lets the foreman talk to different brands of AI helpers in one standard way |
| OTLP | A standard shipping format for monitoring data: traces, counts, and log entries sent to outside tools |
| Workflow | The step-by-step recipe for a kind of job: plan, build, check, deliver |
| Quality gate | A checkpoint with tests the work must pass before it may move forward |
| Garbage collection | The cleanup crew: spotting stale, stuck, or messy work and proposing rulebook fixes |
