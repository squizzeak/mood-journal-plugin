# Therapist handoff entries and source packets

## Entry-series contract

A therapist handoff is a separately stored handoff entry with its own stable entry ID or backend record ID, creation timestamp, content, provenance, source ledger, and coverage fields. Related entries form an ordered handoff series. Sequence numbers describe order, not file changes. Preserve predecessor entries unchanged.

Use exactly `<handoff-series-title> — Entry <N>`, for example:

- `Weekly Therapist Handoff — 2026-09-07 — Entry 1`
- `Weekly Therapist Handoff — 2026-09-07 — Entry 2`
- `Therapist Handoff — September 2026 — Entry 1`

Structured metadata is authoritative. The title must agree with it. The complete field contract and fictional example are in [handoff-entry-schema.md](handoff-entry-schema.md). Use `supersedes_entry_id` only for an explicit correction or replacement of an earlier entry's clinical-continuity role, with a correction reason; ordinary succession uses only predecessor fields.

## Storage capabilities and identity

Use any authorized durable framework: apps/connectors, note systems, files, databases, agent-memory services, or other adapters. Require the ability to enumerate all entries in the exact series, exhaust pagination or equivalent traversal, inspect metadata, retrieve entries in full, create a separate entry, retrieve it, and verify the resulting complete series. A single file or full memory item qualifies only if it can preserve separately identified entry objects and all prior objects unchanged and support complete traversal and read-back. Summary memory or partial chat recall is insufficient for entry creation.

Prefer a stable entry ID or backend record ID. Where neither exists, use an immutable normalized path plus a cryptographic content checksum and retain that identity in predecessor links. For a container holding multiple objects, the identity must also distinguish the immutable entry object; a changing whole-container checksum is not a stable predecessor locator. Disclose reduced identity and concurrency guarantees. If the adapter cannot provide durable identities, full enumeration, or verification, fail closed: create no handoff entry. Independently authorized journaling and a clearly limited, chat-only intermediate report may continue.

Adapter operations are semantic requirements, not vendor API names. The optional [select_handoff.py](../scripts/select_handoff.py) provides executable schema/lineage validation and a reference adapter protocol; Python is not required on cloud or mobile hosts. The primary assistant performs all work directly. Do not delegate.

## Resolve the latest validated handoff entry

Apply this gate whenever a handoff is used as current context: routine journal preflight, one-off logs, incidental handoff updates, explicit summaries, intermediate reports, and resumed sessions.

1. Establish the exact authorized journal and `handoff_series_id` before comparing sequences. Bind the series to its explicit title, user/journal, purpose, and period or coverage scope. Never combine unrelated users, weekly periods, series, or coverage scopes. Adjacent coverage intervals within one established series remain related. A folder name alone neither creates nor resets a series.
2. Enumerate the complete candidate set across relevant containers and statuses; exhaust every page or equivalent traversal. Do not apply the recent-journal retrieval window to the handoff series. Deduplicate identical observations by stable entry ID; conflicting observations of one ID require a fresh resolution.
3. Build a private inventory with stable ID, full title, series ID/title, numeric sequence, creation/update timestamps when available, coverage fields, predecessor ID/title, any explicit replacement, validity/invalidation status and reason, source-ledger presence, provenance, and checksum when supported. Record enumeration scope, traversal evidence, and unresolved failures. An asserted completeness flag is not proof of actual traversal.
4. Require the canonical title and required metadata. Read entries in full. Exclude an entry from continuity only if full content or metadata explicitly marks it invalid, erroneous, incomplete, quarantined, created from the wrong predecessor, or unsuitable for continuity. Keep an invalid branch entry in the audit inventory with its reason. Archived status alone never makes a predecessor invalid.
5. Compare `handoff_sequence` as positive integers and select the valid entry with the highest sequence number. Retrieve it in full and validate its identity, canonical title, coverage, source ledger, provenance, predecessor chain, and available integrity data. The predecessor must be the immediately preceding validated entry in this series, with an exact ID/title match. The initial handoff entry has no predecessor. No self-reference is allowed.
6. Use indexes, canonical pointers, caches, timestamps, filenames, and search order only as cross-checks. A pointer to a lower sequence is stale; do not repair it during read-only resolution. Entry 10 follows Entry 9 numerically.
7. Stop on a duplicate-sequence conflict, title/metadata disagreement, unreadable apparent latest entry, missing or wrong predecessor, ambiguous scope, incomplete traversal, or any failed validation. Return a structured ambiguity report with exact stable IDs, titles, sequence numbers, and failure reasons. Never guess, choose between duplicates, overwrite, delete, archive, invalidate, or create a branch automatically.

Reading an older entry for discovery or dated historical evidence does not make it current. Refresh on resume and before any write; a previous chat's resolution is not a permanent cache. Incomplete context leaves dependent claims and operations pending.

## Coverage, provenance, and source review

Capture actual generation time with timezone/offset and UTC. A normal next entry covers `(predecessor.coverage_end_inclusive, generation time]`; the initial handoff entry uses the explicit requested start or earliest supported source boundary. Store both endpoints, with end after start and no later than entry creation. Do not infer coverage from timestamps or filenames. An explicit correction can revisit earlier coverage, but must identify what it replaces, preserve provenance, and never move the verified cutoff backward.

Read all still-unsummarized handoff source notes and relevant journal entries in the interval, including archived/completed sources where appropriate, deferred sources, new source-record revisions, and corrections not represented by exact ID/revision in the prior source ledger. Include older context needed to explain the current evidence and label it as prior context. Paginate and read sources in full. Missing source reads block claims of complete coverage and prevent entry creation for that claimed interval.

The source ledger records stable source ID/locator, title, kind, source date, update or revision timestamp when available, retrieval time, inclusion role, and omissions. Retain speaker attribution, exact quotations, recollection versus documentation, assistant interpretation, and voice-transcription uncertainty. Missing assessment is not absence of symptoms or risk. Quotes and citations never consume sources by themselves.

## Choose the requested output

- **Summary:** Default full deliverable: a concise first-person read-aloud script, stored as a separate handoff entry after the resolver and source review succeed. A file representation is optional when the backend stores the full entry directly.
- **Packet:** Only for an explicit packet/source bundle/ZIP request. Create an expanded PDF overview and full searchable source PDFs, a PDF source manifest and verification report in a PDF-only ZIP when rendering tools exist. Include provenance and SHA-256 checksums, inspect every rendered page, compare extracted text with sources, and test ZIP extraction. Missing rendering or verification means pending output, no claimed verified packet or cutoff advancement.
- **Intermediate report:** Only when explicitly requested. Follow the non-consuming rules below.

For a read-aloud script, include generation/coverage metadata, a brief opening, meaningful changes, current mood/body/functioning supported by sources, treatment questions, coping/support, relevant events, requested help, and a closing invitation. Put the source ledger after the spoken sections. Do not send any materials to another person or service without explicit sending authorization.

## Create the next entry and commit verification

1. Resolve the latest validated handoff entry and prepare source-grounded content.
2. Immediately before writing, repeat the full series enumeration and resolution. If the predecessor or relevant sources changed, re-resolve and rebuild the content before retrying.
3. For a genuinely empty series propose sequence 1. Otherwise propose the latest valid sequence plus one. Explicitly search the proposed `(handoff_series_id, handoff_sequence)` pair across all candidates, including invalid entries. If claimed, stop and re-resolve; do not reuse it or silently skip to a higher number.
4. Create a separate entry using the canonical title. Entry 1 omits predecessor fields or uses null values. Later entries store the latest validated entry's stable ID and exact title. Preserve all prior entries unchanged. Use a stable operation ID for uncertain-save reconciliation; never repeat a create blindly.
5. Use atomic conditional creation, compare-and-swap, transactions, optimistic concurrency, or a unique series-and-sequence constraint when available. Without atomic support, disclose the limitation, re-enumerate immediately before and after writing, and stop on collision. Single-agent use does not lock other sessions or external editors.
6. Retrieve the new entry in full and re-enumerate the complete series. Verify that it is the only valid entry with its sequence and the sole valid highest entry; verify title/metadata, correct predecessor, full content, provenance, coverage, source ledger, and available checksums. Compare all prior entries with the pre-write inventory to ensure they remain unchanged.
7. Only after all output, source, read-back, and series checks pass may a new latest-entry/coverage receipt be created. Preserve all earlier pointer/coverage records unchanged; resolve effective state from the verified receipt chain. Use a conditional append or exclusive receipt creation when possible. Any failure leaves these unchanged; report partial persistence with the exact created ID rather than claiming the write never happened. Do not automatically clean up a conflicting entry.

## Non-consuming intermediate reports

An intermediate report renders directly in chat. It may resolve and cite the latest validated handoff entry and review all still-unsummarized source entries, but it must:

- Create no artifact and no handoff entry; allocate no sequence.
- Make no storage mutation and update no latest pointer, coverage cutoff, or last-summarization date.
- Change no tags, statuses, reminders, metadata, or ledgers.
- Mark no source summarized, consumed, excluded, reviewed-and-consumed, or complete.

Include source citations, exact stable IDs, source dates, update/revision timestamps, and selective direct quotes as useful. Preserve speaker attribution, context, provenance, and uncertain voice wording. Label the report generation time as not a new cutoff. The next full handoff must reconsider these sources. A report neither closes a live journal session nor authorizes staged saves. If discovery is incomplete, label the report source-limited without claiming a latest validated entry.
