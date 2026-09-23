---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: We improved 15 LLMs at coding in one afternoon. Only the harness changed. — Stencil

### Q1. Why does the article call "which model is best at coding" the wrong question, and what does it mean by the harness?

> [!tip]- Answer
> The article argues the model-only framing is misleading because the harness — tool schemas, error messages, state management, everything between "the model knows what to change" and "the issue is resolved" — is where most failures happen in practice. Being model agnostic makes an open harness a great testing ground, since the model is just a parameter while the harness is the variable the builder actually controls. See [[wiki/01-the-wrong-question|The Wrong Question]].

### Q2. Why does Codex's apply_patch format cause catastrophic failure rates when given to other models?

> [!tip]- Answer
> Apply_patch passes an OpenAI-flavored diff as an unstructured string blob that must follow strict rules, and the article speculates token selection is biased toward that structure at the gateway for Codex variants of GPT. Handed to unaware models, patch failures explode — Grok 4 failed 50.7% of patches and GLM-4.7 failed 46.2% — which the article reads as models not speaking the language rather than being bad models. See [[wiki/01-the-wrong-question|The Wrong Question]].

### Q3. What makes str_replace_exact-match editing so fragile, and what did Cursor do about it?

> [!tip]- Answer
> Str_replace forces the model to reproduce every character of the old text perfectly, including whitespace and indentation, and rejects the edit on multiple matches, producing the notorious "String to replace not found in file" failure with its own issues megathread. Cursor instead trained a separate 70B merger model to fuse a draft edit into the file correctly, yet even their blog admits full-file rewrites beat aider-like diffs for files under 400 lines. See [[wiki/01-the-wrong-question|The Wrong Question]].

### Q4. How does the proposed hashline format let a model express an edit without reproducing file content?

> [!tip]- Answer
> On every read or grep, each line returns tagged with a 2–3 character content hash, e.g. `2:f1|  return "world";`, and the model then references tags such as "replace line 2:f1" or "replace range 1:a3 through 3:0e". If the file changed since the last read, the hashes optimistically mismatch and the edit is rejected before anything is corrupted, so recalling a pseudo-random tag proves the model knows what it is editing without retyping whitespace. See [[wiki/01-the-wrong-question|The Wrong Question]].

### Q5. How was the 16-model benchmark constructed, and which result best shows that patch failures had been hiding true model ability?

> [!tip]- Answer
> Each task mutated a random React file with a mechanical bug (operator swap, boolean flip, off-by-one, removed guard clause) plus a plain-English description, then ran 3 runs of 180 tasks with a fresh agent session using only read, edit, and write tools. The clearest hidden-ability case is Grok Code Fast 1 rising from 6.7% to 68.3% — roughly a tenfold gain — with hashline beating patch in 14 of 16 models and v2 improving further in 12 of 16. See [[wiki/01-the-wrong-question|The Wrong Question]].

### Q6. Why did output tokens fall by up to 61% under hashline, and why does the article compare a +8% Gemini gain to a model upgrade?

> [!tip]- Answer
> Tokens fell — 61% best case for Grok 4 Fast — because the model stopped burning tokens on retry loops after failed patch or str_replace attempts. The +8% Gemini success-rate gain matters because it exceeds what most model upgrades deliver while costing zero training compute and only about $300 in benchmarking, showing the model is usually flaky at expressing itself rather than at understanding the task. See [[wiki/01-the-wrong-question|The Wrong Question]].

### Q7. A team choosing between funding a model upgrade and funding open-harness work (plus a vendor deciding whether to block third-party harnesses) should do what, judging from this article's evidence?

> [!tip]- Answer
> They should fund the harness experiment first, since a one-afternoon, ~$300 edit-tool change lifted models ~15 points on average with no training compute — an ROI most model upgrades cannot match. Vendors should likewise keep harnesses open rather than blocking tools like OpenCode or banning benchmark accounts, because no vendor tunes for competitors' models while an open harness tunes for all of them, making the harness the bridge that carries every vendor's own models forward. See [[wiki/01-the-wrong-question|The Wrong Question]].
