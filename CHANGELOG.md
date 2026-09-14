# Changelog

## Unreleased

- Preserve existing entries without overwriting: record corrections and state changes as new linked entries. Permit optional, explicitly scoped source deletion only after a complete migration or comparable transfer is verified.

- Require a brief current-safety check in every conversational journaling session, with respectful handling of declined answers, responsive follow-up, and faithful recording under existing save boundaries.

- Model therapist handoffs as independently stored entries in an ordered handoff series.
- Use canonical `Entry N` titles and explicit series, positive sequence, creation, provenance, source-ledger, and coverage metadata.
- Validate predecessor identity and exact title; reserve supersession for deliberate clinical-continuity corrections or replacements.
- Resolve the latest validated entry numerically through complete traversal, with duplicate-sequence and branch detection and structured ambiguity reports.
- Fail closed on incomplete enumeration, missing reads, invalid lineage, occupied proposed sequences, or failed post-write verification.
- Preserve non-consuming, chat-only intermediate reports with no artifacts, sequence allocation, storage mutation, or coverage advancement.

No release is asserted by this section. The manually dispatched Release workflow generates release sections from commit history, incrementally after a prior published release when one exists.
