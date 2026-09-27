---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# React — Retrieval Practice

## Section 1: ReAct method: reason+act interleaving

### Q1 (core recall): What is the ReAct action-space expansion, and what headline gains did it report on ALFWorld and WebShop?

<details>
<summary>Answer</summary>

ReAct expands the action space to Â = A ∪ L, where thoughts (L) update context with no environment effect and task actions (A) return observations. Headline results with PaLM-540B and 1–6 in-context examples: +34% absolute on ALFWorld and +10% absolute on WebShop over imitation/RL baselines trained on 10^3–10^5 instances; HotpotQA/FEVER competitive with CoT but more grounded via the Wikipedia API.

</details>

### Q2 (elaboration): Why does interleaving reasoning with acting fix both CoT hallucination and Act-only myopia — what breaks if you use only one side?

<details>
<summary>Answer</summary>

CoT alone is a static black box: it reasons from parametric memory with no live observations, so errors propagate and facts are hallucinated. Act alone predicts actions from language priors with no abstract plan or working memory, so it cannot track progress or recover from exceptions. ReAct fixes both via reason-to-act (plan, track, adjust) and act-to-reason (fetch external facts into context). Remove reasoning and the agent goes myopic; remove acting and it hallucinates.

</details>

## Section 2: Knowledge-intensive and decision-making experiments

### Q3 (core recall): What GPT-3 vs PaLM-540B numbers show ReAct generalizes across models, and what finetuning step counts were used?

<details>
<summary>Answer</summary>

GPT-3 text-davinci-002 with greedy decoding beat PaLM-540B under ReAct: 30.8 vs 29.4 exact match on HotpotQA (500-question validation subset) and 78.4% vs 70.9% success on ALFWorld (all 134 unseen validation instances). Finetuning used batch size 64 everywhere; on PaLM-8B ReAct/Act trained 4,000 steps vs Standard/CoT 2,000 steps, and on PaLM-62B ReAct/Act trained 4,000 steps vs Standard/CoT 1,000 steps, because ReAct/Act keep improving while Standard/CoT degrade soon after finetuning starts.

</details>

### Q4 (elaboration): Why does ReAct answer up-to-date questions (e.g. the hotel-size question) correctly where Standard, CoT, and even Act fail — and what does the thought-editing rescue prove?

<details>
<summary>Answer</summary>

Only ReAct combines reasoning to guide interaction with live retrieval: Standard/CoT answer from frozen parametric memory so they miss facts that changed after training, and Act has web access but no reasoning to direct the search. The ALFWorld rescue — deleting one hallucinating sentence (Act 17) and adding hints (Act 23) — proves thoughts causally steer beliefs and downstream actions: a two-thought edit replaced tens of manual actions.

</details>

## Section 3: Appendices: prompts, trajectories, analysis

### Q5 (core recall): Contrast ReAct vs baselines on the three appendix trajectories using their exact numbers and names.

<details>
<summary>Answer</summary>

FEVER 2491 (Bermuda Triangle, REFUTES): ReAct searches, observes "western part of the North Atlantic Ocean", finishes REFUTES; CoT answers from memory with no search. FEVER 1951 (Soyuz, REFUTES): ReAct searches "Soyuz" and "American space program", finds no link, answers NOT ENOUGH INFO; CoT hallucinates collaboration and says SUPPORTS. Clean-knife ALFWorld task: ReAct decomposes find-take-clean-put, finds knife 1 on countertop 2, cleans at sinkbasin 1, puts on countertop 1; Act issues `clean knife 1 with sinkbasin 1` before navigating and loops "Nothing happens". WebShop banana chips under $50: Act buys B0061IVFZE (strawberry banana, 100-pack, $85.0) for score 0.125; ReAct picks B092JLLYK6 with `apple cinnamon` + `0.53 ounce (pack of 16)` for score 1.0.

</details>

### Q6 (transfer): You are building a shopping assistant that keeps buying the wrong variant (wrong scent/size). How would you apply the ReAct appendix lessons to fix it?

<details>
<summary>Answer</summary>

Apply the WebShop lesson: force an explicit reason-over-options step before clicking — enumerate all results, compare attributes against the request (scent, pack size, price cap), then select. Add ReAct-style subgoal tracking (find → compare → select options → buy) instead of Act-style first-result clicking or ReAct-IM vague thoughts ("find and take"), which the knife trajectory shows leads to skipped steps and "Nothing happens" loops. Log thoughts so a human can edit one bad belief instead of re-running the whole trajectory.

</details>

## Section 4: Evaluation ([[critical_thinking|Critical Analysis]])

### Q7 (evaluation): The paper reports ReAct is "competitive with CoT" on HotpotQA/FEVER rather than clearly beating it, while claiming clear wins on ALFWorld/WebShop. Why is the QA claim weaker evidence than the decision-making claim, and what would you need to see to trust "competitive" as a real result rather than a soft landing?

<details>
<summary>Answer</summary>

The decision-making wins (+34% ALFWorld, +10% WebShop) are head-to-head success-rate deltas against different systems (imitation/RL baselines) on the same task, with full trajectories shown as mechanism. The QA "competitive" claim is weaker because the paper's own best QA result comes from a ReAct+CoT hybrid, not ReAct alone — meaning the headline masks that plain ReAct sometimes ties or loses to CoT on raw exact-match, and grounding (fewer hallucinations) is being substituted for a clear accuracy win. To trust "competitive" as a real result you'd want: ReAct-alone vs CoT-alone exact-match with variance across multiple example sets, not just the hybrid's number, plus a breakdown of how often grounding fixes an answer CoT would have hallucinated versus how often it fixes nothing.

</details>
