# Intake Safety Mechanisms
## Risk Misclassification Prevention

**Date:** 2025-12-12
**Purpose:** Define validation rules, warnings, and safety mechanisms to prevent risk misclassification
**Mitigates:** R-001 (Incorrect risk classification), R-009 (Safety/legal downstream impact)
**Supports:** CTQ-1.1 (Risk classification accuracy), CTQ-3.2 (User comprehension)

---

## Safety Mechanism Layers

```
Layer 1: Input Validation (prevent invalid answers)
    ↓
Layer 2: Cross-Validation (detect contradictions)
    ↓
Layer 3: Risk Indicators (flag high-risk patterns)
    ↓
Layer 4: Warnings & Confirmations (force user acknowledgment)
    ↓
Layer 5: Expert Review Triggers (escalate edge cases)
    ↓
Layer 6: Override & Justification (allow expert override with documentation)
```

---

## Layer 1: Input Validation Rules

### Rule V1: All Questions Required
**Trigger:** User attempts to submit without answering all 7 questions
**Action:** Block submission, highlight unanswered questions
**Message:** "All 7 intake questions must be answered to classify project risk."

### Rule V2: Single Selection Enforced
**Trigger:** User selects multiple options for single-choice questions
**Action:** Only allow one selection
**Message:** N/A (enforced by UI/input method)

### Rule V3: No "Skip" or "N/A"
**Trigger:** User attempts to skip question or select "N/A" / "Don't know" without acknowledgment
**Action:** If "Don't know" option exists, trigger Expert Review flag (Layer 5)
**Message:** "Unable to answer? This will be flagged for expert review."

---

## Layer 2: Cross-Validation Rules (Detect Contradictions)

### Rule CV1: Automated Actions + Low Reversibility + High Impact = Flag
**Trigger:**
- Q2 = "Automated actions" AND
- Q4 = "Hard/irreversible" OR Q4 = "Partial" AND
- Q3 = "Safety/legal/compliance" OR "Financial loss" OR "Reputational damage"

**Action:** ⚠️ WARNING + Auto-escalate to R3 consideration
**Message:**
```
⚠️ SAFETY WARNING: Automated actions with low reversibility and high impact
typically require R3 (Strict rigor, no downgrade).

Your answers indicate:
- System takes automated actions (Q2)
- Failures are difficult to reverse (Q4)
- Worst case involves [safety/legal/financial] consequences (Q3)

Recommended Risk Level: R3
Proceed with caution if classifying lower than R3.
```

### Rule CV2: Informational + Hard to Reverse = Contradiction
**Trigger:**
- Q2 = "Informational only" AND
- Q4 = "Hard/irreversible"

**Action:** ⚠️ CONTRADICTION WARNING
**Message:**
```
⚠️ POSSIBLE CONTRADICTION DETECTED

You indicated:
- System is "Informational only" (Q2)
- But failures are "Hard to reverse" (Q4)

If the system only provides information, failures should be easy to reverse
(fix bug, show correct data). Hard-to-reverse failures suggest the system
influences decisions or actions.

Please review:
- Q2: Does the system influence decisions or actions based on the information?
- Q4: Are you considering consequences of wrong information, not just fixing the bug?
```

### Rule CV3: Recommendations + Safety/Legal = R3 Consideration
**Trigger:**
- Q2 = "Recommendations" AND
- Q3 = "Safety/legal/compliance"

**Action:** ⚠️ WARNING + Flag for review
**Message:**
```
⚠️ SAFETY CONSIDERATION

Your system provides recommendations (Q2) that could lead to safety/legal/compliance
failures (Q3). Even though humans make final decisions, incorrect recommendations can
cause serious harm.

Questions to consider:
- Will users have independent way to verify recommendations?
- What happens if users trust incorrect recommendations?
- Can users easily detect when recommendations are wrong?

If recommendations are heavily relied upon for safety-critical decisions:
→ Consider R3 classification

Current classification: [R2 or R3 based on other factors]
```

### Rule CV4: Internal + Public Scale = Contradiction
**Trigger:**
- Q1 = "Internal" AND
- Q6 = "Organization-wide/public"

**Action:** ⚠️ CLARIFICATION NEEDED
**Message:**
```
⚠️ CLARIFICATION NEEDED

You selected:
- Users: Internal (Q1)
- Scale: Organization-wide/public (Q6)

"Organization-wide/public" typically implies external users. Please clarify:
- Internal organization-wide → Select Q6="Multi-team", Q1="Internal"
- Public users → Select Q1="Public", Q6="Organization-wide/public"
```

### Rule CV5: Not Regulated + Safety Worst Case = Review
**Trigger:**
- Q7 = "No" (not regulated) AND
- Q3 = "Safety/legal/compliance"

**Action:** 💡 INFORMATION + Optional expert review
**Message:**
```
💡 REGULATORY CONSIDERATION

You indicated:
- Worst failure: Safety/legal/compliance (Q3)
- Not regulated: No (Q7)

Note: Systems with safety/legal worst cases are often subject to:
- Industry standards (ISO, IEC, FDA, etc.)
- Internal compliance requirements
- Legal liability even without formal regulation

Consider:
- Could this system face future regulation?
- Are there industry standards that apply?
- Should we treat it as regulated for quality purposes?

Current classification: [R2 or R3 based on answers]
Consider answering Q7="Possibly" if uncertain.
```

---

## Layer 3: Risk Indicators (Pattern Detection)

### Indicator I1: Safety/Legal/Compliance Mentioned → Always Flag
**Trigger:** Q3 = "Safety/legal/compliance"
**Action:** 🔴 HIGH RISK INDICATOR + Show R3 requirements
**Message:**
```
🔴 HIGH RISK INDICATOR DETECTED

Worst credible failure involves SAFETY / LEGAL / COMPLIANCE consequences.

Per intake-rules.md, R3 classification is for:
"Safety, legal, financial, or hard-to-reverse consequences"

Your R3 classification triggers:
- Strict rigor mode (no downgrade allowed)
- 11 quality artifacts required
- All verification and validation activities mandatory
- No artifact may be skipped without formal deviation approval

Current tentative classification: [R2 or R3]

⚠️ If classified as R2: Please justify why safety/legal/compliance risk does not warrant R3.
```

### Indicator I2: Financial Loss + Significant Scale → Flag
**Trigger:**
- Q3 = "Financial loss" AND
- Q6 = "Multi-team" OR "Organization-wide/public"

**Action:** 🔶 MEDIUM-HIGH RISK INDICATOR
**Message:**
```
🔶 FINANCIAL RISK AT SCALE

Worst failure: Financial loss (Q3)
Scale: [Multi-team / Organization-wide] (Q6)

Financial losses at scale can be significant. Consider:
- What is the potential financial impact? (>$10K, >$100K, >$1M?)
- Is this customer money or company money?
- Could financial loss lead to legal liability?

If potential loss is substantial → Consider R3 classification
```

### Indicator I3: Partial Reversibility + High Impact → Flag
**Trigger:**
- Q4 = "Partial" AND
- Q3 = "Safety/legal/compliance" OR "Financial loss" OR "Reputational damage"

**Action:** 🔶 MEDIUM-HIGH RISK INDICATOR
**Message:**
```
🔶 LIMITED REVERSIBILITY WITH HIGH IMPACT

Your answers indicate:
- Some consequences cannot be fully reversed (Q4: Partial)
- High-impact failures possible (Q3: [worst case])

"Partial reversibility" with high impact can be as serious as "Hard/irreversible."

Example: Bug fixed quickly (easy), but wrong data already sent to customers (irreversible harm done).

Consider: Are you thinking about reversing the code, or reversing the consequences?
```

### Indicator I4: Domain Partially/Not Understood + High Risk → Flag
**Trigger:**
- Q5 = "Partially" OR "No (research required)" AND
- Q3 = "Safety/legal/compliance" OR "Financial loss"

**Action:** 🔶 MEDIUM RISK INDICATOR + Recommendation
**Message:**
```
🔶 DOMAIN UNCERTAINTY WITH HIGH STAKES

You indicated:
- Domain is [partially / not] well understood (Q5)
- Worst case involves [high-impact failure] (Q3)

Building systems in poorly understood domains with high-impact failures is risky.

Recommendations:
- Increase domain research and expert consultation
- Consider R3 classification due to uncertainty
- Add extra validation activities (user testing, expert review)
- Document domain knowledge gaps in Assumptions Register

Per intake rule: "If uncertain, select the higher risk."
```

---

## Layer 4: Warnings & Confirmations

### Warning W1: R3 Classification Confirmation
**Trigger:** Tentative classification = R3
**Action:** Require explicit confirmation
**Message:**
```
🔴 R3 CLASSIFICATION - STRICT RIGOR MODE

Based on your answers, this project is classified as:
**Risk Level: R3** (Safety, legal, financial, or hard-to-reverse consequences)

R3 Requirements:
✓ Strict rigor mode (no downgrade without deviation approval)
✓ 11 mandatory quality artifacts
✓ Full verification and validation required
✓ Expert review recommended
✓ Change control and CAPA processes mandatory

This is the highest risk level and requires the most comprehensive quality management.

[ ] I understand the R3 requirements and confirm this classification is appropriate
```

### Warning W2: R0 Classification with Caveats
**Trigger:** Tentative classification = R0 BUT any of:
- Q3 != "Annoyance"
- Q6 != "Individual"
- Q7 != "No"

**Action:** Show warning before confirming R0
**Message:**
```
⚠️ R0 CLASSIFICATION - ADVISORY RIGOR ONLY

Based on your answers, tentative classification is:
**Risk Level: R0** (Internal, low impact, fully reversible)

R0 is the lowest risk level with Advisory rigor (minimal quality activities).

However, we noticed:
[List any non-R0-typical answers]

Are you certain this project:
- Has truly low impact (worst case = minor annoyance)?
- Is fully reversible (no lasting consequences)?
- Requires only advisory quality guidance?

Per intake rule: "If uncertain, select the higher risk."

[Proceed with R0] [Re-classify as R1]
```

### Warning W3: Downgrade from Strict Rigor
**Trigger:** User attempts to downgrade from R2/R3 to R1/R0
**Action:** Require deviation approval (per intake-rules.md:66)
**Message:**
```
🛑 RIGOR DOWNGRADE REQUIRES DEVIATION APPROVAL

You are attempting to downgrade from:
Current: R[X] (Strict rigor) → Requested: R[Y] (Conditional/Advisory rigor)

Per intake-rules.md:66: "Any downgrade requires a deviation record."

To proceed with downgrade:
1. Document justification for downgrade
2. Identify which risks you are accepting
3. Obtain approval from [appropriate authority]
4. Create deviation record in CAPA Log

[Cancel] [Proceed with Deviation]
```

---

## Layer 5: Expert Review Triggers

### Trigger ER1: High-Risk Indicators Present
**Condition:**
- 2 or more 🔴 HIGH RISK INDICATORS triggered OR
- 3 or more 🔶 MEDIUM-HIGH RISK INDICATORS triggered

**Action:** Flag for expert review
**Recommendation:** "This intake has multiple high-risk indicators. Expert review recommended before finalizing classification."

### Trigger ER2: Contradictory Answers
**Condition:**
- Any Rule CV1, CV2, CV4 triggered (contradictions)

**Action:** Flag for expert review
**Recommendation:** "Contradictory answers detected. Please review with quality expert to ensure correct classification."

### Trigger ER3: Edge Case Classification
**Condition:**
- Classification is R2 OR R3 AND
- Answers don't clearly map to one risk level (borderline case)

**Action:** Optional expert review
**Recommendation:** "This is a borderline classification. Consider expert review for confirmation."

### Trigger ER4: User Indicates Uncertainty
**Condition:**
- User selects "I don't know" OR "Unsure" (if option exists)
- User requests help during intake

**Action:** Mandatory expert review
**Recommendation:** "Uncertainty detected. Expert review required to ensure correct classification."

### Trigger ER5: Safety/Legal + Any Mitigation
**Condition:**
- Q3 = "Safety/legal/compliance" AND
- Any other answer suggests mitigation (Q4=Easy, Q1=Internal, Q6=Individual)

**Action:** Flag for expert review
**Recommendation:** "Safety/legal consequences detected but mitigating factors present. Expert review recommended to determine if R2 or R3 is appropriate."

---

## Layer 6: Override & Justification

### Override O1: Expert Override
**Who:** Quality expert, senior engineer, designated authority
**When:** Classification seems incorrect despite intake answers
**Process:**
1. Expert reviews intake answers
2. Expert proposes different classification with justification
3. Justification logged in Change Log (CHG-XXX)
4. Override documented in Quality Plan
5. Override rationale must address why intake answers don't reflect reality

**Example Justification:**
```
Override: R2 → R3
Rationale: While intake answers suggest R2 (internal, recommendations, easy reversibility),
the system provides quality guidance for safety-critical medical device projects. Incorrect
guidance could indirectly cause patient harm. The "easy reversibility" answer focused on
fixing bugs, not preventing downstream safety incidents. Expert determination: R3 appropriate.
Approved by: [Expert Name], Date: [Date]
```

### Override O2: User Self-Override with Justification
**Who:** Project owner
**When:** User disagrees with calculated classification
**Process:**
1. User must provide detailed justification
2. Must answer: "Why do the intake answers not reflect project reality?"
3. Justification logged
4. Optional: Trigger expert review for validation
5. If overriding to lower risk → Requires deviation approval

**Justification Template:**
```
Classification Override Request
From: [Calculated Risk Level]
To: [Desired Risk Level]

Justification:
[Why do you believe the calculated classification is incorrect?]

Specific intake questions that don't reflect reality:
- Q[X]: [Answer] → Actually: [Reality]
- Q[Y]: [Answer] → Actually: [Reality]

Risks accepted by downgrade (if applicable):
[List risks]

Requested by: [Name]
Date: [Date]
Approval: [Required for downgrades]
```

---

## Implementation Priority

### Phase 1: Critical Safety Mechanisms (Implement First)
1. ✅ Layer 2: Cross-Validation Rules (CV1, CV2, CV3)
2. ✅ Layer 3: Risk Indicators (I1 - Safety/Legal flag)
3. ✅ Layer 4: Warning W1 (R3 confirmation)
4. ✅ Layer 4: Warning W3 (Downgrade prevention)

### Phase 2: Enhanced Validation
5. ✅ Layer 1: All Input Validation Rules
6. ✅ Layer 2: Remaining Cross-Validation Rules
7. ✅ Layer 3: All Risk Indicators
8. ✅ Layer 4: All Warnings

### Phase 3: Expert Review Workflow
9. ✅ Layer 5: Expert Review Triggers
10. ✅ Layer 6: Override Mechanisms

---

## Testing Requirements

Each safety mechanism must be verified:

**Test Coverage:**
- All validation rules triggered with appropriate test cases
- All cross-validation rules detect intended contradictions
- All risk indicators flag appropriate patterns
- All warnings displayed with correct messages
- Expert review triggers activate correctly
- Override workflow enforced

**Test Cases:** See Verification Plan VER-001 through VER-005

---

## Success Metrics

**Target (from Measurement Plan):**
- M-001: Risk classification accuracy ≥95% in production
- M-007: User comprehension ≥90%
- Zero safety incidents due to misclassification

**How Safety Mechanisms Support:**
- Validation rules → Prevent invalid classifications
- Cross-validation → Catch logical errors
- Risk indicators → Flag safety-critical patterns
- Warnings → Force user acknowledgment
- Expert review → Catch edge cases
- Override → Allow correction while maintaining traceability

---

## Related QMS Artifacts

- **Risk Register:** R-001 (Incorrect classification), R-009 (Safety/legal downstream)
- **Verification Plan:** VER-001 (Risk classification testing)
- **Validation Plan:** VAL-002 (User comprehension), VAL-005 (Rigor appropriateness)
- **Measurement Plan:** M-001 (Accuracy), M-007 (Comprehension)
- **Control Plan:** Monitor misclassification incidents, CAPA process

---

## Maintenance

This safety mechanism document should be:
- Reviewed after any intake question changes
- Updated based on misclassification incidents (CAPA findings)
- Refined based on validation testing results (VAL-002, VAL-005)
- Expanded as new patterns/edge cases discovered

**Owner:** Project Owner
**Last Updated:** 2025-12-12
**Next Review:** After initial validation testing
