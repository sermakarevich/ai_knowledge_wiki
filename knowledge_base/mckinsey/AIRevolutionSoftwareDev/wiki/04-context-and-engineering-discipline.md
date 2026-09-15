> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Context is the input, discipline is the method

**In one sentence:** Production-grade artificial intelligence (AI) output comes from good context rather than clever wording, which is why the article's engineers predefine agent activity sequences and output templates instead of chatting their way to software.

## Key points

- The article's most quoted engineering maxim states that good AI output comes from good context rather than clever wording, and that production-grade software cannot be reached by chatting alone.
- Engineer work therefore centers on structuring agent tasks into precisely defined workflows so agent activity stays predictable and high quality.
- Predefining the sequence of agent activities is named as the concrete mechanism, turning open-ended delegation into an ordered, reviewable pipeline.
- Templates for agentic output standardize what agents produce, making results comparable, reviewable at pace, and safe to feed into downstream steps.
- The daily review ritual operationalizes the maxim: pull requests carry the change, test evidence carries the proof, and risk flags carry the doubt, so humans verify rather than re-derive.
- Independent analysis sharpens the point into a precondition: context must be a persistent shared layer across decisions, not reassembled at runtime, or multi-agent systems stall at demo scale.
- The failure mode the maxim warns against is lipstick-on-pig adoption — bolting AI chat onto legacy Agile-and-ticket processes built for all-human teams instead of replacing the process `[unverified: practitioner phrasing, consistent with the article's rethink-workflows moral]`.

---

## The maxim

"Good AI output comes from good context, not clever wording. You can't 'chat your way' to production-grade software." The sentence demotes prompt engineering from craft to cosmetic: wording tweaks cannot compensate for missing specifications, absent repository knowledge, or undefined acceptance criteria. Context — the machine-usable statement of what the system does, what the business needs, and what good looks like — is the actual input the model runs on.

## Workflows before agents

"The engineers' focus is much more on structuring agent tasks into precisely defined workflows, ensuring their activities are predictable and high quality (e.g., predefining the sequence of agent activities), and structuring templates for agentic output." Two instruments carry the discipline. First, the predefined activity sequence fixes the order of operations so each agent step has known inputs, known outputs, and a known place for human or automated verification. Second, output templates fix the shape of results so a hundred overnight agents produce one reviewable stream instead of a hundred idiosyncratic dumps. Predictability is the product; autonomy is kept inside guardrails that make review scale sublinearly with agent count.

## The review surface

The vignette's triad — AI-generated pull requests, test evidence, and risk flags — is the maxim made operational. The pull request proposes, the evidence proves, and the flags disclose uncertainty, which together let three engineers clear a night's output from ~100 agents each morning. A subtle trap noted by practitioners: when the same agent writes the code and the tests, a green suite is weaker evidence than it looks, so verifying the verifier — second-agent judges plus human spot checks — becomes part of the workflow.

## The shared-context precondition

The hardest reading of the maxim holds that coordinated agents need shared, structured understanding of context across decisions as a standing system layer. Teams that skip this and run Level 4 agents on Level 2 workflows — AI bolted onto ticket queues and ceremonies designed for humans doing every step — get the coordination costs without the delivery gains. Discovery work that turns ambiguity into agent-actionable specification carries the highest leverage precisely because every downstream stage inherits its errors.

**Covers:** the context-not-wording maxim — predefined activity sequences, output templates, the pull-request/evidence/risk-flag review surface, the verify-the-verifier trap, and the persistent-shared-context precondition.
