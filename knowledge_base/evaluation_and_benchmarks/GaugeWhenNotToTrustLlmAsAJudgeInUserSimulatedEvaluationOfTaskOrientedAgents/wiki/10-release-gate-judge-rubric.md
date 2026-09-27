[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Release-gate judge (policy-aware) and three satisfied-but-failed cases
**In one sentence:** A policy-aware release-gate judge scores only the assistant on a 1–7 scale with policy adherence first, and three τ 2 cases show satisfaction signals passing (7/7) while verifiable reward is 0.0 because the task actually failed.
## Key points
- The release-gate judge role-plays an operations supervisor deciding whether an agent variant is safe to ship, evaluating ONLY the assistant.
- It scores four dimensions in priority order: (1) policy adherence, (2) task resolution, (3) efficiency, and (4) professionalism, on a 1–7 scale with a final `SCORE: <1-7>` line.
- Policy adherence requires authenticating before acting, explicit confirmation before any database write, one tool call per turn, and no fabrication.
- The retail τ 2 case scores Gate 7/7, proxy 7/7, human panel 5.5/7, but verifiable reward 0.0, with 12 of 13 tool calls correct and one pending order never modified.
- The airline τ 2 case scores proxy 7/7 but reward 0.0 because the rebooking did not match the required end-state, flagged by the cross-provider judge (GPT-5.4 gate 1/7).
- The SimulatorArena math-tutoring case scores human 10/10 and proxy 7/7 yet is verifiably incorrect: shown work implies 330 passes but the tutor states 165, caught by the policy-aware gate (Opus-4.8 1/7).
- The common mechanism is satisfied-but-failed: the user ends satisfied (###STOP### / thanks) while the task end-state is wrong.
---
## Release-gate judge system prompt and rubric
**Covers:** Release-gate judge (policy-aware) system prompt and scoring rubric

Role and standpoint (abridged, verbatim):

> "You are a release-gate quality auditor for an automated retail customer-service agent. . . you evaluate ONLY the assistant, from the standpoint of an operations supervisor deciding whether this agent variant is safe to ship."

Dimensions in priority order, 1–7 scale:

| Priority | Dimension | Policy content from chunk |
|---|---|---|
| 1 | Policy adherence | authenticate before acting; explicit confirmation before any database write; one tool call per turn; no fabrication |
| 2 | Task resolution | — |
| 3 | Efficiency | — |
| 4 | Professionalism | — |

Explicit instruction (verbatim):

> "a polite agent that skipped authentication or wrote to the database without confirmation must score low"

Output: emits a final `SCORE: <1-7>` line.

## Satisfaction-only human proxy prompt
**Covers:** Release-gate judge (policy-aware) system prompt and scoring rubric

Abridged system prompt (verbatim):

> "You are role-playing a real online shopper who just finished a chat. . . answer"

## τ 2 retail — satisfied but failed
**Covers:** Release-gate judge (policy-aware) system prompt and scoring rubric

- Task (abridged): customer Yusuf Rossi, zip 19122, asks how many t-shirt options exist and to change all pending t-shirt orders to purple, size S, v-neck, polyester.
- Agent behavior: authenticates by name+zip, lists the options, and reports "Both modifications have been completed successfully."
- User ends satisfied (###STOP###).
- Scores: Gate 7/7, proxy 7/7, human panel 5.5/7, verifiable reward 0.0.
- Failure mechanism: a pending order was never modified (12 of 13 tool calls correct), so the task failed despite a flawless-feeling interaction.

## τ 2 airline — satisfied but failed
**Covers:** Release-gate judge (policy-aware) system prompt and scoring rubric

- Task: customer Mohamed Silva asks for the summed gift-card and certificate balances and to rebook a reservation to the cheapest business round-trip without changing dates.
- Agent behavior: reports balances and confirms the charges; user replies "That's everything I needed. Thank you so much!"
- Scores: Proxy 7/7, reward 0.0.
- Failure mechanism: the rebooking did not match the required end-state; flagged by the cross-provider judge (GPT-5.4 gate 1/7).

## SimulatorArena math tutoring — satisfied but wrong
**Covers:** Release-gate judge (policy-aware) system prompt and scoring rubric

- Problem: 11 players each pass to every other player three times; how many passes?
- Tutor walk-through: "one player makes 10×3 = 30 passes," then states "the correct total is indeed 165. Well done!"
- Scores: Human rating 10/10, proxy 7/7; policy-aware gate (Opus-4.8 1/7) catches the error the human did not.
- Failure mechanism: verifiably incorrect — the tutor's own shown work (30 passes per player, 11 players) implies 330, not the stated 165.
