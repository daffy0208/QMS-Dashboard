# Phase 5 v1 Realignment

**Date:** 2025-12-15
**Status:** REALIGNMENT IN PROGRESS

## Problem Statement

Phase 5 was implemented with v2+ scope including:
- Email notifications
- SLA tracking
- Metrics dashboards
- Queue management
- Workflow infrastructure

**This exceeds Phase 5 v1 requirements.**

## Phase 5 v1 Definition (Hard Constraints)

Phase 5 v1 is a **RECORDED DECISION** system, not a process engine.

### What Phase 5 v1 MUST provide:
1. ReviewRequest (why review triggered, linked to intake_id)
2. ReviewDecision (approve/override/request_info + justification)
3. Immutable audit record stored with intake
4. Ability to attach review outcome to classification + artifacts

### What Phase 5 v1 MUST NOT include:
- ❌ Email notifications
- ❌ SLAs
- ❌ Metrics tracking
- ❌ Queue management
- ❌ Dashboards
- ❌ Assumptions about reviewers or org maturity

---

## Files Analysis

### QUARANTINE (Phase 5 v2+ - Deferred)

#### 1. **src/backend/review/notifications.py** - ENTIRE FILE
- **Size:** 240 lines
- **Reason:** Email system, SMTP configuration, reminders
- **Status:** Move to `src/backend/review/_v2_notifications.py`
- **Action:** Prefix with underscore, add v2+ marker

#### 2. **src/backend/review/request_generator.py** - PARTIAL
- **Keep:** `create_review_request()` core logic
- **Quarantine:**
  - `format_review_email_subject()`
  - `format_review_email_body()`
  - `_calculate_sla_due_date()`
- **Action:** Remove email/SLA functions, keep minimal request creation

#### 3. **src/backend/models/review.py** - PARTIAL
- **Keep:**
  - ReviewRequest (without SLA fields)
  - ReviewResponse
  - ReviewApproval
  - ReviewOverride
  - ReviewInfoRequest
  - ReviewLog
  - ReviewTrigger
  - IntakeDiscrepancy
- **Quarantine:**
  - ReviewMetrics class (entire class)
  - ReviewRequest.sla_due_date field
  - ReviewRequest.assigned_to field
- **Action:** Comment out metrics class, remove SLA/assignment fields

#### 4. **src/backend/review/storage.py** - PARTIAL
- **Keep:**
  - save_review_request()
  - load_review_request()
  - save_review_response()
  - load_review_response()
  - list_pending_reviews() (simple query)
  - append_to_review_log()
- **Quarantine:**
  - update_metrics()
  - load_metrics()
  - save_metrics()
  - ReviewMetrics tracking
- **Action:** Remove metrics functions

#### 5. **src/backend/main.py** - PARTIAL (API endpoints)
- **Keep (4 endpoints):**
  - POST /api/review-request/{intake_id} (simplified, no email)
  - GET /api/review/{review_id}
  - POST /api/review/{review_id}/approve
  - POST /api/review/{review_id}/override
- **Quarantine (3 endpoints):**
  - GET /api/reviews/pending (queue management)
  - POST /api/review/{review_id}/request-info (workflow feature)
  - GET /api/reviews/metrics (metrics dashboard)
- **Action:** Comment out quarantined endpoints

#### 6. **test_expert_review.py** - PARTIAL
- **Keep:** Basic review creation and approval tests
- **Quarantine:** Metrics tests, email tests, SLA tests
- **Action:** Comment out v2+ tests

---

### KEEP ACTIVE (Phase 5 v1)

#### Core Data Models (models/review.py - reduced)
```python
- ReviewRequest (minimal: review_id, intake_id, project_name, answers, classification, warnings, triggers)
- ReviewResponse (decision data)
- ReviewApproval (approve with comments)
- ReviewOverride (override with justification)
- ReviewLog (audit entry)
- ReviewTrigger (why review needed)
- IntakeDiscrepancy (answer vs reality gaps)
```

#### Core Storage (review/storage.py - reduced)
```python
- save_review_request()      # Store review request
- load_review_request()       # Retrieve review request
- save_review_response()      # Store expert decision
- load_review_response()      # Retrieve decision
- append_to_review_log()      # Audit trail
```

#### Core API (main.py - 4 endpoints)
```python
POST /api/review-request/{intake_id}
  - Create review request (no email)
  - Store with intake

GET /api/review/{review_id}
  - Retrieve review details

POST /api/review/{review_id}/approve
  - Record approval decision

POST /api/review/{review_id}/override
  - Record override with justification
```

---

## Minimal Code Changes Required

### 1. models/review.py
```python
# REMOVE from ReviewRequest:
- sla_due_date: Optional[datetime]
- assigned_to: Optional[str]

# COMMENT OUT entirely:
class ReviewMetrics:
    # Phase 5 v2+ - Deferred
    pass
```

### 2. review/storage.py
```python
# REMOVE functions:
- update_metrics()
- load_metrics()
- save_metrics()

# REMOVE from other functions:
- All metrics update calls
- SLA tracking code
```

### 3. review/request_generator.py
```python
# REMOVE functions:
- format_review_email_subject()
- format_review_email_body()
- _calculate_sla_due_date()

# SIMPLIFY create_review_request():
- Remove SLA calculation
- Remove email formatting
```

### 4. main.py
```python
# COMMENT OUT endpoints:
- GET /api/reviews/pending
- POST /api/review/{review_id}/request-info
- GET /api/reviews/metrics

# SIMPLIFY POST /api/review-request/{intake_id}:
- Remove email sending
- Remove metrics updates
- Remove SLA logic
```

### 5. Move to quarantine
```bash
mv src/backend/review/notifications.py src/backend/review/_v2_notifications.py.deferred
```

---

## Verification Checklist

After realignment, Phase 5 v1 must:
- [ ] Store review requests linked to intake
- [ ] Store review decisions (approve/override)
- [ ] Maintain immutable audit log
- [ ] Attach review outcome to intake/artifacts
- [ ] Run without any external services (no SMTP, no email)
- [ ] Have no SLA, metrics, or queue features active

---

## Phase 5 v2+ Deferred Features

The following will be implemented in Phase 5 v2:
- Email notifications to experts
- SLA tracking and enforcement
- Metrics dashboard (request rate, override rate, turnaround time)
- Queue management (pending reviews list)
- Reminder system
- Expert assignment workflow
- Request-for-information workflow

---

## Next Steps

1. Execute code changes to quarantine v2+ features
2. Test that Phase 5 v1 still functions
3. Update documentation to reflect v1 scope
4. Mark quarantined files/sections clearly
5. Verify system runs without external dependencies

---

**Principle:** Phase 5 v1 is a simple audit/decision recording system, not a workflow engine.
