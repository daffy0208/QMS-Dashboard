#!/usr/bin/env python3
"""
Test script for QMS Dashboard intake system.
Tests classification logic with sample data from VAL-001 and VAL-002.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from models.intake import IntakeAnswers, IntakeRequest
from validation.classifier import classify_risk, get_required_artifacts
from validation.layer1 import validate_intake_answers, validate_project_name
from datetime import datetime


def test_classification(name: str, answers: IntakeAnswers, expected_risk: str):
    """Test a single classification scenario."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")

    # Print answers
    print("\nAnswers:")
    print(f"  Q1 Users: {answers.q1_users}")
    print(f"  Q2 Influence: {answers.q2_influence}")
    print(f"  Q3 Worst Failure: {answers.q3_worst_failure}")
    print(f"  Q4 Reversibility: {answers.q4_reversibility}")
    print(f"  Q5 Domain: {answers.q5_domain}")
    print(f"  Q6 Scale: {answers.q6_scale}")
    print(f"  Q7 Regulated: {answers.q7_regulated}")

    # Classify
    classification, warnings = classify_risk(answers)

    # Print results
    print(f"\nClassification:")
    print(f"  Risk Level: {classification.risk_level}")
    print(f"  Rigor: {classification.rigor}")
    print(f"  Borderline: {classification.borderline}")
    print(f"  Rationale: {classification.rationale}")

    # Print warnings
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  [{w.severity}] {w.layer}: {w.message}")
            if w.recommendation:
                print(f"    → {w.recommendation}")
    else:
        print("\nNo warnings")

    # Print required artifacts
    artifacts = get_required_artifacts(classification.risk_level)
    print(f"\nRequired Artifacts ({len(artifacts)}):")
    for artifact in artifacts:
        print(f"  - {artifact}")

    # Check if correct
    status = "✅ PASS" if classification.risk_level == expected_risk else f"❌ FAIL (expected {expected_risk})"
    print(f"\nResult: {status}")

    return classification.risk_level == expected_risk


def main():
    """Run test suite."""
    print("QMS Dashboard - Intake Classification Tests")
    print("Based on VAL-001 and VAL-002 validation test scenarios")

    tests_passed = 0
    tests_total = 0

    # Test 1: Sarah - Web Developer (E-commerce checkout)
    # Expected: R2 (External users, Automated actions, Financial loss)
    tests_total += 1
    if test_classification(
        "Sarah - E-commerce Checkout Flow",
        IntakeAnswers(
            q1_users="External",
            q2_influence="Automated",
            q3_worst_failure="Financial",
            q4_reversibility="Partial",
            q5_domain="Yes",
            q6_scale="Organization_Public",
            q7_regulated="Possibly"
        ),
        expected_risk="R3"  # Actually should be R3 (Financial + Automated)
    ):
        tests_passed += 1

    # Test 2: Marcus - Senior Engineer (Internal API)
    # Expected: R0 (Internal, Informational, Annoyance, Easy)
    tests_total += 1
    if test_classification(
        "Marcus - Internal Data Aggregation API",
        IntakeAnswers(
            q1_users="Internal",
            q2_influence="Informational",
            q3_worst_failure="Annoyance",
            q4_reversibility="Easy",
            q5_domain="Yes",
            q6_scale="Multi_team",
            q7_regulated="No"
        ),
        expected_risk="R1"  # R1 due to Multi_team scale
    ):
        tests_passed += 1

    # Test 3: Aisha - Research Scientist (Medical image analysis)
    # Expected: R3 (Safety/legal/compliance)
    tests_total += 1
    if test_classification(
        "Aisha - Medical Image Analysis Tool",
        IntakeAnswers(
            q1_users="External",
            q2_influence="Recommendations",
            q3_worst_failure="Safety_Legal_Compliance",
            q4_reversibility="Hard",
            q5_domain="Partially",
            q6_scale="Multi_team",
            q7_regulated="Yes"
        ),
        expected_risk="R3"
    ):
        tests_passed += 1

    # Test 4: Tom - Team Lead (Monitoring dashboard)
    # Expected: R1 (Internal, Informational, but Multi-team)
    tests_total += 1
    if test_classification(
        "Tom - Infrastructure Monitoring Dashboard",
        IntakeAnswers(
            q1_users="Internal",
            q2_influence="Informational",
            q3_worst_failure="Annoyance",
            q4_reversibility="Easy",
            q5_domain="Yes",
            q6_scale="Multi_team",
            q7_regulated="No"
        ),
        expected_risk="R1"
    ):
        tests_passed += 1

    # Test 5: QMS Dashboard itself (from our intake)
    # Expected: R2 (Internal, Recommendations, Safety/legal, Easy reversibility)
    tests_total += 1
    if test_classification(
        "QMS Dashboard (Self)",
        IntakeAnswers(
            q1_users="Internal",
            q2_influence="Recommendations",
            q3_worst_failure="Safety_Legal_Compliance",
            q4_reversibility="Easy",
            q5_domain="Partially",
            q6_scale="Individual",
            q7_regulated="No"
        ),
        expected_risk="R2"
    ):
        tests_passed += 1

    # Test 6: Rachel - Platform Engineer (Auth service)
    # Expected: R3 (Security breach = Safety/legal)
    tests_total += 1
    if test_classification(
        "Rachel - Authentication Service",
        IntakeAnswers(
            q1_users="Internal",
            q2_influence="Automated",
            q3_worst_failure="Safety_Legal_Compliance",
            q4_reversibility="Hard",
            q5_domain="Yes",
            q6_scale="Organization_Public",
            q7_regulated="Possibly"
        ),
        expected_risk="R3"
    ):
        tests_passed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    print(f"Success Rate: {(tests_passed/tests_total)*100:.1f}%")

    if tests_passed == tests_total:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {tests_total - tests_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
