# Demo Scenarios: Meta-QMS Principles in Action

**Phase 9 Documentation** | QMS Dashboard v1.0-demo

**Purpose:** This document provides 5 canonical demonstration scenarios that exercise frozen WS-1/WS-2 behavior and make Meta-QMS principles observable.

**Important:** All scenarios use existing Dashboard behavior only. No new logic or capabilities are demonstrated.

---

## How to Use This Document

**Each scenario includes:**
1. **Context:** Project description and risk classification
2. **Setup:** API calls and artifact states
3. **Expected Outputs:** What the Dashboard will return
4. **What to Notice:** Meta-QMS principles made visible
5. **Human Judgment Required:** Boundaries automation cannot cross

**Running scenarios:**
- Start API server: `uvicorn src.backend.main:app --reload`
- Use provided curl commands or API docs at `http://127.0.0.1:8000/docs`
- Observe outputs and compare to "What to Notice" sections

---

## Scenario 1: Low-Risk Learning Project (R0 Advisory Mode)

### Context

**Project:** Internal Data Visualization Dashboard
**User:** Team of 3, building tool for own use
**Risk Classification:** R0 (Minimal)
- Internal users only
- Informational recommendations
- Easy to reverse
- No regulatory requirements

**Why R0:** Internal, low-impact, fully reversible project

---

### Setup

**Step 1: Create intake**
```bash
curl -X POST "http://127.0.0.1:8000/api/intake" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Internal Data Dashboard",
    "answers": {
      "q1_users": "Internal",
      "q2_influence": "Recommendations",
      "q3_worst_failure": "Minor",
      "q4_reversibility": "Easy",
      "q5_domain": "No",
      "q6_scale": "Team",
      "q7_regulated": "No"
    }
  }'
```

**Expected:** Risk level R0, completion threshold 50%

**Step 2: Generate artifacts**
```bash
curl -X POST "http://127.0.0.1:8000/api/intake/{intake_id}/generate-artifacts"
```

**Step 3: Check dependency health (with partial artifacts)**
```bash
curl -X GET "http://127.0.0.1:8000/api/intake/{intake_id}/dependency-health"
```

---

### Expected Outputs

**Risk Register (partial, 45% complete):**
```json
{
  "artifact_name": "Risk Register",
  "readiness": {
    "ready": false,
    "completion": 0.45,
    "threshold": 0.50,
    "epistemic_status": "structural_only",
    "can_proceed_anyway": true,
    "confidence_limits": [
      "Structural validation only; content correctness not assessed"
    ]
  },
  "suggestion": "Risk Register shows 45% completion (R0 threshold: 50%). Consider adding risk descriptions."
}
```

**Key observations:**
- Threshold is 50% (lowest rigor)
- `ready: false` but `can_proceed_anyway: true`
- Language is descriptive ("Consider"), not prescriptive ("You must")

---

### What to Notice

**Meta-QMS Principle: Risk-Proportionate Rigor**
- R0 projects have lowest threshold (50%)
- Encourages iterative learning and drafts
- Does NOT mean "low quality" — means "appropriate rigor for risk level"

**Meta-QMS Principle: Teaching vs Enforcement Separation**
- Even at 45% completion, user can proceed
- No hard blocking at artifact validation layer
- System teaches, does not enforce

**Meta-QMS Principle: Epistemic Status Transparency**
- `epistemic_status: "structural_only"` declares assessment basis
- `confidence_limits` explain what assessment cannot know
- Prevents over-trust in automation

---

### Human Judgment Required

**The Dashboard CANNOT answer:**
- Are the identified risks the right ones for this project?
- Are risk mitigations adequate?
- Is 45% completion sufficient for this team's workflow?
- Should the team proceed or complete more structure first?

**These are strategic and semantic judgments only humans can make.**

---

## Scenario 2: Dependency Readiness Issue (R2 Strict Mode)

### Context

**Project:** Customer-Facing Recommendation Engine
**User:** External product team
**Risk Classification:** R2 (Strict)
- External users affected
- Decision-influencing recommendations
- Moderately difficult to reverse

**Why R2:** External users + decision impact

---

### Setup

**Step 1: Create intake** (R2 classification expected)
```bash
curl -X POST "http://127.0.0.1:8000/api/intake" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Recommendation Engine",
    "answers": {
      "q1_users": "External",
      "q2_influence": "Decisions",
      "q3_worst_failure": "Financial",
      "q4_reversibility": "Hard",
      "q5_domain": "Yes",
      "q6_scale": "Organization",
      "q7_regulated": "No"
    }
  }'
```

**Step 2: Generate artifacts and manually set states:**
- Risk Register: 55% complete (below 80% threshold)
- CTQ Tree: 60% complete (below 80% threshold)
- Verification Plan: 40% complete (depends on Risk Register + CTQ Tree)

**Step 3: Check dependency health**
```bash
curl -X GET "http://127.0.0.1:8000/api/intake/{intake_id}/dependency-health"
```

---

### Expected Outputs

**Verification Plan (depends on Risk Register + CTQ Tree):**
```json
{
  "artifact_name": "Verification Plan",
  "dependencies": ["Risk Register", "CTQ Tree"],
  "all_dependencies_ready": false,
  "readiness": {
    "ready": false,
    "completion": 0.40,
    "threshold": 0.72,
    "epistemic_status": "structural_only",
    "can_proceed_anyway": true
  },
  "suggestion": "Risk Register (55%) and CTQ Tree (60%) are below R2 threshold (80%). Verification Plan may lack context."
}
```

**Next Actions:**
```json
{
  "action": "Consider completing Risk Register structure",
  "artifact_name": "Risk Register",
  "priority": "high",
  "reason": "Verification Plan depends on Risk Register; completing foundation first reduces rework",
  "unblocks": ["Verification Plan", "Control Plan"]
}
```

---

### What to Notice

**Meta-QMS Principle: Directional Dependencies**
- Verification Plan depends on Risk Register and CTQ Tree
- Upstream incompleteness may leave downstream without context
- Dashboard surfaces this; you decide workflow strategy

**Meta-QMS Principle: Artifact Volatility**
- Verification Plan has `draft_friendly` volatility (threshold -10%)
- Adjusted threshold: 80% - 10% = 72%
- System recognizes some artifacts benefit from early drafts

**Meta-QMS Principle: Risk-Proportionate Rigor**
- R2 threshold is 80% (vs R0: 50%)
- Higher-impact projects need more structural rigor
- But NO hard blocking — `can_proceed_anyway: true` still holds

**Key insight:**
- "Consider completing" is teaching language, not a command
- Priority is diagnostic, not mandatory
- You can work top-down (Verification Plan first) if strategically better

---

### Human Judgment Required

**The Dashboard CANNOT answer:**
- Is working bottom-up (foundation-first) the right strategy?
- Or is top-down (goal-driven) better for this team's process?
- Are the risks and CTQs in upstream artifacts correct?
- Is Verification Plan content adequate despite upstream gaps?

**Strategic workflow decisions remain human choices.**

---

## Scenario 3: Volatility Contrast (Draft-Friendly vs Rework-Costly)

### Context

**Project:** Quality Management System (R2)
**User:** Demonstrating how artifact volatility affects thresholds

**Goal:** Show how "draft-friendly" and "rework-costly" artifacts have different thresholds at the same risk level.

---

### Setup

**Step 1: Create R2 intake**

**Step 2: Check two artifacts at same completion (75%):**
- Verification Plan: 75% complete (draft-friendly)
- Traceability Index: 75% complete (rework-costly)

**Step 3: Request dependency health**

---

### Expected Outputs

**Verification Plan (draft-friendly):**
```json
{
  "artifact_name": "Verification Plan",
  "volatility": "draft_friendly",
  "readiness": {
    "ready": true,
    "completion": 0.75,
    "threshold": 0.72,
    "base_threshold": 0.80,
    "modifier": -0.10,
    "reason": "Draft-friendly artifact: early drafts reduce later rework"
  }
}
```
✅ **Ready: true** (75% exceeds 72% threshold)

**Traceability Index (rework-costly):**
```json
{
  "artifact_name": "Traceability Index",
  "volatility": "rework_costly",
  "readiness": {
    "ready": false,
    "completion": 0.75,
    "threshold": 0.88,
    "base_threshold": 0.80,
    "modifier": +0.10,
    "reason": "Rework-costly artifact: higher threshold prevents expensive later corrections"
  }
}
```
❌ **Ready: false** (75% below 88% threshold)

---

### What to Notice

**Meta-QMS Principle: Artifact Volatility Awareness**
- Same completion (75%), different readiness results
- Verification Plan benefits from early iteration (lower threshold)
- Traceability Index is expensive to fix later (higher threshold)

**Design rationale:**
- Some artifacts (Verification Plan) need early drafts to test assumptions
- Some artifacts (Traceability Index) are costly to restructure after downstream work begins
- Volatility modifiers encode this domain knowledge explicitly

**Thresholds are policy, not universal truth:**
- Modifiers are versioned and calibratable
- Different domains might use different values
- But the *principle* of volatility-aware thresholds is Meta-QMS canon

---

### Human Judgment Required

**The Dashboard CANNOT answer:**
- Is the Traceability Index content correct at 75%?
- Should we proceed with downstream work despite 75% < 88%?
- Is the volatility classification correct for our domain?

**Correctness and strategic trade-offs remain human decisions.**

---

## Scenario 4: Override Accumulation (Debt Visibility)

### Context

**Project:** Monitoring Dashboard (R1)
**User:** Experienced team working top-down (goal-first, foundation later)

**Goal:** Demonstrate override debt tracking when user repeatedly proceeds despite warnings.

---

### Setup

**Step 1: Create R1 intake**

**Step 2: Simulate workflow:**
1. Check CTQ Tree (incomplete, proceed anyway) — override count: 1
2. Check Risk Register (incomplete, proceed anyway) — override count: 2
3. Check Measurement Plan (incomplete, proceed anyway) — override count: 3
4. Check Verification Plan (incomplete, proceed anyway) — override count: 4
5. Check Validation Plan (incomplete, proceed anyway) — override count: 5
6. Check Control Plan (incomplete, proceed anyway) — override count: 6

**Step 3: Request dependency health with override tracking**

---

### Expected Outputs

**After 6 overrides:**
```json
{
  "artifact_name": "Control Plan",
  "readiness": {
    "ready": false,
    "completion": 0.50,
    "can_proceed_anyway": true,
    "override_budget": {
      "count": 6,
      "status": "high",
      "message": "You have proceeded 6 times despite structural warnings. This may indicate systematic gaps or intentional top-down workflow."
    }
  }
}
```

**Status progression:**
- Count 0-2: "low" (normal iteration)
- Count 3-5: "medium" (accumulating debt)
- Count 6+: "high" (significant debt visibility)

---

### What to Notice

**Meta-QMS Principle: Override Debt Visibility**
- System tracks proceed-anyway actions across session
- Debt becomes visible without blocking
- No judgment about *whether* this is wrong

**Why this matters:**
- Top-down workflow (goal → foundation) can be strategically correct
- But repeatedly ignoring warnings *might* indicate problems
- Visibility prevents "spiral blindness" without removing agency

**Language is neutral:**
- "This may indicate..." NOT "This is wrong"
- Dashboard surfaces the pattern; you interpret meaning

---

### What to Notice (Continued)

**Soft blocking in practice:**
- Even at count=6, `can_proceed_anyway: true`
- No forced workflow or stage gates
- User retains full control

**Teaching principle:**
- Visibility changes behavior without enforcement
- User becomes aware of accumulated debt
- Can then make informed strategic decision

---

### Human Judgment Required

**The Dashboard CANNOT answer:**
- Is this top-down workflow strategically correct for this team?
- Or does override debt indicate systematic quality issues?
- Should the team pause and complete foundations?
- Or should they continue to goal and backfill later?

**Strategic workflow decisions require human judgment and team context.**

---

## Scenario 5: Strict Mode Boundary (R3 Near-Complete)

### Context

**Project:** Medical Device Software (R3)
**User:** Regulated, safety-critical project
**Risk Classification:** R3 (Maximum)
- Safety-critical (patient harm possible)
- Regulated (FDA, ISO 62304)
- Hard to reverse
- External users

**Why R3:** Safety + regulated + hard-reversibility

---

### Setup

**Step 1: Create R3 intake**
```bash
curl -X POST "http://127.0.0.1:8000/api/intake" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Medical Imaging AI",
    "answers": {
      "q1_users": "External",
      "q2_influence": "Decisions",
      "q3_worst_failure": "Safety_Legal_Compliance",
      "q4_reversibility": "Hard",
      "q5_domain": "Yes",
      "q6_scale": "Organization",
      "q7_regulated": "Yes"
    }
  }'
```

**Expected:** R3 classification, 90% threshold

**Step 2: Simulate near-complete artifacts:**
- Risk Register: 88% complete (below 90%)
- CTQ Tree: 92% complete (above 90%)
- Verification Plan: 91% complete (above 90%, but dependencies incomplete)

**Step 3: Check dependency health**

---

### Expected Outputs

**Risk Register (88% at R3):**
```json
{
  "artifact_name": "Risk Register",
  "readiness": {
    "ready": false,
    "completion": 0.88,
    "threshold": 0.90,
    "epistemic_status": "structural_only",
    "can_proceed_anyway": true,
    "confidence_limits": [
      "Structural validation only",
      "R3 projects require expert review even when structure complete"
    ],
    "reason": "88% completion is close to R3 threshold (90%) but not yet met. 2 minor structural gaps remain."
  }
}
```

**Verification Plan (91%, but dependencies incomplete):**
```json
{
  "artifact_name": "Verification Plan",
  "dependencies": ["Risk Register", "CTQ Tree"],
  "readiness": {
    "ready": true,
    "completion": 0.91,
    "threshold": 0.81,
    "epistemic_status": "structural_only"
  },
  "all_dependencies_ready": false,
  "suggestion": "Risk Register (88%) is below R3 threshold. Verification Plan structure is complete, but foundation artifacts may need review."
}
```

---

### What to Notice

**Meta-QMS Principle: Risk-Proportionate Rigor**
- R3 has highest threshold (90%)
- Even 88% is "not ready" (vs R0 where 50% is threshold)
- Stricter rigor reflects higher consequences

**Even at R3, soft blocking holds:**
- `can_proceed_anyway: true` still present
- NO hard blocking even for safety-critical projects
- Teaching principle applies at all risk levels

**Why no hard blocking at R3?**
- Levels 1-3 (structural validation) use teaching mode at all risk levels
- Hard blocking belongs at Level 4 (stage transitions), not Level 3 (artifact readiness)
- Example: "Can we release to production?" is a Level 4 decision (may hard-block)
- Example: "Can I continue drafting artifacts?" is Level 3 (should not block)

**Critical insight:**
- R3 escalates *tone* and *threshold*, not authority
- "You should strongly consider" vs "Consider" (R0)
- But "should" is still descriptive, not prescriptive
- Final decisions remain with user and expert reviewers

---

### What to Notice (Continued)

**Confidence limits more explicit at R3:**
- "R3 projects require expert review even when structure complete"
- System explicitly states its own boundaries
- Prevents false confidence in high-stakes contexts

**Dependency awareness critical:**
- Verification Plan structurally complete
- But foundation (Risk Register) has gaps
- Downstream work may be based on incomplete context

---

### Human Judgment Required

**The Dashboard CANNOT answer:**
- Are the identified safety risks complete and correct?
- Are mitigations sufficient for regulatory approval?
- Is the team ready for formal design review or FDA submission?
- Should work proceed despite 88% < 90%, or pause until 90%+?

**At R3, human expert review is mandatory:**
- NOT because Dashboard cannot automate it
- Because semantic validation is always a human responsibility
- R3 just makes the stakes more visible

---

## Summary: What These Scenarios Demonstrate

### Across All Scenarios

**Teaching vs Enforcement Separation:**
- `can_proceed_anyway: true` in every scenario, every risk level
- Language is descriptive, never prescriptive
- User agency is preserved even at R3 (safety-critical)

**Structural vs Semantic Boundaries:**
- `epistemic_status: structural_only` appears everywhere
- Dashboard checks form; humans check correctness
- Boundary is explicit and never violated

**Risk-Proportionate Rigor:**
- Thresholds scale: R0 (50%) → R1 (60%) → R2 (80%) → R3 (90%)
- NOT because higher risk needs "better" artifacts
- Because higher risk justifies stricter structural expectations

**Epistemic Status Transparency:**
- Every assessment declares what it can and cannot know
- Confidence limits prevent over-trust
- Automation acknowledges its own boundaries

---

### Key Takeaways

1. **Soft blocking works at all risk levels**
   - Teaching mode is not just for low-risk projects
   - Even R3 (safety-critical) uses `can_proceed_anyway: true`
   - Enforcement belongs at stage transitions, not artifact validation

2. **Structural validation has value despite semantic boundaries**
   - Catching placeholders, missing sections, broken references is useful
   - But it does NOT replace human judgment of correctness
   - Both are necessary; neither is sufficient alone

3. **Override debt visibility prevents spiral blindness**
   - Proceeding despite warnings can be strategically correct
   - But accumulating debt needs visibility
   - Dashboard surfaces patterns; humans interpret meaning

4. **Artifact volatility reflects domain knowledge**
   - Some artifacts benefit from early drafts
   - Some are expensive to restructure later
   - Thresholds encode this explicitly, not implicitly

5. **Dependencies guide workflow but don't enforce it**
   - Bottom-up (foundation-first) reduces rework risk
   - Top-down (goal-first) can be strategically better
   - Dashboard shows relationships; you choose strategy

---

## Running Your Own Scenarios

**To explore further:**

1. **Vary risk levels:** Try same project with different risk answers
2. **Vary completion:** Change artifact states to see threshold effects
3. **Accumulate overrides:** Proceed repeatedly to see debt tracking
4. **Test dependencies:** Make upstream incomplete, observe downstream signals
5. **Mix volatility:** Compare draft-friendly vs rework-costly at same completion

**Remember:**
- All behavior is frozen (v1.0)
- Scenarios exercise existing logic only
- No new capabilities are being demonstrated
- Dashboard is a teaching tool, not a product

---

**End of Demo Scenarios**

**For deeper understanding:**
- **USAGE-GUIDE.md** - How to interpret Dashboard signals
- **META-QMS-CANON-V1.md** - Why these principles exist
- **WS-2-SCOPE-FREEZE.md** - What is frozen and why
