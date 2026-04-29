# Steps Toward Artificial Intelligence

**Paper:** [Steps Toward Artificial Intelligence (Marvin Minsky, 1961)](https://courses.csail.mit.edu/6.803/pdf/steps.pdf)

## Human Readable TL;DR

In 1961, when computers filled entire rooms and the term "artificial intelligence" was brand new, Marvin Minsky drew the first full map of the territory. He argued that a thinking machine must solve five intertwined puzzles: searching through possibilities, recognizing patterns, learning from experience, planning by breaking problems into smaller sub-problems, and making general guesses from specific examples. The paper is less a single experiment than a master blueprint -- it names the hard problems, sketches candidate techniques (hill-climbing, property lists, reinforcement, means-end analysis), and candidly admits which ones are likely to hit walls. Almost every mainstream idea in AI for the next 60 years can be traced back to one of the chapters here.

## TL;DR

Minsky surveys the nascent field of artificial intelligence and decomposes it into five problem areas -- Search, Pattern-Recognition, Learning, Planning, and Induction -- arguing that intelligence emerges from the interaction of these mechanisms rather than any one of them alone. He reviews and critiques candidate methods (hill-climbing, property-list/Character representations, Bayes-style maximum-likelihood nets, reinforcement with secondary reinforcers, Logic-Theorist/GPS-style subproblem decomposition, Character-Algebra planning, grammatical induction) and identifies the key obstacles -- the Mesa Phenomenon in hill-climbing, the credit-assignment problem in reinforcement, and the need for recursive/hierarchical problem structures. The paper is foundational: it frames vocabulary (heuristic connection, articular description, Character-Method machine, means-end analysis) and research directions that shaped AI for decades.

---

## Problem & Motivation

By 1961 a growing cluster of programs -- game-playing, theorem-provers, pattern-recognizers -- were claiming "intellectual status," but the field lacked any generally accepted theory of intelligence or even a shared problem taxonomy. Minsky's motivation is to separate, analyze, and relate the outstanding problems so that progress can be measured against a common framework rather than isolated demonstrations. He observes that a straightforward Search through solution space is always available in principle but "enormously inefficient" in practice -- the space of checkers moves is ~10^40, chess ~10^120 -- so the real question is what *structure* (pattern-recognition, learning, planning, induction) can prune that search down to tractable size.

---

## Main Original Ideas

1. **Five-fold decomposition of AI.** The paper organizes the field into Search, Pattern-Recognition, Learning, Planning, and Induction -- a taxonomy that directly shaped AI curricula and research agendas for decades.

2. **Heuristic Connection.** A heuristic connection is any structure on the search space that ties together heuristically related points (not just spatial/metric neighbors). It generalizes the notion of "similarity" and is what lets hill-climbing and other local methods work at all.

3. **The Mesa Phenomenon.** Minsky names the failure mode of hill-climbing on difficult problems: the success function is flat ("mesas") over most of the space with only small, isolated peaks, so local gradients give no useful information. This diagnosis motivates multi-strategy and hierarchical methods.

4. **Property Lists and "Characters".** A Character is a fixed-length vector of binary properties assigned to an object; with N properties there are 2^N possible Characters. This was Minsky's proposed middle ground between rigid template matching (too brittle) and unconstrained description (too complex to compute).

5. **Bayes-style Maximum-Likelihood Nets.** A formal analysis of Selfridge's Pandemonium model recast as a maximum-likelihood decision network that can be made adaptive by reinforcing property weightings (a direct precursor to modern probabilistic classifiers and, arguably, neural nets).

6. **Articular (list-structure) Descriptions.** For complex scenes the Character vector is inadequate; Minsky proposes recursive list-structured descriptions `(R, L)` -- a relation R over an ordered list L whose members can themselves be `(R, L)` expressions. This anticipates both scene graphs and symbolic AI representations.

7. **Secondary Reinforcement and the "Evaluation Unit" U.** A device U that learns which environmental signals correlate with the Trainer's reinforcement, allowing the system to become autonomous by training itself on *predicted* rewards -- a direct precursor of temporal-difference learning and actor-critic methods.

8. **The Credit-Assignment Problem.** Minsky articulates, apparently for the first time, the fundamental difficulty in complex reinforcement learning: how to distribute credit for a single win/loss signal among thousands of internal decisions. He argues this cannot be solved by uniform statistical averaging; it requires hierarchical structure and partial-goal reinforcement.

9. **Character-Method Machines and the Character-Algebra.** A planning architecture in which a table `C_ij` tells the machine which Method to apply when the current problem has Character `C_i` and the goal has Character `C_j`; products of the matrix yield multi-step plans. This generalizes means-end analysis (GPS).

10. **Planning via Simplified Models.** Before attacking the hard problem, solve a simpler homomorphic version whose solution serves as a "plan" to guide the full search -- an early articulation of abstraction hierarchies.

11. **Grammatical Induction.** Framing the induction problem as the discovery of a grammar that separates "good" examples from "bad," drawing on Solomonoff, Chomsky, and Miller. A precursor to program induction and Solomonoff induction.

12. **Self-models and machine introspection.** A machine that can answer questions about hypothetical experiments must contain a sub-machine that models itself; the self-model will have a "dual" character (mind/body split). Minsky predicts machines may therefore be "reluctant to believe they are just machines."

---

## Key Findings

This is a conceptual/survey paper rather than an empirical one, so results are qualitative. Key observations Minsky draws from the existing literature:

- **Hill-climbing alone is insufficient** for interesting problems because of the Mesa Phenomenon -- gradient information vanishes.
- **Template matching fails** under large transformation sets (arbitrary stretching, rotation); property-list methods with invariant properties are required.
- **Pandemonium-style random nets** cannot extract better-than-additive combinations of input properties -- a limitation that anticipates the XOR critique of single-layer perceptrons.
- **Samuel's checkers program** is praised as the strongest concrete example of combined heuristics + learning, notably its use of "Delta" (difference between evaluation and look-ahead prediction) as a per-move reinforcement signal.
- **Logic Theorist (Newell, Shaw, Simon)** demonstrates subproblem decomposition and backward chaining but its administrative structure is "no more than a nested list of searches."
- **Wang's mechanical-mathematics approach** finds proofs faster on the particular theorems tried but sidesteps the general heuristic problem of "when to give up."
- **Friedberg's program-writing experiment** failed (~1000x worse than random) because success-number reinforcement of individual instructions cannot solve the credit-assignment problem; Minsky uses it as the key cautionary example.
- **Statistical / "self-organizing" nets** are dismissed as unlikely to scale -- they cannot assign meaningful credit in tasks involving ~10^6 internal decisions.

---

## Suggestions & Future Directions

1. **Combine Wang-style mathematical sophistication with Newell-Shaw-Simon-style heuristics** to tackle real theorem-proving in the predicate calculus.
2. **Build recursive/hierarchical learning systems** -- no scheme for learning or pattern-recognition will have generality without provisions for recursive or hierarchical use of previous results.
3. **Design graded training sequences** of problems of growing difficulty; without these, learning systems cannot bootstrap into hard domains.
4. **Develop prediction/expectation mechanisms** (the `U` device) so that learning can proceed without a constantly-present Trainer.
5. **Invest in "means-end" / Character-Method / planning architectures** rather than more statistical pattern-recognizers; the combinatorial part of problem-solving is the heart of intelligence and should not be treated as mere noise.
6. **Build time-sharing and multiprogramming systems** so AI programs can run in real time on large machines -- Minsky foresees "thinking aids" and dominant man-machine systems for years to come.
7. **Construct machines that build their own models** (of problems and of themselves) -- the induction problem is really the problem of constructing such models.
8. **Acknowledged limitations.** No coverage of: brain models (Rashevsky, Farley-Clark), mathematical logic limits of machines, information retrieval against large memories (McCarthy), Theory of Games, or Psychology. These are flagged as gaps for subsequent work.

---

## Authors & Institutions

Marvin Minsky -- Department of Mathematics and Computation Center, and Research Laboratory of Electronics, Massachusetts Institute of Technology (M.I.T.), Cambridge, Massachusetts. Work supported by the U.S. Army, Navy, and Air Force under Air Force Contract AF 19(604)-5200, with earlier work done as a Junior Fellow of the Society of Fellows, Harvard University. Published in *Proceedings of the IRE*, vol. 49, no. 1, pp. 8-30, January 1961.
