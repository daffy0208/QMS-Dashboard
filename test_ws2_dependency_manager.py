#!/usr/bin/env python3
"""
Phase 8A WS-2: Unit tests for Dependency Manager
Tests readiness assessment, dependency checking, and cross-reference validation.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src/backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from artifacts.dependency_manager import (
    DependencyManager,
    ReadinessAssessment,
    DependencyStatus,
    NextActionRecommendation
)
from artifacts.validator import ArtifactValidator, ValidationResult


def create_test_artifact(content: str, risk_level: str = "R2"):
    """Helper to create test artifact content."""
    return content


def test_dependency_manager_initialization():
    """Test that dependency manager initializes correctly."""
    print("\n" + "="*70)
    print("TEST: Dependency Manager Initialization")
    print("="*70)

    dep_manager = DependencyManager()

    # Check configuration loaded
    assert dep_manager.dependencies is not None
    assert dep_manager.thresholds is not None
    assert dep_manager.volatility_lookup is not None

    # Check risk level thresholds
    assert "R0" in dep_manager.thresholds
    assert "R1" in dep_manager.thresholds
    assert "R2" in dep_manager.thresholds
    assert "R3" in dep_manager.thresholds

    print("✓ Dependency manager initialized successfully")
    print(f"✓ Loaded {len(dep_manager.dependencies)} artifact dependencies")
    print(f"✓ Loaded thresholds for {len(dep_manager.thresholds)} risk levels")


def test_risk_proportionate_thresholds():
    """Test that thresholds are risk-proportionate (WS-2 Principle 1)."""
    print("\n" + "="*70)
    print("TEST: Risk-Proportionate Thresholds (Principle 1)")
    print("="*70)

    dep_manager = DependencyManager()

    # Check that thresholds increase with risk level
    r0_threshold = dep_manager.thresholds["R0"]["completion"]
    r1_threshold = dep_manager.thresholds["R1"]["completion"]
    r2_threshold = dep_manager.thresholds["R2"]["completion"]
    r3_threshold = dep_manager.thresholds["R3"]["completion"]

    assert r0_threshold < r1_threshold < r2_threshold < r3_threshold
    print(f"✓ R0 threshold: {r0_threshold} < R1: {r1_threshold} < R2: {r2_threshold} < R3: {r3_threshold}")

    # Check error tolerance decreases
    r0_errors = dep_manager.thresholds["R0"]["max_errors"]
    r3_errors = dep_manager.thresholds["R3"]["max_errors"]

    assert r0_errors > r3_errors
    print(f"✓ R0 max errors: {r0_errors} > R3: {r3_errors}")


def test_volatility_modifier():
    """Test artifact volatility modifier (Dark-Matter Patch #1)."""
    print("\n" + "="*70)
    print("TEST: Artifact Volatility Modifier (Dark-Matter Patch #1)")
    print("="*70)

    dep_manager = DependencyManager()

    # Test draft-friendly artifact (lower threshold)
    verification_plan_volatility = dep_manager.volatility_lookup["Verification Plan"]
    assert verification_plan_volatility == "draft_friendly"
    modifier = dep_manager.volatility_classes[verification_plan_volatility]["modifier"]
    assert modifier == -0.1
    print(f"✓ Verification Plan: {verification_plan_volatility} (modifier: {modifier})")

    # Test foundation artifact (no modifier)
    risk_register_volatility = dep_manager.volatility_lookup["Risk Register"]
    assert risk_register_volatility == "foundation"
    modifier = dep_manager.volatility_classes[risk_register_volatility]["modifier"]
    assert modifier == 0.0
    print(f"✓ Risk Register: {risk_register_volatility} (modifier: {modifier})")

    # Test rework-costly artifact (higher threshold)
    traceability_volatility = dep_manager.volatility_lookup["Traceability Index"]
    assert traceability_volatility == "rework_costly"
    modifier = dep_manager.volatility_classes[traceability_volatility]["modifier"]
    assert modifier == 0.1
    print(f"✓ Traceability Index: {traceability_volatility} (modifier: {modifier})")


def test_readiness_assessment():
    """Test readiness assessment respects WS-1 validation results."""
    print("\n" + "="*70)
    print("TEST: Readiness Assessment (Uses WS-1 Results)")
    print("="*70)

    dep_manager = DependencyManager()

    # Create test artifact with good completion
    test_content = """
# Risk Register
## Project Name: Test Project

### Risk Assessment
- R-001: Authentication failure with description and mitigation plan
- R-002: Data breach risk with impact analysis
- R-003: Performance degradation monitored
"""

    # Assess readiness for R2
    readiness = dep_manager.assess_readiness(
        artifact_name="Risk Register",
        content=test_content,
        risk_level="R2"
    )

    # Check response structure
    assert isinstance(readiness, ReadinessAssessment), f"Expected ReadinessAssessment, got {type(readiness)}"
    assert readiness.artifact_name == "Risk Register", f"Expected 'Risk Register', got '{readiness.artifact_name}'"
    assert 0.0 <= readiness.completion <= 1.0, f"Completion {readiness.completion} not in [0.0, 1.0]"
    assert readiness.epistemic_status == "structural_only", f"Expected 'structural_only', got '{readiness.epistemic_status}'"
    assert readiness.can_proceed_anyway == True, f"can_proceed_anyway must always be True, got {readiness.can_proceed_anyway}"  # Always true per WS-2 non-goal #3

    # Check confidence limits present (Dark-Matter Patch #6)
    assert len(readiness.confidence_limits) > 0, "confidence_limits must not be empty"
    # Check that confidence_limits contains expected messaging
    confidence_text = ' '.join(readiness.confidence_limits).lower()
    assert "structure" in confidence_text or "structural" in confidence_text, f"confidence_limits should mention structure/structural: {readiness.confidence_limits}"

    print(f"✓ Readiness: {readiness.ready}")
    print(f"✓ Completion: {readiness.completion:.0%}")
    print(f"✓ Epistemic status: {readiness.epistemic_status}")
    print(f"✓ Can proceed anyway: {readiness.can_proceed_anyway}")


def test_soft_blocking():
    """Test that WS-2 does NOT hard-block (Principle 3 / Non-Goal #3)."""
    print("\n" + "="*70)
    print("TEST: Soft Blocking (Principle 3 / Non-Goal #3)")
    print("="*70)

    dep_manager = DependencyManager()

    # Create artifact with low completion
    test_content = """
# Risk Register
[TBD]
"""

    readiness = dep_manager.assess_readiness(
        artifact_name="Risk Register",
        content=test_content,
        risk_level="R3"  # Strict risk level
    )

    # Even for R3 with low completion, can_proceed_anyway must be True
    assert readiness.can_proceed_anyway == True
    print(f"✓ Even with {readiness.completion:.0%} completion at R3, can_proceed_anyway = True")

    # Should have reason explaining why not ready, but NOT blocking
    if not readiness.ready:
        assert readiness.reason is not None
        print(f"✓ Reason provided: {readiness.reason}")
        # Check language is NOT prescriptive
        assert "must" not in readiness.reason.lower()
        assert "cannot" not in readiness.reason.lower()
        print("✓ Language is descriptive, not prescriptive")


def test_cross_reference_validation():
    """Test cross-reference validation is structural only (Principle 4)."""
    print("\n" + "="*70)
    print("TEST: Cross-Reference Validation (Structural Only)")
    print("="*70)

    dep_manager = DependencyManager()

    # Test risk ID extraction
    content = """
# Risk Register
- R-001: Authentication
- R-002: Authorization
- R-003: Encryption
"""

    risk_ids = dep_manager._extract_risk_ids(content)
    assert "R-001" in risk_ids
    assert "R-002" in risk_ids
    assert "R-003" in risk_ids
    print(f"✓ Extracted {len(risk_ids)} risk IDs")

    # Test CTQ ID extraction
    ctq_content = """
# CTQ Tree
- CTQ-001: Performance
- CTQ-002: Security
"""

    ctq_ids = dep_manager._extract_ctq_ids(ctq_content)
    assert "CTQ-001" in ctq_ids
    assert "CTQ-002" in ctq_ids
    print(f"✓ Extracted {len(ctq_ids)} CTQ IDs")


def test_dependencies_are_directional():
    """Test dependencies are directional (Principle 2)."""
    print("\n" + "="*70)
    print("TEST: Dependencies Are Directional (Principle 2)")
    print("="*70)

    dep_manager = DependencyManager()

    # Verification Plan depends on Risk Register
    verification_deps = dep_manager.dependencies.get("Verification Plan", [])
    assert "Risk Register" in verification_deps
    print(f"✓ Verification Plan depends on: {', '.join(verification_deps)}")

    # Risk Register does NOT depend on Verification Plan (directional)
    risk_register_deps = dep_manager.dependencies.get("Risk Register", [])
    assert "Verification Plan" not in risk_register_deps
    print(f"✓ Risk Register depends on: {', '.join(risk_register_deps) if risk_register_deps else 'nothing (foundation)'}")


def test_no_revalidation():
    """Test WS-2 uses WS-1 validation, doesn't reimplement (Non-Goal #5)."""
    print("\n" + "="*70)
    print("TEST: WS-2 Uses WS-1 Validation (Non-Goal #5)")
    print("="*70)

    dep_manager = DependencyManager()

    # WS-2 should use WS-1 validator instance
    assert isinstance(dep_manager.validator, ArtifactValidator)
    print("✓ WS-2 uses WS-1 validator (not reimplementing)")

    # Test that assess_readiness calls WS-1 validator
    test_content = """
# Quality Plan
## Purpose
Test purpose
"""

    readiness = dep_manager.assess_readiness(
        artifact_name="Quality Plan",
        content=test_content,
        risk_level="R2"
    )

    # Completion should match WS-1 calculation
    ws1_result = dep_manager.validator.validate_artifact(
        "Quality Plan",
        test_content,
        "R2"
    )

    assert readiness.completion == ws1_result.completion_percent
    print(f"✓ WS-2 completion ({readiness.completion:.0%}) matches WS-1 ({ws1_result.completion_percent:.0%})")


def test_override_budget_tracking():
    """Test override budget tracking (Dark-Matter Patch #3)."""
    print("\n" + "="*70)
    print("TEST: Override Budget Tracking (Dark-Matter Patch #3)")
    print("="*70)

    dep_manager = DependencyManager()

    test_content = """
# Risk Register
## Risk Assessment
Test content
"""

    # Test with override count
    readiness = dep_manager.assess_readiness(
        artifact_name="Risk Register",
        content=test_content,
        risk_level="R2",
        override_count=5  # User has overridden 5 times
    )

    # Should have override budget
    assert readiness.override_budget is not None
    assert readiness.override_budget["count"] == 5
    assert readiness.override_budget["status"] == "high"  # > 2 is high
    print(f"✓ Override budget: {readiness.override_budget}")


def test_no_prescriptive_language():
    """Test messaging uses descriptive language (Non-Goal #4)."""
    print("\n" + "="*70)
    print("TEST: No Prescriptive Language (Non-Goal #4)")
    print("="*70)

    dep_manager = DependencyManager()

    test_content = """
# Risk Register
[TBD]
"""

    readiness = dep_manager.assess_readiness(
        artifact_name="Risk Register",
        content=test_content,
        risk_level="R2"
    )

    # Check reason doesn't use prescriptive words
    if readiness.reason:
        reason_lower = readiness.reason.lower()
        assert "must" not in reason_lower
        assert "cannot" not in reason_lower
        assert "required to" not in reason_lower
        print(f"✓ Reason uses descriptive language: '{readiness.reason}'")


def run_all_tests():
    """Run all unit tests."""
    print("\n" + "="*70)
    print("WS-2 DEPENDENCY MANAGER UNIT TESTS")
    print("="*70)

    tests = [
        test_dependency_manager_initialization,
        test_risk_proportionate_thresholds,
        test_volatility_modifier,
        test_readiness_assessment,
        test_soft_blocking,
        test_cross_reference_validation,
        test_dependencies_are_directional,
        test_no_revalidation,
        test_override_budget_tracking,
        test_no_prescriptive_language
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ FAILED: {test.__name__}")
            print(f"   {str(e)}")
            failed += 1
        except Exception as e:
            print(f"\n❌ ERROR: {test.__name__}")
            print(f"   {str(e)}")
            failed += 1

    print("\n" + "="*70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*70)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
