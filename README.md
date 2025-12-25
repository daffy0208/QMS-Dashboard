# QMS Dashboard

**Status:** 🔒 WS-2 Frozen · Phase 8A Closed · Phase 9 Demonstration
**Notice:** WS-2 logic frozen. Phase 9 documentation and demonstration only. No functional changes permitted.

**One-line description:**
A teaching and diagnostic proof harness for risk-based quality management, used to derive the Meta-QMS Canon v1.0.

---

## 1. What This Is

### 1.1 Purpose Statement

The QMS Dashboard is a **teaching and diagnostic proof harness**, not a production quality system.

Its purpose is to:

* Demonstrate how a risk-based quality management system behaves under real implementation pressure
* Make quality requirements *visible and explainable* without enforcing them
* Provide an evidence base from which the **Meta-QMS Canon v1.0** was extracted

This repository exists to show **how quality systems must behave** in order to remain teachable, auditable, and safe — not to provide an end-user product.

---

### 1.2 What This System Does

Within its frozen scope, the Dashboard demonstrates the following capabilities:

* **Risk classification (R0–R3) for quality rigor selection**
  Determines which rigor mode applies based on project risk, not user role.

* **Artifact validation (structural only)**
  Checks presence, structure, placeholders, and acceptance criteria.
  Does *not* judge semantic correctness.

* **Dependency readiness assessment**
  Evaluates whether upstream artifacts are sufficiently complete for downstream use, using a static dependency graph and dynamic readiness state.

* **Override debt tracking**
  Tracks and surfaces how often users proceed despite warnings, without blocking progression.

* **Teaching-oriented signals**
  Uses descriptive, explanatory language to show gaps, thresholds, and consequences while preserving user agency.

All behaviors are explicitly bounded by frozen contracts and non-goals.

---

### 1.3 Scope Boundaries (Frozen)

The Dashboard scope is complete and frozen as of **2025-12-17**.

Included workstreams:

* **WS-1: Artifact Validation** — ✅ Complete
* **WS-2: Dependency Management & Readiness** — ✅ Complete

Explicitly **out of scope** (by design):

* Semantic judgment or content correctness evaluation
* Guidance generation or "how to fix" recommendations
* Workflow orchestration or lifecycle management
* UX optimization or productization
* Decision-making on behalf of users

These exclusions are intentional and enforced.

---

## 2. What This Is NOT

### 2.1 Not a Product

This repository is **not**:

* A production-ready quality management system
* A SaaS offering or deployable platform
* A general-purpose compliance tool
* A roadmap-driven software product

It is a **reference implementation and demonstration layer** whose purpose is complete.

---

### 2.2 Not a Replacement for Human Judgment

The Dashboard does **not**:

* Evaluate whether content is correct, adequate, or sufficient
* Approve artifacts for production use
* Replace expert review or accountability

All validation is **structural only**.
Human judgment remains mandatory for semantic validation and approval.

---

### 2.3 Not Open for Feature Requests

* WS-2 logic is frozen as of **2025-12-17**
* No new capabilities will be added within this scope
* Feature requests, enhancements, or roadmap proposals will not be accepted

Only changes that **preserve existing behavior** (documentation or qualifying bug fixes) are permitted under governance.

---

## 3. Freeze & Governance Notices

### 3.1 Phase 8A Status

* **Phase:** 8A — Teaching System Core
* **Status:** Closed
* **Closure Date:** 2025-12-17
* **WS-2 Scope:** Frozen
* **Stop Conditions:** All met and audited

The Dashboard's role as a proof harness is complete.

---

### 3.2 What Changes Are Permitted

The following changes are allowed **without unfreezing scope**:

* ✅ Documentation clarification and accuracy improvements
* ✅ Bug fixes that strictly preserve existing behavior
* ✅ Threshold calibration **only via documented policy and versioned configuration files**

The following are **not permitted**:

* ❌ Functional expansion
* ❌ New behaviors or capabilities
* ❌ Scope creep into guidance, simulation, or lifecycle management
* ❌ UX refinement or product polish

---

### 3.3 Governance References

Authoritative documents:

* **WS-2 Scope Freeze:** `WS-2-SCOPE-FREEZE.md`
* **Phase 8A WS-1 Completion Report:** `PHASE-8A-WS1-COMPLETION.md`

These documents define all binding constraints on this repository.

---

## 4. Relationship to Meta-QMS Canon v1.0

### 4.1 What the Meta-QMS Is

The **Meta-QMS Canon v1.0** is a tool-agnostic specification of universal quality management principles extracted from the implementation evidence of WS-1 and WS-2.

It defines:
- **Why** quality systems must behave in specific ways
- **Where** automation must stop and human judgment must begin
- **How** teaching and enforcement zones must be separated
- **What** constitutes risk-proportionate rigor

The Meta-QMS is not specific to this Dashboard. It is transferable to any quality management context.

---

### 4.2 How This Dashboard Relates

The relationship is directional and evidence-based:

```
Dashboard Implementation → Evidence → Meta-QMS Extraction
(specific proof harness)   (observable behavior)   (universal principles)
```

- **The Dashboard is the proof**, not the product
- **The Meta-QMS is the output**, not a description of the Dashboard
- The Dashboard demonstrates that the Meta-QMS principles are *implementable and coherent*

The Dashboard serves as the **existence proof** for Meta-QMS claims. It shows that:
- Risk-proportionate rigor works in practice
- Soft blocking preserves agency while maintaining visibility
- Structural and semantic validation can be cleanly separated
- Teaching systems can maintain discipline without enforcement

---

### 4.3 Key Principles Demonstrated

The Dashboard implementation demonstrates the following Meta-QMS principles:

| Principle | Manifestation in Dashboard |
|-----------|---------------------------|
| **Risk-Proportionate Rigor** | R0: 50% → R1: 60% → R2: 80% → R3: 90% thresholds with explicit policy |
| **Teaching vs Enforcement Separation** | Levels 1-3 teach; no hard blocking at artifact validation layer |
| **Structural vs Semantic Boundaries** | WS-1/WS-2 check structure only; `epistemic_status: structural_only` |
| **Epistemic Status Transparency** | Every assessment declares its basis and confidence limits |
| **Override Debt Visibility** | Tracks proceed-anyway count; surfaces debt without blocking |
| **Artifact Volatility Awareness** | Draft-friendly (-10%), foundation (0%), rework-costly (+10%) modifiers |
| **Directional Dependencies** | Static, acyclic graph; upstream readiness affects downstream |

These principles were **extracted from** Dashboard behavior, not imposed on it afterward.

---

### 4.4 Audience and Use

**For quality engineers and system architects:**
- Use the Dashboard to *see* how Meta-QMS principles manifest in a working system
- Use the Meta-QMS Canon to *understand* why the Dashboard behaves as it does

**For researchers and standards bodies:**
- The Dashboard provides concrete, auditable evidence for Meta-QMS claims
- The Meta-QMS provides a tool-agnostic reference for quality system design

**For practitioners:**
- The Dashboard is not for production use
- The Meta-QMS principles *are* transferable to production quality systems

---

## 5. Architecture Overview (Descriptive)

**Note:** This section describes the implementation **as frozen on 2025-12-17**. All components, data flows, and API surfaces are locked and not subject to change under Phase 9.

---

### 5.1 System Components

The Dashboard consists of four frozen components:

#### Risk Classification Engine
- **Location:** `src/backend/validation/classifier.py`
- **Function:** Maps intake question responses to risk levels (R0-R3) using fixed decision logic
- **Status:** Frozen (Phase 8A WS-1)

#### Artifact Validator (WS-1)
- **Location:** `src/backend/artifacts/validator.py`
- **Function:** Structural validation of QMS artifacts against acceptance criteria
- **Capabilities:**
  - Section presence checking
  - Placeholder detection (`[TBD]`, `TODO`, etc.)
  - Item count validation
  - Cross-reference extraction (Risk IDs, CTQ IDs, etc.)
- **Epistemic Boundary:** Structural only; no semantic judgment
- **Status:** Frozen (Phase 8A WS-1)

#### Dependency Manager (WS-2)
- **Location:** `src/backend/artifacts/dependency_manager.py` (620 lines)
- **Function:** Readiness assessment and dependency checking
- **Capabilities:**
  - Risk-proportionate threshold application
  - Artifact volatility modifiers
  - Static dependency graph traversal
  - Override debt tracking
  - Next action signal generation (teaching-oriented)
- **Invariants:**
  - `can_proceed_anyway: true` (always)
  - `epistemic_status: structural_only` (always)
  - No hard blocking
- **Status:** Frozen (Phase 8A WS-2)

#### API Layer
- **Location:** `src/backend/main.py`
- **Function:** FastAPI endpoints exposing classification, validation, and dependency health
- **Status:** Frozen (Phase 8A)

---

### 5.2 Data Flow

The system follows this fixed sequence:

```
1. Intake Request
   ↓
2. Risk Classification (R0-R3)
   ↓
3. Artifact Template Generation
   ↓
4. Artifact Validation (WS-1) ──→ Completion %, Errors, Warnings
   ↓
5. Dependency Assessment (WS-2) ──→ Readiness, Dependency Status, Next Actions
```

**Key characteristics:**
- Linear flow; no feedback loops
- Each stage reads configuration files (frozen)
- No user state; assessments are stateless
- All decisions based on frozen policy

---

### 5.3 Configuration Files

Three versioned configuration files define system behavior. All are **frozen and version-controlled**:

#### `dependencies.json` (v1.0)
- **Purpose:** Static dependency graph for all 11 QMS artifacts
- **Structure:** Maps each artifact to its prerequisite list
- **Example:**
  ```json
  {
    "Verification Plan": ["Risk Register", "CTQ Tree"],
    "Control Plan": ["Risk Register", "Verification Plan"]
  }
  ```
- **Status:** Frozen; changes require explicit policy versioning

#### `artifact_volatility.json` (v1.0)
- **Purpose:** Defines volatility classes and threshold modifiers
- **Classes:**
  - `draft_friendly`: -10% (e.g., Verification Plan)
  - `foundation`: 0% (e.g., Risk Register)
  - `rework_costly`: +10% (e.g., Traceability Index)
- **Status:** Frozen; calibration requires documented policy change

#### `readiness_thresholds.json` (v1.0)
- **Purpose:** Risk-level-specific thresholds for completion and error tolerance
- **Structure:**
  ```json
  {
    "R0": {"completion": 0.5, "max_errors": 3},
    "R2": {"completion": 0.8, "max_errors": 0},
    "R3": {"completion": 0.9, "max_errors": 0}
  }
  ```
- **Note:** All values are **reference defaults** (explicit, versioned, calibratable per policy)
- **Status:** Frozen; calibration requires explicit policy approval and versioning

---

### 5.4 API Surface

**Freeze Notice:** *Endpoints listed for transparency; API surface is frozen as of 2025-12-17.*

The Dashboard exposes the following REST endpoints:

#### Project Intake & Classification
- `POST /api/intake`
  - **Input:** Project name, 7 intake question responses
  - **Output:** Intake ID, risk level (R0-R3), rigor mode, required artifacts
  - **Status:** Frozen (WS-1)

#### Artifact Generation
- `POST /api/intake/{intake_id}/generate-artifacts`
  - **Input:** Intake ID
  - **Output:** Generated artifact templates (Markdown)
  - **Status:** Frozen (WS-1)

#### Dependency Health (WS-2)
- `GET /api/intake/{intake_id}/dependency-health`
  - **Input:** Intake ID
  - **Output:** ProjectDependencyHealth
    - Per-artifact readiness assessment
    - Dependency status (all dependencies ready?)
    - Cross-reference validation issues
    - Overall readiness boolean
  - **Invariants:**
    - `can_proceed_anyway: true` for all artifacts
    - `epistemic_status: structural_only`
  - **Status:** Frozen (WS-2)

#### Next Actions (WS-2)
- `GET /api/intake/{intake_id}/next-actions`
  - **Input:** Intake ID
  - **Output:** NextActionsResponse
    - Prioritized recommendations (teaching signals)
    - Diagnostic explanations
    - Unblocking relationships
  - **Invariants:**
    - `can_proceed_anyway: true` at response level
    - No prescriptive language ("must", "cannot")
  - **Status:** Frozen (WS-2)

---

### 5.5 Technology Stack

**As implemented (frozen):**

- **Backend:** Python 3.10+, FastAPI
- **Validation Engine:** Custom Pydantic models
- **Storage:** File-based (JSON for intake data, Markdown for artifacts)
- **Testing:** pytest (unit tests), requests (API tests)
  - Runtime deps: `requirements.txt`
  - Dev/test deps: `requirements-dev.txt`

No databases, no external services, no authentication layer.

---

## 6. Quick Start

**Purpose:** Run the Dashboard in demonstration mode to observe frozen WS-1/WS-2 behavior.

### 6.1 Prerequisites

- Python 3.10 or higher
- pip or uv package manager
- Terminal access

### 6.2 Installation

For detailed setup instructions, see **[SETUP.md]**.

Quick steps:
```bash
# Clone repository
git clone [repository-url]
cd qms-dashboard

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Verify installation
python test_ws2_dependency_manager.py
```

### 6.3 Running Demo Scenarios

The Dashboard includes demonstration scenarios that exercise frozen WS-1/WS-2 behavior.

```bash
# Start the API server
uvicorn src.backend.main:app --reload

# In another terminal, run demo scenarios
python demo_scenarios.py
```

For detailed scenario descriptions and "what to notice" guidance, see **[DEMO-SCENARIOS.md]**.

### 6.4 What You Should See

When running demos, observe:
- Risk classification varies by intake responses
- Readiness thresholds scale with risk level (R0: 50% → R3: 90%)
- `can_proceed_anyway` is always `true` (soft blocking)
- `epistemic_status` is always `structural_only`
- Override debt accumulates visibly without blocking
- Next actions use teaching language, not commands

**Note:** The Dashboard does not make decisions or approve artifacts. It provides diagnostic signals only.

---

## 7. Documentation Index

### 7.1 For Users (Demonstration & Orientation)

- **README.md** (this file) — What the Dashboard is and is not
- **SETUP.md** — Environment setup and verification
- **USAGE-GUIDE.md** — When and how to use the Dashboard as a teaching tool
- **DEMO-SCENARIOS.md** — 3-5 canonical scenarios showing Meta-QMS principles in action

### 7.2 For Developers (Implementation Reference)

- **WS-2-SCOPE-FREEZE.md** — Authoritative freeze document
- **WS-2-SCOPE.md** — WS-2 capabilities and boundaries
- **WS-2-NON-GOALS.md** — 13 explicitly rejected behaviors
- **WS-1-TO-WS-2-CONTRACT.md** — Interface contract between workstreams
- **test_ws2_dependency_manager.py** — Unit test suite (10/10 passing)
- **test_ws2_api_endpoints.py** — API test suite (3/3 suites)

### 7.3 For Quality Engineers (Principles & Evidence)

- **PHASE-8A-WS1-COMPLETION.md** — WS-1 completion report
- **WS-2-DEPENDENCY-PRINCIPLES.md** — Dependency logic principles

---

## 8. Test Coverage

### 8.1 Unit Tests

**File:** `test_ws2_dependency_manager.py`
**Status:** 10/10 passing
**Coverage:**

- Dependency manager initialization
- Risk-proportionate thresholds (R0 < R1 < R2 < R3)
- Artifact volatility modifiers (draft-friendly, foundation, rework-costly)
- Readiness assessment using WS-1 results
- Soft blocking invariant (`can_proceed_anyway: true`)
- Cross-reference validation (structural only)
- Directional dependencies (acyclic graph)
- No revalidation (uses WS-1 validator)
- Override budget tracking
- Descriptive language (no prescriptive words)

### 8.2 API Tests

**File:** `test_ws2_api_endpoints.py`
**Status:** 3/3 test suites passing
**Coverage:**

1. **Dependency Health Endpoint**
   - Response structure validation
   - WS-2 contract compliance (can_proceed_anyway, epistemic_status, confidence_limits)
   - Cross-reference issue reporting

2. **Next Actions Endpoint**
   - Response structure validation
   - Teaching language enforcement (no "must", "required", "cannot")
   - User agency preservation

3. **Non-Goals Compliance**
   - All 13 non-goals verified (no auto-generation, no hard blocking, no semantic judgment, etc.)

### 8.3 Running Tests

```bash
# Run unit tests
python test_ws2_dependency_manager.py

# Run API tests (requires server running)
uvicorn src.backend.main:app --reload &
python test_ws2_api_endpoints.py
```

**Expected result:** All tests pass, validating frozen WS-2 behavior.

---

## 9. Frequently Asked Questions

### 9.1 Why is it frozen?

The Dashboard's purpose is complete: implementation evidence has been extracted to the Meta-QMS Canon v1.0.

Further Dashboard development would reduce clarity without adding value. The proof exists; the principles are extracted. Continuing would risk:
- Scope creep into guidance or automation
- Blurring teaching vs enforcement boundaries
- Obscuring the evidence trail

The freeze preserves the integrity of what was proven.

### 9.2 Can I use this in production?

**No.** This is a proof harness, not a production system.

Missing for production use:
- Authentication and authorization
- Multi-user support
- Persistent storage (uses file-based JSON)
- Security hardening
- Scalability design
- Production deployment configuration
- Formal support or maintenance commitment

The **Meta-QMS principles** are production-ready. The **Dashboard implementation** is not.

### 9.3 Can I request new features?

**No.** WS-2 is frozen as of 2025-12-17.

Feature requests will not be accepted because:
- The Dashboard's scope is complete
- New features risk scope creep
- The freeze is governed by `WS-2-SCOPE-FREEZE.md`

If you need capabilities beyond WS-2 (guidance, simulation, lifecycle management), those are explicitly deferred to future workstreams and are not in scope for this repository.

### 9.4 Does this replace expert review?

**No.** The Dashboard provides structural validation only.

It does NOT:
- Judge content correctness or adequacy
- Approve artifacts for production use
- Replace human accountability
- Make decisions on behalf of users

Human expert review remains mandatory for:
- Semantic validation (is the content correct?)
- Risk judgment (are the identified risks the right ones?)
- Approval for downstream use

The Dashboard teaches and diagnoses; it does not decide or approve.

### 9.5 What if I find a bug?

Bug fixes that strictly preserve existing behavior are permitted under governance.

**Process:**
1. Verify the issue is a bug (not a feature request)
2. Confirm the fix preserves WS-2 behavior and contracts
3. Verify all tests still pass after the fix
4. Document the fix in `WS-2-SCOPE-FREEZE.md`

See `WS-2-SCOPE-FREEZE.md:143-149` for the formal change approval process.

### 9.6 Can I adapt this for my own use?

You may study, fork, or adapt the code for your own purposes, subject to the license terms.

However:
- You are responsible for production readiness
- No support or maintenance is provided for forks
- The Meta-QMS principles (not the Dashboard code) are the transferable asset

If adapting, focus on **implementing the Meta-QMS principles**, not replicating Dashboard internals.

### 9.7 How does this relate to ISO/IEC standards?

The Dashboard does not implement any specific standard. The Meta-QMS Canon is tool-agnostic and could inform standard-compliant implementations.

Comparative mapping to ISO 9001, IEC 62304, or other standards is a separate exercise outside this repository's scope.

---

## 10. License & Citation

### 10.1 License

This project is licensed under the **Apache License 2.0**.

See the `LICENSE` file for full text.

**Summary:**
- ✅ Study, reference, and adapt for your own use
- ✅ Attribution required
- ✅ Explicit warranty disclaimer
- ❌ No trademark license

### 10.2 How to Cite

If referencing this work academically or professionally, suggested citation:

```
QMS Dashboard: A Risk-Based Quality Management Proof Harness
Evidence base for Meta-QMS Canon v1.0
Frozen: 2025-12-17, Phase 8A Complete
[Repository URL]
```

---

## 11. Version History

| Version | Date | Phase | Status | Notes |
|---------|------|-------|--------|-------|
| 1.0 | 2025-12-17 | Phase 8A | 🔒 Frozen | WS-1 and WS-2 complete; stop conditions met |
| 1.0-demo | 2025-12-17 | Phase 9 | 📄 Documentation | Read-only demonstration layer; no logic changes |

**Key:**
- 🔒 **Frozen:** No functional changes permitted
- 📄 **Documentation:** Read-only materials; existing behavior unchanged

**Phase 9 Notice:** Version 1.0-demo adds documentation and demonstration materials only. No WS-2 logic, thresholds, or contracts have been modified.
