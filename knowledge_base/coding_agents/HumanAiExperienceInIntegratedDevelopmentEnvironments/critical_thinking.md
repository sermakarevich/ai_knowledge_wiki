> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: Human-AI Experience in Integrated Development Environments: A Systematic Literature Review

## Claims vs. evidence

- Claim: AI assistance boosts productivity (less search, less boilerplate, fewer context switches). Evidence: moderate — 74/90 Impact studies agree directionally, but gains vanish on proprietary/complex logic and no standardized productivity metric is used across studies.
- Claim: verification can consume up to 50% of developer time (Mozannar et al., 2024a). Evidence: strong as an existence proof, weak as a general rate — single-study figure, yet consistent with the broader "subtly flawed output" mechanism (Wermelinger, 2023).
- Claim: trust is calibrated by suggestion quality and task stakes (routine/PoC trusted, production/complex distrusted). Evidence: fairly strong — convergent across attitude studies (11/74), though mostly self-report rather than behavioral acceptance data.
- Claim: novices over-rely, professionals under-rely. Evidence: moderate — the asymmetry replicates across settings, but novice studies use small classroom tasks with weak transfer to production work.
- Claim: hybrid autocompletion-plus-conversation is the right design. Evidence: weak-to-moderate — a synthesis of 28/90 design studies, mostly prototypes and Copilot-adjacent tools, not head-to-head trials.
- Claim: up to 36% of vulnerabilities in AI-assisted code originate from LLMs. Evidence: weak as a point estimate (single-study, language- and benchmark-dependent) but directionally credible given training-data replication mechanisms.
- Meta-evidence caveat: median n=17, rarely justified; Copilot in 36/90 studies; short-term lab evaluations dominate — so most effect sizes should be read as signals, not constants.
- Cross-cutting gap: 250 future-work statements cluster on productivity (43), design (29), and audit (28) — yet governance, privacy-aware prompting, and proactivity are flagged as missing, so the agenda is longer on measurement than on control.

## Genuinely new vs. repackaged

- Genuinely new: the in-IDE HAX framing itself — scoping HAX to where code is written, inspected, or tested, with the Impact/Design/Quality taxonomy built by open coding with adjudication. Prior surveys lacked this boundary.
- Genuinely new: quantifying the verification tax as a first-class cost of AI assistance, plus concrete mitigations (edit-likelihood highlighting, runtime surfacing, multi-alternative comparison).
- Genuinely new: the over-reliance/under-reliance asymmetry by expertise, tied to interface levers (explanations, scope controls, live values) rather than blanket trust advice.
- Repackaged: the "AI as pair-programming collaborator" metaphor — recycled from pre-LLM CSCW literature without testing where the analogy breaks (no shared mental model, no accountability).
- Repackaged: methodological critique (underpowered samples, no preregistration, no sharing) — correct, but the standard HCI/open-science playbook (Caine, 2016; power analysis; versioned repos) applied to a new corpus.
- Repackaged: future-work list (personalization, explainability, lifecycle coverage) — largely the 250 extracted future-work statements reorganized, not a prioritized bet.

## Weaknesses and blind spots

- Tool monoculture: 36/90 studies on GitHub Copilot; agentic/multi-file, terminal-based, and notebook-native assistants are barely represented — findings may not survive the shift to agent-mode IDEs.
- Stage blindness: 46/71 professional studies specify no SDLC stage; mapping to a Waterfall model (Alshamrani and Bahattab, 2015) is anachronistic for iterative/agentic workflows and weakens interpretability.
- Missing voices: no non-users or stopped-users; educational slice (19/90) is thin and possibly under-indexed since students often work outside full IDEs.
- Temporal window: 2022–2024 eligibility plus arXiv preprints captures the LLM boom but mixes peer-reviewed and unreviewed evidence; second snowballing round adding zero papers suggests saturation of a backward-looking graph, not of the field.
- No comparison criterion in eligibility means heterogeneous designs are pooled narratively; vote-counting language ("N/90 studies") risks implying precision the synthesis method cannot support.
- Extraction partially assisted by Elicit (cross-verified, but single-author manual coding) — residual interpretation bias in a 90-paper corpus, acknowledged but not quantified via inter-rater reliability.
- Industry time-horizon tension (1–2 month feedback vs. longitudinal rigor) is named but unresolved; the review recommends collaboration without a mechanism.

## Applicability

- Directly applicable where developers write, review, or test code inside an IDE with AI assistance; less applicable to non-interactive pipelines, batch codegen, or fully autonomous agents operating outside the editor.
- The verification-tax lens transfers to any team measuring "AI speedup": report acceptance, edit, and verification effort — not just time-on-task.
- Trust-calibration findings transfer to code-review policy: stricter scrutiny for generated tests, production paths, and open-ended tasks; lighter touch for boilerplate and PoCs.

**Relevance to my work**

- AI/ML engineering: adopt the verification-burden metric (accept/edit/verify rates) for our own coding-assistant evaluations instead of raw completion time; instrument it in the IDE before claiming productivity wins.
- Agentic systems: the hybrid autocompletion-plus-conversation conclusion under-describes agents — treat agent trajectory review (plans, diffs, test evidence) as the new verification surface, and design scope controls plus runtime evidence into agent UX from day one.
- Elisity data platform: apply the quality-dimension checklist (correctness, readability, security) to generated pipeline/SQL/config code; mandate generated-test skepticism (developers already distrust suggestions in test files) and add post-processing/test-generation gates for AI-produced data logic.

## What this changes

- Treat verification as the interaction, not overhead: keep tests, static analysis, and reference examples inside the editor and surface runtime values at acceptance time.
- Design default: hybrid inline-plus-chat with shared context, brief explanations, and scope/snooze controls — and measure whether each addition reduces verification time or just adds UI.
- For novices and onboarding: structured prompting plus staged AI contribution beats bans or unrestricted access; assess reasoning traces and verification, not just output.
- For studies and internal evals: justify sample sizes, preregister, share codebooks/prompts/tasks, and report SDLC stage plus task taxonomy — otherwise results do not cumulate.
- Deprioritize generic "productivity" claims; prioritize audit assets (vulnerability coverage, quality metrics, longitudinal tracking) since security/maintainability is where the evidence is thinnest and the risk highest.

## Verdict

- This is the best current map of in-IDE HAX, honest about its own threats, but its headline numbers rest on small, Copilot-skewed, short-term studies — use it as a design and evaluation checklist, not a forecast.
- Calibrated caution applies: the review's value is the taxonomy plus the verification framing; the rest is a competent reorganization of a fast-moving, uneven literature.
- Bold call: **trial** — pilot verification-centered practices (accept/edit/verify metrics, hybrid UX with scope controls, audit gates on generated code) and re-evaluate as agentic-IDE evidence arrives.
- Revisit trigger: a follow-up review with agent-mode tools, longitudinal field data, and non-user perspectives would be the signal to upgrade this from **trial** to **adopt**.
