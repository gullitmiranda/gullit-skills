# Known Compromised Tool Versions

Reference list of tools with known supply-chain incidents. Check this before
enabling new tools or upgrading existing ones.

Last updated: 2026-04-01

## Trivy (aquasecurity/trivy)

**Incident**: March 19-23, 2026 -- TeamPCP supply chain attack
**Compromised versions**: v0.69.4, v0.69.5, v0.69.6
**Safe versions**: v0.69.3 and below; v0.70.0+ (post-remediation)
**Impact**: Credential-stealing malware injected into official releases. Targeted
CI/CD secrets, cloud credentials (AWS/GCP/Azure), SSH keys, K8s tokens, Docker
registry tokens, database credentials. Exfiltrated as encrypted archives.
**Distribution**: GitHub Releases, Docker Hub, GHCR, ECR Public, deb/rpm repos.
**CVE**: CVE-2026-336
**References**:
- https://www.microsoft.com/en-us/security/blog/2026/03/24/detecting-investigating-defending-against-trivy-supply-chain-compromise/
- https://www.aquasec.com/blog/trivy-supply-chain-attack-what-you-need-to-know/

### Also affected via same campaign

- **trivy-action** (GitHub Action): 75 of 76 version tags compromised
- **setup-trivy** (GitHub Action): all tags except v0.2.6
- **Checkmarx KICS**: compromised March 23, 2026
- **LiteLLM**: compromised March 24, 2026

## Checkov (bridgecrewio/checkov)

**Status**: No known compromise as of 2026-04-01, but shares the same
distribution pattern as Trivy (Python package on PyPI + GitHub releases).
Monitor for advisories.

## General Risk Indicators

Tools with higher supply-chain risk share these traits:
- Large dependency trees (transitive dependencies)
- Binary downloads from GitHub Releases (no reproducible builds)
- GitHub Actions with mutable version tags (not pinned to SHA)
- Maintainers with broad CI/CD access across multiple projects

## How to Check a Tool Before Enabling

1. Search `https://github.com/advisories` for the tool name
2. Check `https://security.snyk.io` for known vulnerabilities
3. Verify the GitHub repo hasn't had force-pushes on release tags:
   `gh api repos/OWNER/REPO/git/refs/tags --jq '.[].ref'`
4. Compare binary sha256 with official release notes
