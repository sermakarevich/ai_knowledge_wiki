> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Simulated Instrumentation: Adding Debugging Print Statements
**In one sentence:** DebugRepair instruments the buggy Java function with debugging print statements via an LLM prompt (Fig. 4) guarded by a two-stage consistency check, falling back to deterministic rule-based AST instrumentation (Algorithm 2) before capturing a runtime trace for repair.
## Key points
- The instrumentation prompt asks the LLM to "add appropriate debugging print statements to the given Java function" given the buggy function, failing test context, and error information (Fig. 4).
- LLM-generated instrumentation may add unintended edits beyond prints (auxiliary comments, syntactic errors), so a two-stage consistency check enforces `Norm(F_inst) ≡ Norm(F_buggy)` line-wise after stripping prints/comments plus a compilation check on `F_inst`.
- If LLM instrumentation fails the checks over a maximum of `M_inst` attempts, a deterministic rule-based fallback (Algorithm 2) parses `F_buggy` to an AST and reinserts prints mechanically.
- The rule-based fallback inserts `// START_DEBUG` as the first statement, `// DEBUG [VAR] names = vals` after each variable init/assignment, and `// DEBUG [COND] cond =` before each if-condition via a temp variable `t` that replaces the condition to avoid repeated-execution side effects.
- Loops are handled by replacing the loop condition with `true` and inserting `s1` (assign `c` to `t`), `s2` (log `// DEBUG [LOOP] cond =` + `t`), and `s3` (conditional break on non-`t`) at loop entry; returns use the same temp-variable pattern (`// DEBUG [RETURN]`) or a fixed `// DEBUG [RETURN] void` for empty returns, with `// END_DEBUG` before every exit.
- Executing the verified `F_inst` in context `<T_min, D>` yields `τ_runtime = <log1, ..., logk>`, where each log records a critical variable `v ∈ V_crit` and its value before `s_fail`, revealing data-flow issues invisible from outcome-level symptoms.
---
## Instrumentation prompt (Fig. 4)
**Covers:** Fig. 4 prompt template

The template instructs:

> "Please add appropriate debugging print statements to the given Java function to help repair bugs"

Inputs supplied to the prompt:
1. Buggy function
2. Failing test context ("Test Context")
3. Error information ("Error Information")

## Two-stage consistency check
**Covers:** Section 3.3, LLM instrumentation verification

1. Line-wise equivalence after normalization: `Norm(·)` removes all print statements and comments; require `Norm(F_inst) ≡ Norm(F_buggy)` so no extra statement modifies or distorts logic.
2. Compilation check on `F_inst`: accept only if compilation succeeds without errors, since syntactic breakage can survive step 1.

## Rule-based fallback (Algorithm 2)
**Covers:** Section 3.3, Algorithm 2, pp. 111:9–111:10

Activated once LLM instrumentation fails the checks over `M_inst` maximum attempts. Procedure:

| Step (Alg. 2 lines) | Action | Verbatim log marker |
|---|---|---|
| 1–3 | `T := ParseToAST(F_buggy)`; fetch method decl `M`; `InsertPrintAfter(M, "// START_DEBUG")` | `// START_DEBUG` |
| 5–8 | For each var-init/assignment `n`: fetch names and vals, `InsertPrintAfterStmt` | `"// DEBUG [VAR] "+names.join(",")+" = "+vals.join(",")` |
| 9–13 | For each if: `c := FetchConditionExpr(n)`; `(s1,s2,t) := HandleExpr(c, "// DEBUG [COND] " + ToString(c) + " = ")`; replace condition with `t`; insert `[s1; s2]` before if | `// DEBUG [COND]` |
| 14–19 | For each while/for: replace loop condition with `true`; `s3 := GenConBreakStmt(¬t)`; `InsertStmtAtLoopEntry(n, [s1; s2; s3])` | `// DEBUG [LOOP]` |
| 20–24 | For each non-empty return: extract `c`, `HandleExpr(c, "// DEBUG [RETURN] ")`, replace return expr with `t`, insert before return | `// DEBUG [RETURN]` |
| 25–26 | For each empty return: fixed print before return | `"// DEBUG [RETURN] void"` |
| 28–31 | For each exit `r ∈ R`: `InsertPrintBeforeExit(r, "// END_DEBUG")` | `// END_DEBUG` |
| 32–33 | `F_inst := ASTToCode(T)`; return | — |

`HandleExpr(c, LOG)` (lines 34–38): create temp var `t`; `s1 := BuildTempAssignStmt(t, c)`; `s2 := GenPrintStmt(LOG + t)`; return `s1, s2, t`.

Mechanism details from the text:
- If-conditions use temp variable `t` for logging while replacing `c` with `t`, avoiding "unexpected changing of certain variables in c owing to the repeated execution."
- Loop conditions cannot reuse the if-pattern because the condition "will be repeatedly computed to examine the reachability of loop boundary," hence the replace-with-`True` plus conditional-break (`s3` using non-`t`) design.
- Non-empty returns likewise substitute `t` for `c` "thereby avoiding repeated computation."
- The authors note this instrumentation "cannot uncover targeted state updates for different F_buggy" but "still reveals critical breakpoints and variables that developers commonly inspect during debugging" and is useful "as a supplementary to LLM-based instrumentation, especially when LLM-generated code are uncompilable."

## Runtime trace capture
**Covers:** Section 3.3, Runtime Trace Capture

> "Runtime Trace Capture. Executing the verified F_inst within the context of ⟨T_min, D⟩ produces a runtime trace: τ_runtime = ⟨log1, ..., logk⟩, where each log records a critical variable v ∈ V_crit and its value val during execution before s_fail, thereby helping reveal data flow issues that cannot be identified from outcome-level failure symptoms alone."

## Transition to conversational repair (fragment in chunk)
**Covers:** Start of Section 3.4, p. 111:10–111:11 (incomplete in this chunk)

> "Leveraging the captured trace τ_runtime, DebugRepair initiates a conversational repair process."

Chunk states this phase uses a "closed-loop mechanism of generation, verification, and feedback" with a "hierarchical iterative mechanism consisting of debugging sessions and repair rounds" (`N_session` sessions, `K_round` rounds per session); each session starts with direct repair on `F_buggy` plus outcome-level symptoms, and on failure of patch `P0` with error `E0` transitions to debugging mode. Full prompting and validation details continue beyond this chunk.
**Covers:** Section 3.3 (Fig. 4 instrumentation prompt, two-stage check, Algorithm 2 rule-based fallback, runtime trace) through the opening of Section 3.4 (hierarchical iteration setup).
