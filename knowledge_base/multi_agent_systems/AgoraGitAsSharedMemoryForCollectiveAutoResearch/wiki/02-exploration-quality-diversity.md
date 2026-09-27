> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Exploration, open-ended search, and quality diversity
**In one sentence:** Agora borrows exploration–exploitation, novelty search, quality-diversity, and POET intuitions as heuristics (not optimal-planning guarantees) for attention allocation over a Git-backed contribution DAG with evidence-weighted quality and diversity-aware views.
## Key points
- The exploration–exploitation trade-off is formalized by multi-armed bandits (Auer et al., 2002), with UCT applying bandit selection to tree search (Kocsis and Szepesvári, 2006).
- Novelty search abandons a single objective to avoid deceptive local optima (Lehman and Stanley, 2011), while MAP-Elites / quality-diversity methods seek diverse collections of high-performing solutions (Mouret and Clune, 2015; Pugh et al., 2016).
- POET jointly generates problems and solutions, transferring stepping stones between branches (Wang et al., 2019); Agora borrows these intuitions for attention allocation.
- Agora's graph is explicitly "neither a stationary bandit nor a game tree," so its suggestions are heuristics for surfacing underexplored branches, not a guarantee of optimal planning.
- A project state is a DAG 𝐺 = (𝑉, 𝐸) where edge (𝑢, 𝑣) means 𝑣 builds on 𝑢 (𝑢 is a Git parent of commit 𝑣); each node is 𝑣 = (ℎ, 𝑎, 𝑇, 𝑑, 𝑥, 𝑚, 𝑃, 𝜏) with commit hash, account, tags, description, metadata, optional metric, parent set, and server timestamp.
- Evidence score 𝑆(𝑢) is the weighted count of what other accounts built on it (self-citations excluded via 1[𝑎(𝑢) ≠ 𝑎(𝑣)]), with tag weights +5 for setup/result/insight/hypothesis/report, +20/+10/−20 for verification (confirmed/partial/failed), and 0 for endorsed/wip; the newest verification verdict replaces the old one's effect.
- Diversity-aware attention exists because "a leaderboard is a good exploitation signal and a poor map": analyze returns metric leaders, most built-on nodes, leaves, underexplored/unverified/contested results, open hypotheses, activity, tags, and contributors, plus single-link clusters (≥50% embedding coverage, cosine threshold 0.90 default, capped at 5,000 most recent contributions) with cluster counts, top-cluster share, entropy-based effective count, evenness, metric histogram, and a small-cluster frontier.
---
## Exploration, open-ended search, and quality diversity (related work)
The chunk states the lineage in one paragraph: multi-armed bandits formalize exploration–exploitation (Auer et al., 2002); UCT applies bandit selection to tree search (Kocsis and Szepesvári, 2006); novelty search shows abandoning a single objective can avoid deceptive local optima (Lehman and Stanley, 2011); MAP-Elites and quality-diversity seek diverse collections of high-performing solutions (Mouret and Clune, 2015; Pugh et al., 2016); POET jointly generates problems and solutions, transferring stepping stones between branches (Wang et al., 2019).
Verbatim caveat: "Agora borrows these intuitions for attention allocation, but its graph is neither a stationary bandit nor a game tree, and its suggestions are heuristics for surfacing underexplored branches, not a guarantee of optimal planning."
## 3. Agora: A Git-Backed Research DAG — 3.1 Problem setting and design goals
A project has participants 𝒜 and a growing sequence of contributions 𝑉. A contribution may carry code or data artifacts, a description, optional metric values, tags, and a set of parents. At any moment the platform should answer four questions:
1. What has been tried, including failures?
2. Which claims have independent support or conflict?
3. Where is the current frontier, including neglected alternatives?
4. What exact artifact and lineage produced a reported result?
Verbatim framing: "Agora is a coordination substrate, not a lab manager. Projects define their own instructions, metrics, artifact contracts, and safety boundaries; the platform supplies the shared mechanisms for publishing and finding work and does not pretend one scoring rule fits every field."
Table 1 (design goals and Agora mechanism):
| Goal | Failure without a shared institution | Agora mechanism |
|---|---|---|
| Durable memory | Session-local discoveries and negative results disappear. | Append-only Git commits with explicit parent lineage and searchable metadata. |
| Frontier visibility | Workers guess what is open and duplicate the same branch. | Leaf, hypothesis, verification, cluster, and metric-landscape views. |
| Evidence quality | Votes reward popularity; self-citation and repeated endorsement are cheap. | Independent follow-on work, replaceable verification verdicts, and self-citation exclusion. |
| Search diversity | A leaderboard concentrates all workers on one local basin. | Semantic clusters, diversity summaries, frontier candidates, and separate exploit/explore slots. |
| Auditability | A scalar score loses the configuration and code that produced it. | Content-addressed artifacts, canonical commits, immutable revisions, and rebuildable contribution indexes. |
## 3.2 Contribution graph and provenance
State is a directed acyclic graph 𝐺 = (𝑉, 𝐸); for 𝑢, 𝑣 ∈ 𝑉, edge (𝑢, 𝑣) ∈ 𝐸 means 𝑣 builds on 𝑢. Each node stores:
𝑣 = (ℎ, 𝑎, 𝑇, 𝑑, 𝑥, 𝑚, 𝑃, 𝜏) — (1)
where ℎ is canonical commit hash, 𝑎 publishing account, 𝑇 tag set, 𝑑 description, 𝑥 structured metadata, 𝑚 optional project metric, 𝑃 parent set, 𝜏 server timestamp. Code-bearing contributions carry the full repository state; because identity is a hash and parentage is Git parentage, history is append-only and acyclic by construction.
Verbatim system fact: "Git is the only state the system depends on: the SQLite index that answers queries, the analyze views below, and every figure in this report are derived from the Git history and can be rebuilt from it." Participants publish through a CLI or HTTP API and "never share a filesystem, model, or conversation (Figure 1)."
Figure 1 summary: per-project Git holds canonical artifacts; SQLite holds the derived query index; analyze/search/clusters/UCB read from it; participants see a "Ranked frontier: exploit · explore known · explore novel"; no central planner assigns work.
Contribution vocabulary: tags give contributions shared meaning without a rigid ontology; reserved tags carry validation/scoring behavior. Light publication path (metadata-only): client sends JSON, server creates canonical commit. Heavy path (code-bearing): participant commits locally, uploads a Git bundle, server validates before creating a canonical server-timestamped commit. Both yield the same node kind. A project starts with `agora init` (setup contribution); the loop is: analyze, pick a parent, run locally, publish, analyze again.
Table 2 (reserved contribution types; weights applied to a direct parent when the child comes from another account):
| Tag | Weight | Role | Key rule |
|---|---|---|---|
| setup | +5 | Initial project files and instructions. | Commit zero; no project metric. |
| result | +5 | Experimental outcome with optional artifacts and metric. | Successes and failures alike. |
| insight | +5 | Interpretation, pattern, or cited observation. | Parents identify the evidence being synthesized. |
| hypothesis | +5 | Concrete untested proposal. | May not present a metric value as if already tested. |
| report | +5 | Human-readable synthesis across contributions. | Cites the nodes from which conclusions are drawn. |
| verification | +20 / +10 / −20 | Confirmed, partial, or failed reproduction. | Exactly one target; never one's own work. |
| endorsed | 0 | Acknowledgement after inspection. | Visible, but excluded from fitness. |
| wip | 0 | In-flight work, to reduce duplication. | Visible, but does not propagate score. |
Quality from downstream evidence: with 𝑤(𝑣) the tag weight and 𝑎(𝑣) the author, evidence score is:
𝑆(𝑢) = ∑_{𝑣:(𝑢,𝑣)∈𝐸} 1[𝑎(𝑢) ≠ 𝑎(𝑣)] 𝑤(𝑣). — (2)
A separate descendant count tracks qualifying downstream work reachable from 𝑢; endorsements, work in progress, and failed verifications do not add to it. Self-citation exclusion stops a worker from manufacturing impact by extending its own branch. If a verifier changes its verdict, the newest verdict replaces the old one's effect; both commits stay in history. Verbatim: "The score is not a truth signal. It encodes a narrower claim: work that others have reproduced or built on is more actionable than work that has only been voted for."
## 3.3 Diversity-aware attention allocation (partial in this chunk)
Verbatim diagnosis: "A leaderboard is a good exploitation signal and a poor map. It pulls every worker toward the same parent, hides negative results, and makes a saturated basin look like progress." The analyze call therefore returns several views at once: metric leaders, most built-on nodes, leaves, promising but underexplored results, unverified results, contested verifications, open hypotheses, recent activity, tags, and contributors.
Once embeddings cover enough contributions, the service adds single-link clusters over descriptions and reports cluster count and sizes, top-cluster share, an entropy-based effective cluster count, evenness, a metric histogram, and a frontier of promising nodes in small clusters. Exact parameters: clustering requires at least 50% embedding coverage, uses a cosine threshold of 0.90 by default, and caps pairwise analysis at the 5,000 most recent contributions.
Candidates are ranked by a diversity-aware upper-confidence bound "in the spirit of bandit and tree-search selection rules (Auer et al., 2002; Kocsis and Szepesvári, 2006)": 𝑈(𝑣) = 100𝑄(𝑣) + 𝐶√(log(𝑁+1)/(𝑛(𝑣)+1)) + √(100𝐷/(1+𝜌(𝑣))) — (3) (equation truncated at chunk boundary).
**Covers:** Related-work paragraph on exploration / open-ended search / quality diversity + Sections 3–3.3 up to Eq. (3) UCB ranking (chunk truncates mid-equation)
