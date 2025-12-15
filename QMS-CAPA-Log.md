# CAPA Log (Corrective and Preventive Actions)
## QMS Dashboard Project

**Risk Level:** R2
**Date:** 2025-12-12
**Status:** Structure defined (no CAPA entries yet)

---

## Purpose
Track Corrective and Preventive Actions (CAPA) to address quality issues, non-conformances, risks, and opportunities for improvement. Required for R2+ projects per intake-rules.md:85-87.

---

## CAPA Process Overview

### Corrective Action (CA)
**Purpose:** Fix problems that have already occurred
**Trigger:** Defect, incident, non-conformance, audit finding, quality issue

**Process:**
1. Identify problem (what went wrong?)
2. Root cause analysis (why did it happen?)
3. Define corrective action (how to fix it?)
4. Implement action
5. Verify effectiveness (is problem resolved?)

### Preventive Action (PA)
**Purpose:** Prevent potential problems before they occur
**Trigger:** Risk identification, trend analysis, near-miss, process improvement opportunity

**Process:**
1. Identify potential problem (what could go wrong?)
2. Analyze likelihood and impact
3. Define preventive action (how to prevent it?)
4. Implement action
5. Monitor effectiveness (is prevention working?)

---

## CAPA Entry Structure

Each CAPA entry includes:
- **CAPA ID:** Unique identifier (CAPA-001, CAPA-002, etc.)
- **Date Opened:** When CAPA initiated
- **Type:** Corrective / Preventive / Both
- **Trigger:** What caused this CAPA (defect, risk, audit finding, etc.)
- **Problem Description:** What happened or could happen
- **Root Cause:** Why it happened or could happen (5 Whys analysis)
- **Impact:** Severity (Critical / Major / Minor), CTQs affected, risks related
- **Action Plan:** Specific steps to resolve (CA) or prevent (PA)
- **Owner:** Who is responsible for implementation
- **Target Date:** When action should be complete
- **Status:** Open / In Progress / Implemented / Verified / Closed
- **Verification:** How effectiveness was verified
- **Date Closed:** When CAPA completed and verified
- **Related Items:** Links to risks (R-XXX), changes (CHG-XXX), defects, requirements

---

## CAPA Severity Levels

**Critical:**
- Safety/legal/compliance impact (aligns with R-009 worst case)
- System producing incorrect risk classifications
- Silent artifact skipping not enforced
- Traceability completely broken

**Major:**
- CTQ not met (accuracy, completeness issues)
- Significant usability problem preventing users from proceeding
- Assumption invalidated requiring quality plan revision
- High-priority risk mitigation failed

**Minor:**
- Template quality issues
- Documentation gaps
- Process inefficiency
- Low-priority usability improvement

---

## CAPA Entries

*No CAPA entries yet. This section will be populated when issues are identified or preventive actions needed.*

---

## CAPA Entry Template

```
### CAPA-XXX: [Issue Title]
**Date Opened:** YYYY-MM-DD
**Type:** [Corrective / Preventive / Both]
**Severity:** [Critical / Major / Minor]

**Trigger:** [Defect ID, Risk ID, Audit finding, User feedback, etc.]

**Problem Description:**
[What happened (CA) or could happen (PA)?]

**Root Cause Analysis:**
[5 Whys or other root cause analysis]
1. Why did this happen? [Answer]
2. Why? [Answer]
3. Why? [Answer]
4. Why? [Answer]
5. Why? [Root cause identified]

**Impact:**
- **CTQs Affected:** [CTQ-X.X]
- **Risks Related:** [R-XXX]
- **Assumptions Affected:** [A-XXX]
- **Impact Assessment:** [What is the consequence if not addressed?]

**Action Plan:**
1. [Specific action step 1]
2. [Specific action step 2]
3. [Specific action step 3]
   ...

**Owner:** [Person responsible]
**Target Date:** YYYY-MM-DD
**Status:** [Open / In Progress / Implemented / Verified / Closed]

**Implementation Notes:**
[Details of what was done, when, by whom]

**Verification:**
**Method:** [How effectiveness was verified - testing, audit, monitoring, etc.]
**Results:** [Was action effective? Problem resolved/prevented?]
**Date Verified:** YYYY-MM-DD

**Date Closed:** YYYY-MM-DD
**Closed By:** [Name]

**Related Items:**
- Change: CHG-XXX
- Risk: R-XXX
- Requirement: REQ-XXX
- Defect: DEF-XXX

**Lessons Learned:**
[What did we learn? How can we prevent similar issues?]
```

---

## CAPA Triggers and Examples

### From Risk Register
When risk R-XXX manifests as actual incident → CAPA opened
- Example: R-009 (Safety/legal downstream impact) → Incorrect guidance given → CAPA to fix and prevent

### From Verification/Validation
When testing reveals defect or CTQ not met → CAPA opened
- Example: VER-001 (risk classification test) fails → CAPA to correct logic and add test coverage

### From Production Incidents
When quality issue occurs in production → CAPA opened
- Example: User reports artifact set incomplete → CAPA to fix and prevent

### From Measurement Plan
When metric falls below target → CAPA opened
- Example: M-007 (comprehension) <90% → CAPA to improve guidance clarity

### From Control Plan
When monitored assumption invalidated → CAPA opened
- Example: A-006 (internal use) violated by external access → CAPA to reassess risk and add controls

### From User Feedback
When users report problems or suggest improvements → CAPA opened
- Example: Users consistently confused by intake question #3 → CAPA to clarify question

### From Audit/Review
When quality review identifies gap → CAPA opened
- Example: Traceability audit finds orphaned requirements → CAPA to restore links and improve process

---

## CAPA Statistics (Updated Quarterly)

*To be populated after CAPA entries exist*

| Quarter | Total CAPAs | Corrective | Preventive | Critical | Major | Minor | Avg Time to Close |
|---------|-------------|------------|------------|----------|-------|-------|-------------------|
| 2025-Q4 | 0 | 0 | 0 | 0 | 0 | 0 | N/A |
| 2025-Q1 | - | - | - | - | - | - | - |

---

## CAPA Effectiveness Tracking

For each closed CAPA, track:
- **Recurrence:** Did same or similar problem occur again?
- **Effectiveness:** Was action successful in resolving/preventing issue?
- **Timeliness:** Was CAPA closed within target date?

If CAPA ineffective or problem recurs:
- Re-open CAPA or create new CAPA
- Perform deeper root cause analysis
- Escalate if systemic issue identified

---

## CAPA Review

### Monthly Review
- Review all open CAPAs
- Check status and progress
- Identify blocked or overdue CAPAs
- Escalate critical CAPAs if delayed

### Quarterly Review
- Analyze CAPA trends
  - Are similar issues recurring?
  - Which CTQs/risks have most CAPAs?
  - Are preventive actions effective?
- Review CAPA effectiveness
- Identify systemic improvements needed
- Update Risk Register based on CAPA learnings

### Annual Review
- Full CAPA analysis for continuous improvement
- Identify process improvements to reduce CAPA rate
- Review CAPA process effectiveness
- Update CAPA process if needed

---

## CAPA Process Effectiveness Metrics

| Metric | Target | Purpose |
|--------|--------|---------|
| Critical CAPA Time to Close | <1 week | Ensure safety/compliance issues resolved quickly |
| Major CAPA Time to Close | <1 month | Ensure significant issues resolved promptly |
| CAPA Recurrence Rate | <5% | Ensure root cause addressed, not just symptoms |
| CAPA Effectiveness | >95% | Ensure actions actually solve problems |
| Preventive vs. Corrective Ratio | ≥1:1 | Prefer prevention over correction |

---

## Integration with Other QMS Artifacts

### Risk Register
- Risks that manifest → CAPA (Corrective)
- New risks identified through CAPA → Update Risk Register
- Risk mitigation failures → CAPA to improve mitigation

### Change Log
- CAPA actions often result in changes → Link CAPA-XXX to CHG-XXX
- Changes that cause problems → CAPA (Corrective)

### Measurement Plan
- Metrics below target → Trigger CAPA
- CAPA effectiveness measured via metrics

### Control Plan
- Monitored assumptions invalidated → Trigger CAPA
- CAPA effectiveness monitored via Control Plan

### Traceability Index
- CAPA actions may affect requirements, design, tests
- Maintain traceability for CAPA-related changes

---

## CAPA Log Maintenance

**Owner:** Project Owner
**Update Frequency:** Per CAPA (real-time)
**Review Frequency:** Monthly, Quarterly, Annual
**Last Updated:** 2025-12-12
**Next Review:** TBD

---

## CAPA Sign-off

Critical CAPAs (severity=Critical) require sign-off upon closure:

**CAPA ID:** _________________
**Verified by:** _________________
**Date:** _________________
**Signature:** _________________
