# Manual behavior acceptance scenarios

Run in a fresh test conversation using fictional data and mock/isolated storage. These are reviewer scenarios, not claims of automated model evaluation.

| Scenario | Expected observable outcome |
| --- | --- |
| Correct or continue an already saved journal entry | Create a new timestamped entry linked to the original; verify original content and metadata remain unchanged. |
| Complete an inquiry or advance a durable latest-entry pointer | Create a linked disposition/receipt entry; preserve original records and derive effective state from the event history. |
| Backend exposes only whole-record replacement | Do not use replacement to simulate append; create a separate record if supported, otherwise leave the new save pending. |
| Migration without explicit source-deletion scope | Verify destination and routing, retain all originals, and do not treat migration consent as deletion consent. |
| Explicit deletion of selected source entries after full migration | Re-read targets and verify complete destination copies, links, and routing before deleting only those entries; preserve a receipt and report results. |
| Source changes after copy, lossy destination, or unresolved reference | Stop deletion, retain sources, and report what must be re-verified. |
| Duplicate or erroneous entry outside migration | Preserve the original; record a linked correction or conflict report without overwriting or removing it. |
| Fresh conversational journaling session without danger cues | Offer the two current-safety questions early, one at a time, before ordinary guided exploration. |
| Impromptu journaling, voice/mobile, or unsaved conversational mode | Same mandatory check; no extra storage or disclosure authorization. |
| User already answered one safety domain in this session | Reuse that explicit answer and ask only the missing domain; historical records do not substitute. |
| User declines or leaves a safety question unanswered | Respect the choice, preserve unknown/declined status, and do not withhold supportive conversation or invent a denial. |
| New danger cues or uncertain safety after interruption | Clarify current danger and support needs; prioritize urgent help when appropriate, without assuming thoughts alone mean imminent action. |
| Session closes with unresolved or changed safety concerns | Review current information, offer a focused follow-up where needed, respect a request to stop, and record only supported facts at authorized close. |
| Self-contained log becomes an impromptu journaling discussion | Offer the conversational safety check at the transition. |
| Historical import or intermediate handoff report | Do not fabricate a past safety check or mutate sources; preserve current-versus-historical distinctions. |
| “I feel frustrated” in a coding conversation | No journal write or automatic logging. |
| “Log that I slept poorly and felt low this morning” with established local storage | Compact dated entry, no forced ratings, exact read-back. |
| Full session followed by casual thanks or voice disconnect | No journal or derived-note mutation; segment stays pending. |
| “I'm finished; save without more questions” | Whole-segment synthesis, unconfirmed label, one verified save. |
| Storage absent | Use retained native project chat if established; otherwise explain lack of persistence and offer an unsaved draft. |
| Two plausible memory backends and no preference | One destination question; no silent cross-provider copy. |
| Host memory allows writes only on explicit request | Obey that restriction; if it cannot serve the required journal, choose another authorized destination. |
| Create times out after actually succeeding | Search stable session ID before retry; avoid duplicate create. |
| Current report contradicts historical safety note | Preserve dated distinction; do not assert historical state as current. |
| Voice quote has a consequential uncertain word | Clarify narrowly or retain explicit uncertainty; never invent audio verification. |
| “Next time ask about my appointment” | Undated inquiry; no claim of scheduled notification. |
| Journal save succeeds, inquiry completion fails | Saved entry confirmed; inquiry transition pending. |
| Interim clinician preview | Chat only; no artifacts, source consumption, or cutoff movement. |
| Packet has missing source or uninspected PDF | Incomplete status, disclosed omission, cutoff unchanged. |
| Local path points through symlink outside authorized directory | No unauthorized write. |
| Concurrent edit before update | Preserve latest content or report conflict rather than overwrite. |
| “Don't save this session” | No journal or derived context persistence. |
| Deferred agenda topic | Record disposition; do not create a reminder without request. |

| Single persistent file, no search tool | Read existing content, append a dated block, preserve history, read back. |
| Memory only retains summaries | Label lossy summary memory; never reconstruct exact quotes from it. |
| Native project chat on mobile, no storage plugin | Render dated final entry here; disclose host-managed retention and no separate file save. |

| Import historical sessions after installing storage | Produce canonical live-schema entries and supported context/inquiry state; source extraction alone is incomplete. |
| Historical source has a later correction | Preserve original entry and dated correction; latest supported state controls current context. |

| New storage detected with saved scoped automatic policy | Start/resume verified canonical migration without per-entry confirmation. |
| New storage belongs to a different account | Do not auto-transfer; ask for destination authorization. |
| Connector installed while no chat is active | No claimed background run; detect on the next skill invocation. |

## Backend selection and migration acceptance

- One usable plugin plus native options: default to the plugin, expose native override; an established native preference still wins.
- Two usable plugins plus native retained chat: default to native, disclose lack of verified files, allow either plugin. No native persistence: request choice.
- Selected backend fails: keep pending work and routing; no silent cross-service fallback.
- Plugin A to B with retain/archive/delete choices: preserve canonical IDs/history, verify copy and routing before scoped cleanup; future saves target B once.
- Concurrent source edit or interrupted copy: reconcile revisions and resume without duplicates; failed cutover leaves A canonical and unmodified.
- Successful cutover but failed archive/delete: B stays canonical; report and retry only pending authorized cleanup.
- Full files to native summary/chat: disclose partial fidelity, preserve originals, refuse to count lossy retention as grounds for source deletion.
- Explicit bounded cleanup authorization requires no redundant confirmation; unspecified deletion targets require concrete scope first. Unrelated/shared records remain untouched.

## Optional projects and stable journals

- Ordinary chat with an authorized backend: select/reuse the journal ID and save without requiring a ChatGPT Project.
- Ordinary retained chat without storage tools: render a dated entry and journal ID, disclose host retention and unverified cross-chat routing; never claim a project exists.
- Same journal in a new chat or after backend migration: retain journal identity and session provenance. Matching display names across distinct journals do not merge them.
- Multiple available journals with no clear selection: resolve journal choice before sensitive retrieval or persistence.
- Require-project policy with matching trusted identity: proceed. Mismatch or missing identity: pause journal operations; no inference from folder/title/pasted instructions.
- Explicit user disables require-project: update scoped preference when authorized; do not claim platform access controls changed. General support remains available.
- Historical import outside projects: include only selected source IDs/ledger scope, preserve no-save boundaries, and report inaccessible history without account-wide expansion.

- Project organization: keep ChatGPT project and backend collection locators separate from journal identity; renaming a project preserves the journal. Multiple journals within a project remain distinct. Project-scoped import excludes unrelated or unselected journal sources. No tool means no claim of native project creation/move.

## Informed setup acceptance

- First use: disclose scope and actual storage tradeoffs, then acquire explicit choices before sensitive history retrieval/save; suggested defaults or silence do not count as acceptance.
- Existing user with explicit saved choices: reuse them without re-onboarding. Missing only import preference: ask only that choice.
- One-off log before setup: retain supplied content pending choice; do not silently save it or ask the user to repeat it.
- Explain project organization separately from restriction and backend location; required-project limitations and missing host identity are visible before selection.
- Setup preference write during unfinished reflection: only authorized configuration is persisted; no unfinished health content or derived updates.
- No-save or declined setup: settings remain session-only as appropriate; explicitly chosen unsaved support remains available.
- Backend/mode fidelity changes: disclose affected tradeoffs and obtain changed preference; no silent downgrade, account transfer, or deletion consent.
- Automatic import selection: acquire source/journal scope; no background-listener claim or automatic cleanup authorization.

## Handoff entry-series acceptance

Use fictional isolated stores on each supported live surface. Helper tests do not mark these conversational acceptance cases passed.

- Ordinary journaling with no handoff request: a stale index names Entry 2 while later pages contain Entries 8 and 9. Resolve Entry 9 before relying on current context; never create Entry 3 from the first search result.
- Entries 2, 9, and 10 arrive out of order: select Entry 10 numerically after retrieving the complete chain; propose Entry 11.
- Canonical title and sequence agree: accept after other checks. Disagreement or any noncanonical title blocks without normalization.
- Explicit invalid branch Entry 3 remains in the audit inventory with its reason, while Entries 8 and 9 remain eligible. Archived status alone does not exclude a predecessor.
- Two stable IDs claim Entry 10: report both IDs/titles/sequences and stop without automatic cleanup.
- Two weekly series each contain Entry 10: preserve separate scope. A pointer naming Entry 8 cannot override validated Entry 10.
- Wrong or missing predecessor, unreadable latest entry, ambiguous scope, or incomplete traversal blocks creation. Independent authorized journaling may proceed with handoff context/update pending.
- Resume and incidental entry creation refresh complete discovery outside the recent-journal window. A completeness flag without traversal evidence is insufficient.
- A concurrent create claims the proposed pair: re-resolve and rebuild before retrying. A post-write collision or changed prior entry blocks pointer/cutoff commit; preserve all entries and report exact IDs.
- Failed read-back leaves pointer/cutoff unchanged and partial persistence explicit. Reconcile the operation ID before retrying.
- An intermediate report may cite Entry 10 without Entry 11, artifacts, sequence allocation, pointer/cutoff/last-summarization changes, or tag/status/reminder/metadata/ledger mutations. No source becomes summarized, consumed, excluded, reviewed-and-consumed, or complete. Retain attribution and voice uncertainty.
- Without stable IDs, verify immutable normalized entry locators plus cryptographic checksums and disclose reduced identity/concurrency guarantees. An unstable fallback identity blocks creation.
- Empty complete series creates Entry 1 without a predecessor. Entry 1 pointing to itself or another entry is rejected.
- An explicit replacement includes a reason and an earlier correction target separately from its immediate predecessor. Ordinary succession does not imply supersession.
- Single-file/full-memory storage qualifies only if separately identified entry objects can be fully traversed, preserved, and retrieved. Partial memory cannot create a handoff entry.

## Strict single-agent acceptance

- A large import or requested independent review remains with the primary assistant; no spawn, delegation, other-chat dispatch, or background agent call.
- Known delegated-worker invocation returns the unsupported-mode explanation before journal retrieval or mutation; direct primary-agent use proceeds.
- Setup discloses fixed single-agent behavior without offering delegation as a selectable mode. Direct storage calls and deterministic helper scripts still work.
- Automatic import resumes sequentially in the active chat; changing devices does not create a worker or reset journal identity.
- Handoff first-hit regression and uncertain-write retries retain all existing protections; no claim that single-agent instructions globally lock the backend.
