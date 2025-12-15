#!/usr/bin/env python3
"""
Test script for 6-Layer Validation System.
Tests each validation layer individually and the integrated system.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from models.intake import IntakeAnswers, RiskClassification
from validation.layer1 import validate_intake_answers, validate_project_name
from validation.layer2 import cross_validate
from validation.layer3 import detect_risk_indicators
from validation.layer4 import generate_confirmation_warnings, check_downgrade_attempt
from validation.layer5 import determine_expert_review
from validation.layer6 import validate_override_request, OverrideRequest


def test_layer2_cv1():
    """Test CV1: Automated + Low Reversibility + High Impact"""
    print("\n" + "="*60)
    print("TEST: Layer 2 - CV1 (Automated + Hard + Safety)")
    print("="*60)

    answers = IntakeAnswers(
        q1_users="External",
        q2_influence="Automated",  # Automated
        q3_worst_failure="Safety_Legal_Compliance",  # High impact
        q4_reversibility="Hard",  # Low reversibility
        q5_domain="Yes",
        q6_scale="Organization_Public",
        q7_regulated="Yes",
    )

    warnings = cross_validate(answers)
    cv1_warnings = [w for w in warnings if w.layer == "CV1"]

    assert len(cv1_warnings) == 1, "CV1 should trigger"
    assert cv1_warnings[0].severity == "CRITICAL", "CV1 should be CRITICAL"
    print(f"✅ CV1 triggered: {cv1_warnings[0].message}")


def test_layer2_cv2():
    """Test CV2: Informational + Hard to Reverse"""
    print("\n" + "="*60)
    print("TEST: Layer 2 - CV2 (Informational + Hard)")
    print("="*60)

    answers = IntakeAnswers(
        q1_users="Internal",
        q2_influence="Informational",  # Informational
        q3_worst_failure="Annoyance",
        q4_reversibility="Hard",  # Contradiction!
        q5_domain="Yes",
        q6_scale="Individual",
        q7_regulated="No",
    )

    warnings = cross_validate(answers)
    cv2_warnings = [w for w in warnings if w.layer == "CV2"]

    assert len(cv2_warnings) == 1, "CV2 should trigger"
    assert cv2_warnings[0].severity == "WARNING", "CV2 should be WARNING"
    print(f"✅ CV2 triggered: {cv2_warnings[0].message}")


def test_layer3_i1():
    """Test I1: Safety/Legal/Compliance Always Flagged"""
    print("\n" + "="*60)
    print("TEST: Layer 3 - I1 (Safety/Legal flag)")
    print("="*60)

    answers = IntakeAnswers(
        q1_users="Internal",
        q2_influence="Recommendations",
        q3_worst_failure="Safety_Legal_Compliance",  # Should trigger I1
        q4_reversibility="Easy",
        q5_domain="Yes",
        q6_scale="Individual",
        q7_regulated="No",
    )

    warnings = detect_risk_indicators(answers)
    i1_warnings = [w for w in warnings if w.layer == "I1"]

    assert len(i1_warnings) == 1, "I1 should always trigger for safety/legal"
    assert i1_warnings[0].severity == "CRITICAL", "I1 should be CRITICAL"
    print(f"✅ I1 triggered: {i1_warnings[0].message}")


def test_layer3_i4():
    """Test I4: Domain Uncertainty + High Stakes"""
    print("\n" + "="*60)
    print("TEST: Layer 3 - I4 (Unfamiliar domain + Safety)")
    print("="*60)

    answers = IntakeAnswers(
        q1_users="Internal",
        q2_influence="Recommendations",
        q3_worst_failure="Safety_Legal_Compliance",
        q4_reversibility="Easy",
        q5_domain="No",  # Unfamiliar domain
        q6_scale="Individual",
        q7_regulated="No",
    )

    warnings = detect_risk_indicators(answers)
    i4_warnings = [w for w in warnings if w.layer == "I4"]

    assert len(i4_warnings) == 1, "I4 should trigger"
    assert i4_warnings[0].severity == "CRITICAL", "I4 with 'No' should be CRITICAL"
    print(f"✅ I4 triggered: {i4_warnings[0].message}")


def test_layer4_w1():
    """Test W1: R3 Classification Confirmation"""
    print("\n" + "="*60)
    print("TEST: Layer 4 - W1 (R3 confirmation)")
    print("="*60)

    answers = IntakeAnswers(
        q1_users="External",
        q2_influence="Automated",
        q3_worst_failure="Safety_Legal_Compliance",
        q4_reversibility="Hard",
        q5_domain="Yes",
        q6_scale="Organization_Public",
        q7_regulated="Yes",
    )

    classification = RiskClassification(
        risk_level="R3",
        rigor="Maximum",
        rationale="R3 due to safety/legal",
        borderline=False,
    )

    warnings = generate_confirmation_warnings(answers, classification)
    w1_warnings = [w for w in warnings if w.layer == "W1"]

    assert len(w1_warnings) == 1, "W1 should trigger for R3"
    assert w1_warnings[0].severity == "CRITICAL", "W1 should be CRITICAL"
    print(f"✅ W1 triggered: {w1_warnings[0].message[:80]}...")


def test_layer4_w3():
    """Test W3: Downgrade Prevention"""
    print("\n" + "="*60)
    print("TEST: Layer 4 - W3 (Downgrade from R3 to R1)")
    print("="*60)

    warning = check_downgrade_attempt("R3", "R1")

    assert warning is not None, "W3 should trigger for downgrade"
    assert warning.severity == "CRITICAL", "Downgrade from R3 should be CRITICAL"
    assert "DEVIATION" in warning.message, "Should mention deviation requirement"
    print(f"✅ W3 triggered: {warning.message}")


def test_layer5_er1():
    """Test ER1: Multiple High-Risk Indicators"""
    print("\n" + "="*60)
    print("TEST: Layer 5 - ER1 (Multiple high-risk indicators)")
    print("="*60)

    from models.intake import ValidationWarning

    answers = IntakeAnswers(
        q1_users="External",
        q2_influence="Automated",
        q3_worst_failure="Safety_Legal_Compliance",
        q4_reversibility="Hard",
        q5_domain="No",
        q6_scale="Organization_Public",
        q7_regulated="Yes",
    )

    classification = RiskClassification(
        risk_level="R3",
        rigor="Maximum",
        rationale="R3",
        borderline=False,
    )

    # Simulate multiple CRITICAL warnings
    warnings = [
        ValidationWarning(severity="CRITICAL", layer="CV1", message="Test 1", recommendation=""),
        ValidationWarning(severity="CRITICAL", layer="I1", message="Test 2", recommendation=""),
    ]

    required, recommended, reasons = determine_expert_review(
        answers, classification, warnings
    )

    assert required, "ER1 should require expert review for 2+ CRITICAL warnings"
    print(f"✅ ER1 triggered - Expert review REQUIRED")
    print(f"   Reasons: {reasons}")


def test_layer6_override_validation():
    """Test Layer 6: Override Validation"""
    print("\n" + "="*60)
    print("TEST: Layer 6 - Override Validation")
    print("="*60)

    # Test 1: Valid expert override
    expert_override = OverrideRequest(
        calculated_risk="R2",
        requested_risk="R3",
        override_type="expert",
        justification="System provides guidance for safety-critical projects. Incorrect guidance could indirectly cause harm.",
        requested_by="Quality Expert",
        approved_by="Project Owner",
    )

    result = validate_override_request(expert_override)
    assert result.valid, "Expert override should be valid"
    print(f"✅ Expert override (R2→R3): VALID")

    # Test 2: Invalid self-downgrade (missing details)
    try:
        # This should fail Pydantic validation due to short justification
        invalid_downgrade = OverrideRequest(
            calculated_risk="R3",
            requested_risk="R1",
            override_type="self",
            justification="I think R1 is fine",  # Too short (< 50 chars)
            requested_by="User",
        )
        assert False, "Should have raised validation error"
    except Exception as e:
        # Pydantic catches this before our validation
        assert "at least 50 characters" in str(e), "Should enforce min length"
        print(f"✅ Invalid self-downgrade (short justification): REJECTED by Pydantic")

    # Test 3: Invalid self-downgrade (long enough but missing details)
    invalid_downgrade2 = OverrideRequest(
        calculated_risk="R3",
        requested_risk="R1",
        override_type="self",
        justification="I think R1 is fine because this project is not that critical really",
        requested_by="User",
    )

    result = validate_override_request(invalid_downgrade2)
    assert not result.valid, "Self-downgrade without question adjustments should be invalid"
    assert len(result.errors) > 0, "Should have validation errors"
    print(f"✅ Invalid self-downgrade (insufficient details): REJECTED")
    print(f"   Errors: {result.errors}")


def test_integrated_system():
    """Test Integrated 6-Layer System"""
    print("\n" + "="*60)
    print("TEST: Integrated 6-Layer System")
    print("="*60)

    # Scenario: Medical recommendation system (high-risk)
    answers = IntakeAnswers(
        q1_users="External",
        q2_influence="Recommendations",
        q3_worst_failure="Safety_Legal_Compliance",
        q4_reversibility="Partial",
        q5_domain="Partially",
        q6_scale="Multi_team",
        q7_regulated="Yes",
    )

    # Layer 1
    layer1_warnings = validate_intake_answers(answers)
    print(f"Layer 1: {len(layer1_warnings)} warnings")

    # Layer 2
    layer2_warnings = cross_validate(answers)
    print(f"Layer 2: {len(layer2_warnings)} warnings")

    # Layer 3
    layer3_warnings = detect_risk_indicators(answers)
    print(f"Layer 3: {len(layer3_warnings)} warnings")

    # Classification
    from validation.classifier import classify_risk

    classification, classification_warnings = classify_risk(answers)
    print(f"Classification: {classification.risk_level} ({classification.rigor})")

    # Layer 4
    layer4_warnings = generate_confirmation_warnings(answers, classification)
    print(f"Layer 4: {len(layer4_warnings)} warnings")

    # Layer 5
    all_warnings = (
        layer1_warnings
        + layer2_warnings
        + layer3_warnings
        + classification_warnings
        + layer4_warnings
    )
    required, recommended, reasons = determine_expert_review(
        answers, classification, all_warnings
    )
    print(f"Layer 5: Expert review - Required: {required}, Recommended: {recommended}")

    # Summary
    total_warnings = len(all_warnings)
    critical_count = sum(1 for w in all_warnings if w.severity == "CRITICAL")
    warning_count = sum(1 for w in all_warnings if w.severity == "WARNING")

    print(f"\n✅ Integrated System Test Complete")
    print(f"   Total warnings: {total_warnings}")
    print(f"   CRITICAL: {critical_count}")
    print(f"   WARNING: {warning_count}")
    print(f"   Expert review: {'REQUIRED' if required else 'Recommended' if recommended else 'Optional'}")


def main():
    """Run all validation layer tests."""
    print("QMS Dashboard - 6-Layer Validation System Tests")
    print("="*60)

    tests = [
        ("Layer 2 - CV1", test_layer2_cv1),
        ("Layer 2 - CV2", test_layer2_cv2),
        ("Layer 3 - I1", test_layer3_i1),
        ("Layer 3 - I4", test_layer3_i4),
        ("Layer 4 - W1", test_layer4_w1),
        ("Layer 4 - W3", test_layer4_w3),
        ("Layer 5 - ER1", test_layer5_er1),
        ("Layer 6 - Override", test_layer6_override_validation),
        ("Integrated System", test_integrated_system),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ FAILED: {test_name}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ ERROR: {test_name}")
            print(f"   Exception: {e}")
            failed += 1

    # Summary
    print("\n" + "="*60)
    print(f"TEST SUMMARY")
    print("="*60)
    print(f"Tests Passed: {passed}/{len(tests)}")
    print(f"Tests Failed: {failed}/{len(tests)}")
    print(f"Success Rate: {(passed/len(tests))*100:.1f}%")

    if passed == len(tests):
        print("\n✅ All validation layer tests passed!")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
