> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Lineage, Receipts, and the Audit Chain
**In one sentence:** Bernstein records what each agent wrote as hash-chained, HMAC-tagged (HMAC = Hash-based Message Authentication Code) rows in append-only JSONL (JSONL = one JSON object per line) files, and signs selected records with Ed25519 (Ed25519 = a digital-signature algorithm) so they verify offline.
## Key points
- The lineage spine is always on: every adapter artifact write routes through `LineageSpine.record`, while the HMAC audit chain is opt-in at runtime via `BERNSTEIN_AUDIT=1` (src/bernstein/core/lineage/spine.py:12, src/bernstein/core/orchestration/orchestrator.py:1061, src/bernstein/core/security/AGENTS.md:29).
- Each spine entry chains `entry_hash = H(prev_hash, artifact_path, content_hash, ...)` and carries an HMAC tag made with the audit-chain key, and `verify` recomputes the whole chain plus every tag (src/bernstein/core/lineage/spine.py:18, src/bernstein/core/lineage/spine.py:21, src/bernstein/core/lineage/spine.py:612).
- The per-run replay journal is a separate Merkle chain with `event_hash = H(prev_hash, event_type, payload_hash, monotonic_index)`, and its head is sealed into the spine at run finalization (src/bernstein/core/replay/journal.py:14, src/bernstein/core/replay/journal.py:1265).
- Signed lineage entries add attributable non-repudiation on top of the spine: an Ed25519 detached JWS (JWS = JSON Web Signature) over canonical bytes plus an operator-HMAC envelope over every field (src/bernstein/core/lineage/signed_write.py:16, src/bernstein/core/lineage/entry.py:4).
- Evidence bundles bind task-producer outputs into one signed, spine-anchored record stored content-addressed (address = content hash) under a per-blob 1 MiB cap, mirrored into the HMAC audit chain (src/bernstein/core/evidence/bundle.py:104, src/bernstein/core/evidence/bundle.py:114, src/bernstein/core/evidence/bundle.py:703).
- Offline verification needs no orchestrator and no network: the `verify_cli` wheel checks Ed25519 signatures, parent-hash linkage, and canonical bytes using only the pack plus `cryptography` and `click` (verify_cli/README.md:9, verify_cli/README.md:28, verify_cli/README.md:43).
- Any one-byte change surfaces as a named hash mismatch (`entry_hash mismatch`, `hmac mismatch`, `prev_hash break`, blob-diverges messages), which is also how non-deterministic replay shows up: as a mismatch at a precise step index (src/bernstein/core/lineage/spine.py:690, src/bernstein/core/replay/journal.py:1149, src/bernstein/core/evidence/bundle.py:980).
---
## Always-on lineage spine vs opt-in HMAC chain
The spine is the single always-on Merkle-plus-HMAC store, one append-only JSONL file per run under `.sdd/lineage/<run_id>/spine.jsonl` plus a `spine.head` snapshot, and every adapter artifact write routes through it with no per-adapter opt-in (src/bernstein/core/lineage/spine.py:9, src/bernstein/core/lineage/spine.py:362).
Each entry is:
```
entry_hash = H(prev_hash, artifact_path, content_hash, actor,
               step_id, model, timestamp)
```
(src/bernstein/core/lineage/spine.py:18), and each row carries an HMAC tag computed with the existing audit-chain key (src/bernstein/core/lineage/spine.py:21). The on-disk row is canonical JSON (sorted keys, minimal separators, UTF-8), so two byte-identical runs produce byte-identical files including entry order and hashes (src/bernstein/core/lineage/spine.py:26).
The store layout and head handling:
```
_SPINE_LOG_NAME = "spine.jsonl"
_SPINE_HEAD_NAME = "spine.head"
```
(src/bernstein/core/lineage/spine.py:101), with the head recovered from the log tail so a crash-stale `spine.head` cannot lie (src/bernstein/core/lineage/spine.py:407). The wire version is:
```
SPINE_ENTRY_VERSION = 2
```
(src/bernstein/core/lineage/spine.py:83). Version 2 entries use an HKDF-derived per-store key (HKDF = HMAC-based key derivation function) with a domain tag; version 1 keeps the raw key with no domain tag (src/bernstein/core/lineage/spine.py:79, src/bernstein/core/lineage/spine.py:385).
The HMAC audit chain underneath is opt-in. The orchestrator enables it only when asked:
```
self._audit_mode = os.environ.get("BERNSTEIN_AUDIT") == "1" or (
```
(src/bernstein/core/orchestration/orchestrator.py:1061), and the security notes state the chain is opt-in at runtime via `BERNSTEIN_AUDIT=1` while features degrade without it (src/bernstein/core/security/AGENTS.md:29). The key path override is:
```
AUDIT_KEY_ENV = "BERNSTEIN_AUDIT_KEY_PATH"
```
(src/bernstein/core/security/audit.py:68), resolved before the XDG state default (src/bernstein/core/security/audit.py:165). The key file must be mode `0600` (owner read/write only); anything more readable is a hard error at load time (src/bernstein/core/security/AGENTS.md:22, src/bernstein/core/security/audit.py:71). Read-only callers use `load_audit_key` and writers use `load_or_create_audit_key` (src/bernstein/core/security/audit.py:211, src/bernstein/core/security/audit.py:242). The chain starts from:
```
_GENESIS_HMAC = "0" * 64
```
(src/bernstein/core/security/audit.py:63). The `AuditChainStore` facade exposes the head HMAC and embeds the prior digest into each new event before its HMAC is computed (src/bernstein/core/security/audit_chain.py:1090, src/bernstein/core/security/audit_chain.py:1169). Stores never share a key: each derives its own from the master by HKDF-SHA256 under a domain tag also prefixed into the hash preimage, so one store's record cannot replay against another (src/bernstein/core/security/AGENTS.md:22).
Verify outcomes are four-way, not pass/fail: `OK`, `NO_ENTRIES`, `SEAL_ONLY`, `TAMPERED` (src/bernstein/core/lineage/spine.py:294). An empty run reports `NO_ENTRIES` rather than passing trivially, and a chain holding only the internal journal-head seal reports `SEAL_ONLY` rather than `OK` (src/bernstein/core/lineage/spine.py:294, src/bernstein/core/lineage/spine.py:705). Only `OK` counts as verified (src/bernstein/core/lineage/spine.py:316).
## Replay journal
Each run also keeps one always-on Merkle-chained event log under `.sdd/runs/<run_id>/journal.jsonl`, where each event is:
```
event_hash = H(prev_hash, event_type, payload_hash, monotonic_index)
```
(src/bernstein/core/replay/journal.py:14). The `payload_hash` is taken over the canonical JSON projection with the wall-clock envelope (`ts`, `elapsed_s`) excluded, so two byte-identical executions hash identically regardless of timing (src/bernstein/core/replay/journal.py:16, src/bernstein/core/replay/journal.py:83). The head hash content-addresses the surviving journal state (src/bernstein/core/replay/journal.py:19).
At run finalization the journal head is sealed into the same run's spine so artifact provenance and replay identity share one root (src/bernstein/core/replay/journal.py:1273). The seal entry carries the head in its `step_id` under the prefix:
```
JOURNAL_SEAL_STEP_PREFIX = "replay-journal-head:"
```
(src/bernstein/core/lineage/spine.py:90), and spine verification treats a chain built only of such seals (plus artifact-attempt records) as carrying no produced-artifact provenance (src/bernstein/core/lineage/spine.py:699, src/bernstein/core/lineage/spine.py:705). When lineage is disabled the seal is a no-op returning `None` (src/bernstein/core/replay/journal.py:1282).
Journal verification walks every row, recomputing `payload_hash` and `event_hash` and checking the `prev_hash` link, reporting the first break by index (src/bernstein/core/replay/journal.py:730, src/bernstein/core/replay/journal.py:1136). Task artifact reads go fail-closed on a bad journal by default (src/bernstein/core/evidence/run_artifacts.py:622).
## Signed lineage receipts (artifact completion)
The spine proves ordering and integrity for a whole run; signed lineage entries prove attributable non-repudiation, which the spine cannot: a detached Ed25519 signature verifiable offline against a published Agent Card by someone holding no operator secret, plus an operator-HMAC envelope over every field catching post-signing substitution independently of the signature (src/bernstein/core/lineage/signed_write.py:12, src/bernstein/core/lineage/signed_write.py:16). A `LineageEntry` is one immutable record of an agent writing an artefact, and its canonical-bytes form (RFC 8785 JCS; JCS = JSON Canonicalisation Scheme) is what gets HMAC'd and Ed25519-signed (src/bernstein/core/lineage/entry.py:1, src/bernstein/core/lineage/entry.py:4). Recordable kinds form a closed set (`file`, `report`, `dataset`, `action_log`, `ops_result`, `query-result`, `external`, and others); unknown kinds raise (src/bernstein/core/lineage/entry.py:31).
The supported sealing primitive is `seal_write`: hash content, chain to the single current tip, build the entry, HMAC the canonical bytes minus the `operator_hmac` field, sign the canonical bytes as detached JWS, hand to the store (src/bernstein/core/lineage/signed_write.py:146). The signature step is:
```
def sign_detached(payload: bytes, private_key_pem: str, *, kid: str) -> str:
```
(src/bernstein/core/lineage/identity.py:179), verified by:
```
def verify_detached(payload: bytes, jws: str, card: AgentCard) -> bool:
```
(src/bernstein/core/lineage/identity.py:218), which returns False (never raises) on malformed input, mismatched key id, wrong key, or bad signature (src/bernstein/core/lineage/identity.py:218). Keypairs are created by `generate_keypair` returning `(private_pem, public_pem)` (src/bernstein/core/lineage/identity.py:122). The store round-trips with a sanity assert that the returned hash equals the recomputed entry hash (src/bernstein/core/lineage/signed_write.py:306). The old `LineageRecorder` class is only a deprecated shim over `SignedLineageLog` with identical bytes (src/bernstein/core/lineage/recorder.py:1, src/bernstein/core/lineage/recorder.py:36).
The CI gate `check` is read-only over a frozen log plus cards directory and reports whether every entry is parsable, JWS-backed against the agent's card, optionally HMAC-covered, anchored (every parent resolves), fork-free, and steward/mode-coupled where required (src/bernstein/core/lineage/gate.py:1).
The shared receipt protocol is one envelope for all receipt kinds: it names `kind`, the `canonicalization` rule, the `payload`, the payload digest, and a detached Ed25519 signature over kind-plus-payload together (src/bernstein/core/receipts/protocol.py:3). The canonicalisation tag is:
```
CANONICALIZATION_V1 = "receipt-canonical-json/v1"
```
(src/bernstein/core/receipts/protocol.py:60), meaning recursively sorted keys, compact separators, UTF-8, no ASCII escaping (src/bernstein/core/receipts/protocol.py:56). Kinds register once at import (`security.change`, planning recovery, and others); a duplicate kind raises at import time (src/bernstein/core/receipts/protocol.py:10, src/bernstein/core/receipts/kinds.py:14). `verify_receipt` is offline from the receipt alone, ordered as envelope shape, canonicalisation rule, kind registration, payload digest, signature, then the kind's own payload check (src/bernstein/core/receipts/protocol.py:319). A digest mismatch and a signature failure are reported as data, e.g. `payload_digest mismatch` and `signature: ...` (src/bernstein/core/receipts/protocol.py:355, src/bernstein/core/receipts/protocol.py:374).
Agent-posted run artifacts follow the same receipt idea per task: canonical bytes stored content-addressed, sealed into the spine (the spine entry hash is the artifact identity), an `artifact_posted` row appended to the task's Merkle-chained journal, and a best-effort mirror into the HMAC audit chain; reposting a key appends a new version referencing the prior spine hash, never an overwrite (src/bernstein/core/evidence/run_artifacts.py:9, src/bernstein/core/evidence/run_artifacts.py:715, src/bernstein/core/evidence/run_artifacts.py:758). Rendering re-checks the blob hash against the journal row, so a tampered blob displays as tampered, not as content (src/bernstein/core/evidence/run_artifacts.py:21). The per-version verify result keeps a separate `journal_identity` field because artifact bytes can verify even when no terminal-head seal identifies the complete journal (src/bernstein/core/evidence/run_artifacts.py:533).
UI render receipts are a narrower deterministic receipt: environment, layout, styles, and accessibility tree projected to sorted-JSON canonical bytes hashed with SHA-256, with a pure `render_delta` comparison that returns an explicit incomparable result (never an empty delta) when environments or vocabularies differ (src/bernstein/core/evidence/render_receipt.py:1, src/bernstein/core/evidence/render_receipt.py:405, src/bernstein/core/evidence/render_receipt.py:706).
## Evidence bundles (content-addressed)
A task declares evidence producers (test, coverage, lint, screenshot/recording, generic); at gate time they run, outputs are captured, stored content-addressed, and bound into one signed record anchored in the evidence spine (src/bernstein/core/evidence/bundle.py:8, src/bernstein/core/evidence/bundle.py:12). All bundles anchor under one dedicated run so evidence lineage never interleaves with per-task journals:
```
EVIDENCE_RUN_ID = "evidence"
```
(src/bernstein/core/evidence/bundle.py:104), stamped with schema version 1 (src/bernstein/core/evidence/bundle.py:108). Blobs live under `<root>/blobs/<hex[:2]>/<hex>` where the address is the SHA-256 of the stored bytes, so rehashing at verify time detects tampering (src/bernstein/core/evidence/bundle.py:317). The per-blob cap is:
```
DEFAULT_MAX_BLOB_BYTES = 1 << 20  # 1 MiB
```
(src/bernstein/core/evidence/bundle.py:114); the stored (capped) bytes are what the content hash and bundle bind, so replay stays byte-identical (src/bernstein/core/evidence/bundle.py:110). `gc` removes blobs no live bundle references and returns the removal count (src/bernstein/core/evidence/bundle.py:378).
The bundle binding (`schema_version`, `task_id`, `items`, `gate_passed`, `timestamp`, plus the declared-vs-produced output diff when present) is what gets signed and anchored; signature and `journal_entry_hash` are the chain-verifiable identity (src/bernstein/core/evidence/bundle.py:458, src/bernstein/core/evidence/bundle.py:480). The build path stores each output, signs media via a C2PA manifest (C2PA = Coalition for Content Provenance and Authenticity, a media-provenance manifest standard), signs the binding with the install's persisted Ed25519 identity, anchors the bytes in the evidence spine, persists the bundle, and mirrors it into the audit chain (src/bernstein/core/evidence/bundle.py:703, src/bernstein/core/evidence/bundle.py:734, src/bernstein/core/evidence/bundle.py:772, src/bernstein/core/evidence/bundle.py:803). The gate passes only if every required producer passed; advisory failures attach but never block (src/bernstein/core/evidence/bundle.py:761). The completion hook seals a bundle for each completing task but stays fail-open: tasks declaring no producers are a zero-touch no-op, and any sealing error is logged with a sanitised message while completion proceeds unchanged (src/bernstein/core/evidence/completion_gate.py:9, src/bernstein/core/evidence/completion_gate.py:62, src/bernstein/core/evidence/completion_gate.py:88).
Cross-session memory uses the same pattern as a third chain: every memory write becomes an append-only HMAC-tagged record with:
```
entry_hash = H(prev_hash, source_hash, actor, claim, model,
               timestamp, scope, namespace, kind, tombstone_of)
```
(src/bernstein/core/memory/chain.py:13), one JSONL row per write under `<root>/<scope>/<namespace>.jsonl` across the four scopes user/agent/run/app (src/bernstein/core/memory/chain.py:92, src/bernstein/core/memory/chain.py:341). Forgetting appends a signed tombstone, never deletes (src/bernstein/core/memory/chain.py:500). Verification recomputes the hash chain, every HMAC tag, and spine anchoring of each `source_hash` (src/bernstein/core/memory/chain.py:660).
## Offline verification flow (verify_cli)
The standalone auditor wheel verifies a compliance-pack ZIP without the orchestrator: every entry's Ed25519 detached JWS, the signer identity against the bundled Agent Card, parent-hash DAG (DAG = directed acyclic graph) shape with no orphans or duplicates, and byte-identical JCS reproduction (verify_cli/README.md:9). The install/run is:
```
pip install bernstein-verify
bernstein-verify pack ./acme-compliance-2026-q2.zip
```
(verify_cli/README.md:24), with subcommands for `pack`, `chain`, and `forks` (verify_cli/README.md:37). It reports `0` PASS / `1` FAIL with a JSON report on stderr and a human summary on stdout (verify_cli/README.md:43). The package does not import `bernstein.*` at runtime and imports only `cryptography`, `click`, and the standard library, with no code path opening a network socket (verify_cli/README.md:28, verify_cli/README.md:46).
The same offline property holds inside the repo: `verify_receipt` is a function of the receipt bytes only (no clock, no network, no local state), so two holders of the same receipt reach the same verdict (src/bernstein/core/receipts/protocol.py:16). Evidence verification recomputes from the stored bundle and blobs alone: the Ed25519 signature over the canonical binding, the whole evidence spine plus the bundle's anchor, every blob hash against the manifest, and media C2PA manifests against stored media bytes (src/bernstein/core/evidence/bundle.py:899, src/bernstein/core/evidence/bundle.py:907). `bernstein audit verify` runs the same bundle check across every bundle directory entry (src/bernstein/core/evidence/bundle.py:988).
## Hash-mismatch surfacing of non-determinism
Every layer reports divergence with the position attached. The spine flags a broken link, a wrong content hash, or a wrong tag:
```
errors.append(f"line {line_no}: entry_hash mismatch")
```
(src/bernstein/core/lineage/spine.py:690) and:
```
errors.append(f"line {line_no}: hmac mismatch")
```
(src/bernstein/core/lineage/spine.py:694), with `prev_hash break (expected ..., got ...)` for linkage (src/bernstein/core/lineage/spine.py:669). The journal reports `step {i}: prev_hash break` versus `step {i}: event_hash mismatch` so an operator sees exactly which step diverged (src/bernstein/core/replay/journal.py:1149). Because wall-clock fields are excluded from the payload hash, a mismatch at a step means the executed content differed, not the timing; replay divergence therefore surfaces as a hash mismatch at a precise step index rather than silent drift (src/bernstein/core/replay/journal.py:16, src/bernstein/core/replay/journal.py:19). The memory chain mirrors the same three errors plus unsupported versions and dangling `source_hash` pointers (src/bernstein/core/memory/chain.py:719, src/bernstein/core/memory/chain.py:742, src/bernstein/core/memory/chain.py:753).
Evidence verification names the offending item: stored-blob bytes are rehashed with `content_hash_of` against the manifest, and diverged names are joined into:
```
reason=f"evidence file(s) diverge from the sealed bundle: {names}",
```
(src/bernstein/core/evidence/bundle.py:980), alongside `signature does not verify (...)`, `bundle is not anchored in the evidence spine`, and `recorded journal_entry_hash does not match the spine anchor over the bundle bytes` (src/bernstein/core/evidence/bundle.py:934, src/bernstein/core/evidence/bundle.py:950, src/bernstein/core/evidence/bundle.py:952). Run-artifact verification checks the journal chain, the blob rehash, the spine anchor, and the binding between them, e.g. `blob content hash ... does not match journal row ...` and `spine anchor binds ..., journal row says ...` (src/bernstein/core/evidence/run_artifacts.py:1002, src/bernstein/core/evidence/run_artifacts.py:1009, src/bernstein/core/evidence/run_artifacts.py:1014).
## Audit JSONL shape
The on-disk audit log is daily-rotated JSONL whose chain crosses file boundaries (src/bernstein/core/security/AGENTS.md:9). The snapshot test locks the field layout: deterministic fields `event_type`, `actor`, `resource_type`, `resource_id`, `details` plus masked `timestamp`, `hmac`, `prev_hmac` (tests/snapshot/test_audit_jsonl_snapshot.py:108). Each row therefore links to its predecessor via `prev_hmac` and authenticates via `hmac`, which is what `AuditChainStore.prev_chain_digest` exposes as the chain head (src/bernstein/core/security/audit_chain.py:1153). Fork-resolution decisions are also JSONL: one row per event under `.sdd/lineage/merge-audit.jsonl`:
```
DEFAULT_AUDIT_RELPATH = Path("lineage") / "merge-audit.jsonl"
```
(src/bernstein/core/lineage/audit.py:39), carrying `event`, `timestamp`, `artefact_path`, `policy`, `winner_hash`, `candidate_hashes`, `parent_hash`, `reason` (src/bernstein/core/lineage/audit.py:43). The emitter path is tolerant: with no hook infrastructure wired in, the helper still appends the JSONL row so the decision stays recoverable (src/bernstein/core/lineage/audit.py:8). DSSE (DSSE = Dead Simple Signing Envelope, a standard signature wrapper) and in-toto envelopes can wrap a chain range for offline receipt projection, binding the chain-head event against the range's event tree (src/bernstein/core/security/AGENTS.md:11).
**Covers:** src/bernstein/core/lineage/spine.py, src/bernstein/core/lineage/entry.py, src/bernstein/core/lineage/signed_write.py, src/bernstein/core/lineage/identity.py, src/bernstein/core/lineage/gate.py, src/bernstein/core/lineage/audit.py, src/bernstein/core/lineage/recorder.py, src/bernstein/core/receipts/protocol.py, src/bernstein/core/receipts/kinds.py, src/bernstein/core/evidence/bundle.py, src/bernstein/core/evidence/run_artifacts.py, src/bernstein/core/evidence/render_receipt.py, src/bernstein/core/evidence/completion_gate.py, src/bernstein/core/memory/chain.py, src/bernstein/core/replay/journal.py, src/bernstein/core/security/audit.py, src/bernstein/core/security/audit_chain.py, src/bernstein/core/security/AGENTS.md, src/bernstein/core/orchestration/orchestrator.py, verify_cli/README.md, tests/snapshot/test_audit_jsonl_snapshot.py
