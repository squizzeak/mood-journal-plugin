# Repository instructions for contributors and coding agents

## Purpose and scope

Mood Journal is a distributable, storage-neutral journaling skill plugin. This repository contains instructions, fictional tests, optional deterministic helpers, metadata, documentation, and release tooling. It is not a live journal or a storage service. Read README.md and the relevant skill reference before changing behavior. Follow explicit maintainer instructions; report material ambiguities without inventing product requirements.

## Repository map

- `plugins/mood-journal/skills/mood-journal/SKILL.md`: runtime entrypoint and non-negotiable workflow boundaries.
- `references/` within that skill: informed setup, storage, record schemas, historical ingestion, inquiries, handoffs, prompts.
- `scripts/` within that skill: optional standard-library ingestion and handoff-inventory helpers. Core native/cloud/mobile use must not require Python.
- `plugins/mood-journal/plugin.json` and `.codex-plugin/plugin.json`: portable manifest and compatibility overlay.
- `.agents/plugins/marketplace.json`: repository marketplace catalog.
- Root `scripts/`: package validation and deterministic release assembly.
- `tests/`: executable fictional regressions and manual behavioral acceptance scenarios.
- `submission/`: listing worksheet, graphics references, acceptance cases and actual test results.
- `docs/`: capability boundaries and dated research; `.github/workflows/`: CI and manual releases.

Use code graph discovery when available and current; otherwise targeted searches and reads. Avoid broad scans of unrelated directories. This repository's rules do not authorize access to private material outside it.

## Privacy and provenance

Use fictional records only. Never copy personal journal entries, clinical histories, private chat exports, user account identifiers, credentials, local machine paths, Rosetta development-note IDs, or sensitive source transcripts into commits, issues, logs, test fixtures, screenshots, or artifacts. Retained public creator attribution is intentional. Do not modify installed skills, plugin caches, local registries, or synced project sources while developing this distribution.

Review tracked content and proposed commit messages before pushing; releases derive notes from those messages. Inspect history as well as the latest tree before first publication. `.gitignore` and archive allowlists do not make sensitive committed content safe. Preserve originals and do not perform destructive cleanup without explicit scope. Do not add telemetry, a hosted service, secrets, or required provider integration as an incidental implementation choice.

## Runtime invariants

- Strict single-agent chat interaction: no sub-agents, delegated read-only review, cross-chat dispatch, or background agent workers. Direct tools and deterministic helpers are permitted. Future delegation requires an explicit product decision.
- Projects are optional organizational containers. Stable journal identity is independent of chat, project, and backend. Preserve source scope and separate journals.
- Informed setup explicitly acquires missing preferences after explaining available capabilities and tradeoffs. Reuse existing explicit choices. Defaults are recommendations, not consent.
- A sole capable storage plugin is the suggested backend; multiple capable plugins suggest native persistence when available. Honor the selected backend. No silent provider change or fabricated native file capability.
- Full/impromptu journal sessions stage content until explicit close. Authorized one-off logs save after setup. Silence/disconnection is not close. No-save boundaries remain authoritative.
- Distinguish full verified storage, acknowledged summary memory, retained conversation, unverified writes, and unsaved work. No mandatory manual Save-to-project step.
- Optional require-project behavior is not a security boundary. Unknown trusted project identity pauses restricted operations; do not claim host permissions or a global session lock.
- Historical import produces normal canonical journal work, with original dates, provenance, supported context/inquiry state and explicit gaps. Do not manufacture missing quotes, past verification or clinician coverage.
- Migration preserves IDs and source history, verifies destination before routing cutover, and performs only explicitly scoped optional cleanup afterward. Lossy migration cannot justify deletion of full originals.
- Handoff creation requires complete highest-version discovery, numeric ordering, resolved canonical lineage and separate verified coverage baseline. First search hit is insufficient. Incomplete inventory means provisional unnumbered output; no cutoff advancement.
- Preserve user wording, uncertainty, chronology and current-versus-historical evidence. Do not diagnose, infer another person's intentions, or transmit handoffs to others without explicit sending authorization.

## Metadata and compatibility

Keep portable and compatibility manifest name/version/description synchronized; the OpenAI interface must match. Keep skill references relative and self-contained. Include required notices in the standalone skill package. Retain CC BY-SA 4.0 attribution and document adaptations. Do not fabricate unsupported manifest fields to imply permissions or enforcement.

Preserve native cloud/mobile/local fallback behavior without adding mandatory shell, Python, Rosetta, search API, or MCP dependencies. Update README, capability notes, setup explanations and relevant acceptance cases together when behavior changes. A package validator is not OpenAI approval or proof of live compatibility. Submission identity, legal URLs, attestations and live test results must reflect verified facts.

## Validation

Run from the repository root before committing completed changes:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Use Python 3.11+ for development/release tooling. No third-party dependency is required for those checks. Add meaningful executable regressions for helper/release behavior changes; add fictional behavioral scenarios for instruction changes. Do not call manual scenarios passed until actually exercised. `python3 scripts/validate.py --submission` is a separate completeness gate and is expected to fail until all real publisher fields, attestations and live results are supplied. Do not weaken it to make CI green.

For metadata/assets, verify both manifests, relative resource links, image presentation and standalone bundle contents. For storage/handoff changes cover partial reads, retries, duplicate identities, unavailable capability and no-save cases. Deterministic tests do not certify conversational compliance or host permissions.

## Git and release discipline

Use clear commit subjects, preferably Conventional Commits, containing no sensitive information. Preserve history and unrelated changes; no force pushes, tag reassignment or history rewriting after publication without explicit maintainer authorization. Keep the working tree clean at release preparation.

GitHub Actions is the authoritative source of initial and subsequent distributed artifacts. Root `dist/` and `.release/` are ignored local validation outputs; never upload them as official release assets. Do not run local version preparation on the main development checkout. Exercise release code in disposable test repositories when needed.

Only `.github/workflows/release.yml` workflow_dispatch may publish a GitHub release. The separate submission-preparation workflow may run after a published release to verify assets and prepare drafts; it must not submit to OpenAI or perform attestations. Optional Copilot editorial generation is development automation over public release text, not runtime journal delegation; keep it opt-in, without delegation or permitted tools, and document billing. Do not purchase or enable paid usage implicitly. CI on pushes/PRs validates but must not publish. Default dispatch is build-only. Publish only after explicit authorization and from the default branch. Do not bypass branch protections. Minimize workflow permissions, quote shell variables, and keep untrusted commit subjects as data.

The workflow owns UTC CalVer versions and CHANGELOG.md release sections. Until the first Actions publication, keep only the unpublished changelog placeholder; the initial workflow derives notes from all non-release commits. Subsequent notes use commits after the latest applicable published stable release. Never invent a prior release from a local build or draft.

Preserve the four allowlisted packages (directory, skills, marketplace, submission kit), release notes, provenance and checksums. Package tracked allowlisted paths only; reject symlinks and unsafe archive paths. GitHub's automatic source archive is not the directory upload package.

If publishing fails after the branch/tag push, preserve that tag and finish the draft with the exact Actions-produced assets. Do not delete/reassign the tag or rerun preparation to hide a partial release. Verify remote commit, workflow conclusion, asset inventory and checksums before reporting publication complete. GitHub publication is separate from ChatGPT directory submission/approval.

## Project tracking

Use GitHub Issues for actionable tasks, missing publisher inputs, bugs and acceptance work; use GitHub Discussions for design decisions, research notes and the development hub. GitHub is the authoritative tracker for this repository. Do not create new Rosetta development records or duplicate active tasks there. Existing Rosetta records are retired migration history, not the current backlog. Keep development tracking separate from users’ runtime journal storage, which remains provider-neutral. Search existing issues/discussions before creating duplicates and preserve decisions, evidence and unresolved limitations. Never post personal journal content to public tracking.

## Reporting changes

Report what changed, why, validation performed and material limitations. Identify tests not run, pending publisher inputs and host behavior still unverified. Never claim an install, save, migration, release, or directory approval solely because files were generated.
