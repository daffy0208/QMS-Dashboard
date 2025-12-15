"""
Risk classification engine for QMS Dashboard.

Implements classification logic from intake-rules.md.
Phase 1 COMPLETE — Phase 2 will extend via layered validation, not by changing this file.
"""

from models.intake import (
    IntakeAnswers,
    RiskClassification,
    ValidationWarning
)


def classify_risk(
    answers: IntakeAnswers
) -> tuple[RiskClassification, list[ValidationWarning]]:
    """
    Classify risk level based on intake answers.

    Returns:
        (RiskClassification, list[ValidationWarning])

    IMPORTANT:
    - This function MUST remain deterministic.
    - Phase 2+ validation layers MAY ADD WARNINGS
      but MUST NOT override classification silently.
    """

    warnings: list[ValidationWarning] = []

    # --- R3 (highest priority) ---
    if _is_r3(answers):
        classification = _build_r3_classification(answers)
        warnings.extend(_check_r3_warnings(answers))
        return classification, warnings

    # --- R2 ---
    if _is_r2(answers):
        classification = _build_r2_classification(answers)
        warnings.extend(_check_r2_warnings(answers))
        return classification, warnings

    # --- R1 ---
    if _is_r1(answers):
        classification = _build_r1_classification(answers)
        warnings.extend(_check_r1_warnings(answers))
        return classification, warnings

    # --- R0 ---
    classification = _build_r0_classification()
    warnings.extend(_check_r0_warnings(answers))
    return classification, warnings


def get_required_artifacts(risk_level: str) -> list[str]:
    """
    Get list of required QMS artifacts for a given risk level.

    Per intake-rules.md:
    - R0: 5 base artifacts
    - R1: 8 artifacts (base + verification/validation/measurement)
    - R2/R3: 11 artifacts (R1 + control/change/CAPA)

    Args:
        risk_level: Risk level string ("R0", "R1", "R2", "R3")

    Returns:
        List of artifact names
    """
    base_artifacts = [
        "Quality Plan",
        "CTQ Tree",
        "Assumptions Register",
        "Risk Register",
        "Traceability Index"
    ]

    r1_additional = [
        "Verification Plan",
        "Validation Plan",
        "Measurement Plan"
    ]

    r2_additional = [
        "Control Plan",
        "Change Log",
        "CAPA Log"
    ]

    if risk_level == "R0":
        return base_artifacts
    elif risk_level == "R1":
        return base_artifacts + r1_additional
    elif risk_level in ["R2", "R3"]:
        return base_artifacts + r1_additional + r2_additional
    else:
        raise ValueError(f"Invalid risk level: {risk_level}")


# ======================
# RISK DETERMINATION
# ======================

def _is_r3(answers: IntakeAnswers) -> bool:
    # Safety / legal / compliance worst case
    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        mitigated = (
            answers.q4_reversibility == "Easy"
            and answers.q1_users == "Internal"
            and answers.q7_regulated == "No"
        )
        return not mitigated

    # Automated financial or irreversible systems
    if answers.q3_worst_failure == "Financial":
        if answers.q2_influence == "Automated":
            return True
        if answers.q4_reversibility == "Hard":
            return True

    # Automated + hard/partial reversibility
    if answers.q2_influence == "Automated":
        if answers.q4_reversibility in ["Hard", "Partial"]:
            if answers.q3_worst_failure in ["Financial", "Reputational"]:
                return True

    # Regulated systems with meaningful impact
    if answers.q7_regulated == "Yes":
        if answers.q2_influence != "Informational":
            return True

    return False


def _is_r2(answers: IntakeAnswers) -> bool:
    if answers.q1_users in ["External", "Public"]:
        return True

    if answers.q2_influence == "Recommendations":
        if answers.q3_worst_failure in [
            "Financial",
            "Reputational",
            "Safety_Legal_Compliance",
        ]:
            return True

    if answers.q7_regulated in ["Possibly", "Yes"]:
        return True

    if answers.q6_scale == "Organization_Public":
        if answers.q3_worst_failure != "Annoyance":
            return True

    if answers.q4_reversibility == "Partial":
        if answers.q3_worst_failure in ["Financial", "Reputational"]:
            return True

    return False


def _is_r1(answers: IntakeAnswers) -> bool:
    if answers.q1_users != "Internal":
        return False

    if answers.q6_scale in ["Multi_team", "Organization_Public"]:
        return True

    if answers.q2_influence in ["Informational", "Recommendations"]:
        if answers.q3_worst_failure in ["Financial", "Reputational"]:
            return True

    if answers.q2_influence == "Automated":
        if answers.q4_reversibility == "Easy":
            return True

    return False


# ======================
# CLASSIFICATION BUILDERS
# ======================

def _build_r3_classification(answers: IntakeAnswers) -> RiskClassification:
    reasons = []

    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        reasons.append("Safety / legal / compliance impact")

    if answers.q2_influence == "Automated":
        reasons.append("Automated actions")

    if answers.q4_reversibility == "Hard":
        reasons.append("Hard to reverse consequences")

    rationale = "R3 due to: " + "; ".join(reasons)

    return RiskClassification(
        risk_level="R3",
        rigor="Maximum",
        rationale=rationale,
        borderline=False,
    )


def _build_r2_classification(answers: IntakeAnswers) -> RiskClassification:
    reasons = []
    borderline = False

    if answers.q1_users in ["External", "Public"]:
        reasons.append("External or public users")

    if answers.q2_influence == "Recommendations":
        reasons.append("Decision-impacting recommendations")

    if answers.q7_regulated != "No":
        reasons.append("Regulatory exposure")

    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        borderline = True
        reasons.append("Safety / legal risk with mitigating factors")

    return RiskClassification(
        risk_level="R2",
        rigor="Strict",
        rationale="R2 due to: " + "; ".join(reasons),
        borderline=borderline,
    )


def _build_r1_classification(answers: IntakeAnswers) -> RiskClassification:
    reasons = []

    if answers.q6_scale in ["Multi_team", "Organization_Public"]:
        reasons.append("Multi-team scale")

    if answers.q3_worst_failure in ["Financial", "Reputational"]:
        reasons.append("Moderate impact")

    return RiskClassification(
        risk_level="R1",
        rigor="Moderate",
        rationale="R1 due to: " + "; ".join(reasons),
        borderline=False,
    )


def _build_r0_classification() -> RiskClassification:
    return RiskClassification(
        risk_level="R0",
        rigor="Minimal",
        rationale="Internal, low impact, fully reversible",
        borderline=False,
    )


# ======================
# WARNINGS
# ======================

def _check_r3_warnings(answers: IntakeAnswers) -> list[ValidationWarning]:
    warnings = []

    if answers.q5_domain != "Yes":
        warnings.append(ValidationWarning(
            severity="CRITICAL",
            layer="I4",
            message="R3 system with incomplete domain understanding",
            recommendation="Mandatory expert review required",
        ))

    return warnings


def _check_r2_warnings(answers: IntakeAnswers) -> list[ValidationWarning]:
    warnings = []

    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        warnings.append(ValidationWarning(
            severity="WARNING",
            layer="I1",
            message="Safety / legal risk detected (borderline R3)",
            recommendation="Expert review strongly recommended",
        ))

    return warnings


def _check_r1_warnings(answers: IntakeAnswers) -> list[ValidationWarning]:
    warnings = []

    if answers.q5_domain == "No":
        warnings.append(ValidationWarning(
            severity="INFO",
            layer="I4",
            message="Unfamiliar domain",
            recommendation="Document assumptions and plan validation",
        ))

    return warnings


def _check_r0_warnings(answers: IntakeAnswers) -> list[ValidationWarning]:
    warnings = []

    if answers.q6_scale in ["Multi_team", "Organization_Public"]:
        warnings.append(ValidationWarning(
            severity="WARNING",
            layer="I2",
            message="R0 with broad scale is unusual",
            recommendation="Confirm impact is truly minimal",
        ))

    return warnings
