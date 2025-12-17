# Usage Guide: When and How to Use the QMS Dashboard

**Phase 9 Documentation** | QMS Dashboard v1.0-demo

**Purpose:** This guide explains when and how to use the Dashboard as a teaching and diagnostic tool, and when human judgment must replace automation.

**Critical:** This Dashboard does NOT make quality decisions. It provides structural signals to inform human judgment.

---

## 1. When to Use the Dashboard

### 1.1 Appropriate Use Cases

✅ **Use the Dashboard when you need:**

**Teaching & Learning:**
- Understanding how risk-based quality systems work
- Learning what "risk-proportionate rigor" means in practice
- Seeing how dependency relationships affect readiness
- Observing the difference between structural and semantic validation

**Diagnostic Visibility:**
- Checking structural completeness of quality artifacts
- Identifying missing sections or placeholders
- Visualizing artifact dependency relationships
- Tracking how often you've proceeded despite warnings (override debt)

**System Demonstration:**
- Showing stakeholders how quality rigor scales with project risk
- Demonstrating teaching-oriented quality signals
- Proving that soft blocking preserves user agency
- Validating Meta-QMS principles in a working system

**Research & Standards Development:**
- Evidence-based quality system design
- Comparative analysis of rigor modes
- Studying teaching vs enforcement trade-offs

---

### 1.2 Inappropriate Use Cases

❌ **DO NOT use the Dashboard for:**

**Production Decision-Making:**
- Approving artifacts for production use
- Determining if content is correct or adequate
- Making go/no-go decisions for project phases
- Replacing expert review or sign-off

**Semantic Validation:**
- Judging if risks are the right risks
- Evaluating if mitigations are sufficient
- Assessing if requirements are complete
- Determining if test plans are adequate

**Workflow Enforcement:**
- Blocking progression through project stages
- Requiring artifacts to be completed in specific order
- Preventing users from proceeding with their work
- Automating stage-gate approvals

**Content Generation:**
- Auto-filling artifact content
- Suggesting "how to fix" problems
- Generating improvement recommendations
- Completing partial artifacts

**Why these are out of scope:**
- The Dashboard checks structure only (epistemic boundary)
- Teaching systems preserve user agency (no hard blocking)
- Human judgment is mandatory for correctness (automation boundary)
- These capabilities belong to future workstreams (WS-3, WS-4, WS-6)

---

## 2. How to Interpret Dashboard Signals

### 2.1 Readiness Assessment

**What you'll see:**
```json
{
  "ready": false,
  "completion": 0.65,
  "epistemic_status": "structural_only",
  "can_proceed_anyway": true,
  "confidence_limits": [
    "This assessment checks structure only, not content correctness"
  ]
}
```

**How to interpret:**

| Field | Meaning | What it is NOT |
|-------|---------|----------------|
| `ready` | Structural completeness meets threshold | NOT a correctness judgment |
| `completion` | % of acceptance criteria met | NOT a quality score |
| `epistemic_status` | "structural_only" always | NOT semantic validation |
| `can_proceed_anyway` | Always `true` (teaching mode) | NOT a hard block |
| `confidence_limits` | What this assessment cannot know | NOT disclaimers to ignore |

**Key principle:**
- `ready: false` means "structure incomplete, but you can proceed"
- `ready: true` means "structure complete, but correctness unverified"

Neither means "quality approved" or "content correct".

---

### 2.2 Risk Thresholds

**What you'll see:**
- R0 (Minimal): 50% completion threshold
- R1 (Moderate): 60% completion threshold
- R2 (Strict): 80% completion threshold
- R3 (Maximum): 90% completion threshold

**How to interpret:**

**R0/R1 (Advisory/Conditional):**
- Lower thresholds reflect acceptable draft-state work
- Encourages iteration and learning
- Appropriate for reversible, low-impact projects

**R2/R3 (Strict/Maximum):**
- Higher thresholds reflect stricter structural expectations
- Does NOT mean "perfect" or "approved"
- Appropriate for high-impact, regulated, or safety-critical projects

**What thresholds are NOT:**
- NOT quality scores or correctness percentages
- NOT measures of how "good" your artifacts are
- NOT approval gates for production deployment

**They are:** Reference defaults showing how rigor scales with risk.

---

### 2.3 Dependency Status

**What you'll see:**
```json
{
  "artifact_name": "Verification Plan",
  "dependencies": ["Risk Register", "CTQ Tree"],
  "all_dependencies_ready": false,
  "readiness": { ... },
  "suggestion": "Risk Register shows 45% completion (R2 threshold: 80%)"
}
```

**How to interpret:**

**Dependency relationships:**
- Static, directional graph (upstream → downstream)
- If Risk Register incomplete, Verification Plan may lack context
- Does NOT mean you cannot work on Verification Plan

**`all_dependencies_ready: false`:**
- Signals potential context gaps
- Suggests reviewing upstream artifacts first
- Does NOT block you from proceeding

**Why this matters:**
- Working bottom-up (foundation first) reduces rework
- But top-down (goal-driven) is sometimes strategically better
- The Dashboard shows dependency state; you decide strategy

---

### 2.4 Next Actions

**What you'll see:**
```json
{
  "action": "Consider reviewing Risk Register structure",
  "reason": "Verification Plan depends on Risk Register, which shows 45% completion",
  "priority": "high"
}
```

**How to interpret:**

**Language is descriptive, not prescriptive:**
- "Consider reviewing" NOT "You must review"
- "Shows 45% completion" NOT "This is wrong"
- Priority is diagnostic, NOT mandator

y

**These are teaching signals:**
- They explain dependency relationships
- They surface structural gaps
- They do NOT tell you what to do

**You remain in control:**
- You can proceed with downstream artifacts
- You can work top-down instead of bottom-up
- `can_proceed_anyway` is always `true`

---

### 2.5 Override Debt Tracking

**What you'll see:**
```json
{
  "override_budget": {
    "count": 5,
    "status": "high",
    "message": "You have proceeded 5 times despite structural warnings"
  }
}
```

**How to interpret:**

**Override debt is visibility, not enforcement:**
- Tracks how often you proceeded despite `ready: false`
- Surfaces accumulated technical debt
- Does NOT prevent you from proceeding again

**Status levels:**
- Low (0-2): Normal iteration
- Medium (3-5): Accumulating debt
- High (6+): Significant debt visibility

**Why this matters:**
- Proceeding despite warnings is sometimes correct
- But *repeatedly* doing so may indicate systemic issues
- The Dashboard makes this visible; you decide if it's a problem

---

## 3. The Human Judgment Boundary

### 3.1 What the Dashboard Cannot Do

The Dashboard operates in **Levels 1-3** (structural validation only).

**Level 1: Structural Presence**
- ✅ Does this section exist?
- ❌ Is the content correct?

**Level 2: Structural Completeness**
- ✅ Are required items present?
- ❌ Are they the right items?

**Level 3: Readiness for Downstream Use**
- ✅ Do dependencies meet structural thresholds?
- ❌ Is the content adequate for downstream use?

**Levels 4-5 require human judgment:**

**Level 4: Stage Transition Readiness**
- Are artifacts ready for formal review or production deployment?
- This is a human decision, not automated

**Level 5: Semantic Validation**
- Is the content correct, complete, and adequate?
- This is always a human decision

---

### 3.2 When Human Review is Mandatory

**Always require human expert review for:**

1. **Correctness:** Is the content factually accurate?
2. **Adequacy:** Is it sufficient for the intended purpose?
3. **Approval:** Is it ready for production use?
4. **Compliance:** Does it meet regulatory requirements?
5. **Risk Judgment:** Are the right risks identified with appropriate mitigations?

**The Dashboard cannot answer these questions.**

---

### 3.3 How Dashboard and Human Review Work Together

**Dashboard (Structural):**
- "Risk Register has 12 risks listed, no placeholders, 85% complete (R2: 80%)"

**Human Expert (Semantic):**
- "Are these the right 12 risks for this project?"
- "Are the mitigations feasible and sufficient?"
- "Are any critical risks missing?"

**Both are necessary:**
- Dashboard provides diagnostic visibility
- Human provides judgment and approval
- Neither replaces the other

---

## 4. Meta-QMS Principles in Practice

### 4.1 Risk-Proportionate Rigor

**You'll observe:**
- R0 projects have lower thresholds (50%)
- R3 projects have higher thresholds (90%)
- Volatility modifiers adjust thresholds per artifact

**What this demonstrates:**
- Rigor scales with project risk, not project size
- "One size fits all" quality is wasteful (over-rigorous) or dangerous (under-rigorous)
- Thresholds are policy, not universal truth

---

### 4.2 Teaching vs Enforcement Separation

**You'll observe:**
- `can_proceed_anyway: true` on every signal
- Language is descriptive ("shows 45%"), not prescriptive ("you must")
- No hard blocking at artifact validation layer

**What this demonstrates:**
- Teaching systems preserve user agency
- Enforcement belongs at stage transitions (Levels 4-5), not artifact validation (Levels 1-3)
- Users learn better when not blocked

---

### 4.3 Structural vs Semantic Boundaries

**You'll observe:**
- Dashboard checks section presence, item counts, placeholders
- It does NOT judge if content is correct or adequate
- `epistemic_status: structural_only` appears on every assessment

**What this demonstrates:**
- Automation can check form; humans check correctness
- Blurring this boundary creates false confidence or over-trust
- Epistemic honesty prevents misuse

---

### 4.4 Override Debt Visibility

**You'll observe:**
- Override count tracked across sessions
- Status escalates (low → medium → high)
- No blocking, just visibility

**What this demonstrates:**
- Proceeding despite warnings can be strategically correct
- But accumulating debt needs visibility
- Visibility without enforcement prevents "spiral blindness"

---

## 5. Common Misinterpretations

### ❌ "The Dashboard says I'm at 85%, so my artifact is 85% good"

**Correct interpretation:**
- 85% of structural acceptance criteria are met
- Says nothing about correctness or adequacy
- Human review still required

### ❌ "I reached 'ready: true', so I'm done"

**Correct interpretation:**
- Structure is complete per policy thresholds
- Semantic validation has not occurred
- Expert review and approval still required

### ❌ "I have high override debt, so I did something wrong"

**Correct interpretation:**
- You proceeded despite structural warnings 6+ times
- This may be strategically correct (e.g., top-down work)
- Or it may indicate systemic issues to investigate
- Dashboard surfaces this; you decide meaning

### ❌ "Next actions say 'high priority', so I must do them first"

**Correct interpretation:**
- Priority is diagnostic, not mandatory
- You control your workflow strategy
- Dashboard explains dependencies; you choose approach

---

## 6. Workflow Integration

### 6.1 Using the Dashboard During Artifact Development

**Suggested workflow:**

1. **Start with structure:** Use Dashboard to verify sections exist
2. **Iterate with feedback:** Fill in content, check structural completeness
3. **Review dependencies:** Check if upstream artifacts provide needed context
4. **Track override debt:** Notice if you're frequently proceeding despite warnings
5. **Request human review:** When Dashboard shows `ready: true`, engage expert

**Remember:**
- Dashboard is a diagnostic tool, not a workflow orchestrator
- You control when and how you use it
- It informs, not commands

---

### 6.2 Using the Dashboard for Team Teaching

**Effective uses:**

- **Onboarding:** Show new team members how quality rigor scales
- **Principle demonstration:** Use demo scenarios to illustrate Meta-QMS principles
- **Boundary education:** Teach the difference between structural and semantic validation
- **Debt discussion:** Use override tracking to discuss technical debt

**Ineffective uses:**

- **Performance review:** Dashboard signals are not quality scores
- **Blame assignment:** Override debt is visibility, not failure
- **Workflow control:** Dashboard is not a task management system

---

## 7. Advanced Interpretation

### 7.1 Artifact Volatility

**You'll notice:**
- Verification Plan (draft-friendly): threshold -10%
- Risk Register (foundation): threshold +0%
- Traceability Index (rework-costly): threshold +10%

**What this means:**
- Some artifacts benefit from early drafts (Verification Plan)
- Some need stability as foundations (Risk Register)
- Some are expensive to rework (Traceability Index)

**Practical impact:**
- Draft-friendly artifacts have lower thresholds
- Rework-costly artifacts have higher thresholds
- This is explicit policy, visible and versioned

---

### 7.2 Cross-Reference Validation

**You'll see:**
- "Traceability Index references CTQ-005, but CTQ Tree only contains CTQ-001 through CTQ-003"

**What this is:**
- Structural consistency check (IDs match across artifacts)
- Does NOT validate if the right CTQs are linked
- Does NOT judge if linkages are complete

**Why it matters:**
- Catches copy-paste errors or outdated references
- But does NOT replace human judgment of traceability adequacy

---

## 8. Summary: The Dashboard's Role

**The Dashboard is:**
- A teaching tool for understanding quality systems
- A diagnostic layer for structural visibility
- A proof harness for Meta-QMS principles
- A demonstration of risk-proportionate rigor

**The Dashboard is NOT:**
- A production quality management system
- A correctness validator or approval authority
- A replacement for human judgment
- A workflow orchestration tool

**Your role:**
- Interpret Dashboard signals as diagnostic information
- Apply human judgment for semantic validation
- Make strategic decisions about workflow and priorities
- Request expert review when structural readiness is achieved

**Together:**
- Dashboard provides visibility
- You provide judgment
- Quality emerges from both, not either alone

---

## 9. Further Reading

**For deeper understanding:**
- **META-QMS-CANON-V1.md** - Why quality systems must behave this way
- **WS-2-DEPENDENCY-PRINCIPLES.md** - Dependency logic design
- **WS-2-NON-GOALS.md** - What the Dashboard explicitly does not do
- **DEMO-SCENARIOS.md** - Concrete examples of Dashboard use

**For governance:**
- **WS-2-SCOPE-FREEZE.md** - What changes are and are not permitted
- **README.md Section 3** - Freeze and governance notices

---

**End of Usage Guide**

**Next:** See `DEMO-SCENARIOS.md` for concrete examples showing these principles in action.
