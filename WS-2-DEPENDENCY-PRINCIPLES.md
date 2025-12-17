# WS-2 Dependency Principles
## How Dependencies Are Interpreted & What "Ready" Means

**Version:** 1.0-draft
**Date:** 2025-12-17
**Status:** Pre-implementation (awaiting Dark-Matter review)

---

## Core Question

**"When is Artifact A ready enough for Artifact B to proceed?"**

This document defines **readiness semantics** for dependency relationships.

---

## Principle 1: "Ready" Is Risk-Proportionate

### Definition

**"Ready" means different things at different risk levels.**

### Semantics by Risk Level

| Risk Level | Ready Threshold | Error Tolerance | Warning Tolerance | Rationale |
|------------|----------------|-----------------|-------------------|-----------|
| **R0** | 50% complete | Errors OK (up to 3) | Warnings OK (unlimited) | Learning mode: exploration allowed |
| **R1** | 60% complete | Errors OK (up to 2) | Warnings OK (unlimited) | Moderate: some gaps acceptable |
| **R2** | 80% complete | No errors | Warnings OK (up to 5) | Strict: must be substantially complete |
| **R3** | 90% complete | No errors | Warnings OK (up to 3) | Maximum: near-complete before proceeding |

### Rationale

- **R0/R1:** Users learning what quality requires → allow progression with gaps
- **R2/R3:** Safety-critical systems → enforce substantial completeness

### Implementation

```python
def is_ready(validation_result, risk_level):
    thresholds = {
        "R0": {"completion": 0.5, "max_errors": 3, "max_warnings": None},
        "R1": {"completion": 0.6, "max_errors": 2, "max_warnings": None},
        "R2": {"completion": 0.8, "max_errors": 0, "max_warnings": 5},
        "R3": {"completion": 0.9, "max_errors": 0, "max_warnings": 3},
    }

    threshold = thresholds[risk_level]
    error_count = sum(1 for i in validation_result.issues if i.severity == "error")
    warning_count = sum(1 for i in validation_result.issues if i.severity == "warning")

    # Check thresholds
    if validation_result.completion_percent < threshold["completion"]:
        return False
    if error_count > threshold["max_errors"]:
        return False
    if threshold["max_warnings"] and warning_count > threshold["max_warnings"]:
        return False

    return True
```

### Critical Invariant

**WS-2 MUST use WS-1's `completion_percent` directly.** Do NOT recalculate. (Per WS-1→WS-2 contract, Section 2.1)

---

### Principle 1.5: Artifact Volatility Modifier (Dark-Matter Patch #1)

**Issue Identified:** Treating all artifacts equally creates false confidence (draft-friendly artifacts) or unnecessary friction (rework-costly artifacts).

**"Ready" Is Not Purely Numerical—It's Also Artifact-Type Dependent**

### Artifact Volatility Classes

| Artifact Type | Volatility | Threshold Modifier | Rationale |
|---------------|-----------|-------------------|-----------|
| **Verification Plan** | Draft-friendly | -10% (R2: 70% → ready) | Cheap to draft early; helps identify Risk Register gaps |
| **Validation Plan** | Draft-friendly | -10% | Low rework cost; user testing plans evolve |
| **Assumptions Register** | Draft-friendly | -10% | Meant to be iterated; captures uncertainty |
| **Risk Register** | Foundation | No modifier (strict) | Downstream artifacts depend heavily; must be stable |
| **Traceability Index** | Rework-costly | +10% (R2: 90% → ready) | Expensive to rebuild if upstream changes |
| **Control Plan** | Rework-costly | +10% | Requires stable risk/verification baselines |
| **Quality Plan** | Foundation | No modifier (strict) | Project baseline; changes cascade |

### Formula

```python
def effective_threshold(base_threshold, artifact_volatility):
    """Apply volatility modifier to readiness threshold."""
    modifiers = {
        "draft_friendly": -0.1,   # Lower barrier (cheaper to iterate)
        "foundation": 0.0,         # No modifier (critical stability)
        "rework_costly": +0.1      # Higher barrier (expensive to redo)
    }

    modifier = modifiers.get(artifact_volatility, 0.0)
    return max(0.5, min(1.0, base_threshold + modifier))  # Clamp to [0.5, 1.0]
```

### Example

**R2 Verification Plan Generation:**
- Base threshold: 0.8 (R2)
- Volatility: draft-friendly (-0.1)
- Effective threshold: **0.7 (70%)**

**R2 Traceability Index Generation:**
- Base threshold: 0.8 (R2)
- Volatility: rework-costly (+0.1)
- Effective threshold: **0.9 (90%)**

### Storage

Volatility classes stored in `artifact_volatility.json`:

```json
{
  "artifacts": {
    "Verification Plan": "draft_friendly",
    "Risk Register": "foundation",
    "Traceability Index": "rework_costly"
  }
}
```

### Rationale

- **Draft-friendly:** Early generation helps users discover gaps (teaching principle)
- **Foundation:** Stability matters more than early access
- **Rework-costly:** Wait until prerequisites solid to avoid expensive rework

---

## Principle 2: Dependencies Are Directional, Not Bidirectional

### Definition

**If B depends on A, completing B does NOT retroactively validate A.**

### Example

- Risk Register → Verification Plan (dependency exists)
- Completing Verification Plan does NOT mean Risk Register is complete
- Risk Register completeness is measured by WS-1 validation, not by downstream artifacts existing

### Rationale

Prevents circular validation logic. Completeness is **intrinsic** (measured by WS-1), not **extrinsic** (inferred from dependencies).

### Principle 2.5: No Downstream→Upstream Readiness Scoring (Dark-Matter Patch #5)

**Issue Identified:** Circular dependency risk when readiness depends on downstream existence.

**Rule:** Cross-references may only point **upstream → downstream** for readiness scoring. Downstream → upstream cross-refs are **informational drift only**, never affect readiness.

**Example Loop to Prevent:**
- "Verification Plan readiness depends on Risk Register"
- "Risk Register completeness judged by having mitigations tied to verification"
- If WS-2 checks both directions for readiness, implicit cycle created

**Valid Pattern:**
```python
# ✅ Upstream → Downstream check (affects readiness)
def check_verification_plan_readiness(intake_id):
    risk_register_ready = check_readiness("Risk Register", intake_id)

    if not risk_register_ready:
        return {"ready": False, "reason": "Risk Register not ready"}

    return {"ready": True}
```

**Invalid Pattern:**
```python
# ❌ Downstream → Upstream check (creates cycle)
def check_risk_register_completeness(intake_id):
    verification_plan_exists = artifact_exists("Verification Plan", intake_id)

    # WRONG: judging upstream by downstream existence
    if verification_plan_exists:
        return {"complete": True}  # Circular inference

    return {"complete": False}
```

**Informational Drift Check (Allowed):**
```python
# ✅ Downstream → Upstream drift detection (informational only)
def detect_drift(intake_id):
    # Check if downstream references match upstream content
    risks_in_register = extract_risk_ids("Risk Register", intake_id)
    risks_in_verification = extract_risk_refs("Verification Plan", intake_id)

    orphaned = [r for r in risks_in_verification if r not in risks_in_register]

    if orphaned:
        return {
            "drift_warning": f"Verification Plan references {orphaned}, not in Risk Register",
            "affects_readiness": False  # Informational only
        }

    return {"drift_warning": None}
```

**Key:** Downstream artifacts can **inform** about drift but NEVER determine upstream readiness.

---

### Anti-Pattern to Avoid

```python
# ❌ DO NOT DO THIS
def is_risk_register_complete(intake_id):
    # Checking if downstream artifacts exist to infer completeness
    verification_plan_exists = artifact_exists("Verification Plan", intake_id)
    control_plan_exists = artifact_exists("Control Plan", intake_id)

    if verification_plan_exists and control_plan_exists:
        return True  # WRONG: completeness inferred from downstream

    return False
```

**Correct Pattern:**

```python
# ✅ CORRECT
def is_risk_register_complete(intake_id, risk_level):
    content = read_artifact("Risk Register", intake_id)
    result = validator.validate_artifact("Risk Register", content, risk_level)
    return is_ready(result, risk_level)
```

---

## Principle 3: Soft Blocking, Not Hard Blocking

### Definition

**WS-2 recommends, does not enforce.**

### Behavior

When a dependency is not ready:
- ✅ Return diagnostic message explaining why
- ✅ Suggest completing prerequisite first
- ❌ Throw exception to prevent generation
- ❌ Return HTTP 403 Forbidden

### Example API Response

```json
{
  "artifact": "Verification Plan",
  "ready_to_generate": false,
  "reason": "Risk Register only 40% complete (need 80%+ for R2)",
  "blocking_dependencies": [
    {
      "artifact": "Risk Register",
      "current_completion": 0.4,
      "required_completion": 0.8,
      "issues": [
        {"severity": "error", "message": "Missing Risk Assessment section"},
        {"severity": "error", "message": "Expected at least 3 risks, found 1"}
      ]
    }
  ],
  "suggestion": "Complete Risk Register before generating Verification Plan",
  "can_proceed_anyway": true,
  "warning": "Generating Verification Plan now may result in incomplete artifact"
}
```

### Key: `can_proceed_anyway: true`

**Users can override recommendations.** WS-2 does NOT block.

### Rationale

- Users may have valid reasons to work non-linearly
- Strict blocking breaks exploratory workflows
- Teaching principle: guide, don't control

---

## Principle 4: Structural Dependencies, Not Semantic Dependencies

### Definition

**WS-2 checks cross-references (structure), not content quality (semantics).**

### What WS-2 Checks

✅ **Structural Consistency:**
- Risk-001 referenced in Verification Plan → exists in Risk Register
- REQ-005 in Traceability Index → exists in CTQ Tree
- Test case VER-003 references Risk-002 → Risk-002 exists

❌ **Semantic Quality:**
- Is the mitigation for Risk-001 adequate?
- Does Test VER-003 actually test Risk-002?
- Are there enough risks for this system?

### Example: Valid WS-2 Check

```python
# ✅ Valid: Cross-reference check (structural)
def check_cross_references(intake_id):
    risk_register = read_artifact("Risk Register", intake_id)
    verification_plan = read_artifact("Verification Plan", intake_id)

    # Extract risk IDs
    risk_ids = extract_risk_ids(risk_register)  # ["R-001", "R-002", "R-003"]
    referenced_risks = extract_risk_references(verification_plan)  # ["R-001", "R-999"]

    # Find orphaned references
    orphaned = [r for r in referenced_risks if r not in risk_ids]

    if orphaned:
        return {
            "cross_reference_issues": [
                f"Verification Plan references {r}, but {r} not found in Risk Register"
                for r in orphaned
            ]
        }

    return {"cross_reference_issues": []}
```

### Example: Invalid WS-2 Check

```python
# ❌ Invalid: Semantic judgment (belongs in WS-3 or expert review)
def check_risk_quality(risk_register):
    risks = extract_risks(risk_register)

    for risk in risks:
        # Judging content quality (WRONG: this is semantic, not structural)
        if "TBD" in risk["mitigation"]:
            return {"semantic_issue": "Mitigation not specific enough"}

        if len(risk["description"]) < 50:
            return {"semantic_issue": "Description too short"}

    return {"semantic_issue": None}
```

**Why Invalid:** Judging "specific enough" or "too short" is semantic. WS-1 already checks placeholders. WS-2 adds cross-references, not quality judgments.

---

## Principle 5: Dependency Graph Is Static, Readiness Is Dynamic

### Definition

**Dependencies don't change, but readiness does.**

### Static: Dependency Graph

```json
{
  "dependencies": {
    "Verification Plan": ["Risk Register", "CTQ Tree"],
    "Control Plan": ["Risk Register"],
    "Traceability Index": ["CTQ Tree", "Risk Register", "Verification Plan"]
  }
}
```

This graph is **fixed** and defined in `dependencies.json`. It doesn't change based on artifact content.

### Dynamic: Readiness Status

```json
{
  "readiness": {
    "Risk Register": {"ready": true, "completion": 0.95},
    "CTQ Tree": {"ready": false, "completion": 0.4},
    "Verification Plan": {"ready": false, "reason": "CTQ Tree not ready"}
  }
}
```

This status is **computed** each time based on WS-1 validation results.

### Rationale

- Dependency graph = **domain knowledge** (what logically depends on what)
- Readiness = **runtime state** (what's actually complete right now)

### Implementation

```python
# Static: Load once at startup
DEPENDENCIES = load_dependency_graph("dependencies.json")

# Dynamic: Compute on demand
def get_artifact_readiness(artifact_name, intake_id, risk_level):
    prerequisites = DEPENDENCIES[artifact_name]

    for prereq in prerequisites:
        content = read_artifact(prereq, intake_id)
        result = validator.validate_artifact(prereq, content, risk_level)

        if not is_ready(result, risk_level):
            return {
                "ready": False,
                "blocking_artifact": prereq,
                "reason": f"{prereq} only {result.completion_percent:.0%} complete"
            }

    return {"ready": True}
```

---

## Principle 6: No Hidden Thresholds

### Definition

**All readiness thresholds must be explicit in code and documentation.**

### What This Means

❌ **Hidden Heuristics:**
```python
# ❌ Magic number, no documentation
if completion > 0.75:  # Why 0.75? Where did this come from?
    return True
```

✅ **Explicit Thresholds:**
```python
# ✅ Thresholds documented and configurable
READINESS_THRESHOLDS = {
    "R0": 0.5,  # Learning mode: 50% sufficient
    "R1": 0.6,  # Moderate: 60% required
    "R2": 0.8,  # Strict: 80% required
    "R3": 0.9   # Maximum: 90% required
}

if completion > READINESS_THRESHOLDS[risk_level]:
    return True
```

### Why This Matters

- Users need to understand why artifacts are blocked
- Future maintainers need to know where thresholds come from
- Thresholds may need tuning based on user feedback

### Documentation Requirement

Every threshold must have:
1. **Numeric value** (e.g., 0.8)
2. **Rationale** (e.g., "R2 requires substantial completeness")
3. **Location** (e.g., in `READINESS_THRESHOLDS` constant)

---

## Principle 7: Placeholder Density Is Informational, Not Blocking

### Definition

**Placeholder count informs readiness tone, but never blocks progression.**

### Usage

```python
def get_readiness_confidence(validation_result):
    """Calculate confidence in readiness assessment based on placeholder density."""
    placeholder_density = validation_result.placeholder_count / max(1, len(validation_result.content))

    if placeholder_density > 0.3:
        return {
            "confidence": "low",
            "reason": "High placeholder density (30%+) suggests artifact is structurally complete but conceptually early"
        }
    elif placeholder_density > 0.1:
        return {
            "confidence": "medium",
            "reason": "Some placeholders remain (10-30%)"
        }
    else:
        return {
            "confidence": "high",
            "reason": "No significant placeholders"
        }
```

### What This Does NOT Do

❌ Block progression due to placeholder count
❌ Override `is_ready()` based on placeholders (WS-1 already handles this)

### What This DOES Do

✅ Add context to readiness assessment ("structurally ready but conceptually early")
✅ Feed guidance tone in WS-3 ("consider filling in placeholders before proceeding")

---

## Principle 8: Cross-Artifact Validation Is Additive

### Definition

**WS-2 extends WS-1, does not replace it.**

### Pattern

```python
def full_readiness_check(artifact_name, intake_id, risk_level):
    # Step 1: WS-1 validation (foundational)
    content = read_artifact(artifact_name, intake_id)
    ws1_result = validator.validate_artifact(artifact_name, content, risk_level)

    # Step 2: WS-2 dependency checks (additive)
    dependency_issues = check_dependencies(artifact_name, intake_id, risk_level)
    cross_ref_issues = check_cross_references(intake_id)

    # Step 3: Combine (preserve WS-1, add WS-2)
    return {
        "validation": ws1_result,  # Preserve WS-1 results
        "dependencies": dependency_issues,  # Add WS-2 concerns
        "cross_references": cross_ref_issues,
        "overall_ready": ws1_result.valid and not dependency_issues
    }
```

### Anti-Pattern

```python
# ❌ DO NOT DO THIS
def full_readiness_check(artifact_name, intake_id, risk_level):
    # Skipping WS-1, only doing WS-2 checks
    dependency_issues = check_dependencies(artifact_name, intake_id, risk_level)

    if not dependency_issues:
        return {"ready": True}  # WRONG: ignored WS-1 validation

    return {"ready": False}
```

**Why Invalid:** WS-1 validation is foundational. WS-2 extends but never replaces.

---

## Principle 9: Warning Taxonomy (Dark-Matter Patch #2)

**Issue Identified:** "≤5 warnings" is brittle unless warning categories are normalized. Not all warnings are equal.

**Rule:** WS-2 may count warnings by **type** (from WS-1) without reinterpreting content.

### Warning Types (From WS-1)

WS-1 `ValidationIssue` should include `warning_type` field:

```python
class ValidationIssue:
    severity: Literal["error", "warning", "info"]
    warning_type: Optional[Literal[
        "placeholder_density",    # Placeholders remain
        "missing_optional",       # Optional section missing
        "weak_structure",         # Structure exists but minimal
        "other"                   # Uncategorized
    ]]
    section: str
    message: str
    suggestion: str
```

### WS-2 Usage

```python
def assess_warning_severity(validation_result, risk_level):
    """Count warnings by type to determine readiness impact."""
    warnings_by_type = {
        "placeholder_density": 0,
        "missing_optional": 0,
        "weak_structure": 0,
        "other": 0
    }

    for issue in validation_result.issues:
        if issue.severity == "warning":
            wtype = issue.warning_type or "other"
            warnings_by_type[wtype] += 1

    # Risk-specific thresholds
    if risk_level in ["R2", "R3"]:
        # Strict: placeholders matter more
        if warnings_by_type["placeholder_density"] > 3:
            return {"warning_concern": "high", "reason": "Placeholder density warnings exceed threshold"}

    # Total warning count (existing logic)
    total_warnings = sum(warnings_by_type.values())
    max_warnings = {"R0": None, "R1": None, "R2": 5, "R3": 3}[risk_level]

    if max_warnings and total_warnings > max_warnings:
        return {"warning_concern": "high", "reason": f"{total_warnings} warnings exceed {max_warnings}"}

    return {"warning_concern": "acceptable"}
```

### Rationale

- Not all warnings are equal: placeholder warnings more critical for R2/R3
- Allows nuanced readiness assessment without semantic judgment
- WS-2 counts by type, does NOT reinterpret warning content

---

## Principle 10: Threshold Calibration Policy (Dark-Matter Patch #7)

**Issue Identified:** Thresholds (50/60/80/90) lack justification and evolution plan. What happens when real projects don't fit?

**Rule:** Thresholds are **defaults**, stored in versioned file, changed via explicit PR with documented rationale.

### Calibration File Structure

**File:** `readiness_thresholds.json`

```json
{
  "version": "1.0",
  "last_updated": "2025-12-17",
  "rationale": "Initial thresholds based on teaching principle (R0/R1 lenient, R2/R3 strict)",
  "risk_levels": {
    "R0": {
      "completion": 0.5,
      "max_errors": 3,
      "max_warnings": null,
      "notes": "Learning mode: exploration allowed"
    },
    "R1": {
      "completion": 0.6,
      "max_errors": 2,
      "max_warnings": null,
      "notes": "Moderate: some gaps acceptable"
    },
    "R2": {
      "completion": 0.8,
      "max_errors": 0,
      "max_warnings": 5,
      "notes": "Strict: must be substantially complete"
    },
    "R3": {
      "completion": 0.9,
      "max_errors": 0,
      "max_warnings": 3,
      "notes": "Maximum: near-complete before proceeding"
    }
  },
  "tuning_metrics": {
    "false_ready_rate": "TBD",
    "false_not_ready_rate": "TBD",
    "override_rate": "TBD",
    "rework_rate": "TBD"
  }
}
```

### Calibration Process

**When to Tune:**
1. **False "ready":** Users generate artifacts that turn out incomplete (measured by expert review rejections)
2. **False "not ready":** Users override dependencies frequently and succeed (measured by override rate vs rework rate)
3. **User feedback:** Explicit reports of "too lenient" or "too strict"

**How to Tune:**
1. Collect metrics (override rate, rework rate, review rejection rate)
2. Propose threshold change in PR with rationale + data
3. Update `readiness_thresholds.json` with new version number
4. Document change in version history section

**Version History Example:**
```json
{
  "version": "1.1",
  "last_updated": "2025-03-15",
  "changes": [
    {
      "threshold": "R2.completion",
      "old_value": 0.8,
      "new_value": 0.75,
      "rationale": "R2 override rate was 45%; users consistently succeeded with 75%+ completion",
      "data": "50 R2 projects: 42 overrides, 39 succeeded with <80% but >75%"
    }
  ]
}
```

### Rationale

- Thresholds are hypotheses, not laws
- Data-driven tuning prevents dogma
- Explicit versioning prevents silent drift
- Users can see why thresholds exist and how they evolved

---

## Summary: The 10 Principles (Updated with Dark-Matter Patches)

1. **"Ready" Is Risk-Proportionate** - R0 lenient, R3 strict
   - 1.5: **Artifact Volatility Modifier** - Draft-friendly (-10%), foundation (0%), rework-costly (+10%)

2. **Dependencies Are Directional** - B depends on A, not vice versa
   - 2.5: **No Downstream→Upstream Readiness Scoring** - Drift detection OK, readiness inference forbidden

3. **Soft Blocking, Not Hard Blocking** - Recommend, don't enforce

4. **Structural Dependencies, Not Semantic** - Cross-refs, not quality

5. **Dependency Graph Is Static, Readiness Is Dynamic** - Graph fixed, status computed

6. **No Hidden Thresholds** - All thresholds explicit and documented

7. **Placeholder Density Is Informational** - Context, not blocking

8. **Cross-Artifact Validation Is Additive** - Extend WS-1, don't replace

9. **Warning Taxonomy** - Count warnings by type (placeholder_density, missing_optional, weak_structure, other)

10. **Threshold Calibration Policy** - Thresholds stored in versioned file, tuned via data + PR

---

**Status:** Dark-Matter patches applied (Patches #1, #2, #5, #7).
**Next Step:** Apply remaining patches to WS-2-SCOPE.md and WS-2-NON-GOALS.md, then finalize.
