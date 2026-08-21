**Figure 6 – Cross‑dataset (OOD) generalization heatmaps for two baselines.**

**What it shows.** Two 6×6 heatmaps, (a) Search‑R1 and (b) Graph‑R1, that report, per cell, the ratio of evaluation F1 to in‑training F1 (F1(train_eval)/F1(train_eval) × 100). A value of 100% means performance is unchanged on the target dataset; lower values quantify out‑of‑distribution (OOD) degradation when a model trained on one QA dataset is evaluated on another.

**Axes.** Rows and columns are the same six QA datasets (2Wiki, HipPOQA, Mutaice, NQ, PAQuA, TriviaQA). The diagonal therefore corresponds to in‑distribution (train‑dataset) evaluation, while every off‑diagonal cell is a cross‑dataset OOD transfer case. Color encodes the ratio: green ≈ high / near‑diagonal values, red/pink ≈ large OOD drops.

**Trends.**
- In both panels the diagonal is the greenest (highest) band, and performance falls off as you move away from it, confirming that both methods degrade on unseen datasets.
- Search‑R1 (a) shows a predominantly red off‑diagonal block – broad, consistent OOD drops across most target datasets.
- Graph‑R1 (b) has a visibly greener off‑diagonal region than (a), i.e., smaller drops on many cross‑dataset pairs, though several cells remain red (notable residual drops on a few pairs).

**Takeaway.** Outcome‑only retrieval‑augmented training (Search‑R1) overfits to dataset‑specific answer patterns, giving the worst average OOD ratio (≈70%). Introducing graph‑structured retrieval (Graph‑R1) meaningfully improves cross‑dataset transfer (average ratio ≈85–86%) by capturing more generalizable relational structure, but it still leaves non‑trivial OOD gaps on some dataset pairs. Both are substantially below the strongest method reported elsewhere (≈95–96%), so cross‑dataset generalization remains a key differentiator.