# Privacy and data handling

Mood Journal ships instructions and development/release scripts. It includes no telemetry, hosted database, bundled connector, automatic record collection, or background journal job. The host model processes conversation content under its own terms. A chosen storage provider may process records under its own policies.

The skill instructs the host to use authorized storage only, disclose pending saves, and keep sensitive records outside this distribution repository. Actual permissions, encryption, retention, deletion, access controls, and tool availability belong to the host and selected backend. Local files and ZIPs are not inherently encrypted.

Do not put real journal content, medical records, access tokens, or private transcripts in public issues, commits, tests, release notes, or release artifacts. Use fictional examples. Automatic skill selection is enabled, but ordinary emotional conversation is not authorization to store it.

A release archive is software/instructions, not a backup of the user's journal. Release packaging uses an explicit allowlist and tracked files; this does not make it safe to commit private material within those allowed paths.
