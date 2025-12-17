# WS-2 Scope Definition
## Dependency Management & Smart Next Steps

**Version:** 1.0-draft
**Date:** 2025-12-17
**Status:** Pre-implementation (awaiting Dark-Matter review)

---

## What WS-2 Explicitly Does

### 1. Artifact Dependency Modeling

**Capability:** Define and represent artifact dependencies based on:
- Logical ordering (e.g., Risk Register should precede Verification Plan)
- Content prerequisites (e.g., Verification Plan references Risk Register IDs)
- Risk-level-specific requirements (R0 vs R3 artifact sets differ)

**Output:** Dependency graph (artifact → list of prerequisite artifacts)

**Not Included:** Enforcement of dependencies (diagnosis only)

---

### 2. Readiness Assessment

**Capability:** Determine if prerequisite artifacts are "ready enough" for downstream work.

**Inputs:**
- WS-1 validation results (`completion_percent`, `issues`, `valid` flag)
- Risk level (R0/R1/R2/R3)
- Artifact type

**Logic:**
- R0/R1: Lenient thresholds (warnings OK, lower completion % acceptable)
- R2/R3: Strict thresholds (no errors, higher completion % required)

**Output:** Boolean "ready" flag + diagnostic reasons if not ready

**Not Included:** Blocking artifact generation (recommendation only)

---

### 3. Next Action Recommendations

**Capability:** Suggest what user should work on next based on:
- Current artifact states (incomplete, complete, blocked)
- Dependency relationships
- Risk level priorities

**Output:** Ordered list of recommended actions (e.g., "Complete Risk Register to 80%", "Generate Verification Plan")

**Tone:** Suggestions, not commands. Teaching-oriented language.

**Not Included:** Prescriptive instructions, auto-generation, auto-completion

---

### 4. Dependency Health Visualization

**Capability:** Show user which artifacts are:
- Ready to work on (dependencies met)
- Blocked (waiting on prerequisites)
- In progress (partially complete)
- Complete (ready for downstream use)

**Output:** Status summary per artifact (JSON API response)

**Required Fields (Dark-Matter Patch #6):**
```json
{
  "artifact": "Risk Register",
  "ready": false,
  "completion": 0.4,
  "epistemic_status": "structural_only",
  "confidence_limits": [
    "Readiness based on structure, not semantic quality",
    "Completion ≠ correctness",
    "Expert review required for safety-critical systems"
  ],
  "can_proceed_anyway": true,
  "override_budget": {
    "count": 3,
    "status": "high",
    "warning": "Override count: 3 (high). Expect rework risk."
  },
  "placeholder_density": 0.15,
  "readiness_basis": "structural"
}
```

**Key Additions:**
- `epistemic_status`: Always "structural_only" (prevents misinterpretation as "safe" or "approved")
- `confidence_limits`: Fixed strings explaining what readiness does NOT mean
- `override_budget`: Tracks repeated overrides (informational, not blocking)

**Not Included:** Visual UI rendering (frontend concern, out of WS-2 scope)

---

## What WS-2 Explicitly Does NOT Do

### ❌ Not a Workflow Engine

**WS-2 does not:**
- Enforce workflow stages
- Require artifacts be completed in strict order
- Block users from working on artifacts out of order

**Rationale:** Users may have valid reasons to work non-linearly (e.g., drafting Verification Plan while Risk Register is incomplete to identify gaps).

**What WS-2 does instead:** Warn that downstream artifact may be incomplete due to missing prerequisites.

---

### ❌ Not an Auto-Fixer

**WS-2 does not:**
- Auto-generate missing artifacts
- Auto-complete incomplete artifacts
- Fill in placeholders
- Insert missing sections

**Rationale:** Teaching principle. System shows gaps, never fills them.

**What WS-2 does instead:** Recommend artifacts to complete, show what's missing.

---

### ❌ Not a Gating Mechanism (Except Stage Transitions)

**WS-2 does not:**
- Hard-block artifact generation based on dependencies
- Prevent users from proceeding if warnings exist (R0/R1)
- Enforce "must complete X before starting Y"

**Exception:** Stage transitions (Prototype → Development → Production) may have hard gates, but those are **WS-6 (Lifecycle) concerns**, not WS-2.

**Rationale:** Diagnostic, not enforcement. Validator measures, WS-2 recommends, user decides.

---

### ❌ Not a Semantic Validator

**WS-2 does not:**
- Judge content quality ("Is this risk assessment meaningful?")
- Verify logical coherence ("Does this mitigation address the risk?")
- Check adequacy ("Are 5 risks enough?")

**Rationale:** WS-2 extends WS-1 with cross-artifact checks (e.g., Risk Register IDs match Verification Plan references), but does NOT reimplement or override WS-1 structural validation.

**What WS-2 does instead:** Check cross-references (Risk-001 in Verification Plan exists in Risk Register), not content quality.

---

### ❌ Not a Lifecycle Manager

**WS-2 does not:**
- Track project maturity stages (Concept → Prototype → Production)
- Enforce stage-specific artifact requirements
- Manage stage transitions

**Rationale:** That's WS-6 (Lifecycle State Model). WS-2 focuses on artifact-to-artifact dependencies, not project stages.

**Separation of Concerns:**
- WS-2: "Risk Register is 40% complete, blocking Verification Plan"
- WS-6: "Cannot transition to Production stage until all artifacts complete"

---

## Boundary Cases

### Case 1: User Wants to Generate Verification Plan, But Risk Register Is 30% Complete

**WS-2 Behavior:**
- Check: Risk Register completion = 30%
- Threshold: R2 requires 80%+ for dependencies
- Output: `{"ready": false, "reason": "Risk Register only 30% complete (need 80%+)", "suggestion": "Complete Risk Register before generating Verification Plan"}`
- **Does NOT block:** User can still call artifact generation API if they choose

**Rationale:** WS-2 diagnoses and recommends, doesn't enforce.

---

### Case 2: User Completes Risk Register, What Should They Do Next?

**WS-2 Behavior:**
- Check: Risk Register now complete
- Query: What artifacts depend on Risk Register?
- Answer: Verification Plan, Control Plan, Traceability Index
- Prioritize: Verification Plan (highest priority per risk level)
- Output: `{"next_action": "Generate Verification Plan", "reason": "Risk Register complete, Verification Plan next in logical order"}`

**Rationale:** Teaching-oriented guidance, not commands.

---

### Case 3: User Has 5 Incomplete Artifacts, Which to Focus On?

**WS-2 Behavior:**
- Check: Which artifacts are blocking downstream work?
- Identify: Risk Register blocks 3 downstream artifacts
- Output: `{"priority": "Risk Register", "reason": "Completing Risk Register unblocks Verification Plan, Control Plan, Traceability Index"}`

**Rationale:** Help user prioritize, don't dictate.

---

## Integration with Other Workstreams

### WS-1 (Artifact Validation)
- **WS-2 depends on:** WS-1 validation results (`completion_percent`, `valid`, `issues`)
- **WS-2 calls:** `validator.validate_artifact()` to check prerequisite readiness
- **WS-2 does NOT:** Reimplement validation logic (per WS-1→WS-2 contract)

### WS-3 (Guidance Engine)
- **WS-3 depends on:** WS-2 dependency analysis (what's blocked, what's next)
- **WS-2 provides:** Structured readiness data for WS-3 to generate guidance
- **Separation:** WS-2 = "what's blocked", WS-3 = "how to fix it"

### WS-4 (Simulation Mode)
- **WS-4 depends on:** WS-2 readiness thresholds to predict expert review outcomes
- **WS-2 provides:** "Is this artifact set ready for review?" assessment
- **Separation:** WS-2 = readiness check, WS-4 = review prediction

### WS-6 (Lifecycle State Model)
- **WS-6 depends on:** WS-2 readiness data for stage transition gates
- **WS-2 provides:** Artifact completeness assessment
- **Separation:** WS-2 = artifact dependencies, WS-6 = project stage transitions

---

## Success Criteria

### WS-2 is successful when:

1. **Users know what to do next** - Clear, actionable recommendations
2. **Dependencies are visible** - Users understand why artifacts are blocked
3. **Teaching principle preserved** - Guidance, not enforcement
4. **No false confidence** - Readiness checks align with WS-1 validation
5. **Cross-artifact consistency** - Orphaned references detected (e.g., Risk-001 in Verification Plan but not in Risk Register)

### WS-2 has failed if:

1. **Users feel blocked unnecessarily** - System prevents valid workflows
2. **Teaching collapses into enforcement** - Hard gates added for R0/R1
3. **Validation logic diverges** - WS-2 reimplements WS-1 checks differently
4. **Auto-completion creeps in** - System starts filling gaps instead of showing them
5. **Semantic judgment appears** - WS-2 judges content quality, not just structure

---

## Out of Scope (Future Workstreams)

| Feature | Workstream |
|---------|-----------|
| Semantic validation | WS-3 (Guidance Engine) |
| Review simulation | WS-4 (Simulation Mode) |
| Lifecycle stages | WS-6 (Lifecycle State Model) |
| Metrics & analytics | Phase 9 (Intelligence) |
| Multi-user workflows | Phase 9 (Workflow Maturity) |
| Email notifications | Phase 9 (Workflow Maturity) |

---

## Key Principles (Alignment with WS-1)

1. **Diagnostic, Not Prescriptive** - Show gaps, never fill them
2. **Teaching, Not Enforcement** - Guide users, don't block them (except stage transitions in WS-6)
3. **Trust WS-1 Results** - Use validation outputs directly, don't reinterpret
4. **Risk-Proportionate Rigor** - R0/R1 lenient, R2/R3 strict
5. **No Hidden Assumptions** - Make readiness thresholds explicit in code + docs

---

**Status:** Awaiting Dark-Matter review before implementation begins.
**Next Step:** Draft WS-2-DEPENDENCY-PRINCIPLES.md and WS-2-NON-GOALS.md, then run Dark-Matter Mode.
