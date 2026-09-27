> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Composite Scoring

**In one sentence:** To rank items on several criteria at once, break the judgment into independent Score dimensions, normalize each to 0–1, and combine them with weights controlled in code so priorities can shift without rewriting prompts.

## Key points

- The method is: break the judgment into independent dimensions, score each one separately, and combine them with weights controlled in code.
- The resume-screening example scores four dimensions, each a 0–4 Score over five rubric levels: `python_depth`, `team_leadership`, `system_design`, and `generalist` (evidence of picking up unfamiliar tools, roles, or domains).
- Each dimension is normalized to 0–1 by dividing its score by 4, and weights adjust relative importance without losing the nuance of individual scores.
- The Senior IC composite is `(0.40 * py) + (0.10 * lead) + (0.40 * arch) + (0.10 * general)` — Python depth and system design dominate.
- The Engineering Manager composite is `(0.15 * py) + (0.40 * lead) + (0.20 * arch) + (0.25 * general)` — leadership dominates with generalist second.
- Beyond ranking, the formula gives visibility into exactly how the final score is calculated: if top-ranked candidates don't match expectations, adjust the weights to find the right balance.
- The same per-dimension scores serve multiple rankings — one API call feeds both the IC and EM formulas.

---

## Example: resume screening

Resumes for engineering roles are ranked on several criteria to select the top candidates for further review.

## Step 1: score each dimension independently

| Question | Instructions | Levels (0–4) |
|---|---|---|
| `python_depth` (score) | How much depth of python experience, based on the resume? | No Python mentioned / Mentioned but no detail / Used in projects, some specifics / Primary language, multiple projects / Deep expertise: architecture, performance, libraries |
| `team_leadership` (score) | How much experience managing or leading engineering teams? | No management mentioned / Informal mentorship or tech lead / Led a small team or project / Managed a team with direct reports / Managed multiple teams or an engineering org |
| `system_design` (score) | How much experience designing large-scale or distributed systems? | No architecture work / Contributed to design discussions / Designed components of a larger system / Owned architecture of a significant system / Designed systems at scale across multiple domains |
| `generalist` (score) | How much evidence of picking up unfamiliar tools, roles, or domains outside core specialty? | Only one domain or role / Some variety within a narrow field / Worked across a few areas or stacks / Regularly moved between domains, wore many hats / Track record of ramping up in unfamiliar areas and delivering |

## Step 2: combine with weights

> "Each dimension is normalized to 0–1 and weighted. The weights give you an easy way to adjust the relative importance of each dimension, without losing any of the nuance of the individual scores."

```python
py      = response.answers["python_depth"].score / 4
lead    = response.answers["team_leadership"].score / 4
arch    = response.answers["system_design"].score / 4
general = response.answers["generalist"].score / 4

# Senior IC
ic_score = (0.40 * py) + (0.10 * lead) + (0.40 * arch) + (0.10 * general)

# Engineering Manager
em_score = (0.15 * py) + (0.40 * lead) + (0.20 * arch) + (0.25 * general)
```

**Covers:** https://docs.typesafe.ai/patterns/composite-scoring
