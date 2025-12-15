# Phase 8A Scope Lock
## Teaching System Core (WS-1 through WS-4 Only)

**Date:** 2025-12-15
**Branch:** `phase-8a-teaching-core`
**Objective:** Build artifact validation, guidance, and simulation capabilities WITHOUT modifying intake schema or classification logic.

---

## ✅ IN SCOPE (Phase 8A)

### WS-1: Artifact Validation & Acceptance Criteria
- `acceptance_criteria.json` - R2/R3 only, 4 core artifacts
- `validator.py` - Placeholder detection, completeness checking
- Artifact health API endpoint
- Template markers (REQUIRED/OPTIONAL)

### WS-2: Dependency Management & Smart Next Steps
- `dependencies.json` - Artifact dependency graph
- `dependency_manager.py` - Next-action recommendations
- Project state tracking

### WS-3: Guidance Engine & Improvement Suggestions
- `expert_system.py` - Actionable suggestions
- Contextual help system
- Classification explanations

### WS-4: Simulation Mode & Dry-Run Review
- `QMS_MODE=sandbox|production` configuration
- `dry_run_reviewer.py` - Simulate expert review
- Sandbox API endpoints

---

## ❌ OUT OF SCOPE (Deferred to Phase 8B+)

### Explicitly Excluded from Phase 8A:
1. **NO new intake questions** (q8-q11 AI-specific questions deferred)
2. **NO lifecycle_stage field** (lifecycle tracking deferred)
3. **NO changes to classification logic** (classifier.py stays locked)
4. **NO AI-specific artifacts** (model_card, data_sheet, monitoring_plan deferred)
5. **NO lifecycle gating** (stage transitions deferred)
6. **NO schema changes to IntakeAnswers or IntakeRequest**

### WS-5: AI System-Specific Extensions → **DEFERRED**
- AI typology questions (q8-q11)
- Layer 7 AI safety validation
- AI-specific artifact templates
- AI guidance

### WS-6: Lifecycle State Model → **DEFERRED**
- Lifecycle stage tracking
- Stage-specific artifacts
- Stage transition gates
- Maturity-based validation

---

## 🔒 Non-Negotiable Constraints

### 1. No Intake Schema Modifications
**Rule:** `src/backend/models/intake.py` must NOT gain new fields in Phase 8A.

**Rationale:** Intake schema changes cascade through frontend, validation, storage, and expert review. Phase 8A focuses on artifact quality, not intake expansion.

**Enforcement:** Any PR modifying `IntakeAnswers` or `IntakeRequest` will be rejected.

### 2. No Classification Logic Changes
**Rule:** `src/backend/validation/classifier.py` stays deterministic and unchanged.

**Rationale:** Classification must remain auditable and deterministic. Teaching system adds guidance AFTER classification, not modifications TO classification.

**Enforcement:** `classify_risk()` function is read-only in Phase 8A.

### 3. No AI or Lifecycle Semantics
**Rule:** No code references to AI system types, lifecycle stages, or domain-specific logic.

**Rationale:** These are complex features requiring their own design cycles. Phase 8A builds the foundation that will support them later.

**Enforcement:** Code review blocks any AI-specific or lifecycle-specific logic.

---

## 📋 Acceptance Criteria for Phase 8A Completion

Phase 8A is complete when:

1. **WS-1 Complete:**
   - Acceptance criteria JSON covers R2/R3, 4 core artifacts
   - Validator detects placeholders and missing sections
   - Artifact health API returns completeness metrics
   - False positive rate <5%

2. **WS-2 Complete:**
   - Dependency graph defined for all 11 artifacts
   - Smart next-steps replace generic recommendations
   - Blocked artifacts prevented from generation

3. **WS-3 Complete:**
   - Guidance engine generates actionable suggestions
   - Contextual help explains requirements
   - Classification rationale explained in plain language

4. **WS-4 Complete:**
   - Sandbox mode isolates test data
   - Dry-run review predicts approval/override
   - Simulation accuracy ≥70% vs real reviews

5. **Regression:**
   - All Phase 1-7 tests pass (6/6 regression tests)
   - Existing intakes work without modification
   - Performance overhead <500ms

---

## 🚦 Build Order (Sequential)

1. **WS-1.1:** Acceptance criteria schema → COMMIT
2. **WS-1.2:** Validator skeleton → COMMIT
3. **WS-1.3:** Template markers → COMMIT
4. **WS-1.4:** Artifact health endpoint → COMMIT & TEST
5. **WS-2:** Dependency management → COMMIT & TEST
6. **WS-3:** Guidance engine → COMMIT & TEST
7. **WS-4:** Simulation mode → COMMIT & TEST
8. **Integration:** Full regression testing
9. **Merge:** phase-8a-teaching-core → main

---

## 📊 Success Metrics

**Before Phase 8A:**
- Artifact completeness before review: <50%
- Expert review approval rate: ~60%
- Time to review-ready: ~7 days

**After Phase 8A (Target):**
- Artifact completeness before review: ≥80%
- Expert review approval rate: ≥85%
- Time to review-ready: ≤3 days

---

## 🛡️ Audit Shield

**Purpose of This Document:**
- Prevents scope creep during implementation
- Provides clear boundaries for code review
- Documents what WAS and WAS NOT implemented
- Enables audit trail for Phase 8A decisions

**This document is the contract.**
Any deviation requires explicit approval and scope amendment.

---

**Scope Lock Status:** ✅ LOCKED
**Approval Date:** 2025-12-15
**Implementation Start:** 2025-12-15
