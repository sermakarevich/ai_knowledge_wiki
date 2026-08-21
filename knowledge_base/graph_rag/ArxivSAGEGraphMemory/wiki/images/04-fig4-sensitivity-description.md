**Figure 4 — Reader‑side sensitivity analysis (three bar‑chart panels).**

*What it shows:* A sensitivity study of frozen‑reader hyperparameters on two metrics, **reward** (cross‑hatched bars) and **Deducible** (diagonal‑hatched bars), each with approximate value labels.

*Axes:* Every panel uses a vertical **Mean** axis from 0.0 to 1.0. The horizontal axis enumerates the setting being swept in that panel (top‑k values, ranker variants, or on/off initial‑entity‑weight configurations). In each setting, reward sits slightly above Deducible.

*Panel trends (values approximate):*
- **Top‑k budget sweep (k = 3…80):** reward oscillates in a narrow band around ~0.6 (peaks near k = 5 and k = 40, dips near k = 10 and k = 60); Deducible stays flatter around ~0.51–0.53. The curve is non‑monotonic, so larger k does not monotonically help.
- **Ranker variants (idf+topk20 … idf+topk60):** both metrics are comparatively flat, reward ~0.60–0.63 and Deducible ~0.51–0.54, with the idf‑augmented topk20 settings at the high end and idf‑only/topk40/topk60 slightly lower.
- **Initial‑entity weight (on / off / off@10 / off@40):** "on" gives the highest reward (~0.64) and a mid‑range Deducible; "off" is clearly the lowest reward (~0.55); off@10 and off@40 recover to ~0.61 reward with Deducible ~0.53.

*Takeaway:* Reward and Deducible are insensitive to the exact ranker choice (broadly stable across variants), but the top‑k budget exhibits a non‑monotonic budget–noise trade‑off (more retrieval budget adds weakly related evidence and can dilute the reasoning chain), and turning the initial‑entity weight off is the most damaging change. Overall, the reader‑side settings have a moderate, non‑monotonic effect rather than a clean monotonic trend.