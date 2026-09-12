# Clinician handoffs and source packets

## Choose the requested output

- **Intermediate preview:** Only when explicitly requested as interim/intermediate. Read sources, respond in chat, and make no artifact or durable mutation. Do not consume sources, mark them summarized, advance coverage, or close an ongoing journal conversation.
- **Summary:** Default for a therapist or clinician handoff. Produce a concise first-person read-aloud Markdown script; use a file if file output is available and authorized, otherwise give the complete draft in chat with its persistence limitation.
- **Packet:** Only for an explicit packet/source bundle/ZIP request. Produce an expanded PDF overview with full source exports in a PDF-only ZIP when rendering tools exist. If they do not, state the exact missing capability and provide what can be produced without claiming a verified packet.

Do not send or upload these materials to another person or new service without explicit authorization.

In single-file mode, the ledger can occupy a section in that file. With only summary memory or retained conversation context, produce a source-limited summary and label incomplete coverage; do not advance a verified full-handoff cutoff or claim exhaustive source inclusion. Never require a connector merely to produce a clearly qualified conversational summary.

## Coverage and evidence

Capture generation time with timezone/offset and UTC. Retrieve the latest fully verified handoff record and its explicit coverage end and source ledger. The new interval is `(previous verified coverage end, generation time]`. For an initial handoff use the requested interval or available relevant history, stating the limits. Never infer a cutoff from a filename or last-modified time.

Read every available not-yet-summarized handoff note, including archived/completed notes when appropriate, and journal entries in the interval. Include new revisions of older sources, deferred sources, and material not represented by exact ID/revision in the prior ledger. Retrieve current-context notes and older sources needed to explain corrections, chronology, or current questions. Mark old material as related prior context. Paginate relevant searches, deduplicate by ID, read sources in full, and state missing reads. Do not claim complete coverage from incomplete retrieval.

Keep a source ledger with title, locator, kind, source date, revision/update time, retrieval time, inclusion role, and omissions. Preserve every eligible handoff note in the evidence review and ledger even when the script condenses it. Separate current and historical self-report, recollection, documentation, quotes, assistant interpretation, and possible patterns. Missing assessment is not absence of risk or symptoms.

## Read-aloud summary

Use short, speakable first-person sentences. Include generation/coverage metadata, a 60-second opening, meaningful changes, present mood/body/functioning, current safety report only if supported, treatment/medication questions, coping/support, relevant events, requested help, and a closing invitation to discuss. Put the source ledger after the spoken sections. Preserve emotionally important wording without turning the script into an unabridged transcript.

For an intermediate preview label its generation time “not a new cutoff”; keep the previous full-handoff baseline unchanged and include source trace and limitations. The next full handoff must reconsider these sources.

## Explicit source packet

Create a descriptive PDF overview, a PDF source manifest, complete searchable PDFs of included source notes/journal entries and materially cited context, and a PDF verification report. Each source has provenance (ID/path, date, revision, retrieval time, status if available). Preserve original wording and voice qualifiers; presentation may change. Use safe filenames and deduplicate sources.

Calculate SHA-256 for every included PDF except the checksum report itself; include values in that report. Render all final PDF pages for inspection, check extracted text against sources, confirm each PDF opens, and verify ZIP extraction and a PDF-only inventory. Do not call an ordinary ZIP encrypted. If any source or visual check is missing, disclose the limitation and do not mark the packet fully verified.

## Versioning and commit point

Preserve a separately dated handoff version, optionally grouped by local ISO week, with coverage metadata and source ledger. In a memory service, persist and re-read its exact ID; in an authorized local store, reopen the final file. An additional local copy is not mandatory when the selected backend alone holds the verified deliverable. For a packet, verify its files as well.

Only after the output and its durable handoff record are verified, and source retrieval is complete for the claimed interval, update the authorized handoff index/current summary to the new coverage end. Preserve historical versions. If storage or verification is missing, leave the cutoff unchanged and report pending status. A newer generation time alone never advances it. Report artifact/record locators, counts of included handoff notes and journals, related sources, and omissions. Weekly organization does not authorize a background schedule.
