#!/usr/bin/env python3
"""
Phase 8A WS-1.7: Test R0/R1 acceptance criteria
Tests warning-only validation for low-risk projects.
"""

import sys
sys.path.insert(0, 'src/backend')

from artifacts.validator import ArtifactValidator

def test_r0_quality_plan():
    """Test R0 Quality Plan validation (warning-only)."""
    print("Testing R0 Quality Plan validation...")

    validator = ArtifactValidator()

    # R0 Quality Plan with just Purpose section
    content = """# Quality Plan
## Test Project

## Purpose
This is a simple internal tool for team use.
"""

    result = validator.validate_artifact("Quality Plan", content, "R0")

    print(f"  Valid: {result.valid}")
    print(f"  Completion: {result.completion_percent:.1%}")
    print(f"  Issues: {len(result.issues)}")

    # R0 should have warnings, not errors
    has_errors = any(issue.severity == "error" for issue in result.issues)
    has_warnings = any(issue.severity == "warning" for issue in result.issues)

    if has_errors:
        print(f"  ❌ FAIL: R0 should not have errors (warning-only mode)")
        return False

    print(f"  ✅ PASS: R0 validation is warning-only")
    return True


def test_r1_quality_plan():
    """Test R1 Quality Plan validation (moderate rigor)."""
    print("\nTesting R1 Quality Plan validation...")

    validator = ArtifactValidator()

    # R1 Quality Plan missing required sections
    content = """# Quality Plan
## Test Project

## Purpose
This is an internal production tool.
"""

    result = validator.validate_artifact("Quality Plan", content, "R1")

    print(f"  Valid: {result.valid}")
    print(f"  Completion: {result.completion_percent:.1%}")
    print(f"  Issues: {len(result.issues)}")
    print(f"  Missing sections: {result.missing_sections}")

    # R1 should have errors for missing required sections
    has_errors = any(issue.severity == "error" for issue in result.issues)

    if not has_errors:
        print(f"  ❌ FAIL: R1 should have errors for incomplete artifacts")
        return False

    if "Scope" not in result.missing_sections or "Quality Objectives" not in result.missing_sections:
        print(f"  ❌ FAIL: R1 should flag missing Scope and Quality Objectives")
        return False

    print(f"  ✅ PASS: R1 validation has appropriate rigor")
    return True


def test_r0_risk_register():
    """Test R0 Risk Register validation (warning-only)."""
    print("\nTesting R0 Risk Register validation...")

    validator = ArtifactValidator()

    # R0 Risk Register with 1 risk (minimum)
    content = """# Risk Register
## Test Project

### R-001: Basic Risk
**Description:** Something might go wrong
"""

    result = validator.validate_artifact("Risk Register", content, "R0")

    print(f"  Valid: {result.valid}")
    print(f"  Completion: {result.completion_percent:.1%}")
    print(f"  Issues: {len(result.issues)}")

    # R0 should accept 1 risk (min_risks=1)
    has_risk_count_error = any(
        "Expected at least" in issue.message and issue.severity == "error"
        for issue in result.issues
    )

    if has_risk_count_error:
        print(f"  ❌ FAIL: R0 should accept 1 risk (min_risks=1)")
        return False

    print(f"  ✅ PASS: R0 Risk Register accepts 1 risk")
    return True


def test_r1_risk_register():
    """Test R1 Risk Register validation (moderate rigor)."""
    print("\nTesting R1 Risk Register validation...")

    validator = ArtifactValidator()

    # R1 Risk Register with only 1 risk (need 2)
    content = """# Risk Register
## Test Project

### R-001: Basic Risk
**Description:** Something might go wrong
**Mitigation:** We'll handle it
"""

    result = validator.validate_artifact("Risk Register", content, "R1")

    print(f"  Valid: {result.valid}")
    print(f"  Completion: {result.completion_percent:.1%}")
    print(f"  Issues: {len(result.issues)}")

    # R1 should require 2 risks minimum
    has_risk_count_error = any(
        "Expected at least 2 risks" in issue.message
        for issue in result.issues
    )

    if not has_risk_count_error:
        print(f"  ❌ FAIL: R1 should require at least 2 risks")
        return False

    print(f"  ✅ PASS: R1 Risk Register requires 2+ risks")
    return True


def test_placeholders_allowed():
    """Test that R0 allows placeholders."""
    print("\nTesting R0 placeholder handling...")

    validator = ArtifactValidator()

    # R0 Quality Plan with placeholders
    content = """# Quality Plan
## Test Project

## Purpose
[TBD - to be filled in later]
"""

    result = validator.validate_artifact("Quality Plan", content, "R0")

    print(f"  Valid: {result.valid}")
    print(f"  Placeholder count: {result.placeholder_count}")

    # R0 should allow placeholders (no error for placeholders)
    has_placeholder_error = any(
        "placeholder" in issue.message.lower() and issue.severity == "error"
        for issue in result.issues
    )

    if has_placeholder_error:
        print(f"  ❌ FAIL: R0 should allow placeholders")
        return False

    print(f"  ✅ PASS: R0 allows placeholders")
    return True


if __name__ == "__main__":
    print("="*70)
    print("PHASE 8A WS-1.7: R0/R1 Acceptance Criteria Test")
    print("="*70)

    tests = [
        test_r0_quality_plan,
        test_r1_quality_plan,
        test_r0_risk_register,
        test_r1_risk_register,
        test_placeholders_allowed
    ]

    results = [test() for test in tests]

    print("\n" + "="*70)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("="*70)

    if all(results):
        print("✅ WS-1.7 R0/R1 VALIDATION TEST PASSED")
        sys.exit(0)
    else:
        print("❌ WS-1.7 R0/R1 VALIDATION TEST FAILED")
        sys.exit(1)
