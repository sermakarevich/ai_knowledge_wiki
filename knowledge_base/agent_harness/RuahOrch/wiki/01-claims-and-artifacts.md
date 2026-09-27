> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Claims, Artifacts, and Contract Enforcement
**In one sentence:** Ruah isolates concurrent tasks with declared owned, shared-append, and read-only file globs, records what each task changed as a durable artifact, and validates those changes against the declared contract after execution.
## Key points
- A `ClaimSet` declares three glob lists — `ownedPaths`, `sharedPaths`, and `readOnlyPaths` — with optional `ownedSymbols` and `sharedInterfaces`, normalized by backslash-to-slash conversion, trimming, trailing-slash removal, and deduplication (`claims.ts:3-9`, `claims.ts:45-59`, `claims.ts:69-80`).
- Path-to-claim matching checks buckets in fixed precedence — owned, then shared-append, then read-only — using `patternsOverlap` or `matchesPattern`, and returns the first matching bucket and pattern or null (`claims.ts:155-163`, `claims.ts:165-186`).
- Overlap detection compares every pattern pair across two claim sets with `patternsOverlap` and returns both overlapping patterns, while scope checking requires every child pattern to overlap at least one parent pattern unless the parent set is empty (`claims.ts:188-206`, `claims.ts:208-231`).
- A `TaskArtifact` stores `schemaVersion`, `taskName`, `workspaceId`, resolved `baseRef`, `headRef`, `commitSha`, `changedFiles`, full `patch`, `createdAt`, embedded `claims`, and a `validation` triple of `executorSuccess`, `contractSuccess`, and optional `gatesSuccess` (`artifact.ts:5-21`, `artifact.ts:38-63`).
- Contract validation lists changed files against the base ref, accepts files matching `ownedPaths`, rejects any change to a `readOnlyPaths` match as a `read-only` violation, and rejects any other changed file as `outside-contract` (`contract-validator.ts:104-131`, `contract-validator.ts:150-162`).
- Shared-path changes are accepted only if append-only: a missing base version passes, deletion or move fails, identical content passes, and modified content must start with the original bytes without reducing line count, otherwise a `shared-append` violation is recorded (`contract-validator.ts:47-84`, `contract-validator.ts:131-148`).
- `ClaimSource` with `owned`, `sharedAppend`, and `readOnly` keys and `FileContract` with `claims` or `owned`/`sharedAppend`/`readOnly` fields are both converted to the canonical `ClaimSet` before validation, and `artifactPresent` treats an artifact as non-empty only when `changedFiles` or `patch` is non-empty (`claims.ts:17-21`, `contract-validator.ts:86-102`, `artifact.ts:72-77`).
---
## Claim scopes: owned, shared, and read-only globs
A claim is a set of path globs in three buckets (`claims.ts:3-9`). `ownedPaths` grants exclusive write access, `sharedPaths` grants append-only write access, and `readOnlyPaths` grants read access with no writes (`claims.ts:165-186`, `contract-validator.ts:114-148`). Construction helpers map a file list to read-only when `lockMode` is `read` and to owned when `lockMode` is `write` (`claims.ts:82-99`), map a path list to owned (`claims.ts:101-103`), and convert either a `ClaimSet` or a `ClaimSource` with `owned`/`sharedAppend`/`readOnly` keys into a normalized `ClaimSet` (`claims.ts:105-121`). Normalization applies `normalizePathPattern` and `unique` to each list (`claims.ts:45-59`, `claims.ts:69-80`). Conversion back to buckets preserves the three lists separately (`claims.ts:123-136`), while conversion to a flat file list merges all three buckets with deduplication (`claims.ts:138-149`).
### Matching precedence
`claimMatchesPattern` returns true when either `patternsOverlap` or `matchesPattern` matches (`claims.ts:155-163`). `findClaimMatch` iterates `ownedPaths` first, then `sharedPaths`, then `readOnlyPaths`, and returns the bucket and pattern of the first match (`claims.ts:165-186`).
```ts
// claims.ts:165-186
export function findClaimMatch(
	claims: ClaimSet,
	path: string,
	repoRoot?: string,
): ClaimMatchResult {
	for (const pattern of claims.ownedPaths) {
		if (claimMatchesPattern(pattern, path, repoRoot)) {
			return { bucket: "owned", pattern };
		}
	}
	for (const pattern of claims.sharedPaths) {
		if (claimMatchesPattern(pattern, path, repoRoot)) {
			return { bucket: "shared-append", pattern };
		}
	}
	for (const pattern of claims.readOnlyPaths) {
		if (claimMatchesPattern(pattern, path, repoRoot)) {
			return { bucket: "read-only", pattern };
		}
	}
	return { bucket: null, pattern: null };
}
```
## Compatibility checks
The examined sources define the compatibility signal as data, not the computation that produces it (`claims.ts:33-43`). `CompatibilitySignal` carries `clean`, optional `staleBase`, optional `needsReplay`, optional `conflictingFiles`, optional `comparedAgainst` with `baseRef` and `taskName`, and optional `checkedAt` (`claims.ts:33-43`). Overlap and scope helpers provide the pattern-level inputs such checks use: `claimSetsOverlap` reports pairs of patterns that overlap across two sets (`claims.ts:188-206`), and `claimSetWithinScope` reports child patterns that do not overlap any parent pattern, with an empty parent set allowing everything (`claims.ts:208-231`).
## Artifact capture: contents and storage
`buildTaskArtifact` resolves the base ref to a commit SHA when possible, collects `changedFiles` and `patch` from the workspace provider against that base, reads the current head and commit SHA, and returns a `TaskArtifact` with `schemaVersion: 1`, timestamps from `new Date().toISOString()`, embedded `claims` or null, and the caller-supplied `validation` input (`artifact.ts:38-63`). `captureTaskArtifact` is a direct delegation to `buildTaskArtifact` (`artifact.ts:65-70`). The stored record therefore contains identity (`taskName`, `workspaceId`), history pointers (`baseRef`, `headRef`, `commitSha`), content (`changedFiles`, `patch`), the claim set in force, and the validation outcome (`artifact.ts:5-21`). `artifactPresent` returns true only when `changedFiles` is non-empty or `patch` is non-empty (`artifact.ts:72-77`). The three examined files define artifact construction and shape; the state-file write path itself is not defined in these files (`artifact.ts:38-63`).
```ts
// artifact.ts:38-63
export function buildTaskArtifact(
	provider: WorkspaceProvider,
	options: ArtifactBuildOptions,
): TaskArtifact {
	const { taskName, workspace, baseRef, repoRoot, claims, validation } =
		options;
	const resolvedBaseRef = getCommitSha(baseRef, repoRoot) || baseRef;
	const changedFiles = provider.changedFiles(workspace, baseRef, repoRoot);
	const patch = provider.patch(workspace, baseRef, repoRoot);
	const headRef = provider.currentHead(workspace, repoRoot);
	const commitSha = getCurrentCommit(workspace.root) || headRef;

	return {
		schemaVersion: 1,
		taskName,
		workspaceId: workspace.id,
		baseRef: resolvedBaseRef,
		headRef,
		commitSha,
		changedFiles,
		patch,
		createdAt: new Date().toISOString(),
		claims: claims || null,
		validation,
	};
}
```
## Contract validation and enforcement
`validateContractChanges` takes a `FileContract` or `ClaimSet`, worktree path, repo root, and base ref, lists changed files against the base, converts the contract to a canonical `ClaimSet` via `contractToClaims`, and validates each file in owned, read-only, shared, outside-contract order (`contract-validator.ts:90-113`). Owned matches skip further checks (`contract-validator.ts:114-118`). Read-only matches produce a `read-only` violation with the message `read-only file was modified` (`contract-validator.ts:120-129`). Shared matches run `validateAppendOnlyChange` and produce a `shared-append` violation when that check fails (`contract-validator.ts:131-148`). Files matching no bucket produce an `outside-contract` violation with the message `changed file is outside the task contract` (`contract-validator.ts:150-156`). The result returns `valid` as true only when the violations list is empty, alongside the full `changedFiles` list (`contract-validator.ts:158-163`).
### Read-only and shared-append semantics
Shared-append validation reads the file version at the base ref and compares it to the worktree file (`contract-validator.ts:47-66`). A null base version passes, a deleted or moved file fails with `shared file was deleted or moved`, and identical content passes (`contract-validator.ts:53-67`). Changed content must start with the original bytes and must not reduce the line count, otherwise it fails with `modifies existing content instead of only appending` or `removes existing content instead of only appending` (`contract-validator.ts:69-81`). Line counting normalizes CRLF to LF and handles a trailing newline (`contract-validator.ts:38-45`). Violation reports are formatted as `file (pattern): details` lines, omitting the pattern segment when null (`contract-validator.ts:165-172`).
### Rejection before start and after execution
Pattern-level rejection before execution uses `claimSetsOverlap` and `claimSetWithinScope`: overlapping creation-time patterns and child patterns outside the parent scope are detectable before any agent starts (`claims.ts:188-206`, `claims.ts:208-231`). Post-execution enforcement uses `validateContractChanges`, which rejects read-only edits, non-append shared edits, and out-of-contract files after the run (`contract-validator.ts:104-163`).
**Covers:** packages/core/src/core/{claims,artifact,contract-validator}.ts @ 58c4ee5b
