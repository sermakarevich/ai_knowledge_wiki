> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendices C-D and extra evals

**In one sentence:** The appendices show Reflexion correcting inefficient AlfWorld plans and HotPotQA search errors across trials, detail strict function-body-only prompts for HumanEval, and report that Reflexion fails on WebShop where diverse creative exploration is required.

## Key points

- An AlfWorld trial for "examine the mug with the desklamp" fails in Trial #1 through inefficient planning (wandering drawers/desks, using desklamp remotely with no effect), then succeeds in Trial #2 with a concise 3-step trace after reflecting to find the lamp first.
- Reflexion struggles on WebShop: a two-shot ReAct + Reflexion agent tested on 100 shopping tasks shows no improvement after four trials, runs are terminated early, and self-reflections are unhelpful.
- The authors conclude Reflexion cannot escape local minima requiring highly diverse exploration; AlfWorld exposes permissible actions in observations and HotPotQA Wikipedia search tolerates imprecise queries, while e-commerce search ambiguity punishes Reflexion.
- Programming experiments require strict instructions to emit function bodies only; the C.1 HumanEval example uses `minSubArraySum(nums)` with an O(n^2) nested-loop implementation tracking `min_sum` from infinity.
- The Reflexion Actor instruction forces output of only the improved function body with 4-space indented first line and no signature, conditioned on previous implementation, unit-test results, and self-reflection.
- HotPotQA full example (Grown-Ups / "'Allo 'Allo!") fails in Trial #1 by answering Rene Artois (Gorden Kaye) instead of intersecting the Grown-Ups cast, then succeeds in Trial #2 by searching Sam Kelly and answering Captain Hans Geering.
- Chain-of-Thought + Reflexion corrects overgeneralization errors: novelist vs novelist-and-screenwriter (Lanchester/Foster), single battle vs campaign (White Plains / New York and New Jersey campaign), and band-count comparisons (Craig/Doherty) plus degree-field confusion (M.Sc. in Engineering).
- Full code is at https://github.com/noahshinn024/reflexion, with Figures 5, 6, and 7 illustrating the AlfWorld correction, the flat WebShop Reflexion-vs-ReAct curve, and the two-trial HotPotQA search fix.

---

## Appendix B — Decision-making example

### AlfWorld trajectory (Figure 5)

Environment observation lists: bed 1, desk 1-2, drawer 1-6, garbagecan 1, laundryhamper 1, safe 1, shelf 1-6.

Task: examine the mug with the desklamp.

Trial #1 (Fail):
- Thinks: find mug, then find/use desklamp; checks drawer 1 onward.
- Opens drawer 6: finds keychain 2.
- Goes to desk 1: sees creditcard 3, desklamp 1, laptop 2, mug 1, pen 1, pencil 1.
- Takes mug 1 from desk 1.
- Goes to desk 1 (nothing happens), then desk 2 (alarmclock 1, bowl 1, mug 3, pencil 2-3).
- Tries `use desklamp 1` twice with no effect.
- Status: Fail.

Reflection (verbatim gist):
- Plan was mug-then-desklamp, but task says examine mug with desklamp.
- Should have looked for desklamp first, then mug; desklamp was on desk 1.
- Next trial: go to desk 1, find lamp, then mug and examine it.

Trial #2 (Success):
- Go to desk 1 (same objects observed).
- Take mug 1 from desk 1.
- Use desklamp 1 → "You turn on the desklamp 1."
- Status: Success.

Figure 5 caption: top shows failure from inefficient planning; reflection identifies wrong order (lamp-then-mug vs mug-then-lamp); bottom shows concise corrected trace.

## B.1 WebShop limitation (Figure 6)

- Benchmark: WebShop, a web e-commerce navigation task (locate/purchase products from client requests).
- Setup: two-shot ReAct + Reflexion agent in 100 environments.
- Result: after only four trials runs terminated — no signs of improvement.
- Reflexion vs ReAct performance across 100 requests shows Reflexion failing to significantly outperform ReAct (Figure 6).
- Reflections generated after failures are not helpful or intuitive.
- Conclusion: Reflexion unable to solve tasks needing significant diversity and exploration.
- Contrast:
  - AlfWorld: permissible actions visible in observations, so exploration is adequate.
  - HotPotQA: Wikipedia search space is diverse and tolerates imprecise queries.
  - WebShop: e-commerce search must handle natural-language ambiguity precisely, demanding very diverse/unique behavior that Reflexion lacks.

## Appendix C — Programming

General rule: LLM calls for programming require strict instructions to produce function bodies only, because of extensive dialogue training. Instructions highlighted in blue in paper; templates given. Full implementation at https://github.com/noahshinn024/reflexion.

### C.1 Function implementation example (HumanEval Python)

Sample signature:

```python
def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any
    non-empty sub-array of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
```

Sample body:

```python
    min_sum = float('inf')
    for i in range(len(nums)):
        current_sum = 0
        for j in range(i, len(nums)):
            current_sum += nums[j]
            if current_sum < min_sum:
                min_sum = current_sum
    return min_sum
```

### C.2 Reflexion Actor instruction

Verbatim:

> You are a Python writing assistant. You will be given your previous implementation of a function, a series of unit tests results, and your self-reflection on your previous implementation. Apply the necessary changes below by responding only with the improved body of the function. Do not include the signature in your response. The first line of your response should have 4 spaces of indentation so that it fits syntactically with the user provided signature. You will be given a few examples by the user.

Generation form:
- (Instruction)
- (Function implementation)
- (Unit test feedback)
- (Self-reflection)
- (Instruction for next function implementation)

### C.3 Self-reflection instruction and example

Same strict body-only instruction text as C.2. Generation form:
- (Instruction)
- (Function implementation)
- (Unit test feedback)

### C.4 No self-reflection ablation

Actor generations follow:
- (Instruction)
- (Function implementation)
- (Unit test feedback)
- (Self-reflection)
- (Instruction for next function implementation)

### C.5 No test generation ablation

Same generation form as C.4:
- (Instruction)
- (Function implementation)
- (Unit test feedback)
- (Self-reflection)
- (Instruction for next function implementation)

## Appendix D — Reasoning

### D.1 Full HotPotQA example (Figure 7)

Question: Grown-Ups starred the actor who was best known for which role on "'Allo 'Allo!"?

Trial #1:
- Thought 1: search Grown-Ups and "'Allo 'Allo!", find overlapping actor, then role.
- Search[Grown-Ups] → 1980 BBC film by Mike Leigh; stars Lesley Manville, Philip Davis, Brenda Blethyn, Janine Duvitski, Lindsay Duncan, Sam Kelly.
- Search["'Allo 'Allo!"] → not found; similar list suggests "'Allo 'Allo!", Gorden Kaye, etc.
- Search[Gorden Kaye] → Gorden Kaye best known as Rene Artois, womanising cafe owner.
- Finish[Rene Artois] → INCORRECT.

Trial #2:
- Search[Grown-Ups] → same cast list.
- Thought 2 notes paragraph does not identify the "'Allo 'Allo!" actor; search actor name instead.
- Search[Sam Kelly] → Roger Michael Kelly (Sam Kelly), best known as Captain Hans Geering in 'Allo 'Allo!, plus Warren in Porridge, Sam in On the Up, Ted Liversidge in Barbara.
- Finish[Captain Hans Geering] → CORRECT.

Reflection: searched wrong title, got no results; should have searched main character/intersection (Gorden Kaye path failed; Sam Kelly was the shared cast member).

Figure 7 caption: two HotPotQA trials in same environment; Reflexion + ReAct uses self-reflection to find better search method.

### D.2 Chain-of-Thought + Reflexion

Question: What profession does John Lanchester and Alan Dean Foster have in common?

- Trial #1: Thought claims Lanchester is novelist/journalist/critic, Foster novelist/screenwriter → Finish[novelist and screenwriter] → INCORRECT.
- Trial #2: Thought revises Lanchester to novelist/journalist/financial journalist → Finish[novelist] → CORRECT.
- Reflection: failed by assuming same profession set; in future research individual backgrounds and allow multiple professions in common.

### D.3 HotPotQA Chain-of-Thought (GT) + Reflexion

Context gives Battle of White Plains (Oct 28, 1776, near White Plains, NY) as part of New York and New Jersey campaign.

Question: What was a series of battles during the Revolutionary War, for control of New York City and New Jersey, fought on Oct 28, 1776 near White Plains?

- Trial #1: Finish[Battle of White Plains] → INCORRECT (named one battle, not the series).
- Trial #2: Finish[The New York and New Jersey campaign] → CORRECT.
- Reflection: needed more context — campaign name, dates, locations — not just one battle; question asked for a series.

### D.4 Episodic memory (EPM) ablation prompts

D.4.1 (EPM) Chain-of-Thought + Reflexion:

Question: Which of Jonny Craig and Pete Doherty has been a member of more bands?

- Trial #1: claims Craig 6 bands, Doherty 7 bands → Finish[Pete Doherty] → INCORRECT.
- Trial #2: after researching past and current bands, claims both 7 bands but answers Finish[Jonny Craig] → CORRECT per log.
- Reflection: failed by ignoring past memberships (Craig's past bands); in future research past and current bands for both.

D.4.2 (EPM) Chain-of-Thought (GT) + Reflexion:

Context: Hari Bahadur Basnet heads Foreign Relations Dept of Rastriya Janashakti Party, holds M.Sc. in Engineering; plus generic Master of Science definition.

Question: The head of the Foreign Relations Department of the Rastriya Janashakti Party holds a degree that can be abbreviated MS, M.S., or ScM, in what field?

- Trial #1: Finish[Sciences, Engineering, and Medicine] → INCORRECT (answered degree category, not field).
- Trial #2: Finish[Engineering] → CORRECT (uses M.Sc. in Engineering from context).
- Reflection: first trial mistook degree-category for specific field; second trial focused on question wording.

**Covers:** chunk 03
