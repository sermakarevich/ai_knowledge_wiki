**Figure overview.** The plot decomposes a model's gain on the *Pass@2* metric into three condition types, showing for each type both the distribution of individual contributions (gray scatter dots) and an aggregate estimate (colored horizontal bar with a vertical black interval). The headline — "Anti-patterns are the slice that pays" — is the central claim.

**Axes.**
- *Y-axis:* "Contribution to Pass@2 (pp)," i.e., percentage points, spanning roughly −30 to +40, with a reference line at 0.
- *X-axis:* three categorical groups — $R_p$ (rules), $R_n$ (anti-patterns), and $X$ (examples).

**Per-group reading (approximate).**
- **$R_p$ (rules):** tight cluster mostly within ±10 pp; aggregate bar is small and slightly positive (≈ +2–3 pp).
- **$R_n$ (anti-patterns):** widest, most prominent (green) aggregate bar sitting above zero (≈ +2–3 pp) and the most visible positive effect; scatter is wide, with notable positive outliers up to ≈ +40 pp and negatives down to ≈ −25 pp.
- **$X$ (examples):** aggregate bar essentially flat at ≈ 0 pp; scatter is broad and roughly symmetric, including strong negative outliers (≈ −25 to −30 pp).

**Trends.** All three groups show high per-instance variance (the black vertical intervals and the spread of dots), so individual contributions swing in both directions. What differentiates the groups is the *central/aggregate* effect: anti-patterns carry a clearly positive aggregate contribution, rules a small positive one, and examples a negligible (≈ zero) one. The relative thickness of the colored bars tracks this ranking, with the anti-pattern bar the most pronounced.

**Takeaway.** Despite large run-to-run noise, the net positive contribution to Pass@2 is attributable primarily to the anti-pattern ($R_n$) component rather than to explicit rules or plain examples; anti-patterns are the "slice that pays."