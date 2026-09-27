> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Test Semantic Purification
**In one sentence:** Test semantic purification backward-slices the failing test to a minimal reproducing method plus its helper-method and field dependencies, using iterative rescans to capture alias-induced side effects missed in a single pass.
## Key points
- Backward traversal starts from the failure-triggering statement 𝑠_𝑓𝑎𝑖𝑙 and keeps a preceding statement 𝑠_𝑖 when its defined variables/objects or (for non-asserts) used objects intersect the required set 𝑉_𝑟𝑒𝑞 (Algorithm 1, Lines 13–14).
- Statements not dependent on 𝑠_𝑓𝑎𝑖𝑙 can still use objects in 𝑉_𝑟𝑒𝑞 and cause side effects that affect 𝑠_𝑓𝑎𝑖𝑙, so traversal repeats iteratively updating Slice and 𝑉_𝑟𝑒𝑞 until no new objects appear (changed flag fixed to False, Lines 18–19).
- The alias example (Fig. 3): listB is an alias of listA (L2), and `listB.add(...)` at L3 mutates their shared object, implicitly affecting listA checked by the failing assertion at L4.
- First traversal misses the L3 side effect because alias listB is not in 𝑉_𝑟𝑒𝑞 until L2 is processed; discovering listB at L2 sets changed True and triggers a second traversal that captures L3, yielding final Slice {L1, L2, L3, L4} from {L1, L2, L4}.
- The minimal test 𝑇_𝑚𝑖𝑛 is reconstructed by preserving the original method signature of 𝑇 and assembling retained Slice statements in original relative order (Line 24).
- Direct helper-method dependencies D_𝑚 are method callees of 𝑇_𝑚𝑖𝑛 defined in enclosing class C (Lines 25–26); indirect dependencies are found by iteratively intersecting callees with methods defined in C until the intersection is empty (Lines 27–31).
- Class-level field dependencies D_𝑣 are variables/objects of 𝑇_𝑚𝑖𝑛 plus D_𝑚 intersected with fields declared in C (Lines 32–33); required field and method definitions form complete external dependencies D (Line 34).
- The purified context strips irrelevant noise so later simulated instrumentation and repair focus on the failure-triggering scenario while reducing irrelevant log length.
---
## Iterative backward slicing with alias handling
**Covers:** chunk lines 3–14 (slicing rule Lines 15/17, outer loop Lines 18–19)

The inclusion rule adds 𝑠_𝑖 to Slice and expands 𝑉_𝑟𝑒𝑞 with 𝑉_𝑖 = FetchVarAndObj(𝑠_𝑖) (Lines 15, 17 in the prose reference; Algorithm 1 Lines 14–17):

> "since statements that are not dependent on 𝑠_𝑓𝑎𝑖𝑙 may also use objects in 𝑉_𝑟𝑒𝑞, making the potentially caused side effects, in turn, affect 𝑠_𝑓𝑎𝑖𝑙. Thus, we have to repeat the traversal iteratively to update Slice and 𝑉_𝑟𝑒𝑞 until no new objects appear, i.e., fixing the changed flag to False in the outer loop (Lines 18-19)."

Algorithm 1 core loop (verbatim):

| Line | Statement |
|---|---|
| 5–7 | `while 𝑐ℎ𝑎𝑛𝑔𝑒𝑑 do / 𝑐ℎ𝑎𝑛𝑔𝑒𝑑 := False / for 𝑖 := IndexOf(𝑠_𝑓𝑎𝑖𝑙, 𝑆) − 1 to 1 do` (traverse preceding statements backwards) |
| 11–12 | `𝑉_𝑑𝑒𝑓 := FetchDefinedVarAndObj(𝑠_𝑖); 𝑉_𝑢𝑠𝑒 := FetchUsedObj(𝑠_𝑖)` |
| 13–14 | `if (𝑉_𝑑𝑒𝑓 ∩ 𝑉_𝑟𝑒𝑞 ≠ ∅) ∨ (¬IsAssert(𝑠_𝑖) ∧ 𝑉_𝑢𝑠𝑒 ∩ 𝑉_𝑟𝑒𝑞 ≠ ∅) then 𝑆𝑙𝑖𝑐𝑒 := 𝑆𝑙𝑖𝑐𝑒 ∪ {𝑠_𝑖}` |
| 15–17 | `𝑉_𝑖 := FetchVarAndObj(𝑠_𝑖); 𝑉_𝑛𝑒𝑤 := 𝑉_𝑖 \ 𝑉_𝑟𝑒𝑞; 𝑉_𝑟𝑒𝑞 := 𝑉_𝑟𝑒𝑞 ∪ 𝑉_𝑖` |
| 18–19 | `if ∃𝑣 ∈ 𝑉_𝑛𝑒𝑤 such that IsObject(𝑣) then 𝑐ℎ𝑎𝑛𝑔𝑒𝑑 := True` |

## Motivating alias example (Fig. 3)
**Covers:** chunk lines 6–32 (Figure 3 and two-round traversal table)

Code snippet (verbatim):

| Line | Code |
|---|---|
| L1 | `List<String> listA = new ArrayList<>();` |
| L2 | `List<String> listB = listA;` |
| L3 | `listB.add("Bug Trigger!");` |
| L4 | `assertEquals(1, listA.size()); // s_fail` |

Traversal comparison from the chunk table:

| Round | L1 action | L2 action | L3 action | L4 action | Slice after round |
|---|---|---|---|---|---|
| First | Add L1 (𝑉_𝑟𝑒𝑞 {listA, listB}) | Set changed = True | Skip L3 (`listB ∉ 𝑉_𝑟𝑒𝑞`) | Add L4 | {L1, L2, L4} |
| Second | Already in Slice | Already in Slice | Capture L3 (`listB ∈ 𝑉_𝑟𝑒𝑞`) | Already in Slice | {L1, L2, L3, L4} |

> "the first traversal among the statements preceding 𝑠_𝑓𝑎𝑖𝑙 (L4) will miss the implicit state modification at L3, because the object alias listB is not introduced into 𝑉_𝑟𝑒𝑞 until L2 is processed. However, the discovery of listB as a new object at L2 triggers the changed flag from False to True and induces a second traversal."

## Minimal test reconstruction and external dependencies
**Covers:** chunk lines 33–46 and 91–96 (𝑇_𝑚𝑖𝑛, D_𝑚, D_𝑣, D)

> "we reconstruct the minimal test method, 𝑇_𝑚𝑖𝑛, by preserving the original method signature of 𝑇 and sequentially assembling the statements retained in Slice according to their original relative order (Line 24)."

Follow-up context completion (verbatim steps):

> "(1) fetching helper methods defined in C that are directly or indirectly dependent by 𝑇_𝑚𝑖𝑛; (2) fetching class-level fields that are directly or indirectly dependent by 𝑇_𝑚𝑖𝑛."

| Step | Mechanism (Algorithm 1 lines) |
|---|---|
| Direct methods | `D_𝑚 := FetchCalleeSigs(𝑇_𝑚𝑖𝑛) ∩ 𝑀_C` where `𝑀_C := FetchMethodSigs(C)` (Lines 25–26) |
| Indirect methods | `𝑀_𝑛𝑒𝑤 := D_𝑚; while 𝑀_𝑛𝑒𝑤 ≠ ∅ do 𝑀_𝑛𝑒𝑤 := FetchCalleeSigs(𝑀_𝑛𝑒𝑤) ∩ 𝑀_C; D_𝑚 := D_𝑚 ∪ 𝑀_𝑛𝑒𝑤` until intersection empty (Lines 27–31) |
| Fields | `𝑉_𝑎𝑙𝑙 := FetchVarAndObj(𝑇_𝑚𝑖𝑛) ∪ FetchVarAndObj(D_𝑚); D_𝑣 := 𝑉_𝑎𝑙𝑙 ∩ FetchDeclaredFields(C)` (Lines 32–33) |
| Final dependencies | `D := FetchDefinitions(D_𝑚, D_𝑣, C); return ⟨𝑇_𝑚𝑖𝑛, D⟩` (Lines 34–35) |

> "By stripping away irrelevant contextual noise, this purified context ensures that the subsequent simulated instrumentation and repair are focused exclusively on the failure-triggering scenario, while reducing the length of irrelevant logs."

**Covers:** Test Semantic Purification section through Algorithm 1 (chunk lines 3–96; Fig. 3; Algorithm 1 Lines 1–35), excluding the Simulated Instrumentation section that begins at chunk line 101.
