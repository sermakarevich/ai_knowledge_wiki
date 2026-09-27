**Figure 3 — Rubric judge vs. baseline judge (two panels).**

The figure compares a per‑task *rubric* prompt judge against a simpler *baseline* prompt judge (both run on a Codex GPT‑5.5 model, judging rollouts from Claude, Codex, and Faraday). Each dot/point corresponds to one task (SMOTE, A3C, LSTM, LeNet, ICL, Gato, Deep‑nets, AI‑Sci, VAE, ELM).

**Left panel — agreement (Kendall τ).**
- *Y‑axis:* rank agreement, Kendall τ (≈ −0.2 to 1.0; +1 identical ordering, −1 reversed).
- *X‑axis:* six pairwise comparisons — Human vs human, Rubric vs rubric, Baseline vs baseline, Rubric vs humans, Baseline vs humans, Rubric vs baseline — shown as violin/bee‑swarm plots with a central line.
- *Trend:* self‑consistency (judge vs. itself on repeated draws) is highest, with the rubric judge most consistent (≈ 0.6–0.7) and the baseline somewhat lower (≈ 0.4–0.5). Cross‑comparisons are lower, and the key contrast is that the rubric judge agrees with human rankings noticeably better than the baseline does (rubric‑vs‑humans ≈ 0.4–0.5 vs. baseline‑vs‑humans ≈ 0.1–0.2). Two humans themselves agree only moderately (≈ 0.3).

**Right panel — noise vs. averaging.**
- *Y‑axis:* fraction of within‑group score variance attributable to judge noise (≈ 0 to 0.5).
- *X‑axis:* number of judge samples averaged per rollout, *m* (1 to 8).
- *Two curves* with ±1 SEM bands: baseline (gray) and rubric (purple). Both fall monotonically as *m* increases (more averaging → less noise), but the rubric curve sits below the baseline at every *m* — roughly ≈ 0.25 vs. ≈ 0.4 at *m* = 1, converging to ≈ 0.05 vs. ≈ 0.1 at *m* = 8.

**Takeaway:** the rubric‑based judge is both more aligned with human preference and intrinsically less noisy than the baseline judge, so it reaches a given noise level with far fewer samples (about three rubric samples ≈ eight baseline samples). This makes it a more reliable reward signal for GRPO. (Caveat noted in text: a few tasks still show rubric‑human disagreement, leaving room for improvement.)