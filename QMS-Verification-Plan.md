# Verification Plan
## QMS Dashboard Project

**Risk Level:** R2
**Date:** 2025-12-12
**Status:** First-pass

---

## Purpose
Define how to verify that the QMS Dashboard system meets its specifications and requirements. Verification answers: **"Did we build it right?"**

---

## Verification Strategy

### Approach
- **Test-driven where practical:** Write tests alongside or before implementation
- **Risk-based prioritization:** Focus verification on high-risk areas (R-001, R-006, R-009)
- **Automated regression:** Core functionality (risk classification, artifact generation) automated
- **Traceability:** Each CTQ and requirement has defined verification method

### Verification Methods

1. **Unit Testing:** Individual functions and modules
2. **Integration Testing:** Component interactions, artifact generation workflows
3. **System Testing:** End-to-end scenarios, full intake-to-artifacts flow
4. **Inspection/Review:** Code review, artifact template review, logic review
5. **Analysis:** Static analysis, traceability analysis, risk assessment review

---

## Verification Scope

### In Scope
- Risk classification logic (CTQ-1.1)
- Artifact set generation (CTQ-1.2, CTQ-2.1)
- Artifact status enforcement (CTQ-2.2)
- Traceability linkage (CTQ-1.3)
- First-pass content quality (CTQ-2.3)
- Input validation (intake questions)
- Rigor mode selection
- Deviation recording

### Out of Scope (Covered by Validation)
- User comprehension and usability (CTQ-3.2, CTQ-3.3)
- Real-world appropriateness of rigor (CTQ-4.2)
- User ability to complete intake efficiently (CTQ-3.1)

---

## CTQ-to-Verification Mapping

### CTQ-1.1: Risk Classification Accuracy
**Target:** 100% correct risk classification

**Verification Methods:**
- **VER-001-A:** Unit tests for risk classification logic
  - Test all combinations of intake responses
  - Verify R0/R1/R2/R3 boundary conditions
  - Test "if uncertain, select higher risk" rule
- **VER-001-B:** Inspection of risk classification rules against intake-rules.md:48-55
- **VER-001-C:** Test cases covering each risk level:
  - R0: Internal, low impact, fully reversible
  - R1: Internal, moderate impact, reversible
  - R2: Internal decision-impacting OR external users OR auditable
  - R3: Safety/legal/financial OR hard-to-reverse

**Pass Criteria:** All test cases pass, 100% coverage of risk classification paths

---

### CTQ-1.2: Artifact Set Correctness
**Target:** 100% correct artifact list for given risk level

**Verification Methods:**
- **VER-002-A:** Unit tests for artifact generation
  - R0 → 5 baseline artifacts
  - R1 → 8 artifacts (baseline + 3)
  - R2 → 11 artifacts (baseline + 3 + 3)
  - R3 → 11 artifacts (baseline + 3 + 3)
- **VER-002-B:** Integration test: full intake → verify generated file list
- **VER-002-C:** Inspection of artifact list against intake-rules.md:70-88

**Pass Criteria:** Correct artifact count and names for each risk level

---

### CTQ-1.3: Traceability Integrity
**Target:** 100% of requirements have valid traceability links

**Verification Methods:**
- **VER-003-A:** Traceability matrix completeness check (automated)
- **VER-003-B:** Manual audit of traceability links
- **VER-003-C:** Orphan detection (forward and backward)

**Pass Criteria:** No orphaned requirements or implementations, no broken links

---

### CTQ-2.1: Mandatory Artifact Generation
**Target:** 0 missing artifacts

**Verification Methods:**
- **VER-004-A:** System test: Run full intake, verify all required files created
- **VER-004-B:** File existence checks for each risk level
- **VER-004-C:** Content checks: Each artifact has non-empty first-pass content

**Pass Criteria:** All required artifacts present with valid content structure

---

### CTQ-2.2: No Silent Skipping
**Target:** 0% artifacts with undefined status

**Verification Methods:**
- **VER-005-A:** Status enforcement logic tests
  - Test Done/Deferred/Deviated transitions
  - Test that undefined status is rejected
- **VER-005-B:** Artifact status audit function
- **VER-005-C:** Integration test: Attempt to skip artifact without deviation → system rejects

**Pass Criteria:** System prevents silent skipping, requires explicit status

---

### CTQ-2.3: First-pass Content Quality
**Target:** <10% artifacts requiring complete rewrite

**Verification Methods:**
- **VER-006-A:** Inspection of generated artifact templates
- **VER-006-B:** Content structure validation (sections, tables present)
- **VER-006-C:** Spot check: Verify context-specific content vs. generic placeholders

**Pass Criteria:** Artifacts contain project-specific information, not just empty templates

*Note: Full assessment requires validation testing with users*

---

### CTQ-3.1: Intake Completion Time
**Target:** <10 minutes

**Verification Methods:**
- Covered by Validation Plan (user testing)

---

### CTQ-3.2: Guidance Clarity
**Target:** >90% comprehension

**Verification Methods:**
- Covered by Validation Plan (user testing)

---

### CTQ-3.3: Artifact Actionability
**Target:** >80% can proceed without guidance

**Verification Methods:**
- Covered by Validation Plan (user testing)

---

### CTQ-4.1: Domain Alignment
**Target:** No conflicts with applicable standards

**Verification Methods:**
- **VER-007-A:** Expert review of quality framework against ISO 9001, IEC 62304, FDA QSR
- **VER-007-B:** Comparison of intake questions and risk classification with industry practices

**Pass Criteria:** Framework aligns with recognized QMS standards, no contradictions

*Note: Requires subject matter expert involvement*

---

### CTQ-4.2: Risk-appropriate Rigor
**Target:** >85% agreement rigor matches needs

**Verification Methods:**
- **VER-008-A:** Review rigor mode mapping (R0→Advisory, R1→Conditional, R2→Strict, R3→Strict)
- Covered by Validation Plan (user feedback)

---

## Risk-based Verification Priorities

### Priority 1 (Critical - Must Test Before Release)
1. **R-009 Mitigation:** Safety/legal downstream impact
   - VER-001: Risk classification accuracy (prevent misclassification)
   - VER-002: Artifact set correctness (ensure right artifacts generated)
   - VER-004: Mandatory artifact generation (ensure no gaps)

2. **R-001 Mitigation:** Incorrect risk classification
   - VER-001: Comprehensive risk classification testing

3. **R-006 Mitigation:** Inadequate verification
   - All verification tests must be defined and passing

### Priority 2 (High - Test During Development)
4. **R-005 Mitigation:** Silent artifact skipping
   - VER-005: Status enforcement

5. **R-004 Mitigation:** Traceability breakdown
   - VER-003: Traceability integrity

6. **R-002 Mitigation:** Invalid assumptions
   - VER-007: Domain alignment (validates A-003)

### Priority 3 (Medium - Test Before Release)
7. **R-003 Mitigation:** Inadequate CTQ coverage
   - VER-006: First-pass content quality

8. **R-007 Mitigation:** User misunderstanding
   - VER-006: Artifact actionability (partial, rest in validation)

---

## Test Environment

### Setup Requirements
- Development environment with file system access
- Test fixtures: Sample intake responses for R0, R1, R2, R3 scenarios
- Expected outputs: Reference artifact sets for each risk level
- Markdown parser/validator for structure checks

### Test Data
- **Scenario 1 (R0):** Internal, low-impact, reversible, individual project
- **Scenario 2 (R1):** Internal, moderate impact, team project
- **Scenario 3 (R2):** Internal decision-impacting, multi-team (current project)
- **Scenario 4 (R3):** Safety-critical, external users, regulated

---

## Verification Test Cases (Summary)

| Test ID | CTQ | Method | Type | Priority | Status |
|---------|-----|--------|------|----------|--------|
| VER-001-A | CTQ-1.1 | Unit test - risk classification | Automated | P1 | Pending |
| VER-001-B | CTQ-1.1 | Inspection - risk rules | Manual | P1 | Pending |
| VER-001-C | CTQ-1.1 | Boundary test cases | Automated | P1 | Pending |
| VER-002-A | CTQ-1.2 | Unit test - artifact list | Automated | P1 | Pending |
| VER-002-B | CTQ-1.2 | Integration test - full flow | Automated | P1 | Pending |
| VER-002-C | CTQ-1.2 | Inspection - artifact rules | Manual | P1 | Pending |
| VER-003-A | CTQ-1.3 | Traceability matrix check | Automated | P2 | Pending |
| VER-003-B | CTQ-1.3 | Manual traceability audit | Manual | P2 | Pending |
| VER-003-C | CTQ-1.3 | Orphan detection | Automated | P2 | Pending |
| VER-004-A | CTQ-2.1 | System test - artifact generation | Automated | P1 | Pending |
| VER-004-B | CTQ-2.1 | File existence checks | Automated | P1 | Pending |
| VER-004-C | CTQ-2.1 | Content structure validation | Automated | P1 | Pending |
| VER-005-A | CTQ-2.2 | Status enforcement logic | Automated | P2 | Pending |
| VER-005-B | CTQ-2.2 | Artifact status audit | Automated | P2 | Pending |
| VER-005-C | CTQ-2.2 | Integration test - skip rejection | Automated | P2 | Pending |
| VER-006-A | CTQ-2.3 | Template inspection | Manual | P3 | Pending |
| VER-006-B | CTQ-2.3 | Structure validation | Automated | P3 | Pending |
| VER-006-C | CTQ-2.3 | Content specificity check | Manual | P3 | Pending |
| VER-007-A | CTQ-4.1 | Expert review - standards | Manual | P2 | Pending |
| VER-007-B | CTQ-4.1 | Industry practice comparison | Manual | P2 | Pending |
| VER-008-A | CTQ-4.2 | Rigor mapping review | Manual | P3 | Pending |

---

## Regression Testing Strategy

### Automated Regression Suite
- All VER-001 through VER-005 tests (Priority 1 and 2)
- Run on every code change
- Block merges if tests fail

### Manual Regression Checks
- VER-006, VER-007, VER-008 before each release
- Re-run if related code changed

---

## Verification Schedule

| Phase | Activities | Target Date | Status |
|-------|-----------|-------------|--------|
| Planning | Define verification tests (this document) | 2025-12-12 | ✅ Done |
| Setup | Create test environment, fixtures | TBD | Not Started |
| Unit Testing | VER-001, VER-002 | TBD | Not Started |
| Integration Testing | VER-002-B, VER-004-A, VER-005-C | TBD | Not Started |
| System Testing | End-to-end scenarios | TBD | Not Started |
| Inspection | VER-001-B, VER-002-C, VER-006-A, VER-007, VER-008 | TBD | Not Started |
| Traceability Audit | VER-003 | TBD | Not Started |
| Regression | Full test suite | TBD | Not Started |
| Verification Complete | All tests passing | TBD | Not Started |

---

## Pass/Fail Criteria

### Test Level
- **Pass:** Test meets defined pass criteria
- **Fail:** Test does not meet pass criteria → Defect logged, must fix before release

### Overall Verification
- **Pass:** All Priority 1 and Priority 2 tests passing
- **Conditional Pass:** Priority 1 passing, Priority 2 has minor issues with mitigation plan
- **Fail:** Any Priority 1 test failing OR significant gaps in test coverage

---

## Defect Management

- Defects logged with severity: Critical / Major / Minor
- Critical defects (related to R-009, R-001, R-006) block release
- Major defects require risk assessment and mitigation plan
- Minor defects can be deferred with justification

---

## Verification Sign-off

Verification complete when:
- [ ] All Priority 1 verification tests defined and passing
- [ ] All Priority 2 verification tests defined and passing
- [ ] Critical risks (R-001, R-006, R-009) have verified mitigations
- [ ] Traceability audit complete with no critical gaps
- [ ] Regression suite established and passing

**Verified by:** _________________
**Date:** _________________
**Signature:** _________________
