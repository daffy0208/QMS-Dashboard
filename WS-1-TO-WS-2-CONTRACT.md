# WS-1 → WS-2 Interface Contract
## What WS-2 Can Trust (and What It Must Not Reinterpret)

**Version:** 1.0
**Date:** 2025-12-17
**Purpose:** Explicit contract defining the interface between WS-1 (Artifact Validation) and WS-2 (Dependency Management)

---

## 1. Contract Scope

This document defines:
- What WS-2 **MAY trust** from WS-1 outputs
- What WS-2 **MUST NOT reinterpret** or recompute
- What WS-2 **MUST verify** before using
- What WS-2 **MUST preserve** from WS-1

**Violation Risk:** Reinterpreting WS-1 semantics creates silent divergence between diagnostic layer and decision layer, breaking system integrity.

---

## 2. What WS-2 MAY Trust

### 2.1 Validation Results Are Authoritative

**Contract:** `ValidationResult` objects returned by `validator.validate_artifact()` are **authoritative and immutable**.

**What This Means:**
- ✅ WS-2 can trust `valid` flag
- ✅ WS-2 can trust `completion_percent` (0.0 to 1.0)
- ✅ WS-2 can trust `issues` list (severity, section, message)
- ✅ WS-2 can trust `missing_sections` list
- ✅ WS-2 can trust `placeholder_count`

**What WS-2 MUST NOT Do:**
- ❌ Recalculate completion percentage
- ❌ Reinterpret issue severity
- ❌ Re-validate artifacts (call validator again? Yes. Reimplement validation logic? No.)
- ❌ Override `valid` flag based on "better" heuristics

**Example Valid Usage:**
```python
# WS-2 dependency manager
result = validator.validate_artifact("Risk Register", content, "R2")
if result.completion_percent >= 0.8:
    # Risk Register is "ready enough" for downstream artifacts
    return ["Verification Plan", "Control Plan"]  # Unlock dependencies
```

**Example Invalid Usage:**
```python
# ❌ DO NOT DO THIS
result = validator.validate_artifact("Risk Register", content, "R2")
# Recalculating completion based on different logic
my_completion = calculate_my_own_completion(content)  # VIOLATION
if my_completion >= 0.8:
    return downstream_artifacts
```

---

### 2.2 Severity Levels Have Specific Meanings

**Contract:** Issue severity (`error`, `warning`, `info`) has **semantic meaning** tied to risk level.

**Severity Semantics:**
- **`error`**: Blocks acceptance criteria for R1+ (strict rigor)
- **`warning`**: Teaching signal for R0/R1 (guidance, not blocking)
- **`info`**: Optional improvements (never blocking)

**What WS-2 MAY Do:**
- ✅ Use errors as indicators of "not ready for expert review"
- ✅ Use warnings as indicators of "has gaps but progression allowed"
- ✅ Count errors vs warnings for readiness thresholds

**What WS-2 MUST NOT Do:**
- ❌ Treat warnings as errors (collapses teaching into enforcement)
- ❌ Ignore errors for R2/R3 (breaks safety rigor)
- ❌ Create new severity levels (breaks 1:1 contract with WS-1)

**Example Valid Usage:**
```python
# WS-2 readiness check
error_count = sum(1 for issue in result.issues if issue.severity == "error")
warning_count = sum(1 for issue in result.issues if issue.severity == "warning")

if risk_level in ["R2", "R3"]:
    ready = (error_count == 0)  # Strict: no errors allowed
else:  # R0, R1
    ready = (error_count == 0 and warning_count <= 5)  # Lenient: warnings OK up to threshold
```

---

### 2.3 Acceptance Criteria Are The Source of Truth

**Contract:** `acceptance_criteria.json` defines what constitutes artifact completeness. WS-2 **MUST use this same source** for any completeness checks.

**What WS-2 MAY Do:**
- ✅ Read `acceptance_criteria.json` to understand artifact requirements
- ✅ Use criteria to determine dependency readiness thresholds
- ✅ Display criteria to users as "why this artifact isn't ready"

**What WS-2 MUST NOT Do:**
- ❌ Create parallel criteria definitions (duplicates source of truth)
- ❌ Infer unstated requirements from context
- ❌ Add "common sense" rules not in acceptance_criteria.json

**Example Valid Usage:**
```python
# WS-2 dependency manager checks criteria to understand dependencies
criteria = load_acceptance_criteria()
risk_register_criteria = criteria["artifacts"]["Risk Register"]["risk_levels"]["R2"]
required_sections = risk_register_criteria["required_sections"]

# Use to explain why dependency blocked
if "Risk Assessment" not in completed_sections:
    return f"Risk Register missing required section: Risk Assessment (per acceptance criteria R2)"
```

---

### 2.4 Placeholder Count Is Informational

**Contract:** `placeholder_count` is a **teaching signal**, not a blocking metric.

**What WS-2 MAY Do:**
- ✅ Display placeholder count to users
- ✅ Use as input to guidance tone (WS-3 integration)
- ✅ Use as input to simulation confidence (WS-4 integration)
- ✅ Warn users "high placeholder density suggests early stage"

**What WS-2 MUST NOT Do:**
- ❌ Block progression based on placeholder count alone
- ❌ Override `valid` flag due to placeholders (WS-1 already handles this)
- ❌ Create hard thresholds ("more than 3 placeholders = blocked")

**Rationale:** R0 explicitly allows placeholders. Blocking on count violates teaching principle.

---

## 3. What WS-2 MUST NOT Reinterpret

### 3.1 Completion Percentage Calculation

**Rule:** WS-2 MUST NOT recalculate `completion_percent` using different logic.

**Why:**
- WS-1 calculates completion based on:
  - Required sections present
  - Rules satisfied
  - Placeholder count (for R1+)
  - Issue severity distribution
- Recalculating breaks 1:1 contract between validator and acceptance criteria

**If WS-2 Needs Different Metric:**
- Create a **new metric** with a different name (e.g., `dependency_readiness_score`)
- Do NOT replace or override `completion_percent`

---

### 3.2 Validation Logic

**Rule:** WS-2 MUST NOT reimplement any validation checks from `validator.py`.

**Why:**
- Single source of truth prevents divergence
- Parallel implementations drift over time
- Validation rules may change (e.g., WS-1 expansion added 7 new methods)

**If WS-2 Needs Validation:**
- ✅ Call `validator.validate_artifact()` directly
- ❌ Copy validation logic into WS-2
- ❌ Create "simplified" validation for performance

**Exception:**
If WS-2 needs **new checks not in WS-1** (e.g., cross-artifact consistency), those are fair game—but they're WS-2 concerns, not WS-1 reinterpretations.

---

### 3.3 Warning-Only Semantics

**Rule:** WS-2 MUST NOT upgrade R0/R1 warnings to errors.

**Why:**
- R0/R1 are teaching modes (warnings guide, don't block)
- Upgrading warnings to errors collapses teaching into enforcement
- Users building low-risk systems must be able to learn without gatekeeping

**Valid Behavior:**
- ✅ Display warnings prominently to R0/R1 users
- ✅ Recommend fixing warnings before progressing
- ❌ Block progression due to warnings alone

---

## 4. What WS-2 MUST Verify Before Using

### 4.1 Risk Level Match

**Rule:** WS-2 MUST ensure it's using validation results for the **correct risk level**.

**Why:**
- Acceptance criteria differ per risk level (R0 vs R3)
- Using R3 validation results to judge R0 artifact = false strictness
- Using R0 validation results to judge R3 artifact = false leniency

**Verification:**
```python
# WS-2 dependency check
intake = load_intake(intake_id)
risk_level = intake.classification.risk_level  # e.g., "R2"

result = validator.validate_artifact("Risk Register", content, risk_level)
# ✅ Correct: validation matches intake risk level

# ❌ Incorrect: hardcoded risk level
result = validator.validate_artifact("Risk Register", content, "R3")
```

---

### 4.2 Artifact File Freshness

**Rule:** WS-2 MUST NOT cache validation results indefinitely. Artifact files may change between checks.

**Why:**
- Users edit artifacts manually
- Validator reads file content at validation time
- Stale validation results create false readiness signals

**Recommended Pattern:**
- Cache validation results **per artifact file modification time**
- Invalidate cache if file modified
- Or: Always re-validate on dependency check (simple, correct)

---

## 5. What WS-2 MUST Preserve

### 5.1 Teaching Principle

**Rule:** WS-2 dependency logic MUST NOT transform the system from "teaching" to "enforcement" for R0/R1.

**How to Preserve:**
- ✅ Show users **why** a dependency is blocked (diagnostic)
- ✅ Recommend actions to unblock (guidance)
- ❌ Hard-block generation without explanation (enforcement)
- ❌ Add new error severities that override R0/R1 warnings

**Example Valid UX:**
```
Cannot generate Verification Plan yet (recommendation):
- Risk Register is 40% complete (need 80%+)
- Missing sections: Risk Assessment, Mitigation Strategies
- 3 errors, 2 warnings

Suggested action: Complete Risk Register before generating Verification Plan.
```

**Example Invalid UX:**
```
❌ BLOCKED: Verification Plan generation disabled.
```

---

### 5.2 Validator Immutability

**Rule:** WS-2 MUST NOT modify artifacts as a side effect of dependency checks.

**Why:**
- Validator is a pure function (Invariant 3 from SETUP-AND-DEVELOPMENT-GUIDE.md)
- WS-2 dependency logic must also be pure (read-only)
- Mutation breaks auditability and user trust

**What WS-2 MAY Do:**
- ✅ Read artifact files
- ✅ Validate artifact content
- ✅ Return dependency readiness results

**What WS-2 MUST NOT Do:**
- ❌ Insert missing sections into artifacts
- ❌ Fix placeholders automatically
- ❌ Reformat artifact content

---

### 5.3 Single Source of Truth (acceptance_criteria.json)

**Rule:** WS-2 MUST NOT create parallel acceptance criteria or override WS-1 criteria.

**Why:**
- Divergent criteria = conflicting truth
- Users get mixed signals ("WS-1 says complete, WS-2 says incomplete")

**If WS-2 Has New Requirements:**
- Option A: Add to `acceptance_criteria.json` (preferred if structural)
- Option B: Create `dependency_criteria.json` for WS-2-specific concerns (e.g., cross-artifact consistency)
- Document clearly which criteria are WS-1 vs WS-2

---

## 6. Integration Points

### 6.1 WS-2 Calls WS-1 (Not Vice Versa)

**Architecture:**
```
WS-2 (Dependency Management)
    ↓ calls
WS-1 (Artifact Validation)
    ↓ reads
acceptance_criteria.json
```

**Never:**
```
WS-1 (Artifact Validation)
    ↓ calls
WS-2 (Dependency Management)  # ❌ Creates circular dependency
```

**Why:**
- WS-1 is foundational (measurement layer)
- WS-2 is higher-order (decision layer)
- Layering prevents circular dependencies

---

### 6.2 WS-2 May Extend, Not Replace

**Pattern:**
```python
# WS-2 dependency manager
def check_artifact_readiness(artifact_name, intake_id):
    # Step 1: Call WS-1 (foundational check)
    result = validator.validate_artifact(artifact_name, content, risk_level)

    # Step 2: WS-2-specific checks (cross-artifact)
    cross_artifact_issues = check_cross_references(artifact_name, intake_id)

    # Step 3: Combine (extend, don't replace)
    return {
        "validation": result,  # Preserve WS-1 results
        "dependencies": cross_artifact_issues  # Add WS-2 concerns
    }
```

**Invalid Pattern:**
```python
# ❌ DO NOT DO THIS
def check_artifact_readiness(artifact_name, intake_id):
    # Skipping WS-1, using custom logic
    my_validation = my_custom_validator(content)  # VIOLATION
    return my_validation
```

---

## 7. Examples: Valid vs Invalid WS-2 Usage

### Example 1: Dependency Blocking (Valid)

```python
# WS-2 dependency manager
def can_generate_artifact(artifact_name, intake_id):
    dependencies = get_dependencies(artifact_name)  # e.g., ["Risk Register"]

    for dep in dependencies:
        dep_content = read_artifact(dep, intake_id)
        dep_result = validator.validate_artifact(dep, dep_content, risk_level)

        # Use WS-1 validation results to determine readiness
        if dep_result.completion_percent < 0.8:
            return {
                "ready": False,
                "reason": f"{dep} only {dep_result.completion_percent:.0%} complete",
                "suggestion": f"Complete {dep} to at least 80% before generating {artifact_name}"
            }

    return {"ready": True}
```

**Why Valid:**
- Uses WS-1 validation results directly
- Doesn't recalculate completion
- Provides diagnostic + guidance (teaching principle)

---

### Example 2: Dependency Blocking (Invalid)

```python
# ❌ DO NOT DO THIS
def can_generate_artifact(artifact_name, intake_id):
    dependencies = get_dependencies(artifact_name)

    for dep in dependencies:
        dep_content = read_artifact(dep, intake_id)

        # Custom validation logic (VIOLATION)
        if len(dep_content) < 500:  # "Not enough content"
            return {"ready": False, "reason": "Dependency too short"}

        if "[TBD]" in dep_content:  # Custom placeholder check (VIOLATION)
            return {"ready": False, "reason": "Dependency has placeholders"}

    return {"ready": True}
```

**Why Invalid:**
- Reimplements validation logic (breaks single source of truth)
- Ignores risk-level-specific criteria (breaks R0/R1 teaching mode)
- No alignment with acceptance_criteria.json

---

### Example 3: Cross-Artifact Validation (Valid)

```python
# WS-2 adds NEW checks (not reinterpreting WS-1)
def validate_cross_references(intake_id):
    risk_register = read_artifact("Risk Register", intake_id)
    verification_plan = read_artifact("Verification Plan", intake_id)

    # Extract risk IDs from Risk Register
    risk_ids = extract_risk_ids(risk_register)  # e.g., ["R-001", "R-002"]

    # Extract risk IDs referenced in Verification Plan
    referenced_risks = extract_referenced_risks(verification_plan)

    # Check for orphaned references (WS-2 concern, not WS-1)
    orphaned = [r for r in referenced_risks if r not in risk_ids]

    if orphaned:
        return {
            "cross_artifact_issues": [
                f"Verification Plan references {r}, but {r} not in Risk Register"
                for r in orphaned
            ]
        }

    return {"cross_artifact_issues": []}
```

**Why Valid:**
- Adds NEW capability (cross-artifact consistency) not in WS-1
- Does NOT reimplement WS-1 validation logic
- Does NOT override WS-1 completion calculations
- Clearly labeled as WS-2 concern

---

## 8. Testing WS-2 Against This Contract

When building WS-2, verify compliance with this contract:

### 8.1 Unit Tests: Does WS-2 Call WS-1?

```python
def test_ws2_uses_ws1_validation():
    """WS-2 must call validator.validate_artifact(), not reimplement."""
    with mock.patch('artifacts.validator.ArtifactValidator.validate_artifact') as mock_validate:
        mock_validate.return_value = ValidationResult(valid=True, completion_percent=0.9, issues=[])

        # Call WS-2 dependency check
        result = dependency_manager.check_readiness("Verification Plan", "test_intake")

        # Assert WS-1 was called
        assert mock_validate.called, "WS-2 must call WS-1 validator"
```

---

### 8.2 Integration Tests: Does WS-2 Respect Warning-Only?

```python
def test_ws2_allows_r0_warnings():
    """WS-2 must not block R0 artifacts due to warnings."""
    # R0 artifact with warnings (no errors)
    result = validator.validate_artifact("Risk Register", r0_content, "R0")
    assert all(issue.severity == "warning" for issue in result.issues)

    # WS-2 should allow progression
    readiness = dependency_manager.check_readiness("Verification Plan", "test_intake_r0")
    assert readiness["ready"] == True, "WS-2 must allow R0 progression despite warnings"
```

---

### 8.3 Negative Tests: Does WS-2 Avoid Reinterpretation?

```python
def test_ws2_does_not_recalculate_completion():
    """WS-2 must not recalculate completion_percent."""
    # Get WS-1 result
    ws1_result = validator.validate_artifact("Risk Register", content, "R2")
    ws1_completion = ws1_result.completion_percent

    # WS-2 check
    ws2_result = dependency_manager.get_artifact_status("Risk Register", "test_intake")

    # Assert WS-2 uses WS-1 completion directly
    assert ws2_result["completion"] == ws1_completion, \
        "WS-2 must use WS-1 completion_percent, not recalculate"
```

---

## 9. Summary: The Contract in Three Rules

1. **Trust WS-1 Outputs:** Validation results are authoritative. Use them, don't reinterpret them.

2. **Preserve Teaching Principle:** R0/R1 use warnings (teaching), R2/R3 use errors (enforcement). WS-2 must honor this.

3. **Single Source of Truth:** `acceptance_criteria.json` defines completeness. WS-2 may extend (cross-artifact checks) but must not replace (parallel criteria).

---

## 10. Contract Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-17 | Initial contract based on WS-1 completion (Phase 8A) |

---

**Contract Status:** ✅ ACTIVE
**Enforced By:** Code review, integration tests, architectural principles
**Violation Response:** Document divergence, reconcile with WS-1 maintainer

**This contract is binding for all WS-2 development and all future workstreams building on WS-1.**
