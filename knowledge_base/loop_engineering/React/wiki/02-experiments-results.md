> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Knowledge-intensive and decision-making experiments

**In one sentence:** ReAct prompting generalizes across models (PaLM-540B and GPT-3), retrieves up-to-date knowledge that static labels and reasoning- or acting-only baselines miss, supports human thought-editing for behavior correction, and is backed by fully specified finetuning configs and verbatim HotpotQA, FEVER, WebShop, and ALFWorld prompts.

## Key points

- GPT-3 (text-davinci-002, greedy decoding) outperforms PaLM-540B with ReAct prompting: 30.8 vs 29.4 exact match on HotpotQA (500-question validation subset) and 78.4% vs 70.9% success rate on ALFWorld (all 134 unseen validation instances), suggesting instruction tuning helps and ReAct works across different large language models.
- ReAct retrieves up-to-date answers (e.g. a hotel-size question whose answer grew after HotpotQA was built) where Standard and CoT hallucinate and Act fails despite web access, because only ReAct combines reasoning to guide interaction with live retrieval.
- Human-in-the-loop thought editing works: removing one hallucinating sentence (Act 17) and adding hints (Act 23) rescues a failing ALFWorld trajectory, turning tens of manual actions into a two-thought edit that changes beliefs, reasoning style, and subsequent actions.
- Finetuning uses batch size 64 everywhere; on PaLM-8B, ReAct/Act train 4,000 steps vs Standard/CoT 2,000 steps, and on PaLM-62B, ReAct/Act train 4,000 steps vs Standard/CoT 1,000 steps, because ReAct/Act benefit from more steps and data while Standard/CoT degrade soon after finetuning starts.
- The ReAct-IM ablation restricts thoughts to dense external-feedback style: only decomposing the current goal and naming the current subgoal, with no thoughts for subgoal completion, next-subgoal selection, or using pretraining knowledge to locate items.
- Verbatim few-shot prompts are fully specified: 6 HotpotQA examples each for Standard/Act/CoT/ReAct with Search/Lookup/Finish and Thought+Action+Observation traces, 3 FEVER claims (SUPPORTS/REFUTES/NOT ENOUGH INFO), a full WebShop deodorant trajectory (search, think, click scent/size/Buy Now), and ALFWorld clean-lettuce trajectories for Act, ReAct, and ReAct-IM.

---

## Additional results: GPT-3 experiments

Results on two benchmarks (Table 5 in the paper):

| Model | HotpotQA (exact match) | ALFWorld (success rate %) |
|---|---|---|
| PaLM-540B | 29.4 | 70.9 |
| GPT-3 (text-davinci-002, greedy) | 30.8 | 78.4 |

Setup notes from the chunk:

- HotpotQA: random subset of 500 validation questions.
- ALFWorld: all 134 unseen validation task instances, using the best prompt set selected for PaLM-540B.
- GPT-3 consistently outperforms PaLM-540B, possibly because it is finetuned with human instruction following.
- Conclusion stated in the chunk: ReAct prompting is effective across different large language models on different tasks.
- Code reference given in the chunk: https://react-lm.github.io/ .

## Additional results: up-to-date knowledge on HotpotQA

- During trajectory inspection, ReAct sometimes disagrees with dataset labels because the labels themselves are outdated.
- Example (Figure 4): a question about the size of a hotel, which increased after HotpotQA construction.
- Standard and CoT give wrong answers due to hallucination.
- Act fails despite having web access, due to lack of reasoning to guide how to interact with the Internet for QA.
- Only ReAct retrieves up-to-date information and gives a reasonable answer.
- Stated implication: better incorporation of reasoning may benefit Internet-augmented language models (Nakano et al. 2021; Lazaridou et al. 2022; Shuster et al. 2022a) for up-to-date task solving.

## Additional results: human-in-the-loop behavior correction on ALFWorld

Figure 5 example:

- (a) ReAct trajectory fails due to a hallucinating thought (Act 17).
- (b) A human edits two thoughts (Act 17, 23) — removing a hallucinating sentence and adding hints — and the trajectory then produces desirable reasoning traces and actions and succeeds.
- From a human perspective, solving the task drops from typing tens of actions to editing a couple of thoughts, enabling new human-machine collaboration.
- Such on-the-go policy editing is difficult for Act and prior RL methods: a human cannot change model parameters, and changing a few actions may not change the rest of the behavior.
- It goes beyond dialogue-based goal/subgoal updates (Huang et al. 2022b): editing ReAct thoughts can also modify internal belief, reasoning style, or anything the flexible thought space supports.
- Left as future work for human alignment with more systematic study.

## Experiment details: HotpotQA finetuning

- Batch size 64 for all finetuning.
- PaLM-8B: ReAct and Act finetuned for 4,000 steps; Standard and CoT for 2,000 steps.
- PaLM-62B: ReAct and Act finetuned for 4,000 steps; Standard and CoT for 1,000 steps.
- Observation: ReAct and Act generally benefit from more training steps (and more training data), while Standard and CoT degrade soon after finetuning.

## Experiment details: ALFWorld IM-style ablation

- The same expert trajectories used in ReAct are reannotated with dense external-feedback thoughts.
- ReAct-IM is limited to thinking about (1) decomposing the current goal and (2) the current subgoal to complete.
- ReAct-IM lacks thoughts that (1) determine when a subgoal is completed, (2) determine what the next subgoal should be, (3) induce the LLM to use internal pretraining knowledge to identify where items can be in the environment.

## Prompts: HotpotQA

Four prompt styles, each with the same 6 questions (Colorado orogeny elevation, Milhouse/Nixon, Finnish-rock documentary, Nicholas Ray + Elia Kazan professions, Arthur's Magazine vs First for Women, Urysohn vs Levin):

- Standard: Question followed directly by Answer (e.g. "1,800 to 7,000 ft", "Richard Nixon", "The Saimaa Gesture", "director, screenwriter, actor", "Arthur's Magazine", "Yes").
- Act: Question followed by Action/Observation chains using `Search[...]`, `Lookup[...]`, `Finish[...]` (e.g. Search[Colorado orogeny] -> Lookup[eastern sector] -> Search[High Plains] -> Search[High Plains (United States)] -> Finish[1,800 to 7,000 ft]).
- CoT: Question followed by a "Let's think step by step" Thought then Answer.
- ReAct: Question followed by interleaved Thought/Action/Observation (Thought 1..5, e.g. "I need to search Colorado orogeny, find the area that the eastern sector extends into, then find the elevation range...") ending in `Finish[...]`.

## Prompts: FEVER

Task instruction: "Determine if there is Observation that SUPPORTS or REFUTES a Claim, or if there is NOT ENOUGH INFORMATION."

Three claims used in all styles:

- "Nikolaj Coster-Waldau worked with the Fox Broadcasting Company." -> SUPPORTS (Search finds New Amsterdam 2008 and Fox film Virtuality 2009).
- "Stranger Things is set in Bloomington, Indiana." -> REFUTES (set in fictional Hawkins, Indiana).
- "Beautiful reached number two on the Billboard Hot 100 in 2003." -> NOT ENOUGH INFO (Lookup confirms peak at number two, but no year 2003 confirmation).

Act uses Search/Lookup/Finish; CoT uses a single Thought + Answer; ReAct interleaves Thought 1-4 with each Search/Lookup before Finish.

## Prompts: WebShop

- Instruction: "i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars".
- Act trajectory: search "3 ounce bright citrus deodorant sensitive skin" -> click B078GWRC1J (Bright Citrus Deodorant by Earth Mama, $10.99) -> click bright citrus -> click 3 ounce (pack of 1) -> click Buy Now.
- ReAct trajectory: same search and clicks, plus explicit `think` steps ("B078GWRC1J and B078GTKVXY are bright citrus deodorant less then 50 dollars. I can check B078GWRC1J first." and "For 3 ounce bottle of bright citrus deodorant for sensitive skin, the item has options 'bright citrus' and '3 ounce (pack of 1)' and seems good to buy."), each acknowledged with "OK."

## Prompts: ALFWorld

Task: "put a clean lettuce in diningtable." Initial room lists cabinets 1-13, coffeemachine 1, countertop 1, diningtable 1, drawer 1, fridge 1, garbagecan 1, microwave 1, shelves 1-3, sinkbasin 1, stoveburners 1-4, toaster 1.

- Act prompt (Table 7): action-only demo — go to fridge 1, open it (cup 3, egg 2, potato 3, potato 2), go to diningtable 1 (find lettuce 1), take it, go to sinkbasin 1, clean lettuce 1, one `think: Now I clean a lettuce (1)...`, go back, put lettuce in/on diningtable 1.
- ReAct prompt (Table 8): same actions plus planning thoughts — decompose task (find, take, clean, put), prior over lettuce locations (fridge, diningtable, sinkbasin, stoveburner, cabinets), "Now I find/take/clean a lettuce (1)" progress markers before each action.
- ReAct-IM prompt (Table 9): same actions but thoughts restricted to current-goal decomposition ("To solve the task, I need to find and take a lettuce...", "First I need to find a lettuce.", "I need to clean this lettuce (1) using sinkbasin 1.", "I need to put this cleaned lettuce (1) in/on diningtable 1.").

## References in this chunk

Key references listed: Brown et al. 2020 (GPT-3); Nakano et al. 2021 (WebGPT); Lazaridou et al. 2022 and Shuster et al. 2022a/b (Internet-augmented/dialogue LMs); Huang et al. 2022a/b (planners, inner monologue); Shridhar et al. 2020a/b (ALFRED, ALFWorld); Yao et al. 2020/2022 (CALM, WebShop); Wei et al. 2022, Wang et al. 2022a/b, Kojima et al. 2022, Zhou et al. 2022, Creswell et al. 2022, Nye et al. 2021, Zelikman et al. 2022 (reasoning); Lewis et al. 2020 (RAG); plus Vygotsky/Luria/Baddeley and agent papers (Ahn, Reed, Li, Karamcheti, Micheli, Abramson).

**Covers:** chunk 02: sections 3-5
