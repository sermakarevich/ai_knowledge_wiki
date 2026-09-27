> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: What's Next After RLHF? — Diogo Almeida, TypeSafe AI

This note judges the talk's argument on its own terms, using only the digest
and wiki page for this paper. RLHF here means Reinforcement Learning from
Human Feedback: training models to match what human raters prefer. RLVR means
Reinforcement Learning with Verifiable Rewards: training against checks with
right answers, like tests or math proofs.

## Claims vs. evidence

- Claim: today's models are great at assistance but bad at automation because
  RLHF (human-preference training) keeps a human in the loop by design.
- Evidence offered: vivid but anecdotal — the fart-audio "eerie vibe" story,
  the "do not use AI for high-stakes decisions" business pattern, and the
  SaaS-unchanged-since-2019 observation. Plausible, but no numbers or studies.
- Claim: roughly "100% of LLMs" by usage are RLHF-trained, so overpromising
  is a feature, not a bug. This is stated as fact, without usage data or a
  definition of what counts as RLHF versus later fine-tuning mixes.
- Claim: benchmark success (hard tasks solved) coexists with automation
  failure (easy tasks still need humans). The puzzle is real, but the talk
  resolves it by definition — pleasing tasks succeed, removal-of-human tasks
  fail — which risks circular reasoning rather than a testable mechanism.
- Claim: Claude Code still belongs to the assistance era because it is "still
  RLHF." No training details or comparisons are given, so this reads as
  assertion awaiting the promised later justification.
- Claim: a third post-training way beyond RLHF and RLVR enables calibrated
  decision-making. No method, results, or API (Application Programming
  Interface) shape is shown in this chunk — it is a pitch, not evidence.

## Genuinely new vs. repackaged

- Genuinely sharp: the assistance-vs-automation divide as a lens on the two
  "cults" (AI going insanely well vs. insanely poorly). It explains the
  paradox better than vibes or bubble talk alone.
- Genuinely sharp: preference-vs-results gap — when uncertain, a
  preference-trained model picks what pleases over what is true. The
  engagement endgame framing is a useful warning for product design.
- Repackaged: "RLHF causes sycophancy and hallucination" is a known critique;
  the GAN (Generative Adversarial Network) asymmetry analogy for confident
  mode-dropping restates familiar reward-model over-optimization arguments.
- Repackaged: "SaaS plus a latched-on chatbot is not automation" and the
  just-in-time versus smarter-software contrast echo standard
  copilots-vs-agents discourse, with new branding.
- Unclear: the "third way" versus RLVR. RLVR already targets correctness over
  pleasing; calibration (knowing when you are uncertain) is often framed as
  an extension of it, so novelty cannot be judged from this chunk.

## Weaknesses and blind spots

- Single-chunk basis: the digest covers only the opening chunk, so claims
  flagged "I will justify later" cannot be checked here.
- No counter-evidence: agentic coding tools do complete multi-step tasks
  unsupervised; B2B (Business to Business) pilots do automate real workflows.
  The talk's binary sorting of these as "still assistance" needs criteria.
- Missing alternatives: pre-training limits, data quality, tooling, evals
  (evaluations), costs, and liability get little weight; everything is
  attributed to post-training choice.
- Speaker-credential noise: the transcript chunk renders the name as "Tiago
  Almeida" while the paper title says Diogo Almeida — a flag to verify
  identity and the "invented post-training" claim before citing.
- Survivorship framing: NLP (Natural Language Processing) benchmarks "getting
  crushed" is used for cult one, but benchmark contamination and saturation
  are not discussed.

## Applicability

- Use the assistance/automation test before buying or building: if success
  means "the user felt helped," preference-tuned models are fine; if success
  means "correct action with no human watching," demand calibration, abstention,
  cost-aware policies, and audit trails.
- Do not copy the "costs onto the user" pattern (flooding users with docs or
  drafts to review). For internal platforms it just moves toil around.
- Treat "smarter software" as a design prompt: change affordances and
  guarantees (permissions, undo, verification steps), not just generate the
  same code faster.

- **Relevance to my work**
  - AI/ML engineering: add calibration evals alongside correctness — measure
    abstention quality, confidence-vs-accuracy curves, and cost of wrong
    autonomous actions, not just pass@k or preference win-rates.
  - Agentic systems: gate autonomy by stakes — low-stakes steps run freely,
    high-stakes steps require checks, simulations, or approval; log every
    autonomous decision with inputs, confidence, and rollback path.
  - Elisity data platform: do not let assistants make access-policy or
    segmentation decisions on pleasing behavior; require verifiable rules,
    deterministic checks, and human-readable explanations before any
    network or identity change is applied.

## What this changes

- Changes how I scope demos: a great chat demo is weak evidence for
  unsupervised automation; I will ask for unattended-run metrics instead.
- Changes what I measure: preference scores and chat satisfaction go down in
  weight; calibrated autonomy (right action, right abstention, bounded cost)
  goes up.
- Does not change the stack yet: without the third method's details, there is
  nothing concrete to implement — only a sharper checklist for vendor claims.

## Verdict

Useful framing, weak proof, heavy pitch. The assistance-vs-automation divide
and the engagement-vs-calibration warning are worth keeping as review lenses,
but the talk in this chunk asserts more than it shows about Claude Code, RLVR,
and the promised third way. Revisit when method or metrics appear.

**watch**
