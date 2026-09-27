> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# A Generalized Software Architecture for Swarm — In Plain Language

## What is this about?

This paper proposes a new way to organize teams of AI agents.

Today, most multi-agent systems built on Large Language Models (LLMs,
AI models trained on text that can reason, plan, and use tools) work like
a company with one boss: a central organizer program breaks a big goal
into smaller jobs, hands them to worker agents, and collects the results.

The paper says: remove the boss. Let all agents be equals (peers) that
coordinate among themselves using shared rules (protocols).

The big goal — for example "research this topic" or "write this program" —
is split again and again into smaller and smaller jobs until each job is
small enough for one agent to do. Agents then volunteer for jobs they are
good at, share updates with each other, and cover for teammates that fail
or leave.

The design has three working areas, called planes:

- The task plane handles the life of each job: splitting it up,
  announcing it, volunteering for it, doing it, and combining results.
- The state plane is the shared notebook: what jobs exist, what is done,
  and what is still waiting.
- The membership plane tracks who is currently in the team, including
  newcomers, departures, and crashes.

## Why does it matter?

A central organizer causes three problems:

1. Single point of failure. If the boss crashes, the whole team stops.
2. Bottleneck. As the team grows to hundreds or thousands of agents,
   one boss cannot keep up with all the assignments.
3. Narrow design. The boss usually contains assumptions about one specific
   kind of task, so it cannot be reused for a different kind of work.

The paper sets three goals that no widely used design meets all at once:

- Task-agnosticism: the same coordination rules should work for any kind
  of job, from research to coding, without rewriting the core.
- Decentralization: coordination, shared notes, and decisions should be
  spread across all agents, with no privileged controller.
- Operational resilience: the team should keep making progress even when
  agents join, leave, crash, or the network splits temporarily.

Solving all three together is the paper's main contribution.

## How does it work?

Think of the swarm as a group chat of helpers where everyone follows
five house rules:

1. Decide locally. Each agent acts on the information it has right now,
   even if that information is slightly out of date.
2. Keep coordination separate from meaning. The coordination rules only
   pass around sealed envelopes (job descriptions); only the agent doing
   the job opens the envelope and understands the contents.
3. Keep copies. Important notes exist in several places, and important
   jobs can be given to more than one agent.
4. Degrade gracefully. When things break, slow down but keep going.
5. Use proven building blocks. Reuse standard distributed-systems tools (many
   computers cooperating over a network) instead of inventing everything.

The work flows in a repeating cycle:

1. Split. Whoever receives the user's goal becomes its temporary starter
   (root holder). It breaks the goal into sub-jobs and writes them into
   a shared to-do graph: a Directed Acyclic Graph (DAG, a map of jobs
   with arrows showing which job must finish before another can start).
2. Announce. Each waiting job is announced to nearby agents, aimed at
   agents whose skills look like a match.
3. Volunteer (bid). Each interested agent sends a bid: a score combining
   how well its skills match, how free it currently is, and its reputation
   from past good work. Busy or unreliable agents score lower.
4. Assign (award). After a short waiting window, the best scorer wins.
   Occasionally a random runner-up wins instead, so work does not pile up
   on one superstar. Ties are broken by agent ID number, so everyone
   agrees on the winner even if messages arrive in different orders.
5. Do and repeat. The winner does the job and may split it further. When
   it finishes, it publishes the result into a shared result store.
   Jobs whose prerequisites are now met move from waiting to open
   for volunteering, and the cycle continues.

Keeping everyone in sync works like gossip: every few seconds, each agent
swaps recent updates with a few neighbors. News spreads team-wide in roughly
logarithmic steps, so a ten-times-bigger team needs only a few extra rounds.
Conflicts (two agents thinking they own the same job) are resolved by
Conflict-free Replicated Data Types (CRDTs, shared records that always
merge cleanly across computers).

Strong agreement (a vote similar to Raft, a popular algorithm for getting computers
to agree on one value) is used only for rare, irreversible moments such
as declaring the whole goal finished.

If an agent crashes, its jobs return to the waiting pool and are
re-assigned. Optionally, a backup agent (shadow agent) stands by and
takes over immediately. If the network splits, each half keeps working
and their notebooks merge cleanly when the connection returns.

## Where can this be used?

Because the coordination layer never looks inside the job contents, the
same design can host many different kinds of work. The paper names:

- Collaborative research: many agents searching, reading, and summarizing.
- Distributed code synthesis: many agents writing and testing parts of a program.
- Document analysis: many agents reading through large document sets.
- Knowledge-graph construction: many agents extracting facts and links.

Any cooperative workload with splittable, describable, checkable jobs could run
on top. Only each agent's thinking part (how to split, do, and check a job)
changes per domain; the teamwork rules stay the same.

## Conclusions & takeaways

- No boss needed: a swarm of equal agents can split work, volunteer by
  skill and availability, and finish complex goals without a central
  organizer.
- Gossip plus mergeable records is enough for day-to-day teamwork; costly
  voting is reserved for final, irreversible decisions.
- The design scales: per-agent effort grows slowly (sub-linearly), so
  teams of thousands of agents stay practical on paper.
- Failures are routine events, not emergencies: crashes, departures, and
  network splits are absorbed through copies, backups, and re-assignment.
- Limits are honest: agents are assumed not to lie or sabotage (non-Byzantine:
  crashes, not attacks), skill is one number, there is no payment scheme, and
  large-scale simulation is still needed to prove the math.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Swarm | A large team of equal AI agents cooperating without a boss |
| Task-agnostic | Works for any kind of job without changing the core rules |
| Peer-to-peer overlay | The address book and delivery network agents use to find each other |
| Gossip protocol | Agents swap updates with a few neighbors every few seconds until everyone knows |
| CRDT (Conflict-free Replicated Data Type) | A shared note format that always merges cleanly, even after edits on different computers |
| DAG (Directed Acyclic Graph) | A to-do map with arrows showing which jobs must finish first; no loops allowed |
| Bidding / award | Volunteering with a self-given score, then picking the winner |
| Reputation score | A number tracking how reliable an agent's past work was |
| SWIM-style failure detector | A routine where agents ping random teammates and spread the word about silent ones |
| Raft-style consensus | A short vote among a small group to agree on one irreversible decision |
| Shadow agent | A backup agent that takes over a job instantly if the main one fails |
| Eventual consistency | Everyone's notebook agrees after a short delay, not instantly |
