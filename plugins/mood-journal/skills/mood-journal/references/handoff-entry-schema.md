# Handoff entry schema and adapter contract

This is the clean handoff entry schema. [select_handoff.py](../scripts/select_handoff.py) implements `validate_entry` for field validation and `select` for cross-entry validation. No external schema engine or Python runtime is required by the skill; hosts using native tools enforce the same contract.

## Required fields

| Field | Constraint |
| --- | --- |
| `entry_type` | Exactly `therapist_handoff`. |
| `entry_id` | Stable entry ID or backend record ID. If unavailable, derive the disclosed identity from `immutable_path` and `checksum`. |
| `journal_id` | Nonempty selected journal identity, scoped to the authorized user/destination. |
| `handoff_series_id` | Nonempty stable series identity, independent of title or storage location. |
| `handoff_series_title` | Nonempty exact series title, including the period when applicable. |
| `handoff_sequence` | Positive integer; booleans and numeric strings are rejected. |
| `title` | Exactly `<handoff_series_title> — Entry <handoff_sequence>`. |
| `predecessor_entry_id`, `predecessor_entry_title` | Both required for sequence greater than 1; both absent or null for Entry 1. Exact match to the preceding validated entry, no self-reference. |
| `coverage_start_exclusive`, `coverage_end_inclusive` | Timezone-qualified ISO timestamps; start before end; end no later than creation. Normal succession starts at predecessor's coverage end. |
| `source_ledger` | Nonempty array of source objects: `source_id`, `title`, `source_date`, `retrieved_at`, `inclusion_role`; include kind, source-record revision/update time, provenance, and omissions when available. |
| `entry_created_at` | Actual creation timestamp with timezone. Never determines sequence. |
| `content` | Complete nonempty handoff text. |
| `provenance` | Object with nonempty `origin` and stable `operation_id`; retain evidence and source qualifications. |

Optional `updated_at` and backend `status` are audit data, not ordering. Optional `checksum` is lowercase SHA-256 over exact UTF-8 `content`; validate it when present. An adapter using other integrity schemes verifies those before providing a normalized inventory. `immutable_path` is an immutable normalized absolute POSIX-style locator supplied by a capable adapter; the helper derives `path:<path>@sha256:<checksum>` if no ID exists. The path is a backend locator, not a required local filesystem. Do not derive identity from a mutable whole-container path.

`supersedes_entry_id` is optional and names an earlier entry in the same series only for an actual correction/replacement; require a nonempty `correction_reason`. It never substitutes for predecessor fields. A replacement may revisit an earlier coverage start but cannot move the cutoff backward.

When applicable, `invalidation_status` is one of `invalid`, `erroneous`, `incomplete`, `quarantined`, `wrong_predecessor`, or `unsuitable_for_continuity`, with a nonempty `invalidation_reason`. Only explicit stored evidence permits exclusion. The helper retains the canonical identity/title, timestamp and integrity checks for excluded entries while allowing their defective continuity fields to remain audit evidence. Never synthesize invalidity from an archive flag or automatically write an invalidation.

The helper rejects unknown entry fields. Adapter audit field `full_read: true` attests to actual full retrieval; it is not a persisted claim that a not-yet-written output has been verified. New backend IDs may be assigned at creation; preserve all other prepared fields. The adapter must return the normalized entry and disclose any transformations; unexplained differences fail read-back.

## Complete inventory envelope

Provide `journal_id`, `handoff_series_id`, `handoff_series_title`, `entries`, `complete: true`, and `enumeration_evidence` explaining exhausted pagination/traversal. Optional `latest_entry_id` is a pointer cross-check. These attestations require real tool evidence; the pure helper cannot prove backend completeness.

All entries must belong to that exact scope. Identical repeated observations of a stable ID deduplicate; conflicting observations block. Duplicate sequences block with both IDs in a structured ambiguity report. The resolver validates the entire predecessor chain from Entry 1, sorts numerically, retains explicitly invalid entries in `audit_inventory`, returns `latest_entry` and `proposed_sequence`, and warns about stale pointers or fallback identity. A proposal is not an allocation or permission to write.

## Optional adapter protocol

The optional helper calls these semantic Python methods only when an adapter is explicitly supplied; the plugin ships no service integration.

- `enumerate_series(scope)`: return the complete inventory envelope after exhausting traversal; include all statuses and candidates.
- `retrieve_entry(entry_id)`: retrieve the full normalized object, or return null when unreadable. Verify other backend integrity data here.
- `find_sequence(scope, sequence)`: explicitly check whether the exact series/sequence pair is claimed, including invalid entries.
- `create_entry(entry, expected_entries=...)`: create a separate object and return its stable ID; never mutate prior entries. Enforce a unique series/sequence constraint, CAS, transaction, or optimistic check where supported.
- `commit_latest(scope, entry, expected_entries=...)`: only after read-back and full post-write verification, create a new linked receipt for the effective pointer and cutoff together using conditional append or exclusive creation where supported. Never overwrite an existing pointer/ledger entry. On conditional failure, leave effective state unchanged.

Backend exceptions propagate as failures, not success. Without atomic creation/commit, disclose remaining races and stop on detected collisions. The helper never retries writes, chooses duplicates, or deletes entries. The assistant must reconcile an uncertain operation ID before attempting another write. The `intermediate` path calls only enumeration and retrieval, returns no proposed sequence, and cannot consume sources.

## Fictional initial handoff entry

This complete fixture is also validated in the automated tests. The source is fictional.

```json
{
  "entry_id": "example-entry-1",
  "entry_type": "therapist_handoff",
  "journal_id": "example-journal",
  "handoff_series_id": "example-week-2026-09-07",
  "handoff_series_title": "Weekly Therapist Handoff — 2026-09-07",
  "handoff_sequence": 1,
  "title": "Weekly Therapist Handoff — 2026-09-07 — Entry 1",
  "coverage_start_exclusive": "2026-09-07T00:00:00Z",
  "coverage_end_inclusive": "2026-09-08T12:00:00Z",
  "entry_created_at": "2026-09-08T12:00:00Z",
  "content": "I would like to discuss my fictional journal observations.",
  "provenance": {"origin": "fictional test", "operation_id": "example-operation-1"},
  "source_ledger": [{
    "source_id": "example-source-1",
    "title": "Fictional journal observation",
    "source_date": "2026-09-07",
    "retrieved_at": "2026-09-08T11:59:00Z",
    "inclusion_role": "current self-report"
  }]
}
```
