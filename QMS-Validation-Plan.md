# Validation Plan
## QMS Dashboard Project

**Risk Level:** R2
**Date:** 2025-12-12
**Status:** First-pass

---

## Purpose
Define how to validate that the QMS Dashboard system meets user needs and is fit for its intended use. Validation answers: **"Did we build the right thing?"**

---

## Validation Strategy

### Approach
- **User-centered:** Validation involves actual target users (QMS stakeholders, project leads)
- **Real-world scenarios:** Test with representative projects across risk levels
- **Assumption validation:** Explicitly test assumptions A-001, A-002, A-003, A-004, A-010
- **Iterative refinement:** Validation feedback informs design improvements

### Validation vs. Verification
- **Verification (testing):** "Does system work correctly?" → Covered in Verification Plan
- **Validation (acceptance):** "Does system meet user needs?" → This plan

---

## Validation Scope

### In Scope
- User ability to complete intake efficiently (CTQ-3.1)
- User comprehension of guidance and artifacts (CTQ-3.2)
- Artifact actionability - can users proceed with quality plan? (CTQ-3.3)
- Risk-appropriate rigor - does generated plan match project needs? (CTQ-4.2)
- Domain applicability - does framework work across project types? (CTQ-4.1)
- Assumption validation - are key assumptions true? (A-001 through A-010)

### Out of Scope (Covered by Verification)
- Technical correctness of risk classification logic
- Artifact file generation mechanics
- Traceability link integrity

---

## CTQ-to-Validation Mapping

### CTQ-3.1: Intake Completion Time
**Target:** <10 minutes average

**Validation Methods:**
- **VAL-001:** User testing - timed intake sessions
  - 5-10 users from target audience
  - Measure time from start to completion
  - Track hesitation points and confusion

**Pass Criteria:**
- 80% of users complete intake in <10 minutes
- No user takes >15 minutes
- Users report intake was "reasonable" or "easy" (Likert scale ≥3/5)

**Participants:** Internal team members who manage projects

---

### CTQ-3.2: Guidance Clarity
**Target:** >90% comprehension

**Validation Methods:**
- **VAL-002-A:** User comprehension testing
  - After intake, ask users to explain:
    - What risk level their project was classified as and why
    - What artifacts are required
    - What their next steps should be
  - Measure % who answer correctly

- **VAL-002-B:** Artifact interpretation testing
  - Give users generated artifact set
  - Ask them to identify purpose of each artifact
  - Ask what they would do with each artifact

**Pass Criteria:**
- >90% correctly understand their risk classification
- >85% correctly identify purpose of generated artifacts
- >80% can describe next steps without additional guidance

**Participants:** 5-10 users, mix of QMS-experienced and QMS-novice

---

### CTQ-3.3: Artifact Actionability
**Target:** >80% can proceed without additional guidance

**Validation Methods:**
- **VAL-003:** Real-world pilot testing
  - Users take generated artifacts for an actual project
  - Attempt to use artifacts without additional support
  - Track:
    - % who successfully expand CTQ tree
    - % who add relevant risks to Risk Register
    - % who complete at least 3 artifacts to "Done" status
  - Follow-up interview: "What was helpful? What was missing?"

**Pass Criteria:**
- >80% of users successfully use artifacts without needing help
- >75% report artifacts were "helpful" or "very helpful" (Likert ≥4/5)
- <20% abandon artifacts and start from scratch

**Participants:** 5-10 users with actual projects in planning phase

---

### CTQ-4.1: Domain Alignment
**Target:** No conflicts with applicable standards

**Validation Methods:**
- **VAL-004-A:** Expert review
  - QMS expert evaluates framework against:
    - ISO 9001 (general QMS)
    - IEC 62304 (medical device software)
    - FDA QSR (Quality System Regulation)
    - GAMP 5 (pharmaceutical systems)
  - Identify conflicts, gaps, or misalignments

- **VAL-004-B:** Multi-domain pilot testing
  - Test framework with projects from different domains:
    - Web application
    - Embedded system
    - Data science / ML project
    - Infrastructure / DevOps
  - Assess if framework adapts appropriately

**Pass Criteria:**
- Expert confirms no major conflicts with QMS standards
- Framework produces reasonable quality plans for ≥3 different project types
- Users from different domains report framework was applicable (≥3/5 rating)

**Participants:** QMS expert + users from diverse project domains

---

### CTQ-4.2: Risk-appropriate Rigor
**Target:** >85% agreement that rigor matches project needs

**Validation Methods:**
- **VAL-005:** Rigor appropriateness survey
  - After viewing generated quality plan, users rate:
    - "The level of quality rigor is appropriate for my project's risk" (Likert 1-5)
    - "The artifacts required seem necessary" (Likert 1-5)
    - "I feel confident this quality plan will prevent problems" (Likert 1-5)
  - Separate cohorts for R0, R1, R2, R3 projects

**Pass Criteria:**
- >85% rate rigor as "appropriate" or "highly appropriate" (≥4/5)
- No pattern of "too much" or "too little" rigor for any risk level
- Users of R3 projects confirm strict rigor is warranted

**Participants:** 10-20 users across all risk levels (R0-R3)

---

## Assumption Validation

### A-001: Intake Questions Sufficient
**Validation:** VAL-002 (comprehension) + VAL-005 (rigor appropriateness)
- If risk classification matches expert assessment → questions sufficient
- If users consistently misclassify → questions need refinement

**Success Criteria:** >90% agreement between user classification and expert assessment

---

### A-002: User Domain Knowledge
**Validation:** VAL-001 (completion time) + VAL-002 (comprehension)
- Monitor users struggling to answer intake questions
- Track questions with most "I don't know" or hesitation

**Success Criteria:** <10% of users unable to answer intake questions confidently

---

### A-003: Framework Applicability
**Validation:** VAL-004-B (multi-domain pilot)
- Test with web, embedded, data science, infrastructure projects
- Confirm framework generates sensible quality plans for each

**Success Criteria:** Framework works for ≥3 different project types with ≥3/5 user rating

---

### A-004: Artifact Templates Adequate
**Validation:** VAL-003 (actionability) + VAL-006 (content retention)
- **VAL-006:** Measure % of generated content retained vs. rewritten
  - Review completed artifacts from pilot users
  - Calculate % of first-pass content kept, modified, deleted

**Success Criteria:** >50% of generated content retained with modification, <10% requiring complete rewrite

---

### A-005, A-006, A-007, A-008, A-009: Already Validated by Intake
These assumptions were confirmed during intake and require ongoing monitoring (covered in Control Plan), not initial validation.

---

### A-010: Markdown Format Adequate
**Validation:** VAL-007 (format usability)
- User feedback on artifact format
- Track requests for different format (database, spreadsheet, tool integration)
- Assess if markdown links and structure are maintainable

**Success Criteria:** <20% of users request alternative format, >80% find markdown acceptable

---

## Risk-based Validation Priorities

### Priority 1 (Critical - Required for Release)
1. **R-009 Mitigation:** Safety/legal downstream impact
   - VAL-002: Ensure users comprehend guidance (prevent misuse)
   - VAL-005: Ensure rigor is appropriate (prevent under-engineering)
   - VAL-004-A: Expert confirms framework is sound

2. **R-007 Mitigation:** User misunderstanding
   - VAL-002: Comprehension testing
   - VAL-003: Actionability testing

3. **A-001 Validation:** Intake questions sufficient
   - VAL-002, VAL-005: Confirm questions lead to correct classification

### Priority 2 (High - Validate During Development)
4. **R-002 Mitigation:** Invalid assumptions
   - VAL-004-B: Framework applicability (A-003)
   - VAL-006: Template adequacy (A-004)

5. **R-003 Mitigation:** Inadequate CTQ coverage
   - VAL-003: Real-world pilot to identify missing CTQs

### Priority 3 (Medium - Validate Before Final Release)
6. **CTQ-3.1:** Intake efficiency
   - VAL-001: Completion time

7. **A-010 Validation:** Markdown format adequate
   - VAL-007: Format usability

---

## Validation Test Cases (Summary)

| Test ID | CTQ / Assumption | Method | Participants | Priority | Status |
|---------|------------------|--------|--------------|----------|--------|
| VAL-001 | CTQ-3.1 | Timed intake sessions | 5-10 users | P3 | Pending |
| VAL-002-A | CTQ-3.2, A-001 | Comprehension testing | 5-10 users | P1 | Pending |
| VAL-002-B | CTQ-3.2 | Artifact interpretation | 5-10 users | P1 | Pending |
| VAL-003 | CTQ-3.3, A-004 | Real-world pilot | 5-10 users | P1 | Pending |
| VAL-004-A | CTQ-4.1 | Expert review | QMS expert | P1 | Pending |
| VAL-004-B | CTQ-4.1, A-003 | Multi-domain pilot | 4+ diverse users | P2 | Pending |
| VAL-005 | CTQ-4.2, A-001 | Rigor appropriateness survey | 10-20 users | P1 | Pending |
| VAL-006 | A-004 | Content retention analysis | Pilot users | P2 | Pending |
| VAL-007 | A-010 | Format usability feedback | All users | P3 | Pending |

---

## Validation Participants

### Target User Profile
- **Primary:** Project leads, engineering managers, quality engineers
- **Context:** Planning software projects (web, embedded, data science, infrastructure)
- **Experience:** Mix of QMS-experienced and QMS-novice
- **Scale:** Individual to multi-team projects

### Recruitment
- Internal team members
- Partner organizations (if available)
- Professional networks (for domain experts)

### Sample Size
- **Minimum:** 5 users for usability testing (VAL-001, VAL-002, VAL-003)
- **Recommended:** 10-20 users for rigor survey (VAL-005) to cover all risk levels
- **Expert:** 1-2 QMS experts for VAL-004-A

---

## Validation Schedule

| Phase | Activities | Target Date | Status |
|-------|-----------|-------------|--------|
| Planning | Define validation approach (this document) | 2025-12-12 | ✅ Done |
| Participant Recruitment | Identify and schedule users | TBD | Not Started |
| Expert Review | VAL-004-A with QMS expert | TBD | Not Started |
| Usability Testing | VAL-001, VAL-002 | TBD | Not Started |
| Pilot Testing | VAL-003, VAL-004-B, VAL-006 | TBD | Not Started |
| Survey | VAL-005, VAL-007 | TBD | Not Started |
| Analysis | Compile results, identify gaps | TBD | Not Started |
| Refinement | Address validation findings | TBD | Not Started |
| Validation Complete | All Priority 1 tests passing | TBD | Not Started |

---

## Validation Environment

### Setup
- Real or realistic project scenarios for each risk level (R0, R1, R2, R3)
- Generated artifact sets for test projects
- Survey/feedback collection tools (Google Forms, Typeform, etc.)
- Interview guide for qualitative feedback

### Test Scenarios
1. **R0 Scenario:** Internal tool, low impact (e.g., developer productivity script)
2. **R1 Scenario:** Internal service, moderate impact (e.g., CI/CD pipeline)
3. **R2 Scenario:** Decision-impacting system (e.g., recommendation engine, QMS dashboard)
4. **R3 Scenario:** Safety-critical or regulated (e.g., medical device software, financial system)

---

## Pass/Fail Criteria

### Test Level
- **Pass:** Test meets defined pass criteria for that CTQ or assumption
- **Fail:** Test does not meet criteria → Requires design changes and re-validation

### Overall Validation
- **Pass:** All Priority 1 validation tests passing
- **Conditional Pass:** Priority 1 passing with minor findings, mitigation plan in place
- **Fail:** Any Priority 1 test failing OR users unable to use system effectively

---

## Validation Sign-off

Validation complete when:
- [ ] All Priority 1 validation tests complete and passing
- [ ] Critical assumptions (A-001, A-003, A-004) validated
- [ ] Risk mitigations validated (R-007, R-009)
- [ ] Expert review confirms domain alignment (VAL-004-A)
- [ ] Real-world pilot demonstrates actionability (VAL-003)
- [ ] User feedback incorporated and re-tested if significant changes made

**Validated by:** _________________
**Date:** _________________
**Signature:** _________________

---

## Post-validation Actions

Based on validation results:
1. Update CTQ Tree if new quality characteristics identified
2. Revise intake questions if comprehension issues found
3. Improve artifact templates based on actionability feedback
4. Document validated assumptions in Assumptions Register
5. Update Risk Register if new risks identified during validation
6. Refine quality plan based on lessons learned
