> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Satisfaction Matches the Base — Only the Policy-Aware Gate Helps
**In one sentence:** Satisfaction ratings are uninformative about task success because the satisfied-but-failed rate (57.5%) matches the base failure rate (57.3%), and only the policy-aware gate that checks whether the task resolved halves failure risk and discriminates success.
## Key points
- The human panel rated 57.5% of satisfied (≥5/7) conversations as failed, statistically indistinguishable from the stratified sample's own 57.3% base failure rate.
- Conditioning on satisfied does not lower failure, so satisfaction is uninformative rather than merely weak, with transcript-level AUC 0.44.
- The policy-aware gate roughly halves failure risk: 20.0% of gate-accepted conversations fail against a 40.2% base rate on the natural task mix, with AUC 0.73.
- The process-blind proxy, which never sees tool calls or task, behaves like satisfaction not the gate: 32.7% vs. 40.2% base, AUC 0.49.
- Separating these two signals — one uninformative (proxy/satisfaction) and one informative (policy-aware gate) — is the core contribution of this work.
- The panel result is robust to dropping any single annotator (56.4–60.5% leave-one-annotator-out).
- The satisfied-but-failed rate is concordant across five rater populations (human panel plus gate and proxy scorings from two LLM providers; 47.6–59.5%).
- The gap reflects subjective approval in general: all five subjective dimensions (satisfaction, respect, clarity, perceived helpfulness, would-return) are decorrelated from success (|ρ| ≤ 0.17), with overall ρ = −0.147.
---
## Table 2: what is compared
**Covers:** Table 2 scope — per-signal satisfied failure rate vs. pool base rate, relative risk (RR), and AUC

For each signal: the failure rate among the conversations it rated satisfied, the pool's own base failure rate, their ratio (relative risk, RR), and transcript-level discrimination (AUC). The human panel is a stratified sample (base 57.3%); the grid signals use the natural task mix (base 40.2%).

## Uninformative, not merely weak
**Covers:** Table 2 central finding — 57.5% vs. 57.3%, AUC 0.44; gate 20.0% vs. 40.2%, AUC 0.73; proxy 32.7% vs. 40.2%, AUC 0.49

Concretely, 57.5% of the conversations the panel rated satisfied (≥5/7) had failed the task. Interpreted against the base rate, the 57.5% satisfied-but-failed rate is statistically indistinguishable from the stratified sample's own 57.3% base failure rate: conditioning on satisfied does not lower failure, so satisfaction is uninformative rather than merely weak, and at the transcript level it does not discriminate success (AUC 0.44).

By contrast, the policy-aware gate assesses whether the task resolved: it roughly halves failure risk (20.0% of gate-accepted conversations fail against a 40.2% base rate on the natural task mix) and discriminates success (AUC 0.73; per-score calibration in Appendix C.1).

The process-blind proxy, which never sees the tool calls or task, behaves like satisfaction, not the gate (32.7% vs. 40.2%; AUC 0.49). Separating these two signals, one uninformative and one informative, is the core contribution of this work.

## Robust across raters, annotators, and domains
**Covers:** leave-one-annotator-out 56.4–60.5%; five rater populations 47.6–59.5%; per-domain satisfied-but-failed rates

The panel result is robust to dropping any single annotator (56.4–60.5% leave-one-annotator-out; Appendix A).

The satisfied-but-failed rate is robust across sample scale, raters, and providers: it is concordant across five rater populations (the human panel plus gate and proxy scorings from two LLM providers; 47.6–59.5%; Fig. 2a, Table 4).

It also holds within each domain: satisfied-but-failed is 24.1% (retail), 62.1% (airline), and 38.7% (math tutoring), and the ranking replicates per domain (ρ=0.95 retail, 0.80 airline; Appendices F, H).

## Not an artifact of the word "satisfaction"
**Covers:** five subjective dimensions |ρ| ≤ 0.17; overall ρ = −0.147, flat dose-response (Fig. 2b)

Crucially, this is not an artifact of the word "satisfaction": all five subjective dimensions the panel rated (satisfaction, respect, clarity, perceived helpfulness, and would-return) are likewise decorrelated from success (|ρ| ≤ 0.17; Appendix B), so the gap reflects subjective approval in general.

Across all 150 transcripts the correlation is flat and non-positive (ρ= −0.147; dose-response curve flat, Fig. 2b).
