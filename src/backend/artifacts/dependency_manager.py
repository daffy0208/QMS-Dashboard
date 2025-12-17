"""
Dependency Manager - Phase 8A WS-2
Manages artifact dependencies and provides readiness assessment.

Design Principles (from WS-2 docs):
1. Diagnostic, Not Prescriptive - Show gaps, never fill them
2. Soft Blocking, Not Hard Blocking - Recommend, don't enforce
3. Trust WS-1 Results - Use validation outputs directly
4. Risk-Proportionate Rigor - R0/R1 lenient, R2/R3 strict
5. Teaching, Not Enforcement - Guide users, don't block them
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel

# Import WS-1 validator
from .validator import ArtifactValidator, ValidationResult


class ReadinessAssessment(BaseModel):
    """Result of checking if an artifact is ready for downstream use."""
    artifact_name: str
    ready: bool
    completion: float  # WS-1 completion_percent
    epistemic_status: str = "structural_only"
    confidence_limits: List[str]
    can_proceed_anyway: bool = True  # Always true per WS-2 non-goal #3
    placeholder_density: float
    readiness_basis: str = "structural"

    # If not ready, explain why
    reason: Optional[str] = None
    blocking_issues: List[str] = []

    # Dark-Matter Patch #3: Override budget tracking
    override_budget: Optional[Dict] = None


class DependencyStatus(BaseModel):
    """Status of a single artifact's dependencies."""
    artifact_name: str
    dependencies: List[str]  # List of prerequisite artifact names
    all_dependencies_ready: bool
    blocking_dependencies: List[str]  # Which dependencies are not ready
    readiness: ReadinessAssessment

    # Suggested action (teaching-oriented)
    suggestion: Optional[str] = None


class NextActionRecommendation(BaseModel):
    """Recommendation for what user should work on next."""
    action: str  # "Complete X" or "Generate Y"
    artifact_name: str
    priority: str  # "high", "medium", "low"
    reason: str  # Why this is recommended
    unblocks: List[str] = []  # Which downstream artifacts this unblocks


class DependencyManager:
    """
    Manages artifact dependencies and readiness assessment.

    Phase 8A WS-2 scope:
    - Dependency graph management
    - Readiness assessment (risk-proportionate)
    - Cross-artifact validation (structural only)
    - Next action recommendations
    - NO auto-generation or auto-completion (per non-goals)
    """

    def __init__(
        self,
        dependencies_path: Optional[Path] = None,
        thresholds_path: Optional[Path] = None,
        volatility_path: Optional[Path] = None
    ):
        """
        Initialize dependency manager with configuration files.

        Args:
            dependencies_path: Path to dependencies.json
            thresholds_path: Path to readiness_thresholds.json
            volatility_path: Path to artifact_volatility.json
        """
        artifacts_dir = Path(__file__).parent

        if dependencies_path is None:
            dependencies_path = artifacts_dir / "dependencies.json"
        if thresholds_path is None:
            thresholds_path = artifacts_dir / "readiness_thresholds.json"
        if volatility_path is None:
            volatility_path = artifacts_dir / "artifact_volatility.json"

        # Load configuration
        with open(dependencies_path, 'r') as f:
            dep_config = json.load(f)
            self.dependencies = dep_config["dependencies"]
            self.dependency_rationale = dep_config.get("rationale", {})

        with open(thresholds_path, 'r') as f:
            threshold_config = json.load(f)
            self.thresholds = threshold_config["risk_levels"]

        with open(volatility_path, 'r') as f:
            volatility_config = json.load(f)
            self.volatility_lookup = volatility_config["artifact_lookup"]
            self.volatility_classes = volatility_config["volatility_classes"]

        # Initialize WS-1 validator
        self.validator = ArtifactValidator()

        # Confidence limits (Dark-Matter Patch #6)
        self.confidence_limits = [
            "Readiness based on structure, not semantic quality",
            "Completion ≠ correctness",
            "Expert review required for safety-critical systems"
        ]

    def is_ready(
        self,
        validation_result: ValidationResult,
        risk_level: str,
        artifact_name: str
    ) -> bool:
        """
        Determine if an artifact meets readiness threshold for downstream use.

        Implements Principle 1 (Risk-Proportionate) and Dark-Matter Patch #1 (Volatility).

        Args:
            validation_result: WS-1 validation result
            risk_level: Risk level (R0-R3)
            artifact_name: Name of artifact (for volatility lookup)

        Returns:
            True if artifact meets readiness threshold
        """
        # Get base threshold for risk level
        threshold = self.thresholds[risk_level]
        base_completion = threshold["completion"]
        max_errors = threshold["max_errors"]
        max_warnings = threshold["max_warnings"]

        # Apply volatility modifier (Dark-Matter Patch #1)
        volatility_class = self.volatility_lookup.get(artifact_name, "foundation")
        modifier = self.volatility_classes[volatility_class]["modifier"]
        effective_completion = max(0.5, min(1.0, base_completion + modifier))

        # Check completion percentage (using WS-1 result directly per contract)
        if validation_result.completion_percent < effective_completion:
            return False

        # Count errors and warnings
        error_count = sum(1 for issue in validation_result.issues if issue.severity == "error")
        warning_count = sum(1 for issue in validation_result.issues if issue.severity == "warning")

        # Check error threshold
        if error_count > max_errors:
            return False

        # Check warning threshold (if specified)
        if max_warnings is not None and warning_count > max_warnings:
            return False

        return True

    def assess_readiness(
        self,
        artifact_name: str,
        content: str,
        risk_level: str,
        override_count: int = 0
    ) -> ReadinessAssessment:
        """
        Assess if an artifact is ready for downstream use.

        This is a WS-2 extension of WS-1 validation (per contract section 6.2).

        Args:
            artifact_name: Name of artifact
            content: Artifact content (markdown)
            risk_level: Risk level (R0-R3)
            override_count: Number of times user has overridden this dependency (Dark-Matter Patch #3)

        Returns:
            ReadinessAssessment with diagnostic information
        """
        # Step 1: Call WS-1 validation (per contract section 2.1)
        validation_result = self.validator.validate_artifact(
            artifact_name,
            content,
            risk_level
        )

        # Step 2: Check readiness using WS-1 results
        ready = self.is_ready(validation_result, risk_level, artifact_name)

        # Calculate placeholder density
        total_content_length = len(content)
        placeholder_density = (
            validation_result.placeholder_count / total_content_length
            if total_content_length > 0 else 0.0
        )

        # Determine reason if not ready
        reason = None
        blocking_issues = []

        if not ready:
            threshold = self.thresholds[risk_level]
            volatility_class = self.volatility_lookup.get(artifact_name, "foundation")
            modifier = self.volatility_classes[volatility_class]["modifier"]
            effective_completion = max(0.5, min(1.0, threshold["completion"] + modifier))

            if validation_result.completion_percent < effective_completion:
                blocking_issues.append(
                    f"Completion {validation_result.completion_percent:.0%} "
                    f"(need {effective_completion:.0%}+ for {risk_level})"
                )

            error_count = sum(1 for issue in validation_result.issues if issue.severity == "error")
            if error_count > threshold["max_errors"]:
                blocking_issues.append(
                    f"{error_count} errors found "
                    f"(max {threshold['max_errors']} allowed for {risk_level})"
                )

            warning_count = sum(1 for issue in validation_result.issues if issue.severity == "warning")
            if threshold["max_warnings"] is not None and warning_count > threshold["max_warnings"]:
                blocking_issues.append(
                    f"{warning_count} warnings found "
                    f"(max {threshold['max_warnings']} allowed for {risk_level})"
                )

            reason = "; ".join(blocking_issues) if blocking_issues else "Not ready"

        # Dark-Matter Patch #3: Override budget tracking
        override_budget = None
        if override_count > 0:
            status = "low" if override_count <= 2 else "high"
            override_budget = {
                "count": override_count,
                "status": status,
                "warning": f"Override count: {override_count} ({status}). Expect rework risk."
            }

        return ReadinessAssessment(
            artifact_name=artifact_name,
            ready=ready,
            completion=validation_result.completion_percent,
            epistemic_status="structural_only",
            confidence_limits=self.confidence_limits,
            can_proceed_anyway=True,
            placeholder_density=placeholder_density,
            readiness_basis="structural",
            reason=reason,
            blocking_issues=blocking_issues,
            override_budget=override_budget
        )

    def check_dependencies(
        self,
        artifact_name: str,
        artifacts_dir: Path,
        risk_level: str
    ) -> DependencyStatus:
        """
        Check if all dependencies for an artifact are ready.

        Implements Principle 2 (Directional Dependencies) and Principle 3 (Soft Blocking).

        Args:
            artifact_name: Name of artifact to check
            artifacts_dir: Directory containing artifact files
            risk_level: Risk level for this project

        Returns:
            DependencyStatus with diagnostic information
        """
        # Get dependencies for this artifact
        dependencies = self.dependencies.get(artifact_name, [])

        # Check each dependency
        blocking_dependencies = []

        for dep_name in dependencies:
            # Read dependency artifact
            dep_filename = self._artifact_name_to_filename(dep_name)
            dep_path = artifacts_dir / dep_filename

            if not dep_path.exists():
                # Dependency doesn't exist yet
                blocking_dependencies.append(dep_name)
                continue

            with open(dep_path, 'r') as f:
                dep_content = f.read()

            # Validate dependency
            dep_result = self.validator.validate_artifact(dep_name, dep_content, risk_level)

            # Check if ready
            if not self.is_ready(dep_result, risk_level, dep_name):
                blocking_dependencies.append(dep_name)

        # Check current artifact readiness
        artifact_filename = self._artifact_name_to_filename(artifact_name)
        artifact_path = artifacts_dir / artifact_filename

        if artifact_path.exists():
            with open(artifact_path, 'r') as f:
                artifact_content = f.read()
            readiness = self.assess_readiness(artifact_name, artifact_content, risk_level)
        else:
            # Artifact doesn't exist - create empty readiness assessment
            readiness = ReadinessAssessment(
                artifact_name=artifact_name,
                ready=False,
                completion=0.0,
                epistemic_status="structural_only",
                confidence_limits=self.confidence_limits,
                placeholder_density=0.0,
                readiness_basis="structural",
                reason="Artifact not generated yet"
            )

        # Determine suggestion (teaching-oriented language)
        suggestion = None
        if blocking_dependencies:
            if len(blocking_dependencies) == 1:
                suggestion = f"Consider completing {blocking_dependencies[0]} before generating {artifact_name}"
            else:
                dep_list = ", ".join(blocking_dependencies)
                suggestion = f"Consider completing prerequisites ({dep_list}) before generating {artifact_name}"

        return DependencyStatus(
            artifact_name=artifact_name,
            dependencies=dependencies,
            all_dependencies_ready=len(blocking_dependencies) == 0,
            blocking_dependencies=blocking_dependencies,
            readiness=readiness,
            suggestion=suggestion
        )

    def get_next_actions(
        self,
        artifacts_dir: Path,
        risk_level: str,
        required_artifacts: List[str]
    ) -> List[NextActionRecommendation]:
        """
        Recommend what user should work on next.

        Implements Principle 3 (Soft Blocking) - recommendations, not commands.

        Args:
            artifacts_dir: Directory containing artifact files
            risk_level: Risk level for this project
            required_artifacts: List of artifacts required for this risk level

        Returns:
            Ordered list of recommended actions
        """
        recommendations = []

        # Build dependency graph awareness
        artifact_status = {}
        for artifact_name in required_artifacts:
            status = self.check_dependencies(artifact_name, artifacts_dir, risk_level)
            artifact_status[artifact_name] = status

        # Find artifacts that are:
        # 1. Incomplete
        # 2. Have all dependencies ready (or no dependencies)
        # 3. Would unblock downstream artifacts

        for artifact_name in required_artifacts:
            status = artifact_status[artifact_name]

            # Skip if already complete
            if status.readiness.ready and status.readiness.completion > 0.85:
                continue

            # Check if dependencies are ready
            if not status.all_dependencies_ready:
                continue

            # Count how many downstream artifacts this would unblock
            unblocks = []
            for other_name in required_artifacts:
                other_status = artifact_status[other_name]
                if artifact_name in other_status.blocking_dependencies:
                    unblocks.append(other_name)

            # Determine priority based on:
            # - Number of downstream artifacts blocked
            # - Current completion level
            # - Artifact volatility class

            if len(unblocks) >= 3:
                priority = "high"
                reason = f"Completes {artifact_name}, unblocking {len(unblocks)} downstream artifacts"
            elif len(unblocks) >= 1:
                priority = "medium"
                reason = f"Completes {artifact_name}, unblocking {', '.join(unblocks)}"
            else:
                priority = "low"
                reason = f"Completes {artifact_name}"

            # Determine action type
            if status.readiness.completion == 0.0:
                action = f"Generate {artifact_name}"
            else:
                action = f"Complete {artifact_name}"

            recommendations.append(NextActionRecommendation(
                action=action,
                artifact_name=artifact_name,
                priority=priority,
                reason=reason,
                unblocks=unblocks
            ))

        # Sort by priority (high > medium > low)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda r: priority_order[r.priority])

        return recommendations

    def check_cross_references(
        self,
        artifacts_dir: Path,
        risk_level: str
    ) -> Dict[str, List[str]]:
        """
        Check for cross-artifact reference consistency.

        Implements Principle 4 (Structural Dependencies, Not Semantic).

        This is a WS-2-specific check (not in WS-1) per contract section 6.2.
        Checks STRUCTURE (do referenced IDs exist?), not SEMANTICS (is reference meaningful?).

        Args:
            artifacts_dir: Directory containing artifact files
            risk_level: Risk level for this project

        Returns:
            Dictionary mapping artifact names to lists of cross-reference issues
        """
        cross_ref_issues = {}

        # Extract Risk IDs from Risk Register
        risk_register_path = artifacts_dir / "QMS-Risk-Register.md"
        risk_ids = set()
        if risk_register_path.exists():
            with open(risk_register_path, 'r') as f:
                risk_content = f.read()
            risk_ids = self._extract_risk_ids(risk_content)

        # Extract CTQ IDs from CTQ Tree
        ctq_tree_path = artifacts_dir / "QMS-CTQ-Tree.md"
        ctq_ids = set()
        if ctq_tree_path.exists():
            with open(ctq_tree_path, 'r') as f:
                ctq_content = f.read()
            ctq_ids = self._extract_ctq_ids(ctq_content)

        # Check Verification Plan references
        verification_plan_path = artifacts_dir / "QMS-Verification-Plan.md"
        if verification_plan_path.exists():
            with open(verification_plan_path, 'r') as f:
                verification_content = f.read()

            # Check for risk references
            referenced_risks = self._extract_risk_references(verification_content)
            orphaned_risks = [r for r in referenced_risks if r not in risk_ids]

            if orphaned_risks:
                cross_ref_issues["Verification Plan"] = [
                    f"References {r} not found in Risk Register" for r in orphaned_risks
                ]

        # Check Traceability Index references
        traceability_path = artifacts_dir / "QMS-Traceability-Index.md"
        if traceability_path.exists():
            with open(traceability_path, 'r') as f:
                trace_content = f.read()

            # Check for risk and CTQ references
            referenced_risks = self._extract_risk_references(trace_content)
            orphaned_risks = [r for r in referenced_risks if r not in risk_ids]

            referenced_ctqs = self._extract_ctq_references(trace_content)
            orphaned_ctqs = [c for c in referenced_ctqs if c not in ctq_ids]

            issues = []
            if orphaned_risks:
                issues.extend([f"References {r} not found in Risk Register" for r in orphaned_risks])
            if orphaned_ctqs:
                issues.extend([f"References {c} not found in CTQ Tree" for c in orphaned_ctqs])

            if issues:
                cross_ref_issues["Traceability Index"] = issues

        return cross_ref_issues

    def _artifact_name_to_filename(self, artifact_name: str) -> str:
        """Convert artifact name to filename."""
        return f"QMS-{artifact_name.replace(' ', '-')}.md"

    def _extract_risk_ids(self, content: str) -> set:
        """Extract risk IDs from content (e.g., R-001, RISK-001)."""
        pattern = r'(?:Risk[- ])?([A-Z]-?\d{3})'
        matches = re.findall(pattern, content, re.IGNORECASE)
        return set(m.upper() for m in matches)

    def _extract_ctq_ids(self, content: str) -> set:
        """Extract CTQ IDs from content (e.g., CTQ-001, CTQ-1)."""
        pattern = r'CTQ-?\d+'
        matches = re.findall(pattern, content, re.IGNORECASE)
        return set(m.upper() for m in matches)

    def _extract_risk_references(self, content: str) -> set:
        """Extract risk ID references from content."""
        return self._extract_risk_ids(content)

    def _extract_ctq_references(self, content: str) -> set:
        """Extract CTQ ID references from content."""
        return self._extract_ctq_ids(content)
