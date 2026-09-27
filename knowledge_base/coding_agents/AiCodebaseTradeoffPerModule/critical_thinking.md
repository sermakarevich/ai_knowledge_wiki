> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: If you are letting AI agents write large chunks of your codebase, here is something I would recommend - decide your tradeoff per file / module. | Arpit Bhayani

## Claims vs. evidence

The central claim is stark: you cannot have both AI shipping speed and deep
understanding everywhere — trying to get both yields neither. The prescription
is a per-file sort into Bucket one (speed over understanding) and Bucket two
(failure expensive or irreversible). The evidence base is thin for the claim
itself: a LinkedIn post with 1,258 reactions and 41 comments, plus anecdotal
commenter agreement — popularity, not measurement. No defect rates, review
times, or incident data are offered for the two-bucket split working in
practice. The strongest quasi-evidence comes sideways from the related-posts
feed: hard token caps (2,000,000/day, 25,000/request), ~$27 per shipped agent
task (~$5.50 first-try) with ~$3,200/month lost to retry loops, and repeated
guardrail stories (CI, contracts, transactional persistence). Those numbers
support "unreviewed agent code is expensive" but do not validate the specific
two-bucket boundary the post draws.

## Genuinely new vs. repackaged

The per-module framing is the genuinely useful contribution: most AI-coding
advice is global ("always review" or "trust the agent"), while this makes the
tradeoff explicit, local, and decided before handing work to the agent. The
reallocation idea — spend time saved in Bucket one on deep reading in Bucket
two — is a crisp attention-budgeting rule. Much else is repackaged: risk-based
review (auth/payments/data-integrity get scrutiny) is decades-old safety
engineering; "agent output is a first draft" restates standard code-review
practice; "use agent working time to read code" is just parallelised review.
The comment refinements (Bucket one shrinks as instructions mature; read while
the agent works) are the most practice-near additions and arguably more
actionable than the post itself.

## Weaknesses and blind spots

First, the binary is too clean: real modules sit on a spectrum (billing-adjacent
helpers, migrations, config, glue code) and the post gives no triage rule for
the middle. Second, classification itself is unexamined — who labels modules,
where is the label stored, and what stops Bucket-one code from silently
migrating into critical paths as prototypes harden? Third, "read the diff line
by line, trace the system, make the agent explain itself" is a review
aspiration with no checklist, no time box, and no acknowledgment that agent
self-explanations are unreliable narrations, not evidence. Fourth, the post
ignores the failure mode the feed documents: agents failing expensively and
quietly (retry loops, runaway token spend, same-vendor correlated outages) —
cost and blast-radius controls get no bucket. Fifth, there is survivorship bias
throughout: commenters who agree are visible; teams burned by misclassified
Bucket-one code are not.

## Applicability

The rule travels well wherever agent-written code volume exceeds human review
bandwidth — which is to say, nearly everywhere now. It is most applicable to
teams with a clear critical path (payments, identity, data planes) and a large
tail of scaffolding, and least applicable to small codebases where the sorting
overhead exceeds the review savings.

- **Relevance to my work**
  - AI/ML engineering: evaluation harnesses, prompt fixtures, and offline
    experiment scripts are natural Bucket one; training-data pipelines,
    feature definitions, and serving/inference paths are Bucket two where
    silent corruption compounds.
  - Agentic systems: tool definitions, permission scopes, retry/cap policies,
    and persistence (Saga/Outbox, LLM-outside-transaction) belong in Bucket
    two — the feed's transaction and token-cap posts are the missing
    operational half of Bhayani's rule.
  - Elisity data platform: anything touching data integrity, identity/policy
    enforcement, or network segmentation decisions is Bucket two by the
    post's own examples; collectors, dashboards, and one-off migration or
    analysis scripts are Bucket one — but the boundary needs a written
    registry, since today's prototype connector is tomorrow's trust input.

## What this changes

Little in principle, something in practice. The post does not invent
risk-based review, but it gives teams permission to stop pretending all
agent-generated code deserves equal attention — and a vocabulary ("which
bucket is this file in?") for the merge-review conversation. Adopted
literally, it changes where review hours go rather than how many are spent.
Adopted with the feed's guardrail lesson, it pairs the bucket decision with
mechanical backstops (caps, CI gates, contracts) so a misclassification is
caught by tooling rather than by incident. Without that pairing, it changes
almost nothing: an unrecorded mental bucket is just vibes.

## Verdict

A sound attention-allocation heuristic with an overstated binary and no
operational machinery — worth adopting as a team convention only if the bucket
labels are written down and backed by guardrails that survive misclassification.
The engagement (1,258 reactions, 41 comments) signals the problem is real and
shared; the absence of data signals the solution is still folk wisdom. Pair it
with priced runs, token caps, and mandatory CI/contracts on Bucket-two paths,
revisit classifications as code hardens, and treat agent explanations as
interrogation aids rather than proof. On that basis: **trial**.
