#!/usr/bin/env python3
"""
Test script for Phase 5: Expert Review Workflow.
Tests expert review request generation, approvals, overrides, and metrics.
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from models.intake import IntakeRequest, IntakeResponse, IntakeAnswers, RiskClassification
from models.review import (
    ReviewRequest,
    ReviewResponse,
    ReviewApproval,
    ReviewOverride,
    ReviewInfoRequest,
    ReviewTrigger,
    IntakeDiscrepancy
)
from review.request_generator import (
    create_review_request,
    format_review_request_text
    # Phase 5 v2+ - Email formatting functions quarantined
    # format_review_email_subject,
    # format_review_email_body
)
from review.storage import ReviewStorage


def test_create_review_request():
    """Test creating an expert review request."""
    print("\n" + "="*60)
    print("TEST: Create Expert Review Request")
    print("="*60)

    # Create sample intake
    intake_request = IntakeRequest(
        project_name="High-Risk Medical System",
        timestamp=datetime.now(timezone.utc),
        answers=IntakeAnswers(
            q1_users="External",
            q2_influence="Automated",
            q3_worst_failure="Safety_Legal_Compliance",
            q4_reversibility="Hard",
            q5_domain="Partially",
            q6_scale="Multi_team",
            q7_regulated="Yes"
        )
    )

    intake_response = IntakeResponse(
        intake_id="test-intake-123",
        project_name="High-Risk Medical System",
        timestamp=datetime.now(timezone.utc),
        answers=intake_request.answers,
        classification=RiskClassification(
            risk_level="R3",
            rigor="Maximum",
            rationale="R3 due to: Safety/legal concerns + automated actions + hard reversibility",
            borderline=False
        ),
        warnings=[],
        expert_review_required=True,
        expert_review_recommended=True,
        next_steps=[],
        artifacts_required=[]
    )

    # Create review triggers
    review_triggers = [
        ReviewTrigger(
            trigger_id="ER1",
            description="Safety-critical system requiring expert validation",
            severity="mandatory"
        ),
        ReviewTrigger(
            trigger_id="ER3",
            description="Regulated domain (medical) - expert review mandatory",
            severity="mandatory"
        )
    ]

    # Create review request
    review_request = create_review_request(
        intake_request=intake_request,
        intake_response=intake_response,
        review_type="mandatory",
        review_triggers=review_triggers,
        user_comment="Unsure if R3 is appropriate for this prototype phase"
    )

    # Verify review request
    assert review_request.project_name == "High-Risk Medical System"
    assert review_request.review_type == "mandatory"
    assert review_request.calculated_classification == "R3"
    assert review_request.confidence == "HIGH"
    assert len(review_request.review_triggers) == 2
    assert review_request.user_comment is not None
    # Phase 5 v2+ - SLA tracking removed
    # assert review_request.sla_due_date is not None

    print(f"✅ Review request created: {review_request.review_id}")
    print(f"   Project: {review_request.project_name}")
    print(f"   Type: {review_request.review_type}")
    print(f"   Classification: {review_request.calculated_classification}")
    print(f"   Confidence: {review_request.confidence}")
    # Phase 5 v2+ - SLA tracking removed
    # print(f"   SLA Due: {review_request.sla_due_date}")

    return review_request


def test_format_review_request():
    """Test formatting review request as text."""
    print("\n" + "="*60)
    print("TEST: Format Review Request Text")
    print("="*60)

    # Create sample intake
    intake_request = IntakeRequest(
        project_name="Test System",
        timestamp=datetime.now(timezone.utc),
        answers=IntakeAnswers(
            q1_users="Internal",
            q2_influence="Recommendations",
            q3_worst_failure="Safety_Legal_Compliance",
            q4_reversibility="Easy",
            q5_domain="Partially",
            q6_scale="Individual",
            q7_regulated="No"
        )
    )

    intake_response = IntakeResponse(
        intake_id="test-123",
        project_name="Test System",
        timestamp=datetime.now(timezone.utc),
        answers=intake_request.answers,
        classification=RiskClassification(
            risk_level="R2",
            rigor="Strict",
            rationale="R2 due to recommendations + safety concerns",
            borderline=True
        ),
        warnings=[],
        expert_review_required=False,
        expert_review_recommended=True,
        next_steps=[],
        artifacts_required=[]
    )

    review_triggers = [
        ReviewTrigger(
            trigger_id="ER2",
            description="Borderline classification - expert review recommended",
            severity="recommended"
        )
    ]

    review_request = create_review_request(
        intake_request=intake_request,
        intake_response=intake_response,
        review_type="recommended",
        review_triggers=review_triggers
    )

    # Format as text
    text = format_review_request_text(review_request)

    assert "Expert Review Request" in text
    assert review_request.project_name in text
    assert review_request.calculated_classification in text
    assert "Review Checklist" in text

    print("✅ Review request formatted successfully")
    print("\n" + "-"*60)
    print(text[:500] + "...")  # Preview first 500 chars
    print("-"*60)

    # ========================================================================
    # Phase 5 v2+ - Email formatting tests quarantined
    # ========================================================================
    # # Test email formatting
    # subject = format_review_email_subject(review_request)
    # assert "Recommended" in subject
    # assert review_request.project_name in subject
    #
    # body = format_review_email_body(review_request, "http://example.com/review")
    # assert "http://example.com/review" in body
    #
    # print(f"\n✅ Email subject: {subject}")
    # print(f"✅ Email body generated ({len(body)} chars}")
    # ========================================================================


def test_review_storage():
    """Test review storage and retrieval."""
    print("\n" + "="*60)
    print("TEST: Review Storage")
    print("="*60)

    # Setup test directory
    test_data_dir = Path(__file__).parent / "data" / "test_reviews"
    if test_data_dir.exists():
        shutil.rmtree(test_data_dir)
    test_data_dir.mkdir(parents=True, exist_ok=True)

    storage = ReviewStorage(test_data_dir)

    # Create sample review request
    intake_request = IntakeRequest(
        project_name="Storage Test Project",
        timestamp=datetime.now(timezone.utc),
        answers=IntakeAnswers(
            q1_users="Internal",
            q2_influence="Informational",
            q3_worst_failure="Annoyance",
            q4_reversibility="Easy",
            q5_domain="Yes",
            q6_scale="Individual",
            q7_regulated="No"
        )
    )

    intake_response = IntakeResponse(
        intake_id="storage-test",
        project_name="Storage Test Project",
        timestamp=datetime.now(timezone.utc),
        answers=intake_request.answers,
        classification=RiskClassification(
            risk_level="R0",
            rigor="Minimal",
            rationale="Low risk internal tool",
            borderline=False
        ),
        warnings=[],
        expert_review_required=False,
        expert_review_recommended=False,
        next_steps=[],
        artifacts_required=[]
    )

    review_request = create_review_request(
        intake_request=intake_request,
        intake_response=intake_response,
        review_type="recommended",
        review_triggers=[ReviewTrigger(
            trigger_id="TEST",
            description="Test trigger",
            severity="recommended"
        )]
    )

    # Save review request
    storage.save_review_request(review_request)

    # Load review request
    loaded = storage.load_review_request(review_request.review_id)
    assert loaded is not None
    assert loaded.project_name == "Storage Test Project"
    assert loaded.calculated_classification == "R0"

    print(f"✅ Review request saved and loaded: {review_request.review_id}")

    # Test listing pending reviews
    pending = storage.list_pending_reviews()
    assert len(pending) == 1
    assert pending[0].review_id == review_request.review_id

    print(f"✅ Pending reviews: {len(pending)}")

    return storage, review_request


def test_expert_approval(storage: ReviewStorage, review_request: ReviewRequest):
    """Test expert approval workflow."""
    print("\n" + "="*60)
    print("TEST: Expert Approval")
    print("="*60)

    approval = ReviewApproval(
        review_id=review_request.review_id,
        reviewer_name="Dr. Jane Smith",
        reviewer_qualifications="Senior QA Engineer, 15 years experience",
        classification_approved=review_request.calculated_classification,
        expert_comments="Classification is appropriate for this internal tool. R0 rigor is sufficient."
    )

    # Create review response
    review_response = ReviewResponse(
        review_id=review_request.review_id,
        intake_id=review_request.intake_id,
        project_name=review_request.project_name,
        reviewer_name=approval.reviewer_name,
        reviewer_qualifications=approval.reviewer_qualifications,
        review_type=review_request.review_type,
        decision="approved",
        original_classification=review_request.calculated_classification,
        final_classification=approval.classification_approved,
        approval=approval,
        review_triggers=review_request.review_triggers,
        outcome="Classification approved, user notified"
    )

    # Save response
    storage.save_review_response(review_response)

    # Load response
    loaded = storage.load_review_response(review_request.review_id)
    assert loaded is not None
    assert loaded.decision == "approved"
    assert loaded.final_classification == review_request.calculated_classification

    print(f"✅ Expert approval saved: {review_request.review_id}")
    print(f"   Reviewer: {approval.reviewer_name}")
    print(f"   Decision: APPROVED")
    print(f"   Classification: {loaded.final_classification}")

    # Phase 5 v2+ - Metrics tracking removed
    # storage.update_metrics(review_request, review_response)

    return review_response


def test_expert_override():
    """Test expert override workflow."""
    print("\n" + "="*60)
    print("TEST: Expert Override")
    print("="*60)

    # Setup
    test_data_dir = Path(__file__).parent / "data" / "test_override"
    if test_data_dir.exists():
        shutil.rmtree(test_data_dir)
    test_data_dir.mkdir(parents=True, exist_ok=True)

    storage = ReviewStorage(test_data_dir)

    # Create intake that might be misclassified
    intake_request = IntakeRequest(
        project_name="Borderline System",
        timestamp=datetime.now(timezone.utc),
        answers=IntakeAnswers(
            q1_users="Internal",
            q2_influence="Recommendations",
            q3_worst_failure="Financial",
            q4_reversibility="Partial",
            q5_domain="Partially",
            q6_scale="Multi_team",
            q7_regulated="No"
        )
    )

    intake_response = IntakeResponse(
        intake_id="override-test",
        project_name="Borderline System",
        timestamp=datetime.now(timezone.utc),
        answers=intake_request.answers,
        classification=RiskClassification(
            risk_level="R1",
            rigor="Moderate",
            rationale="R1 due to internal use + moderate impact",
            borderline=True
        ),
        warnings=[],
        expert_review_required=False,
        expert_review_recommended=True,
        next_steps=[],
        artifacts_required=[]
    )

    review_request = create_review_request(
        intake_request=intake_request,
        intake_response=intake_response,
        review_type="recommended",
        review_triggers=[ReviewTrigger(
            trigger_id="ER2",
            description="Borderline classification",
            severity="recommended"
        )]
    )

    storage.save_review_request(review_request)

    # Expert overrides to R2
    override = ReviewOverride(
        review_id=review_request.review_id,
        reviewer_name="Dr. John Doe",
        reviewer_qualifications="Lead Quality Engineer",
        original_classification="R1",
        new_classification="R2",
        justification="While the intake suggests R1, the financial loss potential at multi-team scale combined with partial reversibility requires R2 rigor. The system's recommendations could lead to significant financial decisions affecting multiple teams, warranting stricter quality controls.",
        intake_discrepancies=[
            IntakeDiscrepancy(
                question_id="q3_worst_failure",
                original_answer="Financial",
                actual_situation="Financial loss at Multi_team scale is more serious than answered",
                explanation="User underestimated the financial impact at multi-team scale"
            )
        ],
        additional_factors="Multi-team scale amplifies financial risk. Organization policy requires R2+ for financial systems.",
        risks_accepted=None  # Upgrade, not downgrade
    )

    review_response = ReviewResponse(
        review_id=review_request.review_id,
        intake_id=review_request.intake_id,
        project_name=review_request.project_name,
        reviewer_name=override.reviewer_name,
        reviewer_qualifications=override.reviewer_qualifications,
        review_type=review_request.review_type,
        decision="overridden",
        original_classification=override.original_classification,
        final_classification=override.new_classification,
        override=override,
        review_triggers=review_request.review_triggers,
        outcome=f"Classification overridden from R1 to R2"
    )

    storage.save_review_response(review_response)

    # Verify
    loaded = storage.load_review_response(review_request.review_id)
    assert loaded is not None
    assert loaded.decision == "overridden"
    assert loaded.original_classification == "R1"
    assert loaded.final_classification == "R2"
    assert loaded.override is not None
    assert len(loaded.override.intake_discrepancies) == 1

    print(f"✅ Expert override saved: {review_request.review_id}")
    print(f"   Reviewer: {override.reviewer_name}")
    print(f"   Decision: OVERRIDDEN")
    print(f"   Change: {override.original_classification} → {override.new_classification}")
    print(f"   Discrepancies: {len(override.intake_discrepancies)}")

    # ========================================================================
    # Phase 5 v2+ - Metrics tracking removed
    # ========================================================================
    # storage.update_metrics(review_request, review_response)
    #
    # metrics = storage.load_metrics()
    # assert metrics.overrides > 0
    # assert metrics.upgrades > 0
    #
    # print(f"✅ Metrics updated: {metrics.overrides} overrides, {metrics.upgrades} upgrades")
    # ========================================================================


# ============================================================================
# PHASE 5 V2+ TEST - QUARANTINED
# Metrics tracking is not part of Phase 5 v1 scope
# Phase 5 v1 is a RECORDED DECISION system, not a metrics engine
# ============================================================================
# def test_review_metrics():
#     """Test review metrics tracking."""
#     print("\n" + "="*60)
#     print("TEST: Review Metrics")
#     print("="*60)
#
#     test_data_dir = Path(__file__).parent / "data" / "test_metrics"
#     if test_data_dir.exists():
#         shutil.rmtree(test_data_dir)
#     test_data_dir.mkdir(parents=True, exist_ok=True)
#
#     storage = ReviewStorage(test_data_dir)
#
#     # Ensure clean metrics start
#     from models.review import ReviewMetrics
#     clean_metrics = ReviewMetrics()
#     storage.save_metrics(clean_metrics)
#
#     # Simulate multiple reviews
#     for i in range(5):
#         intake_request = IntakeRequest(
#             project_name=f"Test Project {i}",
#             timestamp=datetime.utcnow(),
#             answers=IntakeAnswers(
#                 q1_users="Internal",
#                 q2_influence="Informational",
#                 q3_worst_failure="Annoyance",
#                 q4_reversibility="Easy",
#                 q5_domain="Yes",
#                 q6_scale="Individual",
#                 q7_regulated="No"
#             )
#         )
#
#         intake_response = IntakeResponse(
#             intake_id=f"metric-test-{i}",
#             project_name=f"Test Project {i}",
#             timestamp=datetime.utcnow(),
#             answers=intake_request.answers,
#             classification=RiskClassification(
#                 risk_level="R0",
#                 rigor="Minimal",
#                 rationale="Low risk",
#                 borderline=False
#             ),
#             warnings=[],
#             expert_review_required=False,
#             expert_review_recommended=True,
#             next_steps=[],
#             artifacts_required=[]
#         )
#
#         review_request = create_review_request(
#             intake_request=intake_request,
#             intake_response=intake_response,
#             review_type="recommended" if i < 3 else "mandatory",
#             review_triggers=[ReviewTrigger(
#                 trigger_id="TEST",
#                 description="Test",
#                 severity="recommended" if i < 3 else "mandatory"
#             )]
#         )
#
#         storage.save_review_request(review_request)
#         storage.update_metrics(review_request)
#
#         # Simulate approval for some
#         if i < 4:
#             approval = ReviewApproval(
#                 review_id=review_request.review_id,
#                 reviewer_name="Test Reviewer",
#                 reviewer_qualifications="Expert",
#                 classification_approved=review_request.calculated_classification
#             )
#
#             review_response = ReviewResponse(
#                 review_id=review_request.review_id,
#                 intake_id=review_request.intake_id,
#                 project_name=review_request.project_name,
#                 reviewer_name=approval.reviewer_name,
#                 reviewer_qualifications=approval.reviewer_qualifications,
#                 review_type=review_request.review_type,
#                 decision="approved",
#                 original_classification=review_request.calculated_classification,
#                 final_classification=approval.classification_approved,
#                 approval=approval,
#                 review_triggers=review_request.review_triggers,
#                 outcome="Approved"
#             )
#
#             storage.save_review_response(review_response)
#             storage.update_metrics(review_request, review_response)
#
#     # Load and verify metrics
#     metrics = storage.load_metrics()
#
#     print(f"\n[DEBUG] Metrics values:")
#     print(f"   review_requests: {metrics.review_requests} (expected: 5)")
#     print(f"   mandatory_reviews: {metrics.mandatory_reviews} (expected: 2)")
#     print(f"   recommended_reviews: {metrics.recommended_reviews} (expected: 3)")
#     print(f"   approvals: {metrics.approvals} (expected: 4)")
#
#     assert metrics.review_requests == 5, f"Expected 5 review_requests, got {metrics.review_requests}"
#     assert metrics.mandatory_reviews == 2, f"Expected 2 mandatory_reviews, got {metrics.mandatory_reviews}"
#     assert metrics.recommended_reviews == 3, f"Expected 3 recommended_reviews, got {metrics.recommended_reviews}"
#     assert metrics.approvals == 4, f"Expected 4 approvals, got {metrics.approvals}"
#
#     print(f"\n✅ Metrics tracking verified:")
#     print(f"   Total reviews: {metrics.review_requests}")
#     print(f"   Mandatory: {metrics.mandatory_reviews}")
#     print(f"   Recommended: {metrics.recommended_reviews}")
#     print(f"   Approvals: {metrics.approvals}")
#     print(f"   Review request rate: {metrics.review_request_rate:.1f}%")
#     print(f"   Override rate: {metrics.override_rate:.1f}%")
# ============================================================================


def main():
    """Run all expert review tests."""
    print("QMS Dashboard - Phase 5: Expert Review Workflow Tests")
    print("="*60)

    tests = [
        ("Create Review Request", test_create_review_request),
        ("Format Review Request", test_format_review_request),
        ("Review Storage", lambda: test_review_storage()),
        ("Expert Override", test_expert_override),
        # Phase 5 v2+ - Metrics test quarantined
        # ("Review Metrics", test_review_metrics),
    ]

    passed = 0
    failed = 0
    results = {}

    for test_name, test_func in tests:
        try:
            if test_name == "Review Storage":
                storage, review_request = test_func()
                results["storage"] = storage
                results["review_request"] = review_request
            elif test_name == "Expert Approval":
                test_expert_approval(results["storage"], results["review_request"])
            else:
                test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ FAILED: {test_name}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ ERROR: {test_name}")
            print(f"   Exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    # Run expert approval test after storage
    if "storage" in results and "review_request" in results:
        try:
            test_expert_approval(results["storage"], results["review_request"])
            passed += 1
        except Exception as e:
            print(f"\n❌ ERROR: Expert Approval")
            print(f"   Exception: {e}")
            failed += 1

    # Summary
    print("\n" + "="*60)
    print(f"TEST SUMMARY")
    print("="*60)
    print(f"Tests Passed: {passed}/{len(tests) + 1}")  # +1 for expert approval
    print(f"Tests Failed: {failed}/{len(tests) + 1}")

    if failed == 0:
        print("\n✅ All expert review tests passed!")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
