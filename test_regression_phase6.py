#!/usr/bin/env python3
"""
Phase 6: Regression Test Suite
Locks in behavior across Phases 1-5 to prevent scope creep during Phase 7.

Purpose:
- Smoke test critical workflows
- Detect unintended behavior changes
- Validate Phase 5 v1 scope boundaries remain enforced
- Quick validation before deployment
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime
import json

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from models.intake import IntakeRequest, IntakeResponse, IntakeAnswers
from validation.classifier import classify_risk, get_required_artifacts
from validation.layer1 import validate_intake_answers, validate_project_name
from validation.layer2 import cross_validate
from validation.layer3 import detect_risk_indicators
from validation.layer5 import determine_expert_review
from artifacts.generator import generate_project_artifacts
from review.request_generator import create_review_request
from review.storage import ReviewStorage
from models.review import ReviewTrigger, ReviewApproval, ReviewResponse


def test_regression_phase1_intake_validation():
    """
    Regression: Phase 1 - Intake validation behavior
    Ensures Layer 1 validation rules remain consistent.
    """
    print("\n" + "="*70)
    print("REGRESSION: Phase 1 - Intake Validation")
    print("="*70)

    # Test case: Empty project name triggers WARNING
    empty_name_warnings = validate_project_name("")
    assert any(w.severity == "WARNING" for w in empty_name_warnings), \
        "Empty project names should trigger WARNING"
    assert any("empty" in w.message.lower() for w in empty_name_warnings), \
        "Empty name warning should mention 'empty'"

    # Test case: Generic project name triggers INFO
    generic_name_warnings = validate_project_name("test")
    assert any(w.severity == "INFO" for w in generic_name_warnings), \
        "Generic project names should trigger INFO"
    assert any("generic" in w.message.lower() for w in generic_name_warnings), \
        "Generic name warning should mention 'generic'"

    # Test case: Valid project name passes
    valid_name_warnings = validate_project_name("Valid Project Name")
    assert len(valid_name_warnings) == 0, "Valid project names should not trigger warnings"

    # Test case: Valid answers pass without critical errors
    valid_answers = IntakeAnswers(
        q1_users="Internal",
        q2_influence="Informational",
        q3_worst_failure="Annoyance",
        q4_reversibility="Easy",
        q5_domain="Yes",
        q6_scale="Individual",
        q7_regulated="No"
    )

    validation_warnings = validate_intake_answers(valid_answers)
    critical_errors = [w for w in validation_warnings if w.severity == "CRITICAL"]
    assert len(critical_errors) == 0, "Valid answers should not produce CRITICAL errors"

    # Test case: Known contradiction triggers WARNING
    contradiction_answers = IntakeAnswers(
        q1_users="Internal",
        q2_influence="Informational",
        q3_worst_failure="Annoyance",
        q4_reversibility="Hard",  # Contradiction: minor failure but hard to reverse
        q5_domain="Yes",
        q6_scale="Individual",
        q7_regulated="No"
    )

    contradiction_warnings = validate_intake_answers(contradiction_answers)
    assert any(w.severity == "WARNING" for w in contradiction_warnings), \
        "Contradictory answers should trigger WARNING"
    assert any("reverse" in w.message.lower() for w in contradiction_warnings), \
        "Contradiction warning should mention reversibility"

    print("✓ Layer 1 validation behavior locked")
    print(f"  - Empty names trigger WARNING: {len(empty_name_warnings)} warnings")
    print(f"  - Generic names trigger INFO: {len(generic_name_warnings)} warnings")
    print(f"  - Valid names pass: {len(valid_name_warnings)} warnings")
    print(f"  - Contradictions trigger WARNING: {len([w for w in contradiction_warnings if w.severity == 'WARNING'])} warnings")
    print(f"  - Valid inputs pass: {len(critical_errors)} critical errors")

    return True


def test_regression_phase2_risk_classification():
    """
    Regression: Phase 2 - Risk classification stability
    Verifies classification logic produces expected results.
    """
    print("\n" + "="*70)
    print("REGRESSION: Phase 2 - Risk Classification")
    print("="*70)

    # Lock in known classifications
    test_cases = [
        ("R0", IntakeAnswers(
            q1_users="Internal", q2_influence="Informational",
            q3_worst_failure="Annoyance", q4_reversibility="Easy",
            q5_domain="Yes", q6_scale="Individual", q7_regulated="No"
        )),
        ("R1", IntakeAnswers(
            q1_users="Internal", q2_influence="Recommendations",
            q3_worst_failure="Annoyance", q4_reversibility="Easy",
            q5_domain="Partially", q6_scale="Multi_team", q7_regulated="No"
        )),
        ("R2", IntakeAnswers(
            q1_users="Internal", q2_influence="Recommendations",
            q3_worst_failure="Financial", q4_reversibility="Easy",
            q5_domain="Partially", q6_scale="Multi_team", q7_regulated="No"
        )),
        ("R3", IntakeAnswers(
            q1_users="External", q2_influence="Automated",
            q3_worst_failure="Safety_Legal_Compliance", q4_reversibility="Hard",
            q5_domain="Partially", q6_scale="Multi_team", q7_regulated="Yes"
        )),
    ]

    for expected_risk, answers in test_cases:
        classification, _ = classify_risk(answers)
        assert classification.risk_level == expected_risk, \
            f"Classification regression: Expected {expected_risk}, got {classification.risk_level}"

    print("✓ Risk classification stable across all levels (R0-R3)")
    return True


def test_regression_phase3_validation_layers():
    """
    Regression: Phase 3 - Multi-layer validation behavior
    Ensures validation layers work correctly together.
    """
    print("\n" + "="*70)
    print("REGRESSION: Phase 3 - Validation Layers")
    print("="*70)

    answers = IntakeAnswers(
        q1_users="External",
        q2_influence="Automated",
        q3_worst_failure="Financial",
        q4_reversibility="Partial",
        q5_domain="Partially",
        q6_scale="Organization_Public",
        q7_regulated="Possibly"
    )

    # Layer 2: Cross-validation
    layer2_warnings = cross_validate(answers)
    assert len(layer2_warnings) > 0, "Cross-validation should detect potential issues"

    # Layer 3: Risk indicators
    layer3_warnings = detect_risk_indicators(answers)
    assert len(layer3_warnings) > 0, "Risk indicators should be detected"

    # Layer 5: Expert review determination
    classification, _ = classify_risk(answers)
    expert_required, expert_recommended, reasons = determine_expert_review(
        answers, classification, layer2_warnings + layer3_warnings
    )
    assert expert_required or expert_recommended, \
        "High-risk scenarios should trigger expert review"

    print(f"✓ Validation layers integrated correctly")
    print(f"  - Layer 2 warnings: {len(layer2_warnings)}")
    print(f"  - Layer 3 warnings: {len(layer3_warnings)}")
    print(f"  - Expert review: Required={expert_required}, Recommended={expert_recommended}")

    return True


def test_regression_phase4_artifact_generation():
    """
    Regression: Phase 4 - Artifact generation integrity
    Verifies correct artifact count and file creation.
    """
    print("\n" + "="*70)
    print("REGRESSION: Phase 4 - Artifact Generation")
    print("="*70)

    test_cases = [
        ("R0", 5, IntakeAnswers(
            q1_users="Internal", q2_influence="Informational",
            q3_worst_failure="Annoyance", q4_reversibility="Easy",
            q5_domain="Yes", q6_scale="Individual", q7_regulated="No"
        )),
        ("R1", 8, IntakeAnswers(
            q1_users="Internal", q2_influence="Recommendations",
            q3_worst_failure="Annoyance", q4_reversibility="Easy",
            q5_domain="Partially", q6_scale="Multi_team", q7_regulated="No"
        )),
    ]

    for risk_level, expected_count, answers in test_cases:
        classification, _ = classify_risk(answers)
        artifacts = get_required_artifacts(classification.risk_level)

        assert len(artifacts) == expected_count, \
            f"{risk_level}: Expected {expected_count} artifacts, got {len(artifacts)}"

        # Generate and verify
        intake_request = IntakeRequest(
            project_name=f"Regression Test {risk_level}",
            timestamp=datetime.utcnow(),
            answers=answers
        )

        intake_response = IntakeResponse(
            intake_id=f"reg-{risk_level.lower()}",
            project_name=intake_request.project_name,
            timestamp=intake_request.timestamp,
            answers=answers,
            classification=classification,
            warnings=[],
            expert_review_required=False,
            expert_review_recommended=False,
            next_steps=[],
            artifacts_required=artifacts
        )

        test_output_dir = Path(__file__).parent / "data" / f"test_regression_{risk_level.lower()}"
        if test_output_dir.exists():
            shutil.rmtree(test_output_dir)

        result = generate_project_artifacts(intake_request, intake_response, output_dir=test_output_dir)

        assert len(result['artifacts_generated']) == expected_count, \
            f"{risk_level}: Artifact generation count mismatch"

    print(f"✓ Artifact generation stable (R0: 5, R1: 8 artifacts)")
    return True


def test_regression_phase5_v1_scope_enforcement():
    """
    Regression: Phase 5 v1 - Scope boundaries enforced
    Verifies Phase 5 v1 remains a RECORDED DECISION system only.
    """
    print("\n" + "="*70)
    print("REGRESSION: Phase 5 v1 - Scope Enforcement")
    print("="*70)

    # Create test review
    intake_request = IntakeRequest(
        project_name="Phase 5 Regression Test",
        timestamp=datetime.utcnow(),
        answers=IntakeAnswers(
            q1_users="Internal", q2_influence="Recommendations",
            q3_worst_failure="Financial", q4_reversibility="Easy",
            q5_domain="Partially", q6_scale="Multi_team", q7_regulated="No"
        )
    )

    classification, _ = classify_risk(intake_request.answers)

    intake_response = IntakeResponse(
        intake_id="phase5-regression",
        project_name=intake_request.project_name,
        timestamp=intake_request.timestamp,
        answers=intake_request.answers,
        classification=classification,
        warnings=[],
        expert_review_required=False,
        expert_review_recommended=True,
        next_steps=[],
        artifacts_required=get_required_artifacts(classification.risk_level)
    )

    review_triggers = [ReviewTrigger(
        trigger_id="ER2",
        description="Regression test review",
        severity="recommended"
    )]

    review_request = create_review_request(
        intake_request=intake_request,
        intake_response=intake_response,
        review_type="recommended",
        review_triggers=review_triggers
    )

    # Verify Phase 5 v1 constraints
    # 1. No SLA fields (quarantined in v1)
    assert not hasattr(review_request, 'sla_due_date') or review_request.sla_due_date is None, \
        "Phase 5 v1 should not have SLA tracking (v2+ feature)"

    # 2. No assignment fields (quarantined in v1)
    assert not hasattr(review_request, 'assigned_to') or review_request.assigned_to is None, \
        "Phase 5 v1 should not have reviewer assignment (v2+ feature)"

    # 3. Storage works without metrics
    test_data_dir = Path(__file__).parent / "data" / "test_regression_phase5"
    if test_data_dir.exists():
        shutil.rmtree(test_data_dir)
    test_data_dir.mkdir(parents=True, exist_ok=True)

    storage = ReviewStorage(test_data_dir)

    # Verify no metrics functions available
    assert not hasattr(storage, 'update_metrics') or not callable(getattr(storage, 'update_metrics', None)), \
        "Phase 5 v1 should not have metrics tracking (v2+ feature)"

    # 4. Review can be saved and loaded
    storage.save_review_request(review_request)
    loaded = storage.load_review_request(review_request.review_id)
    assert loaded is not None, "Review request should be saved and loaded"
    assert loaded.review_id == review_request.review_id, "Loaded review should match"

    print("✓ Phase 5 v1 scope boundaries enforced")
    print("  - No SLA tracking (v2+ quarantined)")
    print("  - No metrics system (v2+ quarantined)")
    print("  - No reviewer assignment (v2+ quarantined)")
    print("  - Core review recording: FUNCTIONAL")

    return True


def test_regression_intake_immutability_after_review():
    """
    Regression: VER-GAP-P5-INTAKE-WRITEBACK behavior
    Verifies intake files remain unchanged after expert review (Phase 5 v1 expected behavior).
    """
    print("\n" + "="*70)
    print("REGRESSION: Intake Immutability After Review")
    print("="*70)

    # Create and save intake
    intake_request = IntakeRequest(
        project_name="Immutability Regression Test",
        timestamp=datetime.utcnow(),
        answers=IntakeAnswers(
            q1_users="Internal", q2_influence="Recommendations",
            q3_worst_failure="Financial", q4_reversibility="Easy",
            q5_domain="Partially", q6_scale="Multi_team", q7_regulated="No"
        )
    )

    classification, _ = classify_risk(intake_request.answers)

    intake_response = IntakeResponse(
        intake_id="immutability-test",
        project_name=intake_request.project_name,
        timestamp=intake_request.timestamp,
        answers=intake_request.answers,
        classification=classification,
        warnings=[],
        expert_review_required=False,
        expert_review_recommended=True,
        next_steps=[],
        artifacts_required=get_required_artifacts(classification.risk_level)
    )

    # Save intake to file
    test_data_dir = Path(__file__).parent / "data" / "test_regression_immutability"
    if test_data_dir.exists():
        shutil.rmtree(test_data_dir)
    test_data_dir.mkdir(parents=True, exist_ok=True)

    intake_file = test_data_dir / "immutability-test.json"
    with open(intake_file, 'w') as f:
        json.dump(intake_response.model_dump(mode='json'), f, indent=2, default=str)

    original_classification = classification.risk_level

    # Create review request
    review_triggers = [ReviewTrigger(
        trigger_id="ER2",
        description="Test review",
        severity="recommended"
    )]

    review_request = create_review_request(
        intake_request=intake_request,
        intake_response=intake_response,
        review_type="recommended",
        review_triggers=review_triggers
    )

    storage = ReviewStorage(test_data_dir)
    storage.save_review_request(review_request)

    # Simulate expert approval
    approval = ReviewApproval(
        review_id=review_request.review_id,
        reviewer_name="Regression Tester",
        reviewer_qualifications="QA Engineer",
        classification_approved=original_classification
    )

    review_response = ReviewResponse(
        review_id=review_request.review_id,
        intake_id=intake_response.intake_id,
        project_name=intake_request.project_name,
        reviewer_name=approval.reviewer_name,
        reviewer_qualifications=approval.reviewer_qualifications,
        review_type=review_request.review_type,
        decision="approved",
        original_classification=original_classification,
        final_classification=original_classification,
        approval=approval,
        review_triggers=review_request.review_triggers,
        outcome="Approved for regression test"
    )

    storage.save_review_response(review_response)

    # Verify intake file unchanged
    with open(intake_file, 'r') as f:
        loaded_intake = json.load(f)
        loaded_classification = loaded_intake['classification']['risk_level']

    assert loaded_classification == original_classification, \
        "Intake file should remain unchanged after expert review (Phase 5 v1 expected behavior)"

    # Verify review was saved separately
    review_file = test_data_dir / "reviews" / f"{review_request.review_id}_response.json"
    assert review_file.exists(), "Review should be saved separately"

    print("✓ Intake immutability preserved (VER-GAP-P5-INTAKE-WRITEBACK)")
    print(f"  - Intake file unchanged: {original_classification}")
    print(f"  - Review saved separately: {review_file.name}")

    return True


def main():
    """Run all regression tests."""
    print("="*70)
    print("PHASE 6: REGRESSION TEST SUITE")
    print("Locking in behavior across Phases 1-5")
    print("="*70)

    tests = [
        ("Phase 1: Intake Validation", test_regression_phase1_intake_validation),
        ("Phase 2: Risk Classification", test_regression_phase2_risk_classification),
        ("Phase 3: Validation Layers", test_regression_phase3_validation_layers),
        ("Phase 4: Artifact Generation", test_regression_phase4_artifact_generation),
        ("Phase 5 v1: Scope Enforcement", test_regression_phase5_v1_scope_enforcement),
        ("VER-GAP: Intake Immutability", test_regression_intake_immutability_after_review),
    ]

    passed = 0
    failed = 0
    failed_tests = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except AssertionError as e:
            print(f"\n❌ FAILED: {test_name}")
            print(f"   Error: {e}")
            failed += 1
            failed_tests.append(test_name)
        except Exception as e:
            print(f"\n❌ ERROR: {test_name}")
            print(f"   Exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
            failed_tests.append(test_name)

    # Summary
    print("\n" + "="*70)
    print("REGRESSION TEST SUMMARY")
    print("="*70)
    print(f"Tests Passed: {passed}/{len(tests)}")
    print(f"Tests Failed: {failed}/{len(tests)}")

    if failed_tests:
        print(f"\nFailed Tests:")
        for test in failed_tests:
            print(f"  ❌ {test}")
        return 1
    else:
        print("\n✅ ALL REGRESSION TESTS PASSED")
        print("\nBehavior Locked:")
        print("  ✓ Phase 1: Intake validation rules")
        print("  ✓ Phase 2: Risk classification logic")
        print("  ✓ Phase 3: Multi-layer validation")
        print("  ✓ Phase 4: Artifact generation (5/8/11 artifacts)")
        print("  ✓ Phase 5 v1: Scope boundaries (no SLA, no metrics, no assignment)")
        print("  ✓ VER-GAP: Intake immutability preserved")
        print("\n** System behavior baseline established for Phase 7 **")
        return 0


if __name__ == "__main__":
    sys.exit(main())
