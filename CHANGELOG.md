# Changelog
## QMS Dashboard

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Phase 7 - Deployment & Operational Hardening

---

## [0.7.3] - 2025-12-15

### Phase 7 WS-4: Release Governance

**Objective:** Establish formal release process suitable for audit scrutiny.

#### Added

- **RELEASE-PROCESS.md** - Comprehensive release governance documentation
  - Semantic versioning strategy (SemVer 2.0.0)
  - Release types (Phase, Workstream, Hotfix, Maintenance)
  - Release preparation procedures
  - Release manifest format and generation
  - Change log requirements and enforcement
  - Complete release checklist (pre-release, release, post-release)
  - Release artifacts (Git tags, manifests, bundles, checksums)
  - Rollback procedures with severity levels (P0-P3)
  - Verification requirements (testing, security, post-deployment)
  - Compliance and audit trail documentation
  - Release scenarios (normal, hotfix, 1.0.0 production)

#### Release Process Components

**Versioning:**
- ✅ Semantic versioning rules defined (MAJOR.MINOR.PATCH)
- ✅ Pre-1.0 versioning documented (0.x.x current state)
- ✅ Post-1.0 breaking change policy established
- ✅ Version increment procedures

**Release Types:**
- ✅ Phase releases (MINOR version)
- ✅ Workstream releases (PATCH version)
- ✅ Hotfix releases (expedited PATCH)
- ✅ Maintenance releases (routine PATCH)

**Release Checklist:**
- ✅ Pre-release verification (code, tests, documentation)
- ✅ Release creation (manifest, tags, bundles)
- ✅ Post-release verification (deployment, health checks)
- ✅ Production approval gates (security, operations, CAB)

**Release Manifest:**
- ✅ Manifest format defined (standardized structure)
- ✅ Generation script outline (`scripts/generate-release-manifest.py`)
- ✅ Contents: changes, verification, breaking changes, file list
- ✅ Optional file integrity checksums (SHA-256)

**Rollback Procedures:**
- ✅ Rollback triggers defined (P0-P3 severity)
- ✅ Step-by-step rollback procedures
- ✅ Code restoration (git checkout tag)
- ✅ Data restoration (if format changed)
- ✅ Verification and documentation steps
- ✅ Estimated rollback time: 5-30 minutes

**Compliance:**
- ✅ Audit trail requirements (what, who, when, verification)
- ✅ Traceability (commit → tag → manifest → deployment)
- ✅ Retention policy (permanent tags and manifests)
- ✅ Standards alignment (ISO 9001, SOC 2, GDP)

#### Verification

- **Phase 6 Regression Tests:** ✅ 6/6 passing (no code changes in WS-4)
- **Documentation Review:** ✅ Complete release governance coverage
- **Process Readiness:** ✅ Ready for formal version releases

#### Breaking Changes

**None** - WS-4 is documentation-only.

**Release Process Benefits:**
- Formal version control with semantic versioning
- Complete audit trail for compliance
- Repeatable release procedures
- Documented rollback capability
- Evidence for quality management audits

---

## [0.7.2] - 2025-12-15

### Phase 7 WS-3: Operational Readiness Documentation

**Objective:** Make the system operable by operators who didn't build it.

#### Added

- **OPERATIONS.md** - Comprehensive day-to-day operations guide
  - System overview and architecture
  - Data directory structure documentation
  - Startup and shutdown procedures
  - Health checks and monitoring
  - Common operations (view intakes, reviews, statistics)
  - Log file locations and analysis
  - Backup procedures (3 methods: simple copy, rsync, cloud)
  - Maintenance window procedures
  - Quick reference commands

- **RUNBOOK.md** - Troubleshooting and incident response guide
  - Quick incident response checklist
  - Common issues with solutions (10+ scenarios)
  - Error messages reference (configuration, application, runtime)
  - Failure scenarios ("what happens if X fails")
    - Complete system failure
    - Data directory corruption
    - Disk full
    - Configuration error after update
  - Recovery procedures (full system restore, single intake restore, regenerate artifacts)
  - Debug procedures
  - Data recovery techniques
  - Performance troubleshooting
  - Security incident response
  - Escalation procedures

#### Documentation Coverage

**OPERATIONS.md (500+ lines):**
- Prerequisites and system requirements
- Standard data directory layout
- Pre-startup checklist
- Development, production (systemd), and verification modes
- Health endpoint validation
- Monitoring setup (basic, Prometheus, log analysis)
- Alert thresholds
- Disk space management
- Maintenance procedures

**RUNBOOK.md (600+ lines):**
- 5 common issues with detailed solutions
- 15+ error messages with fixes
- 4 detailed failure scenarios
- 3 recovery procedures with time estimates
- Debug procedures (enable logging, trace requests, inspect data)
- Performance issue diagnosis
- Security incident response

#### Operational Improvements

**Startup:**
- ✅ Pre-startup checklist (6 items)
- ✅ Verification procedures (health, logs, data directory)
- ✅ Startup issue troubleshooting (3 common causes)

**Monitoring:**
- ✅ Health check automation (cron, systemd timer)
- ✅ Key metrics defined (request rate, response time, error rate)
- ✅ Alert thresholds (critical and warning levels)

**Backup:**
- ✅ Three backup methods documented
  - Simple copy (development)
  - rsync with snapshots (production)
  - Cloud backup (AWS S3 example)
- ✅ Backup verification procedures
- ✅ Restore procedures with time estimates

**Troubleshooting:**
- ✅ Quick incident response (< 5 minutes)
- ✅ Common issues solved (10+ scenarios)
- ✅ Error message reference (20+ errors)
- ✅ Failure recovery documented

#### Verification

- **Phase 6 Regression Tests:** ✅ 6/6 passing (no code changes in WS-3)
- **Documentation Review:** ✅ Complete operational coverage
- **Procedures Tested:** ✅ Backup/restore verified

#### Breaking Changes

**None** - WS-3 is documentation-only.

**Operator Benefits:**
- Complete startup-to-shutdown procedures
- Troubleshooting guides for all common issues
- Recovery procedures with time estimates
- No tribal knowledge required

---

## [0.7.1] - 2025-12-15

### Phase 7 WS-2: Security & Access Controls

**Objective:** Reduce deployment risk with hardened request handling and path sanitization.

#### Added

- **Security Utilities Module** (`src/backend/security.py`)
  - `sanitize_project_name()` - Prevents path traversal in filenames
  - `sanitize_artifact_name()` - Safe artifact filename generation
  - `validate_intake_id()` - UUID format validation
  - `validate_review_id()` - Review ID format validation
  - `safe_path_join()` - Path traversal prevention
  - `validate_file_extension()` - Extension whitelist validation
  - `validate_json_depth()` - Prevents stack overflow attacks

- **Request Validation Middleware** (`main.py`)
  - Request size limits (10 MB maximum)
  - Content-type enforcement (whitelist)
  - Automatic validation on all requests

- **Documentation**
  - `doc/SECURITY-UPDATES-PHASE7-WS2.md` - Comprehensive security enhancements guide

#### Changed

- **artifacts/generator.py** - Uses path sanitization
  - `_write_artifact_file()` - Sanitizes artifact names
  - `_create_zip_archive()` - Sanitizes project names

- **main.py** - Enhanced endpoint security
  - All intake_id endpoints validate ID format
  - All review_id endpoints validate ID format
  - Request size and content-type validation middleware

#### Security Improvements

**Path Traversal Prevention:**
- Input: `"../../etc/passwd"` → Output: `"etc-passwd"`
- Input: `"Test<>Project"` → Output: `"Test-Project"`
- All filesystem operations use sanitized names

**Request Validation:**
- Maximum request size: 10 MB (prevents DoS)
- Content-type whitelist: JSON, multipart, form-urlencoded
- ID format validation: Prevents injection attacks

**Attack Surface Reduction:**
- ✅ Path traversal blocked
- ✅ Request size DoS mitigated
- ✅ Content-type abuse prevented
- ✅ ID injection blocked

#### Phase 6 Advisory Findings Addressed

- ⚠️ **Path Sanitization** (Medium) → ✅ **RESOLVED**
  - Project names sanitized in all file operations
  - Path traversal attempts blocked

- ⚠️ **Request Validation** (Medium) → ✅ **IMPLEMENTED**
  - Size limits enforced
  - Content-type validation
  - ID format validation

#### Verification

- **Phase 6 Regression Tests:** ✅ 6/6 passing (no behavior changes)
- **Security Utilities Tests:** ✅ 11/11 passing
- **Integration Tests:** ✅ 6/6 passing

#### Breaking Changes

**None** - Phase 7 WS-2 is fully backward compatible.

**Security Enhancement Notes:**
- Malformed IDs now return 400 Bad Request (previously 404 Not Found)
- Oversized requests return 413 Payload Too Large (previously processed)
- Invalid content-types return 415 Unsupported Media Type (previously processed)

---

## [0.7.0] - 2025-12-15

### Phase 7 WS-1: Runtime & Environment Hardening

**Objective:** Prepare for controlled, repeatable deployment with environment-aware configuration.

#### Added

- **Centralized Configuration Module** (`src/backend/config.py`)
  - Environment-aware configuration system
  - Support for `development`, `verification`, and `production` environments
  - Fail-fast validation for production deployments
  - Comprehensive startup validation

- **Environment Variables**
  - `QMS_ENV` - Environment name (development|verification|production)
  - `QMS_DATA_ROOT` - Absolute path to data root directory
  - `QMS_LOG_LEVEL` - Logging verbosity (DEBUG|INFO|WARNING|ERROR)
  - `QMS_HOST` - Server bind address (default: 0.0.0.0)
  - `QMS_PORT` - Server port (default: 8000)
  - `QMS_CORS_ORIGINS` - Comma-separated allowed CORS origins

- **Documentation**
  - `doc/runtime-config.md` - Complete runtime configuration guide
  - Environment setup examples (development, verification, production)
  - Troubleshooting guide
  - Migration guide from Phase 6

#### Changed

- **main.py** - Uses centralized configuration
  - Startup configuration validation (fail-fast on invalid config)
  - CORS origins loaded from environment
  - Server settings (host, port, reload) from environment
  - Data directory from centralized config

- **review/storage.py** - Uses centralized configuration
  - Data directory from config (with backward compatibility)
  - Singleton pattern updated for config integration

- **artifacts/generator.py** - Uses centralized configuration
  - Default artifact paths from config
  - Backward compatible with explicit output_dir parameter

#### Technical Details

**Filesystem Boundaries:**
- All writes confined to `QMS_DATA_ROOT`
- No writes outside configured data directory
- Configurable data root with validation

**CORS Policy Enforcement:**
- Development: Wildcard allowed (default)
- Production: Must explicitly specify allowed origins
- No wildcard CORS in production mode

**Configuration Validation:**
- Production requires explicit `QMS_DATA_ROOT`
- Production requires explicit `QMS_CORS_ORIGINS`
- Data directory writability check on startup
- Port number validation (1-65535)

#### Verification

- **Phase 6 Regression Tests:** ✅ 6/6 passing (no behavior changes)
- **Backward Compatibility:** ✅ Existing deployments continue to work
- **Default Behavior:** ✅ Development mode works without environment variables

#### Breaking Changes

**None** - Phase 7 WS-1 is fully backward compatible.

**Optional Migration (Production):**
- Set `QMS_ENV=production` for production deployments
- Set `QMS_DATA_ROOT` explicitly for production (no defaults)
- Configure `QMS_CORS_ORIGINS` for production (no wildcards)

---

## [0.6.0] - 2025-12-15

### Phase 6: Verification & Testing

**Objective:** Establish verified baseline for Phase 7 development.

#### Added

- **Verification Test Suites**
  - VER-001: Risk Classification (15 tests)
  - VER-002: Artifact Generation (4 tests)
  - VER-003: Traceability Matrix (3 tests)
  - VER-004: System Files (12 tests)
  - Integration Tests (6 tests)
  - Regression Tests (6 tests)
  - **Total:** 46 tests, 100% pass rate

- **Documentation**
  - `PHASE-6-VERIFICATION-REPORT.md` - Comprehensive verification report
  - `SECURITY-PRIVACY-REVIEW-PHASE6.md` - Security analysis
  - VER-GAP-P5-INTAKE-WRITEBACK documented as expected behavior

- **Security Review**
  - PII minimization verified
  - Input validation verified
  - Audit log design verified
  - Advisory findings documented for Phase 7+

#### Changed

- **Phase 5 v1 Scope Verification**
  - Confirmed no SLA tracking (v2+ feature)
  - Confirmed no metrics system (v2+ feature)
  - Confirmed no reviewer assignment (v2+ feature)

#### Verification Results

- **All Tests:** ✅ 46/46 passing
- **Security:** ✅ No blocking issues
- **Phase 7 Ready:** ✅ Approved to proceed

---

## [0.5.0] - 2025-12-15

### Phase 5 v1: Expert Review Recording

**Objective:** Record expert review decisions (not a workflow engine).

#### Added

- **Review Request Creation** (`POST /api/review-request/{intake_id}`)
  - Create expert review request from intake
  - Capture review triggers and user comments
  - Store review requests in `data/reviews/`

- **Expert Approval** (`POST /api/review/{review_id}/approve`)
  - Expert approves calculated classification
  - Records expert decision in review response
  - Appends entry to Expert-Review-Log.md

- **Expert Override** (`POST /api/review/{review_id}/override`)
  - Expert overrides calculated classification
  - Requires justification for all overrides
  - Documents risks accepted for downgrades
  - Records intake discrepancies identified

- **Review Storage** (`src/backend/review/storage.py`)
  - File-based storage for review requests/responses
  - JSON format for review data
  - Append-only Expert-Review-Log.md

- **Review Models** (`src/backend/models/review.py`)
  - ReviewRequest - Structured review request
  - ReviewResponse - Expert decision record
  - ReviewLog - Audit log entry
  - ReviewTrigger - Reason for review
  - IntakeDiscrepancy - Intake issues identified

#### Changed

- **Phase 5 v1 Scope** (Recorded Decision System)
  - ✅ Review recording functional
  - ❌ No SLA tracking (v2+)
  - ❌ No metrics dashboard (v2+)
  - ❌ No reviewer assignment (v2+)
  - ❌ No queue management (v2+)
  - ❌ No request-for-info workflow (v2+)

#### Known Limitations

- **VER-GAP-P5-INTAKE-WRITEBACK**
  - Intake files remain unchanged after expert review
  - Expert decisions stored separately in reviews/
  - Planned resolution in Phase 5 v2+

---

## [0.4.0] - 2025-12-15

### Phase 4: Artifact Generation

**Objective:** Generate QMS artifacts based on risk classification.

#### Added

- **Artifact Generator** (`src/backend/artifacts/generator.py`)
  - Generates 5/8/11 artifacts based on risk level (R0/R1/R2-R3)
  - Context-aware content (not empty templates)
  - Markdown format with QMS-* naming convention
  - ZIP archive creation

- **Artifact Templates** (`src/backend/artifacts/templates/`)
  - Quality Plan, CTQ Tree, Assumptions Register, Risk Register, Traceability Index (R0 base)
  - Verification Plan, Validation Plan, Measurement Plan (R1 additional)
  - Control Plan, Change Log, CAPA Log (R2/R3 additional)

- **API Endpoint** (`POST /api/intake/{intake_id}/generate-artifacts`)
  - Generate artifacts for existing intake
  - Returns file paths and ZIP location
  - Stores artifacts in `data/artifacts/{intake_id}/`

#### Artifact Counts

- **R0 (Minimal):** 5 artifacts
- **R1 (Moderate):** 8 artifacts
- **R2/R3 (Strict/Maximum):** 11 artifacts

---

## [0.3.0] - 2025-12-15

### Phase 3: Multi-Layer Validation

**Objective:** Comprehensive validation across 6 layers.

#### Added

- **Layer 2: Cross-Validation** (`src/backend/validation/layer2.py`)
  - Detects contradictions between answers
  - Flags unlikely combinations
  - Sanity checks for consistency

- **Layer 3: Risk Indicators** (`src/backend/validation/layer3.py`)
  - Pattern matching for high-risk scenarios
  - Domain-specific risk factors
  - Scale and impact analysis

- **Layer 4: Confirmation Warnings** (`src/backend/validation/layer4.py`)
  - Generates user acknowledgment requirements
  - Context-specific warnings
  - Risk communication

- **Layer 5: Expert Review Triggers** (`src/backend/validation/layer5.py`)
  - Determines when expert review is required/recommended
  - Multiple trigger conditions
  - Confidence-based escalation

---

## [0.2.0] - 2025-12-15

### Phase 2: Risk Classification

**Objective:** Automated risk level calculation (R0-R3).

#### Added

- **Classification Engine** (`src/backend/validation/classifier.py`)
  - Deterministic risk classification algorithm
  - Four risk levels: R0 (Minimal), R1 (Moderate), R2 (Strict), R3 (Maximum)
  - Borderline detection for boundary cases
  - Classification rationale generation

- **Risk Levels**
  - **R0:** Internal, informational, low impact
  - **R1:** Internal recommendations, team-scale
  - **R2:** High stakes, potential financial/legal impact
  - **R3:** External automated decisions, safety-critical

---

## [0.1.0] - 2025-12-15

### Phase 1: Core Intake System

**Objective:** Capture project characteristics through 7 questions.

#### Added

- **FastAPI Application** (`src/backend/main.py`)
  - REST API for quality intake
  - Health check endpoint
  - CORS middleware for development

- **Intake Models** (`src/backend/models/intake.py`)
  - IntakeRequest - 7 mandatory questions
  - IntakeResponse - Classification result with warnings
  - Pydantic validation with strict types

- **Layer 1 Validation** (`src/backend/validation/layer1.py`)
  - Input validation
  - Project name validation
  - Sanity checks

- **API Endpoints**
  - `POST /api/intake` - Submit intake request
  - `GET /api/intake/{intake_id}` - Retrieve intake
  - `GET /api/intakes` - List all intakes

- **Data Storage**
  - File-based JSON storage
  - Intake responses in `data/intake-responses/`

#### The 7 Questions

1. Who are the users? (Internal/External/Public)
2. How does the system influence decisions? (Informational/Recommendations/Automated)
3. What's the worst realistic failure? (Annoyance/Financial/Safety-Legal/Reputational)
4. How easily can failures be reversed? (Easy/Partial/Hard)
5. Do you understand the domain? (Yes/Partially/No)
6. What's the scale of impact? (Individual/Team/Multi-team/Organization-Public)
7. Is this regulated? (No/Possibly/Yes)

---

## Version History

- **0.7.0** - Phase 7 WS-1: Runtime & Environment Hardening
- **0.6.0** - Phase 6: Verification & Testing Baseline
- **0.5.0** - Phase 5 v1: Expert Review Recording
- **0.4.0** - Phase 4: Artifact Generation
- **0.3.0** - Phase 3: Multi-Layer Validation
- **0.2.0** - Phase 2: Risk Classification
- **0.1.0** - Phase 1: Core Intake System

---

**Changelog Format:** [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
**Versioning:** [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
