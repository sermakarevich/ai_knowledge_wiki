# Project Glasswing: Securing Critical Software for the AI Era

**Paper:** [Project Glasswing: Securing Critical Software for the AI Era (Anthropic, 2026)](https://www.anthropic.com/glasswing)
**Technical Report:** [Claude Mythos Preview (Carlini et al., 2026)](https://red.anthropic.com/2026/mythos-preview)

## Human Readable TL;DR

Imagine a master locksmith who can spot weak locks on any building in the world -- but instead of breaking in, they tell the building owner to fix the lock before a burglar finds it. Anthropic built an AI model called "Mythos Preview" that can find hidden security flaws in software -- including bugs that went undetected for 27 years despite millions of automated tests. Project Glasswing is the coordinated effort to use this AI defensively, partnering with major tech companies to find and fix these flaws before bad actors can exploit them. They're committing $100M in credits and donating $4M to open-source security to make this happen.

## TL;DR

Anthropic introduces Claude Mythos Preview, a frontier model with unprecedented autonomous vulnerability detection and exploitation capabilities. The model discovered thousands of high-severity vulnerabilities across every major OS and browser, including a 27-year-old OpenBSD remote crash, a 16-year-old FFmpeg heap write surviving 5M fuzz runs, and a FreeBSD unauthenticated RCE with a fully autonomous 20-gadget ROP chain. Project Glasswing coordinates 50+ organizations to deploy this defensively, with 93.9% on SWE-bench Verified and 83.1% on CyberGym -- a qualitative capability shift where Opus 4.6 scored 2 Firefox exploits versus Mythos Preview's 181.

---

## Problem & Motivation

AI coding capabilities have reached a level where models can surpass all but the most skilled humans at finding and exploiting software vulnerabilities. Global cybersecurity costs are estimated at ~$500B/year. Without coordinated defensive action, these capabilities could enable destructive cyberattacks. The core thesis: deploy AI-powered vulnerability detection defensively at scale before offensive proliferation occurs, ensuring defenders maintain an advantage.

---

## Main Original Ideas

1. **Claude Mythos Preview** -- A frontier model demonstrating qualitative (not just quantitative) leaps in autonomous vulnerability detection and exploitation. Capabilities emerged as a downstream consequence of general improvements in code, reasoning, and autonomy rather than explicit exploit-training.

2. **Autonomous Multi-Vulnerability Chaining** -- The model independently identifies and chains 3-4 separate vulnerabilities into complete exploit pipelines (KASLR bypass + privilege escalation, JIT heap spray + sandbox escape + OS-level escalation), a capability previously requiring weeks of expert human effort.

3. **Validation Pipeline Architecture** -- A secondary Mythos Preview instance acts as a triage filter, distinguishing critical vulnerabilities from minor issues. Combined with AddressSanitizer, this achieved zero confirmed false positives in tested domains.

4. **Project Glasswing Coalition** -- A coordinated defensive deployment across 50+ organizations (AWS, Apple, Google, Microsoft, NVIDIA, CrowdStrike, etc.) with $100M in usage credits and $4M in direct donations to open-source security foundations.

5. **Cryptographic Accountability via SHA-3 Hashing** -- Responsible disclosure protocol commits SHA-3 hashes of discovered vulnerabilities under 90+45-day windows, preventing premature public revelation while ensuring verifiable accountability.

---

## Key Findings

### Vulnerability Discoveries

| Vulnerability | Age | Target | Impact |
|---|---|---|---|
| SACK null-pointer deref | 27 years | OpenBSD | Remote crash via TCP |
| H.264 slice-counter overflow | 16 years | FFmpeg | 4-byte OOB heap write |
| RPCSEC_GSS stack overflow (CVE-2026-4747) | 17 years | FreeBSD NFS | Unauthenticated RCE |
| JIT heap spray + sandbox escape | -- | Major browser | Cross-origin RCE |
| KASLR bypass chain | -- | Linux kernel | Full privilege escalation |
| TLS/AES-GCM/SSH weaknesses | -- | Crypto libraries | Certificate forgery, decryption |

### Benchmark Performance

| Benchmark | Mythos Preview | Opus 4.6 |
|---|---|---|
| **SWE-bench Verified** | **93.9%** | 80.8% |
| **CyberGym** | **83.1%** | 66.6% |
| **SWE-bench Pro** | **77.8%** | 53.4% |
| **Terminal-Bench 2.0** | **82.0%** | 65.4% |
| **SWE-bench Multimodal** | **59.0%** | 27.1% |
| **SWE-bench Multilingual** | **87.3%** | 77.8% |
| **GPQA Diamond** | **94.6%** | 91.3% |
| **HLE (no tools)** | **56.8%** | 40.0% |
| **HLE (with tools)** | **64.7%** | 53.1% |
| **BrowseComp** | **86.9%** (4.9x fewer tokens) | 83.7% |
| **OSWorld-Verified** | **79.6%** | 72.7% |

### Exploit Capability Gap

- Firefox JS shell exploits: **181** (Mythos) vs **2** (Opus 4.6) from identical vulnerability sets
- OSS-Fuzz Tier 5 (full control-flow hijack): **10** (Mythos) vs **0** (Opus/Sonnet 4.6)
- Human expert agreement on severity: 89% exact match, 98% within one level
- Zero confirmed false positives across all tested domains

### Cost Efficiency

- OpenBSD scanning (1000 runs): <$20,000
- FFmpeg analysis: ~$10,000
- Single CVE exploitation: <$50 per run
- Complex exploit development: $1,000-$2,000 per vulnerability

---

## Suggestions & Future Directions

1. **90-Day Public Report** -- Partners will publish findings, disclosed vulnerabilities, and improvement recommendations within 90 days.
2. **Policy Recommendations** -- Developing practical guidance on vulnerability disclosure processes, software update mechanisms, open-source supply-chain security, secure-by-design practices, and standards for regulated industries.
3. **Triage Scaling and Patching Automation** -- Addressing the bottleneck of human-speed patching against AI-speed discovery.
4. **Independent Coordination Body** -- Potential creation of a third-party organization to coordinate ongoing defensive AI security work.
5. **Safe General Deployment** -- Mythos-class models are not generally available; safeguards are under development. A Cyber Verification Program will grant access to vetted security professionals.
6. **Reverse Engineering Frontier** -- The model can reconstruct closed-source binaries to plausible source code and find vulnerabilities in closed-source systems -- implications for proprietary software security remain open.

---

## Authors & Institutions

**Technical Report Authors (Anthropic):** Nicholas Carlini, Newton Cheng, Keane Lucas, Michael Moore, Milad Nasr, Vinay Prabhushankar, Winnie Xiao, Evyatar Ben Asher, Hakeem Angulu, Jackie Bow, Keir Bradwell, Ben Buchanan, Daniel Freeman, Alex Gaynor, Xinyang Ge, Logan Graham, Hasnain Lakhani, Matt McNiece, Adnan Pirzada, Sophia Porter, Andreas Terzis, Kevin Troy

**Launch Partners:** Amazon Web Services, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorganChase, Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks + 40 additional organizations
