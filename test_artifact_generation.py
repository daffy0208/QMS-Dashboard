#!/usr/bin/env python3
"""
Test script for Phase 4: Artifact Generation.
Tests artifact generation for different risk levels.
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from models.intake import IntakeRequest, IntakeResponse, IntakeAnswers, RiskClassification, ValidationWarning
from artifacts.generator import generate_project_artifacts


def test_r2_artifact_generation():
    """Test artifact generation for R2 project (QMS Dashboard itself)."""
    print("\n" + "="*60)
    print("TEST: Artifact Generation for R2 Project")
    print("="*60)

    # Create sample intake (QMS Dashboard itself)
    intake_request = IntakeRequest(
        project_name="QMS Dashboard Test",
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
        project_name="QMS Dashboard Test",
        timestamp=datetime.now(timezone.utc),
        answers=intake_request.answers,
        classification=RiskClassification(
            risk_level="R2",
            rigor="Strict",
            rationale="R2 due to: Recommendations + safety/legal concerns",
            borderline=True
        ),
        warnings=[],
        expert_review_required=False,
        expert_review_recommended=True,
        next_steps=[],
        artifacts_required=[
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
    )

    # Generate artifacts
    test_output_dir = Path(__file__).parent / "data" / "test_artifacts"
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)

    result = generate_project_artifacts(
        intake_request,
        intake_response,
        output_dir=test_output_dir
    )

    # Verify results
    print(f"\n✅ Generated {len(result['artifacts_generated'])} artifacts")
    print(f"   Expected: 11 (R2 requires all artifacts)")
    assert len(result['artifacts_generated']) == 11, "R2 should generate 11 artifacts"

    print(f"\n📁 Output directory: {result['output_directory']}")
    print(f"📦 ZIP file: {result['zip_file']}")

    # Verify files exist
    print(f"\n📄 Generated files:")
    for file_path in result['file_paths']:
        path = Path(file_path)
        assert path.exists(), f"File not found: {file_path}"
        size = path.stat().st_size
        print(f"   - {path.name} ({size} bytes)")

    # Verify ZIP exists
    zip_path = Path(result['zip_file'])
    assert zip_path.exists(), "ZIP file not created"
    zip_size = zip_path.stat().st_size
    print(f"\n   ✅ ZIP archive created: {zip_size} bytes")

    # Read and display sample of Quality Plan
    quality_plan_path = test_output_dir / "QMS-Quality-Plan.md"
    with open(quality_plan_path, 'r') as f:
        content = f.read()
        lines = content.split('\n')
        print(f"\n📖 Quality Plan Preview (first 20 lines):")
        print("   " + "-"*56)
        for line in lines[:20]:
            print(f"   {line}")
        print("   " + "-"*56)

    print(f"\n✅ R2 Artifact Generation Test PASSED")
    return True


def test_r0_artifact_generation():
    """Test artifact generation for R0 project (minimal rigor)."""
    print("\n" + "="*60)
    print("TEST: Artifact Generation for R0 Project")
    print("="*60)

    intake_request = IntakeRequest(
        project_name="Simple Internal Tool",
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
        intake_id="test-r0",
        project_name="Simple Internal Tool",
        timestamp=datetime.now(timezone.utc),
        answers=intake_request.answers,
        classification=RiskClassification(
            risk_level="R0",
            rigor="Minimal",
            rationale="Internal, low impact, fully reversible",
            borderline=False
        ),
        warnings=[],
        expert_review_required=False,
        expert_review_recommended=False,
        next_steps=[],
        artifacts_required=[
            "Quality Plan",
            "CTQ Tree",
            "Assumptions Register",
            "Risk Register",
            "Traceability Index"
        ]
    )

    test_output_dir = Path(__file__).parent / "data" / "test_artifacts_r0"
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)

    result = generate_project_artifacts(
        intake_request,
        intake_response,
        output_dir=test_output_dir
    )

    print(f"\n✅ Generated {len(result['artifacts_generated'])} artifacts")
    print(f"   Expected: 5 (R0 requires base artifacts only)")
    assert len(result['artifacts_generated']) == 5, "R0 should generate 5 artifacts"

    print(f"\n✅ R0 Artifact Generation Test PASSED")
    return True


def main():
    """Run all artifact generation tests."""
    print("QMS Dashboard - Phase 4: Artifact Generation Tests")
    print("="*60)

    tests = [
        ("R2 Artifact Generation", test_r2_artifact_generation),
        ("R0 Artifact Generation", test_r0_artifact_generation),
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
            import traceback
            traceback.print_exc()
            failed += 1

    # Summary
    print("\n" + "="*60)
    print(f"TEST SUMMARY")
    print("="*60)
    print(f"Tests Passed: {passed}/{len(tests)}")
    print(f"Tests Failed: {failed}/{len(tests)}")

    if passed == len(tests):
        print("\n✅ All artifact generation tests passed!")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
