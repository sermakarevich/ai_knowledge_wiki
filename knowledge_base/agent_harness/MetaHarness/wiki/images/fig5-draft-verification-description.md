**Figure 5 — Draft‑verification classification harness (control‑flow diagram).** This is not a quantitative plot; it has no axes or trends. It is a node‑and‑arrow flow diagram depicting a two‑call inference procedure for online text classification.

**What it shows / flow.**
- **Entry:** a single root node, *Query + memory* (the query plus a growing memory of past labeled examples), which fans out into two branches.
- **Branch 1 (left, draft):** *Retrieve top‑5 similar examples* → *Draft call*, which emits an initial label *D*.
- **Branch 2 (right, verification):** *Retrieve confirmers (label = D) and challengers (label ≠ D)* → *Verification call*, which either keeps or revises *D*.
- **Key dependency:** an arrow labeled *D* runs from the *Draft call* node into the *Retrieve confirmers/challengers* node, i.e., the second retrieval is **conditioned on the draft prediction**, not just the raw query.
- **Convergence:** both the *Draft call* and the *Verification call* feed into a single terminal node, *Final label*.

**Takeaway.** The harness turns a single prediction into a cheap two‑step procedure: a short‑context draft call proposes *D*, then a second short‑context call retrieves evidence both *for* and *against* *D* and issues the final answer. Because the second retrieval depends on *D*, it can surface counterexamples targeted at the model's current guess rather than only generic near‑neighbors, improving verification at low context cost (two model invocations with short retrieved contexts).