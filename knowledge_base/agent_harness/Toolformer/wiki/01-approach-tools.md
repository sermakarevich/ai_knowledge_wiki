> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Approach and tool set (intro-3)

**In one sentence:** Toolformer teaches a language model (in this paper, GPT-J with 6.7B parameters) to use external tools by sampling candidate API calls via in-context learning from a handful of demonstrations, keeping only calls that reduce next-token loss by at least a filtering threshold, and finetuning on the augmented texts so the model itself decides when, which, and how to call each tool.

## Key points

- Toolformer targets four inherent LM weaknesses — stale knowledge/hallucination, low-resource languages, imprecise arithmetic, and no sense of time — by giving the model callable tools instead of relying on further scaling.
- Learning is self-supervised from only a handful of human-written demonstrations per API: the LM annotates a large pretraining-style corpus with candidate calls, and a loss-based filter decides which calls are actually useful.
- API calls use special markers `<API> a_c(i_c) </API>` without the result and `<API> a_c(i_c) -> r </API>` with the result (implemented as `[`, `]`, `->` so no vocabulary change is needed), seamlessly interleaved into plain text.
- Sampling keeps positions where P(`<API>`) exceeds threshold tau_s (top-k kept), then samples up to m calls per position ending with `</API>`; filtering keeps a call only if L_i(-) - L_i(+) >= tau_f, i.e. the call plus its result lowers weighted cross-entropy over future tokens versus no call or call-without-result.
- The augmented dataset C* contains exactly the same texts as C plus inserted useful calls, so finetuning on C* preserves general language modeling ability while teaching the model where and how to use tools.
- Five tools are covered: Atlas-based factoid QA, BM25 Wikipedia search over the KILT dump, four-operation calculator (rounded to 2 decimals), NLLB-600M translation into English for 200 languages with fastText language detection, and an input-free calendar returning the current date.
- After finetuning, inference decodes normally until the model emits `->`, at which point decoding pauses, the API is executed, and the response plus `</API>` is inserted before continuing.

---

## Abstract and problem statement

- Language models (LMs) solve new tasks from few examples or instructions at scale, yet struggle with basic functionality such as arithmetic or factual lookup where smaller models excel.
- Toolformer is trained to decide which APIs to call, when to call them, what arguments to pass, and how to incorporate results into future token prediction.
- Training is self-supervised, requiring nothing more than a handful of demonstrations per API.
- Tools incorporated: calculator, Q&A system, search engine, translation system, calendar.
- Result: substantially improved zero-shot performance across downstream tasks, often competitive with much larger models, without sacrificing core language modeling abilities.

## 1 Introduction

- Large LMs show strong zero-/few-shot results and emergent capabilities, but retain limitations only partially fixed by scaling: no access to up-to-date information, hallucinated facts, poor low-resource language understanding, weak precise calculation, no awareness of time progression.
- Figure 1 (described): exemplary predictions where the model autonomously calls a QA system, calculator, machine translation system, and Wikipedia search engine to complete text.
- Existing tool-use approaches either need large human annotation efforts or restrict tool use to task-specific settings, hindering widespread adoption.
- Two desiderata: (1) tool use learned self-supervised without large human annotations — also because what humans find useful may differ from what a model finds useful; (2) the LM keeps full generality and decides itself when and how to use which tool, not tied to specific tasks.
- Method sketch: from a handful of human-written API-use examples, let an LM annotate a huge LM dataset with potential API calls, use a self-supervised loss to test which calls help predict future tokens, then finetune the LM on the useful calls.
- Because the method is dataset-agnostic, it can run on the exact pretraining dataset, preserving generality and LM ability.
- Headline experiment: Toolformer based on pretrained GPT-J (6.7B parameters) achieves much stronger zero-shot results, clearly outperforming much larger GPT-3 and several baselines on various tasks.

## 2 Approach

### 2.1 Setup and notation

- Goal: equip LM M with ability to use tools via API calls where every input and output is representable as text.
- Each call is a tuple c = (a_c, i_c) with API name a_c and input i_c; with result r the linearized forms are:
- `e(c) = <API> a_c(i_c) </API>` (call without result)
- `e(c,r) = <API> a_c(i_c) -> r </API>` (call with result)
- In practice `<API>`, `</API>`, `->` arrow are implemented as token sequences `[`, `]`, `->` so the LM vocabulary is unchanged; the paper still writes them as `<API>` / `</API>` / arrow for readability.
- Pipeline on plain-text dataset C = {x^1, ..., x^|C|}: sample candidate calls via in-context learning, execute them, filter by whether responses help predict future tokens, merge calls across tools into augmented dataset C*, finetune M on C*.
- Figure 2 (described, QA example): from input x, sample position i and candidates c_i^1..c_i^k, execute them, filter out calls that do not reduce loss L_i over next tokens, interleave survivors with original text to get x*.

### 2.2 Sampling API calls

- Per API, write a prompt P(x) encouraging annotation of example x = x_1..x_n (Figure 3 shows the QA prompt; all prompts in Appendix A.2).
- Candidate positions: compute p_i = p_M(`<API>` | P(x), x_1:i-1) for each i; keep I = {i | p_i > tau_s} with sampling threshold tau_s, capped at top-k positions.
- Per kept position i, sample up to m calls c_i^1..c_i^m from M given prefix [P(x), x_1..x_i-1, `<API>`] with `</API>` as end-of-sequence token.
- Discard examples where M never generates `</API>`.

### 2.3 Executing API calls

- Execute every generated call to get a single text-sequence response r_i.
- Mechanism depends on the API: calling another neural network, running a Python script, or retrieval over a large corpus.

### 2.4 Filtering API calls

- Let i be the call position in x = x_1..x_n, r_i the API response, and define weighted cross-entropy over tokens x_i..x_n given prefix z:
- `L_i(z) = -sum_{j=i..n} w_{j-i} * log p_M(x_j | z, x_1:j-1)`
- Compare `L_i(+) = L_i(e(c_i, r_i))` (prefix = call plus result) against `L_i(-) = min(L_i(empty), L_i(e(c_i, empty)))` (no call, or call without result).
- Rationale: a call is helpful if giving both its input and output eases future-token prediction versus no call or input-only; e(c_i, r_i) is supplied as a prefix rather than inserted at i because M is not yet finetuned on API-call text and mid-sequence insertion would break flow and hurt perplexity.
- Keep calls with `L_i(-) - L_i(+) >= tau_f` for filtering threshold tau_f.

### 2.5 Model finetuning

- Merge surviving calls across APIs: for text x = x_1..x_n with call/result (c_i, r_i) at i, build x* = x_1:i-1, e(c_i, r_i), x_i:n; generalize to multiple calls per text; repeat for all x in C to form C*.
- Finetune M on C* with a standard LM objective.
- Because C* holds the same content as C plus only loss-reducing inserted calls, M sees the same content as finetuning on C while learning from its own feedback exactly where and with what inputs to use each tool.

### 2.6 Inference

- After finetuning, decode normally until M produces the `->` token, signaling it expects an API response.
- Interrupt decoding, call the API, insert the response and the `</API>` token, then resume decoding.

## 3 Tools

- Constraints on tools: (i) inputs and outputs representable as text sequences, (ii) a few demonstrations of intended use obtainable.
- Five tools explored, with example inputs/outputs in Table 1:

| API Name | Example Input | Example Output |
|---|---|---|
| Question Answering | Where was the Knights of Columbus founded? | New Haven, Connecticut |
| Wikipedia Search | Fishing Reel Types | Spin fishing — Spin fishing is distinguished between fly fishing and bait cast fishing by the type of rod and reel used. There are two types of reels used when spin fishing, the open faced reel and the closed faced reel. |
| Calculator | 27 + 4 * 2 | 35 |
| Calendar | (empty input) | Today is Monday, January 30, 2023. |
| Machine Translation | sûreté nucléaire | nuclear safety |

### Question Answering

- Factoid QA based on another LM: Atlas, a retrieval-augmented LM finetuned on Natural Questions.

### Calculator

- Simple numeric calculations with the four basic arithmetic operations only; results always rounded to two decimal places.

### Wikipedia Search

- Given a search term, returns short Wikipedia snippets; richer than QA but the model must extract relevant parts itself.
- Backend: BM25 retriever indexing the Wikipedia dump from KILT.

### Machine Translation System

- Translates a phrase from any language into English; backbone is the 600M-parameter NLLB model covering 200 languages including low-resource ones.
- Source language auto-detected with the fastText classifier; target always English.

### Calendar

- Input-free API returning the current date, supplying temporal context for time-sensitive predictions.

**Covers:** chunk 01
