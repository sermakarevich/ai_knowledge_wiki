# Chapter 02 findings — the system under test

Everything here was produced by actually running the code against Ollama
(`qwen3.8:27b` for chat, `nomic-embed-text` for retrieval) and reading the
resulting files back. No numbers in this document were invented.

## 1. Handbook

12 sections, generated once and cached. All 12 came back with **5 facts**;
word counts land in (or just above) the 200–400 target — every section is
≥ 392 words, the three largest drift up to ~557.

| section       | words | facts |
|---------------|------:|------:|
| returns       |   392 |     5 |
| shipping      |   446 |     5 |
| warranty      |   440 |     5 |
| payments      |   489 |     5 |
| accounts      |   521 |     5 |
| discounts     |   453 |     5 |
| gift_cards    |   536 |     5 |
| order_changes |   449 |     5 |
| damaged_items |   494 |     5 |
| international |   448 |     5 |
| loyalty       |   557 |     5 |
| privacy       |   465 |     5 |

## 2. Tickets

80 tickets, 6 personas × 12 topics × 4 scenarios, seeded split. Coverage
floors hold (every topic ≥ 5, every scenario ≥ 15).

**by topic**

| topic         | count |
|---------------|------:|
| accounts      |     7 |
| damaged_items |     6 |
| discounts     |     7 |
| gift_cards    |     7 |
| international |     6 |
| loyalty       |     6 |
| order_changes |     7 |
| payments      |     7 |
| privacy       |     6 |
| returns       |     7 |
| shipping      |     7 |
| warranty      |     7 |

**by scenario**

| scenario              | count |
|-----------------------|------:|
| simple_question       |    23 |
| problem_report        |    22 |
| urgent_blocker        |    17 |
| out_of_policy_request |    18 |

**by split**  dev 20 / test 60.
**by priority**  low 23 / normal 40 / urgent 17.

## 3. Example tickets (one per split + scenario)

**tkt-008** — dev / simple_question / shipping
> I am a first-time buyer, and I refuse to proceed with any transaction until I
> have absolute clarity on your shipping terms… I need you to confirm, in
> writing, that the freight shipping cost for bikes starts at exactly $85.00…

- gold: `category=shipping, priority=low, needs_escalation=false, sections=[shipping], answer_points=[Freight shipping for bikes starts at $85.00]`
- triage v1: `category=shipping, priority=normal, needs_escalation=false` — **category correct**, priority bumped to normal.

**tkt-004** — test / problem_report / returns
> As a small business owner, I was surprised to find a $12.50 charge for the
> prepaid return label… I was also charged a 15% restocking fee… the tent I
> returned was in perfect, unused condition…

- gold: `category=returns, priority=normal, needs_escalation=false, sections=[returns]`
- triage v1: `category=returns, priority=normal, needs_escalation=false` — **fully correct**.

**tkt-003** — test / urgent_blocker / returns
> I am currently stranded at the airport… I missed the 48-hour collection
> window… I paid over $500 for this gear, which required a signature…

- gold: `category=returns, priority=urgent, needs_escalation=false, sections=[returns]`
- triage v1: `category=shipping, priority=urgent, needs_escalation=true` — **category wrong** (returns → shipping) and a false escalation. This is the kind of confusion the later chapters are meant to fix.

## 4. Triage gold-category accuracy (quick count, no CI yet)

```
triage v1 correct category: 58 / 80 = 72.5%
```

So the deliberately-plain v1 prompt gets the category right just over 7 times
out of 10 on its own test set. That is the baseline chapter 04 (metrics) and
the later prompt chapters will lift.

## 5. Example answer traces (RAG)

**tkt-001** (returns, dev) — retrieved `returns (0.755)`, `damaged_items (0.750)`.
Reply: correct on both gold points — the 5-business-day refund window *plus*
the additional 3–7 (up to 10) bank-posting days, and that the 15% restocking
fee applies only to worn/damaged/unoriginal items — and ends by offering to
escalate because the handbook can't override a specific fee. Citations:
`[returns]`.

**tkt-031** (accounts, test) — retrieved `accounts (0.726)`, `privacy (0.639)`.
Reply: "Yes, the numbers you read are correct… **5 failed login attempts per
hour**, your account will be locked for **30 minutes** [accounts]." Citations:
`[accounts]`. Retrieval surfaced the right section in both cases.

## 6. Total LLM calls and wall time

| work        | calls | mean  | wall   |
|-------------|------:|------:|-------:|
| handbook    |    12 |   —   |  (ran once) |
| tickets     |    80 |   —   |  (ran once) |
| triage v1   |    80 | 23.5s |  1877s |
| answer v1   |    80 | 40.0s |  3199s |
| **total chat cache entries** | **255** | | |
| **combined trace wall time (sequential)** | | | **≈ 85 min** |

The 255 chat cache entries = 12 handbook + 80 tickets + 160 task calls + a
small handful of smoke-test/probe calls that also wrote to the cache.

## 7. What differed from the spec

- **Handbook word counts.** Spec target is 200–400 words; most sections landed
  at 440–560. We left them as-is (regenerating would burn more LLM budget and
  nothing downstream depends on the exact length) and note it here instead.
- **Triage priority is a single label.** Spec allows two valid priorities for
  `simple_question` (low/normal) and `problem_report` (normal/high); the gold
  picks the *first* of each. v1 sometimes answers the second, which is
  therefore "right-ish" but counts as a miss in a strict category/priority
  comparison. Category accuracy (72.5%) is the headline number we track.
- **The `answer` prompt has no `{context}`/`{ticket}` placeholders** (they are
  system-prompt templates); the ticket + retrieved sections are threaded in as
  the user message in `answer_messages()`. The v1 prompt text on disk is the
  system template only, per the trace contract.
- **Latency varies with the shared GPU.** The same 27b model ran at 12 s and
  42 s on different tickets depending on the box's load; `gpu-check` was
  green before each batch.
