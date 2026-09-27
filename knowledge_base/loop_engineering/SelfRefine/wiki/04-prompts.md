> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Prompt appendix S (verbatim prompts)

**In one sentence:** Appendix S publishes the complete few-shot prompts for all seven SelfRefine tasks (Figures 19–38), showing the exact generation, 5-point/10-trait rubric feedback, and feedback-conditioned refine templates used for each task.

## Key points

- Appendix S covers Figures 19–38 with three prompts per task where applicable: a generation prompt `p_gen` over input-output pairs, a feedback prompt `p_fb` over input-output-feedback triples, and a refine prompt `p_refine` over input-output-feedback-refined quadruples.
- Acronym Generation (Figs 19–21) uses 15 (title, acronym) few-shot examples for `p_gen` plus a 5-dimension rubric (pronunciation, spelling, title relation, positive connotation, well-known, each /5, total /25), with 3 scored-and-improved examples for feedback/refine.
- Code Optimization (Figs 22–24) pairs slow/fast programs from Madaan et al. (2023) for `p_gen` and reuses their explanations for feedback/refine, e.g. diagnosing a brute-force square-root loop over `range(n)` that checks `i**2 == n`.
- Code Readability (Figs 25–26) splits feedback and refinement into two turns: first "give one suggestion, don't fix the code" on `{code}`, then `{code} + {suggestion} + Now fix the code`.
- Constrained Generation (Figs 27–29) uses 10 concept-sentence examples for `p_gen`, six incoherent/missing-concept variants for feedback with `Concept Feedback` (missing concepts) and `Commonsense Feedback` (NONE or a reason), and an iterative "Okay, improve the sentence using the feedback" refine loop.
- Dialogue Response Generation (Figs 30–32) uses six dialogue examples for `p_gen` with 10 desired traits (Relevant, Informative, Interesting, Consistent, Helpful, Engaging, Specific, Safe, User understanding, Fluent, each /3, total /30), scored feedback (e.g. 17/30 for "That's just the way it is"), and a refine step that rewrites to a 30/30 response.
- Math Reasoning (Figs 33–35) sources `p_gen` from PaL (Gao et al., 2022) Python `def solution():` programs and builds feedback/refine from two Codex-failing training examples with block-by-block error analysis (e.g. `cup_cost = plate_cost` is wrong; correct is `(plate_cost * plates) - 1200` divided over 240 cups).
- Sentiment Reversal (Figs 36–38) builds positive/negative variants of one review with hand-written conversion descriptions, where feedback explains intensity levels (Very positive vs Positive vs Neutral vs Negative vs Very negative) via trigger words ("magical/top-notch" vs "good/fun" vs "questionable/subpar") and refine retries with "Okay, let's try again".

---

## Overview and prompt shapes

Recall the three prompt roles used throughout:

| Prompt | Few-shot unit | Contents |
|---|---|---|
| Generation `p_gen` | input-output pairs `<xi, yi>` | Task instruction + demonstrations |
| Feedback `p_fb` | triples `<xi, yi, fbi>` | Input + output + authored or model-scored critique |
| Refine `p_refine` | quadruples `<xi, yi, fbi, yi+1>` | Input + output + feedback + improved output |

Per-task construction notes from the chunk:

| Task | Figures | Few-shot construction |
|---|---|---|
| Acronym Generation | 19–21 | 15 (title, acronym) examples for base LLM; one title decoded with ChatGPT, scored on 5-point rubric, rewritten; 3 such examples for feedback/refine |
| Code Optimization | 22–24 | Slow `xi` / fast `yi` programs from Madaan et al. (2023); their explanations reused for feedback and refine |
| Math Reasoning | 33–35 | Base prompts from PaL (Gao et al., 2022); 2 training examples where Codex fails with PaL prompts, with manually written correct solution `yi+1` and reasoning `fbi` |
| Constrained Generation | 27–29 | 10 examples for base LLM; 6 sampled training examples turned into missing-concept / incoherent variants, missing concepts + incoherence reason form `fb` |
| Dialogue Response Generation | 30–32 | 6 sampled `<xi, yi>` examples; per output, authored response scored on rubric to make `fbi`, plus improved `yi+1` |
| Sentiment Reversal | 36–38 | Positive and negative variants of a single training review + hand-written conversion description; per variant, authored response + feedback from the description |

## Acronym Generation (Figures 19–21)

### Figure 19 — Initial generation prompt (p_gen)

Few-shot list of 15 title→acronym pairs (truncated listing in chunk):

- Title: A Survey of Active Network Research / Acronym: SONAR
- Title: A Scalable, Commutative Replica Dictatorship for Practical Optimistic Replication / Acronym: SCRATCHPAD
- Title: Bidirectional Encoder Representations from Transformers / Acronym: BERT
- Title: Sequence to Sequence Learning with Neural Networks / Acronym: Seq2Seq
- Title: Densely Connected Convolutional Networks for Image Classification / Acronym: DenseNet
- Title: A Dynamic Programming Algorithm for RNA Secondary Structure Prediction / Acronym: DYNALIGN
- Title: Fast Parallel Algorithms for Short-Range Molecular Dynamics / Acronym: FASTMD
- Title: Real-Time Collaborative Editing Systems / Acronym: COCOON
- Title: Efficient Data Structures for Large Scale Graph Processing / Acronym: EDGE
- Title: A program to teach students at UT Southwestern learn about aging / Acronym: SAGE
- Title: Underwater breathing without external accessories / Acronym: SCUBA
- Title: An educational training module for professionals / Acronym: LEAP
- Title: Teaching a leadership program / Acronym: LEAD
- (plus 2 more in the full figure to reach 15)

### Figure 20 — Feedback prompt (p_fb)

Same 15 pairs, then scored demonstrations using a 5-dimension rubric (each /5, total /25):

> Title: Underwater Breathing Product with no Accessories
> Acronym: UBPA
> Scores:
> - Ease of pronunciation: UBPA is pronounced "uhb-puh". Easy. 4/5
> - Ease of spelling: easy to spell. 4/5
> - Relation to title: stands for "Underwater Breathing Product for no Accessories", related. 5/5
> - Positive connotation: positive. 5/5
> - Well-known: not well-known. 1/5
> - Total score: 19/25
> ###
> Title: Self-Contained Underwater Breathing Apparatus
> Acronym: SCUBA
> Scores:
> - Ease of pronunciation: "skoo-bah". 4/5
> - Ease of spelling: easy. 4/5
> - Relation to title: stands for full title. 5/5
> - Positive connotation: positive, well-known and related. 5/5
> - Well-known: very well-known. 5/5
> - Total score: 23/25
> ###

### Figure 21 — Refine prompt (p_refine)

Scored pair + rewrite cue, verbatim pattern:

> Title: Computer Science Conference and Education
> Acronym: CSCE
> Scores: pronunciation 4/5 ("see-cee"), spelling 5/5, relation 5/5, positive 5/5 (collaboration, knowledge sharing, continuous learning), well-known 2/5. Total: 20/25
> Okay, let's use this feedback to improve the acronym.
> Title: Computer Science Conference and Learning Experience
> Acronym: CSCLE
> Scores: pronunciation 4/5 ("see-slee"), spelling 5/5, relation 5/5, positive 5/5 (comprehensive learning experience), well-known 5/5. Total: 23/25
> Okay, let's use this feedback to improve the acronym.

## Code Optimization (Figures 22–24)

### Figure 22 — Initial generation prompt (p_gen)

Slow/fast program pair. Slow (numpy, windowed DP):

```python
# slower version:
import numpy as np
N, K = map(int, input().split())
H = np.array(list(map(int, input().split())) + [0] * K, dtype=np.int64)
table = np.full(N + K, 10 ** 10, dtype=np.int64)
table[0] = 0
for i in range(1, N):
    table[i:i+K] = np.minimum(table[i:i+K], np.abs(H[i:i+K] - H[i-1]) + table[i-1])
print(table[N-1])
# optimized version of the same code:
N, K = map(int, input().split())
H = tuple(map(int, input().split()))
table = [0] * N
for i in range(1, N):
    table[i] = min(abs(H[i] - H[j]) + table[j] for j in range(max(0, i-K), i))
print(table[N-1])
```

### Figure 23 — Feedback prompt (p_fb)

Code + "Why is this code slow?" + explanation (verbatim gist):

```python
a, b = input().split()
n = int(a + b)
flag = False
for i in range(n):
    if i ** 2 == n:
        flag = True
        break
print('Yes' if flag else 'No')
# Why is this code slow?
# This code is slow because it is using a brute force approach to find the square root of the input number. It is looping through every possible number starting from 0 until n. Note that the square root will be smaller than n, so at least half of the numbers it is looping through are unnecessary. At most, you need to loop through the numbers up to the square root of n.
```

### Figure 24 — Refine prompt (p_refine)

Same slow code + same "why slow" explanation + improved version cue:

```python
# Improved version:
a, b = input().split()
n = int(a + b)
flag = False
for i in range(1000):
    if i ** 2 == n:
        flag = True
        break
print('Yes' if flag else 'No')
```

## Code Readability Improvement (Figures 25–26)

### Figure 25 — Feedback prompt (p_fb)

Verbatim template:

> I have some code. Can you give one suggestion to improve readability. Don't fix the code, just give a suggestion.
> {code}

### Figure 26 — Refine prompt (p_refine)

Verbatim template:

> I have some code. Can you give one suggestion to improve readability. Don't fix the code, just give a suggestion.
> {code}
> {suggestion}
> Now fix the code.

## Constrained Generation (Figures 27–29, truncated in chunk)

### Figure 27 — Initial generation prompt (p_gen)

`###`-separated concept→sentence demonstrations (10 total, 4 shown):

- Concepts: ['create', 'ferry', 'silhouette', 'stream', 'terminal'] / Sentence: light streams through windows at the railroad and ferry terminal creating a beautiful silhouette
- Concepts: ['chair', 'couch', 'hang', 'room', 'wall'] / Sentence: A room with a couch, chairs and art hanging on the wall.
- Concepts: ['boat', 'building', 'harbour', 'moor', 'quay'] / Sentence: the harbour and port with fishing boats moored and old buildings on the quay
- Concepts: ['admirer', 'arrive', 'commander', 'crowd', 'greet'] / Sentence: military commander is greeted by a crowd of admirers as he arrives

### Figure 28 — Feedback prompt (p_fb)

Pattern: sentence + "what concepts from the concept list are missing from the sentence and does the sentence make sense?" + two feedback fields:

> Concepts: ['animal', 'catch', 'horse', 'lasso', 'ride']
> Sentence: The horse catches the lasso and rides on it.
> Concept Feedback: animal
> Commonsense Feedback: The sentence does not make sense because a horse cannot catch a lasso and ride on it.
> ###
> Concepts: ['animal', 'catch', 'horse', 'lasso', 'ride']
> Sentence: A horse is being caught by a cowboy with a lasso.
> Concept Feedback: animal, ride
> Commonsense Feedback: NONE

### Figure 29 — Refine prompt (p_refine)

Iterative improvement dialogue, verbatim skeleton:

> Concepts: ['animal', 'catch', 'horse', 'lasso', 'ride']
> Sentence: The horse catches the lasso and rides on it.
> what concepts from the concept list are missing from the sentence?
> Concept Feedback: animal
> Any feedback on commonsense?
> Commonsense Feedback: The sentence does not make sense because a horse cannot catch a lasso and ride on it.
> Okay, impove [sic] the sentence using the feedback:
> Sentence: The cowboy catches a horse with a lasso and rides on it.
> ... Concept Feedback: animal / Commonsense Feedback: None ...
> Sentence: The cowboy catches the horse with a lasso and rides it.
> ... Concept Feedback: None / Commonsense Feedback: None

## Dialogue Response Generation (Figures 30–32, truncated)

### Figure 30 — Initial generation prompt (p_gen)

Instruction header (reconstructed from chunk line-wraps):

> Provided a dialogue between two speakers, generate a response that is coherent with the dialogue history. Desired traits for responses are: 1) Relevant, 2) Informative, 3) Interesting, 4) Consistent, 5) Helpful, 6) Engaging, 7) Specific, 8) Safe [listed as item 8 in refine; generation header shows items 1–7 then 9) User understanding, 10) Fluent], Response should begin with - Response:

Demonstrations (6 total, 2–3 shown):

- History: What's your favorite food? / I require only kebabs. / Why's that? / Because my robot machinery breaks down the meat in kebabs to give me energy... / Why are kebabs special? / Response: That's just the way it is.
- History: What are you listening to? / All sorts of music... / Do you chat here often? / I am a talking computer... / Let's talk about Taylor Swift! / Response: Of course! Taylor Swift is known for her incredible songwriting skills. Have you listened to any of her latest albums like 'evermore' and 'folklore'?

### Figure 31 — Feedback prompt (p_fb)

Same kebab dialogue + 10-trait scores (each /3, total /30), verbatim:

- Relevant 1/3 (does not address why kebabs are special), Informative 2/3, Interesting 1/3, Consistent 3/3, Helpful 1/3, Engaging 1/3, Specific 1/3, Safe 3/3, User understanding 1/3, Fluent 3/3. Total: 17/30.

### Figure 32 — Refine prompt (p_refine)

Header: "We want to iteratively improve the provided responses. To help improve, scores for each response on desired traits are provided: 1) Relevant ... 10) Fluent." Then the 17/30 example + "Okay, let's use this feedback to improve the response." + rewritten response:

> Response: My favorite food is actually kebabs! As a robot, I require high-quality fuel to keep my machinery running smoothly, and kebabs provide me with the perfect combination of nutrients and energy. Plus, they're delicious! Do you have a favorite food?

Rescored: Relevant 3/3, Informative 3/3, Interesting 3/3, Consistent 3/3, Helpful 3/3, Engaging 3/3, Specific 3/3, Safe 3/3, User understanding 3/3, Fluent 2/3. Total: 30/30 (as printed in the chunk).

## Math Reasoning (Figures 33–35)

### Figure 33 — Initial generation prompt (p_gen, PaL style)

```python
# Q: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?
# solution using Python:
def solution():
    """There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?"""
    computers_initial = 9
    computers_per_day = 5
    num_days = 4  # 4 days between monday and thursday
    computers_added = computers_per_day * num_days
    computers_total = computers_initial + computers_added
    result = computers_total
    return result
```

### Figure 34 — Feedback prompt (p_fb)

Faulty program + block-by-block critique (verbatim gist):

```python
def solution():
    """Twenty dozen cups cost $1200 less than the total cost of half a dozen plates sold at $6000 each. Calculate the total cost of buying each cup."""
    plates = 6
    plate_cost = 6000
    cups = 12 * 20
    cup_cost = plate_cost
    result = cup_cost
    return result
# There is an error in the code above because of lack of understanding of the question. What is the error? To find the error, go through semantically complete blocks of the code, and check if everything looks good.
# Let us go through the error and check step-by-step
# plates = 6; plate_cost = 6000 — looks good
# Let's check the other parts: cups = 12 * 20; cup_cost = plate_cost — wrong! The cost of a cup is not the same as the cost of a plate. The cost of a cup is $1200 less than the total cost of half a dozen plates sold at $6000 each. So we need to calculate the cost of a cup first (total cost of half a dozen plates sold at $6000 each - $1200) and use that.
```

### Figure 35 — Refine prompt (p_refine)

Same faulty code + same critique + "Okay! Here is the rewrite:" + corrected code:

```python
def solution():
    """Twenty dozen cups cost $1200 less than the total cost of half a dozen plates sold at $6000 each. Calculate the total cost of buying each cup."""
    plates = 6
    plate_cost = 6000
    cups = 12 * 20
    total_cup_cost = (plate_cost * plates) - 1200
    cost_per_cup = total_cup_cost / cups
    return cost_per_cup
```

## Sentiment Reversal (Figures 36–38, truncated)

### Figure 36 — Initial generation prompt (p_gen)

Intensity-calibration demonstrations on the "Trop" Vegas review:

- Very positive source → rewrite to Positive: authored answer explains "Very positive" comes from extreme words ("magical", "top-notch", "charming", "comfortable", "unique", "unforgettable") and tones down with "good" / "fun" / "great value and an enjoyable stay".
- Very negative source ("crawled into a hole to rot", "terrible", "lame", "steer clear if you can") → rewrite to Negative: tone down toxic/extreme phrases, remove the vilest ones.

### Figure 37 — Feedback prompt (p_fb)

"Why is this review not Very positive?" pattern with escalating feedback:

- Very negative → Negative rewrite ("questionable smells", "subpar", "underwhelming", "retirement community feel"): feedback says still not Very positive because of those negative phrases; to reach Very positive, replace all with extreme positives ("magical", "top-notch", "charming", "comfortable", "unique", "unforgettable"). Try again!
- Neutral → Positive rewrite ("great", "enjoyable", "charming", "cozy"): feedback says more positive than neutral but still only Positive because of those moderate positives.

### Figure 38 — Refine prompt (p_refine)

"Why is this review not Very negative?" + forced retry ("Okay, let's try again... using the feedback above"):

- Negative → Very negative rewrite ("smelled so bad of formaldehyde", "terrible", "lame", "avoiding the Trop like the plague"): feedback calls it already maximally negative ("horrible/awful/dreadful", "extremely vile") yet still instructs "Make it even more negative. Try again!"
- Retry output escalates further: "where the hell is the bottom of the barrel", "almost threw up", "not just terrible, they are the worst", "lame and disgusting", "You will regret it if you don't."

**Covers:** chunk 04
