# Runtime capability notes

Existing stored entries, including their content and metadata, are never overwritten. Logical corrections and state changes are new linked entries/events; current state is resolved from their history. Single-file storage requires true append without replacing existing bytes; update-only memory backends cannot satisfy this guarantee and must leave unsupported saves pending. Source deletion is optional only for explicitly scoped migrations or comparable verified transfers, after full-copy, link, and routing verification. Retention is the default. This is a skill behavior rule, not an immutable-storage guarantee from the provider.

Every conversational journaling session requires a brief current-safety check for suicide/self-harm thoughts and immediate physical danger, following [safety.md](../plugins/mood-journal/skills/mood-journal/references/safety.md). This applies across full/impromptu, text/voice, mobile, and unsaved modes. The user may decline; no clinical screening, absence of risk, or safety guarantee is implied. Current-session answers may satisfy the check, but historical records cannot. Follow up on changing concerns and review safety at close without overriding save boundaries.

The same skill files are packaged for directory submission, standalone skill upload, and marketplace installation. No required provider, account ID, MCP server, or hook is declared. Optional historical-import Python code runs only when explicitly needed and available. Core journaling does not require Python, a shell, or a local filesystem.

| Available environment | Journal operation | Limits |
| --- | --- | --- |
| Native cloud durable file tools | Write/read back complete dated records in the authorized project destination. | Must verify tools and persistence; no undocumented API is assumed. |
| Native retained project chat, no storage plugin | Render the complete dated entry in the retained conversation; use accessible project history for continuity. | Host-managed retention, no separate save receipt, no promise of exhaustive or exact future retrieval. |
| Native summary memory only | Store an authorized compact summary/pointer if an operation exists; retain the full entry in project chat when possible. | Lossy; no exact quotes or full coverage claims based on remembered summary alone. |
| Single persistent file or full memory record | Read all current content, append/update a dated session block, preserve history, read back. | Less efficient as it grows; do not silently truncate or overwrite older entries. |
| Local project files only | Persist in a private authorized directory or a single journal file. | Local durability does not mean cross-device synchronization. |
| Compatible storage plugin | Use its actual schemas and authorized record operations; prefer revision checks and exact verification. | Tool availability and permissions can vary by surface. |
| No persistent destination | Explain limitation; provide explicitly chosen unsaved reflection or an interrupted-session draft. | No save claim or promise of background recovery. |

## Progressive storage upgrades

A new storage plugin can become the destination for future entries after user selection. On explicit migration request, the skill inventories earlier project chats and memory-backed entries, retrieves full sources where possible, produces full files/records, and verifies them individually. It retains original dates, provenance, old/new locators, and partial-migration state. Originals stay intact. Installation alone does not authorize a transfer.

The optional export helper materializes explicitly selected source conversations and a synthesis queue. The skill then reconstructs journal entries against the sources. If only compressed memory survives, import it as a partial historical record, not a reconstructed full transcript. Historical ingestion does not consume clinician-handoff coverage.

## Verification vocabulary

- **Verified full record:** exact destination read matches the intended content.
- **Acknowledged memory summary:** backend accepted summary memory; full original retention is not established.
- **Recorded in project conversation:** final entry is presented in an established retained chat; retention is managed by ChatGPT.
- **Write unverified:** a write may have occurred but read-back is unavailable or failed.
- **Unsaved/pending:** no durable write or established retained conversation is available.

A generated file link, same-thread context, or fluent recollection alone does not prove cross-device file persistence. Test full storage separately from conversation behavior. Live cloud/mobile tests and directory approval remain publisher tasks; local archive tests cannot certify them.

## Historical/live parity

A completed historical import must resemble the normal live work product: the same journal schemas, titles, destination layout, supported context revisions, inquiry state, and indexes. Replay chronologically so later knowledge does not contaminate earlier records. Keep original session dates and separate reconstruction/verification timestamps. Source extraction is only the first phase. Do not invent missing facts, past verification, or handoff documents to make the archive look complete.

## Automatic migration timing

With a saved, scoped opt-in, capability detection at session start/resume or active tool refresh can initiate migration automatically. It checks the approved account/destination and source ledger, preserves originals, excludes unfinished sessions, and resumes verified progress. A new destination outside that authorization requires a new choice. There is no guaranteed cloud/mobile connector-install event or background listener in a skills-only package.

## Backend selection and migration

Users can select any capable installed or native storage option. An established choice persists. Initially, one capable installed storage plugin is the default; multiple capable plugins default to native storage when available. If native persistence is unavailable, ask for a destination instead of picking a service arbitrarily. No plugins falls back to available native/local persistence. Defaults never invent file capabilities or authorize historical transfers.

“Move my journal to [backend] and use it for future entries” migrates canonical records and switches routing after verification. Source disposition is selectable: retain (default), archive, or explicitly scoped deletion. Verify the destination and cutover before cleanup; never delete full originals after a lossy summary-memory/chat-only migration. Interrupted copies resume from the ledger; failed cleanup stays pending without reverting successful future-save routing. Unrelated/shared data is excluded. Native archival/deletion is offered only where real tools support it.

## Projects are optional

A journal has a stable identity independent of its ChatGPT Project, current conversation, or storage provider. Use the same selected journal from ordinary chats or projects whenever its authorized backend is accessible. Backend migrations preserve that identity. If several journals are available, select the intended one before accessing history; matching names do not authorize merging.

Without a storage plugin, an ordinary retained chat can hold a complete dated entry, with host-managed retention and no independent save receipt or guarantee of exact retrieval in later chats. A native full record/file can be used if actually exposed. No durable destination means explicitly unsaved reflection. No mandatory manual Save-to-project step is introduced.

Historical import outside projects accepts explicitly selected chats, exports, or an authorized source ledger. It does not silently search or import the whole account. Automatic import preferences bind to the journal and exact source scope, not merely a project name.

Users may opt into a require-project policy for a journal. The skill checks trusted host project identity and pauses journal retrieval, writes, and migration outside the allowed project or when identity is unknown. This is behavioral enforcement, not a directory manifest restriction or security boundary. It does not prevent host chat retention; an explicit user policy change can disable it. No such restriction is enabled by default.

### Projects remain supported for organization

Use a ChatGPT Project to organize related journal chats, instructions, and sources, and optionally a backend project/folder/collection to organize stored records. These are separate containers. Track organizational membership independently from journal identity and storage routing, so renaming or moving a project does not create a new journal. A project may contain several distinct journals; do not merge them automatically. Project-scoped imports remain available, with explicit source and journal boundaries. Creating/moving native projects depends on actual host tools; optional organization setup never becomes a manual per-entry saving requirement.

## Informed first-use setup

The skill explicitly asks for operational preferences before first journal-history retrieval or saving, after explaining capabilities, limitations, benefits and drawbacks. Project choices are: no preferred project, a preferred project for organization while remaining usable elsewhere, or a required project with the disclosed limits of behavioral enforcement. Storage selection is separate and covers actual full-record, local, single-record, summary-memory, retained-chat or unsaved options. The plugin-count defaults are recommendations the user accepts or overrides, not silent choices.

Setup records the selected journal, project preference, backend, saving behavior and manual/disabled/automatic historical-import policy. It explains save timing and the absence of a guaranteed background import listener. Previously explicit choices are reused; only missing or materially changed preferences require questions. Users can say “show my journal settings,” “explain the modes,” or “change my journal setup.” Configuration is conversational and stored in authorized journal storage where possible; there is no custom installer, native settings panel, or permission toggle. Configuration writes do not save unfinished journal content or authorize historical copying/deletion. Unverified preference persistence is disclosed.

## Handoff entry series

Each full therapist handoff is an independently stored **handoff entry**, with a stable ID, creation timestamp, complete content, provenance, source ledger, and coverage interval. Related entries form an explicitly identified **handoff series**. Use exactly `<handoff-series-title> — Entry <N>`, such as `Weekly Therapist Handoff — 2026-09-07 — Entry 1` and `Weekly Therapist Handoff — 2026-09-07 — Entry 2`.

Structured `handoff_series_id` and positive integer `handoff_sequence` determine membership and order. The title must agree. Entry 1 has no predecessor; every later entry records the preceding validated entry's stable ID and exact title. Predecessor entries remain unchanged. `supersedes_entry_id` is reserved for an actual correction or replacement of clinical-continuity content, with an explicit reason.

The resolver exhausts all pages or equivalent traversal within the authorized series, deduplicates by stable ID, reads full entries, and compares sequences numerically. Entry 10 follows Entry 9. Search order, modification time, filenames, and cached pointers cannot identify the latest entry; a pointer to Entry 8 is stale if enumeration validates Entry 10. Archived entries remain eligible. Explicit invalid branch entries remain in the audit inventory, with the documented reason for exclusion.

A duplicate-sequence conflict, wrong/missing predecessor, title mismatch, ambiguous series, or incomplete retrieval blocks creation and yields exact IDs, titles, sequences, and failure reasons. The skill never chooses a branch or cleans up conflicting entries automatically. Before creation it repeats enumeration and explicitly checks that the proposed series/sequence pair is unclaimed; after creation it verifies the full new entry and that all predecessors remain unchanged. Only then may the latest pointer and coverage cutoff advance.

Apps, connectors, note systems, local files, databases, and agent-memory services qualify by actual capability. The backend must enumerate the complete series, inspect metadata, retrieve full entries, create a separate entry, and verify it and the series afterward. Without stable IDs, an immutable normalized entry path plus cryptographic content checksum can provide fallback identity, with reduced identity and concurrency guarantees. Atomic conditional creation, transactions, or a unique series/sequence constraint are preferred; otherwise pre/post enumeration detects some collisions but cannot eliminate races. Insufficient capability means no handoff entry is created; independent journaling remains available.

**Intermediate reports are non-consuming and chat-only:** no artifacts, new entries, sequence allocation, storage mutations, pointer updates, cutoff or last-summarization changes, tags/status/reminder changes, ledger writes, or sources marked summarized/consumed/complete. They may cite Entry 10 and source IDs/dates, source-record revisions, and exact attributed quotes without creating Entry 11 or consuming anything. Voice uncertainty remains visible.

See the [workflow](../plugins/mood-journal/skills/mood-journal/references/handoffs.md) and [field schema and adapter contract](../plugins/mood-journal/skills/mood-journal/references/handoff-entry-schema.md). The optional deterministic helper and fictional tests exercise schema, lineage, and verification gates; they do not certify live conversational compliance or backend permissions. Python is not required for native skill use.

## Single-agent chat operation

This release is for direct interaction with one primary assistant. It performs the conversation, historical import, handoff preparation, verification, and all saves itself. Sub-agents, delegated read-only review, cross-chat task dispatch, and autonomous background agent work are unsupported. Direct tool calls and deterministic helpers remain available. Approved automatic import runs during the active chat.

This is a skill behavior rule, not a plugin permission that disables host agent tools or globally locks other chats. Sequential cross-device use remains supported. Ordinary revision checks, latest-handoff-entry resolution, and safe retries remain necessary even with one agent. No multi-agent infrastructure or lock service is required. Future narrowly scoped delegation is a separate development consideration, not an enabled mode.
