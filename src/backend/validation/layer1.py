"""
Layer 1: Input Validation

Ensures all required fields are present and sane.
NO classification decisions happen here.
"""

from models.intake import IntakeAnswers, ValidationWarning


def validate_intake_answers(answers: IntakeAnswers) -> list[ValidationWarning]:
    warnings: list[ValidationWarning] = []

    # Automated actions sanity check
    if answers.q2_influence == "Automated":
        if not (
            answers.q4_reversibility == "Easy"
            and answers.q3_worst_failure == "Annoyance"
        ):
            warnings.append(ValidationWarning(
                severity="INFO",
                layer="Layer1",
                message="Automated actions detected",
                recommendation="Ensure monitoring and safeguards exist",
            ))

    # Contradiction: minor failure but hard to reverse
    if (
        answers.q3_worst_failure == "Annoyance"
        and answers.q4_reversibility == "Hard"
    ):
        warnings.append(ValidationWarning(
            severity="WARNING",
            layer="Layer1",
            message="Minor failure but hard to reverse is unusual",
            recommendation="Re-check reversibility assumption",
        ))

    # Scale vs users consistency
    if (
        answers.q1_users == "Internal"
        and answers.q6_scale == "Organization_Public"
    ):
        warnings.append(ValidationWarning(
            severity="INFO",
            layer="Layer1",
            message="Internal users at organization-wide scale",
            recommendation="Confirm scope is correct",
        ))

    return warnings


def validate_project_name(project_name: str) -> list[ValidationWarning]:
    warnings: list[ValidationWarning] = []

    if not project_name or not project_name.strip():
        warnings.append(ValidationWarning(
            severity="WARNING",
            layer="Layer1",
            message="Project name is empty",
            recommendation="Provide a descriptive name",
        ))
    elif project_name.lower() in ["test", "untitled", "unnamed"]:
        warnings.append(ValidationWarning(
            severity="INFO",
            layer="Layer1",
            message="Generic project name detected",
            recommendation="Consider a more specific name",
        ))

    return warnings
