# WS-2 AI Containment (Quick Reference)
## For AI Coding Assistants Implementing WS-2

**Version:** 1.0
**Date:** 2025-12-17
**Purpose:** Short, copy-pastable rules preventing WS-2 principle violations

---

## ⚠️ CRITICAL: If You're an AI Assistant Implementing WS-2

**Read this BEFORE writing any WS-2 code.**

---

## The 5 Non-Negotiable Rules

### 1. WS-2 MUST Call Validator, MUST NOT Reproduce Logic

```python
# ✅ CORRECT
result = validator.validate_artifact(artifact_name, content, risk_level)
readiness = is_ready(result, risk_level)

# ❌ WRONG: Reimplementing validation
if len(content) < 500:  # Custom validation logic
    return {"ready": False}
```

**Why:** Single source of truth. Validation logic lives in WS-1 only.

---

### 2. WS-2 MUST Treat Readiness as Advisory Only

```python
# ✅ CORRECT: Recommend, don't block
if not readiness["ready"]:
    return {
        "ready": False,
        "reason": "Risk Register 40% complete (need 80%)",
        "can_proceed_anyway": True  # User can override
    }

# ❌ WRONG: Hard blocking
if not readiness["ready"]:
    raise HTTPException(403, "Cannot proceed")
```

**Why:** Teaching system. Diagnose and recommend, never enforce (except WS-6 stage gates).

---

### 3. WS-2 MUST Preserve Override Capability

```python
# ✅ CORRECT: Override path exists
@app.post("/api/generate/{artifact}")
def generate(artifact: str, intake_id: str, force: bool = False):
    readiness = check_readiness(artifact, intake_id)

    if not readiness["ready"] and not force:
        return {"warning": readiness["reason"], "can_force": True}

    # Proceed with generation (even if not ready)
    return generator.generate(artifact, intake_id)

# ❌ WRONG: No override path
@app.post("/api/generate/{artifact}")
def generate(artifact: str, intake_id: str):
    readiness = check_readiness(artifact, intake_id)

    if not readiness["ready"]:
        raise HTTPException(403, "Blocked")  # No escape hatch
```

**Why:** User agency. System recommends, user decides.

---

### 4. WS-2 MUST NOT Generate Suggestions Beyond "Recommended Next Artifact"

```python
# ✅ CORRECT: Structural recommendation
return {
    "next_action": "Complete Risk Register",
    "reason": "Risk Register at 40%, blocks 3 downstream artifacts"
}

# ❌ WRONG: Semantic guidance (belongs in WS-3)
return {
    "next_action": "Complete Risk Register",
    "how_to_fix": [
        "Add mitigation strategies to each risk",  # Semantic
        "Consider technical vs process controls",  # Semantic
        "Assign risk owners"  # Semantic
    ]
}
```

**Why:** WS-2 identifies problems, WS-3 suggests solutions. Don't conflate layers.

---

### 5. WS-2 MUST Include Epistemic Status in All Responses

```python
# ✅ CORRECT: Explicit epistemic markers
return {
    "artifact": "Risk Register",
    "ready": False,
    "completion": 0.4,
    "epistemic_status": "structural_only",  # Required
    "confidence_limits": [  # Required
        "Readiness based on structure, not semantic quality",
        "Completion ≠ correctness",
        "Expert review required for safety-critical systems"
    ],
    "readiness_basis": "structural"
}

# ❌ WRONG: No epistemic markers
return {
    "artifact": "Risk Register",
    "ready": False,
    "completion": 0.4
}
```

**Why:** Prevents misinterpretation of "ready" as "safe" or "approved".

---

## Quick Decision Tree

**Before adding any feature to WS-2:**

```
Does it call validator.validate_artifact()?
  NO → ❌ DON'T ADD (violates Rule #1)
  YES → Continue

Does it hard-block users?
  YES → ❌ DON'T ADD (violates Rule #2)
  NO → Continue

Does it remove override capability?
  YES → ❌ DON'T ADD (violates Rule #3)
  NO → Continue

Does it suggest *how* to fix issues?
  YES → ❌ DON'T ADD (violates Rule #4, belongs in WS-3)
  NO → Continue

Does it include epistemic_status field?
  NO → ❌ DON'T ADD (violates Rule #5)
  YES → ✅ OK to add
```

---

## Common Traps for AI Assistants

### Trap 1: "Helpful" Recalculation

```python
# ❌ TRAP
# "Let me recalculate completion % for better accuracy"
completion = calculate_my_own_completion(content)

# ✅ CORRECT
completion = validator.validate_artifact(...).completion_percent
```

---

### Trap 2: "Helpful" Hard Blocking

```python
# ❌ TRAP
# "Let me prevent users from making mistakes"
if not ready:
    raise BlockingError()

# ✅ CORRECT
if not ready:
    return {"ready": False, "can_proceed_anyway": True}
```

---

### Trap 3: "Helpful" Guidance

```python
# ❌ TRAP
# "Let me suggest how to fix this"
return {"suggestion": "Add these 5 mitigations..."}

# ✅ CORRECT
return {"suggestion": "Complete Risk Register", "reason": "Missing 3 mitigations"}
```

---

### Trap 4: "Performance" Caching

```python
# ❌ TRAP
# "Let me cache validation results for 5 minutes"
cache[artifact] = result
time.sleep(300)

# ✅ CORRECT
# Cache by file modification time or don't cache
mod_time = os.path.getmtime(artifact_path)
cache_key = (artifact, intake_id, risk_level, mod_time)
```

---

### Trap 5: "User Experience" UI Disablement

```tsx
// ❌ TRAP
// "Let me disable the button to prevent errors"
<button disabled={!readiness.ready}>Generate</button>

// ✅ CORRECT
<button disabled={false}>Generate</button>
{!readiness.ready && <Warning>{readiness.reason}</Warning>}
```

---

## If You Violate These Rules

**Your code will:**
- Break teaching principle (transforms system from diagnostic to prescriptive)
- Create silent divergence from WS-1 (validation logic drifts)
- Remove user agency (enforces instead of teaching)
- Conflate structural and semantic validation (creates false confidence)

**Result:** System becomes unsafe for its intended purpose (teaching what quality requires).

---

## When In Doubt

**Ask:**
- "Does this extend WS-1 or replace it?" (extend OK, replace forbidden)
- "Does this recommend or enforce?" (recommend OK, enforce forbidden)
- "Does this check structure or judge quality?" (structure OK, quality belongs in WS-3/expert review)

**If still unsure:** Don't add it. Propose it for review first.

---

## Further Reading

- **WS-2-SCOPE.md** - Full scope definition
- **WS-2-DEPENDENCY-PRINCIPLES.md** - 10 principles (updated with Dark-Matter patches)
- **WS-2-NON-GOALS.md** - 13 explicitly rejected behaviors
- **WS-1-TO-WS-2-CONTRACT.md** - Interface contract with WS-1
- **SETUP-AND-DEVELOPMENT-GUIDE.md Section 7** - System invariants

---

**Status:** Containment rules active.
**Enforcement:** Code review, integration tests, architectural principles.
**Violation Response:** Immediate correction, not merge.
