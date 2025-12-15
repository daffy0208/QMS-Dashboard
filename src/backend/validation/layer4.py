"""
Layer 4: Warnings & Confirmations

Generate warnings that require user acknowledgment before proceeding.
Implements W1-W3 from intake-safety-mechanisms.md.
"""

from models.intake import IntakeAnswers, RiskClassification, ValidationWarning


def generate_confirmation_warnings(
    answers: IntakeAnswers, classification: RiskClassification
) -> list[ValidationWarning]:
    """
    Generate warnings that require explicit user confirmation.
    These are more severe than informational warnings.
    """
    warnings: list[ValidationWarning] = []

    warnings.extend(_w1_r3_classification_confirmation(classification))
    warnings.extend(_w2_r0_classification_with_caveats(answers, classification))
    # W3 (downgrade prevention) is handled in API layer, not here

    return warnings


def _w1_r3_classification_confirmation(
    classification: RiskClassification
) -> list[ValidationWarning]:
    """
    W1: R3 Classification Confirmation

    Trigger: classification.risk_level = "R3"

    R3 is the highest risk level and requires the most comprehensive
    quality management. User must explicitly confirm understanding.
    """
    if classification.risk_level != "R3":
        return []

    return [
        ValidationWarning(
            severity="CRITICAL",
            layer="W1",
            message="R3 CLASSIFICATION - STRICT RIGOR MODE: This is the highest risk level requiring 11 mandatory quality artifacts, full V&V, and no downgrades without deviation approval",
            recommendation="Confirm you understand R3 requirements before proceeding. Expert review recommended.",
        )
    ]


def _w2_r0_classification_with_caveats(
    answers: IntakeAnswers, classification: RiskClassification
) -> list[ValidationWarning]:
    """
    W2: R0 Classification with Caveats

    Trigger: classification.risk_level = "R0" BUT any of:
    - Q3 != "Annoyance"
    - Q6 != "Individual"
    - Q7 != "No"

    R0 is the lowest risk level. If any answers suggest higher risk,
    warn the user before confirming R0.
    """
    if classification.risk_level != "R0":
        return []

    caveats = []

    if answers.q3_worst_failure != "Annoyance":
        caveats.append(f"Worst failure: {answers.q3_worst_failure} (not just Annoyance)")

    if answers.q6_scale != "Individual":
        caveats.append(f"Scale: {answers.q6_scale} (not just Individual)")

    if answers.q7_regulated != "No":
        caveats.append(f"Regulated: {answers.q7_regulated} (not No)")

    if not caveats:
        return []

    caveat_text = "; ".join(caveats)

    return [
        ValidationWarning(
            severity="WARNING",
            layer="W2",
            message=f"R0 CLASSIFICATION - ADVISORY RIGOR ONLY: Note unusual factors: {caveat_text}",
            recommendation="R0 is minimal rigor. Per intake rules: 'If uncertain, select higher risk.' Consider R1 if unsure.",
        )
    ]


def check_downgrade_attempt(
    current_risk: str, requested_risk: str
) -> ValidationWarning | None:
    """
    W3: Downgrade from Strict Rigor

    This is called separately from the main validation flow
    when a user attempts to override classification.

    Returns warning if downgrade from R2/R3 to R0/R1 is attempted.
    """
    risk_levels = {"R0": 0, "R1": 1, "R2": 2, "R3": 3}

    current_level = risk_levels.get(current_risk, 0)
    requested_level = risk_levels.get(requested_risk, 0)

    # Not a downgrade
    if requested_level >= current_level:
        return None

    # Downgrade from R2 or R3 (strict rigor)
    if current_level >= 2:
        return ValidationWarning(
            severity="CRITICAL",
            layer="W3",
            message=f"RIGOR DOWNGRADE REQUIRES DEVIATION: Attempting {current_risk} → {requested_risk}",
            recommendation="Per intake-rules.md: Any downgrade requires deviation record with justification and approval.",
        )

    # Downgrade from R1 to R0 (less critical but still needs review)
    return ValidationWarning(
        severity="WARNING",
        layer="W3",
        message=f"Risk downgrade: {current_risk} → {requested_risk}",
        recommendation="Document justification for downgrade. Consider if you're accepting additional risk.",
    )
