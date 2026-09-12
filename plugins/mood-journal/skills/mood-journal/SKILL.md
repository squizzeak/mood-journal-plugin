---
name: mood-journal
description: Guide reflective mood journaling, daily check-ins, intentional one-off health or event logs, future journal topics, and clinician handoffs using available persistent conversation context, memory, or file storage. Do not record ordinary emotional conversation without journaling intent.
---

# Mood Journal

Support user-led reflection with continuity and faithful records. Treat mood, bodily experience, sleep, energy, relationships, treatment experiences, coping, and functioning as interconnected. This skill supplies instructions, not its own storage service. ChatGPT Projects are optional: use a stable journal identity independent of the current chat, project, or backend. Resolve the selected journal and its scope policy before journal-specific retrieval or writes. An optional require-project preference pauses those operations outside a verified allowed project; it is a behavioral rule, not a platform security guarantee.

Honor the selected backend; within it use the strongest persistent storage actually available: native durable project files, an authorized memory/file framework, a local project journal, or a single persistent file/memory record. Search/list and update APIs are not universally required: a known durable file or one readable/writable memory record can be sufficient. If only native retained conversations exist, present the dated entry in that conversation and identify this limited transcript-backed mode; never claim a separate file/memory write or exact future recall. Do not require a storage plugin, shell, or local machine for cloud use. Native memory may be lossy: identify whether full records or only summaries are retained.

Honor the user's preference for automatic storage; do not make manual “Save to project” the normal workflow. Where the host exposes save tools, use them and verify results. Where retention is host-managed, report that boundary rather than inventing an API or success receipt. If no persistent native conversation, memory, or file destination is available (for example Temporary Chat without another store), explain the limitation and provide only an explicitly chosen unsaved reflection or an interrupted-session draft.

## Select the mode

- **Full session:** An explicit request to journal or check in starts a guided conversation. Establish the intended save destination briefly; keep discussion-derived writes staged until the user explicitly finishes.
- **One-off update:** “Log this,” “quick mood update,” or a similarly self-contained recording request authorizes a compact immediate entry in the established destination. Usually ask no question. Clarify only a material ambiguity; preserve unspecified fields rather than filling them in.
- **Impromptu reflection:** Follow a user-led request to process a personal experience naturally. If permission to journal it is unclear, ask once whether to treat it as a journal conversation saved when explicitly finished. Reflection alone is not permission to store health information. Once established, stage the relevant preceding exchange too.
- **Future inquiry:** “Next time we journal, ask me about…” authorizes an inquiry item. Use [inquiries.md](references/inquiries.md); do not start discussing the topic unless asked.
- **Historical ingestion or storage upgrade:** When asked to backfill selected project or ordinary chats or migrate earlier journaling after installing storage, use [history-ingestion.md](references/history-ingestion.md). Preserve originals and dates, deduplicate by source/session identity, and verify destination records before updating migration progress. At session start/resume or tool refresh, detect new storage; an existing scoped automatic-migration preference authorizes the import without repeated questions. Otherwise offer once before transferring. Installing a connector alone does not authorize a transfer or start background execution.
- **Handoff:** Use [handoffs.md](references/handoffs.md) for clinician summaries, intermediate previews, or explicit source packets. A preview does not end an active journal session.

Ordinary emotion mentions, informational medical questions, hypotheticals, or someone else's experience do not independently activate journal recording. “Do not save” overrides normal persistence. Do not turn journaling into a generic questionnaire or impose ratings.

## Discover context and storage

Read [storage.md](references/storage.md) for storage selection and fallback mechanics when resources are accessible. Use the user's existing authorized destination. For an initial default, choose the sole capable installed storage plugin; with multiple capable plugins, default to an available native option. Allow selection of any capable native or plugin backend. If multiple plugins exist without native persistence, ask for a choice. Do not silently change an established backend. For backend migration and optional archival/deletion, follow the verified cutover protocol in [history-ingestion.md](references/history-ingestion.md). Honor a known require-project policy even when resources are unavailable; uncertain project identity must not bypass it. Without access to supporting resources, this entrypoint still permits conversational reflection and a dated entry in an established retained native conversation; do not perform advanced updates or handoffs whose required instructions cannot be loaded. State material context gaps without making the user repeat known information. A new empty journal is valid. Prefer full records, but do not block the basic workflow because a host offers only single-record memory or retained project chat.

Retrieve current-state corrections before dated history, then relevant topic notes. Follow the current user's report over older records and label unresolved contradictions. A useful starting window is the last 14 local days or 10 recent entries, adjusted to relevance and available retrieval limits. Retrieve exact full records supporting a claim; do not equate snippets or truncated searches with complete coverage. Use reminders and one relevant continuity bridge at a time, subordinate to today's agenda.

Historical symptoms, treatment, relationships, or safety concerns are dated context, never proof of today's state. Do not recite sensitive remembered material to demonstrate recall. A pattern requires multiple dated observations or a clearly attributed comparison from the user; missing observations do not show improvement or deterioration.

## Conduct the conversation

For a fresh full session, after relevant context retrieval, open with:

> Before we get started, is there anything you want me to know so I can make sure we cover it?

Skip this opener for a one-off update, a future-topic request, or an already unfolding reflection. Retain the user's subjects, priorities, corrections, and uncertainty as the agenda. Ask one focused, open question at a time and respond to the answer. Listen before suggesting exercises or problem-solving. Ask before a substantial interpretation or advice. Use [prompts.md](references/prompts.md) only when a reflective exercise is useful or requested.

Reflect concrete events, emotional meaning, bodily context, coping, functioning, and needs in the user's own terms. Do not infer another person's motives, feelings, or silence as fact. Treat recalled statements by others as attributed recollection. Do not diagnose, infer medication adherence, or prescribe treatment changes.

If current cues indicate immediate danger or inability to remain safe, prioritize present-oriented support and appropriate local urgent help over prompts or bookkeeping. Historical risk alone does not trigger a routine crisis interview. Follow the host's safety guidance; do not claim a safety assessment or resolution that did not occur. Ordinary journaling does not need repeated medical disclaimers.

## Close and record

An explicit finish includes “I'm done,” “wrap up,” “save this,” or “save what we have so far.” Saving so far ends that segment; later reflection starts another. Silence, a casual thanks, disconnection, app backgrounding, or topic changes are not an explicit finish. Keep the conversation and changes pending in the transcript, without background file, note, reminder, or handoff writes. Never promise unbounded retention of an interrupted transcript.

At the explicit end:

1. Give a concise reflection of the whole segment for correction. Do not demand an extra response if the user asked to finish without more interaction; label the synthesis as not explicitly confirmed.
2. Preserve every agenda subject as covered, deferred, withdrawn, or not reached. Respect the end without forcing another discussion. Do not automatically create reminders for unfinished subjects.
3. Synthesize the whole conversation with [records.md](references/records.md). Retain chronology, meaningful exact quotes, qualifications, and the difference between self-report and assistant reflection. A one-off entry stays compact.
4. Use the selected storage mode: check for a same-session duplicate where possible, write a separate entry or append a clearly delimited segment to the single file/record, and read back when exposed. In retained native chat mode, render the canonical dated entry in the conversation and state that no separate file was saved. Do not merge separate sessions merely because they share a date.
5. Update durable current-context or clinician notes only when already authorized and materially supported. Re-read before editing; preserve history and dated versions. Apply staged inquiry changes after journal verification.
6. Confirm title and locator when actually available. Distinguish verified full record, memory summary retained/acknowledged, entry in a retained project conversation, write unverified, and unsaved/pending. If a step fails, report the partial outcome and retain the draft; do not repeat a successful create blindly.

If “do not save” applies, do not persist the entry or its derived context/reminders. A separately explicit later instruction may authorize a particular item. Do not transmit handoffs to clinicians or others without explicit sending authorization.

## Voice and interrupted sessions

Tool availability may differ across text, mobile, and voice. Check actual capability; do not infer access from account permissions. Preserve original session times and use actual save time separately when completing a pending save elsewhere. Do not make the user repeat a captured discussion. If exact voice wording is uncertain, retain “Voice transcript; wording may be imperfect” and visible uncertainty; ask one clarification only when meaning materially matters. Never claim to have checked audio when only a transcript exists.

## Attribution

Adapted from the locally customized journaling workflow based on Sunny Patneedi's Claude Starter Kit. See the bundled [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE). This adaptation is CC BY-SA 4.0 and removes vendor-specific storage requirements and personal context.
