# OpenAI directory submission guide

This is the maintainer runbook for submitting Mood Journal as a **skills-only plugin**. The [main README](../README.md#submitting-to-the-openai-plugins-directory) provides the overview. [Issue #2](https://github.com/squizzeak/mood-journal-plugin/issues/2) tracks the actual submission, review and publication. No submission has been made. `listing.json` is our worksheet, not an OpenAI API payload.

## Contents

- [Route and authority](#route-and-authority)
- [Field-to-file checklist](#field-to-file-checklist)
- [Preparation order](#preparation-order)
- [Testing and evidence](#testing-and-evidence)
- [Package selection](#package-selection)
- [Release and submission notes](#release-and-submission-notes)
- [Automated preparation and Copilot](#automated-preparation-and-copilot)
- [Billing and the existing ChatGPT subscription](#billing-and-the-existing-chatgpt-subscription)
- [Portal procedure](#portal-procedure)
- [Review, publication and updates](#review-publication-and-updates)

## Route and authority

OpenAI documents a skills-only route: no hosted MCP server is required for this plugin. The optional storage providers used by users are not bundled existing-integration references. Core journaling requires no local executable, required storage connector, or shell. Do not invent native file-write capabilities or guaranteed cross-device retention in the listing.

Before submission, recheck [official submission instructions](https://developers.openai.com/plugins/deploy/submission), [package documentation](https://developers.openai.com/plugins/build/plugins), and the live portal. Requirements and accepted upload controls can change. The reviewed documentation describes portal submission, not a supported public submission API. Automatic portal submission, attestations, approval and publication are **not implemented**. Do not reverse-engineer private endpoints, copy browser cookies to Actions, or imply an ordinary OpenAI API key can publish a plugin.

## Field-to-file checklist

| Portal material | Repository source | Completion evidence / owner task |
| --- | --- | --- |
| Product name, descriptions, category | `listing.json`; both plugin manifests | Reviewed copy matching actual behavior; #12 |
| Developer identity / submission access | Verified publisher decision, selected Platform organization | Verified individual/business identity and Apps Management write access; #7. Keep private verification documents out of GitHub. |
| Website/support URLs | `listing.json`, finalized public publisher metadata | URLs publicly resolve and match the publisher; #6 |
| Privacy/terms URLs | Root `PRIVACY.md`, `TERMS.md`, final hosted copies | Publisher-reviewed terms/data handling; reachable canonical URLs; #6 |
| Countries/regions | `listing.json` | Explicit availability decision; #5 |
| Logo/prompt-preview image | `plugins/mood-journal/assets/` | Visual review and accepted portal formats; #12 |
| Skill bundle | Packaged `SKILL.md`, references, optional helpers and notices | Tested final tree, exact release/commit and checksums; #13 |
| Starter prompts | `listing.json` and manifests | Realistic triggering examples; #12 |
| Five positive / three negative cases | `test-cases.json` | Reproducible fictional fixtures and expected behavior; #3 |
| Live test results | `test-results.md`, behavioral scenarios | Actual date, host/version, surface, case and observation; #3 |
| Reviewer notes and user-facing changes | Prepared drafts plus review evidence | Edited for accuracy; initial/update status and reviewer setup confirmed |
| Policy attestations | Publisher review and actual portal | Accurate authorized attestations; #2. Never set flags merely to pass validation. |
| Submission/review/publication record | Issue #2 and portal receipt/status | Exact submitted version and outcome; no private portal credentials or account IDs in public issues |

## Preparation order

1. Gather identity/access, public URLs and availability decisions (#7, #6, #5). Prepare a portal draft if needed to access supported testing facilities; do not submit yet.
2. Populate/review listing and manifests in #12; keep unknown fields unfilled. Test the local package with fictional fixtures. Local artifacts are sufficient for build testing at this stage.
3. Run actual supported cloud web, mobile, and relevant storage-mode tests (#3). Record limitations and failures. If a pre-submission test surface is unavailable, record the gap and seek the official supported testing route; do not claim it passed.
4. Complete the publisher's substantive policy review. Record truthful worksheet flags for completed verification and testing; portal-only attestations remain pending until made. Run normal validation throughout. Run `python3 scripts/validate.py --submission` as the final worksheet completeness check only when its required facts are true. It checks presence/flags, not identity ownership, URL reachability, semantic quality, or OpenAI approval.
5. Commit the reviewed package materials. Generate the exact submission packages through GitHub Actions (#13) when ready. A public GitHub Release is our distribution/provenance choice, not an OpenAI prerequisite. Do not rebuild or edit an uploaded ZIP in place.
6. Review the generated editorial drafts and portal form, complete accurate portal attestations and any remaining checklist entries, and submit in #2. If the prior submitted version differs from the previous GitHub release, revise the change summary to cover the correct interval.

All commands run from the source repository root; the supporting submission kit does not contain root development scripts. GitHub blocked-by relationships record the order but do not prevent someone from using the external portal.

## Testing and evidence

Use only fictional conversations and supported installation/test surfaces. A local checkout is not a cloud/mobile installation. Record date, app/host version, web/iOS/Android/voice surface as applicable, fixture, prompt, expected behavior, actual result and evidence. Never mark unrun cases as passed.

Cover explicit informed setup, single-agent operation, ordinary and project chats, optional require-project behavior with absent identity, available full/native/plugin/local/single-record/summary/chat storage, no-save and explicit-close boundaries, unsupported capability disclosures, interrupted saves, voice transcription uncertainty, historical/live parity, backend migration/cleanup, and highest-handoff-version discovery. Test across devices only when the same authorized destination is actually accessible. Read-back and lineage tests matter independently of conversational quality. See [capability notes](../docs/capabilities.md).

## Package selection

| Artifact | Intended use |
| --- | --- |
| `mood-journal-VERSION-skills.zip` | Final skill bundle for the documented Skills upload step; includes references/helpers/notices |
| `mood-journal-VERSION-directory.zip` | Portable root plugin package if the live portal accepts a plugin-package upload |
| `mood-journal-VERSION-submission-kit.zip` | Supporting listing/test/legal materials and graphics; not the skill upload |
| `mood-journal-VERSION-marketplace.zip` | Repository marketplace distribution; not the default public-directory upload |
| `RELEASE-NOTES.md`, `BUILD-INFO.json`, `SHA256SUMS` | Technical change record, provenance and integrity checks |

Confirm the actual accepted layout/size/image controls in the live portal. Use the same tested file tree. Optional Python helpers remain optional; they do not create a required local runtime. GitHub's automatic source ZIP is not the curated skill bundle.

## Release and submission notes

Maintain three distinct documents:

- **Technical changelog:** deterministic commit-derived engineering history since the previous published GitHub release. Preserve it unchanged.
- **User-facing changelog:** concise plain-language improvements/fixes and relevant limitations, omitting internal housekeeping. Explain concrete benefits, not commit mechanics. Generated text is a draft; verify against actual implementation and test evidence.
- **Reviewer submission notes:** what the plugin does, initial submission or update, changes since the prior *submitted* version, supported surfaces, reproducible setup/fixtures, and material limitations. Do not infer submission history from GitHub tags. No approval, clinical-outcome, storage, security or privacy claim may exceed evidence.

Suggested reviewer structure: product purpose; candidate version/commit; initial/update status; user-visible changes; testing/setup; limitations; exact package references. Link final reviewed notes and checksums in #2. Do not copy raw internal commit subjects as the entire reviewer narrative.

## Automated preparation and Copilot

`.github/workflows/prepare-submission.yml` prepares drafts after a stable release is published. The Release workflow calls it explicitly after successful publication; this avoids relying on a release event suppressed when created with `GITHUB_TOKEN`. A `release: published` trigger covers other publication routes, and manual dispatch accepts an exact published tag or resolves latest once. It never runs from an ordinary push/PR or a build-only Release dispatch.

Preparation resolves a published stable release, downloads its existing assets, validates checksums/archive paths and the clean tagged-commit provenance, and produces an Actions artifact containing a listing snapshot, technical notes, reviewer-note draft, user-changelog draft, and provenance/readiness report. It uses the packaged release metadata, not unreleased worksheet changes. Missing fields stay listed as blockers; nothing is submitted, auto-attested, posted to OpenAI, or marked approved. Drafts are not attached to or substituted for the immutable release packages.

Copilot drafting is **off by default**. To enable it, an authorized maintainer must:

1. Verify Copilot CLI eligibility, current billing/usage controls and a compatible tested CLI version.
2. Set repository variable `SUBMISSION_COPILOT_CLI_VERSION` to that exact numeric version.
3. Set `SUBMISSION_COPILOT_ENABLED=true` after accepting the usage implications. No PAT is required by this workflow: it uses the documented short-lived `GITHUB_TOKEN` with `copilot-requests: write`.
4. Test on an existing published release when one exists; inspect the draft before using it. If generation fails, preparation reports failure while retaining available deterministic drafts; there is no silent claim of successful AI generation.

GitHub documents billing personally owned repository requests to the owner's Copilot seat. This is development editorial automation, not delegation of user journal work. The Copilot process receives bounded public release text, runs in an empty directory with fresh configuration, has built-in MCP disabled, no delegation tools, and no permitted read/write/shell/network tools. It returns text only. The workflow has no OpenAI credentials and does not pass personal journal data. Track final copy review in [issue #15](https://github.com/squizzeak/mood-journal-plugin/issues/15) and live portal/account preflight in [issue #16](https://github.com/squizzeak/mood-journal-plugin/issues/16). Human editorial review remains necessary; tool restrictions do not make model output factual or deterministic.

Sources checked 2026-09-12: [Copilot in Actions](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-in-actions), [authentication and billing](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/copilot-cli-in-github-actions), [programmatic CLI options](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference).

## Billing and the existing ChatGPT subscription

Billing facts checked 2026-09-12; account entitlement and remaining allowance have not been inspected. Do not assume a particular ChatGPT or Copilot plan from the existence of this repository.

| Component | What is required / billed | Does an existing ChatGPT subscription cover it? |
| --- | --- | --- |
| Local validation and package builds | Python/Git on your machine; no model/API call in deterministic scripts | No subscription needed |
| Standard GitHub Actions runner | This public repo uses standard Ubuntu runners; standard public-repo runner minutes are free. Artifact storage/retention and any future larger/private runners follow GitHub billing rules. | No; GitHub billing is separate |
| Deterministic submission preparation | Same Actions infrastructure; no AI token/API expenditure | No additional AI subscription needed |
| Optional Copilot changelog generation | Copilot CLI access and available GitHub AI credits under the account's actual plan. CLI is offered across Copilot plans, including Free, but allowance/model/access must be checked. `GITHUB_TOKEN` authentication does not mean free model usage; personal-repo usage is billed to the owner's Copilot seat. | No; ChatGPT does not supply Copilot entitlement or credits |
| Interactive drafting and plugin testing in ChatGPT | Can use your existing subscription within its supported features and limits. It can help edit public release text and test available plugin surfaces. | Yes, for supported interactive use; it does not guarantee developer access, all test modes, or unlimited usage |
| OpenAI API generation, if added later | Separate API credentials, usage billing and budget; not used by these workflows | No; API billing is separate from ChatGPT subscriptions |
| OpenAI portal submission | Verified publisher and submission permissions. Reviewed submission docs do not establish a per-submission charge; confirm any actual fee/account requirement in the live portal. No paid API balance requirement is asserted for this skills-only workflow. | A subscription is not proof of publisher verification or portal access |
| Optional storage backend | Depends on the user's chosen provider and plan; no paid backend is bundled or required | Only if that particular native capability is included; third-party charges remain separate |

**No-Copilot path:** leave `SUBMISSION_COPILOT_ENABLED` unset/false. Deterministic preparation and local build testing still work. Edit the draft yourself or use the existing ChatGPT subscription interactively with public release text, then review and retain the final notes. Do not copy ChatGPT session cookies/OAuth credentials into Actions or treat the subscription as a general-purpose API credential.

Before enabling Copilot, record the current plan/allowance, eligible models, payer, permitted overage/budget settings, and explicit choice in [billing/configuration issue #14](https://github.com/squizzeak/mood-journal-plugin/issues/14). Included credits may be sufficient; buying a paid plan is not assumed. No subscription purchase, paid usage enablement or account-setting change was performed here. Timeouts bound runtime but are not dollar-spend caps. Reruns can consume additional credits; keep automatic generation off until those choices are resolved. Draft Actions artifacts expire after seven days; preserve reviewed submission evidence in the tracker or approved release process before expiration.

Sources: [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [Copilot CLI availability](https://github.com/features/copilot/cli), [Copilot billing](https://docs.github.com/en/billing/concepts/product-billing/github-copilot-billing), [CLI Actions billing](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/copilot-cli-in-github-actions), [ChatGPT versus API billing](https://help.openai.com/en/articles/9039756-billing-settings-in-chatgpt-vs-platform).

## Portal procedure

1. Select the correct publishing organization and verified identity in OpenAI Platform. Confirm Apps Management write access.
2. Open the plugin submission portal from the current official instructions; create/open the tracked draft and select **Skills only**.
3. Populate Info, Skills, Prompts, Testing and Global sections as exposed by the portal. Use the reviewed field-to-file mapping; omit MCP-server setup for this skills-only package.
4. Upload the tested bundle. Review scanning/validation results and remediate real failures. Do not bypass checks or invent accepted formats.
5. Review the complete draft, insert the edited reviewer notes, and make truthful policy attestations. Select Submit for Review only when prerequisites are satisfied and submission is authorized.
6. Record date, version, source commit, Actions run, exact artifact hashes, safe receipt/status and any reviewer requirements in #2. Keep credentials and private verification evidence out of public tracking.

## Review, publication and updates

Submission starts review; approval is separate. Track feedback, revisions and resubmissions in #2 with their exact versions. Do not overwrite a prior submission record. After approval, the publisher chooses when to publish in the portal; verify and record the resulting public listing URL and availability. Rejection/withdrawal is an explicit outcome, not successful publication. Keep the tracker open until the intended outcome or an explicitly accepted terminal disposition.

For updates, repeat the applicable tests and review, build a new version, and submit the changed skill snapshot. A GitHub release does not update the directory automatically. An official public submission API could support more automation in the future; none was established in the reviewed documentation. Retain the manual portal boundary until a supported interface, authentication model, attestations, idempotency and status handling are verified.
