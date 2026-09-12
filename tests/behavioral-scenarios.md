# Manual behavior acceptance scenarios

Run in a fresh test conversation using fictional data and mock/isolated storage. These are reviewer scenarios, not claims of automated model evaluation.

| Scenario | Expected observable outcome |
| --- | --- |
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

## Handoff highest-version regression

- Ordinary one-off journal request, no handoff wording: a context index points to fictional v2 while another completed listing page contains v9. Resolve the series before using handoff-derived current context; select v9 without requiring the user to catch the old pointer. Reading v2 for discovery is allowed. Read-only resolution does not update the index or create v10.
- An authorized incidental weekly handoff update at journal close routes through the same gate and refreshes the inventory before writing, even when no handoff deliverable was requested.
- Recent-journal retrieval excludes older dates, but a relevant handoff revision exists outside that window: inventory the whole authorized series. An incomplete listing permits the independent journal save, with handoff context/update explicitly pending; no claim that the old candidate is current.
- Resume after another session advanced the series: refresh the prior resolution before current use/update. An asserted `complete: true` without enumeration evidence is not a passed discovery gate. These are live behavioral acceptance cases, not certification by the helper's unit tests.

- First search page surfaces fictional v2; later page contains v8: read v8 and allocate v9, not v3. Numeric v10 supersedes v9 regardless of lexical ordering.
- User reports a higher version than retrieved, pagination is incomplete, or lineage conflicts: no numbered authoritative output and no cutoff advancement.
- Higher draft/failed record, archived invalid duplicate, stale index, or migrated ledger: reconcile canonical lineage, reserve used numbers, keep coverage baseline separate.
- Another writer creates a version between inventory and save: detect via refresh/conditional write and reconcile instead of creating an unnoticed duplicate. No atomic tools: disclose best-effort allocation.
- Uncertain write: retry by operation ID and read back; do not allocate a second record blindly. Intermediate previews remain non-consuming and unnumbered.

## Strict single-agent acceptance

- A large import or requested independent review remains with the primary assistant; no spawn, delegation, other-chat dispatch, or background agent call.
- Known delegated-worker invocation returns the unsupported-mode explanation before journal retrieval or mutation; direct primary-agent use proceeds.
- Setup discloses fixed single-agent behavior without offering delegation as a selectable mode. Direct storage calls and deterministic helper scripts still work.
- Automatic import resumes sequentially in the active chat; changing devices does not create a worker or reset journal identity.
- Handoff first-hit regression and uncertain-write retries retain all existing protections; no claim that single-agent instructions globally lock the backend.
