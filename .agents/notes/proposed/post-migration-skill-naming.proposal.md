# Post-migration skill naming review

Revisit the public names `work-plan` and `build-plan` only after the target source-home tree is complete and skills have been reinstalled from it.

## Prerequisites

- The target source-home tree is complete.
- Skills have been reinstalled from a clean state before the CLI rewrite continues.
- Supported runtime behavior has been verified in the environments that will expose the skills.

## Decision to make

Evaluate whether simpler public names improve usability without creating ambiguous or conflicting skill identities. Do not add runtime-command invocation guidance to documentation before that review has verified a specific runtime need.

## Compatibility cleanup

Reinstall skills with the rewritten CLI rather than preserving legacy wrapper skills. New installations must not discover or install legacy aliases as ordinary skills.
