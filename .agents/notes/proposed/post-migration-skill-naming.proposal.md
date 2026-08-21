# Post-migration skill naming review

Revisit the public names `plan` and `build-plan` only after source-home migration is complete and installed skills have been safely reconciled.

## Prerequisites

- The installer supports migration of existing source paths, renames, retirements, and declared dependencies.
- The target source-home tree has been applied without breaking existing installations.
- Supported runtime behavior has been verified in the environments that will expose the skills.

## Decision to make

Evaluate whether simpler public names improve usability without creating ambiguous or conflicting skill identities. Do not add runtime-command invocation guidance to documentation before that review has verified a specific runtime need.
