# QMS Dashboard: Setup and Development Guide
## For Human Developers and AI Coding Assistants

**Version:** 8A-1.2
**Date:** 2025-12-17
**Purpose:** Canonical reference for running, extending, and NOT misusing the QMS Dashboard

---

## 1. System Purpose (Anti-Misinterpretation Signal)

### What QMS Dashboard IS

**A teaching system that diagnoses artifact completeness.**

The QMS Dashboard is a meta-system designed to **teach people what quality actually requires** by:
- Classifying project risk based on explicit intake rules
- Generating structured QMS artifact templates
- **Validating artifacts against acceptance criteria (diagnostic, not prescriptive)**
- Surfacing gaps without filling them
- Teaching users through progressive rigor (R0 → R3)

**Core Principle:** The system **shows you what's wrong**, but **never fixes it for you**.

### What QMS Dashboard IS NOT

❌ **Not a workflow automation system**
❌ **Not an artifact auto-completer**
❌ **Not a prescriptive compliance engine**
❌ **Not an AI-powered content generator**
❌ **Not a blocking gate (except at production transitions)**

**Critical Distinction:**
- **Teaching** = "Your Risk Register is missing 3 mitigations" (✅ This system)
- **Automation** = "I've filled in 3 mitigations for you" (❌ NOT this system)

If you find yourself auto-completing artifacts, **you've broken the teaching principle.**

---

## 2. How to Run (Human + AI Safe)

### System Requirements

- **Python:** 3.10+ (tested on 3.10.12)
- **OS:** Linux, macOS, Windows (WSL recommended on Windows)
- **Dependencies:** See `requirements.txt` (FastAPI, Pydantic, etc.)

### Setup (First Time)

#### On Linux / macOS:
```bash
# Clone repository
git clone <repo-url>
cd "QMS Dashboard"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 -m pytest test_regression_phase6.py
```

#### On Windows (WSL):
```bash
# Same as Linux/macOS (use WSL terminal)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### On Windows (Native):
```powershell
# Use PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Running the System

**Start Backend (Development):**
```bash
cd src/backend
python3 main.py
# Server runs on http://localhost:8000
```

**Run Tests:**
```bash
# Phase 6 regression tests (must always pass)
python3 test_regression_phase6.py

# WS-1 validation tests
python3 test_ws1_artifact_health.py
python3 test_ws1_r0r1_validation.py
```

### Common Failure Modes

**1. "Module not found" errors:**
- **Cause:** Virtual environment not activated
- **Fix:** `source venv/bin/activate` (Linux/macOS) or `.\venv\Scripts\Activate.ps1` (Windows)

**2. "Port 8000 already in use":**
- **Cause:** Previous server instance still running
- **Fix:** `pkill -f "python3 main.py"` or `taskkill /F /IM python.exe` (Windows)

**3. "Pydantic validation errors":**
- **Cause:** Intake request doesn't match IntakeAnswers schema
- **Fix:** Check `/api/intake` endpoint expects exact field names (q1_users, q2_influence, etc.)

**4. "File not found: acceptance_criteria.json":**
- **Cause:** Running from wrong directory
- **Fix:** Always run `python3 main.py` from `src/backend/` directory

---

## 3. Validation Architecture (For AI Coders)

### The Three Pillars

```
acceptance_criteria.json  ←→  validator.py  ←→  templates/*.py
     (Source of Truth)      (Deterministic     (Structure +
                              Validation)        Markers)
```

**Pillar 1: acceptance_criteria.json**
- **What:** JSON schema defining what makes an artifact "complete" per risk level
- **Where:** `src/backend/artifacts/acceptance_criteria.json`
- **Format:**
  ```json
  {
    "artifacts": {
      "Quality Plan": {
        "risk_levels": {
          "R2": {
            "required_sections": ["Purpose", "Scope", ...],
            "rules": {"placeholders_not_allowed": true, "min_sections_present": 4}
          }
        }
      }
    }
  }
  ```
- **Rule:** This is the ONLY source of truth. Never hard-code validation logic elsewhere.

**Pillar 2: validator.py**
- **What:** Deterministic validation engine that checks artifacts against criteria
- **Where:** `src/backend/artifacts/validator.py`
- **Design:** Pure rule-based (no AI, no heuristics)
- **Rule:** If a validation type isn't in acceptance_criteria.json, the validator doesn't check it.

**Pillar 3: Template Markers**
- **What:** HTML comments in templates marking required sections
- **Where:** `src/backend/artifacts/templates/*.py`
- **Format:** `<!-- REQUIRED[R2,R3]: Section name -->`
- **Rule:** Markers are informational for humans. Validator parses markdown structure, not markers.

### Validation Flow

```
1. User submits intake → Classification (R0-R3)
2. Generate artifacts from templates
3. Validator loads acceptance_criteria.json
4. Validator checks artifact content against criteria
5. Return ValidationResult (valid, completion_percent, issues)
6. API returns diagnostic health (NOT commands)
```

**Critical:** Validation is **diagnostic** (reports state), **not prescriptive** (issues commands).

---

## 4. Guardrails for AI Assistants (Critical)

### AI Behavior Contract

If you are an AI coding assistant (Claude, Cursor, GitHub Copilot, etc.), **you MUST follow these rules:**

#### ❌ DO NOT (Violations of Teaching Principle)

1. **DO NOT add prescriptive language to API responses**
   - ❌ "You must fix X before proceeding"
   - ❌ "This will fail review"
   - ❌ "Complete these tasks: [list]"
   - ✅ "Artifact X has Y issues" (descriptive)

2. **DO NOT auto-fix artifacts**
   - ❌ Filling in placeholders automatically
   - ❌ Generating missing sections
   - ❌ "Helpfully" completing incomplete content

3. **DO NOT infer missing requirements**
   - ❌ "I think this artifact also needs..."
   - ❌ Adding criteria not in acceptance_criteria.json
   - ❌ Creating validation rules based on "common sense"

4. **DO NOT add workflow blocking**
   - ❌ `if not valid: raise Exception("Cannot proceed")`
   - ❌ Preventing artifact generation if previous artifacts incomplete
   - ❌ Hard-blocking based on completion percentage

5. **DO NOT collapse teaching → automation**
   - ❌ "Let me complete this Risk Register for you"
   - ❌ "I'll fix all validation errors automatically"
   - ❌ Building features that auto-complete artifacts

#### ✅ DO (Teaching System Principles)

1. **DO surface gaps, never fill them**
   - ✅ "Quality Plan missing Purpose section"
   - ✅ "Risk Register has 1 risk, R3 requires 5"
   - ✅ Show what's incomplete, let user complete

2. **DO prefer warnings over errors for R0/R1**
   - ✅ R0/R1: `warning_only=true` (teaching mode)
   - ✅ R2/R3: Errors appropriate (strict rigor)

3. **DO maintain 1:1 alignment**
   - ✅ acceptance_criteria.json = validator.py = templates
   - ✅ Every rule in JSON has validator method
   - ✅ Every required section has template marker

4. **DO use descriptive language**
   - ✅ "Most artifacts incomplete (45% overall)"
   - ✅ "3 placeholders detected"
   - ✅ "Risk-002 missing mitigation field"

5. **DO enforce deterministic validation**
   - ✅ No AI/ML in validator
   - ✅ No heuristics or guessing
   - ✅ Pure rule-based checks (regex, counts, presence)

### Warning Signs of Violation

If you see yourself about to:
- Generate content to "help" the user
- Add validation logic not in acceptance_criteria.json
- Create blocking behavior (raise exceptions, prevent access)
- Use words like "must", "cannot", "will fail"
- Implement "smart" completion or suggestion features

**STOP. You're violating the teaching principle.**

---

## 5. How to Extend Safely

### Adding a New Artifact

**Steps:**
1. **Create template** in `src/backend/artifacts/templates/new_artifact.py`
   - Follow existing template pattern
   - Add VALIDATION block at top
   - Add REQUIRED markers to sections

2. **Add acceptance criteria** in `acceptance_criteria.json`
   ```json
   "New Artifact": {
     "description": "...",
     "risk_levels": {
       "R0": { "required_sections": [...], "rules": {...} },
       ...
     }
   }
   ```

3. **No validator changes needed** (unless new rule type)
   - Existing validators handle most cases
   - If new rule type needed, see next section

4. **Update `get_required_artifacts()`** in `validation/classifier.py`
   - Add artifact to appropriate risk level list

5. **Test:**
   - Generate artifact for each risk level
   - Verify validation works
   - Check markers render correctly

### Adding a New Validation Rule

**Example: Adding `min_paragraphs` rule**

1. **Add to acceptance_criteria.json:**
   ```json
   "rules": {
     "min_paragraphs": 3
   }
   ```

2. **Add validator method** in `validator.py`:
   ```python
   def _validate_min_paragraphs(self, content, rules, warning_only=False):
       paragraphs = content.split('\n\n')
       count = len([p for p in paragraphs if p.strip()])
       min_para = rules.get("min_paragraphs", 0)
       if count < min_para:
           severity = "warning" if warning_only else "error"
           issues.append(ValidationIssue(...))
       return issues
   ```

3. **Call in `validate_artifact()`:**
   ```python
   if "min_paragraphs" in rules:
       issues.extend(self._validate_min_paragraphs(content, rules, warning_only))
   ```

4. **Test with sample artifact**

### Adding a New Risk Level

**NOT RECOMMENDED.** The 4-level system (R0-R3) is architecturally sound:
- R0: Minimal (advisory)
- R1: Moderate (conditional)
- R2: Strict (mandatory)
- R3: Maximum (regulated)

Adding R4+ breaks this balance. If you think you need R4, you probably need:
- Better criteria for R3
- Or a different classification dimension (not just "more rigor")

### What Requires a New WS vs a Patch

**New Workstream (WS) Required:**
- Adding cross-artifact validation (dependencies, traceability)
- Adding workflow features (SLA tracking, approvals)
- Adding AI/ML features (content generation, smart suggestions)
- Changing architectural principles (deterministic → heuristic)

**Patch Acceptable:**
- Adding 1-2 new artifacts
- Adding 1-2 new validation rules
- Fixing bugs in existing validators
- Updating acceptance criteria thresholds
- Improving error messages

---

## 6. Architecture Decisions (Dark-Matter View)

### Why Deterministic Validation?

**Decision:** No AI/ML in validator, only rule-based checks.

**Rationale:**
- **Predictability:** Users need to know exactly why validation failed
- **Trust:** No "black box" decisions
- **Debugging:** Failures traceable to specific rule
- **Safety:** Can't hallucinate requirements

**Consequence:** Some validation is coarse (e.g., "at least 3 items" vs "meaningful items"). This is intentional. Teaching system shows structural gaps, not content quality.

### Why R0/R1 Warning-Only?

**Decision:** R0/R1 use `warning_only=true`, R2/R3 use errors.

**Rationale:**
- **R0/R1:** Low-risk projects, encourage quality without blocking
- **R2/R3:** High-risk projects, stricter gates prevent harm
- **Teaching:** Warnings teach without punishing

**Consequence:** R0/R1 projects can have "invalid" artifacts but still proceed. This is intentional - we're teaching, not policing.

### Why No Cross-Artifact Validation (Yet)?

**Decision:** WS-1 validates artifacts individually, not relationships.

**Rationale:**
- **Complexity:** Cross-artifact validation requires dependency graph (WS-2)
- **Scope:** Phase 8A focuses on measurement layer only
- **Future:** WS-2 will add "Risk-001 referenced in Verification Plan" checks

**Consequence:** Validator won't catch "Risk Register IDs don't match Verification Plan tests" yet. Acceptable for WS-1 scope.

### Why File-Based Storage?

**Decision:** No database, artifacts saved as `.md` files.

**Rationale:**
- **Simplicity:** No DB setup, works out-of-the-box
- **Portability:** Artifacts are human-readable markdown
- **Version control:** Can commit artifacts to git
- **Future:** May add DB for search/analytics (v3.0+)

**Consequence:** No advanced queries, no multi-user locking. Acceptable for single-user local deployment (Phase 8A scope).

---

## 7. System Invariants (Explicit Contracts)

These are **non-negotiable principles** that protect system integrity. Violating these invariants transforms the system from teaching to automation.

### Invariant 1: Validator Diagnoses, Never Blocks

**Rule:** The validator MUST NEVER block artifact generation or progression on its own.

**Rationale:**
- Blocking is a higher-order concern handled by:
  - Dependency logic (WS-2)
  - Lifecycle rules (WS-6)
  - Stage transition gates
- Validator role: **measure and report**, not **enforce and gate**

**What This Means:**
- ✅ Validator returns issues (errors, warnings, info)
- ✅ Caller decides what to do with issues
- ❌ Validator never throws exceptions to prevent generation
- ❌ Validator never returns "cannot proceed" status

**Future Risk:** A well-intentioned contributor might add `if not valid: raise BlockingError()`. This violates the teaching principle.

---

### Invariant 2: Structure ≠ Semantic Correctness

**Rule:** The validator validates **structural and formal completeness only**. It does NOT assert correctness, adequacy, or truth of content.

**What Validator Checks:**
- ✅ Required sections present
- ✅ Minimum item counts met (5 risks, 3 metrics, etc.)
- ✅ Placeholders removed (R1+)
- ✅ Headers and structure exist

**What Validator Does NOT Check:**
- ❌ Semantic quality ("Is this risk assessment meaningful?")
- ❌ Logical coherence ("Do these mitigations actually address the risk?")
- ❌ Adequacy ("Are 5 risks *enough* for this system?")
- ❌ Truth ("Is this assumption actually true?")

**Why This Matters:**
A future AI assistant could generate *syntactically perfect but semantically hollow* content and pass validation.

**Where Semantic Judgment Lives:**
- Expert review (Phase 5)
- Simulation engine (WS-4)
- Guidance engine (WS-3)
- Human interpretation (always)

**Consequence:** Passing validation means "structurally ready for review", NOT "correct and sufficient".

---

### Invariant 3: Validator Never Mutates Input

**Rule:** The validator is a **pure function**. It reads artifact content, returns diagnostic results, and **never modifies the artifact**.

**What This Means:**
- ✅ Input artifact content is immutable
- ✅ Validator returns `ValidationResult` object only
- ❌ Validator never inserts missing sections
- ❌ Validator never fixes placeholders
- ❌ Validator never "corrects" formatting

**Test Coverage:** No negative tests yet enforce this (see WS-1 completion report, gap #5). Future work should add mutation detection tests.

---

### Invariant 4: Acceptance Criteria Are Canonical

**Rule:** `acceptance_criteria.json` is the **single source of truth** for what constitutes artifact completeness.

**Hierarchy:**
```
acceptance_criteria.json (SOURCE OF TRUTH)
        ↓
validator.py (IMPLEMENTS CHECKS)
        ↓
templates/*.py (GENERATE STRUCTURE)
```

**What This Means:**
- ✅ All validation logic derives from acceptance_criteria.json
- ✅ Changing criteria changes validation behavior (1:1 mapping)
- ❌ Never add validation logic that isn't in acceptance criteria
- ❌ Never infer missing requirements from context

**Consequence:** If a requirement isn't in acceptance_criteria.json, it doesn't exist.

---

### Invariant 5: Teaching vs Enforcement Boundary

**Rule:** R0/R1 use **warnings** (teaching mode). R2/R3 use **errors** (enforcement mode).

**Implementation:**
```python
warning_only = risk_criteria.get("rules", {}).get("warning_only", False)
severity = "warning" if warning_only else "error"
```

**Why This Matters:**
- R0/R1: Users learning what quality requires → guide without blocking
- R2/R3: Safety-critical systems → enforce completeness before review

**Future Risk:** A contributor might "help" R0/R1 users by upgrading warnings to errors. This collapses teaching into enforcement and breaks the learning model.

---

### Invariant 6: Placeholder Count Is Informational, Not Blocking

**Rule:** Placeholder detection informs users but **never blocks progression**.

**Current Behavior:**
- Validator counts placeholders (`[TBD]`, `[Name]`, etc.)
- R0: Placeholders allowed (no error)
- R1+: Placeholders trigger errors

**Hidden Metric:**
Placeholder density is a **teaching signal**:
- High placeholder count = "structurally complete but conceptually early"
- This should feed guidance tone (WS-3) and simulation confidence (WS-4)

**Future Work:** Expose placeholder count as explicit metric in artifact health API.

---

### Invariant 7: Acceptance Criteria Versioning

**Current State:** Schema versioned as a whole (`8A-1.2`).

**Missing:** Artifact-level evolution notes.

**Future Risk:** When criteria evolve, you'll want to say *"Risk Register v1 vs v2"* without diffing a 461-line JSON.

**Recommendation (Lightweight):**
Add comment convention inside `acceptance_criteria.json`:
```json
"_notes": "Risk Register criteria stabilized in Phase 8A WS-1.8"
```

Pure metadata. Zero runtime effect.

---

### Why These Invariants Matter

**For Human Developers:**
- Clear boundaries prevent scope creep
- Explicit contracts reduce ambiguity
- Future changes stay aligned with principles

**For AI Assistants:**
- Prevents "helpful" behaviors that break teaching principle
- Makes implicit assumptions explicit
- Reduces risk of well-intentioned misalignment

**For System Evolution:**
- WS-2 (Dependencies) can trust these invariants
- WS-3 (Guidance) can build on these foundations
- WS-4 (Simulation) can rely on these contracts

---

## 8. Testing Strategy

### Must-Pass Tests (Regression)

**Phase 6 Regression Suite** (`test_regression_phase6.py`):
- **What:** Locks in behavior from Phases 1-6
- **When:** Run before EVERY commit
- **Pass Criteria:** 6/6 tests must pass
- **If Fails:** You broke something fundamental

### WS-1 Validation Tests

**R0/R1 Validation** (`test_ws1_r0r1_validation.py`):
- Tests warning-only semantics
- Tests placeholder allowance
- Tests minimum criteria (1 risk for R0, 2 for R1)

**Artifact Health API** (`test_ws1_artifact_health.py`):
- Tests end-to-end validation
- Tests messaging discipline (no prescriptive commands)
- Tests all 11 artifacts × 4 risk levels

### Writing New Tests

**Pattern:**
```python
def test_new_validation():
    validator = ArtifactValidator()
    content = "... artifact markdown ..."
    result = validator.validate_artifact("Artifact Name", content, "R2")

    assert result.valid == expected_valid
    assert result.completion_percent == expected_completion
    assert len(result.issues) == expected_issue_count
```

**Golden Rule:** If you change validation logic, add a test. No exceptions.

---

## 9. Common Anti-Patterns (What NOT to Do)

### Anti-Pattern 1: "Helpful" Auto-Completion

```python
# ❌ WRONG
def generate_risk_register(intake):
    content = template.generate(intake)
    if validator.validate(content).valid == False:
        # "Help" user by filling in missing content
        content = auto_complete_risks(content)
    return content
```

**Why Wrong:** Violates teaching principle. User doesn't learn what was missing.

**Correct:**
```python
# ✅ RIGHT
def generate_risk_register(intake):
    content = template.generate(intake)
    # Return as-is, let validator report gaps
    return content
```

### Anti-Pattern 2: Hard-Coded Validation

```python
# ❌ WRONG
def validate_risk_register(content):
    if "R3" in content and content.count("Risk-") < 5:
        raise ValueError("R3 needs 5 risks")
```

**Why Wrong:** Criteria not in acceptance_criteria.json. Not maintainable.

**Correct:**
```python
# ✅ RIGHT
# Add to acceptance_criteria.json:
# "R3": {"rules": {"min_risks": 5}}
# Validator reads from JSON, no hard-coding
```

### Anti-Pattern 3: Prescriptive Error Messages

```python
# ❌ WRONG
return {
    "message": "You must add 3 more risks before proceeding to Verification Plan"
}
```

**Why Wrong:** Prescriptive command, not descriptive state.

**Correct:**
```python
# ✅ RIGHT
return {
    "message": "Expected at least 5 risks, found 2"
}
```

### Anti-Pattern 4: Workflow Blocking

```python
# ❌ WRONG
def generate_verification_plan(intake_id):
    health = get_artifact_health(intake_id)
    if health.overall_completion < 0.8:
        raise HTTPException(403, "Complete other artifacts first")
```

**Why Wrong:** Adds blocking behavior. WS-1 is diagnostic only.

**Correct:**
```python
# ✅ RIGHT
def generate_verification_plan(intake_id):
    # Generate regardless of other artifact status
    # Validator will surface gaps, user decides when to proceed
    return generate(intake_id)
```

---

## 10. AI Assistant Quick Reference

**If you're an AI assistant reading this file:**

### Your Job
- **Diagnose** artifact completeness
- **Report** gaps without filling them
- **Teach** users what quality requires
- **Surface** issues, not solutions

### Your Limits
- ❌ No auto-completion
- ❌ No prescriptive commands
- ❌ No workflow blocking
- ❌ No hard-coded validation

### Your Tools
- ✅ acceptance_criteria.json (source of truth)
- ✅ validator.py (deterministic checks)
- ✅ Descriptive language ("X is missing Y")
- ✅ Warning-only mode for R0/R1

### Your Test
Before proposing a change, ask:
1. Does this teach or automate?
2. Does this report state or issue commands?
3. Does this follow acceptance_criteria.json or invent rules?
4. Does this respect warning-only for R0/R1?

If any answer is wrong, **don't do it.**

---

## 11. Troubleshooting

### "Validator not detecting my new rule"

**Check:**
1. Rule added to `acceptance_criteria.json`?
2. Validator method added to `validator.py`?
3. Method called in `validate_artifact()`?
4. Rule name matches exactly (case-sensitive)?

### "Markers not showing in validation"

**Understanding:** Markers are for **humans**, not validator.
Validator parses **markdown structure**, not HTML comments.
Markers help humans understand what's required, validator checks actual content.

### "R0 artifacts showing errors"

**Check:** Does criteria have `"warning_only": true`?
R0 should use warnings, not errors (teaching mode).

### "Placeholder count always 0"

**Check:** Are placeholders being counted?
Validator always counts placeholders (even if allowed).
If count is 0, content genuinely has no placeholders.

---

## 12. Contribution Guidelines

### Before Submitting Code

1. **Run regression tests:** `python3 test_regression_phase6.py` (must pass 6/6)
2. **Run WS-1 tests:** Validate new validation logic
3. **Check alignment:** acceptance_criteria.json ↔ validator.py ↔ templates
4. **Verify messaging:** No prescriptive language in API responses
5. **Test all risk levels:** R0, R1, R2, R3

### Code Review Checklist

- [ ] Follows teaching principle (diagnostic, not prescriptive)
- [ ] No hard-coded validation logic
- [ ] Validation rules in acceptance_criteria.json
- [ ] Deterministic only (no AI/ML/heuristics)
- [ ] R0/R1 use warning-only where appropriate
- [ ] Tests added for new validation types
- [ ] Regression tests still pass
- [ ] No workflow blocking added

---

## 13. Contact and Support

**Project Maintainer:** [To be filled]
**Repository:** [To be filled]
**Issues:** Report via GitHub Issues
**Questions:** See documentation in `docs/` directory

**For AI Assistants:** If you're unsure whether a change violates the teaching principle, **ask the human developer first.** Do not assume.

---

## Version History

- **8A-1.2** (2025-12-17): Initial setup guide with AI guardrails
- **8A-1.1** (2025-12-16): WS-1.7-1.9 complete (R0-R3, all 11 artifacts)
- **8A-1.0** (2025-12-15): WS-1.1-1.4 initial validation foundation

---

**Remember:** This system teaches what quality requires. It shows gaps, never fills them. Keep it that way.
