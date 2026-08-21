**Figure 5 – Technical Summary**

**What it shows.** A set of three five‑axis radar (spider) charts comparing the proposed method *GraphPlanner* against baselines across five task domains under the Phase‑2 protocol. The three panels isolate three different questions: (a) zero‑shot generalization to LLMs not seen in training, (b) an ablation of how historical interaction memory is encoded, and (c) transductive vs. inductive routing inference.

**Axes.**
- *Angular (categorical) axes:* five scenarios — **Math, Code, CS, WK, Popular**.
- *Radial axis:* a scalar performance score (accuracy‑like), with gridlines running from about **0.2 at the center to ~0.8 at the outer ring**. Larger area = better performance on that domain.
- *Legends per panel:* (a) GraphRouter, Router‑R1, GraphPlanner; (b) w/o History, Homo‑Graph, Hetero‑Graph, GraphPlanner; (c) Router‑R1, GraphPlanner‑Ind, GraphPlanner‑Trans.

**Trends.**
- In every panel the **GraphPlanner polygon is the outermost**, i.e., it attains the highest value on essentially all five domains, enclosing the competitors.
- Panel (a): GraphPlanner clearly dominates GraphRouter and Router‑R1 across Math, Code, CS, WK and Popular, with its advantage most visible on the "harder" domains (Code, CS, Math), where baselines pull in toward the center.
- Panel (b): removing history (w/o History) yields the smallest polygon; Homo‑ and Hetero‑Graph are larger, and full GraphPlanner is largest — indicating historical memory and its heterogeneous encoding help.
- Panel (c): GraphPlanner‑Trans (transductive) is the largest, beating both the inductive variant and the Router‑R1 baseline across the board.

**Takeaway.** GraphPlanner consistently achieves the best scores across all five scenarios in all three settings, supporting (i) robust zero‑shot transfer to unseen backbone LLMs, (ii) the value of retaining and heterogeneously encoding interaction history, and (iii) the benefit of transductive over inductive routing. The consistent area dominance, rather than wins on isolated axes, is the central message.

*(Exact axis tick values and vertex positions are read approximately from the chart.)*