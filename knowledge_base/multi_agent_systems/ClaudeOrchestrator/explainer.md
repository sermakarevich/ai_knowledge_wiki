> [[index|Wiki]] | [[summary|Summary]]

# Claude-Orchestrator Skill + Orchestration-Playbook Core — In Plain Language

## What is this about?

Imagine hiring a crew of fast but overconfident builders (AI coding helpers — programs that write software from your instructions). Each one works quickly, but sometimes says "finished!" when the work was never saved, or paints the wrong house, or shows you a photo of a different house as proof yours is done.

This system is a rulebook for managing that crew. One boss (the orchestrator — the main AI that hands out work and checks it) breaks a big job into small written work orders (task contracts — forms describing exactly what to do and how to prove it), sends each worker to their own separate copy of the construction site (an isolated worktree — a separate folder copy of the code where one worker builds without disturbing others), checks every finished piece personally, combines the good pieces, and then brings in an outside inspector from a different company (cross-model review — a second AI from a different maker double-checking the work) to catch mistakes everyone else missed.

## Why does it matter?

When AI writes code fast, the hard part is no longer writing — it is trusting. Workers forget to save their work, wander into files they were told to avoid, or claim "tests pass" without running them. Without discipline, a team of agents produces a pile of half-done, overlapping, unverified changes.

This rulebook exists because those failures actually happened in big real runs (dozens of batches — rounds of parallel work — and tens of thousands of lines of code), and each rule was written only after a real incident proved it was needed.

## How does it work?

Step-by-step in plain terms, using a restaurant kitchen analogy:

1. **Morning prep (recon).** The head chef checks what is cooking, what is left over, and what orders came in — the boss agent checks the code state and the to-do docs.
2. **Write the tickets (contracts).** Every dish gets a written ticket: what "done" looks like, which station may touch it, which cooking checks must pass, and what proof is required. No ticket, no cooking.
3. **Cook in separate stations (dispatch).** Each cook works at their own counter (worktree) on their own copy of the recipe (branch — a separate line of work), so nobody knocks over anyone else's pots.
4. **Taste everything yourself (accept).** The head chef does not trust "I cooked it" — they check the plate exists, taste it, and re-run the checks personally.
5. **Plate and clean (merge).** Only the head chef combines dishes, sends them out, and cleans the stations.
6. **Outside food critic (review).** After each round, an inspector from a different restaurant group tastes everything and files a report; ignored warnings get louder each round until the kitchen stops.

## Where can this be used?

- **Running several coding helpers at once** without them overwriting each other's work.
- **Any team review process:** written work orders, honest evidence labels, and independent re-checks work for humans too.
- **Outside software:** the same pattern fits any crew of fast workers whose claims need verification — label every claim by how it was proven, never inflate the label, and have someone outside the team double-check.
- **Fleet (this team's own agent manager):** the seven borrowable ideas in [[wiki/05-cross-model-review-fleet-lessons|Cross-Model Review and Fleet Lessons]] — evidence labels, numbered failure names, work-order checklists, and enforced outside review.

## Conclusions & takeaways

What to remember a month from now: trust is a procedure, not a feeling. Write down what "done" means before work starts, check it yourself after, label proof honestly, get an outsider to look, and delete any rule that never catches a real mistake. Honest limitations: the big success numbers come without full data or error rates, several thresholds are rough guesses, and the whole flow assumes you are always allowed to publish to the main code line.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Orchestrator | The boss agent that hands out work, checks it, and combines results |
| Task (dispatch) contract | A written work order: what to do, what not to touch, how to prove it |
| Worktree | A separate working copy of the code where one agent builds in isolation |
| Branch | A named separate line of work that later gets combined into the main line |
| Evidence label (direct/proxy/local/blocked) | How a claim was proven: in the real setting, via a substitute, only on the worker's machine, or not provable yet |
| Acceptance gate | A concrete check (usually a command) that must pass before work counts as done |
| Cross-model review | A second AI from a different maker double-checking finished work |
| ORC anti-pattern | A numbered, named common failure (e.g. claiming work is saved when it is not) |
| P1 / P2 finding | A review problem: fix now (P1) vs record and fix later (P2) |
| Batch Status Report | The end-of-round summary: what shipped, what failed, what is next |
