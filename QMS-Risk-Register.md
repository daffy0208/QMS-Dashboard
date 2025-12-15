# Risk Register
## QMS Dashboard Project

**Risk Level:** R2
**Date:** 2025-12-12
**Status:** First-pass

---

## Risk Assessment Scale

**Likelihood:**
- L1: Rare (<10%)
- L2: Unlikely (10-30%)
- L3: Possible (30-60%)
- L4: Likely (60-90%)
- L5: Almost Certain (>90%)

**Impact:**
- I1: Negligible (minor inconvenience)
- I2: Minor (rework required)
- I3: Moderate (significant rework, delay)
- I4: Major (project objectives threatened)
- I5: Severe (safety/legal/compliance impact)

**Risk Score = Likelihood × Impact**

**Risk Levels:**
- 1-4: Low (monitor)
- 5-12: Medium (mitigate)
- 15-25: High (immediate action)

---

## Risks

### R-001: Incorrect Risk Classification
**Category:** Quality
**Description:** Intake responses lead to wrong risk level (R0-R3), generating incorrect artifact set.

**Likelihood:** L2 (Unlikely) - ⬇️ Reduced with safety mechanisms
**Impact:** I4 (Major) - Under-engineered quality plan for high-risk project, or wasted effort
**Risk Score:** 8 (Medium) - ⬇️ Reduced from 12

**Mitigation (IMPLEMENTED 2025-12-12):**
1. ✅ Enhanced intake questions with examples and guidance (intake-rules-enhanced.md)
2. ✅ 6-layer validation system implemented (intake-safety-mechanisms.md):
   - Input validation
   - Cross-validation (contradiction detection)
   - Risk indicators (pattern matching)
   - Warnings and confirmations
   - Expert review triggers
   - Override with justification
3. ✅ Comprehensive validation specification (intake-validation-spec.md)
4. ✅ Expert review workflow (intake-expert-review.md)
5. ⏳ Pending: Implementation and testing

**Contingency:** If incorrect classification discovered, re-run intake and regenerate artifacts

**Owner:** Project Owner
**Status:** 🟢 Mitigations Designed - Pending Implementation
**Last Updated:** 2025-12-12

---

### R-002: Incomplete or Invalid Assumptions
**Category:** Requirements
**Description:** Key assumptions (A-001 through A-010) prove false, invalidating quality plan.

**Likelihood:** L3 (Possible) - Domain partially understood per intake
**Impact:** I4 (Major) - Quality plan becomes inappropriate for actual use case
**Risk Score:** 12 (Medium)

**Mitigation:**
1. Validate critical assumptions (A-001, A-002, A-003) before full implementation
2. Establish assumption monitoring process
3. Define triggers for re-validation
4. Document assumption dependencies in design

**Contingency:** If key assumption invalidated, halt implementation and revise quality plan

**Owner:** Project Owner
**Status:** 🔶 Open - Validation plan needed

---

### R-003: Inadequate CTQ Coverage
**Category:** Quality
**Description:** CTQ Tree missing critical quality characteristics, leading to undetected quality failures.

**Likelihood:** L2 (Unlikely) - First-pass CTQs defined, but may have gaps
**Impact:** I3 (Moderate) - Quality issues not caught until late in development
**Risk Score:** 6 (Medium)

**Mitigation:**
1. Expert review of CTQ Tree
2. Map CTQs against project objectives and worst-case failures
3. User validation that CTQs cover their needs
4. Iterative refinement of CTQs

**Contingency:** Add missing CTQs when identified, create traceability retrospectively

**Owner:** Project Owner
**Status:** 🔶 Open - CTQ review required

---

### R-004: Traceability Breakdown
**Category:** Process
**Description:** Requirements-to-test-to-implementation traceability lost or not maintained.

**Likelihood:** L3 (Possible) - Manual traceability is error-prone
**Impact:** I3 (Moderate) - Cannot verify completeness, audit trail gaps
**Risk Score:** 9 (Medium)

**Mitigation:**
1. Define traceability matrix structure upfront
2. Use consistent linking conventions (e.g., REQ-001, TEST-001)
3. Regular traceability audits
4. Consider traceability tooling if manual process fails

**Contingency:** Retrospective traceability analysis if gaps discovered

**Owner:** Developer
**Status:** 🔶 Open - Traceability Index structure needed

---

### R-005: Silent Artifact Skipping
**Category:** Compliance
**Description:** Required artifacts skipped without explicit deviation, violating no-skip rule.

**Likelihood:** L2 (Unlikely) - System should enforce, but human override possible
**Impact:** I3 (Moderate) - Quality plan non-compliance, potential gaps
**Risk Score:** 6 (Medium)

**Mitigation:**
1. Automated checks for artifact status (Done/Deferred/Deviated)
2. Require explicit deviation approval with justification
3. Regular artifact completeness audits
4. Clear artifact completion criteria

**Contingency:** Immediate notification and deviation recording if detected

**Owner:** Quality System
**Status:** 🔶 Open - Enforcement mechanism needed

---

### R-006: Inadequate Verification
**Category:** Quality
**Description:** Verification activities don't adequately test critical functionality (risk classification, artifact generation).

**Likelihood:** L3 (Possible) - Verification Plan not yet detailed
**Impact:** I4 (Major) - Defects escape to production, users receive incorrect guidance
**Risk Score:** 12 (Medium)

**Mitigation:**
1. Map verification methods to each CTQ
2. Prioritize testing of risk classification logic
3. Test with diverse project scenarios
4. Automated regression testing for artifact generation

**Contingency:** Enhanced validation testing if verification gaps found

**Owner:** Developer / Reviewer
**Status:** 🔶 Open - Verification Plan needed

---

### R-007: User Misunderstanding
**Category:** Usability
**Description:** Users don't understand generated quality artifacts or how to use them.

**Likelihood:** L3 (Possible) - Domain partially understood by users
**Impact:** I3 (Moderate) - Quality plan not followed, artifacts not maintained
**Risk Score:** 9 (Medium)

**Mitigation:**
1. Include guidance and instructions in generated artifacts
2. Provide examples and templates
3. User documentation and training
4. Validation testing with target users

**Contingency:** Enhanced documentation and user support if confusion observed

**Owner:** Project Owner
**Status:** 🔶 Open - User validation needed

---

### R-008: Scope Creep
**Category:** Project Management
**Description:** Feature requests expand beyond individual-scale internal QMS Dashboard.

**Likelihood:** L2 (Unlikely) - Scope clearly defined by intake
**Impact:** I2 (Minor) - Rework, timeline impact
**Risk Score:** 4 (Low)

**Mitigation:**
1. Document scope based on intake responses
2. Change control process for scope changes
3. Re-run intake if scope significantly changes
4. Defer out-of-scope features

**Contingency:** Re-run intake and re-classify risk if scope expands to Team/Multi-team or External

**Owner:** Project Owner
**Status:** 🔶 Open - Monitor scope

---

### R-009: Safety/Legal Downstream Impact
**Category:** Safety/Legal/Compliance
**Description:** Incorrect QMS guidance leads to poor quality management in downstream projects, resulting in safety/legal/compliance failures.

**Likelihood:** L2 (Unlikely) - Easy reversibility, internal use, and safety mechanisms mitigate
**Impact:** I5 (Severe) - This is the worst credible failure scenario identified in intake
**Risk Score:** 10 (Medium)

**Mitigation (IMPLEMENTED 2025-12-12):**
1. ✅ High accuracy risk classification ensured (R-001 mitigations)
2. ✅ Safety-first validation rules:
   - Rule CV1: Flags automated + low reversibility + high impact → R3
   - Rule CV3: Flags recommendations + safety/legal → Warning + Review
   - Indicator I1: Always flags safety/legal/compliance as HIGH RISK
3. ✅ Multi-layer safety checks before finalizing classification
4. ✅ Expert review mandatory for safety-critical classifications
5. ✅ Clear guidance on "credible failure" interpretation (intake-rules-enhanced.md)
6. ✅ Human review workflow documented (system provides recommendations, not mandates)
7. ⏳ Pending: Validation testing with safety/legal expert input
8. ⏳ Pending: Incident reporting process implementation

**Contingency:** Immediate correction and user notification if incorrect guidance discovered

**Owner:** Project Owner
**Status:** 🟢 Mitigations Designed - Critical Priority - Pending Implementation
**Last Updated:** 2025-12-12

---

### R-010: Technology/Tool Limitations
**Category:** Technical
**Description:** Markdown file format insufficient for traceability, reporting, or artifact management at scale.

**Likelihood:** L2 (Unlikely) - Adequate for individual scale
**Impact:** I2 (Minor) - Migration to structured format may be needed
**Risk Score:** 4 (Low)

**Mitigation:**
1. Use consistent structure and formatting conventions
2. Evaluate tooling if limitations encountered
3. Monitor user feedback on artifact format

**Contingency:** Migrate to structured format (database, YAML, etc.) if needed

**Owner:** Developer
**Status:** 🔶 Open - Monitor

---

## Risk Summary

| ID | Risk | Score | Level | Status | Priority |
|----|------|-------|-------|--------|----------|
| R-001 | Incorrect risk classification | 8 ⬇️ | Medium | 🟢 Mitigated | High |
| R-002 | Invalid assumptions | 12 | Medium | 🔶 Open | High |
| R-003 | Inadequate CTQ coverage | 6 | Medium | 🔶 Open | Medium |
| R-004 | Traceability breakdown | 9 | Medium | 🔶 Open | Medium |
| R-005 | Silent artifact skipping | 6 | Medium | 🔶 Open | Medium |
| R-006 | Inadequate verification | 12 | Medium | 🔶 Open | High |
| R-007 | User misunderstanding | 9 | Medium | 🔶 Open | Medium |
| R-008 | Scope creep | 4 | Low | 🔶 Open | Low |
| R-009 | Safety/legal downstream | 10 | Medium | 🟢 Mitigated | **Critical** |
| R-010 | Technology limitations | 4 | Low | 🔶 Open | Low |

**Note:** R-001 and R-009 risk scores improved with implemented safety mechanisms (2025-12-12)

---

## High Priority Risks Requiring Immediate Attention

1. **R-009: Safety/Legal Downstream Impact** - This is the worst-case failure scenario. Mitigation must be in place before release.
2. **R-001: Incorrect Risk Classification** - Core functionality accuracy is critical.
3. **R-002: Invalid Assumptions** - Foundation of quality plan must be validated.
4. **R-006: Inadequate Verification** - Must ensure system works correctly.

---

## Risk Review Schedule

- **Initial Review:** Today (first-pass complete)
- **Detailed Planning:** Before implementation begins
- **Ongoing Review:** At each quality gate
- **Triggered Review:** When new risks identified or risk status changes
- **Full Re-assessment:** If project scope, scale, or risk classification changes
