# QMS Dashboard

Quality Management System intake and artifact generation tool.

## Project Status

**Phase 1: Core Intake System** - ✅ COMPLETE
**Phase 2: Validation Layers** - ✅ COMPLETE
**Phase 4: Artifact Generation** - ✅ COMPLETE
**Phase 5: Expert Review Workflow** - ✅ COMPLETE

### Completed Features

- ✅ Intake form UI (HTML/CSS/JS)
- ✅ Python FastAPI backend
- ✅ Data models (Pydantic)
- ✅ Risk classification engine
- ✅ **6-Layer Validation System:**
  - ✅ Layer 1: Input Validation
  - ✅ Layer 2: Cross-Validation Rules (CV1-CV5)
  - ✅ Layer 3: Risk Indicators (I1-I4)
  - ✅ Layer 4: Warnings & Confirmations (W1-W3)
  - ✅ Layer 5: Expert Review Triggers (ER1-ER5)
  - ✅ Layer 6: Override & Justification
- ✅ **Artifact Generation System:**
  - ✅ 11 QMS artifact templates
  - ✅ Context-aware content population
  - ✅ Risk-based artifact selection (5/8/11 artifacts)
  - ✅ Markdown file generation
  - ✅ ZIP archive download
- ✅ **Expert Review Workflow:**
  - ✅ Review request generation with full intake context
  - ✅ Email notifications (SMTP-based, configurable)
  - ✅ Expert review interface (approve/override/request-info)
  - ✅ Review logging and audit trail
  - ✅ Metrics tracking (request rate, override rate, SLA compliance)
  - ✅ SLA-based review urgency
- ✅ File-based storage
- ✅ Comprehensive test suite (23/23 - 100%)

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
# Start the FastAPI server
cd src/backend
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **Frontend:** http://localhost:8000/
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Run Tests

```bash
# Run classification tests
python test_intake.py
```

## Architecture

```
QMS Dashboard/
├── src/
│   ├── frontend/           # HTML/CSS/JS intake form
│   │   ├── intake.html     # Main intake form
│   │   └── intake.js       # Form interactivity
│   └── backend/            # Python FastAPI backend
│       ├── main.py         # FastAPI application
│       ├── models/         # Pydantic data models
│       │   └── intake.py
│       └── validation/     # Validation layers
│           ├── classifier.py   # Risk classification
│           └── layer1.py       # Input validation
├── data/
│   └── intake-responses/   # Saved intake responses (JSON)
├── test_intake.py          # Classification tests
└── requirements.txt        # Python dependencies
```

## Risk Classification

The system implements a 4-tier risk classification based on intake responses:

- **R0 (Minimal):** Internal, low impact, fully reversible
- **R1 (Moderate):** Internal, moderate impact, reversible
- **R2 (Strict):** External users, decision-impacting, or auditable
- **R3 (Maximum):** Safety, legal, financial, or hard-to-reverse consequences

### Classification Logic

See `src/backend/validation/classifier.py` for detailed implementation based on:
- intake-rules.md (classification rules)
- intake-safety-mechanisms.md (6-layer validation)

## API Endpoints

### POST /api/intake
Submit quality intake and receive risk classification.

**Request:**
```json
{
  "project_name": "Example Project",
  "timestamp": "2025-12-13T10:00:00Z",
  "answers": {
    "q1_users": "Internal",
    "q2_influence": "Recommendations",
    "q3_worst_failure": "Safety_Legal_Compliance",
    "q4_reversibility": "Easy",
    "q5_domain": "Partially",
    "q6_scale": "Individual",
    "q7_regulated": "No"
  }
}
```

**Response:**
```json
{
  "intake_id": "uuid",
  "project_name": "Example Project",
  "classification": {
    "risk_level": "R2",
    "rigor": "Strict",
    "rationale": "R2 classification due to: ...",
    "borderline": true
  },
  "warnings": [...],
  "expert_review_required": false,
  "expert_review_recommended": true,
  "next_steps": [...],
  "artifacts_required": [...]
}
```

### GET /api/intake/{intake_id}
Retrieve a saved intake response.

### GET /api/intakes
List all saved intake responses (summary view).

### POST /api/intake/{intake_id}/generate-artifacts
Generate QMS artifacts for an existing intake. Returns artifact file paths and ZIP archive.

### POST /api/review-request/{intake_id}
Create an expert review request for an intake. Sends email notification to designated experts.

### GET /api/review/{review_id}
Get details of an expert review request.

### GET /api/reviews/pending
List all pending expert review requests.

### POST /api/review/{review_id}/approve
Expert approves the calculated classification.

### POST /api/review/{review_id}/override
Expert overrides the calculated classification with justification.

### POST /api/review/{review_id}/request-info
Expert requests more information from user before making decision.

### GET /api/reviews/metrics
Get expert review effectiveness metrics (request rate, override rate, SLA compliance).

## Testing

### Classification Tests (test_intake.py)
Validates classification logic with 6 realistic scenarios:

1. **Sarah - E-commerce Checkout** → R3 (Automated financial actions)
2. **Marcus - Internal API** → R1 (Multi-team scale)
3. **Aisha - Medical Image Analysis** → R3 (Safety/legal + hard reversibility)
4. **Tom - Monitoring Dashboard** → R1 (Multi-team, informational)
5. **QMS Dashboard (Self)** → R2 (Recommendations + safety/legal, borderline R3)
6. **Rachel - Auth Service** → R3 (Security breach = safety/legal)

### Validation Layer Tests (test_validation_layers.py)
Tests all 6 validation layers with 9 comprehensive scenarios covering CV1-CV5, I1-I4, W1-W3, ER1-ER5, and override validation.

### Artifact Generation Tests (test_artifact_generation.py)
Tests artifact generation for R0 (5 artifacts) and R2 (11 artifacts) with context-aware content population.

### Expert Review Tests (test_expert_review.py)
Tests expert review workflow including:
- Review request generation and formatting
- Review storage and retrieval
- Expert approval workflow
- Expert override workflow (upgrade/downgrade)
- Metrics tracking (request rate, override rate, SLA compliance)

**Total: 23/23 tests passing (100%)**

## Quality Documentation

- **QUALITY_KERNEL.md** - Quality-first initialization
- **intake-rules.md** - Core classification rules
- **intake-user.md v1.0** - User-facing intake form (5.2KB)
- **intake-rules-enhanced.md** - Comprehensive guidance (18KB)
- **intake-safety-mechanisms.md** - 6-layer validation system
- **QMS-*.md** - Quality management artifacts (11 files)

## Next Steps (Phases 6-7)

- [x] **Phase 1:** Core Intake System - COMPLETE
- [x] **Phase 2:** Validation Layers (6-layer safety system) - COMPLETE
- [x] **Phase 3:** Classification Engine - COMPLETE (implemented in Phase 1)
- [x] **Phase 4:** Artifact Generation (auto-generate QMS artifacts) - COMPLETE
- [x] **Phase 5:** Expert Review Workflow - COMPLETE
- [ ] **Phase 6:** Testing & Verification (VER-001 through VER-008)
- [ ] **Phase 7:** Deployment & Monitoring

See **Implementation-Plan.md** for detailed roadmap.

## License

Internal use only.

## Version

**Version:** 1.5.0 (Phases 1, 2, 4, 5)
**Date:** 2025-12-15
**Risk Level:** R2 (Strict rigor)
