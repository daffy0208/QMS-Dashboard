# Traceability Index
## QMS Dashboard Project

**Risk Level:** R2
**Date:** 2025-12-12
**Status:** First-pass (structure defined, content pending requirements phase)

---

## Purpose
Maintain bidirectional traceability between requirements, design, implementation, verification, and validation activities to ensure:
- All requirements are implemented
- All implementation has requirements justification
- All requirements are verified and validated
- Impact analysis possible for changes

---

## Traceability Matrix Structure

```
USER NEED
    ↓
REQUIREMENT (REQ-xxx)
    ↓
DESIGN (DES-xxx)
    ↓
IMPLEMENTATION (CODE-xxx)
    ↓
VERIFICATION (VER-xxx) ← Tests
    ↓
VALIDATION (VAL-xxx) ← User acceptance
```

---

## Traceability Links

### Format
- **Requirements:** REQ-001, REQ-002, etc.
- **CTQs:** CTQ-1.1, CTQ-2.1, etc. (already defined in CTQ Tree)
- **Design Elements:** DES-001, DES-002, etc.
- **Code Modules:** CODE-001, CODE-002, etc.
- **Verification Tests:** VER-001, VER-002, etc.
- **Validation Tests:** VAL-001, VAL-002, etc.
- **Risks:** R-001, R-002, etc. (already defined in Risk Register)
- **Assumptions:** A-001, A-002, etc. (already defined in Assumptions Register)

---

## Initial Traceability: CTQs to Requirements

*Note: Requirements not yet defined. This section will be populated during detailed planning phase.*

### Critical to Quality → Requirements (Placeholder)

| CTQ ID | CTQ Name | Related Requirements | Status |
|--------|----------|---------------------|--------|
| CTQ-1.1 | Risk Classification Accuracy | REQ-TBD | Pending |
| CTQ-1.2 | Artifact Set Correctness | REQ-TBD | Pending |
| CTQ-1.3 | Traceability Integrity | REQ-TBD | Pending |
| CTQ-2.1 | Mandatory Artifact Generation | REQ-TBD | Pending |
| CTQ-2.2 | No Silent Skipping | REQ-TBD | Pending |
| CTQ-2.3 | First-pass Content Quality | REQ-TBD | Pending |
| CTQ-3.1 | Intake Completion Time | REQ-TBD | Pending |
| CTQ-3.2 | Guidance Clarity | REQ-TBD | Pending |
| CTQ-3.3 | Artifact Actionability | REQ-TBD | Pending |
| CTQ-4.1 | Domain Alignment | REQ-TBD | Pending |
| CTQ-4.2 | Risk-appropriate Rigor | REQ-TBD | Pending |

---

## Requirements to Design/Implementation (Placeholder)

*To be populated during implementation phase*

| Requirement | Design | Implementation | Verification | Validation | Status |
|-------------|--------|----------------|--------------|------------|--------|
| REQ-TBD | DES-TBD | CODE-TBD | VER-TBD | VAL-TBD | Not Started |

---

## Risk to Mitigation Traceability

| Risk ID | Risk Name | Mitigation Requirements | Verification | Status |
|---------|-----------|------------------------|--------------|--------|
| R-001 | Incorrect risk classification | REQ-TBD (validation checks, examples) | VER-TBD | Open |
| R-002 | Invalid assumptions | REQ-TBD (assumption validation) | VER-TBD | Open |
| R-003 | Inadequate CTQ coverage | REQ-TBD (CTQ review process) | VER-TBD | Open |
| R-004 | Traceability breakdown | REQ-TBD (traceability tooling) | VER-TBD | Open |
| R-005 | Silent artifact skipping | REQ-TBD (status enforcement) | VER-TBD | Open |
| R-006 | Inadequate verification | REQ-TBD (verification methods) | VER-TBD | Open |
| R-007 | User misunderstanding | REQ-TBD (documentation, guidance) | VAL-TBD | Open |
| R-008 | Scope creep | REQ-TBD (change control) | N/A | Open |
| R-009 | Safety/legal downstream | REQ-TBD (accuracy, review, disclaimers) | VER-TBD, VAL-TBD | Open |
| R-010 | Technology limitations | REQ-TBD (format conventions) | VER-TBD | Open |

---

## Assumptions to Validation Traceability

| Assumption ID | Assumption | Validation Method | Validation Test | Status |
|---------------|------------|-------------------|-----------------|--------|
| A-001 | Intake questions sufficient | Pilot testing, expert review | VAL-TBD | Not Validated |
| A-002 | User domain knowledge | User testing | VAL-TBD | Not Validated |
| A-003 | Framework applicability | Expert review, multi-domain test | VAL-TBD | Not Validated |
| A-004 | Artifact templates adequate | User feedback | VAL-TBD | Not Validated |
| A-005 | Individual scale appropriate | Monitor usage | N/A | Validated (Monitor) |
| A-006 | Internal use only | Access control review | VER-TBD | Validated (Monitor) |
| A-007 | Easy reversibility | Incident response testing | VER-TBD | Validated (Monitor) |
| A-008 | No direct regulation | Legal review | N/A | Validated (Monitor) |
| A-009 | Recommendations not automated | Architecture review | VER-TBD | Validated (Monitor) |
| A-010 | Markdown format adequate | User feedback | VAL-TBD | Not Validated |

---

## Quality Artifacts to Requirements Traceability

| Artifact | Purpose | Requirements Traced | Status |
|----------|---------|-------------------|--------|
| Quality Plan | Overall quality strategy | All requirements | Draft |
| CTQ Tree | Define critical characteristics | CTQ-1.1 through CTQ-4.2 | First-pass |
| Assumptions Register | Document assumptions | A-001 through A-010 | First-pass |
| Risk Register | Identify and mitigate risks | R-001 through R-010 | First-pass |
| Traceability Index | Maintain linkages | CTQ-1.3 (Traceability Integrity) | First-pass |
| Verification Plan | Define testing strategy | All CTQs | Pending |
| Validation Plan | Define user acceptance | CTQ-3.x, CTQ-4.2 | Pending |
| Measurement Plan | Define metrics | All CTQs | Pending |
| Control Plan | Ongoing monitoring | CTQ-2.2, CTQ-4.2 | Pending |
| Change Log | Track changes | CTQ-1.3, R-004 | Structure defined |
| CAPA Log | Corrective/preventive actions | All risks, R-009 | Structure defined |

---

## Traceability Completeness Checklist

- [ ] All CTQs map to requirements
- [ ] All requirements map to design elements
- [ ] All design elements map to implementation
- [ ] All implementation has verification tests
- [ ] Critical CTQs have validation tests
- [ ] All risks have mitigation requirements
- [ ] Critical assumptions have validation tests
- [ ] All verification tests trace back to requirements
- [ ] All validation tests trace back to user needs/CTQs

---

## Orphan Detection

**Forward Orphans** (requirements with no implementation):
- To be checked during implementation phase

**Backward Orphans** (implementation with no requirements):
- To be checked during implementation phase

**Untested Requirements:**
- To be checked during verification phase

---

## Traceability Maintenance

### Update Triggers
- New requirement added → Create traceability links
- Requirement changed → Update downstream links
- Design changed → Update requirement and implementation links
- Test added/modified → Update verification/validation links
- Risk identified → Create mitigation requirement

### Review Frequency
- Before each quality gate
- At code review
- Before release

### Audit Schedule
- Full traceability audit before first release
- Spot checks during development
- Triggered audit if orphans suspected

---

## Tools and Conventions

**File Naming:**
- Requirements: `requirements.md` or `REQ-xxx` inline
- Tests: `test_*.py`, `*_test.js`, etc.
- Design: `design.md` or inline comments with DES-xxx

**Linking Convention:**
- Use explicit IDs in comments: `# Implements REQ-001, REQ-002`
- Use test names: `test_risk_classification_accuracy_CTQ_1_1()`
- Cross-reference in artifact files

**Traceability Report:**
- Generate before each milestone
- Include completeness metrics
- Highlight gaps and orphans
