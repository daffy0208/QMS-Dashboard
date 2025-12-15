# Measurement Plan
## QMS Dashboard Project

**Risk Level:** R2
**Date:** 2025-12-12
**Status:** First-pass

---

## Purpose
Define metrics to track quality, performance, and effectiveness of the QMS Dashboard system. Measurements support:
- Monitoring CTQ achievement
- Risk mitigation effectiveness
- Continuous improvement
- Quality gate decisions

---

## Measurement Strategy

### Approach
- **CTQ-driven:** Each CTQ has defined measurement method
- **Risk-based:** Prioritize metrics for high-risk areas (R-001, R-006, R-009)
- **Actionable:** Metrics trigger improvement actions when targets not met
- **Baseline → Monitor → Improve:** Establish baseline, track trends, drive improvements

### Measurement Types
1. **Quality Metrics:** Accuracy, completeness, correctness
2. **Performance Metrics:** Speed, efficiency, resource usage
3. **Usability Metrics:** User satisfaction, comprehension, ease of use
4. **Process Metrics:** Artifact completion, traceability, compliance

---

## CTQ Measurements

### M-001: Risk Classification Accuracy (CTQ-1.1)
**Definition:** Percentage of intake sessions producing correct risk classification per intake-rules.md

**Measurement Method:**
- **Development/Test:** Automated test suite pass rate (VER-001)
- **Production:** Expert review of sample classifications (quarterly)
- **Production:** User corrections (track if users manually override classification)

**Formula:** `Accuracy = (Correct Classifications / Total Classifications) × 100%`

**Target:** ≥100% in testing, ≥95% in production (allowing for edge cases)

**Data Collection:**
- Test results: Continuous (automated)
- Expert review: Quarterly sample (n=10 projects)
- User corrections: Log all manual overrides

**Reporting:** Monthly summary, exception report for failures

**Trigger Actions:**
- <100% in testing → Fix defects before release
- <95% in production → Review intake questions, add guidance/examples

---

### M-002: Artifact Set Correctness (CTQ-1.2)
**Definition:** Percentage of sessions generating complete and correct artifact set for risk level

**Measurement Method:**
- Automated check: Verify file count and names match requirements for R0/R1/R2/R3
- Manual audit: Sample review of artifact sets (monthly)

**Formula:** `Correctness = (Correct Artifact Sets / Total Generated Sets) × 100%`

**Target:** 100%

**Data Collection:**
- Automated: Every artifact generation
- Manual audit: Monthly (n=10 sessions)

**Reporting:** Real-time dashboard, monthly summary

**Trigger Actions:**
- Any failure → Critical defect, immediate fix

---

### M-003: Traceability Integrity (CTQ-1.3)
**Definition:** Percentage of requirements with valid traceability links (no orphans)

**Measurement Method:**
- Automated traceability matrix check (VER-003-A)
- Manual traceability audit (quarterly)

**Formula:** `Integrity = (Requirements with Valid Links / Total Requirements) × 100%`

**Target:** 100%

**Data Collection:**
- Automated: At each build/commit
- Manual audit: Quarterly

**Reporting:** Build status, quarterly traceability report

**Trigger Actions:**
- <100% → Block release, fix traceability gaps

---

### M-004: Artifact Completion Rate (CTQ-2.1, CTQ-2.2)
**Definition:** Percentage of required artifacts reaching "Done" status (not silently skipped)

**Measurement Method:**
- Track artifact status: Done / Deferred / Deviated / Undefined
- Monitor for undefined status (silent skipping)

**Formula:** `Completion = (Done + Deferred + Deviated) / Total Required × 100%`

**Target:**
- 100% have defined status (no undefined)
- ≥80% reach "Done" status by project end

**Data Collection:**
- Automated status check (if tooling exists)
- Manual audit during quality gates

**Reporting:** Per-project artifact status dashboard

**Trigger Actions:**
- Any undefined status → Flag for immediate attention
- <80% Done at release → Review deviations, assess risk

---

### M-005: First-pass Content Quality (CTQ-2.3)
**Definition:** Percentage of generated artifact content retained (not requiring complete rewrite)

**Measurement Method:**
- User survey: "How much of the generated content was useful?" (scale 1-5)
- VAL-006: Content retention analysis (manual review of completed artifacts)

**Formula:** `Quality = (Artifacts Rated ≥3 / Total Artifacts Reviewed) × 100%`

**Target:** ≥90% rated useful (≥3/5), <10% requiring complete rewrite

**Data Collection:**
- User survey: After each project (voluntary)
- Content retention: Validation phase (VAL-006)

**Reporting:** Quarterly summary

**Trigger Actions:**
- <90% useful → Review and improve templates
- Specific artifact consistently low → Prioritize that artifact for improvement

---

### M-006: Intake Completion Time (CTQ-3.1)
**Definition:** Average time for users to complete 7-question intake

**Measurement Method:**
- Timed sessions during validation (VAL-001)
- Log timestamps if tooling exists: start intake → submit responses

**Formula:** `Average Time = Σ(Completion Times) / Number of Sessions`

**Target:** <10 minutes average, <15 minutes maximum

**Data Collection:**
- Validation: VAL-001 timing
- Production: Timestamps (if logged)

**Reporting:** Validation report, ongoing monitoring if instrumented

**Trigger Actions:**
- >10 minute average → Simplify questions or provide better guidance
- Users consistently stuck on specific question → Clarify that question

---

### M-007: User Comprehension Rate (CTQ-3.2)
**Definition:** Percentage of users who correctly understand their risk classification and required artifacts

**Measurement Method:**
- Validation testing (VAL-002-A, VAL-002-B)
- Post-intake quiz: "What risk level was assigned? Why?"
- User support tickets related to confusion

**Formula:** `Comprehension = (Users Answering Correctly / Total Users Tested) × 100%`

**Target:** >90% comprehension

**Data Collection:**
- Validation: VAL-002 results
- Production: Support ticket analysis (quarterly)

**Reporting:** Validation report, quarterly user feedback summary

**Trigger Actions:**
- <90% → Improve guidance, add explanations, clarify terminology

---

### M-008: Artifact Actionability (CTQ-3.3)
**Definition:** Percentage of users able to proceed with generated artifacts without additional guidance

**Measurement Method:**
- Validation pilot testing (VAL-003)
- User survey: "Were you able to use the artifacts effectively?" (Yes/No/Partially)
- Support request rate

**Formula:** `Actionability = (Users Proceeding Successfully / Total Users) × 100%`

**Target:** >80%

**Data Collection:**
- Validation: VAL-003 results
- Production: User survey, support tickets

**Reporting:** Validation report, quarterly survey

**Trigger Actions:**
- <80% → Improve artifact content, add examples, provide guidance

---

### M-009: Rigor Appropriateness (CTQ-4.2)
**Definition:** User agreement that quality rigor matches project risk

**Measurement Method:**
- Validation survey (VAL-005): Likert scale 1-5
- Post-project feedback: "Was the quality plan appropriate?"

**Formula:** `Appropriateness = (Users Rating ≥4 / Total Users) × 100%`

**Target:** >85% rate ≥4/5

**Data Collection:**
- Validation: VAL-005 survey
- Production: Post-project survey (optional)

**Reporting:** Validation report, annual review

**Trigger Actions:**
- <85% → Review rigor mode mapping, adjust if pattern emerges
- Specific risk level consistently inappropriate → Revise requirements for that level

---

### M-010: Defect Density
**Definition:** Number of defects found per phase (testing, validation, production)

**Measurement Method:**
- Track all defects by severity (Critical / Major / Minor) and phase detected
- Calculate defect escape rate (defects found in production vs. testing)

**Formula:**
- `Defect Density = Total Defects / Size (e.g., per 1000 lines of code)`
- `Escape Rate = Production Defects / Total Defects × 100%`

**Target:**
- <5 critical defects in testing (should be 0 at release)
- <5% escape rate (most defects caught before production)

**Data Collection:**
- Defect tracking system (issue tracker)

**Reporting:** Weekly during development, monthly summary

**Trigger Actions:**
- Critical defects → Immediate fix, root cause analysis
- High escape rate → Improve testing, verification coverage

---

### M-011: Risk Mitigation Effectiveness
**Definition:** Percentage of identified risks with effective mitigations (no incidents)

**Measurement Method:**
- Track incidents related to identified risks (R-001 through R-010)
- Monitor if mitigations prevented incidents
- CAPA Log entries

**Formula:** `Effectiveness = (Risks with No Incidents / Total Risks) × 100%`

**Target:** >95% (incidents for <5% of identified risks)

**Data Collection:**
- Incident reports
- CAPA Log
- Risk Register updates

**Reporting:** Quarterly risk review

**Trigger Actions:**
- Incident occurs → CAPA process, review and enhance mitigation
- Pattern of same risk type → Systematic improvement needed

---

## Measurement Schedule

| Metric | Frequency | Owner | Report To |
|--------|-----------|-------|-----------|
| M-001: Risk classification accuracy | Continuous (test), Quarterly (review) | Developer | Project Owner |
| M-002: Artifact set correctness | Continuous (automated), Monthly (audit) | Developer | Project Owner |
| M-003: Traceability integrity | Per build, Quarterly audit | Developer | Project Owner |
| M-004: Artifact completion | Per project, Quality gates | Project Owner | Project Owner |
| M-005: Content quality | Validation, Quarterly survey | Project Owner | Project Owner |
| M-006: Intake completion time | Validation (VAL-001) | Project Owner | Project Owner |
| M-007: User comprehension | Validation (VAL-002), Quarterly | Project Owner | Project Owner |
| M-008: Artifact actionability | Validation (VAL-003), Quarterly | Project Owner | Project Owner |
| M-009: Rigor appropriateness | Validation (VAL-005), Annual | Project Owner | Project Owner |
| M-010: Defect density | Weekly (dev), Monthly (summary) | Developer | Project Owner |
| M-011: Risk mitigation effectiveness | Quarterly | Project Owner | Project Owner |

---

## Measurement Infrastructure

### Tools and Systems
- **Automated Testing:** Test framework with metrics dashboard
- **Defect Tracking:** Issue tracker (GitHub Issues, Jira, etc.)
- **Survey:** Google Forms, Typeform for user feedback
- **Logs:** Timestamps, usage logs (if instrumented)
- **Audit:** Manual reviews using checklists

### Data Storage
- Test results: CI/CD system
- User feedback: Survey responses, stored securely
- Metrics dashboard: Spreadsheet or BI tool
- Historical data: Retained for trend analysis

---

## Baseline Establishment

### Phase 1: Validation (Initial Baseline)
- Collect M-005, M-006, M-007, M-008, M-009 during validation testing
- Establish initial targets based on validation results

### Phase 2: Production (Ongoing Measurement)
- Continue monitoring all metrics
- Refine targets based on actual performance
- Identify improvement opportunities

---

## Measurement Review and Action

### Monthly Review
- M-002: Artifact set correctness
- M-010: Defect density
- M-004: Artifact completion (for active projects)

### Quarterly Review
- M-001: Risk classification (expert review)
- M-003: Traceability audit
- M-005: Content quality survey
- M-007: Comprehension (support ticket analysis)
- M-011: Risk mitigation effectiveness

### Annual Review
- Full measurement plan review
- Trend analysis for all metrics
- Update targets based on maturity
- Continuous improvement initiatives

### Triggered Reviews
- When any metric falls below target → Root cause analysis, corrective action
- Critical incidents → CAPA process, immediate review

---

## Reporting

### Metrics Dashboard (if tooling exists)
- Real-time: M-001, M-002, M-003 (automated checks)
- Weekly: M-010 (defect tracking)
- Monthly: M-004 (artifact completion)

### Quality Report (Quarterly)
- Summary of all metrics
- Trend analysis (improving/declining)
- Action items and status
- Risk review findings

---

## Continuous Improvement

Based on measurement results:
1. **Metrics below target:** Root cause analysis, improvement plan
2. **Consistent excellence:** Share best practices, consider raising targets
3. **New risks identified:** Update Risk Register, add mitigations
4. **User feedback:** Prioritize improvements based on impact
5. **Defect trends:** Focus verification efforts on problem areas

---

## Measurement Plan Sign-off

**Approved by:** _________________
**Date:** _________________
**Signature:** _________________
