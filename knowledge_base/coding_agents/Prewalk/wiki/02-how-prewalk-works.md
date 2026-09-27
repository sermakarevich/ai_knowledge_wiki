> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# How Prewalk Works

**In one sentence:** `/prewalk` starts the task on the frontier model with a hidden "plan deeply, capture the plan as a todo list, then start" instruction, lets it explore and land its first edit, then swaps to a cheap model and deletes the planning instruction from context — so the cheap model inherits a real, lived-in trajectory (explored files, a todo checklist, one already-completed edit) instead of a plan document it has to re-derive from scratch.

## Key points

- The core idea: **hand off a trajectory, not a fairytale.** A plan document is "a literal postcard, describing a journey to a model that never took it" ([[01-the-plan-paradox|The /plan Paradox]]). What actually transfers value is the context window itself — the record of files read, dead ends ruled out, and the first concrete action taken.
- Mechanically, `/prewalk` does three things in order: (1) start the frontier model with a hidden prefixed instruction to plan deeply, then capture the plan as a todo list, then begin executing; (2) let the frontier model explore, write its plan, and initialize the todo list; (3) the moment its first edit lands — the point where it was confident enough to act — swap to the cheap model and prune the planning instruction from context.
- The swap works because of what's *removed*, not just what's added: the cheap model's context contains no visible planning instruction, so it never encounters a moment of "wait, I thought we were planning." As far as it can tell, it explored, built a comprehensive plan (now a todo list), and started executing with full confidence.
- The cheap model even inherits a **free in-context example**: the frontier model's first edit is already a demonstration, in place, in the target codebase's own style — not an abstract instruction to imitate.
- On SWE-Bench Pro (`django-13279` test ride), three arms are compared directly: `Opus 4.8 + /plan` ($3.18, 12.7 min, 84.6%), `Opus 4.8` alone ($2.78, 10.1 min, 84.6%), and `Opus 4.8 + /prewalk` (executing with Gemini Flash 3.5) at **$1.46** — with Opus doing recon → plan → one edit, then handing off to Flash for fix → tests → debug warnings → checks → close. Token totals per arm are shown as Σ: 1.34M (`/plan`), 1.10M (Opus alone), 1.13M (`/prewalk`).
- A second benchmark run (`django-12325`) compares `5.6 Sol + /prewalk` (executing with 5.6 Luna) at **$1.04 / 300s**, `5.6 Sol` alone at $1.71/372s, with Sol's own oneshot pass rate reported separately at 88% and Luna's oneshot at 77% — see [[04-the-receipts|The Receipts]] for the full pass-rate/cost/duration table.
- Anatomy of the wasted work `/plan` causes: Opus reads `base.py`, `signing.py`, and the test file under `/plan`, writes its plan, and leaves — then "the first thing Flash does with that beautiful document [is] re-read `base.py` and the test file, because a plan is not a file and you cannot edit prose." The same files get read twice, once at Opus prices and once at Flash prices.

---

## Why the trick works on the model, not just the token budget

The article frames `/prewalk` as depending on a specific illusion: the executor model has no channel that distinguishes context it generated itself from context it was handed. Once the planning instruction is gone and the todo list plus a completed first edit remain, the cheap model has no signal telling it this was someone else's plan — it reads its own context as evidence of its own prior competence and continues in the same register. This mechanism is examined more directly, including its resemblance to LLM *prefill* jailbreaks, in [[05-cheating-and-prefill|Cheating and the Prefill Connection]].

## Covers

The article's "Hand off a trajectory, not a fairytale" section and the two SWE-Bench Pro diagram comparisons (`django-13279`, `django-12325`).
