# Post-migration skill naming review

Revisit the public names `work-plan` and `build-plan` only after the target source-home tree is installed by the rewritten CLI.

## Prerequisites

- The rewritten installer supports the target source-home tree and declared dependencies.
- Skills can be reinstalled from a clean state after the CLI rewrite.
- Supported runtime behavior has been verified in the environments that will expose the skills.

## Decision to make

Evaluate whether simpler public names improve usability without creating ambiguous or conflicting skill identities. Do not add runtime-command invocation guidance to documentation before that review has verified a specific runtime need.

## Compatibility cleanup

Reinstall skills with the rewritten CLI rather than preserving legacy wrapper skills. New installations must not discover or install legacy aliases as ordinary skills.
