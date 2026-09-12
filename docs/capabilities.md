# Runtime capability notes

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
