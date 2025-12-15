# Control Plan
## QMS Dashboard Project

**Risk Level:** R2
**Date:** 2025-12-12
**Status:** First-pass

---

## Purpose
Define ongoing monitoring and control activities to maintain quality throughout the system lifecycle. The Control Plan ensures:
- Validated assumptions remain valid (monitoring)
- CTQs continue to be met in production
- Changes are controlled and don't introduce quality regressions
- Corrective and preventive actions are triggered when needed

---

## Control Strategy

### Approach
- **Monitor validated assumptions:** Track triggers that would invalidate A-005 through A-009
- **Continuous measurement:** Ongoing collection of metrics from Measurement Plan
- **Change control:** All changes evaluated for quality impact before implementation
- **Incident response:** Process for handling quality issues and triggering CAPA
- **Periodic review:** Regular quality reviews to identify trends and improvements

### Control Phases
1. **Initial Release:** Establish baseline measurements and controls
2. **Production Operation:** Active monitoring and measurement
3. **Continuous Improvement:** Regular reviews and refinements

---

## Monitored Assumptions (from Assumptions Register)

### A-005: Individual Scale Appropriate
**Assumption:** System designed for individual use, not multi-user collaboration

**Control Method:** **MONITOR**
- Track user requests for collaboration features
- Monitor if multiple users attempt to work on same project
- Watch for scale expansion requests (Team, Multi-team)

**Monitoring Frequency:** Quarterly review of user feedback and support tickets

**Trigger for Re-assessment:**
- ≥3 requests for multi-user features
- Deployment for team/multi-team use
- Shared file access patterns detected

**Action if Triggered:**
- Re-run quality intake with updated scale
- Re-classify risk (may increase from R2)
- Assess architecture changes needed for collaboration
- Update quality plan accordingly

**Owner:** Project Owner

---

### A-006: Internal Use Only
**Assumption:** System used internally, no external access

**Control Method:** **MONITOR**
- Review deployment environment (quarterly)
- Check access controls and authentication
- Monitor if system exposed to external networks
- Track if external users given access

**Monitoring Frequency:** Quarterly deployment review

**Trigger for Re-assessment:**
- System deployed to public-facing server
- External users granted access
- Plans to open-source or share externally

**Action if Triggered:**
- **CRITICAL:** Re-run quality intake with "External" or "Public" users
- Risk classification will likely increase to R3
- Add security and privacy requirements
- Implement authentication, authorization, audit logging
- Update all quality artifacts for higher risk level

**Owner:** Project Owner

---

### A-007: Easy Reversibility
**Assumption:** Failures can be easily detected and corrected

**Control Method:** **MONITOR**
- Track time-to-detect issues (M-011: incident reports)
- Track time-to-correct issues (CAPA Log)
- Monitor if incorrect guidance causes downstream harm before detection

**Monitoring Frequency:** Per incident (immediate), Quarterly trend analysis

**Trigger for Re-assessment:**
- Time-to-detect >1 week for any issue
- Any incident where incorrect guidance not caught before downstream impact
- Pattern of delayed detection

**Action if Triggered:**
- Re-assess reversibility assumption (may need to change to "Partial" or "Hard")
- Risk classification may increase
- Enhance monitoring, alerts, validation checks
- Add review gates before critical decisions

**Owner:** Project Owner

---

### A-008: No Direct Regulation
**Assumption:** QMS Dashboard not subject to regulatory oversight

**Control Method:** **MONITOR**
- Monitor regulatory landscape changes
- Review if system used for regulated projects
- Check if system inherits regulatory requirements from context
- Legal/compliance updates

**Monitoring Frequency:** Annual regulatory review, Triggered by use case changes

**Trigger for Re-assessment:**
- System used to manage FDA/EMA regulated projects
- Legal advice indicates regulatory applicability
- Audit reveals compliance requirements
- System becomes part of regulated process

**Action if Triggered:**
- **CRITICAL:** Re-run quality intake with "Yes" for regulated
- Risk classification will likely increase to R3
- Add design controls, validation evidence
- Implement full compliance documentation
- Consider regulatory expert involvement

**Owner:** Project Owner

---

### A-009: Recommendations Not Automated
**Assumption:** System provides recommendations, humans review and approve

**Control Method:** **MONITOR**
- Review system architecture for automated actions
- Check if "auto-apply" features added
- Monitor if human review bypassed in workflow
- Code review for automated artifact application

**Monitoring Frequency:** Each release (code review), Quarterly architecture review

**Trigger for Re-assessment:**
- Any feature that auto-applies quality artifacts without human approval
- Workflow that bypasses human review
- User requests for automation of critical decisions

**Action if Triggered:**
- Re-assess risk classification (may increase to R3)
- Ensure human-in-the-loop for all critical decisions
- Add approval gates and audit trail
- Update quality plan for higher risk

**Owner:** Developer / Project Owner

---

## CTQ Monitoring (from Measurement Plan)

| CTQ | Metric | Target | Monitoring Frequency | Alert Threshold |
|-----|--------|--------|---------------------|-----------------|
| CTQ-1.1 | M-001: Risk classification accuracy | ≥95% | Quarterly | <95% |
| CTQ-1.2 | M-002: Artifact set correctness | 100% | Monthly | Any failure |
| CTQ-1.3 | M-003: Traceability integrity | 100% | Per build | <100% |
| CTQ-2.1 | M-004: Artifact completion | 100% status defined | Per project | Any undefined |
| CTQ-2.2 | M-004: No silent skipping | 0 undefined | Per project | Any undefined |
| CTQ-2.3 | M-005: Content quality | ≥90% useful | Quarterly | <90% |
| CTQ-3.1 | M-006: Intake time | <10 min avg | Validation, Ad-hoc | >10 min |
| CTQ-3.2 | M-007: User comprehension | >90% | Quarterly | <90% |
| CTQ-3.3 | M-008: Artifact actionability | >80% | Quarterly | <80% |
| CTQ-4.2 | M-009: Rigor appropriateness | >85% | Annual | <85% |

**Control Actions:**
- Green (meets target): Continue monitoring
- Yellow (approaching threshold): Investigate, trend analysis
- Red (below threshold): CAPA process, immediate action

---

## Change Control Process

All changes to the QMS Dashboard system must follow this process:

### Change Request
1. **Identify change:** Feature request, bug fix, improvement, etc.
2. **Document change:** Description, justification, impact assessment
3. **Log in Change Log:** Entry created with status "Proposed"

### Impact Assessment
Evaluate change against:
- **Risk classification:** Does change affect intake, risk logic, artifact generation?
- **Assumptions:** Does change invalidate any assumptions (A-001 through A-010)?
- **CTQs:** Does change impact any CTQ (positively or negatively)?
- **Traceability:** Does change require traceability updates?
- **Verification/Validation:** Does change require re-testing or re-validation?

### Change Approval
- **Low impact:** Developer approval (e.g., UI text, documentation)
- **Medium impact:** Project Owner approval (e.g., new feature, template changes)
- **High impact:** Full quality review + approval (e.g., risk classification changes, new artifact types)

### Implementation
1. Implement change with traceability (link to requirements, Change Log entry)
2. Update affected artifacts (CTQ Tree, Risk Register, etc.)
3. Perform verification testing (regression suite minimum)
4. Update documentation

### Verification
- Run regression tests (M-001, M-002, M-003)
- Verify traceability maintained
- Confirm no quality regressions

### Change Log Update
- Mark change as "Implemented"
- Document verification results
- Close change request

---

## Incident Response Process

When quality issue, defect, or non-conformance detected:

### 1. Report Incident
- Document issue in defect tracker or CAPA Log
- Classify severity: Critical / Major / Minor
- Identify which CTQ, risk, or assumption affected

### 2. Immediate Action (Critical/Major only)
- Contain issue: Prevent further impact
- Notify affected users if needed
- Apply temporary workaround if available

### 3. Root Cause Analysis
- Investigate why issue occurred
- Identify contributing factors
- Determine if issue indicates systemic problem

### 4. Corrective Action (CAPA)
- Create CAPA Log entry
- Define corrective action to fix issue
- Define preventive action to prevent recurrence
- Assign owner and due date

### 5. Implement CAPA
- Implement corrective action
- Verify fix effectiveness
- Update processes, documentation, tests to prevent recurrence

### 6. Close Incident
- Verify issue resolved
- Update CAPA Log with results
- Document lessons learned

---

## Periodic Quality Reviews

### Monthly Review (if system in active use)
**Participants:** Project Owner, Developer
**Duration:** 30 minutes

**Agenda:**
- Review metrics: M-002 (artifact correctness), M-004 (completion), M-010 (defects)
- Open CAPA status review
- Recent Change Log entries and impact
- User feedback summary
- Action items from previous review

**Output:** Action items, CAPA entries if needed

---

### Quarterly Review
**Participants:** Project Owner, Developer, Stakeholders
**Duration:** 1-2 hours

**Agenda:**
- Full metrics review (M-001 through M-011)
- Assumption monitoring (A-005 through A-009)
- Risk Register review and update
- Traceability audit (M-003)
- Change Control summary
- CAPA effectiveness review
- Continuous improvement opportunities

**Output:**
- Updated Risk Register
- CAPA entries for identified issues
- Improvement plan

---

### Annual Review
**Participants:** Project Owner, Developer, QMS Expert, Stakeholders
**Duration:** Half day

**Agenda:**
- Full quality plan review
- Risk re-classification assessment (should intake be re-run?)
- Assumption re-validation (A-001 through A-010)
- CTQ Tree review and updates
- Measurement Plan review (targets still appropriate?)
- Control Plan review (this document)
- Long-term improvement roadmap

**Output:**
- Updated Quality Plan and all artifacts as needed
- Strategic improvement initiatives
- Resource planning

---

## Compliance Monitoring

### Artifact Status Enforcement
**Control:** Ensure no artifacts silently skipped (CTQ-2.2)

**Method:**
- Audit artifact status at each quality gate
- Check for undefined status (must be Done/Deferred/Deviated)
- Require deviation approval for any skipped artifact

**Frequency:** Per project, at quality gates

**Action if Non-compliant:**
- Flag immediately
- Require status definition before proceeding
- Log deviation if artifact skipped

---

### Traceability Maintenance
**Control:** Ensure requirements-to-implementation traceability maintained (CTQ-1.3)

**Method:**
- Automated traceability check per build (M-003)
- Quarterly manual traceability audit
- Code review includes traceability verification

**Frequency:** Continuous (automated), Quarterly (audit)

**Action if Non-compliant:**
- Block release until traceability gaps resolved
- CAPA entry to identify why traceability broke

---

## Control Plan Activation

This Control Plan activates upon:
- [ ] Initial release to production/use
- [ ] All Priority 1 verification tests passing
- [ ] All Priority 1 validation tests passing
- [ ] Baseline measurements established (Measurement Plan)

**Activation Date:** _________________
**Activated by:** _________________

---

## Control Plan Maintenance

This Control Plan is a living document:
- Updated when assumptions, risks, or CTQs change
- Updated when new control needs identified
- Reviewed annually and revised as needed

**Last Review Date:** 2025-12-12
**Next Review Date:** TBD (annual)
**Document Owner:** Project Owner

---

## Control Plan Sign-off

**Approved by:** _________________
**Date:** _________________
**Signature:** _________________
