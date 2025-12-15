# Assumptions Register
## QMS Dashboard Project

**Risk Level:** R2
**Date:** 2025-12-12
**Status:** First-pass

---

## Purpose
Document key assumptions that, if proven false, would require significant changes to the quality plan or system design.

---

## Assumptions

### A-001: Intake Questions Sufficient
**Assumption:** The 7 mandatory intake questions are sufficient to classify project risk accurately.

**Impact if False:** Risk misclassification could lead to under-engineering (missing critical quality activities) or over-engineering (wasted effort).

**Validation Method:**
- Pilot testing with 5-10 diverse projects
- Expert review by quality professionals
- Post-deployment analysis of risk classification accuracy

**Validation Status:** ✅ Validated (2025-12-12)
**Validation Evidence:** VAL-002 testing with 10 diverse users (web, ML, medical, DevOps, security, fintech) achieved 100% correct classification. All users correctly understood their risk level and could explain classification drivers.
**Priority:** Critical
**Owner:** Project Owner

---

### A-002: User Domain Knowledge
**Assumption:** Users can accurately answer intake questions about their own projects (failure modes, reversibility, scale, etc.).

**Impact if False:** Garbage-in-garbage-out: System produces correct artifacts for incorrect inputs, leading to inappropriate quality plans.

**Validation Method:**
- User testing with realistic project scenarios
- Compare user answers against expert assessment
- Provide guidance/examples in intake questions

**Validation Status:** ✅ Validated with caveat (2025-12-12)
**Validation Evidence:** VAL-002 testing showed users accurately assessed their projects when provided clear examples and guidance. Users with "Partially" understood domains (Aisha, Carlos, Elena) still classified correctly. Caveat: Accuracy depends on quality of examples and guidance—without them, accuracy might decrease.
**Priority:** High
**Owner:** Project Owner

---

### A-003: QMS Framework Applicability
**Assumption:** This risk-based QMS framework applies across diverse project types (web apps, embedded systems, data science, etc.).

**Impact if False:** Framework may work for some project types but fail for others, requiring specialized variants.

**Validation Method:**
- Test framework against different project archetypes
- Industry expert review
- Comparison with domain-specific standards (e.g., IEC 62304 for medical devices)

**Validation Status:** ❓ Not yet validated
**Priority:** High
**Owner:** Project Owner
**Note:** Intake response indicates domain "partially understood"

---

### A-004: Artifact Templates Adequate
**Assumption:** The generated first-pass artifact content provides useful starting point (not just empty templates).

**Impact if False:** Users must start from scratch anyway, reducing value of automated generation.

**Validation Method:**
- User feedback on first-pass content quality
- Measure % of generated content retained vs. rewritten
- Compare time-to-complete with/without generated content

**Validation Status:** ❓ Not yet validated
**Priority:** Medium
**Owner:** Project Owner

---

### A-005: Individual Scale Appropriate
**Assumption:** System is designed for individual use and doesn't need multi-user collaboration features.

**Impact if False:** Scalability issues if multiple users need to collaborate on quality artifacts simultaneously.

**Validation Method:**
- Monitor actual usage patterns
- User requests for collaboration features
- Evaluate if scale assumption changes

**Validation Status:** ✅ Validated by intake (Individual scale selected)
**Priority:** Low
**Owner:** Project Owner
**Monitor:** If scale increases to Team or Multi-team, re-evaluate architecture

---

### A-006: Internal Use Only
**Assumption:** System will only be used internally and doesn't require external-facing security, privacy, or data protection measures.

**Impact if False:** Security vulnerabilities, privacy violations, or compliance issues if exposed externally.

**Validation Method:**
- Access control review
- Monitor deployment environment
- Confirm usage remains internal

**Validation Status:** ✅ Validated by intake (Internal users selected)
**Priority:** Medium
**Owner:** Project Owner
**Monitor:** Alert if deployment plans change to external access

---

### A-007: Easy Reversibility
**Assumption:** Failures in QMS Dashboard (incorrect guidance, missing artifacts) can be easily detected and corrected before causing downstream harm.

**Impact if False:** Incorrect quality guidance could propagate through project lifecycle undetected, leading to safety/legal/compliance failures.

**Validation Method:**
- Review change control process
- Test artifact correction workflow
- Measure time-to-detect and time-to-correct errors

**Validation Status:** ✅ Validated by intake (Easy reversibility selected)
**Priority:** High
**Owner:** Project Owner
**Monitor:** Track actual incident response times

---

### A-008: No Direct Regulation
**Assumption:** QMS Dashboard itself is not subject to regulatory oversight or formal audits.

**Impact if False:** Would require significant additional compliance documentation, validation evidence, design controls.

**Validation Method:**
- Legal/compliance review
- Confirm regulatory status
- Monitor regulatory landscape changes

**Validation Status:** ✅ Validated by intake (Not regulated selected)
**Priority:** Medium
**Owner:** Project Owner
**Monitor:** If system is used for regulated projects, may inherit regulatory requirements

---

### A-009: Recommendations vs. Automated Actions
**Assumption:** System provides recommendations that humans review and approve, rather than taking automated actions.

**Impact if False:** If system automatically generates and applies quality artifacts without human review, risk level may increase.

**Validation Method:**
- Architecture review
- Confirm human-in-the-loop for all critical decisions
- Test approval workflow

**Validation Status:** ✅ Validated by intake (Recommendations selected)
**Priority:** High
**Owner:** Project Owner
**Monitor:** Ensure automated artifact application not added without risk re-assessment

---

### A-010: Markdown Format Adequate
**Assumption:** Markdown files are sufficient for QMS artifact storage and management.

**Impact if False:** May need database, version control integration, or structured format for traceability and reporting.

**Validation Method:**
- User feedback on artifact format
- Evaluate traceability maintenance effort
- Test artifact linking and reporting

**Validation Status:** ❓ Not yet validated
**Priority:** Low
**Owner:** Project Owner

---

## Assumption Summary

| ID | Assumption | Priority | Validation Status | Action Required |
|----|------------|----------|-------------------|-----------------|
| A-001 | Intake questions sufficient | Critical | ✅ Validated | VAL-002 complete |
| A-002 | User domain knowledge | High | ✅ Validated (caveat) | VAL-002 complete |
| A-003 | Framework applicability | High | ❓ Not validated | Expert review |
| A-004 | Artifact templates adequate | Medium | ❓ Not validated | User feedback |
| A-005 | Individual scale appropriate | Low | ✅ Validated | Monitor |
| A-006 | Internal use only | Medium | ✅ Validated | Monitor |
| A-007 | Easy reversibility | High | ✅ Validated | Monitor |
| A-008 | No direct regulation | Medium | ✅ Validated | Monitor |
| A-009 | Recommendations not automated | High | ✅ Validated | Monitor |
| A-010 | Markdown format adequate | Low | ❓ Not validated | User feedback |

---

## Review Schedule

- **Initial Review:** Before implementation begins (today)
- **Ongoing Review:** At each quality gate / milestone
- **Triggered Review:** When assumption validation status changes
- **Full Re-validation:** If risk classification changes or major scope change occurs
