> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Benchmark Construction Pipeline
**In one sentence:** MSI-Bench builds multi-speaker test cases across eight real-world domains through a four-stage pipeline — inputs, planner-script planning, dialogue plus tool/rubric generation, and TTS-plus-mixing synthesis — gated by structural, schema, and semantic checks, yielding 1,152 hand-reviewed cases from 1,420 candidates as 24-kHz mono PCM16 WAV files.
## Key points
- Eight behavior-setting domains are covered: commerce service; domestic household; education learning; healthcare caregiving accessibility; leisure media social; mobility transportation; public civic; and work professional, inspired by Barker's ecological framework (Barker 1968).
- Each scene fixes participants' identities, relationships, roles, and responsibilities, so the correct assistant behavior depends on the full scene rather than the wording of the final request.
- Cases are generated in four stages (Figure 2): 1. Inputs, 2. Planning, 3. Generation, 4. Synthesis, each with structural gates that return violations for correction.
- Evaluation targets are derived from the primary goal and generated dialogue: the atomic rubric and reference answer, plus the available-function schema with gold tool calls; the catalog also carries decoy functions.
- Tool arguments are closed domains (enumerations for categorical slots, bounded numeric ranges, canonical clock-time/date formats, stable speaker references Si indexed by order of first appearance), and gold tool calls must type-check against the declared schema.
- Synthesis uses Boson Higgs TTS 3 with custom voices cloned from human-validated Common Voice 17.0 clips, three listener-relative distances via gain attenuation plus low-pass filtering plus reverberation, an ASR/energy gate requiring agreement with Higgs-audio-v3-stt, and mixing over Freesound beds with Qwen3-ForcedAligner-0.6B timestamps, ESC-50 / UrbanSound8K burst events cropped to loudest RMS window with 50-ms edge fades.
- Final yield after hand review: 1,152 passed of 1,420 generated candidates constitute the benchmark.
---
## Eight domains and scene grounding
Inspired by Barker's ecological framework of behavior settings (Barker 1968), test cases span eight real-world domains: commerce service; domestic household; education learning; healthcare caregiving accessibility; leisure media social; mobility transportation; public civic; and work professional.

Each setting establishes the participants' identities, relationships, roles, and responsibilities, which determine whose information and constraints apply, who may authorize an action, and which requirements take priority; the correct next-assistant behavior therefore depends on the full scene rather than the wording of the final request.

## Four-stage pipeline overview
Cases are generated in four stages (Figure 2): 1. Inputs, 2. Planning, 3. Generation, 4. Synthesis.

## 1. Inputs
Each test case starts from metadata fixing speaker count, language, and topic, together with an interaction pattern, a scene, and the list of acoustic assets belonging to that scene.

## 2. Planning
A planner LLM turns these inputs into a script. It first instantiates the cast: each speaker receives a name, a scene role, a gender, an age bucket, and a permission set if needed. Gender and age bucket later select the voice pool at synthesis, so the plan fixes speaker identity before any line exists.

The planner then sketches a storyline that pins down how information surfaces, leaving exact wording to the next stage. Alongside the script, the plan states the primary goal the assistant is expected to serve and selects the background-audio bed the scene is later mixed over.

A structural gate checks the result against the sampled parameters (e.g., the participant roster matches the sampled speaker count) and returns violations to the planner for correction.

## 3. Generation
A lines-generation LLM expands the script into a multi-turn dialogue ending in an assistant-directed handoff. A Tool & Rubric design LLM then derives the evaluation targets from the primary goal and the generated dialogue: the atomic rubric and reference answer, and the available-function schema together with the gold tool calls.

The catalog also carries decoy functions. Arguments are declared as closed domains: enumerations for categorical slots, bounded ranges for numbers, canonical formats for clock times and dates, and the stable speaker references Si in place of spelled names, where i indexes speakers by order of first appearance in the conversation.

Rubric dimensions are fixed per pattern; the criteria filling them are case-specific, disjoint, and each states the minimum condition for a correct answer. A further structural gate requires gold tool calls to type-check against the declared schema. Finally, all text artifacts pass through a semantic verifier that gates answer leakage and checks that the gold answer and tool call are unique.

## 4. Synthesis
TTS renders each line under its planned speaker identity, using Boson Higgs TTS 3 (Boson AI Team 2026) with custom voices cloned from human-validated Common Voice 17.0 reference clips (Ardila et al. 2020) to diversify speakers across language, gender, age, and accent. Inline emotion, style, and prosody tags steer delivery.

Each speaker is placed at one of three listener-relative distances by a deterministic signal-processing chain: gain attenuation, low-pass filtering, and a reverberant reflection. An ASR/energy gate screens every clip for anomalous pauses and requires transcription agreement with Higgs-audio-v3-stt (Boson AI 2026).

Mixing finally combines the accepted speech with the planned background audio, drawn from Freesound assets (Font, Roma, and Serra 2013), while word-level timestamps from Qwen3-ForcedAligner-0.6B (Shi et al. 2026) anchor loudness-calibrated distant speech overlays, insert burst events between words, and truncate interrupted lines at word boundaries. Burst events are real recordings drawn from ESC-50 (Piczak 2015) and UrbanSound8K (Salamon, Jacoby, and Bello 2014), cropped to their loudest RMS window with 50-ms edge fades. All rendered audio is emitted as 24-kHz mono PCM16 WAV files.

## Human review yield
Every case was additionally reviewed by hand: of 1,420 generated candidates, 1,152 passed and constitute the final benchmark.

**Covers:** Section 3.2 Benchmark Construction (four-stage pipeline, stages 1–4) through Section 4–5 spillover in chunk (evaluation protocol, metrics, Table 1 overall results)
