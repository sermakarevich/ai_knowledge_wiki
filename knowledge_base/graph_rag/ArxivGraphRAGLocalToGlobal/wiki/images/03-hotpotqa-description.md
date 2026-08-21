**Figure 3 — Technical Summary**

**What it shows:** A line plot measuring how many entity references are extracted from the HotPotQA dataset using a generic entity‑extraction prompt (GPT‑4‑turbo), as a function of two variables: text chunk size and the number of self‑reflection iterations applied.

**Axes:**
- **X‑axis:** Number of self‑reflection iterations performed (0 → 3).
- **Y‑axis:** Entity references detected (roughly 0 → 30,000).
- **Series:** Three chunk sizes — 600 (top line), 1200 (middle), 2400 (bottom) tokens.

**Trends:**
- At **0 iterations**, smaller chunks win: the 600‑token line starts highest (~10k), followed by 1200 (~7–8k) and 2400 (~6k). This reflects the LLM's tendency to extract fewer entities from larger chunks.
- As iterations increase, **all three lines rise** monotonically.
- The gap between chunk sizes **narrows with each iteration**: the 2400‑token line has the steepest climb, partially "catching up" to the 600‑token line. By iteration 3, the three lines have largely converged (≈ 20k–28k), with 600 still slightly ahead.

**Takeaway:** Self‑reflection is an effective remedy for the entity‑extraction deficit of large chunks. A few reflection passes both boost total entity recall across the board and substantially mitigate the quality loss from using larger (cheaper, fewer‑call) chunk sizes — letting one trade more self‑reflection iterations for larger chunks without the usual drop in extraction completeness.