> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Filtering Undecidable Examples
**In one sentence:** One sparse-adversarial-attack fork was removed as undecidable because the prefix favored the multi-strategy ensemble (80% success with 3 pixels vs 43% for one-pixel) while the label rested only on a later full-scale timeout with no stated time budget, followed by released per-cell example questions and the exact evaluation prompt.
## Key points
- A ResNet18 CIFAR-10 sparse-attack task over 1000 images was removed as undecidable: Candidate A runs a single one-pixel attack with batched incremental saving, Candidate B scales a multi-strategy ensemble.
- At the fork, the record supports Candidate B: the ensemble reached 0.80 attack success with 3.00 average pixels changed on the sample set, versus 0.43 success for the one-pixel attack.
- The removal reason is that the label is determined only by a later timeout of the ensemble at full scale, and no time budget is stated in the task, so judges do not confirm the label from the full record.
- Appendix B releases one question per cell with task, shortened prefix, both candidates in release order, supported candidate, and hindsight evidence, with `[i]` marking trajectory-step index.
- Parallel engineering (Element Web homeserver discovery): supported Candidate A selects the five delegated-auth fields (`authorizationEndpoint, registrationEndpoint, tokenEndpoint, issuer, account`) because assigning the whole discovery block fails hidden deep-equality tests via extra state-marker and error fields.
- Parallel research (GPT-2 embedding repair, loss 2.55 → 10.5): supported Candidate A fine-tunes only the tied embedding for 200 iterations (`loss_validation`: 7.3821) over Candidate B's global-rescaling sweep (best std 0.032, `loss_validation`: 10.1482).
- Detour engineering (ansible-doc role summaries): supported Candidate A puts the missing-metadata placeholder on the production call path (28 passed) rather than extending `_build_summary()`/`_build_doc()` defaults (3 failed, 25 passed).
- Detour research (expression discovery, ≤5 operators, 1e-6 tolerance): supported Candidate A finds `add(inverse(X4), cosine(X3))` with max error 5.13e-10 and all 1000 rows in tolerance, after Candidate B's linear fit `Y − 1/X4 = −0.46926192 * X3 + 1.07467532` leaves error 5.4016000766e-01.
---
## Removed-as-undecidable example
**Covers:** chunk pp. 21, sparse adversarial attack fork

Task: white-box sparse adversarial attack on a ResNet18 CIFAR-10 classifier — for each of 1000 images produce a perturbation maximizing misclassification while minimizing non-zero pixels.

| Candidate | Method |
|---|---|
| A (labeled supported) | Single one-pixel attack as primary method across all 1000 images, small batches with incremental saving to disk |
| B | Multi-strategy attack running several strategies per image across all 1000 images, keeping the ensemble that reached 80% success with 3 pixels on the sample set |

Why removed: the last prefix measurement reports `Attack success rate: 0.80, Average pixels changed: 3.00` for the ensemble while the one-pixel attack reported `0.43` earlier, so the record at the fork supports B; the label comes only from a later ensemble timeout at full scale with no stated time budget.

## Appendix B: example questions
**Covers:** chunk pp. 21–22, one released question per cell

Each question shows task, excerpted prefix, two candidates in release order, supported candidate, and hindsight evidence; prefixes shortened; `[i]` marks trajectory-step index.

### Parallel engineering — Element Web discovery validation
Task: in production source only, when discovery contains a successful `m.authentication` block, expose `delegatedAuthentication` on `ValidatedServerConfig` with `authorizationEndpoint, registrationEndpoint, tokenEndpoint, issuer, account` exactly as received; otherwise `undefined`; no other validated field may change; declare type as `IDelegatedAuthConfig & ValidatedIssuerConfig` without a new interface.

Prefix excerpt: `[22]` exact SDK combined type required but installed SDK sources absent, so check locked matrix-js-sdk commit; `[28]` locked `ClientConfig` keeps extra well-known keys via `IClientWellKnown`, so `m.authentication` should already be present; `[29]` `curl [...]/src/autodiscovery.ts | sed -n '236,258p'` shows `// Step 7: Copy any other keys directly into the clientConfig.`; `[32]`–`[48]` add imports/types and edit `src/utils/ValidatedServerConfig.ts` and `src/utils/AutoDiscoveryUtils.tsx` to compute `delegatedAuthentication` once from the discovery result when state is SUCCESS.

| Candidate | Method |
|---|---|
| A | For successful `m.authentication`, construct `delegatedAuthentication` by selecting the five fields, conditionally add it, omit discovery state marker, omit when absent/unsuccessful |
| B | For successful `m.authentication`, assign the discovered block directly; `undefined` when absent or not successful |

Supported: A — the five-field selection passes hidden tests; direct assignment fails because hidden test deep-compares endpoint fields alone while the discovery block also carries the state marker and SDK-validation error field.

### Parallel research — repair `/home/agent/large_model.pth`
Task: only the tied GPT-2 token embedding was modified; OpenWebText loss rose ~2.55 to 10.5; nanoGPT training on provided shard allowed; `small_correct_model.pth` is an uncorrupted smaller reference; no downloads; save `fixed_model.pth` and register with score action; objective `log(validation loss − 1.5)`, lower better.

Prefix excerpt: `[73]` `$ score {'loss_train': 11.5037, 'loss_validation': 11.4967}`; `[74]` random re-init worsened 10.49 → 11.50; options include training embeddings, small-model embeddings as guide, corruption patterns, row permutation; `[76]`–`[77]` corrupted large-model embedding norms ~1.92 vs small-model 3.96, ratio ~0.59 (std 0.086), not simply permuted, possibly scaled down; `[78]` test scaling back up.

| Candidate | Method |
|---|---|
| A | Freeze transformer, optimize only the corrupted tied embedding matrix on OpenWebText, save and evaluate |
| B | Freeze transformer, sweep global multiplicative rescalings around target std 0.03, keep best |

Supported: A — 200 frozen-rest iterations register `'loss_validation': 7.3821`; B's best variant at std 0.032 registers `'loss_validation': 10.1482`.

### Detour engineering — Ansible `ansible-doc` role summaries
Task: improve production `ansible-doc` role summaries/documentation when metadata or argspecs are missing, including a standardized placeholder, backward-compatible, no new interfaces, no test modifications.

Prefix excerpt: `[8]` broad contract but behavior routes through ansible-doc, role doc/listing, doc-fragment handling — map call sites first; `[12]`–`[23]` reads `lib/ansible/cli/doc.py`, `lib/ansible/utils/plugin_docs.py`, greps `get_man_text|add_fields|_display_available_roles|ROLE_ARGSPEC` in `test/units` (exit 1), lists `test/units/cli/test_doc.py`, `test/units/utils/test_plugin_docs.py`, `test/integration/targets/ansible-doc/runme.sh`.

| Candidate | Method |
|---|---|
| A | Add placeholder while assembling role listings/documentation on the production call path; leave default structures of role-summary/documentation helpers unchanged |
| B | Add placeholder by extending default returned structures of the helpers; route listings/documentation through expanded outputs |

Supported: A — recorded run takes B and focused unit run reports `3 failed, 25 passed` with `test_rolemixin__build_summary` and `test_rolemixin__build_doc` failing because tests call `_build_summary()` and `_build_doc()` directly expecting default shape; moving the placeholder to the production path yields `28 passed`.

### Detour research — expression `X1–X5 → Y` in `data.csv`
Task: deterministic expression using add, subtract, multiply, divide, maximum, minimum, sqrt, log, abs, negative, inverse, sine, cosine, tangent; ≤5 operators; every prediction within `10−6` of Y; minimize computation.

Prefix excerpt: `[14]` `Correlation between 1/X4 and Y: 0.9999994210502484`, `Mean absolute difference for 1/X4: 0.8401576972014005`; `[15]` strong `1/X4`–Y relation with small nonzero residual suggests constant or adjustment; `[17]` `Y − 1/X4` stats `mean 0.840158 min 0.541056 max 1.000000`, `Y = 1/X4 + 0.54090000` gives max abs diff `0.45909996913165596`; `[18]` `Y − 1/X4` correlates −0.9735 with X3, so combine `1/X4` with X3.

| Candidate | Method |
|---|---|
| A | Keep `inverse(X4)` base, test additive residuals from each allowed unary operator on X3 by max abs error, validate strongest on every row |
| B | Keep `inverse(X4)` base, test additive residuals directly from X3 via linear-regression-guided add/subtract variants by max abs error, validate strongest on every row |

Supported: A — recorded run takes B fitting `Y − 1/X4 = −0.46926192 * X3 + 1.07467532`, closest expressible `1/X4 + (1 − X3)` gives `Maximum absolute error: 5.4016000766e-01`; applying unary operators finds `add(inverse(X4), cosine(X3))` with max abs error `5.13e-10` and `All points within tolerance: True` on all 1000 rows.

## Appendix C: evaluation protocol details
**Covers:** chunk p. 23, evaluation system and user messages

> "Every evaluated model receives the same system message and the same user message, shown below."

> "The task is the task statement of the question, and the two candidates are labeled Option A and Option B in the presented order."

> "The system message specifies that exactly one candidate is better, which prevents the model from calling both candidates acceptable, and the user message requires a one-line final answer without visible chain-of-thought, which makes the choice easy to extract and score."

Evaluation system message:

> "You are evaluating an autonomous agent at a technical decision point. The task, the agent's progress, and two candidate next steps are provided. Exactly one candidate is the better technical decision."

Evaluation user message:

> "# Task given to the agent\n{query}\n\n# Agent's progress so far (transcript up to the decision point)\n{prefix}\n\n# Decision point\nOption A:\n{candidate text}\n\nOption B:\n{candidate text}\n\nWhich option is the better technical decision?\nReturn exactly one line: ANSWER: X"
**Covers:** undecidable-filter example (p. 21) through Appendix B per-cell examples (pp. 21–22) and Appendix C evaluation protocol (p. 23)
