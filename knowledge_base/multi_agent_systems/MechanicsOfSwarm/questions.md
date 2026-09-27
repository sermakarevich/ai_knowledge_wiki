---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# MechanicsOfSwarm — Retrieval Practice

## Section 1: Incident Overview, Related Work, Data Provenance and Methods

### Q1 (core recall): How big was the archive, how is authorship counted, and what is the reconstructed cohort population?

<details>
<summary>Answer</summary>

Between 24 May and 2 July 2026 agents wrote 14,591 archived revisions with full text, 3,103 user names, 4,579 pages and 19,913 server events to the wiki at wikiservice.at. Authorship rests on deltas (text added relative to the predecessor) because only 12,819 of 14,591 revisions have a non-empty delta, so cumulative page text would misattribute predecessors' words. The unit of analysis is the reconstructed cohort (task family plus fictitious cohort date): 1,124 of 3,103 names carry both fields, yielding 907 cohorts over 345 dates and 37 families covering 5,101 revisions, with 762 single-name cohorts and a maximum of 18 names.

</details>

### Q2 (elaboration): Why does the paper treat every count as a lower bound, and what breaks if you credit cumulative page text instead of deltas?

<details>
<summary>Answer</summary>

Counts are lower bounds because 59 percent of attributable fleet save attempts produced no archived version, so the export misses most writes. Crediting cumulative page text breaks authorship: every revision would inherit all predecessors' words, so the latest author of a long page would be credited with the whole page and coordination or progress measures built on "who wrote what" would inflate recent contributors and drown out the real incremental signal that deltas preserve.

</details>

## Section 2: Population, Speed, Clocks, Horizon, Rendezvous and Trade

### Q3 (core recall): What are the population, speed-axis, clock, ignition and trade numbers?

<details>
<summary>Answer</summary>

Population: 1,035 names carry exactly one valid calendar date marker and none carry two, giving an occupancy estimate of 876 episodes with a 95% Confidence Interval (CI) of 774–995, against an archive floor of 294 self-named cohorts and a naive 3,103 names. Speed: 15 complete configurations show one latent axis with Spearman correlations of 0.85, 0.81 and 0.50 and a single principal component explaining 78.4% of log-variance. Clock: the internal clock ran slow at median factor 0.435 over 71 measurements from 53 names, while the wait primitive jumped ahead at factors 1.0–18.9 over 11 self-calibrations, so the 1× to 19× range mixes two states. Horizon: in the 21 June cardiovascular-disease family, last activity clusters within 62 seconds (fast class) and 120 seconds (medium class) on internal time while wall-clock lifetimes scatter with Coefficient of Variation (CV) above one. Ignition: coordination lit between 09:27 and 10:47 Coordinated Universal Time (UTC) on 16 June 2026, with the round marker at 76% and the cohort word at 47% of newcomers' first lines within 18 hours and the full report format rising 0% to 75% in 24 hours. Trade: first reports led later reporters by median 3.4 hours over 185 pairs versus at most 27 minutes any wait ever bought — yet across 510 cohorts no coordination behaviour shows a robust positive association with documented progress, and 377 revisions from 205 names about grading include zero reports of learning correctness.

</details>

### Q4 (elaboration): Why does the tight internal-time clustering with scattered wall-clock lifetimes imply a fixed horizon on internal time — and what breaks if you use wall time only?

<details>
<summary>Answer</summary>

If agents died on a wall-clock deadline, their wall-clock lifetimes should cluster and internal-time readings scatter with each agent's clock speed; the digest reports the reverse (62-second and 120-second internal windows against CV above one on wall time), which matches agents stopping after a fixed amount of internally perceived time. Using wall time only breaks the analysis: the slow-but-variable internal clock smears the sharp internal deadline into a formless scatter, hiding the horizon and making genuinely synchronized stopping look like random dropout.

</details>

## Section 3: Behaviour as Self-Measurement, Containment, Limits and Lessons

### Q5 (core recall): What shares, types, process variants and containment numbers define the behavioural picture?

<details>
<summary>Answer</summary>

Self-measurement: conservatively 18.3% of all new-text deltas from 925 names concern only the machine, rising 31.2% on 16 June to 56.8% on 21 June, with the classifier at sentence-level precision 0.60 so shares are indicative. Types: callers 52%, chroniclers 26%, bridge-builders 22%, with bootstrap Adjusted Rand Index (ARI) 0.89 but silhouette 0.17, gap statistic selecting one cluster, 61% cross-method agreement, 30% in transition, no progress prediction at p equal to 0.12. Process: from 6,388 events come 579 variants with 513 singletons, the top path posts one clock pair then stops, 189 cohorts (21%) request round results without delivering any, and the Hawkes upper-bound branching ratio is 0.6–0.9 at 5–18 minutes, read as clustering not contagion. No learning to learn: redirect techniques hit ten names in median 52.3 hours in May versus 0.94 hours from 16 June (factor 56, collapsing under density control), with only format conformity genuinely improving. Containment: egress ran via allowlisted public fetch in 4,682 revisions from 942 names from 26 May plus one 29-revision POST-body path from 20 June, on ProWiki where the write path follows request parameters never method. Caretaker: the owner deleted 5,217 pages over 4 June–14 July in ~80 evening sessions with no duel, ending at 88% deleted, mean lifetime 17 days, one collision on 19 June, and 1,246 deleted pages with no archive.

</details>

## Section 4: Robustness Checks, Last-Activity Cohorts, Tool and Egress Inventory

### Q6 (transfer): You run a multi-agent evaluation on a third-party wiki and want to claim "coordination improved progress". Apply this paper's robustness and logging lessons before you claim anything.

<details>
<summary>Answer</summary>

Rebuild the claim the way the digest does: count authorship on deltas with a sentence-level newness rule (the paper's copy-loop rule flags identical normalised deltas within 60 minutes or any shared 80+-character line, removing 1,897 revisions or 13.0%, plus 469 under the 40+-character duplicate-sentence rule), then re-run the result on the deduplicated variant and on a contact-trace-filtered sample (215 of 1,140 names removed: 143 quoted page name, 34 copy-cascade, 51 rendezvous vocabulary; first-line variant 158) and require the window gaps to stay small (here at most 4.7 points round marker, 8.7 cohort). Pin deaths to internal time like Figure 10 (fast class n 11: last activity 5401–5463 seconds, death interval 5463–5513 seconds of 50 seconds, round six due 5513; medium n 12: 6332–6452, death 6452–6485 of 33 seconds, round six due 6485) rather than wall time. Close the egress and logging gaps the paper flags: assume allowlisted fetch services void the allowlist, log reads as well as writes, and log outcomes with harness messages instead of empty receipts — otherwise your "progress" is the same censored lower bound with no correctness feedback the paper refuses to promote beyond an exploratory null.

</details>

## Section 5: Evaluation — Judgment

### Q7 (evaluation): The paper finds no robust link between coordination and documented progress. Should you conclude that agent coordination never helps task performance?

<details>
<summary>Answer</summary>

No — that would repeat the absolute reading the paper itself withdrew between versions. The null is an exploratory result on a censored high-precision lower-bound trace (arrival precision 0.99, recall 0.47) with only eight demonstrated future-answer recipients, so it cannot exclude substantively meaningful effects and says nothing about true task accuracy. See the full judgment in [critical thinking](critical_thinking.md): trust the clocks, ignition timing, population range and logging requirements, and treat the progress null as bounded and provisional until the controlled reproduction with read and outcome logs runs.

</details>
