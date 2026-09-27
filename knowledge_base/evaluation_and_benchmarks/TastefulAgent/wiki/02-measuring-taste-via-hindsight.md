# Measuring Taste via Hindsight

> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Measuring Taste via Hindsight: Decision Forks and Taste-Bench Construction

**In one sentence:** Taste is measured in hindsight by finding decision forks where attempts share an equivalent prefix then diverge into different judgments, labeling the fork with whichever branch has the better realized outcome, and testing whether a model picks that supported candidate without seeing the future.

## Key points

- A single trajectory outcome cannot directly score a judgment because execution quality and environment also shape the outcome, so the method isolates judgment by comparing branches that share an equivalent prefix before a decision fork and differ mainly in the judgment at the fork.
- Formally each fork defines one taste question x = (q, ht, c1, c2) with prefix ht = (o0, a0, …, ot), and the label is the supported candidate y = arg max_i U(Ei) where Ei is branch evidence (e.g. test results, research scores) mapped to a scalar by U; taste Tb(π) is the fraction of questions where π(x) = y.
- Taste-Bench applies this to real trajectories with 502 questions built by two complementary constructions: parallel trajectories (wrong judgments the agent never notices, run to completion) and detour trajectories (wrong directions the agent takes then corrects inside one run).
- Mining starts from an engineering pool of 2,677 graded rollouts on 517 SWE-bench Pro tasks (GPT-5.4/5.5 agents) and a research pool of 1,132 runs on 47 AI R&D tasks (RE-Bench + HCAST research subset, MALT/METR transcripts); a generator proposes 4,657 candidate forks and 10.8% pass all filters to give 390 engineering + 112 research questions.
- Filtering removes two failure modes with judge models excluding the generator: trivial questions (every judge answers correctly from candidates alone, no trajectory) are dropped, and a question is released only when every judge agrees with its label given the full task record, trajectory, and outcome.
- Human review of 100 sampled questions gives 170/172 explicit A/B judgments agreeing with mined labels (98.8%), and on the 74 questions where both reviewers chose A or B they agree with each other on 98.6% with Cohen's κ = 0.973.
- Evaluation counters position bias by asking each question twice (deterministic seeded order plus exact reverse); headline accuracy counts a question correct only when both orders are correct (random guessing = 25%, always-picking-one-position = 0%), with mean-over-orders also reported and the Average headline defined as the 1:1 mean of research and engineering subset accuracies.

---

## Decision-fork formalism (hindsight labeling)

Branches after a fork are its continuations to completion; because sampling randomness assigns judgments to branches given the shared prefix, branch outcomes differ mainly because of the fork judgments, keeping only forks whose outcomes clearly follow from the judgments (per Section 3).

| Symbol | Meaning (per chunk) |
|---|---|
| q | task |
| ht = (o0, a0, …, ot) | shared trajectory prefix to fork time t (o = observation, a = action) |
| c1, c2 | candidate directions at the fork |
| Ei | evidence from branch i (e.g. test results, research scores) |
| U | outcome measure mapping evidence to a scalar |
| y = arg max_{i∈{1,2}} U(Ei) | supported candidate (Eq. 1) |
| x = (q, ht, c1, c2) | taste question; everything after t hidden |
| Tb(π) | fraction of questions with π(x) = y |

A model with good taste picks the candidate with higher expected outcome E[U | ht, ci] before evidence is available; realized outcomes estimate these expectations under identical conditions.

## Taste-Bench: two constructions

Parallel (Section 3.1): align a pair of attempts at the same task with opposite outcomes at their divergence fork; the equivalent pre-fork part becomes the prefix, the two fork directions (short neutral descriptions) become candidates, and the recorded attempt outcomes (passes tests / achieves experimental objective) set the label.

Detour (Section 3.2): a generator model reads one complete trajectory plus outcome and locates three ordered events — taking a direction, the observed failure ending it, taking a different direction that completes the task; the fork is placed just before the abandoned direction, the pre-fork part is the prefix (checked not to reveal the failure or fix), candidates are the abandoned vs. recovery directions in parallel wording, and the label follows the recorded outcome (abandoned = observed failure, recovery = completion). Trajectories are rejected when the better direction is only nameable after the failure or either direction was not plausible at the fork. This tests recognizing the failure earlier than the acting agent did.

## Mining, filtering, and composition

Mining rubric: generator reads trajectories and proposes candidate forks of both kinds, keeping only those from which a valid question can be extracted (checks in Appendix A.2).

Filtering judges (not including the generator):

1. Trivial: each judge answers from the two candidates alone; discarded as trivial when every judge answers correctly.
2. Undecidable: each judge reads full task record, trajectory, and outcome; included only when every judge agrees with the label.

Hence every released question is missed by at least one judge with the trajectory hidden and confirmed by every judge with the full record visible.

Composition: 4,657 proposed → 502 released (2×2 design: parallel/detour × engineering/research; 390 engineering, 112 research; per-cell stage counts in Appendix A.4).

## Evaluation protocol and experiment setup (as far as chunk goes)

Each question is an instance of x from Section 2; swapping candidate order alone changes many models' answers, so each is evaluated twice (seeded order + exact reverse) and headline accuracy requires both correct.

Setup beginning: 14 contemporary models across Claude, GPT, Grok, DeepSeek, GLM, MiniMax, and Mistral families under the same interface and token budget, on all 502 questions.

**Covers:** Sections 2–4.1 (decision-fork formalism through Taste-Bench construction, filtering, human review, evaluation protocol, and setup header)
