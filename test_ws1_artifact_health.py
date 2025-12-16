#!/usr/bin/env python3
"""
Phase 8A WS-1: End-to-end test for Artifact Health API
Tests artifact validation and health reporting.
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_artifact_health():
    """Test the artifact health API endpoint."""

    print("="*70)
    print("PHASE 8A WS-1: Artifact Health API Test")
    print("="*70)
    print()

    # Step 1: Create a test intake (R2/R3 system with some risk factors)
    print("Step 1: Creating test intake (R2/R3 classification expected)...")
    intake_request = {
        "project_name": "WS1-Test-AI-Dashboard",
        "answers": {
            "q1_users": "External",
            "q2_influence": "Recommendations",
            "q3_worst_failure": "Financial",
            "q4_reversibility": "Hard",
            "q5_domain": "Yes",
            "q6_scale": "Team",
            "q7_regulated": "No"
        }
    }

    response = requests.post(f"{BASE_URL}/api/intake", json=intake_request)
    if response.status_code not in [200, 201]:
        print(f"❌ Failed to create intake: {response.status_code}")
        print(response.text)
        return False

    intake_response = response.json()
    intake_id = intake_response["intake_id"]
    risk_level = intake_response["classification"]["risk_level"]
    print(f"✓ Intake created: {intake_id}")
    print(f"✓ Classification: {risk_level}")
    print()

    # Step 2: Generate artifacts
    print("Step 2: Generating artifacts...")
    response = requests.post(f"{BASE_URL}/api/intake/{intake_id}/generate-artifacts")
    if response.status_code != 200:
        print(f"❌ Failed to generate artifacts: {response.status_code}")
        print(response.text)
        return False

    artifacts_response = response.json()
    artifact_count = len(artifacts_response.get("artifacts_generated", []))
    print(f"✓ Generated {artifact_count} artifacts")
    for artifact in artifacts_response.get("artifacts_generated", []):
        print(f"  - {artifact}")
    print()

    # Step 3: Call artifact health endpoint (NEW IN WS-1.4)
    print("Step 3: Checking artifact health...")
    response = requests.get(f"{BASE_URL}/api/intake/{intake_id}/artifact-health")
    if response.status_code != 200:
        print(f"❌ Failed to get artifact health: {response.status_code}")
        print(response.text)
        return False

    health = response.json()
    print(f"✓ Artifact health retrieved")
    print()

    # Step 4: Validate response structure
    print("Step 4: Validating response structure...")

    required_fields = [
        "intake_id", "project_name", "risk_level", "overall_completion",
        "artifacts", "total_artifacts", "complete_artifacts",
        "artifacts_with_errors", "observations"
    ]

    for field in required_fields:
        if field not in health:
            print(f"❌ Missing required field: {field}")
            return False
    print("✓ All required fields present")
    print()

    # Step 5: Display health summary
    print("Step 5: Artifact Health Summary")
    print("-" * 70)
    print(f"Project: {health['project_name']}")
    print(f"Risk Level: {health['risk_level']}")
    print(f"Overall Completion: {health['overall_completion']:.1%}")
    print(f"Total Artifacts: {health['total_artifacts']}")
    print(f"Complete Artifacts: {health['complete_artifacts']}")
    print(f"Artifacts with Errors: {health['artifacts_with_errors']}")
    print()

    print("Observations:")
    for obs in health['observations']:
        print(f"  • {obs}")
    print()

    # Step 6: Check individual artifact health
    print("Step 6: Individual Artifact Health")
    print("-" * 70)

    for artifact_name, artifact_health in health['artifacts'].items():
        print(f"\n{artifact_name}:")
        print(f"  Completion: {artifact_health['completion_percent']:.1%}")
        print(f"  Valid: {artifact_health['valid']}")
        print(f"  Issues: {artifact_health['issue_count']} ({artifact_health['error_count']} errors, {artifact_health['warning_count']} warnings)")
        print(f"  Placeholders: {artifact_health['placeholder_count']}")

        if artifact_health['missing_sections']:
            print(f"  Missing Sections: {', '.join(artifact_health['missing_sections'])}")

        if artifact_health['top_issues']:
            print(f"  Top Issues:")
            for issue in artifact_health['top_issues'][:3]:
                print(f"    - {issue}")
    print()

    # Step 7: Verify validator is detecting placeholders (expected in fresh templates)
    print("Step 7: Validator Detection Tests")
    print("-" * 70)

    # Fresh templates should have placeholders
    has_placeholders = any(
        a['placeholder_count'] > 0
        for a in health['artifacts'].values()
    )

    if has_placeholders:
        print("✓ Validator detected placeholders in templates")
    else:
        print("⚠ No placeholders detected (unexpected for fresh templates)")

    # R2 artifacts should have required sections defined
    for artifact_name, artifact_health in health['artifacts'].items():
        if artifact_name in ["Quality Plan", "Risk Register"]:
            if artifact_health['issue_count'] > 0:
                print(f"✓ Validator found issues in {artifact_name} (expected)")
            else:
                print(f"⚠ No issues found in {artifact_name} (unexpected for fresh template)")
    print()

    # Step 8: Test messaging discipline
    print("Step 8: Messaging Discipline Check")
    print("-" * 70)

    # Check that observations are descriptive, not prescriptive
    prescriptive_words = ["must", "should", "fix", "cannot", "will fail", "blocked"]
    messaging_clean = True

    for obs in health['observations']:
        obs_lower = obs.lower()
        for word in prescriptive_words:
            if word in obs_lower:
                print(f"⚠ Prescriptive language detected: '{word}' in '{obs}'")
                messaging_clean = False

    if messaging_clean:
        print("✓ Observations are descriptive (no prescriptive commands)")
    print()

    print("="*70)
    print("✅ WS-1 ARTIFACT HEALTH API TEST PASSED")
    print("="*70)

    # Output JSON for inspection
    print("\nFull Response JSON:")
    print(json.dumps(health, indent=2))

    return True

if __name__ == "__main__":
    try:
        success = test_artifact_health()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
