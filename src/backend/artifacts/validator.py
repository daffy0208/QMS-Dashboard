"""
Artifact Validator - Phase 8A WS-1.2
Validates artifacts against acceptance criteria for completeness and quality.

Design Principles:
- Deterministic validation (no AI, no magic)
- Placeholder detection (TBD, [Name], etc.)
- Section presence checking
- Field completeness (Risk Register structured data)
- NO cross-artifact validation (deferred to WS-2)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel


class ValidationIssue(BaseModel):
    """A single validation issue found in an artifact."""
    severity: str  # "error" or "warning"
    section: Optional[str]  # Which section has the issue (if applicable)
    message: str  # Human-readable description
    suggestion: Optional[str] = None  # How to fix it


class ValidationResult(BaseModel):
    """Result of validating a single artifact."""
    artifact_name: str
    risk_level: str
    valid: bool  # True if meets all acceptance criteria
    completion_percent: float  # 0.0 to 1.0
    issues: List[ValidationIssue]
    missing_sections: List[str]
    placeholder_count: int


class ArtifactValidator:
    """
    Validates artifacts against acceptance criteria.

    Phase 8A scope:
    - R0-R3 validation (all risk levels)
    - All 11 artifacts covered
    - Placeholder detection
    - Section presence
    - Risk-specific validation (Risk Register, CTQ Tree, Measurement Plan, etc.)
    - NO cross-artifact validation (deferred to WS-2)
    """

    def __init__(self, criteria_path: Optional[Path] = None):
        """
        Initialize validator with acceptance criteria.

        Args:
            criteria_path: Path to acceptance_criteria.json (defaults to same directory)
        """
        if criteria_path is None:
            criteria_path = Path(__file__).parent / "acceptance_criteria.json"

        with open(criteria_path, 'r') as f:
            self.criteria = json.load(f)

        # Placeholder patterns to detect
        self.placeholder_patterns = [
            r'\[Name\]',
            r'\[Description\]',
            r'\[.*?\]',  # Any [bracketed text]
            r'TBD',
            r'To be determined',
            r'TODO',
            r'FIXME',
            r'XXX',
            r'<placeholder>',
            r'\{.*?\}',  # Any {braced text} that looks like a placeholder
        ]

        self.placeholder_regex = re.compile(
            '|'.join(self.placeholder_patterns),
            re.IGNORECASE
        )

    def validate_artifact(
        self,
        artifact_name: str,
        content: str,
        risk_level: str
    ) -> ValidationResult:
        """
        Validate an artifact against acceptance criteria.

        Args:
            artifact_name: Name of artifact (e.g., "Quality Plan")
            content: Full markdown content of artifact
            risk_level: Risk level (R0, R1, R2, R3)

        Returns:
            ValidationResult with validation details
        """
        # Check if artifact has acceptance criteria defined
        if artifact_name not in self.criteria["artifacts"]:
            # No criteria defined - consider valid for now (R0/R1)
            return ValidationResult(
                artifact_name=artifact_name,
                risk_level=risk_level,
                valid=True,
                completion_percent=1.0,
                issues=[],
                missing_sections=[],
                placeholder_count=0
            )

        artifact_criteria = self.criteria["artifacts"][artifact_name]

        # Check if risk level has criteria
        if risk_level not in artifact_criteria.get("risk_levels", {}):
            # Risk level not covered (likely R0/R1) - consider valid
            return ValidationResult(
                artifact_name=artifact_name,
                risk_level=risk_level,
                valid=True,
                completion_percent=1.0,
                issues=[],
                missing_sections=[],
                placeholder_count=0
            )

        risk_criteria = artifact_criteria["risk_levels"][risk_level]
        issues: List[ValidationIssue] = []

        # WS-1.7: Check if warning-only mode (R0/R1 teaching-oriented validation)
        warning_only = risk_criteria.get("rules", {}).get("warning_only", False)

        # 1. Check for placeholders
        rules = risk_criteria.get("rules", {})

        # WS-1.7: Always count placeholders (for informational purposes)
        placeholder_count = len(self.placeholder_regex.findall(content))

        # WS-1.7: Check placeholders (handle both placeholders_not_allowed and placeholders_allowed)
        placeholders_not_allowed = rules.get("placeholders_not_allowed", False)
        placeholders_allowed = rules.get("placeholders_allowed", False)

        # If placeholders explicitly NOT allowed, raise an issue
        if placeholders_not_allowed and not placeholders_allowed:
            if placeholder_count > 0:
                severity = "warning" if warning_only else "error"
                issues.append(ValidationIssue(
                    severity=severity,
                    section=None,
                    message=f"Found {placeholder_count} placeholder(s) that must be filled in",
                    suggestion="Replace all [bracketed], TBD, and TODO placeholders with actual content"
                ))

        # 2. Check for required sections
        missing_sections = []
        if "required_sections" in risk_criteria:
            for section in risk_criteria["required_sections"]:
                if not self._section_exists(content, section):
                    missing_sections.append(section)
                    severity = "warning" if warning_only else "error"
                    issues.append(ValidationIssue(
                        severity=severity,
                        section=section,
                        message=f"Required section '{section}' is missing or empty",
                        suggestion=f"Add a '{section}' section with appropriate content"
                    ))

        # 3. Check minimum sections present (if specified)
        min_sections = risk_criteria.get("rules", {}).get("min_sections_present")
        if min_sections:
            section_count = self._count_sections(content)
            if section_count < min_sections:
                severity = "warning" if warning_only else "error"
                issues.append(ValidationIssue(
                    severity=severity,
                    section=None,
                    message=f"Expected at least {min_sections} sections, found {section_count}",
                    suggestion="Add more detailed sections to meet minimum requirements"
                ))

        # 4. Artifact-specific validation (WS-1.9.1)
        if artifact_name == "Risk Register":
            risk_issues = self._validate_risk_register(content, risk_criteria, warning_only)
            issues.extend(risk_issues)

        # WS-1.9.1: New artifact-specific validations
        # Check for rules that apply to this artifact
        if "min_content_length" in rules:
            min_length_issues = self._validate_min_content_length(content, rules, warning_only)
            issues.extend(min_length_issues)

        if "min_items" in rules:
            min_items_issues = self._validate_min_items(content, risk_criteria, warning_only)
            issues.extend(min_items_issues)

        if "min_metrics" in rules:
            min_metrics_issues = self._validate_min_metrics(content, rules, warning_only)
            issues.extend(min_metrics_issues)

        if "min_assumptions" in rules:
            min_assumptions_issues = self._validate_min_assumptions(content, rules, warning_only)
            issues.extend(min_assumptions_issues)

        if "min_entries" in rules:
            min_entries_issues = self._validate_min_entries(content, rules, warning_only)
            issues.extend(min_entries_issues)

        if "has_header" in rules:
            header_issues = self._validate_has_header(content, warning_only)
            issues.extend(header_issues)

        if "has_structure" in rules:
            structure_issues = self._validate_has_structure(content, warning_only)
            issues.extend(structure_issues)

        # Calculate completion percentage
        completion_percent = self._calculate_completion(
            issues=issues,
            placeholder_count=placeholder_count,
            missing_sections=missing_sections,
            risk_criteria=risk_criteria
        )

        # Determine if valid (no errors)
        valid = all(issue.severity != "error" for issue in issues)

        return ValidationResult(
            artifact_name=artifact_name,
            risk_level=risk_level,
            valid=valid,
            completion_percent=completion_percent,
            issues=issues,
            missing_sections=missing_sections,
            placeholder_count=placeholder_count
        )

    def _section_exists(self, content: str, section_name: str) -> bool:
        """
        Check if a section exists and has content.

        Looks for markdown headers like:
        ## Section Name
        ### Section Name
        """
        # Match section headers (## or ###)
        pattern = rf'^##+ +{re.escape(section_name)}\s*$'

        # Find the section
        lines = content.split('\n')
        section_found = False
        section_content = []

        for i, line in enumerate(lines):
            if re.match(pattern, line, re.IGNORECASE):
                section_found = True
                # Collect content until next section or end
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('#'):
                        break
                    section_content.append(lines[j])
                break

        if not section_found:
            return False

        # Check if section has actual content (not just whitespace)
        content_text = '\n'.join(section_content).strip()
        return len(content_text) > 0

    def _count_sections(self, content: str) -> int:
        """Count the number of sections (## headers) in the artifact."""
        return len(re.findall(r'^##+ ', content, re.MULTILINE))

    def _validate_risk_register(
        self,
        content: str,
        risk_criteria: Dict,
        warning_only: bool = False
    ) -> List[ValidationIssue]:
        """
        Validate Risk Register structure.

        Checks:
        - Minimum number of risks
        - Required fields per risk
        """
        issues = []
        rules = risk_criteria.get("rules", {})

        # Extract risks (look for risk IDs like R-001, RISK-001, etc.)
        risk_pattern = r'(?:^|\n)(?:#{1,6}\s+)?(?:Risk[- ])?([A-Z]-?\d{3})'
        risks_found = re.findall(risk_pattern, content, re.IGNORECASE | re.MULTILINE)
        num_risks = len(set(risks_found))  # Deduplicate

        # Check minimum risks
        min_risks = rules.get("min_risks", 0)
        if num_risks < min_risks:
            severity = "warning" if warning_only else "error"
            issues.append(ValidationIssue(
                severity=severity,
                section="Risks",
                message=f"Expected at least {min_risks} risks, found {num_risks}",
                suggestion=f"Add {min_risks - num_risks} more risk(s) to meet requirements"
            ))

        # Check required fields
        required_fields = rules.get("required_fields", [])
        if required_fields and num_risks > 0:
            # Simple heuristic: check if field names appear in content
            missing_fields = []
            for field in required_fields:
                # Look for field name as a header or bold text
                field_patterns = [
                    rf'\*\*{re.escape(field)}\*\*',  # **field**
                    rf'#{1,6}\s+{re.escape(field)}',  # # field
                    rf'{re.escape(field)}:',  # field:
                ]
                found = any(
                    re.search(pattern, content, re.IGNORECASE)
                    for pattern in field_patterns
                )
                if not found:
                    missing_fields.append(field)

            if missing_fields:
                issues.append(ValidationIssue(
                    severity="warning",
                    section="Risk Fields",
                    message=f"Some risks may be missing fields: {', '.join(missing_fields)}",
                    suggestion="Ensure all risks include: " + ", ".join(required_fields)
                ))

        return issues

    def _validate_min_content_length(
        self,
        content: str,
        rules: Dict,
        warning_only: bool = False
    ) -> List[ValidationIssue]:
        """WS-1.9.1: Validate minimum content length (lightweight check)."""
        issues = []
        min_length = rules.get("min_content_length", 0)

        # Strip markdown headers and count actual content
        content_clean = re.sub(r'^#+ .*$', '', content, flags=re.MULTILINE)
        content_clean = content_clean.strip()
        actual_length = len(content_clean)

        if actual_length < min_length:
            severity = "warning" if warning_only else "error"
            issues.append(ValidationIssue(
                severity=severity,
                section=None,
                message=f"Content too short: {actual_length} characters (minimum {min_length})",
                suggestion="Add more detailed content to meet minimum length requirement"
            ))

        return issues

    def _validate_min_items(
        self,
        content: str,
        risk_criteria: Dict,
        warning_only: bool = False
    ) -> List[ValidationIssue]:
        """WS-1.9.1: Validate minimum items in sections (for CTQ Tree)."""
        issues = []
        rules = risk_criteria.get("rules", {})
        min_items = rules.get("min_items", 0)

        # Count list items (- or *) and numbered items
        list_items = len(re.findall(r'^[\s]*[-*]\s+\w', content, re.MULTILINE))
        numbered_items = len(re.findall(r'^[\s]*\d+\.\s+\w', content, re.MULTILINE))
        total_items = list_items + numbered_items

        if total_items < min_items:
            severity = "warning" if warning_only else "error"
            issues.append(ValidationIssue(
                severity=severity,
                section=None,
                message=f"Expected at least {min_items} items, found {total_items}",
                suggestion=f"Add {min_items - total_items} more item(s) to meet requirements"
            ))

        return issues

    def _validate_min_metrics(
        self,
        content: str,
        rules: Dict,
        warning_only: bool = False
    ) -> List[ValidationIssue]:
        """WS-1.9.1: Validate minimum metrics (for Measurement Plan)."""
        issues = []
        min_metrics = rules.get("min_metrics", 0)

        # Count metric definitions (look for patterns like "Metric:", "**Metric**:", etc.)
        metric_patterns = [
            r'\*\*.*?Metric.*?\*\*:',  # **Some Metric**:
            r'Metric \d+:',  # Metric 1:
            r'^\s*-\s+.*?:.*?(target|baseline|threshold)',  # List items with targets
        ]

        metrics_found = sum(
            len(re.findall(pattern, content, re.IGNORECASE | re.MULTILINE))
            for pattern in metric_patterns
        )

        if metrics_found < min_metrics:
            severity = "warning" if warning_only else "error"
            issues.append(ValidationIssue(
                severity=severity,
                section="Key Metrics",
                message=f"Expected at least {min_metrics} metrics, found {metrics_found}",
                suggestion=f"Add {min_metrics - metrics_found} more metric(s) with targets/baselines"
            ))

        return issues

    def _validate_min_assumptions(
        self,
        content: str,
        rules: Dict,
        warning_only: bool = False
    ) -> List[ValidationIssue]:
        """WS-1.9.1: Validate minimum assumptions (for Assumptions Register)."""
        issues = []
        min_assumptions = rules.get("min_assumptions", 0)

        # Count assumption entries (look for numbered or bulleted assumptions)
        assumption_pattern = r'(?:^|\n)(?:[\s]*(?:[-*]|\d+\.)\s+)(?:Assumption|ASS-\d+|A-\d+)'
        assumptions_found = len(re.findall(assumption_pattern, content, re.IGNORECASE | re.MULTILINE))

        # Also count table rows under assumptions section
        if assumptions_found == 0:
            # Alternative: count list items in critical assumptions section
            assumptions_found = len(re.findall(r'^[\s]*[-*]\s+\w', content, re.MULTILINE))

        if assumptions_found < min_assumptions:
            severity = "warning" if warning_only else "error"
            issues.append(ValidationIssue(
                severity=severity,
                section="Critical Assumptions",
                message=f"Expected at least {min_assumptions} assumptions, found {assumptions_found}",
                suggestion=f"Add {min_assumptions - assumptions_found} more assumption(s)"
            ))

        return issues

    def _validate_min_entries(
        self,
        content: str,
        rules: Dict,
        warning_only: bool = False
    ) -> List[ValidationIssue]:
        """WS-1.9.1: Validate minimum entries (for Traceability Index, logs)."""
        issues = []
        min_entries = rules.get("min_entries", 0)

        # Count table rows (look for | separators) or list items
        table_rows = len(re.findall(r'^\|.*?\|.*?\|', content, re.MULTILINE))
        list_items = len(re.findall(r'^[\s]*[-*]\s+\w', content, re.MULTILINE))
        entries_found = max(table_rows - 1, list_items)  # -1 for header row

        if entries_found < min_entries:
            severity = "warning" if warning_only else "error"
            issues.append(ValidationIssue(
                severity=severity,
                section=None,
                message=f"Expected at least {min_entries} entries, found {entries_found}",
                suggestion=f"Add {min_entries - entries_found} more entry(ies)"
            ))

        return issues

    def _validate_has_header(
        self,
        content: str,
        warning_only: bool = False
    ) -> List[ValidationIssue]:
        """WS-1.9.1: Validate artifact has proper header structure."""
        issues = []

        # Check for title (# header) at top
        has_title = bool(re.match(r'^#\s+\w', content, re.MULTILINE))

        # Check for project name subtitle (## header)
        has_project = bool(re.search(r'^##\s+\w', content, re.MULTILINE))

        if not (has_title and has_project):
            severity = "warning" if warning_only else "error"
            issues.append(ValidationIssue(
                severity=severity,
                section=None,
                message="Missing proper header structure (title + project name)",
                suggestion="Add '# Title' and '## Project Name' headers at top"
            ))

        return issues

    def _validate_has_structure(
        self,
        content: str,
        warning_only: bool = False
    ) -> List[ValidationIssue]:
        """WS-1.9.1: Validate artifact has proper structure (sections/table/list)."""
        issues = []

        # Check for at least one section header (## or ###)
        has_sections = bool(re.search(r'^##+ ', content, re.MULTILINE))

        # Check for table or list structure
        has_table = bool(re.search(r'^\|.*?\|', content, re.MULTILINE))
        has_list = bool(re.search(r'^[\s]*[-*]\s+\w', content, re.MULTILINE))

        if not (has_sections and (has_table or has_list)):
            severity = "warning" if warning_only else "error"
            issues.append(ValidationIssue(
                severity=severity,
                section=None,
                message="Missing proper structure (sections + table/list)",
                suggestion="Add section headers and organize content in table or list format"
            ))

        return issues

    def _calculate_completion(
        self,
        issues: List[ValidationIssue],
        placeholder_count: int,
        missing_sections: List[str],
        risk_criteria: Dict
    ) -> float:
        """
        Calculate artifact completion percentage.

        Formula:
        - Start at 100%
        - Subtract 10% per missing required section
        - Subtract 5% per placeholder
        - Subtract 20% per error issue (non-section, non-placeholder)
        - Minimum 0%, maximum 100%
        """
        completion = 1.0

        # Penalize missing sections
        num_required_sections = len(risk_criteria.get("required_sections", []))
        if num_required_sections > 0:
            section_penalty = len(missing_sections) / num_required_sections * 0.5
            completion -= section_penalty

        # Penalize placeholders (up to 20% total)
        if placeholder_count > 0:
            placeholder_penalty = min(placeholder_count * 0.05, 0.2)
            completion -= placeholder_penalty

        # Penalize other errors
        other_errors = [
            issue for issue in issues
            if issue.severity == "error" and issue.section not in missing_sections
        ]
        completion -= len(other_errors) * 0.1

        # Clamp to [0, 1]
        return max(0.0, min(1.0, completion))


def validate_artifact_file(
    artifact_path: Path,
    artifact_name: str,
    risk_level: str
) -> ValidationResult:
    """
    Convenience function to validate an artifact from a file.

    Args:
        artifact_path: Path to artifact markdown file
        artifact_name: Name of artifact
        risk_level: Risk level (R0-R3)

    Returns:
        ValidationResult
    """
    validator = ArtifactValidator()

    with open(artifact_path, 'r') as f:
        content = f.read()

    return validator.validate_artifact(artifact_name, content, risk_level)


def validate_project_artifacts(
    artifacts_dir: Path,
    risk_level: str
) -> Dict[str, ValidationResult]:
    """
    Validate all artifacts in a project directory.

    Args:
        artifacts_dir: Directory containing QMS-*.md files
        risk_level: Risk level for this project

    Returns:
        Dictionary mapping artifact names to ValidationResults
    """
    validator = ArtifactValidator()
    results = {}

    # Map filename patterns to artifact names
    artifact_mapping = {
        "QMS-Quality-Plan.md": "Quality Plan",
        "QMS-Risk-Register.md": "Risk Register",
        "QMS-Verification-Plan.md": "Verification Plan",
        "QMS-Control-Plan.md": "Control Plan",
    }

    for filename, artifact_name in artifact_mapping.items():
        artifact_path = artifacts_dir / filename
        if artifact_path.exists():
            result = validate_artifact_file(artifact_path, artifact_name, risk_level)
            results[artifact_name] = result

    return results
