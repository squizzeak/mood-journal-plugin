# Informed setup and operational preferences

Before the first journal-specific history retrieval or save, explicitly acquire the user's operational preferences. Read only the configuration needed to identify an existing journal and prior choices, and inspect available tool capabilities without reading unrelated health content. Installation, a generic journaling request, silence, or an offered default is not a completed setup choice.

Reuse explicit preferences already supplied in this conversation or retrieved from a trustworthy authorized configuration. Do not ask the user to repeat them. If choices are incomplete, ask only for the missing parts. Existing users without recorded preferences receive this brief setup at their next relevant use, not a silent assignment of modes.

## Explain the choices before asking

Use a short, concrete comparison suitable for the surface. In voice, summarize aloud and ask one question at a time. In text, use a compact table or short parallel options. Explain the benefit and the material limitation of each choice, identify what is actually available, and label unknown capabilities as unverified. Do not present unavailable storage as selectable or bury limitations in linked documentation.

Project organization and enforcement are separate from storage. Present these three scope options:

| Scope mode | Benefit | Limitation |
| --- | --- | --- |
| Projects optional, no preferred project | Journal from ordinary chats or projects using the same selected journal. | Requires access to the journal configuration/backend for reliable continuity; no automatic project grouping or isolation. |
| Projects optional, preferred organizational project | Group related chats, instructions and sources in a chosen project while allowing use elsewhere. | A preferred project is not a restriction. Moving/creating chats or projects needs actual host support; project context may be unavailable elsewhere. |
| Require a selected project | The skill pauses journal operations outside the verified allowed project. | A behavioral rule, not plugin permissions or a security boundary. Missing trusted project identity blocks journal operations; unavailable preference retrieval prevents a guarantee of cross-chat enforcement. Host retention is unaffected. |

Explain storage separately, covering the available choices and briefly noting unavailable alternatives:

| Storage mode | Benefit | Limitation |
| --- | --- | --- |
| Native durable files/records | Complete records without an additional provider when real native tools exist. | Automatic persistent native file tools must be verified; temporary artifacts are not enough. |
| Compatible storage plugin | Structured records and possibly cross-device access. | Requires authorized account/destination and tools on each surface; connector access alone proves neither persistence nor synchronization. |
| Local project files | Full records under the user's local organization. | Not inherently accessible from mobile/cloud or synchronized between devices. |
| Single durable file/full memory record | Works with minimal storage operations and preserves a full journal when capacity permits. | Growing read/write cost, capacity and concurrency limits; never silently truncate history. |
| Summary memory | Lightweight continuity where supported. | Lossy and non-exhaustive; cannot replace full entries, exact quotes or a complete handoff ledger. |
| Retained conversation only | Works in ordinary or project chats without another storage plugin. | Host-managed retention, no independent save receipt or guaranteed exact retrieval across chats. |
| Unsaved reflection | Allows discussion without skill-initiated durable writes. | No durable journal or automatic recovery; cannot disable the host's independent chat retention. |

For the proposed destination state where records will live, whether full text is preserved, what read-back can verify, and whether cross-device access is tested or unknown. Apply the user's requested defaults from storage.md: one capable plugin suggests that plugin; multiple suggest capable native storage; keep existing choices. Explicitly ask the user to accept the suggestion or choose another option. Defaults guide the choice, not bypass it.

## Acquire and record preferences

1. Explain scope modes and ask which the user prefers. Resolve an organizational/required project only if selected; do not require project creation for ordinary-chat use.
2. Explain actual storage options and ask for the destination choice, including account/path when necessary. Accept an explicit response covering several choices without repeating questions.
3. State saving behavior: full and impromptu journal sessions save automatically at explicit close; intentional one-off logs save immediately after setup. No per-entry manual Save-to-project step is required. Unsaved reflection remains selectable. Ask about any missing or conflicting saving preference, not redundant confirmation of an already explicit choice.
4. Ask whether historical import should be manual-only, disabled, or automatic when the selected destination becomes available. Explain that automatic import needs accessible authorized full sources and runs during active skill use, not as a guaranteed background install event. Resolve journal/source scope before enabling automatic import. Do not start copying history simply because setup was completed. A separately explicit scoped import request is sufficient authorization.
5. Summarize the selected journal, project organization/restriction, destination, saving behavior, import policy, and material limits. Persist the preference record in the chosen authorized configuration and read it back where possible. Explicit setup responses authorize this minimal configuration write immediately; they do not authorize saving an unfinished journal or its derived health context. Do not ask for another confirmation if the choices are already explicit and complete.

Record schema version, journal ID, scope policy, organizational project locators, canonical destination identity, saving mode, historical-import preference and source scope, capability/verification snapshot, disclosure version `1`, choice timestamps, and exact authorization source where available. Keep unknown fields unknown. Never record a user acknowledgment they did not give. If configuration is only in chat or summary memory, say that reliable later preference recovery is unverified. Do not persist preference changes under an applicable no-save request; disclose session-only settings.

If the user declines setup, allow explicitly chosen unsaved reflection and retain only a pending draft under host chat behavior. Preserve already supplied one-off content while waiting for the missing choice rather than asking the user to repeat it. Urgent present-oriented support takes precedence over onboarding. Do not force irrelevant health questionnaires or repeated onboarding in routine sessions.

## Review and changes

Support “show my journal settings,” “explain the modes,” and “change my journal setup” through conversation. No custom installation screen, native settings panel, or permission toggle is supplied by this package. Before a material mode change, explain its concrete effect and obtain the missing preference. Revisit only affected choices when storage fidelity, account/destination, project enforcement, source scope, or available capabilities change. Never silently downgrade or transfer to a new service. Source retention/archive/deletion is a separate migration choice; setup does not grant cleanup authority.
