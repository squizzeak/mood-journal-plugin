# Public directory submission kit

This folder contains prepared listing copy, a logo, an illustrative prompt-preview PNG, five positive and three negative reproducible test cases, policy documents, and cloud/mobile test instructions. `listing.json` is a maintainer worksheet, not a documented upload API schema. Null fields are deliberately unfilled publisher facts; never invent verification or attestations.

Submit as **skills-only**. The package has no bundled MCP server, existing-integration reference, shell hook, required app, or local runtime. The skill prefers verified persistent files/records, can use single-file or single-record memory, and falls back to a retained native conversation inside or outside projects without inventing a separate save. No storage plugin is necessary. Native cloud/mobile exact file writes remain unverified, but the conversational workflow is designed for those surfaces. User-assisted saving is not the normal path. A ZIP alone does not publish or install a cloud plugin.

## Artifacts

- `mood-journal-VERSION-directory.zip`: portable root `plugin.json`, skills, referenced resources, legal notices, and logo; no marketplace or development scripts.
- `mood-journal-VERSION-skills.zip`: self-contained `mood-journal/SKILL.md` and its supporting resources for a portal skill-bundle upload.
- `mood-journal-VERSION-submission-kit.zip`: listing worksheet, test cases, policy drafts, and logo. This is supporting material, not the plugin upload.
- `mood-journal-VERSION-marketplace.zip`: repository marketplace for desktop/workspace GitHub distribution.

Use the directory package where the portal accepts a plugin package, and the skills bundle in its skill-upload step. The exact upload controls and accepted archive layout must be confirmed in the live portal; both deliverables contain the same tested skill files.

## Publisher completion

1. Fill `listing.json` with the actual verified publisher, public website/support/privacy/terms URLs, and chosen countries. Review and host PRIVACY.md and TERMS.md. Mirror public listing URLs and publisher identity into both manifests when finalized.
2. Run `python3 scripts/validate.py --submission` to check the local worksheet. This checks required values and attestations, not identity ownership, live URL reachability, or OpenAI approval.
3. Run the cases in fresh cloud web and mobile chats, recording actual results in `test-results.md`. Include a missing-storage negative test and voice if offered. Mark completion only after running tests.
4. Open the submission portal, use the skills-only route, supply materials and required attestations, and submit for review. Approval and publication are separate from GitHub releases.

Account access, verified identity, listing requirements, and review are controlled by OpenAI. Consult the current [submission instructions](https://developers.openai.com/plugins/deploy/submission). The [package specification](https://developers.openai.com/plugins/build/plugins) distinguishes public packages from local marketplaces. This kit prepares the files; it does not assert directory eligibility has been accepted. Validate the advertised fallback modes in cloud/mobile before submission; do not advertise unverified automatic native file writes. See `docs/native-storage-research.md` in the source repository.

## Cloud/mobile acceptance

Install the submitted/test plugin through a surface-supported mechanism; copying local files to a laptop does not install it into a cloud chat. Check that the skill activates, supporting resources can load, no local executable is required, storage tiers are selected honestly, with a useful retained-project fallback when available, saves are not fabricated, transcript uncertainty survives voice, and storage failures preserve drafts without claiming a completed entry. Test on web and available iOS/Android clients using fictional content. Record app/host version, date, surface, case IDs, observed output, and pass/fail. If reference loading is unavailable, the entrypoint must still support a dated native project-chat entry or clearly unsaved reflection according to actual retention; do not claim full handoff behavior without its reference.

## Additional capability acceptance

Test starting in native project-chat mode without a storage plugin, then installing/selecting compatible storage and explicitly migrating prior journal material. Verify preserved dates, original-source retention, no duplicate entries on retry, and explicit partial status when only compressed memory survives. Test one authorized local journal file without a search API. The complete capability tiers are in [capabilities.md](../docs/capabilities.md), included in this submission kit, and in the packaged skill/source README.

## Publication provenance

Use only artifacts produced by the repository’s manually dispatched GitHub Actions Release workflow for submission. Local archives are validation builds. The GitHub repository may be public while publisher identity, final legal URLs, availability decisions and live cloud/mobile tests remain incomplete; public source availability does not claim directory approval.
