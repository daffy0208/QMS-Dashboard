# CTQ Tree (Critical to Quality)
## QMS Dashboard Project

**Risk Level:** R2
**Date:** 2025-12-12
**Status:** First-pass (requires expansion)

---

## CTQ Structure

```
                           QMS Dashboard Quality
                                    |
        ____________________________________________
        |                   |                      |
    Accuracy           Completeness            Usability
        |                   |                      |
```

---

## 1. Accuracy

**Definition:** System correctly classifies risk and generates appropriate artifacts

### CTQ-1.1: Risk Classification Accuracy
- **Requirement:** Risk level (R0-R3) must match intake responses per intake-rules.md:48-55
- **Measurement:** % of intake sessions producing correct risk classification
- **Target:** 100%
- **Priority:** Critical

### CTQ-1.2: Artifact Set Correctness
- **Requirement:** Generated artifact list must match requirements for risk level
- **Measurement:** % of sessions generating complete and correct artifact set
- **Target:** 100%
- **Priority:** Critical

### CTQ-1.3: Traceability Integrity
- **Requirement:** Requirements must trace to verification methods without breaks
- **Measurement:** % of requirements with valid traceability links
- **Target:** 100%
- **Priority:** High

---

## 2. Completeness

**Definition:** System generates all required artifacts and prevents silent skipping

### CTQ-2.1: Mandatory Artifact Generation
- **Requirement:** All artifacts required for risk level must be created
- **Measurement:** Count of missing artifacts per session
- **Target:** 0 missing artifacts
- **Priority:** Critical

### CTQ-2.2: No Silent Skipping
- **Requirement:** Every artifact must have explicit status (Done/Deferred/Deviated)
- **Measurement:** % of artifacts with undefined status
- **Target:** 0%
- **Priority:** Critical

### CTQ-2.3: First-pass Content Quality
- **Requirement:** Generated artifacts contain actionable first-pass content
- **Measurement:** % of artifacts requiring complete rewrite vs. refinement
- **Target:** <10% requiring complete rewrite
- **Priority:** Medium

---

## 3. Usability

**Definition:** Users can efficiently complete intake and understand quality requirements

### CTQ-3.1: Intake Completion Time
- **Requirement:** Users can complete 7-question intake in reasonable time
- **Measurement:** Average time to complete intake
- **Target:** <10 minutes
- **Priority:** Medium

### CTQ-3.2: Guidance Clarity
- **Requirement:** Users understand what quality activities are required and why
- **Measurement:** User comprehension rate (validation testing)
- **Target:** >90% comprehension
- **Priority:** High

### CTQ-3.3: Artifact Actionability
- **Requirement:** Generated artifacts provide clear next steps
- **Measurement:** % of users able to proceed without additional guidance
- **Target:** >80%
- **Priority:** Medium

---

## 4. Cross-cutting CTQs

### CTQ-4.1: Domain Alignment
- **Requirement:** System reflects current QMS best practices
- **Measurement:** Alignment with ISO 9001, IEC 62304, FDA QSR where applicable
- **Target:** No conflicts with applicable standards
- **Priority:** High
- **Note:** Domain partially understood per intake; requires validation

### CTQ-4.2: Risk-appropriate Rigor
- **Requirement:** Quality activities scale with risk (avoid over/under-engineering)
- **Measurement:** User feedback on appropriateness of generated plan
- **Target:** >85% agreement that rigor matches project needs
- **Priority:** High

---

## 5. CTQ Relationships and Dependencies

```
Risk Classification Accuracy (CTQ-1.1)
    ↓ enables
Artifact Set Correctness (CTQ-1.2)
    ↓ enables
Mandatory Artifact Generation (CTQ-2.1)
    ↓ supports
No Silent Skipping (CTQ-2.2)
```

**Key Dependency:** If risk classification is wrong, entire artifact set will be incorrect.

---

## 6. CTQ Priorities for V&V

**Must Verify:**
1. Risk classification logic (CTQ-1.1)
2. Artifact generation completeness (CTQ-2.1)
3. Status enforcement (CTQ-2.2)
4. Traceability links (CTQ-1.3)

**Must Validate:**
1. User comprehension (CTQ-3.2)
2. Artifact actionability (CTQ-3.3)
3. Risk-appropriate rigor (CTQ-4.2)

---

## 7. Next Steps

- [ ] Expand each CTQ with specific measurable limits (LSL/USL)
- [ ] Define verification methods for each CTQ
- [ ] Link CTQs to specific requirements (when requirements are written)
- [ ] Validate CTQs with intended users
- [ ] Add CTQs for performance, security if needed based on requirements
