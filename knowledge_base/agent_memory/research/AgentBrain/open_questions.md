# Open questions — agent_memory / AgentBrain

Focus: Which of these 20 agent second-brain GitHub projects are worth using for a system that captures sources, connects ideas, remembers context, and helps agents act on it, and how do they compare across capture, linking, memory/recall, and agentic action?

Seed note: each question below names its parent sub-topic. A re-run may add one sub-topic per question. No question is answered by the current digests.

## Questions

1. Which capture lanes handle image-only PDFs and scanned documents (OCR), and which silently fail at ingest?
   - Sub-topic: 01-capture-ingest-lanes
   - Why it matters: the focus requires capturing arbitrary sources; Chubbyskills is text-layer-only per its digest, and DocMason's renderer stack is unverified at code level, so "worth using" for paper/scan-heavy flows cannot be decided without this answer.

2. Which capture lanes work fully offline, and what exactly breaks when the network or API key is missing?
   - Sub-topic: 01-capture-ingest-lanes
   - Why it matters: every lane claims local-first with opt-in cloud edges (Deepgram transcription, Jina Reader/Translate, group sync), but OpenWiki's default-on exceptions and each lane's dependency-gated paths mean offline-worthiness — a core "worth using" criterion — is still unknown.

3. Human-gated keep (popup/queue) vs. agent-classified capture vs. build-validated publish: which loses the least and noises the most?
   - Sub-topic: 01-capture-ingest-lanes
   - Why it matters: comparing capture across the 20 projects reduces to this keep-decision tradeoff (OpenWiki popup, AgentSecondBrain classification, DocMason validation gates); without loss/noise figures the capture ranking is guesswork.

4. Persistent typed graph vs. ledger-plus-links vs. ephemeral suggestions: which linking shape gives agents the best recall per unit of maintenance?
   - Sub-topic: 02-linking-kg-wiki
   - Why it matters: the linking comparison hinges on graph weight (Swarmvault/SageWiki persistent graphs vs. ClaudeObsidian ledgers vs. VaultCurate suggestion-only); the digests describe the shapes but not which one an agent should pay for.

5. Which freshness/staleness model actually prevents stale answers — bi-temporal invalidation, decay scoring, Hot/Cold tiering, or lint — and at what upkeep cost?
   - Sub-topic: 02-linking-kg-wiki
   - Why it matters: every linking source models time differently (`as_of` queries, half-life decay, link-plus-recency tiers, UTC lint); "remembers context" depends on picking one, and the digests give no comparative effectiveness or maintenance burden.

6. How accurate is entity resolution and dedup in each linking approach, and how much human review does it demand?
   - Sub-topic: 02-linking-kg-wiki
   - Why it matters: identity handling ranges from opt-in keep/fold/drop passes with no-fold rules (SageWiki) to synonym lists (VaultCurate) to frontmatter aliases (ClaudeObsidian); without accuracy-vs-review-burden data, "connects ideas" cannot be compared.

7. How do the six memory/recall substrates rank on a shared harness, given current numbers are vendor-reported or absent?
   - Sub-topic: 03-memory-recall-substrate
   - Why it matters: only OpenViking (LoCoMo), Hindsight (LongMemEval), and Agentmemory (snapshot R@5) report figures, with version discrepancies, while TencentDB, MemU, and OpenSecondBrain report none; a like-for-like comparison is required to answer which substrate is worth using for recall.

8. LLM-on-every-path vs. embedding-only service vs. keyless BM25 with opt-in upgrades: what is the latency/cost/quality tradeoff for recall?
   - Sub-topic: 03-memory-recall-substrate
   - Why it matters: Hindsight requires an LLM per recall, MemU forbids LLM calls in-service, Agentmemory runs keyless BM25 by default; the digests note the split but not what each choice costs or buys, which decides the "remembers context" substrate pick.

9. What is the minimal viable scoping/governance (ACLs, banks, subtrees, visibility boundaries) for single-owner vs. team use, and what overhead does each add?
   - Sub-topic: 03-memory-recall-substrate
   - Why it matters: governance ranges from TencentDB/OpenSecondBrain ACLs and hash chains to MemU/Agentmemory simplicity; "worth using" differs for a solo vault vs. a shared team brain, and the digests give shapes without overhead or breach-resistance evidence.

10. Which agentic harness reliably completes outward-effect tasks (send, publish, share, destructive calls), at what success rate and latency?
    - Sub-topic: 04-agentic-action-harness
    - Why it matters: none of the five action digests reports task-success, latency, or recall-precision figures — claims are structural only; "helps agents act on it" cannot be ranked without measured outcomes.

11. Opt-in verification (V-model, test lanes) vs. always-on governance (Tool Guard, contradiction demotion): what is the false-block vs. miss rate of each?
    - Sub-topic: 04-agentic-action-harness
    - Why it matters: the action comparison turns on approval/verification posture (CogSecondBrain/RowBot opt-in vs. MateClaw/SecondBrainCloudflare always-on); without error-rate and friction data, the safety-vs-velocity choice behind "worth using" is undecided.

12. For each deployment shape — local-first desktop, self-hosted runtime, user-owned cloud worker, zero-server markdown plugin — what does adoption and operation actually cost (setup, secrets, multi-user, sharing)?
    - Sub-topic: 04-agentic-action-harness
    - Why it matters: the five harnesses split across RowBot local desktop, MateClaw JAR/Docker/Postgres, SecondBrainCloudflare Worker (D1/Vectorize/AI/KV), and file-only plugins; total cost of ownership and private-by-default vs. team-sharing behavior determine which of the 20 an operator should actually adopt.
