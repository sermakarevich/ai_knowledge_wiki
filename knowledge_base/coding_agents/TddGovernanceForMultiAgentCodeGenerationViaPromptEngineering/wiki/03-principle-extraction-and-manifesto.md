# Principle Extraction and Manifesto

> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Principle Extraction and Manifesto

**In one sentence:** The paper extracts a bounded canonical TDD corpus of historically "right" but economically fragile human-era principles — organized into order, granularity, feedback quality, and design hygiene — and represents each as a structured record (label, canonical quote, intent, bibliographic pointer) to be translated into AI-native governance rules.

## Key points

- Four principle categories are defined in Table 1: Order (Test-first, Red→Green→Refactor), Granularity (minimal failing test, minimal passing code, one failing test at a time), Feedback quality (FAST, independent, repeatable, self-validating, timely tests with meaningful assertions), and Design hygiene (remove duplication, refactor continuously while green) [2, 19].
- Each category has a typical human-era failure mode: "just code it" feels faster than front-loaded thinking; batching reduces perceived overhead but increases hidden risk; slow/flaky suites and weak tests become socially tolerated to ship; delayed invisible refactor benefits make refactoring optional.
- The extracted set intentionally over-represents principles humans find hard to sustain: "run tests constantly" and "refactor as a required step" are accepted but abandoned because short-term cost is salient while benefit is delayed.
- "Tests must be self-validating" is accepted in principle, yet humans commonly ship weak (or non-assertive) tests because they are faster to write.
- The extraction targets known failure points of human-era TDD: principles requiring repeated, immediate investment to preserve long-term optionality.
- Each principle becomes a structured record with label, canonical quote (when available), human-era intent statement, and bibliographic pointer, designed as input for translating human-era discipline into enforceable AI-native governance rules.
- Figure 1 illustrates three enforceable governance principles: requiring pre-change failing tests (RED) for behavior modifications, treating refactoring as a gated phase with full-suite regression and duplication controls, and operationalizing FIRST test quality via quantitative checks for speed, determinism, self-validation, and timeliness.

---

## Table 1: Principle categories and typical human-era failure modes

| Category | Canonical principle form | Why humans dropped it under pressure [2, 19] |
|---|---|---|
| Order | Test-first and Red→Green→Refactor | Front-loads thinking and "just code it" feels faster |
| Granularity | Minimal failing test, minimal passing code, and one failing test at a time | Batching reduces perceived overhead but increases hidden risk |
| Feedback quality | FAST, independent, repeatable, self-validating, and timely tests with meaningful assertions | Slow or flaky suites and weak tests become socially tolerated to ship |
| Design hygiene | Remove duplication and refactor continuously while green | Benefits are delayed and invisible, so refactor becomes optional |

## Historically "right" but economically fragile

The extracted set intentionally over-represents principles that are difficult for humans to sustain. For example, "run tests constantly" and "refactor as a required step" are widely accepted, but frequently abandoned because the short-term cost is salient while the benefit is delayed. Similarly, "tests must be self-validating" is accepted in principle, yet humans commonly ship weak tests (or non-assertive tests) because they are faster to write. In other words, the extraction targets the known failure points of human-era TDD: principles that require repeated, immediate investment to preserve long-term optionality.

## Outputs and representation

The outcome of this step is a curated list of principles representing the bounded canonical TDD corpus used in this study. Each principle is represented as a structured record containing: a label, a canonical quote (when available), a human-era intent statement, and a bibliographic pointer. This representation is designed as the input to the next step: translating human-era discipline into AI-native governance rules that autonomous or semi-autonomous systems can ingest and enforce.

## Figure 1: enforceable governance principles

Figure 1 illustrates three enforceable governance principles: requiring pre-change failing tests (RED) for behavior modifications, treating refactoring as a gated phase with full-suite regression and duplication controls, and operationalizing FIRST test quality via quantitative checks for speed, determinism, self-validation, and timeliness.

Manifesto source: https://github.com/shahbazsiddeeq/TDD-manifesto/blob/main/tdd_principles_manifesto.json

**Covers:** Principle extraction method, order/granularity/feedback/hygiene categories, machine-readable manifesto
