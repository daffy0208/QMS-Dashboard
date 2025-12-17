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

## Principle 2: Dependencies Are Directional, Not Bidirectional

### Definition

**If B depends on A, completing B does NOT retroactively validate A.**

### Example

- Risk Register → Verification Plan (dependency exists)
- Completing Verification Plan does NOT mean Risk Register is complete
- Risk Register completeness is measured by WS-1 validation, not by downstream artifacts existing

### Rationale

Prevents circular validation logic. Completeness is **intrinsic** (measured by WS-1), not **extrinsic** (inferred from dependencies).

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

## Summary: The 8 Principles

1. **"Ready" Is Risk-Proportionate** - R0 lenient, R3 strict
2. **Dependencies Are Directional** - B depends on A, not vice versa
3. **Soft Blocking, Not Hard Blocking** - Recommend, don't enforce
4. **Structural Dependencies, Not Semantic** - Cross-refs, not quality
5. **Dependency Graph Is Static, Readiness Is Dynamic** - Graph fixed, status computed
6. **No Hidden Thresholds** - All thresholds explicit and documented
7. **Placeholder Density Is Informational** - Context, not blocking
8. **Cross-Artifact Validation Is Additive** - Extend WS-1, don't replace

---

**Status:** Awaiting Dark-Matter review before implementation begins.
**Next Step:** Draft WS-2-NON-GOALS.md, then run Dark-Matter Mode on all 3 documents.
