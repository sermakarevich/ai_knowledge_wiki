**Figure 5 — Impact of the number of poisoning text variants (Nₐ)**

**Type:** 2D line chart (multi‑series, with point markers).

**Axes / components:**
- **Y‑axis:** Attack Success Rate (ASR), plotted from roughly 60 to 100 (percent).
- **X‑axis:** "Number of Poisoning Text Variants per Relation Injection (Nₐ)," a non‑linear/categorical scale with ticks at 0, 1, 3, 5, and 10.
- **Four data series** (legend in the lower‑right): *MuSiQue* (blue), *Geographic* (red), *Medical* (orange), *Cybersecurity* (green), each a line connecting circular markers across the Nₐ values.
- A light grid aids reading.

**What it shows / trend:** All four curves rise steeply from Nₐ = 1 to Nₐ = 3 and then flatten. The *Cybersecurity* series starts highest and stays near the top (~98–99) across the range. The other three (Geographic, Medical, MuSiQue) begin in the low‑70s to high‑70s at Nₐ = 1, climb into the ~80–90s by Nₐ = 3, and then show only marginal increases at Nₐ = 5 and 10.

**Takeaway:** Adding poisoning text variants per relation injection boosts attack success, but with strong diminishing returns beyond about three variants — once the targeted relation is retrievable, extra variants add little, so Nₐ ≈ 3 is a near‑optimal cost/efficacy point.

*(The page also contains Table 3, "Impact of knowledge graph awareness," a results table comparing KG‑Aware vs. KG‑Agnostic settings across MuSiQue/Geographic/Medical/Cyber‑Security for GPT‑4o and Llama 3.1‑8B on ASR/QPP/TPQ; it is a data table rather than a flow diagram.)*