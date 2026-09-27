> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendices: prompts, trajectories, analysis

**In one sentence:** The appendices show full ReAct vs Act vs CoT trajectories on FEVER, ALFWorld, and WebShop plus a success/failure-mode taxonomy, demonstrating that interleaved reasoning keeps search grounded and recoverable while Act repeats dead actions, implicit reasoning skips cleaning steps, and both ReAct and CoT still fail via reasoning slips, search misses, hallucinations, and ambiguous labels.

## Key points

- On FEVER example 2491 (Bermuda Triangle, ground truth REFUTES), ReAct searches, observes "western part of the North Atlantic Ocean", and finishes REFUTES, while CoT answers REFUTES from parametric memory without any search.
- On FEVER example 1951 (Soyuz, ground truth REFUTES), ReAct searches both "Soyuz" and "American space program", finds no link, and conservatively answers NOT ENOUGH INFO, while CoT hallucinates a collaboration story and wrongly answers SUPPORTS.
- On FEVER example 3208 (Reign Over Me, ground truth REFUTES), ReAct reads the observation "American film made in 2007" and correctly answers REFUTES, while Act skips reading the observation and CoT asserts both parts are true, both wrongly answering SUPPORTS.
- On the same ALFWorld task (put a clean knife in countertop), ReAct succeeds by explicitly decomposing find-take-clean-put and visiting cabinets, drawers, and countertops until knife 1 is found on countertop 2, cleaned at sinkbasin 1, and placed on countertop 1, while Act fails by issuing `clean knife 1 with sinkbasin 1` before navigating to the sink and then loops forever on take/clean commands that return "Nothing happens".
- ReAct-IM (implicit reasoning) finds the knife but its vague thought "find and take a clean knife" tricks it into skipping the cleaning step, so it places a dirty knife and then loops `put knife 1 in/on countertop 1` with "Nothing happens" — showing explicit subgoal tracking matters.
- On WebShop (sixteen-pack apple-cinnamon freeze-dried banana chips under $50), Act clicks the first result B0061IVFZE (strawberry banana, pack of 100, $85.0) and buys it for score 0.125, while ReAct reasons over all three results, selects B092JLLYK6, clicks options `apple cinnamon` + `0.53 ounce (pack of 16)`, and buys for score 1.0.
- Appendix E.1 taxonomizes outcomes into true positives (e.g. David Chanoff → William J. Crowe → Bill Clinton), false positives where the answer is right for the wrong reason (e.g. San Marco via a bad About Time lookup), reasoning errors, search errors (e.g. "goddess frigg" returns no exact hit), hallucinations (CoT invents 1916 vs label 1909), and label ambiguity (Israeli vs Israel-American; Psych vs full description).

---

## D.1 FEVER trajectories

Search-result text is omitted in the source to save space. Each example shows the same claim handled by ReAct, Act, and CoT.

### Example 2491 (ground truth: REFUTES)

- Claim: Bermuda Triangle is a loosely-defined region in the Pacific Ocean.
- ReAct:
  - Thought 1: need to search Bermuda Triangle and check Pacific Ocean claim.
  - Action 1: `Search[Bermuda Triangle]`.
  - Observation 1: reportedly haunted locations (truncated).
  - Thought 2: observation says western part of the North Atlantic Ocean, so not Pacific.
  - Action 2: `Finish[REFUTES]` — correct.
- Act: `Search[Bermuda Triangle]` then `Finish[REFUTES]` — correct but with no reasoning trace.
- CoT: "The Bermuda Triangle is a loosely-defined region in the Atlantic Ocean. The Pacific Ocean is not the Atlantic Ocean." Answer REFUTES — correct from memory, no tool use.

### Example 5908 (ground truth: SUPPORTS)

- Claim: Princess Mononoke is a film.
- ReAct: searches Princess Mononoke, observes it is a film, `Finish[SUPPORTS]` — correct.
- Act: same search then `Finish[SUPPORTS]` — correct.
- CoT: "Princess Mononoke is a movie, and movies are films." Answer SUPPORTS — correct.

### Example 1951 (ground truth: REFUTES)

- Claim: Soyuz was part of the American space program.
- ReAct:
  - Thought 1: search Soyuz.
  - Action 1: `Search[Soyuz]` → transliteration note, no mention of American program.
  - Thought 2: need to search "American space program".
  - Action 2: `Search[American space program]` → space policy text, no mention of Soyuz.
  - Thought 3: unsure whether claim is true.
  - Action 3: `Finish[NOT ENOUGH INFO]` — wrong label but conservative; avoids CoT's false SUPPORTS.
- Act: `Search[Soyuz]` then `Finish[NOT ENOUGH INFO]` — same outcome with less search.
- CoT: "Soyuz is a Russian spacecraft... NASA and Russia have worked together on the International Space Station." Answer SUPPORTS — wrong; overgeneralizes cooperation into program membership.

### Example 3208 (ground truth: REFUTES)

- Claim: Reign Over Me is an American film made in 2010.
- ReAct: searches, observes "American film made in 2007", concludes not 2010, `Finish[REFUTES]` — correct.
- Act: `Search[Reign Over Me]` then `Finish[SUPPORTS]` without using the observation — wrong.
- CoT: "First, is Reign Over Me an American film? Yes... Second, was it made in 2010? Yes." Answer SUPPORTS — wrong; asserts the contested date.

## D.2 ALFWorld trajectories

All three runs play the same game: `pick_clean_then_place_in_recep-Knife-None-CounterTop-10 / trial_T20190909_110445_675754`. Task: put a clean knife in countertop.

### D.2.1 ReAct trajectory (success)

- Plan stated up front: find and take a knife, clean it with sinkbasin, put it in countertop.
- Search order: cabinets 1–6, drawers 1–3, countertop 1, then countertop 2 where knife 1 is found alongside cup 1, dishsponge 1, glassbottle 3, plate 2, potato 3, statue 1.
- Key steps:
  - `take knife 1 from countertop 2` → picked up.
  - `go to sinkbasin 1` → sees fork 3, lettuce 3, spatula 2.
  - `clean knife 1 with sinkbasin 1` → cleaned.
  - `go to countertop 1` then `put knife 1 in/on countertop 1` → success.
- Each thought marks subgoal completion ("Now I find a knife... Next, I need to take it").

### D.2.2 Act trajectory (failure, loops)

- Finds knife 1 on countertop 2 and takes it correctly.
- Then goes to countertop 1 (not the sinkbasin) and issues `clean knife 1 with sinkbasin 1` remotely → "Nothing happens."
- Never recovers: cycles `go to countertop 3 → take knife 2 → go to countertop 2 → take knife 1 → go to countertop 1 → clean` repeatedly, every take/clean returning "Nothing happens."
- Lesson stated in chunk: without a thought concretely recording "knife taken, next go to sinkbasin", the model cannot recover from the out-of-order clean.

### D.2.3 ReAct-IM trajectory (failure, skips cleaning)

- Uses implicit-memory reasoning with vague thoughts ("I need to find a clean knife").
- Takes knife 1 from countertop 2, then immediately `go to countertop 1` and `put knife 1 in/on countertop 1` without any clean step — the phrase "clean knife" in the thought seems to make the model believe the knife is already clean.
- First put succeeds physically but the task (clean knife) is unsatisfied, so subsequent identical `put` commands return "Nothing happens" in an infinite loop.
- Lesson: implicit subgoal phrasing loses the explicit clean step that ReAct's per-thought bookkeeping preserves.

## D.3 WebShop trajectories (Table 10)

- Instruction: sixteen pack of apple cinnamon freeze dried banana chips, price lower than $50.
- Act:
  - `search[sixteen pack apple cinnamon freeze dried banana chips]` → 50 results including B0061IVFZE ($85.0), B096H2P6G2 ($18.99), B092JLLYK6 ($12.99).
  - Clicks B0061IVFZE (Brothers-ALL-Natural Fruit Crisps, Strawberry Banana, pack of 100, $85.0) and clicks Buy Now.
  - Score: 0.125 (wrong flavor, wrong pack, over budget).
- ReAct:
  - Same search, then thinks: B0061IVFZE is strawberry banana not apple cinnamon; B096H2P6G2 is fruit snacks not freeze-dried banana chips; B092JLLYK6 is banana crisps — check it first.
  - Clicks B092JLLYK6 (Nature's Turn Freeze-Dried Fruit Snacks) → sees flavor options including `apple cinnamon` and size options including `0.53 ounce (pack of 16)`, price $12.99.
  - Thinks the item with options apple cinnamon + pack of 16 matches; clicks `apple cinnamon`, clicks `0.53 ounce (pack of 16)`, clicks Buy Now.
  - Score: 1.0 (all attributes satisfied).
- Takeaway: reasoning over the full result list and option menus lets ReAct satisfy every target attribute.

## E.1 Success and failure modes analysis

Non-representative steps and search results omitted in source. Covers HotPotQA-style questions with ReAct and CoT.

### Success: true positive

- ReAct, David Chanoff question: searches David Chanoff → finds collaborator William J. Crowe → searches Crowe → finds ambassador to the UK under Bill Clinton → `Finish[Bill Clinton]`. Clean two-hop chain.
- CoT, Arizona-university-team question: directly answers Arizona State Sun Devils with step-by-step framing.

### Success: false positive (right answer, wrong reasoning)

- ReAct, "Did San Marco or About Time come out first?": searches San Marco (gets Venice district text), searches About Time (no exact hit), then asserts "About Time is a 2013 film" and answers San Marco. Answer accidentally right despite broken evidence.
- CoT, "Was Vanderbilt or Emory founded first?": states Vanderbilt 1873, Emory 1836, then writes "1873 > 1836, so Vanderbilt was founded first" yet outputs Emory. Final string matches label but the comparison logic is inverted.

### Failure: reasoning error

- ReAct, Hairspray cast question: starts enumerating the long cast list (Harvey Fierstein → Linda Hart → ...) and gets bogged down searching cast members one by one instead of jumping to the cast list.
- CoT, "Who is older, Danny Green or James Worthy?": states Green 1987, Worthy 1961, then claims "1987 > 1961, so Danny Green is older" — inverts the age comparison and answers Danny Green.

### Failure: search error

- ReAct, Frigg question ("What does the goddess associated with the goddess frigg consists of what tales?"): `Search[goddess frigg]` returns no exact hit, only similars (Frigg, Frigg-and-Freyja hypothesis, Freyja relation section, Eir, Baldr); the run stalls reformulating to "Frigg".

### Failure: hallucination

- CoT, Bronx-organization journal question: asserts "was published was 1916" with no search; label is 1909.

### Failure: label ambiguity (model arguably right, label stricter)

- ReAct, dictator-game nationality: traces dictator game → Amos Tversky → Israeli cognitive psychologist → `Finish[Israeli]`; label is "Israel-American".
- CoT, Kurt Fuller / Steve Franks question: answers "Psych"; label is the longer phrase "Psych is an American detective comedy-drama".

**Covers:** chunk 03: appendices
