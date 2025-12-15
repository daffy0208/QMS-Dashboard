# Intake Question Analysis
## Usability Issues and Misclassification Risks

**Date:** 2025-12-12
**Purpose:** Identify and address intake question clarity issues and risk misclassification risks

---

## Current Intake Questions - Issue Analysis

### Q1: Who are the users?
**Current:** Internal / External / Public

**Potential Issues:**
- ✅ Clear and straightforward
- ⚠️ "Internal" might be ambiguous for contractors, partners, or subsidiaries
- ⚠️ Doesn't capture "internal at first, then external later" scenarios

**Risk:** Low misclassification risk, but could miss future expansion plans

---

### Q2: What decisions or actions will this system influence?
**Current:** Informational only / Recommendations / Automated actions

**Potential Issues:**
- ⚠️ "Informational only" vs "Recommendations" distinction unclear
  - Example: A dashboard shows data (informational) but users make decisions based on it (decision-influencing)
- ⚠️ "Recommendations" is broad - doesn't distinguish between "suggestions" and "critical guidance"
- ⚠️ Users might underestimate influence ("it just provides info" when users heavily rely on it)

**Risk:** MEDIUM-HIGH misclassification risk - users may understate impact

---

### Q3: What is the worst credible failure?
**Current:** Annoyance / Financial loss / Safety/legal/compliance / Reputational damage

**Potential Issues:**
- ⚠️⚠️ "Credible" is subjective - users might say "technically possible but unlikely" or "very unlikely but technically could happen"
- ⚠️⚠️ Multiple failure modes might apply (e.g., financial AND reputational)
- ⚠️⚠️ Users might not consider indirect failures (system fails → people make bad decisions → downstream harm)
- ⚠️ "Annoyance" covers huge range (minor UI bug to data loss)
- ⚠️ Safety/legal/compliance lumped together - very different severity levels

**Risk:** HIGH misclassification risk - this is the most critical question and most subjective

---

### Q4: How reversible are failures?
**Current:** Easy / Partial / Hard/irreversible

**Potential Issues:**
- ⚠️ "Easy" is subjective - easy for whom? In what timeframe?
- ⚠️ Doesn't capture "easy to detect" vs "easy to fix" distinction
- ⚠️ Users might conflate "we can rollback the code" with "we can undo the consequences"
- ⚠️ Doesn't address time-to-detect (if detected late, "easy" fix has already caused harm)

**Risk:** MEDIUM misclassification risk - users may overestimate reversibility

---

### Q5: Is the domain well understood?
**Current:** Yes / Partially / No (research required)

**Potential Issues:**
- ⚠️ "Well understood by whom?" - by the team, by the industry, by the user?
- ⚠️ Users might overestimate their understanding (Dunning-Kruger effect)
- ✅ Relatively clear question

**Risk:** LOW-MEDIUM misclassification risk

---

### Q6: What is the expected scale?
**Current:** Individual / Team / Multi-team / Organization-wide/public

**Potential Issues:**
- ✅ Clear and straightforward
- ⚠️ Doesn't capture "starts small, grows large" scenario
- ⚠️ Users might underestimate future scale

**Risk:** LOW misclassification risk, but could miss growth scenarios

---

### Q7: Is the project regulated or auditable?
**Current:** No / Possibly / Yes

**Potential Issues:**
- ⚠️ "Possibly" is vague - triggers uncertainty
- ⚠️ Users might not know if their project is regulated
- ⚠️ Doesn't distinguish "subject to regulation" vs "used in regulated context"
- ⚠️ "Auditable" vs "regulated" are different - conflates compliance and oversight

**Risk:** MEDIUM misclassification risk - users may not understand regulatory context

---

## Risk Classification Logic - Safety Analysis

### Current Classification Rules (intake-rules.md:48-55)
- **R0:** Internal, low impact, fully reversible
- **R1:** Internal, moderate impact, reversible
- **R2:** External users, decision-impacting, or auditable
- **R3:** Safety, legal, financial, or hard-to-reverse consequences

### Identified Safety Issues

#### Issue 1: "OR" logic ambiguity
**Problem:** R2 uses "OR" (external users OR decision-impacting OR auditable), but R3 also uses "OR" (safety OR legal OR financial OR hard-to-reverse)

**Risk:** If Q3 = "Safety/legal/compliance" → should ALWAYS be R3, but current logic might classify as R2 if other factors are moderate

**Example:** Our QMS Dashboard case:
- Internal (not external) ✓
- Decision-impacting ✓ → triggers R2
- Worst failure: Safety/legal/compliance ✓ → should trigger R3
- Easy reversibility → mitigates to R2?

**Current classification:** R2 (reasonable but edge case)
**Possible classification:** R3 (if safety/legal is prioritized)

#### Issue 2: No weighting of factors
**Problem:** All factors treated equally, but "worst credible failure = safety" should be weighted more heavily than "individual scale"

**Risk:** Low-scale but safety-critical projects might be under-classified

#### Issue 3: No cross-validation
**Problem:** Contradictory answers not flagged
- Example: "Automated actions" + "Easy reversibility" + "Safety worst case" → contradictory
- Example: "Informational only" + "Hard to reverse" → doesn't make sense

**Risk:** Inconsistent answers → incorrect classification

#### Issue 4: "If uncertain, select higher risk" not operationalized
**Problem:** Rule exists (intake-rules.md:55) but:
- When is user "uncertain"?
- How do we detect uncertainty?
- How do we enforce this rule?

**Risk:** Users who should be uncertain proceed with lower classification

---

## High-Risk Question Combinations (Misclassification Scenarios)

### Scenario 1: "Recommendation System with Safety Impact"
**Answers:**
- Q2: Recommendations (not automated)
- Q3: Safety/legal/compliance
- Q4: Easy (user thinks "we can fix bugs easily")

**Likely Classification:** R2 (decision-impacting)
**Correct Classification:** Probably R3 (safety impact should override)
**Mitigation Needed:** Flag Q2=Recommendations + Q3=Safety → Warning + Consider R3

---

### Scenario 2: "Internal Tool with External Data/Impact"
**Answers:**
- Q1: Internal (only internal users access it)
- Q2: Automated actions
- Q3: Financial loss (affects external customers but internal system)

**Likely Classification:** R1-R2
**Correct Classification:** Probably R3 (automated financial impact)
**Mitigation Needed:** Flag Q1=Internal + Q2=Automated + Q3=Financial → Warning

---

### Scenario 3: "Prototype That Becomes Production"
**Answers:**
- Q6: Individual (it's just a prototype!)
- Q3: Safety/legal (but "it's just a prototype")
- Q7: No (we're just testing)

**Likely Classification:** R0-R1
**Correct Classification:** If prototype affects real decisions → R2-R3
**Mitigation Needed:** Flag "prototype" language → Warning about production use

---

### Scenario 4: "Informational Dashboard Driving Critical Decisions"
**Answers:**
- Q2: Informational only (users think "we just show data")
- Q3: Safety/legal (but they don't connect it)
- Reality: Users make safety-critical decisions based on dashboard

**Likely Classification:** R0-R1
**Correct Classification:** R2-R3 (decision-impacting even if not automated)
**Mitigation Needed:** Clarify Q2 with examples, ask "will users make decisions based on this?"

---

## Summary: Critical Improvements Needed

### Priority 1 (CRITICAL - Safety)
1. **Add cross-validation rules** to detect contradictory answers
2. **Weight safety/legal/financial answers heavily** → Auto-flag for R3 consideration
3. **Add "Are you sure?" confirmations** for high-risk indicators
4. **Implement expert review triggers** for edge cases

### Priority 2 (HIGH - Clarity)
5. **Add examples to each question** (especially Q2, Q3, Q4)
6. **Clarify "credible" in Q3** - provide probability guidance
7. **Split Q4 into "time to detect" and "time to fix"**
8. **Clarify Q2 with indirect decision influence**

### Priority 3 (MEDIUM - Usability)
9. **Add guidance for "uncertain" answers** - when to select higher risk
10. **Show tentative risk classification during intake** (preview)
11. **Allow "I don't know" answers** → Auto-escalate to expert review
12. **Add explanations of R0-R3 levels** during intake

---

## Next Steps
1. Design safety mechanisms (validation rules, warnings)
2. Create enhanced intake with examples and guidance
3. Implement expert review workflow
4. Update Risk Register and Mitigation Plans
