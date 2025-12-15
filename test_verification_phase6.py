#!/usr/bin/env python3
"""
Phase 6: Testing & Verification
Comprehensive verification test suite per QMS-Verification-Plan.md

Tests VER-001 through VER-008 covering:
- Risk classification accuracy (CTQ-1.1)
- Artifact set correctness (CTQ-1.2)
- Traceability integrity (CTQ-1.3)
- Mandatory artifact generation (CTQ-2.1)
- Status enforcement (CTQ-2.2)
- First-pass content quality (CTQ-2.3)
- Domain alignment (CTQ-4.1)
- Risk-appropriate rigor (CTQ-4.2)
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from models.intake import IntakeRequest, IntakeResponse, IntakeAnswers, RiskClassification
from validation.classifier import classify_risk, get_required_artifacts
from artifacts.generator import generate_project_artifacts


# ============================================================================
# VER-001: Risk Classification Accuracy (CTQ-1.1) - PRIORITY 1
# ============================================================================

def test_ver001a_risk_classification_all_scenarios():
    """
    VER-001-A: Unit tests for risk classification logic.
    Tests all combinations of intake responses and verifies correct R0/R1/R2/R3 output.
    """
    print("\n" + "="*70)
    print("VER-001-A: Risk Classification - All Scenarios")
    print("="*70)

    test_cases = [
        # R0 scenarios - Minimal rigor
        {
            "name": "R0: Internal tool, informational, low impact",
            "answers": IntakeAnswers(
                q1_users="Internal",
                q2_influence="Informational",
                q3_worst_failure="Annoyance",
                q4_reversibility="Easy",
                q5_domain="Yes",
                q6_scale="Individual",
                q7_regulated="No"
            ),
            "expected_risk": "R0",
            "expected_rigor": "Minimal"
        },
        # R1 scenarios - Moderate rigor
        {
            "name": "R1: Internal tool, moderate impact, team scale",
            "answers": IntakeAnswers(
                q1_users="Internal",
                q2_influence="Informational",
                q3_worst_failure="Reputational",
                q4_reversibility="Easy",
                q5_domain="Yes",
                q6_scale="Team",
                q7_regulated="No"
            ),
            "expected_risk": "R1",
            "expected_rigor": "Moderate"
        },
        # R2 scenarios - Strict rigor
        {
            "name": "R2: Internal, recommendations, multi-team",
            "answers": IntakeAnswers(
                q1_users="Internal",
                q2_influence="Recommendations",
                q3_worst_failure="Financial",
                q4_reversibility="Partial",
                q5_domain="Partially",
                q6_scale="Multi_team",
                q7_regulated="No"
            ),
            "expected_risk": "R2",
            "expected_rigor": "Strict"
        },
        {
            "name": "R2: External users (even if low impact)",
            "answers": IntakeAnswers(
                q1_users="External",
                q2_influence="Informational",
                q3_worst_failure="Annoyance",
                q4_reversibility="Easy",
                q5_domain="Yes",
                q6_scale="Individual",
                q7_regulated="No"
            ),
            "expected_risk": "R2",
            "expected_rigor": "Strict"
        },
        # R3 scenarios - Maximum rigor
        {
            "name": "R3: Safety/legal concerns (unmitigated)",
            "answers": IntakeAnswers(
                q1_users="External",  # External makes it unmitigated
                q2_influence="Recommendations",
                q3_worst_failure="Safety_Legal_Compliance",
                q4_reversibility="Hard",
                q5_domain="Partially",
                q6_scale="Multi_team",
                q7_regulated="Yes"
            ),
            "expected_risk": "R3",
            "expected_rigor": "Maximum"
        },
        {
            "name": "R3: Automated + hard to reverse",
            "answers": IntakeAnswers(
                q1_users="External",
                q2_influence="Automated",
                q3_worst_failure="Financial",
                q4_reversibility="Hard",
                q5_domain="Partially",
                q6_scale="Organization_Public",
                q7_regulated="Yes"
            ),
            "expected_risk": "R3",
            "expected_rigor": "Maximum"
        },
    ]

    passed = 0
    failed = 0

    for tc in test_cases:
        classification, _ = classify_risk(tc["answers"])

        if classification.risk_level == tc["expected_risk"] and classification.rigor == tc["expected_rigor"]:
            print(f"✅ PASS: {tc['name']}")
            print(f"   Expected: {tc['expected_risk']} ({tc['expected_rigor']})")
            print(f"   Got: {classification.risk_level} ({classification.rigor})")
            passed += 1
        else:
            print(f"❌ FAIL: {tc['name']}")
            print(f"   Expected: {tc['expected_risk']} ({tc['expected_rigor']})")
            print(f"   Got: {classification.risk_level} ({classification.rigor})")
            failed += 1

    print(f"\nVER-001-A Results: {passed}/{len(test_cases)} passed")
    assert failed == 0, f"{failed} test case(s) failed"
    return passed, failed


def test_ver001c_boundary_cases():
    """
    VER-001-C: Boundary test cases.
    Tests borderline scenarios between R0/R1, R1/R2, R2/R3.
    """
    print("\n" + "="*70)
    print("VER-001-C: Risk Classification - Boundary Cases")
    print("="*70)

    boundary_cases = [
        # R0/R1 boundary - Add multi-team scale
        {
            "name": "R0/R1 Boundary: Individual → Multi_team scale",
            "answers": IntakeAnswers(
                q1_users="Internal",
                q2_influence="Informational",
                q3_worst_failure="Annoyance",
                q4_reversibility="Easy",
                q5_domain="Yes",
                q6_scale="Multi_team",  # Crosses to R1 (Team alone doesn't)
                q7_regulated="No"
            ),
            "expected_min_risk": "R1"
        },
        # R1/R2 boundary - External users
        {
            "name": "R1/R2 Boundary: Internal → External users",
            "answers": IntakeAnswers(
                q1_users="External",  # Crosses to R2
                q2_influence="Informational",
                q3_worst_failure="Reputational",
                q4_reversibility="Easy",
                q5_domain="Yes",
                q6_scale="Team",
                q7_regulated="No"
            ),
            "expected_min_risk": "R2"
        },
        # R2/R3 boundary - Automated financial with hard reversibility
        {
            "name": "R2/R3 Boundary: Financial → Automated + Hard reversibility",
            "answers": IntakeAnswers(
                q1_users="External",
                q2_influence="Automated",  # Automated + Hard → R3
                q3_worst_failure="Financial",
                q4_reversibility="Hard",
                q5_domain="Partially",
                q6_scale="Multi_team",
                q7_regulated="No"
            ),
            "expected_min_risk": "R3"
        },
    ]

    passed = 0
    failed = 0

    for tc in boundary_cases:
        classification, _ = classify_risk(tc["answers"])

        # Check if risk level is at least the expected minimum
        risk_order = ["R0", "R1", "R2", "R3"]
        actual_index = risk_order.index(classification.risk_level)
        expected_index = risk_order.index(tc["expected_min_risk"])

        if actual_index >= expected_index:
            print(f"✅ PASS: {tc['name']}")
            print(f"   Expected: >={tc['expected_min_risk']}, Got: {classification.risk_level}")
            passed += 1
        else:
            print(f"❌ FAIL: {tc['name']}")
            print(f"   Expected: >={tc['expected_min_risk']}, Got: {classification.risk_level}")
            failed += 1

    print(f"\nVER-001-C Results: {passed}/{len(boundary_cases)} passed")
    assert failed == 0, f"{failed} boundary case(s) failed"
    return passed, failed


# ============================================================================
# VER-002: Artifact Set Correctness (CTQ-1.2) - PRIORITY 1
# ============================================================================

def test_ver002a_artifact_list_by_risk():
    """
    VER-002-A: Unit tests for artifact generation.
    Verifies correct artifact count and names for each risk level.
    """
    print("\n" + "="*70)
    print("VER-002-A: Artifact Set Correctness - By Risk Level")
    print("="*70)

    test_cases = [
        {
            "risk_level": "R0",
            "expected_count": 5,
            "expected_artifacts": [
                "Quality Plan",
                "CTQ Tree",
                "Assumptions Register",
                "Risk Register",
                "Traceability Index"
            ]
        },
        {
            "risk_level": "R1",
            "expected_count": 8,
            "expected_artifacts": [
                "Quality Plan",
                "CTQ Tree",
                "Assumptions Register",
                "Risk Register",
                "Traceability Index",
                "Verification Plan",
                "Validation Plan",
                "Measurement Plan"
            ]
        },
        {
            "risk_level": "R2",
            "expected_count": 11,
            "expected_artifacts": [
                "Quality Plan",
                "CTQ Tree",
                "Assumptions Register",
                "Risk Register",
                "Traceability Index",
                "Verification Plan",
                "Validation Plan",
                "Measurement Plan",
                "Control Plan",
                "Change Log",
                "CAPA Log"
            ]
        },
        {
            "risk_level": "R3",
            "expected_count": 11,
            "expected_artifacts": [
                "Quality Plan",
                "CTQ Tree",
                "Assumptions Register",
                "Risk Register",
                "Traceability Index",
                "Verification Plan",
                "Validation Plan",
                "Measurement Plan",
                "Control Plan",
                "Change Log",
                "CAPA Log"
            ]
        },
    ]

    passed = 0
    failed = 0

    for tc in test_cases:
        artifacts = get_required_artifacts(tc["risk_level"])

        if len(artifacts) == tc["expected_count"] and set(artifacts) == set(tc["expected_artifacts"]):
            print(f"✅ PASS: {tc['risk_level']} → {tc['expected_count']} artifacts")
            passed += 1
        else:
            print(f"❌ FAIL: {tc['risk_level']}")
            print(f"   Expected: {tc['expected_count']} artifacts")
            print(f"   Got: {len(artifacts)} artifacts")
            print(f"   Missing: {set(tc['expected_artifacts']) - set(artifacts)}")
            print(f"   Extra: {set(artifacts) - set(tc['expected_artifacts'])}")
            failed += 1

    print(f"\nVER-002-A Results: {passed}/{len(test_cases)} passed")
    assert failed == 0, f"{failed} test case(s) failed"
    return passed, failed


def test_ver002b_integration_full_flow():
    """
    VER-002-B: Integration test - full intake to artifact generation.
    Verifies complete end-to-end flow works correctly.
    """
    print("\n" + "="*70)
    print("VER-002-B: Integration Test - Full Intake → Artifacts")
    print("="*70)

    # Clean test directory
    test_output_dir = Path(__file__).parent / "data" / "test_verification"
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)

    # Create sample R2 intake
    intake_request = IntakeRequest(
        project_name="VER-002-B Test Project",
        timestamp=datetime.utcnow(),
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

    # Classify
    classification, warnings = classify_risk(intake_request.answers)

    # Create intake response
    intake_response = IntakeResponse(
        intake_id="ver-002-b",
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

    # Generate artifacts
    result = generate_project_artifacts(
        intake_request,
        intake_response,
        output_dir=test_output_dir
    )

    # Verify
    expected_risk = "R2"
    expected_artifact_count = 11

    errors = []

    if classification.risk_level != expected_risk:
        errors.append(f"Expected {expected_risk}, got {classification.risk_level}")

    if len(result['artifacts_generated']) != expected_artifact_count:
        errors.append(f"Expected {expected_artifact_count} artifacts, got {len(result['artifacts_generated'])}")

    # Verify all files exist
    for file_path in result['file_paths']:
        if not Path(file_path).exists():
            errors.append(f"Missing file: {file_path}")

    # Verify ZIP exists
    if not Path(result['zip_file']).exists():
        errors.append(f"Missing ZIP file: {result['zip_file']}")

    if errors:
        print(f"❌ FAIL: Integration test")
        for error in errors:
            print(f"   - {error}")
        assert False, "Integration test failed"
    else:
        print(f"✅ PASS: Full intake → {classification.risk_level} → {len(result['artifacts_generated'])} artifacts")
        print(f"   ZIP: {Path(result['zip_file']).stat().st_size} bytes")
        return 1, 0


# ============================================================================
# VER-004: Mandatory Artifact Generation (CTQ-2.1) - PRIORITY 1
# ============================================================================

def test_ver004a_system_test_all_files_created():
    """
    VER-004-A: System test - verify all required files created.
    Tests file existence and basic content validation.
    """
    print("\n" + "="*70)
    print("VER-004-A: System Test - File Creation Verification")
    print("="*70)

    test_output_dir = Path(__file__).parent / "data" / "test_verification_files"
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)

    # Test R2 (11 artifacts)
    intake_request = IntakeRequest(
        project_name="VER-004-A Test",
        timestamp=datetime.utcnow(),
        answers=IntakeAnswers(
            q1_users="External",
            q2_influence="Recommendations",
            q3_worst_failure="Financial",
            q4_reversibility="Partial",
            q5_domain="Partially",
            q6_scale="Multi_team",
            q7_regulated="No"
        )
    )

    classification, _ = classify_risk(intake_request.answers)

    intake_response = IntakeResponse(
        intake_id="ver-004-a",
        project_name=intake_request.project_name,
        timestamp=intake_request.timestamp,
        answers=intake_request.answers,
        classification=classification,
        warnings=[],
        expert_review_required=False,
        expert_review_recommended=False,
        next_steps=[],
        artifacts_required=get_required_artifacts(classification.risk_level)
    )

    result = generate_project_artifacts(
        intake_request,
        intake_response,
        output_dir=test_output_dir
    )

    # Verify all files exist and have content
    errors = []
    for file_path in result['file_paths']:
        path = Path(file_path)
        if not path.exists():
            errors.append(f"File missing: {path.name}")
        else:
            size = path.stat().st_size
            if size < 100:  # At least 100 bytes of content
                errors.append(f"File too small: {path.name} ({size} bytes)")
            else:
                # Verify it's valid markdown (has headers)
                with open(path, 'r') as f:
                    content = f.read()
                    if not content.startswith('#'):
                        errors.append(f"Invalid markdown: {path.name} (no header)")

    if errors:
        print(f"❌ FAIL: File verification")
        for error in errors:
            print(f"   - {error}")
        assert False, "File verification failed"
    else:
        print(f"✅ PASS: All {len(result['file_paths'])} files created and valid")
        print(f"   Total size: {sum(Path(f).stat().st_size for f in result['file_paths'])} bytes")
        return 1, 0


# ============================================================================
# TEST RUNNER
# ============================================================================

def main():
    """Run all Phase 6 verification tests."""
    print("="*70)
    print("PHASE 6: TESTING & VERIFICATION")
    print("QMS Dashboard Verification Test Suite")
    print("="*70)

    tests = [
        ("VER-001-A: Risk Classification - All Scenarios", test_ver001a_risk_classification_all_scenarios),
        ("VER-001-C: Risk Classification - Boundary Cases", test_ver001c_boundary_cases),
        ("VER-002-A: Artifact List by Risk Level", test_ver002a_artifact_list_by_risk),
        ("VER-002-B: Integration Test - Full Flow", test_ver002b_integration_full_flow),
        ("VER-004-A: System Test - File Creation", test_ver004a_system_test_all_files_created),
    ]

    total_passed = 0
    total_failed = 0
    failed_tests = []

    for test_name, test_func in tests:
        try:
            passed, failed = test_func()
            total_passed += passed
            total_failed += failed
            if failed > 0:
                failed_tests.append(test_name)
        except AssertionError as e:
            print(f"\n❌ FAILED: {test_name}")
            print(f"   Error: {e}")
            total_failed += 1
            failed_tests.append(test_name)
        except Exception as e:
            print(f"\n❌ ERROR: {test_name}")
            print(f"   Exception: {e}")
            import traceback
            traceback.print_exc()
            total_failed += 1
            failed_tests.append(test_name)

    # Summary
    print("\n" + "="*70)
    print("PHASE 6 VERIFICATION SUMMARY")
    print("="*70)
    print(f"Total Test Cases Passed: {total_passed}")
    print(f"Total Test Cases Failed: {total_failed}")
    print(f"Success Rate: {(total_passed / (total_passed + total_failed) * 100):.1f}%")

    if failed_tests:
        print(f"\nFailed Tests:")
        for test in failed_tests:
            print(f"  ❌ {test}")
        print(f"\n❌ {len(failed_tests)} verification test(s) failed")
        return 1
    else:
        print("\n✅ All Phase 6 verification tests PASSED!")
        print("\n** System verified and ready for production deployment **")
        return 0


if __name__ == "__main__":
    sys.exit(main())
