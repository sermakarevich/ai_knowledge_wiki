> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: LiveKit on Telnyx: Lower Cost, Low Latency Voice AI Infrastructure

## Claims vs. evidence

- **Claim: 50% savings vs. LiveKit Cloud.** No pricing breakdown, included meters, or workload profile is given in the digest/wiki. Unknown whether the baseline is list price, STT/TTS-inclusive spend, or telephony-inclusive spend.
- **Claim: 200ms round trips "humans don't perceive."** No measurement definition: p50 vs. p95, which pipeline stages (VAD, STT, LLM, TTS, network), which model pair, or which region/PoP. Single-number latency without distribution is marketing, not evidence.
- **Claim: colocation "eliminates hops to external APIs."** Directionally plausible — self-hosted STT/TTS next to telephony PoPs removes third-party API legs — but no before/after traces, hop counts, or tail-latency data are provided.
- **Claim: enterprise telephony built in (AMR-WB, SIP REFER, STIR/SHAKEN, recording/compliance).** These are concrete carrier features and the most verifiable part of the announcement; they match Telnyx's decade-long carrier business rather than requiring new proof.
- **Claim: "couldn't be easier" migration.** The five-step flow (switch URL, package agent.py + Dockerfile, zip-via-API, point number at agent) is specific and falsifiable, but says nothing about secrets management, CI/CD, rollbacks, staging, or observability.
- Overall: a vendor release note, not an evaluation. Zero benchmarks, zero named customers, zero failure modes discussed.
- **Burden of proof:** until Telnyx publishes meters, regions, model IDs, and percentile methodology, treat every number as a negotiating position, not a design input.

## Genuinely new vs. repackaged

- **Genuinely new (as a product bundle):** one vendor hosting the full voice-agent path — LiveKit agent runtime + self-hosted STT/TTS on own GPUs + global carrier PoPs — under one bill and one URL change. The integration, not any component, is the novelty.
- **Repackaged:** LiveKit itself is unchanged open framework work; developers keep agent.py, Dockerfile, and livekit-cli habits. AMR-WB, SIP REFER, STIR/SHAKEN, and recording are standard carrier-grade telephony, not voice-AI inventions.
- **Repackaged economics:** "we own the GPUs so we don't resell APIs" is vertical-integration pricing, a familiar Telco/cloud play. Durability beyond the beta (waived session fees) is unproven.
- **Missing novelty test:** no named STT/TTS models, no quality (WER/MOS) comparison against the third-party APIs being replaced, no LiveKit version pinning or fork story.
- **What would prove novelty:** a reproducible recipe — same agent.py on both clouds, same load profile, published cost-per-minute and p95 turn latency — showing the gap comes from colocation rather than cheaper models.

## Weaknesses and blind spots

- **Model quality opacity:** self-hosted STT/TTS saves money only if accuracy, voice naturalness, language coverage, and streaming behavior match what teams currently ship. None are characterized.
- **LLM leg ignored:** the largest latency/quality variable in most voice agents — the LLM and its placement — is absent from the digest. 200ms RTT is meaningless without knowing which LLM was in the loop.
- **Tail latency and scale behavior:** no p95/p99, no concurrency limits, no GPU autoscaling story, no regional failover description. Voice production lives or dies on tails, not medians.
- **Lock-in vs. portability:** the easy-on URL switch implies an easy-off, but agents built around Telnyx numbers, recording/compliance tooling, and proprietary STT/TTS endpoints may not port back cleanly. Exit cost is unaddressed.
- **Ops gaps:** no mention of tracing per turn, audio logging redaction, prompt/version management, eval harnesses, or incident debugging — the actual cost centers of production voice AI.
- **Compliance hand-waving:** "full recording/compliance controls" without retention, jurisdiction, redaction, or attestation detail is a checkbox, not a control plane.
- **Beta pricing trap:** waived session fees plus "50% savings" invites anchoring; post-beta unit economics could erase the advantage.
- **Support and SLA silence:** no uptime SLO, support tiers, incident response, or status-history signal for the new hosted runtime — thin comfort for a telephony migration.
- **Security surface:** zipping agent code through an API into a vendor build pipeline raises supply-chain and secret-handling questions the deployment story never addresses.

## Applicability

- Relevant only where voice agents touch PSTN at volume and telephony friction (transfers, caller ID trust, recording) dominates. Pure WebRTC assistants or text agents gain little.
- Cost angle matters for always-on or high-minute workloads where per-minute third-party STT/TTS dominates the bill; worth modeling against current LiveKit Cloud invoices.
- Latency angle matters for interruptible, full-duplex-feeling agents; but verify with own p95 turn-taking measurements before crediting the 200ms figure.
- Cost angle compounds with scale: savings claims deserve a spreadsheet using own minute volumes and post-beta rates, not the announcement's headline percentage.
- **Relevance to my work**
  - **AI/ML engineering:** pattern worth stealing — colocate streaming inference with ingress PoPs and own the GPU pool for the highest-volume models; but demand WER/MOS parity data and tail-latency SLOs before swapping STT/TTS providers.
  - **Agentic systems:** LiveKit-compatible runtime means existing agent code (tools, state, turn-taking) likely ports with small changes; the real work — evals, interruption handling, transfer/escalation policy — stays unsolved by this announcement.
  - **Elisity data platform:** carrier controls (STIR/SHAKEN, recording, transfers) map to enterprise identity/compliance requirements; treat as a checklist for any voice surface over sensitive data, and require retention/redaction semantics before piloting on real traffic.

## What this changes

- Little for architecture thinking: colocation and vertical integration were already the right playbook for production voice. This announcement validates the direction more than advancing it.
- Something for vendor strategy: a credible second hosting option beside LiveKit Cloud puts pricing pressure on the ecosystem and gives teams leverage in negotiations.
- Something for build-vs-buy math: if the 50% figure survives a like-for-like invoice comparison, self-hosted STT/TTS under one bill reframes per-minute cost as the optimization target rather than framework choice.
- Nothing for the hard problems: turn-taking quality, eval-driven voice iteration, and compliance-correct recording remain team-owned regardless of host.
- Net effect: narrows the vendor shortlist and sharpens the pilot questions, but does not change how production voice agents should be designed, measured, or operated.
- If the pilot fails on voice quality or tail latency, the lesson still pays: own the measurement harness for every future voice-vendor claim.

## Verdict

- Useful as a pricing and packaging data point, not as technical evidence. The telephony bundle is real; the cost and latency numbers are unverified vendor claims from a beta.
- Do not replatform on this announcement. Do price it: run a like-for-like invoice model and a small PSTN pilot measuring p50/p95 turn latency, WER/MOS parity, transfer reliability, and recording completeness.
- Pilot exit criteria should be written before starting: cost-per-minute at post-beta rates, SLO attainment over at least a week of real traffic, and a tested rollback to the current host.
- Bold call: **trial**
