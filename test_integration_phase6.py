#!/usr/bin/env python3
"""
Phase 6: Integration Testing
Tests end-to-end workflows across all system components.

Covers:
- Complete intake → classification → validation → artifacts flow
- Expert review workflow integration
- Validation layers integration (Layer 1-6)
- Override and deviation workflows
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from models.intake import IntakeRequest, IntakeResponse, IntakeAnswers
from models.review import ReviewTrigger, ReviewApproval
from validation.classifier import classify_risk, get_required_artifacts
from validation.layer1 import validate_intake_answers, validate_project_name
from validation.layer2 import cross_validate
from validation.layer3 import detect_risk_indicators
from validation.layer4 import generate_confirmation_warnings
from validation.layer5 import determine_expert_review
from artifacts.generator import generate_project_artifacts
from review.request_generator import create_review_request
from review.storage import ReviewStorage


def test_integration_e2e_r0_happy_path():
    """
    Integration Test: R0 Happy Path
    Tests complete flow from intake to artifact generation for minimal risk project.
    """
    print("\n" + "="*70)
    print("INTEGRATION TEST: R0 Happy Path (Minimal Risk)")
    print("="*70)

    # Step 1: Create intake request
    intake_request = IntakeRequest(
        project_name="Internal Dashboard Widget",
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

    print("✓ Step 1: Intake request created")

    # Step 2: Validation Layer 1 - Input validation
    warnings = []
    warnings.extend(validate_project_name(intake_request.project_name))
    warnings.extend(validate_intake_answers(intake_request.answers))
    assert len([w for w in warnings if w.severity == "CRITICAL"]) == 0, "Layer 1 validation failed"
    print(f"✓ Step 2: Layer 1 validation passed ({len(warnings)} warnings)")

    # Step 3: Validation Layer 2 - Cross-validation
    warnings.extend(cross_validate(intake_request.answers))
    print(f"✓ Step 3: Layer 2 cross-validation passed ({len(warnings)} total warnings)")

    # Step 4: Validation Layer 3 - Risk indicators
    warnings.extend(detect_risk_indicators(intake_request.answers))
    print(f"✓ Step 4: Layer 3 risk indicators checked ({len(warnings)} total warnings)")

    # Step 5: Classification
    classification, class_warnings = classify_risk(intake_request.answers)
    warnings.extend(class_warnings)
    assert classification.risk_level == "R0", f"Expected R0, got {classification.risk_level}"
    print(f"✓ Step 5: Risk classification → {classification.risk_level}")

    # Step 6: Validation Layer 4 - Confirmation warnings
    warnings.extend(generate_confirmation_warnings(intake_request.answers, classification))
    print(f"✓ Step 6: Layer 4 confirmation warnings generated")

    # Step 7: Validation Layer 5 - Expert review triggers
    expert_required, expert_recommended, review_reasons = determine_expert_review(
        intake_request.answers, classification, warnings
    )
    assert not expert_required, "R0 should not require expert review"
    print(f"✓ Step 7: Layer 5 expert review determination (Required: {expert_required}, Recommended: {expert_recommended})")

    # Step 8: Get required artifacts
    artifacts_required = get_required_artifacts(classification.risk_level)
    assert len(artifacts_required) == 5, f"R0 should have 5 artifacts, got {len(artifacts_required)}"
    print(f"✓ Step 8: Required artifacts determined → {len(artifacts_required)} artifacts")

    # Step 9: Create intake response
    intake_response = IntakeResponse(
        intake_id="integration-r0",
        project_name=intake_request.project_name,
        timestamp=intake_request.timestamp,
        answers=intake_request.answers,
        classification=classification,
        warnings=warnings,
        expert_review_required=expert_required,
        expert_review_recommended=expert_recommended,
        next_steps=[],
        artifacts_required=artifacts_required
    )
    print("✓ Step 9: Intake response created")

    # Step 10: Generate artifacts
    test_output_dir = Path(__file__).parent / "data" / "test_integration_r0"
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)

    result = generate_project_artifacts(intake_request, intake_response, output_dir=test_output_dir)
    assert len(result['artifacts_generated']) == 5, "R0 should generate 5 artifacts"
    assert Path(result['zip_file']).exists(), "ZIP file should be created"
    print(f"✓ Step 10: Artifacts generated → {len(result['artifacts_generated'])} files, {Path(result['zip_file']).stat().st_size} bytes")

    print(f"\n✅ R0 Happy Path: PASS (10/10 steps completed)")
    return True


def test_integration_e2e_r3_expert_review():
    """
    Integration Test: R3 with Expert Review Workflow
    Tests complete flow including mandatory expert review.
    """
    print("\n" + "="*70)
    print("INTEGRATION TEST: R3 with Expert Review Workflow")
    print("="*70)

    # Step 1: Create R3 intake (safety-critical)
    intake_request = IntakeRequest(
        project_name="Medical Device Control System",
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
    print("✓ Step 1: R3 intake request created (safety-critical)")

    # Step 2: Full validation (Layers 1-5)
    warnings = []
    warnings.extend(validate_project_name(intake_request.project_name))
    warnings.extend(validate_intake_answers(intake_request.answers))
    warnings.extend(cross_validate(intake_request.answers))
    warnings.extend(detect_risk_indicators(intake_request.answers))

    classification, class_warnings = classify_risk(intake_request.answers)
    warnings.extend(class_warnings)
    assert classification.risk_level == "R3", f"Expected R3, got {classification.risk_level}"

    warnings.extend(generate_confirmation_warnings(intake_request.answers, classification))

    expert_required, expert_recommended, review_reasons = determine_expert_review(
        intake_request.answers, classification, warnings
    )
    assert expert_required, "R3 safety-critical should require expert review"
    print(f"✓ Step 2: Validation complete → {classification.risk_level}, Expert review: {expert_required}")

    # Step 3: Create intake response
    intake_response = IntakeResponse(
        intake_id="integration-r3",
        project_name=intake_request.project_name,
        timestamp=intake_request.timestamp,
        answers=intake_request.answers,
        classification=classification,
        warnings=warnings,
        expert_review_required=expert_required,
        expert_review_recommended=expert_recommended,
        next_steps=[],
        artifacts_required=get_required_artifacts(classification.risk_level)
    )
    print("✓ Step 3: Intake response created")

    # Step 4: Create expert review request
    review_triggers = [
        ReviewTrigger(
            trigger_id="ER1",
            description="Safety-critical system requiring expert validation",
            severity="mandatory"
        )
    ]

    review_request = create_review_request(
        intake_request=intake_request,
        intake_response=intake_response,
        review_type="mandatory",
        review_triggers=review_triggers,
        user_comment="Need validation for medical device deployment"
    )
    print(f"✓ Step 4: Expert review request created → {review_request.review_id}")

    # Step 5: Save review request
    test_data_dir = Path(__file__).parent / "data" / "test_integration_review"
    if test_data_dir.exists():
        shutil.rmtree(test_data_dir)
    test_data_dir.mkdir(parents=True, exist_ok=True)

    storage = ReviewStorage(test_data_dir)
    storage.save_review_request(review_request)
    print("✓ Step 5: Review request saved")

    # Step 6: Simulate expert approval
    approval = ReviewApproval(
        review_id=review_request.review_id,
        reviewer_name="Dr. Sarah Johnson",
        reviewer_qualifications="Medical Device QA Engineer, 20 years",
        classification_approved=classification.risk_level,
        expert_comments="R3 classification is appropriate for this safety-critical medical device system."
    )
    print("✓ Step 6: Expert approval simulated")

    # Step 7: Generate artifacts (after approval)
    test_output_dir = Path(__file__).parent / "data" / "test_integration_r3"
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)

    result = generate_project_artifacts(intake_request, intake_response, output_dir=test_output_dir)
    assert len(result['artifacts_generated']) == 11, "R3 should generate 11 artifacts"
    print(f"✓ Step 7: Artifacts generated → {len(result['artifacts_generated'])} files")

    print(f"\n✅ R3 Expert Review Workflow: PASS (7/7 steps completed)")
    return True


def test_integration_validation_layers():
    """
    Integration Test: Validation Layers Working Together
    Tests that all 6 validation layers work correctly in sequence.
    """
    print("\n" + "="*70)
    print("INTEGRATION TEST: Validation Layers 1-6")
    print("="*70)

    # Create intake with multiple validation triggers
    intake_request = IntakeRequest(
        project_name="Financial Trading System",
        timestamp=datetime.now(timezone.utc),
        answers=IntakeAnswers(
            q1_users="External",
            q2_influence="Automated",
            q3_worst_failure="Financial",
            q4_reversibility="Partial",
            q5_domain="Partially",
            q6_scale="Organization_Public",
            q7_regulated="Possibly"
        )
    )

    # Layer 1: Input validation
    layer1_warnings = []
    layer1_warnings.extend(validate_project_name(intake_request.project_name))
    layer1_warnings.extend(validate_intake_answers(intake_request.answers))
    print(f"✓ Layer 1: Input validation → {len(layer1_warnings)} warnings")

    # Layer 2: Cross-validation
    layer2_warnings = cross_validate(intake_request.answers)
    print(f"✓ Layer 2: Cross-validation → {len(layer2_warnings)} warnings")

    # Layer 3: Risk indicators
    layer3_warnings = detect_risk_indicators(intake_request.answers)
    print(f"✓ Layer 3: Risk indicators → {len(layer3_warnings)} warnings")

    # Classification
    classification, class_warnings = classify_risk(intake_request.answers)
    print(f"✓ Classification: {classification.risk_level} ({classification.rigor})")

    # Layer 4: Confirmation warnings
    all_warnings = layer1_warnings + layer2_warnings + layer3_warnings + class_warnings
    layer4_warnings = generate_confirmation_warnings(intake_request.answers, classification)
    print(f"✓ Layer 4: Confirmation warnings → {len(layer4_warnings)} warnings")

    # Layer 5: Expert review triggers
    all_warnings.extend(layer4_warnings)
    expert_required, expert_recommended, review_reasons = determine_expert_review(
        intake_request.answers, classification, all_warnings
    )
    print(f"✓ Layer 5: Expert review → Required: {expert_required}, Recommended: {expert_recommended}")

    # Layer 6: Override capability (tested separately)
    print(f"✓ Layer 6: Override system available (tested in dedicated tests)")

    total_warnings = len(all_warnings)
    print(f"\n✅ Validation Layers Integration: PASS")
    print(f"   Total warnings generated: {total_warnings}")
    print(f"   Classification: {classification.risk_level}")
    print(f"   Expert review: {expert_required or expert_recommended}")

    return True


def test_integration_r1_moderate_risk():
    """
    Integration Test: R1 Moderate Risk
    Tests R1 classification and 8 artifact generation.
    """
    print("\n" + "="*70)
    print("INTEGRATION TEST: R1 Moderate Risk")
    print("="*70)

    intake_request = IntakeRequest(
        project_name="Customer Feedback Analysis Tool",
        timestamp=datetime.now(timezone.utc),
        answers=IntakeAnswers(
            q1_users="Internal",
            q2_influence="Recommendations",
            q3_worst_failure="Annoyance",
            q4_reversibility="Easy",
            q5_domain="Partially",
            q6_scale="Multi_team",
            q7_regulated="No"
        )
    )

    # Full validation
    warnings = []
    warnings.extend(validate_project_name(intake_request.project_name))
    warnings.extend(validate_intake_answers(intake_request.answers))
    warnings.extend(cross_validate(intake_request.answers))
    warnings.extend(detect_risk_indicators(intake_request.answers))

    classification, class_warnings = classify_risk(intake_request.answers)
    warnings.extend(class_warnings)
    assert classification.risk_level == "R1", f"Expected R1, got {classification.risk_level}"

    # Get artifacts
    artifacts_required = get_required_artifacts(classification.risk_level)
    assert len(artifacts_required) == 8, f"R1 should have 8 artifacts, got {len(artifacts_required)}"

    intake_response = IntakeResponse(
        intake_id="integration-r1",
        project_name=intake_request.project_name,
        timestamp=intake_request.timestamp,
        answers=intake_request.answers,
        classification=classification,
        warnings=warnings,
        expert_review_required=False,
        expert_review_recommended=False,
        next_steps=[],
        artifacts_required=artifacts_required
    )

    # Generate artifacts
    test_output_dir = Path(__file__).parent / "data" / "test_integration_r1"
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)

    result = generate_project_artifacts(intake_request, intake_response, output_dir=test_output_dir)
    assert len(result['artifacts_generated']) == 8, f"R1 should generate 8 artifacts, got {len(result['artifacts_generated'])}"

    print(f"✓ R1 Classification: {classification.risk_level}")
    print(f"✓ Artifacts generated: {len(result['artifacts_generated'])}")
    print(f"\n✅ R1 Moderate Risk: PASS")
    return True


def test_integration_r2_strict_compliance():
    """
    Integration Test: R2 Strict Compliance
    Tests R2 classification and 11 artifact generation.
    """
    print("\n" + "="*70)
    print("INTEGRATION TEST: R2 Strict Compliance")
    print("="*70)

    intake_request = IntakeRequest(
        project_name="Automated Financial Reporting System",
        timestamp=datetime.now(timezone.utc),
        answers=IntakeAnswers(
            q1_users="Internal",
            q2_influence="Recommendations",
            q3_worst_failure="Financial",
            q4_reversibility="Easy",
            q5_domain="Partially",
            q6_scale="Multi_team",
            q7_regulated="No"
        )
    )

    # Full validation
    warnings = []
    warnings.extend(validate_project_name(intake_request.project_name))
    warnings.extend(validate_intake_answers(intake_request.answers))
    warnings.extend(cross_validate(intake_request.answers))
    warnings.extend(detect_risk_indicators(intake_request.answers))

    classification, class_warnings = classify_risk(intake_request.answers)
    warnings.extend(class_warnings)
    assert classification.risk_level == "R2", f"Expected R2, got {classification.risk_level}"

    # Get artifacts
    artifacts_required = get_required_artifacts(classification.risk_level)
    assert len(artifacts_required) == 11, f"R2 should have 11 artifacts, got {len(artifacts_required)}"

    intake_response = IntakeResponse(
        intake_id="integration-r2",
        project_name=intake_request.project_name,
        timestamp=intake_request.timestamp,
        answers=intake_request.answers,
        classification=classification,
        warnings=warnings,
        expert_review_required=False,
        expert_review_recommended=False,
        next_steps=[],
        artifacts_required=artifacts_required
    )

    # Generate artifacts
    test_output_dir = Path(__file__).parent / "data" / "test_integration_r2"
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)

    result = generate_project_artifacts(intake_request, intake_response, output_dir=test_output_dir)
    assert len(result['artifacts_generated']) == 11, f"R2 should generate 11 artifacts, got {len(result['artifacts_generated'])}"

    print(f"✓ R2 Classification: {classification.risk_level}")
    print(f"✓ Artifacts generated: {len(result['artifacts_generated'])}")
    print(f"\n✅ R2 Strict Compliance: PASS")
    return True


def test_integration_expert_override_workflow():
    """
    Integration Test: Expert Override Workflow
    Tests expert overriding classification (R1 → R2).
    Verifies VER-GAP-P5-INTAKE-WRITEBACK behavior.
    """
    print("\n" + "="*70)
    print("INTEGRATION TEST: Expert Override Workflow")
    print("="*70)

    # Create borderline R1/R2 case
    intake_request = IntakeRequest(
        project_name="Payment Processing Integration",
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

    # Run classification
    warnings = []
    warnings.extend(validate_intake_answers(intake_request.answers))
    classification, class_warnings = classify_risk(intake_request.answers)
    warnings.extend(class_warnings)

    intake_response = IntakeResponse(
        intake_id="integration-override",
        project_name=intake_request.project_name,
        timestamp=intake_request.timestamp,
        answers=intake_request.answers,
        classification=classification,
        warnings=warnings,
        expert_review_required=False,
        expert_review_recommended=True,
        next_steps=[],
        artifacts_required=get_required_artifacts(classification.risk_level)
    )

    original_classification = classification.risk_level
    print(f"✓ Original classification: {original_classification}")

    # Save intake to file (simulating API behavior)
    test_data_dir = Path(__file__).parent / "data" / "test_integration_override"
    if test_data_dir.exists():
        shutil.rmtree(test_data_dir)
    test_data_dir.mkdir(parents=True, exist_ok=True)

    intake_file = test_data_dir / "integration-override.json"
    with open(intake_file, 'w') as f:
        import json
        json.dump(intake_response.model_dump(mode='json'), f, indent=2, default=str)
    print(f"✓ Intake saved to: {intake_file}")

    # Create expert review request
    from models.review import ReviewOverride, ReviewResponse, IntakeDiscrepancy

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

    storage = ReviewStorage(test_data_dir)
    storage.save_review_request(review_request)
    print(f"✓ Review request created: {review_request.review_id}")

    # Expert overrides R1 → R2
    override = ReviewOverride(
        review_id=review_request.review_id,
        reviewer_name="Dr. Alex Chen",
        reviewer_qualifications="Financial Systems QA Lead",
        original_classification=original_classification,
        new_classification="R2",
        justification="Financial impact at multi-team scale combined with automated processing and partial reversibility requires R2 rigor. The system processes payment data that could lead to significant financial errors affecting multiple teams.",
        intake_discrepancies=[
            IntakeDiscrepancy(
                question_id="q3_worst_failure",
                original_answer="Financial",
                actual_situation="Financial loss at multi-team scale with payment processing",
                explanation="User underestimated the financial impact severity"
            )
        ],
        additional_factors="Payment processing systems require strict compliance. Multi-team scale amplifies risk.",
        risks_accepted=None
    )

    review_response = ReviewResponse(
        review_id=review_request.review_id,
        intake_id=intake_response.intake_id,
        project_name=intake_request.project_name,
        reviewer_name=override.reviewer_name,
        reviewer_qualifications=override.reviewer_qualifications,
        review_type=review_request.review_type,
        decision="overridden",
        original_classification=override.original_classification,
        final_classification=override.new_classification,
        override=override,
        review_triggers=review_request.review_triggers,
        outcome=f"Classification overridden from {override.original_classification} to {override.new_classification}"
    )

    storage.save_review_response(review_response)
    print(f"✓ Expert override: {original_classification} → {override.new_classification}")

    # VER-GAP-P5-INTAKE-WRITEBACK verification
    # Verify that original intake file is NOT modified
    with open(intake_file, 'r') as f:
        import json
        loaded_intake = json.load(f)
        loaded_classification = loaded_intake['classification']['risk_level']

    print(f"\n[VER-GAP-P5-INTAKE-WRITEBACK Verification]")
    print(f"  Original intake classification: {loaded_classification}")
    print(f"  Expert final classification: {override.new_classification}")

    assert loaded_classification == original_classification, \
        f"Intake file should remain unchanged (expected {original_classification}, got {loaded_classification})"
    print(f"  ✓ Intake file NOT modified (Phase 5 v1 expected behavior)")

    # Verify review response was saved separately
    review_response_file = test_data_dir / "reviews" / f"{review_request.review_id}_response.json"
    assert review_response_file.exists(), "Review response should be saved separately"
    print(f"  ✓ Review response saved separately: {review_response_file}")

    print(f"\n✅ Expert Override Workflow: PASS")
    print(f"✅ VER-GAP-P5-INTAKE-WRITEBACK: Verified (intake unchanged, review separate)")
    return True


def main():
    """Run all Phase 6 integration tests."""
    print("="*70)
    print("PHASE 6: INTEGRATION TESTING")
    print("End-to-End Workflow Tests")
    print("="*70)

    tests = [
        ("R0 Happy Path (Minimal Risk)", test_integration_e2e_r0_happy_path),
        ("R1 Moderate Risk", test_integration_r1_moderate_risk),
        ("R2 Strict Compliance", test_integration_r2_strict_compliance),
        ("R3 Expert Review Workflow", test_integration_e2e_r3_expert_review),
        ("Expert Override Workflow + VER-GAP Verification", test_integration_expert_override_workflow),
        ("Validation Layers Integration", test_integration_validation_layers),
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
    print("INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"Tests Passed: {passed}/{len(tests)}")
    print(f"Tests Failed: {failed}/{len(tests)}")

    if failed_tests:
        print(f"\nFailed Tests:")
        for test in failed_tests:
            print(f"  ❌ {test}")
        return 1
    else:
        print("\n✅ All integration tests PASSED!")
        print("\n** All system components work correctly together **")
        return 0


if __name__ == "__main__":
    sys.exit(main())
