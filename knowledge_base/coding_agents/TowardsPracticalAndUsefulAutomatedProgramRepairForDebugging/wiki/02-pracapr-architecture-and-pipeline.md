> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# PracAPR Architecture and Pipeline
**In one sentence:** PracAPR is an envisioned IDE-integrated repair system that, starting from a debugger-stopped program and a developer-provided problem specification, performs test-free fault localization, local plus global patch generation, and re-execution-free patch validation to present previewable repair suggestions.
## Key points
- PracAPR is designed to work in conjunction with an IDE debugger, assuming the program is stopped at a location where a problem is observed.
- It interacts with the developer to obtain a description of the problem (the problem specification) and drives fault localization, patch generation, and patch validation from that description.
- It removes the unrealistic test-suite assumption: it does not assume the existence of a test suite and does not require program re-execution.
- Fault localization is flow-analysis-based and takes into account the problem symptom, current values from the debugger, and the current runtime stack to compute a backward slice containing potential repair locations.
- Patch generation is split into local and global repair, to be discussed later in the source.
- Patch validation generates simulated traces via a live programming mechanism that reflect the real executions of the original and repaired programs, then compares the traces to infer patch correctness.
- The developer can choose to preview any of the repairs and further accept it to allow changes to be applied to the program.
---
## An envisioned repair system for 2030
The chunk introduces Section 2, "AN ENVISIONED REPAIR SYSTEM FOR 2030", and states:

> "We envision a repair system PracAPR that addresses the aforementioned challenges and provides quick repair suggestions for realistic debugging. Figure 1 shows an overview of PracAPR."

Figure 1 is captioned "An overview of the PracAPR repair system" and its pipeline is labeled as steps 1–5 inside an Integrated Development Environment (IDE):

| Step | Label in Figure 1 | Role |
|---|---|---|
| 1 | Problem Specification | Developer describes the observed problem |
| 2 | Test-Free Fault Localization | From Problem Specification to Repair Locations |
| 3 | Patch Generation | Local and global repair branches |
| 4 | Program Re-execution-Free Patch Validation | Validated Patches |
| 5 | Patch Presentation | Patches for Preview |

The two generation branches shown in the figure are "LLM-Based Local Repair" and "Tailored Strategy-Driven Global Repair".

## Test-free fault localization
Verbatim mechanism from the chunk:

> "Without a test suite, PracAPR performs flow-analysis-based fault localization while taking into account the problem symptom, current values from the debugger, and the current runtime stack to compute a backward slice containing potential repair locations."

The chunk also states the operating assumptions:

> "It works in conjunction with an IDE debugger and assumes that the program is stopped at a location where a problem is observed."

> "PracAPR interacts with the developer to obtain a description of the problem and performs test-free fault localization, patch generation, and patch validation based on the description (the problem specification) to generate repair suggestions."

The opening fragment reinforces the IDE-integration goal: "if integrated into an IDE to provide repair suggestions, is highly expected to be quick."

## Patch generation: local and global repair
The chunk defers details but defines the split:

> "Patch generation is done with local and global repair, which we will discuss later."

No exact patch counts, repair rates, or model names for PracAPR itself appear in this chunk.

## Re-execution-free patch validation and presentation
Verbatim mechanism from the chunk:

> "Patch validation does not require program re-execution. Instead, PracAPR generates via a live programming mechanism simulated traces that reflect the real executions of the original and repaired programs and compares the traces to infer patch correctness."

Presentation behavior:

> "Finally, PracAPR presents the repair suggestions to the developer. The developer can choose to preview any of the repairs and further accept it to allow changes to be applied to the program."

**Covers:** Section 2, PracAPR overview in IDE, test-free fault localization, patch generation and validation pipeline (Figure 1)
