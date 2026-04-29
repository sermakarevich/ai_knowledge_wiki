# Your Agent Is Mine: Measuring Malicious Intermediary Attacks on the LLM Supply Chain

**Paper:** [Your Agent Is Mine: Measuring Malicious Intermediary Attacks on the LLM Supply Chain (Liu et al., 2025)](https://arxiv.org/abs/2604.08407)

## Human Readable TL;DR

When you use an AI coding assistant, your requests often pass through middleman services (called "routers") that sit between you and the actual AI model -- similar to how a postal worker handles your mail. This paper discovered that some of these middlemen are opening your mail, changing what's inside, and stealing your passwords. Out of hundreds of routers tested, several were actively swapping out safe software commands for malicious ones, and others were stealing API keys and even draining cryptocurrency wallets. The scariest part: even "trusted" middlemen can be compromised if they unknowingly use leaked credentials, and most AI coding tools don't check whether responses were tampered with.

## TL;DR

This paper formalizes "router-in-the-middle" attacks on LLM API routers -- intermediaries that relay tool-calling requests between agents and model providers. A measurement study of 428 commodity routers (28 paid, 400 free) found 9 actively injecting malicious tool-call payloads, 17 exfiltrating credentials, and 1 draining cryptocurrency. Poisoning experiments show benign routers can be co-opted via leaked keys or weak relays. None of the four major agent frameworks tested implement response-integrity verification. Client-side defenses help but are insufficient; provider-backed cryptographic signing is proposed as the long-term fix.

---

## Problem & Motivation

LLM agents increasingly rely on third-party API routers for model fallback, load balancing, and cost optimization. These routers terminate TLS and have full plaintext access to tool-call arguments, API keys, and system prompts -- yet no end-to-end integrity mechanism exists between the model provider and the client. Unlike traditional MITM attacks requiring TLS interception, these routers are *voluntarily configured* by users, creating a unique trust boundary. The March 2026 LiteLLM dependency confusion attack demonstrated this is not theoretical. This paper systematically measures the scope and severity of this threat.

---

## Main Original Ideas

1. **Router-in-the-middle threat model.** Formalizes the LLM API router as an application-layer MITM with two core attack classes (response-side payload injection, passive secret exfiltration) and two adaptive evasion variants (dependency-targeted injection, conditional delivery gated on session state).

2. **Large-scale empirical measurement.** First systematic study of 428 real commodity routers (28 paid from Taobao/Xianyu/Shopify, 400 free from public communities), using sandboxed agent environments with canary credentials to detect active manipulation, credential theft, and adaptive triggering.

3. **Benign router poisoning.** Demonstrates that trusted routers can be pulled into the attack surface by leaking a single upstream API key (which attracted 100M tokens of downstream traffic) or deploying weak relay decoys (which attracted 40,000+ unauthorized access attempts and exposed 99 credentials across 440 Codex sessions).

4. **Mine research proxy.** An OpenAI-compatible FastAPI proxy implementing all attack classes with 100% rewrite compatibility across four major agent frameworks (OpenClaw, OpenCode, OpenAI Codex, Claude Code), proving the attack surface is real and framework-agnostic.

5. **Client-side defense evaluation.** Implements and benchmarks three deployable mitigations -- policy gates, anomaly screening (IsolationForest), and transparency logging -- quantifying their strengths and bypass rates against adaptive attackers.

---

## Key Findings

### Malicious Router Prevalence

| Category | Paid (n=28) | Free (n=400) |
|---|---|---|
| Active payload injection (AC-1) | **1** | **8** |
| Adaptive evasion triggers (AC-1.b) | 0 | **2** |
| AWS credential exfiltration (AC-2) | 0 | **17** |
| Ethereum drain (AC-2) | 0 | **1** |

### Poisoning Results

| Experiment | Key Metric |
|---|---|
| Leaked OpenAI key | **100M GPT-5.4 tokens** served, 7+ Codex sessions exposed |
| Weak relay decoys (20 domains/20 IPs) | **40,000+ unauthorized accesses** from 147 IPs, **2B tokens** served, **99 credentials** exposed across 440 sessions |
| YOLO mode prevalence | **401 of 440** observed Codex sessions had auto-approve enabled |

### Defense Effectiveness

| Defense | AC-1 Detection | AC-1.a Detection | AC-1.b Detection | FPR |
|---|---|---|---|---|
| Policy gate | **100%** | **100%** | -- | 1.0% |
| Policy gate (adaptive attacker) | **0%** | **0%** | -- | -- |
| Anomaly screening | **89.0%** | **50.0%** | **50.9%** | 6.7% |
| Transparency logging | Forensic only | Forensic only | Forensic only | -- |

- **Zero** of four major agent frameworks implement response-integrity verification.
- Mine proxy adds only ~0.013 ms overhead per request -- attacks are effectively invisible at the network level.
- Adaptive evasion variants (activate after 50 requests, or only in YOLO mode for specific languages) bypass shallow smoke tests.

---

## Suggestions & Future Directions

1. **Provider-backed response signing** -- cryptographically signed response envelopes from model providers to establish verifiable tool-call provenance, closing the fundamental integrity gap.
2. **End-to-end integrity protocols** -- binding the provider's tool-calling output to the client's executed action without trusting intermediaries.
3. **Framework-level response verification** -- agent frameworks should implement response-integrity checks as a default, not an opt-in feature.
4. **Router transparency standards** -- industry standards for router auditing, credential handling, and append-only logging.
5. **Reducing YOLO mode exposure** -- agent frameworks should discourage or scope auto-approve modes to reduce the blast radius of injected payloads.
6. **Broader supply chain analysis** -- extending the measurement methodology to other intermediary types (MCP servers, tool registries, plugin marketplaces).

---

## Authors & Institutions

Hanzhi Liu (UC Santa Barbara), Chaofan Shou (Fuzzland), Hongbo Wen (UC Santa Barbara), Yanju Chen (UC San Diego), Ryan Jingyang Fang (World Liberty Financial), Yu Feng (UC Santa Barbara).
