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
