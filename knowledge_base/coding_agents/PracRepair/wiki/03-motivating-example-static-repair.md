> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Bug Information & A. Repairing with Static
**In one sentence:** The chunk presents the Compress-21 `writeBits` bug information (failing test, failure message, and buggy code) and shows the static-only repair attempt that reasons from program context and targeted questions without execution traces.
## Key points
- The failing test is `testSevenEmptyFiles`, which calls `testCompress252(7, 0)`, and the reported failure is `java.io.IOException: Unknown property 128`.
- The buggy method is `writeBits(final DataOutput header, final BitSet bits, final int length)`, initialized with `int cache = 0` and `int shift = 7`.
- The in-loop logic does `cache |= ((bits.get(i) ? 1 : 0) << shift)`, then `--shift`, and flushes with `if (shift == 0) { header.write(cache); shift = 7; cache = 0; }`.
- The after-loop logic flushes leftovers with `if (length > 0 && shift > 0) { header.write(cache); }`.
- The static-context repair task is framed as `## Task: generate a corrected patch...` with `## Input: Bug_Info, Program_Context`.
- The static program context supplies `testCompress252`, imports (`DataOutput`, `DataOutputStream`, `File`, `org.apache.commons.compress.archivers`), `writeFileEmptyFiles`, the `writeBits(out, emptyFiles, emptyStreamCounter)` call, and `out.flush()`.
- Diagnosis in this pane answers `What are cache and shift when if (shift == 0) is entered?` with `When branch is entered, cache = 254 and shift = 0 after i = 6`.
- The static repair proposes masking and a final-flush change: `Writing cache directly may produce invalid data, so use cache & 0xFF to keep only the lower 8 bits`, and `Change 'shift > 0' to 'shift < 8' to ensure any remaining cached bits are flushed after writing`, yielding `if (length > 0 && shift < 8 ) { header.write(cache); }`.
---
## Bug Information
**Covers:** Fig. 1 motivating example based on Compress-21 — test suite, failure info, and buggy code pane.

| Field | Exact content from chunk |
|---|---|
| Test Suite | `public void testSevenEmptyFiles() throws Exception { testCompress252(7, 0); }` |
| Failure Info | `java.io.IOException: Unknown property 128` |
| Buggy Code (lines 01–16) | `01 private void writeBits(final DataOutput header, final BitSet bits, final int length) throws IOException {` / `02 int cache = 0;` / `03 int shift = 7;` / `04 for (int i = 0; i < length; i++) {` / `05 cache \|= ((bits.get(i) ? 1 : 0) << shift);` / `06 --shift;` / `07 if (shift == 0) {` / `08 header.write(cache);` / `09 shift = 7;` / `10 cache = 0;` / `11 }` / `12 }` / `13 if (length > 0 && shift > 0) {` / `14 header.write(cache);` / `15 }` / `16 }` |

Verbatim failure quote:

> `java.io.IOException: Unknown property 128`

## A. Repairing with Static Context
**Covers:** Fig. 1 column A — task/input framing, static program context, and static-only fix suggestion.

Task/input framing (verbatim):

> `## Task: generate a corrected patch...`
> `## Input: Bug_Info, Program_Context`

Static program context (exact items present in chunk):

| Item | Exact content from chunk |
|---|---|
| Test helper | `private void testCompress252(int numberOfFiles, int numberOfNonEmptyFiles) throws Exception { ... verifyCompress252(output, numberOfFiles, numberOfNonEmptyFiles);}` |
| Imports | `import java.io.DataOutput;` / `import java.io.DataOutputStream;` / `import java.io.File;` / `import org.apache.commons.compress.archivers.` |
| Call site | `private void writeFileEmptyFiles(final DataOutput header) throws IOException { ... writeBits(out, emptyFiles, emptyStreamCounter); out.flush(); ...}` |

Question-driven diagnosis inside the static pane (verbatim):

> `What are cache and shift when if (shift == 0) is entered?`
> `When branch is entered, cache = 254 and shift = 0 after i = 6`
> `Writing cache directly may produce invalid data, so use cache & 0xFF to keep only the lower 8 bits.`
> `if (shift == 0) { header.write(cache & 0xFF); ... }`

Proposed static fix (verbatim):

> `Change 'shift > 0' to 'shift < 8' to ensure any remaining cached bits are flushed after writing.`
> `if (length > 0 && shift < 8 ) { header.write(cache); }`

**Covers:** Compress bug illustration and static-only repair attempt (Fig. 1, Bug Information + column A panes).
