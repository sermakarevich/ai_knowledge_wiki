> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Dataset statistics (Table 2)
**In one sentence:** IHBench comprises 45 conversations across 10 domains with 428 interruption points (avg. 30.1 messages per conversation), skewed toward challenging interruption types and early-turn interruptions by design and by synthesis constraints.
## Key points
- The dataset contains 45 conversations across 10 domains with 428 total interruption points and an average of 30.1 messages per conversation (min 19 / max 40).
- Pushback is the most frequent interruption type at 105 cases (24.5%), followed by impatient 84 (19.6%), normal 81 (18.9%), topic switch 73 (17.1%), filler 60 (14.0%), and correction 25 (5.8%).
- Pushback dominates because the user intent generator is prompted to prefer challenging interruption scenarios over cooperative ones, with pushback the dominant type (probability ≥ 0.25) in 26 of 45 conversations versus only 6 for correction.
- Correction is under-generated relative to its average profile probability (12.3%, ~53 expected) with only 25 actual cases (5.8%), because corrections require the user to have provided a revisable piece of information in a prior turn and the round planner skips them when no natural self-correction opportunity exists.
- All interruption types besides correction track their profile probabilities within 2–5 percentage points.
- Interruptions concentrate in early turns — 169 (39.5%) at turns 0–4, 130 (30.4%) at 5–9, 80 (18.7%) at 10–14, and 49 (11.4%) at 15–19 — because fewer conversations reach deeper turns and so offer fewer interruption opportunities.
- Each conversation is seeded from a (domain, goal, user intent) triple: 10 listed domains × 5 goals × 10 user intents yields 500 possible configurations, of which 50 were randomly sampled and reduced to 45 conversations with 428 points after the verify–modify loop and well-formed-item filtering.
---
## Table 2: Dataset statistics
**Covers:** Dataset statistics, domain coverage, interruption-type distribution

| Statistic | Value |
|---|---|
| Conversations | 45 |
| Domains | 10 |
| Total interruption points | 428 |
| Avg. messages per conversation | 30.1 |
| Min / max messages | 19 / 40 |

### Interruption type distribution

| Type | Count (share) |
|---|---|
| Pushback | 105 (24.5%) |
| Impatient | 84 (19.6%) |
| Normal | 81 (18.9%) |
| Topic switch | 73 (17.1%) |
| Filler | 60 (14.0%) |
| Correction | 25 (5.8%) |

The chunk states: "The uneven type distribution reflects two factors. First, the user intent generator is prompted to prefer challenging interruption scenarios over cooperative ones. This is directly visible in the user intent interruption profiles: pushback is the dominant type (probability ≥ 0.25) in 26 of 45 conversations, while correction is dominant in only 6."

On correction: "correction is the only type where the actual count (25, 5.8%) falls well below what the average profile probability (12.3%) would predict (∼53 expected). This gap arises because corrections require the user to have provided a specific piece of information in a prior turn that they can then revise; the round planner under-generates corrections when no natural self-correction opportunity exists."

"All other types track their profile probabilities within 2–5 percentage points."

### Interruptions by depth (user turn index)

| Depth | Count (share) |
|---|---|
| 0–4 | 169 (39.5%) |
| 5–9 | 130 (30.4%) |
| 10–14 | 80 (18.7%) |
| 15–19 | 49 (11.4%) |

The chunk states: "Interruptions are concentrated in earlier turns (40% in turns 0–4) and taper off at depth (11% in turns 15–19). This is a natural consequence of the conversation length distribution: fewer conversations reach deeper turns, so there are fewer interruption opportunities at greater depth."

### Conversation seeding and domains
Each conversation is seeded from a (domain, goal, user intent) triple. Ten domains are covered: "SaaS, financial services, healthcare, telecom, e-commerce, travel, education, government, subscription media, and professional services."

"Five goals are generated per domain, and ten user intents per goal, yielding 500 possible configurations. Fifty are randomly sampled for conversation synthesis; after the verify–modify loop discards unfixable samples and we keep only interruption points that yield a well-formed evaluation item for every model, 45 conversations with 428 interruption points remain."

"Multiple conversations may share the same (domain, goal) pair but differ in user intent (personality, interruption profile, hidden information)."
