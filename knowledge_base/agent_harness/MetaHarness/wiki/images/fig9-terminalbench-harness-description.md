**Figure 9 — "Discovered TerminalBench‑2 harness."** This is not a quantitative plot; it has no axes or trends. It is a top‑to‑bottom flowchart (with one conditional feedback loop) describing the agent‑execution pipeline, with color coding that distinguishes inherited components (green) from the newly discovered one (red).

**Pipeline (top → bottom):**
1. **Task instruction** (neutral/indigo box) — entry point.
2. **Env bootstrap** (red) — collects a sandbox snapshot: `pwd`, files, languages, package managers, memory.
3. **Initial prompt** (green) — task + the bootstrap snapshot.
4. **Agent loop** (green) — native tool calling with an ~30 KB output cap.
5. **Multi‑perspective completion checklist** (green) — gates the outcome.
   - **pass** → **Task complete**.
   - **fail** → curved arrow loops back to the **Agent loop** (retry).

**Takeaway:** The harness reuses Terminus‑KIRA's native tool calling, output cap, and completion checklist (the green stages). The red **environment‑bootstrap** stage is the component Meta‑Harness discovers: by gathering the sandbox snapshot *before* the agent loop starts, it removes the ~2–4 early exploratory turns the agent would otherwise spend probing the environment. The text notes this is most valuable on tasks with tight turn budgets or non‑obvious environments, where those wasted early turns can flip an outcome between pass and fail.

*(Note: the surrounding page text below the figure is unrelated dataset documentation — OOD text‑classification benchmarks such as SciCite, FiNER‑139, Amazon Reviews, Financial PhraseBank — and is not part of Figure 9.)*