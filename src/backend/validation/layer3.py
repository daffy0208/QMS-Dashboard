"""
Layer 3: Risk Indicators

Pattern detection for high-risk answer combinations.
Implements I1-I4 from intake-safety-mechanisms.md.
"""

from models.intake import IntakeAnswers, ValidationWarning


def detect_risk_indicators(answers: IntakeAnswers) -> list[ValidationWarning]:
    """
    Detect high-risk patterns in answers.
    Returns list of risk indicator warnings.
    """
    warnings: list[ValidationWarning] = []

    warnings.extend(_i1_safety_legal_compliance_mentioned(answers))
    warnings.extend(_i2_financial_loss_at_scale(answers))
    warnings.extend(_i3_partial_reversibility_high_impact(answers))
    warnings.extend(_i4_domain_uncertainty_high_stakes(answers))

    return warnings


def _i1_safety_legal_compliance_mentioned(
    answers: IntakeAnswers
) -> list[ValidationWarning]:
    """
    I1: Safety/Legal/Compliance Mentioned → Always Flag

    Trigger: Q3 = "Safety_Legal_Compliance"

    This is the highest severity indicator - any safety/legal/compliance
    worst case requires special attention and typically R3 classification.
    """
    if answers.q3_worst_failure != "Safety_Legal_Compliance":
        return []

    return [
        ValidationWarning(
            severity="CRITICAL",
            layer="I1",
            message="HIGH RISK: Safety/legal/compliance worst case detected",
            recommendation="R3 classification typical. 11 artifacts required. Strict rigor mandatory unless strong mitigations exist.",
        )
    ]


def _i2_financial_loss_at_scale(answers: IntakeAnswers) -> list[ValidationWarning]:
    """
    I2: Financial Loss + Significant Scale → Flag

    Trigger:
    - Q3 = "Financial" AND
    - Q6 = "Multi_team" OR "Organization_Public"
    """
    if answers.q3_worst_failure != "Financial":
        return []

    if answers.q6_scale not in ["Multi_team", "Organization_Public"]:
        return []

    return [
        ValidationWarning(
            severity="WARNING",
            layer="I2",
            message="Financial risk at multi-team or organization scale",
            recommendation="Consider potential financial impact. Substantial losses may warrant R3 classification.",
        )
    ]


def _i3_partial_reversibility_high_impact(
    answers: IntakeAnswers
) -> list[ValidationWarning]:
    """
    I3: Partial Reversibility + High Impact → Flag

    Trigger:
    - Q4 = "Partial" AND
    - Q3 = "Safety_Legal_Compliance" OR "Financial" OR "Reputational"
    """
    if answers.q4_reversibility != "Partial":
        return []

    if answers.q3_worst_failure not in [
        "Safety_Legal_Compliance",
        "Financial",
        "Reputational",
    ]:
        return []

    return [
        ValidationWarning(
            severity="WARNING",
            layer="I3",
            message="Partial reversibility with high-impact failures",
            recommendation="'Partial' with high impact can be as serious as 'Hard'. Consider consequences vs code fixes.",
        )
    ]


def _i4_domain_uncertainty_high_stakes(
    answers: IntakeAnswers
) -> list[ValidationWarning]:
    """
    I4: Domain Partially/Not Understood + High Risk → Flag

    Trigger:
    - Q5 = "Partially" OR "No" AND
    - Q3 = "Safety_Legal_Compliance" OR "Financial"
    """
    if answers.q5_domain not in ["Partially", "No"]:
        return []

    if answers.q3_worst_failure not in ["Safety_Legal_Compliance", "Financial"]:
        return []

    severity = "CRITICAL" if answers.q5_domain == "No" else "WARNING"
    domain_desc = "unfamiliar" if answers.q5_domain == "No" else "partially understood"

    return [
        ValidationWarning(
            severity=severity,
            layer="I4",
            message=f"High-stakes system in {domain_desc} domain",
            recommendation="Increase research, expert consultation, and validation. Per intake rules: 'If uncertain, select higher risk.'",
        )
    ]
