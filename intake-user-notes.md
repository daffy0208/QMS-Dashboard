# Intake User Notes
## Background Information (Optional Reading)

**Purpose:** This document provides background information about how the intake system works. Users do NOT need to read this—it's purely informational for those curious about the safety mechanisms and validation logic.

**For users:** Start with intake-user.md (the front door)
**For implementers:** See intake-validation-spec.md
**For detailed guidance:** See intake-rules-enhanced.md

---

## How the Intake System Works

### User Journey

1. **User reads** intake-user.md (simple, 7 questions)
2. **User answers** questions with inline examples as needed
3. **System validates** answers automatically (behind the scenes)
4. **User sees** results:
   - ✅ Classification if everything looks good
   - ⚠️ Warnings if something seems contradictory
   - 🔍 Expert review request if needed
5. **User approves** quality plan
6. **Development begins** with appropriate quality rigor

---

## Risk Levels Explained

The system classifies projects into 4 risk levels:

### R0 (Low Risk) - Advisory Rigor
**Typical projects:**
- Internal, individual use
- Informational only
- Worst case: minor annoyance
- Easy to reverse
- Well-understood domain

**Quality activities:** 5 baseline artifacts, advisory guidance

**Example:** Personal automation script, simple team dashboard

---

### R1 (Medium-Low Risk) - Conditional Rigor
**Typical projects:**
- Internal, team/multi-team use
- Recommendations or moderate impact
- Worst case: financial loss or reputation damage (moderate)
- Partially reversible
- Domain partially understood

**Quality activities:** 8 artifacts (baseline + 3 more)

**Example:** Internal service, department tool with business impact

---

### R2 (Medium-High Risk) - Strict Rigor
**Typical projects:**
- External users OR
- Decision-impacting (recommendations heavily relied upon) OR
- Possibly regulated/auditable
- Worst case: financial loss, reputational damage, or potential safety/legal issues (with mitigation)

**Quality activities:** 11 artifacts (comprehensive)

**Example:** Customer-facing product, B2B platform, QMS Dashboard

---

### R3 (High Risk) - Strict Rigor (No Downgrade)
**Typical projects:**
- Safety/legal/compliance worst case OR
- Hard-to-reverse consequences OR
- Automated actions with high impact OR
- Formally regulated

**Quality activities:** 11 artifacts (comprehensive, no exceptions)

**Example:** Medical device software, financial trading, safety-critical systems

---

## Validation Layers (Behind the Scenes)

When you submit your answers, the system automatically applies 6 layers of validation:

### Layer 1: Input Validation
- Ensures all 7 questions are answered
- Verifies valid option selections
- No blank or invalid responses

### Layer 2: Cross-Validation
Detects logical contradictions in your answers:

**Rule CV1: Automated + High Impact**
- Flags: Automated actions + Low reversibility + High impact
- Warning: "This typically requires R3 classification"

**Rule CV2: Informational Contradiction**
- Flags: "Informational only" but "Hard to reverse"
- Warning: "Informational failures should be easy to reverse"

**Rule CV3: Recommendations + Safety**
- Flags: Recommendations with safety/legal consequences
- Warning: "Consider carefully—incorrect recommendations can cause harm"

**Rule CV4: Internal + Public Scale**
- Flags: "Internal users" but "Organization-wide/public scale"
- Warning: "Please clarify—these seem contradictory"

**Rule CV5: Unregulated Safety**
- Flags: Not regulated but safety/legal worst case
- Info: "Safety-critical systems often face regulatory requirements"

### Layer 3: Risk Indicators
Pattern detection for high-risk scenarios:

**Indicator I1: Safety/Legal/Compliance 🔴**
- Always flags safety/legal/compliance as HIGH RISK
- Shows R3 requirements
- Requires justification if classified lower

**Indicator I2: Financial at Scale 🔶**
- Flags financial losses at large scale
- Prompts consideration of impact magnitude

**Indicator I3: Partial Reversibility + High Impact 🔶**
- Flags "partial reversibility" with serious consequences
- Clarifies difference between fixing code vs. fixing damage

**Indicator I4: Domain Uncertainty + High Stakes 🔶**
- Flags poorly understood domains with high-impact failures
- Recommends extra validation, expert consultation

### Layer 4: Warnings & Confirmations
For critical warnings, the system:
- Shows detailed warning message
- Explains why it's flagged
- Requires user acknowledgment
- Provides recommendations

User must explicitly acknowledge warnings before proceeding.

### Layer 5: Expert Review Triggers
The system automatically triggers expert review when:

**Mandatory triggers:**
- 2+ CRITICAL warnings detected
- Contradictory answers (logical inconsistencies)
- User indicates uncertainty ("I don't know")
- Downgrade request (R3→R2 or R2→R1)

**Recommended triggers:**
- Borderline classification (could be R2 or R3)
- Safety/legal worst case with R2 classification
- 3+ medium-high risk indicators
- User requests review

### Layer 6: Override & Justification
Two types of overrides:

**Upgrade (Allowed):**
- User wants higher risk level (more conservative)
- Requires justification but no approval
- Example: R1→R2 "Plan to expand to external users"

**Downgrade (Requires Approval):**
- User wants lower risk level
- BLOCKED without expert approval
- Requires formal deviation record
- Example: R3→R2 requires expert review and sign-off

---

## Expert Review Process

### When It Happens
- System flags for mandatory review → Process blocked until review
- System recommends review → User can proceed or wait for review
- User requests review → Always honored

### What Experts Do
1. Review intake answers
2. Assess if answers reflect reality
3. Consider domain-specific factors
4. Approve classification OR override with justification

### Timeline
- Safety-critical (mandatory): 2-8 business hours
- Other mandatory: 1-3 business days
- Recommended: 2 days to 1 week

### Outcome
- **Approved:** User proceeds with calculated classification
- **Overridden:** Expert assigns different risk level with documented justification
- **More info needed:** Expert asks clarifying questions

---

## Why These Safety Mechanisms?

### Problem They Solve

**Risk R-001: Incorrect Risk Classification**
- Issue: User misunderstands questions → wrong risk level → inappropriate quality plan
- Solution: Cross-validation, risk indicators, expert review catch errors

**Risk R-009: Safety/Legal Downstream Impact**
- Issue: QMS Dashboard gives wrong guidance → downstream project has safety issues
- Solution: Safety-first indicators, mandatory review for safety-critical cases

**Risk R-007: User Misunderstanding**
- Issue: Users don't understand guidance or requirements
- Solution: Plain language, examples, warnings explain "why"

### How They Work Together

```
User Answer → Validation Layers → Classification Result
                    ↓
            Warnings if needed
                    ↓
         Expert review if needed
                    ↓
          Approved classification
                    ↓
          Quality plan generated
```

Each layer catches different types of errors:
- Layer 1-2: Basic mistakes
- Layer 3-4: Pattern-based risks
- Layer 5-6: Edge cases and overrides

---

## Classification Logic (Simplified)

### R3 Triggers (Highest Priority)
- Q3 = "Safety/legal/compliance" AND (Q2 = "Automated" OR Q4 = "Hard/irreversible")
- Q7 = "Yes" (formally regulated)
- Q3 = "Safety/legal/compliance" (with some exceptions if heavily mitigated)

### R2 Triggers
- Q1 = "External" or "Public"
- Q2 = "Automated" (with non-trivial impact)
- Q7 = "Possibly" (possibly regulated)
- Q2 = "Recommendations" + Q3 = "Safety/legal/financial/reputational"
- Q6 = "Organization-wide/public" (with non-trivial impact)

### R1 Triggers
- Q2 = "Recommendations" + Q3 = "Annoyance"
- Q3 = "Financial/Reputational" + Internal + Reversible
- Q6 = "Team/Multi-team" (with moderate impact)

### R0 Triggers
- Q3 = "Annoyance" + Q4 = "Easy" + Q1 = "Internal" + Q6 = "Individual/Team"

**Rule:** If uncertain or borderline → Select higher risk

---

## Common Scenarios

### Scenario 1: "It's Just a Prototype"
**User thinking:** "R0—it's just testing"
**Reality check:** Does it affect real decisions or data?
- If YES → At least R1, possibly R2
- If prototype will become production → Classify for end state

**System helps:** Asks about scale (Q6) and influence (Q2)

---

### Scenario 2: "Informational Dashboard"
**User thinking:** "R0—we just show data"
**Reality check:** Do users make decisions based on this data?
- If users trust the data without verification → R1 or R2
- If wrong data causes harm → Consider impact level

**System helps:** Q2 key question: "Would people notice before acting?"

---

### Scenario 3: "Internal but Safety-Critical"
**User thinking:** "R1—internal use, small team"
**Reality check:** What's the worst credible failure?
- If Q3 = "Safety/legal/compliance" → Usually R2 or R3
- Internal doesn't automatically mean low risk

**System helps:** I1 indicator flags all safety/legal cases

---

### Scenario 4: "Recommendations for Safety Decisions"
**User thinking:** "R1—humans make final decisions"
**Reality check:** Do users have independent verification?
- If users heavily rely on recommendations → R2
- If recommendations affect safety → Consider R3

**System helps:** CV3 rule flags this exact combination

---

## Tips for Accurate Classification

### Do:
✅ Think about what COULD happen (realistic worst case)
✅ Consider indirect consequences (wrong info → bad decisions → harm)
✅ Plan for end state (production), not current state (prototype)
✅ Choose higher risk when uncertain
✅ Request expert review if unsure
✅ Be honest about domain knowledge gaps

### Don't:
❌ Downplay risks to avoid quality work
❌ Think "it's just a prototype" if it affects real decisions
❌ Confuse "fixing the bug" with "fixing the consequences"
❌ Ignore indirect failures (system → user decisions → outcomes)
❌ Assume internal = low risk automatically
❌ Skip details in the examples

---

## Why Plain Language Matters

The intake questions use plain language instead of QMS terminology:

| QMS Term | Plain Language |
|----------|----------------|
| "Stakeholders" | "Users" |
| "Impact assessment" | "What's the worst that could happen?" |
| "Mitigation capability" | "How easily can failures be fixed?" |
| "Domain maturity" | "Do you understand the problem?" |
| "Deployment scope" | "How many people will use this?" |
| "Regulatory compliance" | "Is this project regulated?" |

**Why:** Users shouldn't need QMS expertise to get accurate classification.

---

## Success Metrics

The intake system targets:

**M-001: Risk Classification Accuracy**
- Target: ≥95% accuracy in production
- Mechanism: 6-layer validation catches misclassification

**M-006: Intake Completion Time**
- Target: <10 minutes average
- Mechanism: Minimal format, progressive disclosure

**M-007: User Comprehension**
- Target: >90% correctly understand classification
- Mechanism: Plain language, examples, inline help

**CTQ-1.1: Risk Classification Accuracy**
- Target: 100% correct risk classification
- Mechanism: Automated validation + expert review

**CTQ-3.2: Guidance Clarity**
- Target: >90% comprehension
- Mechanism: Plain language, examples, warnings

---

## Related Documents

**For users:**
- **intake-user.md** - Start here (7 questions, minimal)
- **intake-rules-enhanced.md** - Detailed guidance with comprehensive examples

**For experts:**
- **intake-expert-review.md** - Expert review process and workflow
- **intake-safety-mechanisms.md** - 6-layer validation system design

**For implementers:**
- **intake-validation-spec.md** - Implementation specification with code
- **intake-analysis.md** - Issue analysis and improvement rationale

---

## Questions?

**"Why so many validation layers?"**
Defense in depth. Each layer catches different error types. Redundancy prevents misclassification.

**"Can I skip expert review?"**
If mandatory: No. If recommended: Yes, but not advised for borderline cases.

**"What if I disagree with classification?"**
You can override to higher risk (safer) anytime. Lower risk requires expert approval.

**"Why can't I downgrade without approval?"**
Downgrades accept more risk. Expert verification ensures appropriate safety.

**"How accurate is the automated classification?"**
Target: 95%+. The 6-layer system catches most errors before they affect your project.

**"What if my project changes?"**
Re-run intake anytime. Requirements change → Risk changes → Quality plan updates.

---

**This document is informational only. Users do not need to read it.**

**Version:** 1.0
**Date:** 2025-12-12
**Related:** intake-user.md v1.0 (minimal front door)
