# ChatGPT native storage assessment

Assessed 2026-09-12. Preferred capability: automatic persistent journal saves, exact retrieval, and read-back verification across devices. The final design also accepts single-file/memory storage and a clearly limited retained-project-conversation fallback. User-assisted “Save to project” is not an accepted substitute. Third-party providers are outside this native-capability assessment.

| Native feature | Evidence and boundary | Decision for this plugin |
| --- | --- | --- |
| Project chats and sources | Projects retain chats/files and support contextual reuse. A response can be saved as a source through its message menu. This is a documented user operation; the reviewed page does not establish an automatic plugin write/update/read-back API. | Useful context; automatic journal storage unverified. |
| Project memory | Draws on project conversations; its memory is not presented as an enumerable record list. | Do not use contextual recall as verification of a complete saved entry. |
| Personal memory | The current system maintains a changing synthesis. | Suitable for context/preferences under user authorization, not the authoritative verbatim journal. |
| Generated downloadable files | Producing a file does not demonstrate that it became a durable project source accessible from a new chat/device. | No success claim without durable destination and read-back evidence. |
| Local agent files | Can be persistent on the local machine, but that does not establish native cloud/mobile access. | Supported locally when authorized and verified; cross-device support unverified. |

Sources: [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), [Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq), [Work with files](https://learn.chatgpt.com/docs/artifacts-viewer).

**Conclusion for full-file storage:** No reviewed documentation establishes the complete automatic native-cloud record lifecycle required here. This is a limitation of the evidence and exposed capabilities, not a claim that OpenAI can never support it. Full automated native project-file operation remains unverified. The skill can operate through native project conversations with explicit retrieval limits, or a single writable memory record/file when exposed. Mobile is a target, not a tested runtime. Packaging a skill for the directory cannot add a missing storage tool.

## Required future verification

Use fictional records in an isolated project. Identify documented, actually exposed native operations for enumeration, exact read, create, and update. Create a timestamped record at explicit journal close, fetch its full content, then read the same ID and revision from a new chat on another device. Update it safely and verify again. Test interruption/retry without duplication and confirm retention expectations. Record host/app versions, dates, tool identities, and evidence in the submission test log.

Do not certify support from merely seeing the old conversation, model recollection, a download link, a laptop file, or a successful create with no independent read. Do not implement browser automation as an undocumented substitute for mobile plugin capabilities. Until full-file verification succeeds, identify the actual fallback: single-record memory, retained project conversation, or unsaved draft. Do not imply equivalence between these tiers.
