# WS-2 Non-Goals
## Explicitly Rejected Behaviors

**Version:** 1.0-draft
**Date:** 2025-12-17
**Status:** Pre-implementation (awaiting Dark-Matter review)

---

## Purpose of This Document

This document lists **behaviors WS-2 must NEVER exhibit**, even if they seem "helpful" or "obvious improvements."

Each non-goal includes:
- **Temptation:** Why someone might want to add this
- **Why Rejected:** Why it violates system principles
- **Alternative:** What to do instead

---

## Non-Goal 1: Auto-Generation of Missing Artifacts

### Temptation

"If Risk Register is complete and Verification Plan doesn't exist, just generate it automatically."

### Why Rejected

**Violates teaching principle.** User must consciously decide when to proceed.

### What Happens Instead

```json
{
  "next_action": "Generate Verification Plan",
  "reason": "Risk Register is complete (90%), Verification Plan not started",
  "suggestion": "Click 'Generate Verification Plan' when ready"
}
```

User clicks button. System does NOT auto-generate.

### Code to Avoid

```python
# ❌ DO NOT DO THIS
def check_next_steps(intake_id):
    if risk_register_complete() and not verification_plan_exists():
        # Auto-generating (VIOLATION)
        generate_artifact("Verification Plan", intake_id)
        return "Verification Plan auto-generated"
```

---

## Non-Goal 2: Auto-Completion of Incomplete Artifacts

### Temptation

"Risk Register is 80% complete with 3 placeholders. Let's fill them in with AI-generated content."

### Why Rejected

**Violates teaching principle.** System shows gaps, never fills them.

### What Happens Instead

```json
{
  "artifact": "Risk Register",
  "completion": 0.8,
  "issues": [
    {"severity": "warning", "message": "3 placeholders remaining"},
    {"severity": "info", "message": "Consider filling in: Risk-002 mitigation, Risk-003 owner, Risk-004 likelihood"}
  ],
  "suggestion": "Complete placeholders before proceeding"
}
```

User fills them in manually. System does NOT auto-complete.

### Code to Avoid

```python
# ❌ DO NOT DO THIS
def improve_artifact(artifact_name, content):
    placeholders = find_placeholders(content)

    for placeholder in placeholders:
        # AI-generating content to fill placeholder (VIOLATION)
        generated_content = ai_generate(placeholder.context)
        content = content.replace(placeholder.text, generated_content)

    save_artifact(artifact_name, content)
```

---

## Non-Goal 3: Hard Blocking Based on Dependencies

### Temptation

"Risk Register is only 40% complete. Block Verification Plan generation entirely."

### Why Rejected

**Breaks exploratory workflows.** User may want to draft Verification Plan to identify gaps in Risk Register.

### What Happens Instead

```json
{
  "artifact": "Verification Plan",
  "ready_to_generate": false,
  "reason": "Risk Register only 40% complete (need 80%+ for R2)",
  "can_proceed_anyway": true,
  "warning": "Generating now may result in incomplete Verification Plan"
}
```

If user calls `POST /api/generate` anyway, it succeeds (with warning logged).

### API Behavior

```python
# ✅ CORRECT
@app.post("/api/generate/{artifact_name}")
def generate_artifact_endpoint(artifact_name: str, intake_id: str):
    readiness = check_readiness(artifact_name, intake_id)

    if not readiness["ready"]:
        # Log warning, but DO NOT block
        logger.warning(f"Generating {artifact_name} despite dependencies not ready: {readiness['reason']}")

    # Proceed with generation
    artifact = generator.generate(artifact_name, intake_id)
    return {"artifact": artifact, "warning": readiness.get("warning")}
```

### API Behavior to Avoid

```python
# ❌ DO NOT DO THIS
@app.post("/api/generate/{artifact_name}")
def generate_artifact_endpoint(artifact_name: str, intake_id: str):
    readiness = check_readiness(artifact_name, intake_id)

    if not readiness["ready"]:
        # Hard blocking (VIOLATION)
        raise HTTPException(status_code=403, detail="Dependencies not met")

    artifact = generator.generate(artifact_name, intake_id)
    return {"artifact": artifact}
```

---

## Non-Goal 4: Prescriptive Language in Responses

### Temptation

"Tell user 'You must complete Risk Register before proceeding.'"

### Why Rejected

**Prescriptive, not descriptive.** System teaches, doesn't command.

### Good Language (Descriptive)

```json
{
  "message": "Risk Register is 40% complete. Verification Plan requires Risk Register at 80%+.",
  "suggestion": "Consider completing Risk Register before generating Verification Plan."
}
```

### Bad Language (Prescriptive)

```json
{
  "message": "You must complete Risk Register to 80% before you can generate Verification Plan.",
  "command": "Complete Risk Register now."
}
```

### Linguistic Rules

| ❌ Avoid | ✅ Use Instead |
|---------|---------------|
| "You must..." | "Recommended: ..." |
| "Required to..." | "Suggested: ..." |
| "Cannot proceed until..." | "Ready to proceed after..." |
| "Fix this now." | "Consider addressing: ..." |
| "Blocked." | "Not ready: [reason]" |

---

## Non-Goal 5: Revalidating Artifacts (Duplicating WS-1)

### Temptation

"Let's add custom validation in WS-2 to check if Risk Register has enough detail."

### Why Rejected

**Violates single source of truth.** WS-1 is validation layer. WS-2 extends (cross-refs) but never replaces.

### What WS-2 Should Do

```python
# ✅ CORRECT: Call WS-1, extend with cross-ref check
def check_artifact_readiness(artifact_name, intake_id, risk_level):
    # Step 1: Use WS-1 validation
    result = validator.validate_artifact(artifact_name, content, risk_level)

    # Step 2: Add WS-2 cross-reference check
    cross_ref_issues = check_cross_references(intake_id)

    # Step 3: Combine
    return {
        "validation": result,  # WS-1 results
        "cross_references": cross_ref_issues  # WS-2 addition
    }
```

### What WS-2 Should NOT Do

```python
# ❌ DO NOT DO THIS: Custom validation logic
def check_artifact_readiness(artifact_name, intake_id, risk_level):
    content = read_artifact(artifact_name, intake_id)

    # Custom validation (VIOLATION: reimplementing WS-1)
    if len(content) < 500:
        return {"valid": False, "reason": "Content too short"}

    if content.count("Risk-") < 5:
        return {"valid": False, "reason": "Not enough risks"}

    return {"valid": True}
```

**Why Invalid:** Parallel validation logic diverges from WS-1. Always call `validator.validate_artifact()`.

---

## Non-Goal 6: Semantic Judgment of Content Quality

### Temptation

"Risk-001 mitigation says 'We'll monitor it.' That's not a real mitigation. Flag it."

### Why Rejected

**Semantic judgment belongs in expert review or WS-3 (Guidance Engine), not WS-2.**

### What WS-2 Checks (Structural)

✅ Risk-001 exists in Risk Register
✅ Risk-001 has a mitigation field (not empty)
✅ Risk-001 referenced in Verification Plan → matches Risk Register ID

### What WS-2 Does NOT Check (Semantic)

❌ Is the mitigation adequate?
❌ Is "monitor it" a good strategy?
❌ Does this mitigation address the root cause?

### Example: Valid WS-2 Check

```python
# ✅ Valid: Structural cross-reference
def check_risk_references(intake_id):
    risks_in_register = extract_risk_ids("Risk Register", intake_id)
    risks_in_verification = extract_risk_references("Verification Plan", intake_id)

    orphaned = [r for r in risks_in_verification if r not in risks_in_register]

    if orphaned:
        return {"cross_ref_issue": f"Verification Plan references {orphaned}, not in Risk Register"}

    return {"cross_ref_issue": None}
```

### Example: Invalid WS-2 Check

```python
# ❌ Invalid: Semantic judgment
def check_mitigation_quality(risk_register):
    risks = extract_risks(risk_register)

    for risk in risks:
        mitigation = risk["mitigation"].lower()

        # Judging content (VIOLATION: this is semantic)
        if "monitor" in mitigation or "watch" in mitigation:
            return {"quality_issue": f"{risk['id']} mitigation too vague"}

    return {"quality_issue": None}
```

---

## Non-Goal 7: Inferring Missing Requirements from Context

### Temptation

"This is a medical device (from intake answers). Let's require FDA-specific artifacts even though acceptance_criteria.json doesn't mention them."

### Why Rejected

**Violates single source of truth.** If requirement isn't in `acceptance_criteria.json`, it doesn't exist.

### What Happens Instead

If FDA artifacts are needed:
1. Add them to `acceptance_criteria.json` explicitly
2. Update artifact generator to produce them
3. Update WS-1 validation to check them

WS-2 then uses updated criteria. WS-2 does NOT infer new requirements.

### Code to Avoid

```python
# ❌ DO NOT DO THIS
def get_required_artifacts(intake):
    base_artifacts = ["Quality Plan", "Risk Register", ...]

    # Inferring requirements from context (VIOLATION)
    if "medical" in intake.project_description.lower():
        base_artifacts.append("FDA 510k Summary")  # Not in acceptance_criteria.json

    if intake.risk_level == "R3":
        base_artifacts.append("Safety Case")  # Not in acceptance_criteria.json

    return base_artifacts
```

**Why Invalid:** Requirements must be explicit in `acceptance_criteria.json`, not inferred.

---

## Non-Goal 8: Workflow Stage Management

### Temptation

"Track project stages (Concept → Prototype → Development → Production) in WS-2."

### Why Rejected

**That's WS-6 (Lifecycle State Model).** WS-2 handles artifact-to-artifact dependencies, not project stages.

### Separation of Concerns

| Concern | Workstream |
|---------|------------|
| Artifact dependencies | WS-2 |
| Project stages | WS-6 |
| Expert review | Phase 5 (existing) |
| Simulation | WS-4 |
| Guidance | WS-3 |

### What WS-2 Does

- "Risk Register is 40% complete, blocking Verification Plan"

### What WS-6 Does (Future)

- "Cannot transition to Production stage until all artifacts complete"

**WS-2 provides data TO WS-6, but does NOT manage stages itself.**

---

## Non-Goal 9: Caching Validation Results Indefinitely

### Temptation

"Cache validation results to avoid re-running validator on every dependency check."

### Why Rejected

**Artifact files change.** Stale cache creates false readiness signals.

### What to Do Instead

**Option A: No caching (simple, correct)**

```python
def check_readiness(artifact_name, intake_id, risk_level):
    # Always fresh: read file, validate
    content = read_artifact(artifact_name, intake_id)
    return validator.validate_artifact(artifact_name, content, risk_level)
```

**Option B: Cache by file modification time**

```python
_validation_cache = {}

def check_readiness_cached(artifact_name, intake_id, risk_level):
    file_path = get_artifact_path(artifact_name, intake_id)
    mod_time = os.path.getmtime(file_path)
    cache_key = (artifact_name, intake_id, risk_level, mod_time)

    if cache_key in _validation_cache:
        return _validation_cache[cache_key]

    content = read_artifact(artifact_name, intake_id)
    result = validator.validate_artifact(artifact_name, content, risk_level)

    _validation_cache[cache_key] = result
    return result
```

**Option C: Time-based cache (dangerous)**

```python
# ⚠️ RISKY: Time-based cache (user edits may be missed)
def check_readiness_timed_cache(artifact_name, intake_id, risk_level):
    cache_key = (artifact_name, intake_id, risk_level)
    cached_result, timestamp = _cache.get(cache_key, (None, 0))

    # Cache valid for 60 seconds
    if cached_result and time.time() - timestamp < 60:
        return cached_result

    # Re-validate
    content = read_artifact(artifact_name, intake_id)
    result = validator.validate_artifact(artifact_name, content, risk_level)

    _cache[cache_key] = (result, time.time())
    return result
```

**Recommendation:** Start with Option A (no caching). Add Option B (file-based) only if performance issues arise.

---

## Non-Goal 10: Changing Validation Semantics for Convenience

### Temptation

"R0 allows 3 errors, but that feels too lenient. Let's make it 1 error in WS-2."

### Why Rejected

**Violates WS-1→WS-2 contract.** WS-2 must respect WS-1 severity semantics.

### What WS-2 Must Do

Use thresholds from WS-2-DEPENDENCY-PRINCIPLES.md:
- R0: 3 errors OK
- R1: 2 errors OK
- R2: 0 errors
- R3: 0 errors

If these feel wrong, **change WS-1 acceptance criteria**, not WS-2 thresholds.

### Why This Matters

If WS-1 says "valid" (3 errors for R0) but WS-2 says "not ready" (0 errors for R0), users get conflicting signals.

**Alignment is critical.** One source of truth.

---

## Non-Goal 11: Guidance Generation

### Temptation

"Risk Register is missing mitigation for Risk-002. Generate suggested mitigation text."

### Why Rejected

**That's WS-3 (Guidance Engine).** WS-2 identifies problems, WS-3 suggests solutions.

### Separation of Concerns

| Layer | Responsibility |
|-------|---------------|
| WS-1 | Validate structure |
| WS-2 | Check dependencies + cross-refs |
| WS-3 | Generate improvement suggestions |
| WS-4 | Simulate expert review |

### What WS-2 Does

```json
{
  "missing": ["Risk-002 mitigation"],
  "suggestion": "Add mitigation for Risk-002"
}
```

### What WS-3 Does (Future)

```json
{
  "missing": ["Risk-002 mitigation"],
  "guidance": {
    "suggestion": "Consider: technical controls, process changes, or accept with justification",
    "examples": ["Implement input validation", "Add monitoring alerts", "Accept risk with rationale"]
  }
}
```

**WS-2 identifies, WS-3 guides.** Don't conflate.

---

## Non-Goal 12: Expert Review Triggering

### Temptation

"If all artifacts are 90%+ complete, automatically request expert review."

### Why Rejected

**User initiates review, not system.** User decides when ready.

### What Happens Instead

```json
{
  "readiness": {
    "all_artifacts_ready": true,
    "completion_average": 0.92,
    "expert_review_recommended": true
  },
  "next_action": "Ready for expert review. Click 'Request Review' when ready."
}
```

User clicks button. System does NOT auto-submit.

### Why This Matters

- User may want final polish before review
- User may want to add context/notes to review request
- Auto-triggering removes user agency

---

## Summary: The 12 Non-Goals

1. **No Auto-Generation** - User decides when to generate
2. **No Auto-Completion** - User fills gaps, not system
3. **No Hard Blocking** - Recommend, don't enforce
4. **No Prescriptive Language** - Descriptive guidance only
5. **No Revalidation** - Call WS-1, don't duplicate
6. **No Semantic Judgment** - Structure only, not quality
7. **No Inferred Requirements** - Only what's in acceptance_criteria.json
8. **No Workflow Stages** - WS-6 concern, not WS-2
9. **No Indefinite Caching** - Fresh or file-based caching only
10. **No Semantic Override** - Respect WS-1 thresholds
11. **No Guidance Generation** - WS-3 concern, not WS-2
12. **No Auto-Review** - User initiates, not system

---

**Status:** Awaiting Dark-Matter review.
**Next Step:** Run Dark-Matter Mode on WS-2-SCOPE.md, WS-2-DEPENDENCY-PRINCIPLES.md, and WS-2-NON-GOALS.md before any WS-2 code is written.
