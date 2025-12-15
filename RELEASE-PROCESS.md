# Release Process
## QMS Dashboard Release Governance

**Document Version:** 1.0
**Effective Date:** 2025-12-15
**Phase:** 7 WS-4 - Release Governance

---

## Overview

This document defines the formal release process for QMS Dashboard, establishing version control, release manifest generation, and change documentation procedures suitable for audit environments.

**Purpose:** Ensure repeatable, traceable, and auditable software releases.

**Scope:** All QMS Dashboard releases from Phase 7 onward.

---

## Table of Contents

1. [Versioning Strategy](#versioning-strategy)
2. [Release Types](#release-types)
3. [Release Preparation](#release-preparation)
4. [Release Manifest](#release-manifest)
5. [Change Log Requirements](#change-log-requirements)
6. [Release Checklist](#release-checklist)
7. [Release Artifacts](#release-artifacts)
8. [Rollback Procedures](#rollback-procedures)
9. [Verification Requirements](#verification-requirements)
10. [Compliance & Audit](#compliance--audit)

---

## Versioning Strategy

### Semantic Versioning (SemVer)

QMS Dashboard follows [Semantic Versioning 2.0.0](https://semver.org/):

**Format:** `MAJOR.MINOR.PATCH` (e.g., `0.7.2`)

**Version Components:**

- **MAJOR** - Incompatible API changes or breaking changes
- **MINOR** - New functionality in backward-compatible manner
- **PATCH** - Backward-compatible bug fixes

### Pre-1.0 Versioning (Current)

**Status:** QMS Dashboard is currently in `0.x.x` (pre-production development)

**Pre-1.0 Rules:**
- `0.x.0` - Major phase completions (e.g., `0.7.0` = Phase 7 start)
- `0.x.y` - Workstream completions or patches (e.g., `0.7.1`, `0.7.2`)
- Breaking changes allowed in MINOR versions during 0.x

**Example Pre-1.0 Version History:**
```
0.1.0 - Phase 1: Core Intake System
0.2.0 - Phase 2: Risk Classification
0.3.0 - Phase 3: Multi-Layer Validation
0.4.0 - Phase 4: Artifact Generation
0.5.0 - Phase 5 v1: Expert Review Recording
0.6.0 - Phase 6: Verification & Testing
0.7.0 - Phase 7 WS-1: Runtime Hardening
0.7.1 - Phase 7 WS-2: Security Controls
0.7.2 - Phase 7 WS-3: Operational Documentation
```

### Post-1.0 Versioning (Future)

**1.0.0 Release Criteria:**
- All Phase 7 workstreams complete
- Full Phase 6 test suite passing
- Production deployment validated
- Operations documentation complete
- Security hardening complete

**Post-1.0 Breaking Change Policy:**
- MAJOR version bump required for breaking changes
- Deprecation warnings in MINOR version before removal in MAJOR
- Migration guides required for MAJOR version changes

---

## Release Types

### 1. Phase Release (MINOR)

**Definition:** Completion of a major development phase or significant feature set.

**Versioning:** `0.x.0` increment (pre-1.0) or `1.x.0` increment (post-1.0)

**Requirements:**
- All phase objectives met
- Full regression test suite passing
- CHANGELOG updated with phase summary
- Phase verification report (if applicable)

**Example:** `0.7.0` - Phase 7 WS-1: Runtime & Environment Hardening

### 2. Workstream Release (PATCH)

**Definition:** Completion of a specific workstream within a phase.

**Versioning:** `0.x.y` increment (pre-1.0) or `1.x.y` increment (post-1.0)

**Requirements:**
- Workstream deliverables complete
- Regression tests passing
- CHANGELOG updated with workstream details

**Example:** `0.7.1` - Phase 7 WS-2: Security & Access Controls

### 3. Hotfix Release (PATCH)

**Definition:** Emergency fix for critical production issues.

**Versioning:** `x.y.z` increment (PATCH only)

**Requirements:**
- Critical issue documented
- Fix tested in isolation
- Regression tests passing
- CHANGELOG updated with hotfix details
- Expedited release (skip normal timeline)

**Example:** `0.7.3` - Hotfix for critical security vulnerability

### 4. Maintenance Release (PATCH)

**Definition:** Routine bug fixes, documentation updates, dependency updates.

**Versioning:** `x.y.z` increment (PATCH only)

**Requirements:**
- Non-breaking changes only
- All tests passing
- CHANGELOG updated

---

## Release Preparation

### 1. Pre-Release Checklist

**Code Readiness:**
- [ ] All planned features/fixes complete
- [ ] Code reviewed (if multi-developer)
- [ ] No outstanding critical bugs
- [ ] All TODOs addressed or documented

**Testing:**
- [ ] Unit tests passing (if applicable)
- [ ] Integration tests passing
- [ ] Phase 6 regression tests passing (6/6)
- [ ] Manual verification complete

**Documentation:**
- [ ] CHANGELOG.md updated with new version entry
- [ ] Breaking changes documented (if any)
- [ ] Migration guide written (if breaking changes)
- [ ] API documentation updated (if API changes)

**Version Control:**
- [ ] All changes committed
- [ ] Working directory clean (`git status`)
- [ ] On correct branch (e.g., `main` or `release/x.y.z`)

### 2. Version Increment

**Determine Version Number:**
1. Review changes since last release
2. Apply SemVer rules (MAJOR/MINOR/PATCH)
3. Update version in relevant files:
   - `CHANGELOG.md` (version heading)
   - `src/backend/main.py` (if version constant exists)
   - `pyproject.toml` or `setup.py` (if packaging)

**Example:**
```bash
# Current version: 0.7.2
# Next version: 0.7.3 (WS-4 completion)

# Update CHANGELOG.md
vim CHANGELOG.md
# Add: ## [0.7.3] - 2025-12-15

# Commit version change
git add CHANGELOG.md
git commit -m "chore: bump version to 0.7.3"
```

### 3. Generate Release Manifest

**Run manifest generation script:**
```bash
python3 scripts/generate-release-manifest.py 0.7.3
```

**Output:** `releases/RELEASE-MANIFEST-0.7.3.md`

(See [Release Manifest](#release-manifest) section for format details)

---

## Release Manifest

### Purpose

The release manifest provides a complete, auditable record of:
- What is included in the release
- What changed since the last release
- Verification status (tests passing, security scan results)
- File integrity checksums (optional)

### Manifest Format

**File:** `releases/RELEASE-MANIFEST-{VERSION}.md`

**Template:**

```markdown
# Release Manifest
## QMS Dashboard v{VERSION}

**Release Date:** YYYY-MM-DD
**Release Type:** Phase / Workstream / Hotfix / Maintenance
**Previous Version:** {PREVIOUS_VERSION}

---

## Release Summary

{One-paragraph summary of what this release delivers}

---

## Changes Included

### Added
- {New features or capabilities}

### Changed
- {Modifications to existing functionality}

### Fixed
- {Bug fixes}

### Security
- {Security improvements or fixes}

---

## Verification Status

**Test Results:**
- Phase 6 Regression Tests: {PASS_COUNT}/{TOTAL_COUNT} passing
- Integration Tests: {PASS_COUNT}/{TOTAL_COUNT} passing
- Security Scan: {PASS/ADVISORY/FAIL}

**Verification Date:** YYYY-MM-DD
**Verified By:** {Name/Role}

---

## Breaking Changes

{List breaking changes, or "None" if backward compatible}

**Migration Required:** Yes / No

{If yes, link to migration guide or include steps}

---

## Files Modified

**Source Code:**
- src/backend/config.py (198 lines, +198/-0)
- src/backend/main.py (450 lines, +50/-20)
- ...

**Documentation:**
- CHANGELOG.md (+50 lines)
- doc/runtime-config.md (600 lines, +600/-0)
- ...

**Tests:**
- tests/integration/test_security.py (+100 lines)

---

## Dependencies

**No dependency changes** / **Dependency changes:**
- Added: package-name==1.2.3
- Updated: another-package 1.0.0 → 1.1.0
- Removed: deprecated-package

---

## Deployment Notes

**Environment Variables:**
- {List any new or changed environment variables}

**Data Migration:**
- {Describe any data migration steps, or "None required"}

**Rollback Procedure:**
- {Link to rollback section or describe specific steps}

---

## File Integrity (Optional)

**SHA-256 Checksums:**
```
{CHECKSUM}  src/backend/main.py
{CHECKSUM}  src/backend/config.py
...
```

**Manifest Checksum:**
```
{CHECKSUM}  RELEASE-MANIFEST-{VERSION}.md
```

---

**Manifest Generated:** YYYY-MM-DD HH:MM:SS UTC
**Manifest Version:** 1.0
```

### Manifest Generation Script

**File:** `scripts/generate-release-manifest.py`

```python
#!/usr/bin/env python3
"""
Generate release manifest for QMS Dashboard releases.

Usage:
    python3 scripts/generate-release-manifest.py 0.7.3
"""

import sys
import hashlib
from pathlib import Path
from datetime import datetime

def generate_manifest(version: str):
    """Generate release manifest for the specified version."""
    manifest_dir = Path("releases")
    manifest_dir.mkdir(exist_ok=True)

    manifest_path = manifest_dir / f"RELEASE-MANIFEST-{version}.md"

    # Extract changes from CHANGELOG.md
    changes = extract_changelog_entry(version)

    # Get file list and checksums
    files = get_modified_files()

    # Generate manifest
    manifest_content = format_manifest(version, changes, files)

    # Write manifest
    with open(manifest_path, 'w') as f:
        f.write(manifest_content)

    print(f"✅ Release manifest generated: {manifest_path}")

def extract_changelog_entry(version: str) -> dict:
    """Extract the changelog entry for this version."""
    # Implementation: Parse CHANGELOG.md for version section
    pass

def get_modified_files() -> list:
    """Get list of files modified since last release."""
    # Implementation: Use git diff or file timestamps
    pass

def format_manifest(version: str, changes: dict, files: list) -> str:
    """Format the release manifest content."""
    # Implementation: Format according to template
    pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 generate-release-manifest.py <version>")
        sys.exit(1)

    version = sys.argv[1]
    generate_manifest(version)
```

### Manual Manifest Creation

If automated generation is not available:

1. Copy template from this document
2. Fill in version-specific details
3. Extract changes from CHANGELOG.md
4. Run test suite and record results
5. List modified files (use `git diff --stat`)
6. Generate checksums: `sha256sum src/backend/*.py`
7. Save to `releases/RELEASE-MANIFEST-{VERSION}.md`

---

## Change Log Requirements

### CHANGELOG.md Format

QMS Dashboard follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

**Required Sections for Each Release:**

```markdown
## [VERSION] - YYYY-MM-DD

### {Phase/Workstream Title}

**Objective:** {One-line description of release purpose}

#### Added
- {New files, features, capabilities}

#### Changed
- {Modified behavior, refactored code}

#### Fixed
- {Bug fixes}

#### Security
- {Security improvements}

#### Breaking Changes
{Description of breaking changes, or "None"}

#### Verification
- {Test results}
- {Security scan results}
```

### Change Log Enforcement

**Pre-Release Check:**
```bash
# Verify CHANGELOG.md has entry for new version
grep -q "## \[$NEW_VERSION\]" CHANGELOG.md || {
    echo "❌ CHANGELOG.md missing entry for version $NEW_VERSION"
    exit 1
}

# Verify release date is set (not "Unreleased")
grep "## \[$NEW_VERSION\] - [0-9]" CHANGELOG.md || {
    echo "❌ CHANGELOG.md missing release date for version $NEW_VERSION"
    exit 1
}

echo "✅ CHANGELOG.md verification passed"
```

**Enforcement in Release Process:**
- Pre-release checklist includes CHANGELOG verification
- Automated release script checks for version entry
- Release manifest links to CHANGELOG section

---

## Release Checklist

### Pre-Release (Development Complete)

- [ ] All planned work complete
- [ ] Code reviewed (if applicable)
- [ ] All tests passing
  - [ ] Phase 6 regression tests: 6/6
  - [ ] Integration tests (if applicable)
  - [ ] Security utilities tests (if applicable)
- [ ] Documentation updated
  - [ ] CHANGELOG.md has version entry with date
  - [ ] Breaking changes documented
  - [ ] Migration guide written (if needed)
- [ ] Version number determined (SemVer)
- [ ] Git working directory clean

### Release Creation

- [ ] Version number updated in CHANGELOG.md
- [ ] Release manifest generated
  - [ ] `releases/RELEASE-MANIFEST-{VERSION}.md` created
  - [ ] Manifest includes test results
  - [ ] Manifest includes file list
  - [ ] Checksums generated (optional)
- [ ] Git tag created
  ```bash
  git tag -a v{VERSION} -m "Release v{VERSION}: {TITLE}"
  git push origin v{VERSION}
  ```
- [ ] Release bundle created (optional)
  ```bash
  python3 scripts/create-release-bundle.py {VERSION}
  ```

### Post-Release (Deployment)

- [ ] Release notes published (GitHub releases, internal wiki)
- [ ] Deployment executed (see OPERATIONS.md)
- [ ] Post-deployment verification
  - [ ] Health check passing
  - [ ] Application logs clean
  - [ ] Sample intake request successful
- [ ] Stakeholders notified
- [ ] Release retrospective scheduled (if major release)

### Release Approval (Production)

For production deployments, additional approvals may be required:

- [ ] Security review approval (Phase 7+ releases)
- [ ] Operations team approval (deployment readiness)
- [ ] Change Advisory Board approval (if applicable)
- [ ] Rollback plan documented and reviewed

---

## Release Artifacts

### 1. Git Tag

**Format:** `v{VERSION}` (e.g., `v0.7.3`)

**Creation:**
```bash
git tag -a v0.7.3 -m "Release v0.7.3: Phase 7 WS-4 - Release Governance"
git push origin v0.7.3
```

**Tag Message Format:**
```
Release v{VERSION}: {Phase/Workstream Title}

{One-paragraph summary}

See CHANGELOG.md for details.
```

### 2. Release Manifest

**File:** `releases/RELEASE-MANIFEST-{VERSION}.md`

**Purpose:** Auditable record of release contents and verification

**Retention:** Permanent (never delete)

### 3. Release Bundle (Optional)

**Purpose:** Self-contained deployment package

**Contents:**
- Source code snapshot
- CHANGELOG.md (full history)
- Release manifest
- Verification test results
- Dependencies list (requirements.txt)
- Deployment guide (OPERATIONS.md)

**Creation:**
```bash
python3 scripts/create-release-bundle.py 0.7.3
```

**Output:** `releases/qms-dashboard-0.7.3.tar.gz`

**Bundle Structure:**
```
qms-dashboard-0.7.3/
├── src/
│   └── backend/
│       ├── main.py
│       ├── config.py
│       ├── security.py
│       └── ...
├── CHANGELOG.md
├── OPERATIONS.md
├── RUNBOOK.md
├── RELEASE-MANIFEST-0.7.3.md
├── requirements.txt
└── INSTALL.md
```

### 4. File Integrity Checksums (Optional)

**Purpose:** Verify file integrity for audit/compliance

**Generation:**
```bash
# SHA-256 checksums for all source files
find src -type f -name "*.py" -exec sha256sum {} \; > releases/checksums-0.7.3.txt

# Checksum the manifest itself
sha256sum releases/RELEASE-MANIFEST-0.7.3.md >> releases/checksums-0.7.3.txt
```

**Verification:**
```bash
sha256sum -c releases/checksums-0.7.3.txt
```

---

## Rollback Procedures

### When to Rollback

Rollback is recommended if:
- Critical functionality broken in production
- Security vulnerability introduced
- Data corruption detected
- Unrecoverable errors in logs

**Severity Levels:**
- **P0 (Critical):** Immediate rollback, no approval needed
- **P1 (High):** Rollback within 1 hour, notify stakeholders
- **P2 (Medium):** Evaluate fix vs rollback, rollback within 4 hours
- **P3 (Low):** Fix forward, rollback not required

### Rollback Steps

**1. Identify Previous Version**
```bash
# List recent tags
git tag -l "v0.*" | tail -5

# Previous version: v0.7.2
```

**2. Stop Application**
```bash
# Production (systemd)
sudo systemctl stop qms-dashboard

# Development
# (Ctrl+C or kill process)
```

**3. Restore Code**
```bash
# Checkout previous version tag
git checkout v0.7.2

# Verify version
grep "## \[0.7.2\]" CHANGELOG.md
```

**4. Restore Data (if needed)**
```bash
# Only if data format changed between versions
# See RUNBOOK.md "Recovery: Full System Restore"
sudo tar -xzf /backup/qms-data-pre-0.7.3.tar.gz -C /var/lib/qms-dashboard/
```

**5. Restart Application**
```bash
# Production
sudo systemctl start qms-dashboard
sudo systemctl status qms-dashboard

# Verify health
curl http://localhost:8000/health
```

**6. Verify Rollback**
```bash
# Check version (if version endpoint exists)
curl http://localhost:8000/api/version

# Test basic functionality
curl http://localhost:8000/api/intakes
```

**7. Document Rollback**
- Update incident log (RUNBOOK.md procedures)
- Document root cause
- Schedule fix and re-release
- Notify stakeholders

**Estimated Rollback Time:** 5-15 minutes (code only), 15-30 minutes (with data restore)

---

## Verification Requirements

### Pre-Release Testing

**Minimum Test Suite:**
- Phase 6 regression tests: 6/6 passing
- Integration tests: All passing (if applicable)
- Manual verification: Basic workflow tested

**Test Execution:**
```bash
# Run Phase 6 regression tests
python3 tests/test_phase6_regression.py

# Expected output:
# Tests Passed: 6/6
# Tests Failed: 0/6
# ✅ ALL REGRESSION TESTS PASSED
```

**Test Result Documentation:**
- Record in release manifest
- Include test output in release notes
- Document any test failures and resolutions

### Security Verification

**Phase 7+ Releases:**
- Security utilities tests passing (11/11)
- No new OWASP Top 10 vulnerabilities introduced
- Advisory findings from previous phases addressed
- Path sanitization functional
- Request validation enforced

**Security Test Execution:**
```bash
# Run security utilities tests
python3 tests/test_security_utilities.py

# Expected output:
# ✅ 11/11 security tests passed
```

### Post-Deployment Verification

**Production Health Checks:**
```bash
# 1. Health endpoint
curl http://localhost:8000/health
# Expected: {"status": "healthy", ...}

# 2. Application logs
sudo journalctl -u qms-dashboard -n 50 --no-pager
# Expected: No errors

# 3. Data directory
ls $QMS_DATA_ROOT/intake-responses/*.json | wc -l
# Expected: Non-zero count

# 4. Sample intake request
curl -X POST http://localhost:8000/api/intake \
  -H "Content-Type: application/json" \
  -d @tests/sample-intake.json
# Expected: 200 OK with intake_id
```

---

## Compliance & Audit

### Audit Trail Requirements

**For Each Release, Document:**
1. **What Changed:** CHANGELOG.md entry
2. **Who Approved:** Release checklist signoff (if multi-person team)
3. **When Released:** Git tag timestamp + release manifest date
4. **Verification:** Test results in release manifest
5. **Deployment:** Deployment log (see OPERATIONS.md)

**Retention Policy:**
- Git tags: Permanent
- Release manifests: Permanent (never delete from `releases/` directory)
- CHANGELOG.md: Permanent (full history maintained)
- Test results: Retain for audit period (recommend 2+ years)

### Traceability

**Code Changes → Release → Deployment:**
```
Git Commit → Git Tag → Release Manifest → Deployment Log
    ↓            ↓             ↓                ↓
  SHA hash    v0.7.3    Test results      Timestamp
                        File list         Server ID
                        Checksums         Operator
```

**Example Trace:**
```bash
# 1. Find release tag
git tag -l "v0.7.3"

# 2. View tag details
git show v0.7.3

# 3. View release manifest
cat releases/RELEASE-MANIFEST-0.7.3.md

# 4. View deployment log (if maintained)
cat /var/log/qms-dashboard/deployments.log | grep "0.7.3"
```

### Compliance Standards

**QMS Dashboard Release Process Aligns With:**
- **ISO 9001:** Change control and document management
- **FDA 21 CFR Part 11:** Audit trails and electronic records (if applicable to usage domain)
- **SOC 2:** Change management and version control
- **Good Documentation Practices (GDP):** Traceable, attributable, contemporaneous

**Evidence for Auditors:**
- CHANGELOG.md (complete change history)
- `releases/` directory (release manifests)
- Git history (code change attribution)
- Test results (verification evidence)
- OPERATIONS.md + RUNBOOK.md (procedures)

---

## Release Scenarios

### Scenario 1: Normal Workstream Release

**Situation:** Completed Phase 7 WS-4 (Release Governance)

**Steps:**
1. Verify WS-4 deliverables complete (RELEASE-PROCESS.md, scripts)
2. Run Phase 6 regression tests → 6/6 passing
3. Update CHANGELOG.md with v0.7.3 entry
4. Generate release manifest: `python3 scripts/generate-release-manifest.py 0.7.3`
5. Commit changes: `git commit -m "chore: release v0.7.3"`
6. Create tag: `git tag -a v0.7.3 -m "Release v0.7.3: Phase 7 WS-4 - Release Governance"`
7. Push: `git push origin main --tags`
8. Deploy (if applicable): See OPERATIONS.md

**Estimated Time:** 30 minutes

### Scenario 2: Hotfix Release

**Situation:** Critical security vulnerability discovered in production

**Steps:**
1. Create hotfix branch: `git checkout -b hotfix/0.7.4 v0.7.3`
2. Implement fix with tests
3. Run regression tests → Verify passing
4. Update CHANGELOG.md with hotfix entry (mark as SECURITY)
5. Generate release manifest (expedited)
6. Commit and tag: `v0.7.4`
7. Deploy immediately (follow RUNBOOK.md emergency procedures)
8. Notify stakeholders
9. Merge hotfix to main branch

**Estimated Time:** 2-4 hours (expedited)

### Scenario 3: 1.0.0 Production Release

**Situation:** Phase 7 complete, ready for 1.0.0 production release

**Steps:**
1. Complete Phase 7 final verification sweep
2. Run full test suite (all phases)
3. Security review approval
4. Operations team deployment readiness review
5. Update CHANGELOG.md with v1.0.0 entry
6. Generate release manifest with full audit trail
7. Create release bundle: `python3 scripts/create-release-bundle.py 1.0.0`
8. Generate checksums for all files
9. Create annotated tag with detailed message
10. Change Advisory Board approval (if required)
11. Production deployment (with rollback plan)
12. Post-deployment verification (full test suite)
13. Announce release to stakeholders

**Estimated Time:** 1-2 days (including approvals)

---

## Tools & Automation

### Recommended Tooling

**Version Control:**
- Git tags for version tracking
- GitHub/GitLab releases for release notes
- Signed tags for security (optional): `git tag -s v0.7.3`

**Automation Scripts:**
- `scripts/generate-release-manifest.py` - Release manifest generation
- `scripts/create-release-bundle.py` - Deployment bundle creation
- `scripts/verify-release.sh` - Pre-release verification checks

**CI/CD Integration (Future):**
- Automated test runs on tag creation
- Automated release manifest generation
- Automated deployment to staging/production

### Future Enhancements

**Planned (Phase 8+):**
- Automated release notes generation from CHANGELOG
- Semantic versioning enforcement (pre-commit hook)
- Automated rollback triggers (health check failures)
- Release approval workflow (GitHub Actions)

---

## Summary

**Key Principles:**
1. **Semantic Versioning** - Predictable version numbers
2. **Comprehensive Documentation** - CHANGELOG + Release Manifest
3. **Verification Required** - All tests passing before release
4. **Audit Trail** - Complete traceability from code to deployment
5. **Rollback Ready** - Documented rollback procedures

**Release Artifacts:**
- Git tag (version marker)
- CHANGELOG.md entry (changes)
- Release manifest (verification + audit)
- Checksums (integrity, optional)

**For Every Release:**
- [ ] CHANGELOG updated
- [ ] Tests passing
- [ ] Release manifest generated
- [ ] Git tag created
- [ ] Deployment verified

---

**Document Owner:** QMS Dashboard Development Team
**Review Frequency:** Quarterly or after major process changes
**Next Review:** 2026-03-15

**Version History:**
- 1.0 (2025-12-15) - Initial release process definition (Phase 7 WS-4)
