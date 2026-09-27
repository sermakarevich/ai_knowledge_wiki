> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# 6.4 Why does corpus-scope reflection win?

**In one sentence:** Corpus-scope reflection wins because it writes statistical rules from the whole rollout pool — frequency-counted errors, cross-episode duplicates, and corpus-level absences — in a single gateless pass that avoids validation-gate overfitting.

## Key points

- The chunk's explanation is reflection scope: three observations support that corpus-wide statistics, not minibatch anecdotes, explain the win.
- Statistical, not anecdotal rules: the telecom skill's top rule targets fabricated identity-lookup arguments seen in 16/50 episodes (32% frequency), which no single-minibatch reflection reliably surfaces and GEPA's telecom prompts never address.
- Efficiency rules need duplicate counts: detecting that 123 of 284 `get_details_by_id` calls were exact duplicates requires joining tool calls across the whole episode set — a one-liner in pandas but invisible in context-window reflection.
- No gate, no gate-overfitting: search methods keep an edit only if a small validation batch approves, which overfits small pools and inflates variance.
- The overfitting cost is concrete: GEPA-telecom-LD collapses to 17.5, SkillOpt retail variance reaches SD 10.1, while CASD's single pass has no acceptance step and variance across independently produced skills is small (SD ≤ 3.1 on 3 of 4 benchmarks).
- Figure 4 mechanism: a single test ticket has two independent root causes and reward is granted only if the target agent repairs both.
- The device-side cause is visible in any individual failed trajectory and all three optimizers encode a rule for it; the account-side cause appears only as an absence — a payment call no rollout ever makes — so only CASD writes a rule for it and only CASD solves the episode.

---

## 1. Rules are statistical, not anecdotal

The telecom skill's top rule targets fabricated identity-lookup arguments observed in 16/50 episodes. No single-minibatch reflection reliably surfaces a 32%-frequency error, and GEPA's telecom prompts never address it.

**Covers:** Section 6.4, observation (1)

## 2. Efficiency rules need duplicate counts

Detecting that 123 of 284 `get_details_by_id` calls were exact duplicates requires joining tool calls across a whole episode set — a one-liner in pandas, but invisible in a context-window reflection.

**Covers:** Section 6.4, observation (2)

## 3. No gate, no gate-overfitting

Search methods keep an edit only if a small validation batch approves, which both overfits small pools (Smith and Winkler 2006; Dwork et al. 2015) (GEPA-telecom-LD collapsing to 17.5) and inflates variance (SkillOpt retail SD 10.1). CASD's single pass has no acceptance step to overfit; its variance across independently produced skills is small (SD ≤ 3.1 on 3 of 4 benchmarks).

**Covers:** Section 6.4, observation (3)

## 4. Figure 4: corpus-level absences are invisible to minibatch reflection

Figure 4 makes the mechanism concrete on a single test episode. The ticket has two independent root causes, and reward is granted only if the target agent repairs both. The device-side cause is the kind of failure a minibatch reflection can see — it is visible in any individual failed trajectory — and all three optimizers encode a rule for it. The account-side cause is not: it appears in the corpus only as an absence, a payment call that no rollout ever makes, which is a statement about the whole pool rather than about any one episode it contains. Only CASD writes a rule for it, and only CASD solves the episode.

Verbatim caption from the chunk:

> Figure 4: Corpus-level absences are invisible to minibatch reflection. A τ2-telecom "no service" ticket requires repairing two independent root causes. Columns show the prompts distilled by the three optimizers from the same 50-rollout pool and the resulting agent behavior. The device issue is evident in individual trajectories and is captured by all methods. In contrast, the billing issue appears only as a corpus-level absence — make_payment is never invoked in the rollout pool. Only CASD identifies this missing behavior from corpus-level statistics and distills the required billing rule, whereas GEPA and SkillOpt omit it and fail the task.

**Covers:** Section 6.4 + Figure 4
