"""
Layer 5: Expert Review Triggers

Determine when expert review is required or recommended.
Implements ER1-ER5 from intake-safety-mechanisms.md.
"""

from models.intake import IntakeAnswers, RiskClassification, ValidationWarning


def determine_expert_review(
    answers: IntakeAnswers,
    classification: RiskClassification,
    all_warnings: list[ValidationWarning],
) -> tuple[bool, bool, list[str]]:
    """
    Determine if expert review is required or recommended.

    Returns:
        (required: bool, recommended: bool, reasons: list[str])
    """
    required = False
    recommended = False
    reasons: list[str] = []

    # ER1: High-Risk Indicators Present
    er1_result = _er1_high_risk_indicators(all_warnings)
    if er1_result["required"]:
        required = True
        reasons.append(er1_result["reason"])
    elif er1_result["recommended"]:
        recommended = True
        reasons.append(er1_result["reason"])

    # ER2: Contradictory Answers
    er2_result = _er2_contradictory_answers(all_warnings)
    if er2_result["required"]:
        required = True
        reasons.append(er2_result["reason"])
    elif er2_result["recommended"]:
        recommended = True
        reasons.append(er2_result["reason"])

    # ER3: Edge Case Classification
    er3_result = _er3_edge_case_classification(classification)
    if er3_result["recommended"]:
        recommended = True
        reasons.append(er3_result["reason"])

    # ER5: Safety/Legal + Mitigations
    er5_result = _er5_safety_legal_with_mitigations(answers, classification)
    if er5_result["recommended"]:
        recommended = True
        reasons.append(er5_result["reason"])

    return required, recommended, reasons


def _er1_high_risk_indicators(
    all_warnings: list[ValidationWarning]
) -> dict[str, bool | str]:
    """
    ER1: High-Risk Indicators Present

    Condition:
    - 2+ CRITICAL warnings OR
    - 3+ WARNING warnings
    """
    critical_count = sum(1 for w in all_warnings if w.severity == "CRITICAL")
    warning_count = sum(1 for w in all_warnings if w.severity == "WARNING")

    if critical_count >= 2:
        return {
            "required": True,
            "recommended": False,
            "reason": f"Multiple high-risk indicators detected ({critical_count} critical warnings)",
        }

    if warning_count >= 3:
        return {
            "required": False,
            "recommended": True,
            "reason": f"Multiple risk indicators detected ({warning_count} warnings)",
        }

    return {"required": False, "recommended": False, "reason": ""}


def _er2_contradictory_answers(
    all_warnings: list[ValidationWarning]
) -> dict[str, bool | str]:
    """
    ER2: Contradictory Answers

    Condition: Any cross-validation warning (CV1, CV2, CV4)
    """
    contradiction_layers = {"CV1", "CV2", "CV4"}

    contradictions = [w for w in all_warnings if w.layer in contradiction_layers]

    if contradictions:
        return {
            "required": False,
            "recommended": True,
            "reason": f"Contradictory answers detected ({len(contradictions)} contradictions)",
        }

    return {"required": False, "recommended": False, "reason": ""}


def _er3_edge_case_classification(
    classification: RiskClassification
) -> dict[str, bool | str]:
    """
    ER3: Edge Case Classification

    Condition: Borderline R2/R3 classification
    """
    if classification.borderline:
        return {
            "required": False,
            "recommended": True,
            "reason": "Borderline classification detected - expert confirmation recommended",
        }

    return {"required": False, "recommended": False, "reason": ""}


def _er5_safety_legal_with_mitigations(
    answers: IntakeAnswers, classification: RiskClassification
) -> dict[str, bool | str]:
    """
    ER5: Safety/Legal + Mitigations

    Condition:
    - Q3 = "Safety_Legal_Compliance" AND
    - Mitigating factors present (Q4=Easy, Q1=Internal, Q6=Individual)
    """
    if answers.q3_worst_failure != "Safety_Legal_Compliance":
        return {"required": False, "recommended": False, "reason": ""}

    # Check for mitigating factors
    has_mitigations = (
        answers.q4_reversibility == "Easy"
        or answers.q1_users == "Internal"
        or answers.q6_scale == "Individual"
    )

    if has_mitigations and classification.risk_level == "R2":
        return {
            "required": False,
            "recommended": True,
            "reason": "Safety/legal consequences with mitigating factors - confirm R2 vs R3 appropriate",
        }

    return {"required": False, "recommended": False, "reason": ""}
