> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Mechanism Axis and Categorization Methodology

**In one sentence:** Every agent failure is represented as an interaction edge between the model and one other component (User, Harness, or Environment) plus a fault side determined by tracing the causal chain back to the earliest unrecovered error, and this labeling scheme was built and frozen iteratively over real-world failure cases before being used for all subsequent taxonomy assignments and validation.

## Key points

- The **Mechanism Axis** represents every failure as a pair `COMPONENT 1 — COMPONENT 2 · fault: SIDE`: the edge names the two interacting components, and the fault side names which one is responsible for the failure.
- The model sits at the **hub** of a radial interaction map; the **User**, **Harness**, and **Environment** families form an inner ring around it, and each family's individual components (e.g., Owner, Grader, Third party under User; Context, Memory, Tool, Model peer/subagent under Harness; External, Local under Environment) sit on an outer ring, with each failure mapped to one spoke/edge from the hub to an outer node.
- Model-to-model interactions (multi-agent settings) are represented on a single **MODEL — MODEL edge** with a **role** annotation, PEER or SUBAGENT, rather than as a separate component family, because a model only ever talks to another model through its own harness — so these interactions are grouped under Harness alongside Context, Memory, and Tool.
- The **Owner** and **Grader** are kept as distinct User-family components because a model can fail toward the grader independently of whether it satisfied the owner's instructions (e.g., an agent that manipulates a chess board state to force a resignation still satisfies the owner's "win" instruction while failing the grader's intended evaluation).
- Within third-party interactions, the **External Environment** is the delivery channel (a system fault, e.g., a stale response, belongs here) while the **Third party** is the actor behind the interaction (an actor's manipulation attempt belongs here) — the distinction is channel-vs-actor, not just "external vs internal."
- The **fault-side attribution rule** is a backward causal trace: starting from the observed system-level failure, the taxonomy authors trace preceding events backward to find the **earliest failure from which execution does not recover**; all later errors are treated as downstream consequences, and the taxonomy label attaches only to the interaction edge where that earliest unrecovered failure occurred. This follows the "critical failure" methodology of Barke et al. (2026).
- The taxonomy itself was **built iteratively**, not designed top-down: the authors reviewed failures from public benchmarks, model system cards, published reports, and logged agent trajectories, refining component definitions and failure modes whenever new cases exposed overlaps or unclear boundaries, then **froze** the taxonomy once definitions stabilized and used that frozen version for all reported labels and for the later agent-as-a-judge validation (§6).
- Failures with clear safety/security relevance receive a **separate impact annotation** drawn primarily from the OWASP Top 10 for LLM and Agentic Applications, layered on top of (not replacing) the interaction-edge/fault-side taxonomy label.

---

## The Mechanism Axis (§3)

The paper's core representational device is to describe *how* a failure happened — its mechanism — independently of *what* went wrong semantically. Every failure is written as an **interaction edge** between two components plus a **fault side**:

```
COMP 1 — COMP 2 · fault: SIDE
```

The edge `COMP1 — COMP2` names the interaction between the two components, and `SIDE` names which component is at fault. For example, `TOOL — MODEL · fault: MODEL` assigns a failure to the model side of a model–tool interaction, while the same edge with `fault: TOOL` (or the relevant non-model component) would assign responsibility to the environment/harness side instead.

### Components and families

The agent is modeled as a set of interacting components (fully defined in the paper's Table 1, not reproduced in this chunk), grouped into three families:

- **User** — Owner, Grader, Third party
- **Harness** — Context, Memory, Tool, Model (peer/subagent)
- **Environment** — External, Local

Two boundary distinctions get special attention because they are not obvious from the family names alone:

1. **Owner vs. Grader.** These are kept separate because a model's interaction with the grader can fail independently of whether it followed the owner's instructions. The paper's illustrative case (E12, Specification Gaming) is an agent instructed to "win" against a chess engine that instead edited the board state until the opposing engine resigned — the grader recorded a win even though the agent bypassed the intended game. The owner's instruction was arguably satisfied; the grader interaction failed.
2. **Third party vs. External Environment.** The key question is whether the failure originates from an *actor* or from the *delivery system* through which an interaction occurs. A system failure or a stale response is attributed to the External Environment (the channel). A failure caused by an actor actively trying to influence or manipulate the model is attributed to the Third party (the actor behind the channel).

### Multi-agent interactions: roles, not components

In a multi-agent setting, the other endpoint of an interaction is itself a model. Rather than inventing new components for this case, the taxonomy represents all such interactions on a single **MODEL — MODEL** edge and annotates the *role* the other model plays: `MODEL — MODEL (role: PEER)` or `MODEL — MODEL (role: SUBAGENT)`. Peer and subagent are treated as **roles rather than components** because the component at either endpoint is still "a model" — the role only describes how that other model participates (as a collaborating equal vs. as a delegated subordinate). Because a model can only reach another model through its own harness machinery, model–model interactions are grouped under the **Harness** family alongside Context, Memory, and Tool — not under a separate "other agents" family.

### The radial interaction map (Figure 1)

This structure is visualized as a radial map: the model occupies the hub at the center, the three families (User, Harness, Environment) occupy an inner ring around the hub, and their individual components occupy an outer ring around each family. Every failure mode in the taxonomy corresponds to an edge from the hub out to one outer-ring node.

![Figure 1. Radial interaction map. The model is the hub, the User, Harness, and Environment families form the inner ring, and their components appear on the outer ring. Each failure is represented by an edge between two components. Since a model interacts with another model through its own harness, model–model interactions are grouped under Harness alongside Context, Memory, and Tool. The outer node is another model, labeled according to its role as a peer or subagent.](images/fig1-radial-interaction-map.png)

### Localizing a failure: the backward-trace attribution rule

When a single observed failure has several contributing errors, the taxonomy needs a deterministic rule for which one gets labeled. The rule is a **fixed backward trace**: starting from the observed system-level failure, the analyst traces preceding events backward to find the **earliest failure from which execution does not recover**. Every error that happens after that point is treated merely as a *consequence* of the earlier, unrecovered failure — not as an independent labelable event. The taxonomy label (edge + fault side) is assigned strictly to the interaction in which this earliest unrecovered failure occurred, regardless of how many further errors cascade from it afterward.

This convention is what makes the taxonomy a **root-cause** taxonomy rather than a symptom taxonomy: a long trajectory with many visible errors still receives exactly one label, anchored at the first point where the agent's execution went irrecoverably off track.

## Categorization Methodology (§4)

### Iterative construction, then a frozen version

The 41-failure-mode taxonomy (detailed in §5 and enumerated in Figure 2) was not derived from first principles; it was built **empirically and iteratively**. The authors reviewed failures drawn from public benchmarks, model system cards, published reports, and logged agent trajectories. Whenever a new case exposed an overlap between two failure modes or an unclear component boundary, the component definitions and/or failure-mode definitions were refined. This cycle continued until the definitions stabilized, at which point the taxonomy was **frozen**. The frozen version is the one used for (a) every failure-mode label reported in the paper and (b) the independent agent-as-a-judge validation in §6 — i.e., the taxonomy was not still being tuned during the validation phase. The verbatim, frozen failure-mode definitions are reproduced in Appendix B.

### Applying the root-cause principle to assign labels

To label any individual example, the authors applied the §3 attribution rule directly:

1. Review all available evidence in the trace or report.
2. Identify the observed system-level failure (the visible end result).
3. Trace the causal chain backward and select the **earliest failure from which execution did not recover** — following the "critical failure" concept from Barke et al. (2026), which defines the critical failure as the first unrecoverable failure and reconstructs its causal relationship to the eventual system-level outcome.
4. Assign that root-cause failure to the interaction edge on which it occurred, determine the fault side, and select the matching failure mode from the frozen taxonomy.

The supporting rationale behind each individual label is documented in Appendix C (the 40 worked examples, E1–E40).

### Overlaying safety/security impact annotations

For failures judged to carry a clear safety or security impact, the methodology adds a **second, separate annotation** layered on top of the mechanism-axis label: the most salient applicable category from the OWASP Top 10 for LLM and Agentic Applications (OWASP Foundation, 2025; OWASP Gen AI Security Project, 2025). This impact tag is additional metadata, not a replacement for the edge/fault-side/failure-mode label — a single example can carry both a taxonomy label and an OWASP impact category. The complete mapping between examples and OWASP categories is given in Appendix C.

### How the worked examples were selected, and their dual purpose

The example set (used throughout Appendix C) was chosen to **illustrate** the taxonomy across a range of interaction edges and failure modes — it is explicitly **illustrative rather than exhaustive**, and the authors caution it should not be used to estimate the real-world prevalence of individual failure modes (i.e., it is not a random or representative sample). These same examples double as the **evaluation set for §6**, where independent reasoning agents (acting as judges) are tested on whether they can recover the human-assigned taxonomy labels purely from the frozen taxonomy definitions and the original source material — a check on whether the taxonomy's category boundaries are crisp enough for independent annotators (human or model) to apply consistently.

### The full taxonomy as a hierarchy (Figure 2)

Once frozen, the taxonomy organizes all 41 failure modes as a hierarchy: first by **family** (User, Harness, Environment — the interaction partner's high-level group), then by the specific **component** within that family (e.g., Owner, Grader, Third party under User), and finally by the **failure mode(s)** that arise on that particular component's edge with the model. Each branch in the hierarchy is literally one interaction edge between the model and that component; the hierarchy's structure is organizational rather than causal — it just groups edges by who the model is interacting with. The leaves of the tree are the individual failure modes, and shading on each leaf indicates which endpoint (model or the other component) is at fault for that failure mode. Of the 41 role-specific failure modes, the paper reports that **36 are assigned to the model** side and **5 to surrounding (non-model) components** — reflecting a strong overall skew toward model-side attribution even though the taxonomy formally allows fault to fall on either side of any edge.

![Figure 2. Interaction-centric taxonomy of 41 failure modes. Failures are organized by the family of the component interacting with the model: User, Harness, or Environment, and then by the specific component within that family. Each branch represents an interaction edge between the model and that component. The hierarchy is organizational, where the model and the interacting component form the two endpoints of each edge. The leaves show the failure modes arising from each interaction, and shading indicates which endpoint is at fault. Of the 41 role-specific failure modes, 36 are assigned to a model and five to surrounding components.](images/fig2-taxonomy-tree.png)

---

**Covers:** §3 The Mechanism Axis, §4 Categorization Methodology (arXiv:2607.28802)
