# Expert Review and Override Mechanism
## Quality Assurance for Risk Classification

**Date:** 2025-12-12
**Purpose:** Define expert review process and override workflow for intake classifications
**Mitigates:** R-001 (Incorrect risk classification), R-009 (Safety/legal downstream impact)
**Supports:** CTQ-1.1 (Risk classification accuracy)

---

## Overview

The expert review mechanism provides a safety net when:
- Automated classification may be incorrect
- User is uncertain about answers
- Contradictions or edge cases detected
- Safety-critical projects need validation

**Key Principle:** Expert review is **additional validation**, not replacement for intake process.

---

## When Expert Review is Triggered

### Mandatory Expert Review (System Blocks Until Review)
1. **Multiple critical safety indicators** (2+ CRITICAL warnings)
2. **Contradictory answers** (logical inconsistencies detected)
3. **User indicates uncertainty** ("I don't know" selected)
4. **Override to lower risk** (R3→R2 or R2→R1 requires approval)

### Recommended Expert Review (User Can Proceed But Warned)
5. **Borderline classification** (Low confidence, multiple possibilities)
6. **Safety/legal + R2 classification** (Could be R3, needs justification)
7. **3+ medium-high risk indicators** (Pattern suggests higher risk)
8. **User requests review** (Always honor user uncertainty)

---

## Expert Review Workflow

```
                    Intake Completed
                           ↓
              [Validation & Classification]
                           ↓
            ┌──────────────┴──────────────┐
            │                              │
     No Triggers                    Expert Review Triggered
            │                              │
            ↓                              ↓
    Display Classification         [Mandatory or Recommended?]
            │                              │
            ↓                    ┌─────────┴─────────┐
    User Approves               Mandatory         Recommended
            │                    │                    │
            ↓                    ↓                    ↓
    Generate Artifacts      Block & Notify      Warn & Allow Continue
                                 │                    │
                                 ↓                    │
                         Expert Reviews         ┌────┴────┐
                                 │              │         │
                    ┌────────────┴────────┐   Skip    Request
                Approve            Override  Review   Review
                    │                │       │         │
                    ↓                ↓       ↓         ↓
            User Notified      New Risk  Continue  [Expert Reviews]
                    │          Assigned     │         │
                    └────────────┬──────────┘         │
                                 ↓                    ↓
                         Generate Artifacts     [Same as Approve/Override]
```

---

## Expert Reviewer Qualifications

### Minimum Qualifications
- Experience with QMS or quality management systems
- Understanding of software risk assessment
- Familiarity with regulatory standards (ISO, IEC, FDA, etc.) if applicable
- Authority to approve deviations

### Designated Reviewers (by Project Type)
| Project Type | Recommended Reviewer |
|-------------|---------------------|
| Safety-critical | Quality Engineer + Domain Expert |
| Regulated | Compliance Officer + QMS Expert |
| Financial systems | Security + Risk Management |
| General software | Senior Engineer + QMS Lead |
| Prototype/Research | Tech Lead + Project Sponsor |

---

## Expert Review Process

### Step 1: Review Request Notification

**Information Provided to Expert:**
```
Expert Review Request
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: [Project Name]
Requested by: [User Name]
Date: [Timestamp]
Review Type: [Mandatory | Recommended]

Intake Answers:
  Q1: Users → [Answer]
  Q2: Decisions/Actions → [Answer]
  Q3: Worst Credible Failure → [Answer]
  Q4: Reversibility → [Answer]
  Q5: Domain Understanding → [Answer]
  Q6: Scale → [Answer]
  Q7: Regulated → [Answer]

Calculated Classification: R[X]
Confidence: [HIGH | MEDIUM | LOW]

Validation Results:
  ⚠️ [List all warnings triggered]
  🔶 [List all indicators flagged]

Expert Review Triggers:
  • [Reason 1]
  • [Reason 2]

User Comment (if provided):
  "[User can optionally explain uncertainty]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Expert Actions:
[Approve Classification]  [Override with Justification]  [Request More Info]
```

### Step 2: Expert Analysis

**Review Checklist:**
- [ ] Do intake answers accurately reflect project reality?
- [ ] Is calculated classification appropriate for described project?
- [ ] Are there factors not captured by intake questions?
- [ ] Do contradictions indicate user misunderstanding or system limitation?
- [ ] What is the actual worst credible failure scenario?
- [ ] Is domain-specific knowledge needed (medical, financial, safety)?
- [ ] Are there regulatory or compliance factors?
- [ ] Should rigor be increased or decreased?

**Expert Consideration Questions:**
1. **If this system fails, what is the realistic worst case?**
2. **Are users qualified to implement quality at the calculated rigor level?**
3. **Does the classification match similar projects we've done?**
4. **Are there organizational standards or policies that override?**
5. **Is this a known edge case in the intake framework?**

### Step 3: Expert Decision

**Option A: Approve Classification**
```
Expert Approval
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Classification: R[X] ✅ APPROVED
Reviewed by: [Expert Name]
Date: [Timestamp]

Expert Comments:
[Optional: Expert can add notes about rationale, considerations, or recommendations]

This classification is appropriate for the described project.

[Confirm Approval]
```

**Option B: Override Classification**
```
Classification Override
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From: R[Original] → To: R[New]
Reviewed by: [Expert Name]
Date: [Timestamp]

Justification (Required):
┌────────────────────────────────────────┐
│ [Expert must provide detailed          │
│  explanation of why calculated         │
│  classification is incorrect and       │
│  why new classification is appropriate]│
└────────────────────────────────────────┘

Intake Questions Misrepresenting Reality:
  ☐ Q1: [If checked, explain discrepancy]
  ☐ Q2: [If checked, explain discrepancy]
  ☐ Q3: [If checked, explain discrepancy]
  ☐ Q4: [If checked, explain discrepancy]
  ☐ Q5: [If checked, explain discrepancy]
  ☐ Q6: [If checked, explain discrepancy]
  ☐ Q7: [If checked, explain discrepancy]

Additional Factors Considered:
  [Factors not captured by intake, e.g., organizational policy,
   domain-specific requirements, regulatory interpretation]

Risks Accepted by Downgrade (if lowering risk):
  [If R3→R2 or R2→R1, list risks being accepted]

[Confirm Override]  [Cancel]
```

**Option C: Request More Information**
```
Information Request
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Expert needs clarification before approving classification.

Questions for User:
┌────────────────────────────────────────┐
│ [Expert asks specific questions]       │
│                                        │
│ Examples:                              │
│ - Can you describe a realistic         │
│   failure scenario?                    │
│ - How will users verify the system's   │
│   recommendations?                     │
│ - What safeguards exist against        │
│   worst-case failures?                 │
└────────────────────────────────────────┘

[Send to User]
```

### Step 4: Documentation

All expert reviews are logged:

```markdown
### Expert Review Log Entry

**Review ID:** ER-[YYYYMMDD]-[NNN]
**Date:** [Timestamp]
**Project:** [Project Name]
**Intake ID:** [Intake UUID]

**Reviewer:** [Expert Name]
**Reviewer Qualifications:** [Role / Expertise]

**Review Type:** [Mandatory | Recommended]
**Triggers:** [List of trigger IDs that caused review]

**Original Classification:** R[X] (Confidence: [Level])
**Expert Decision:** [Approved | Overridden to R[Y]]

**Justification:**
[Expert's detailed explanation]

**Intake Discrepancies Identified:**
[List any questions where answers didn't reflect reality]

**Additional Considerations:**
[Domain factors, organizational policies, etc.]

**Outcome:** [User notified, classification finalized]
**Artifacts Generated:** [List of artifact files created]

**Logged to:** QMS-Change-Log.md, Expert-Review-Log.md
```

---

## User-Initiated Override (Without Expert)

### When Allowed
- User disagrees with calculated classification
- User has domain knowledge system doesn't capture
- User accepts responsibility for classification accuracy

### Override Requirements

**For Lower Risk (Downgrade):**
- ❌ R3→R2 or R2→R1: **NOT ALLOWED** without expert approval
- Requires: Deviation approval per intake-rules.md:66
- Must go through expert review workflow

**For Higher Risk (Upgrade):**
- ✅ R0→R1, R1→R2, R2→R3: **ALLOWED** with justification
- User providing more conservative classification (safer)

### Upgrade Override Workflow

```
User Disagrees with R[X]
         ↓
    Requests R[Y] (where Y > X)
         ↓
System Asks: "Why do you believe higher risk is appropriate?"
         ↓
User Provides Justification:
  ┌─────────────────────────────────────┐
  │ [Free text explanation]              │
  │                                      │
  │ Example:                             │
  │ "Although intake suggests R1,        │
  │  this system will eventually         │
  │  interface with safety-critical      │
  │  medical devices. I want R2 rigor    │
  │  to ensure proper validation."       │
  └─────────────────────────────────────┘
         ↓
    Override Logged
         ↓
Generate R[Y] Artifacts
```

### Override Documentation

```markdown
### User Override (Upgrade)

**Override ID:** UO-[YYYYMMDD]-[NNN]
**Date:** [Timestamp]
**Project:** [Project Name]

**Calculated Classification:** R[X]
**User Override:** R[Y] (Upgrade)

**User Justification:**
[User's explanation]

**Approved:** Self-approved (upgrade is conservative choice)
**Logged to:** QMS-Change-Log.md
```

---

## Override Rejection (Downgrade Attempt)

```
Override Request Denied
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You requested: R3 → R2 (Downgrade)

🛑 DOWNGRADE REQUIRES EXPERT APPROVAL

Per intake-rules.md:66: "Any downgrade requires a deviation record."

Downgrades are not permitted without expert review because:
• R3/R2 classification is based on safety/impact assessment
• Lowering quality rigor accepts additional risk
• Deviation must be formally approved and justified

To proceed with downgrade:
1. Request expert review
2. Expert evaluates appropriateness
3. If approved, expert creates deviation record
4. Justification logged in CAPA Log

[Request Expert Review]  [Cancel - Keep R3]
```

---

## Expert Review SLA (Service Level Agreement)

| Review Type | Response Time | Max Wait Time |
|------------|--------------|---------------|
| Mandatory (Safety-critical) | 2 business hours | 8 business hours |
| Mandatory (Other) | 1 business day | 3 business days |
| Recommended | 2 business days | 1 week |
| Downgrade request | 1 business day | 3 business days |

**If SLA exceeded:** Escalate to QMS Lead or Project Sponsor

---

## Expert Review Metrics

Track expert review effectiveness:

**Metrics to Monitor:**
- **Review Request Rate:** % of intakes requiring expert review
- **Override Rate:** % of reviews resulting in override
- **Override Direction:** How many upgrades vs. downgrades?
- **Review Turnaround Time:** Average time from request to decision
- **User Satisfaction:** Do users find expert review helpful?
- **Misclassification Prevention:** Did expert review catch incorrect classifications?

**Target Metrics:**
- Review request rate: <20% (intake should handle most cases)
- Override rate: <30% of reviews (system generally correct)
- Review turnaround: Meet SLA 95% of time
- Misclassification prevention: 100% (no misclassifications escape expert review)

---

## Edge Cases and Special Situations

### Case 1: Prototype Becoming Production
**Scenario:** User answers for prototype (R0), but system will become production (R2+)

**Expert Guidance:**
- Classify for **end state**, not current state
- If uncertain, start with higher risk and downgrade later with explicit decision
- Consider phased approach: R1 for prototype, R2 for production deployment

### Case 2: Organizational Policy Override
**Scenario:** Organization requires R2+ for all customer-facing systems, regardless of intake

**Expert Action:**
- Override classification with justification: "Organizational policy requires R2 minimum for customer-facing systems"
- Document policy reference
- Approve override

### Case 3: Domain Expert Disagrees
**Scenario:** Domain expert (e.g., medical device specialist) believes intake doesn't capture domain-specific risks

**Expert Action:**
- Defer to domain expert for specialized domains
- Document domain-specific factors
- Consider updating intake questions for future use

### Case 4: Unclear Intake Questions
**Scenario:** User and expert both unclear on what a question means

**Expert Action:**
- Document unclear question as improvement opportunity
- Make best judgment based on project reality
- Flag for intake question revision (log in CAPA)

---

## Integration with QMS Artifacts

### Change Log
Every expert review and override is logged in QMS-Change-Log.md

### CAPA Log
- Misclassifications identified through expert review → CAPA entry
- Intake question confusion → Preventive action to clarify question

### Risk Register
- New risks identified during expert review → Added to Risk Register
- Risk mitigation effectiveness evaluated

### Assumptions Register
- Expert review validates or invalidates assumptions

---

## Training for Expert Reviewers

### Required Training Topics
1. Intake question interpretation
2. Risk classification logic (R0-R3)
3. Safety and compliance considerations
4. Regulatory standards (if applicable)
5. Override justification requirements
6. Documentation and traceability

### Training Materials
- intake-rules-enhanced.md (full guidance)
- intake-safety-mechanisms.md (validation rules)
- Example review cases (good and bad)
- Domain-specific standards (ISO, IEC, FDA, etc.)

---

## Success Criteria

✅ Expert review process implemented and documented
✅ Expert review triggers correctly identify edge cases
✅ All overrides have documented justification
✅ SLA met for 95%+ of reviews
✅ Misclassification rate reduced to near-zero
✅ User confidence in classification improves

---

**Version:** 1.0
**Owner:** Project Owner
**Related Documents:**
- intake-safety-mechanisms.md (triggers)
- intake-validation-spec.md (implementation)
- intake-rules-enhanced.md (user guidance)
- QMS-Risk-Register.md (R-001, R-009)
