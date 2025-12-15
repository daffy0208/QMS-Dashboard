"""
Layer 2: Cross-Validation Rules

Detect contradictions and dangerous patterns in intake answers.
Implements CV1-CV5 from intake-safety-mechanisms.md.
"""

from models.intake import IntakeAnswers, ValidationWarning


def cross_validate(answers: IntakeAnswers) -> list[ValidationWarning]:
    """
    Apply all cross-validation rules.
    Returns list of warnings for contradictory or dangerous answer combinations.
    """
    warnings: list[ValidationWarning] = []

    warnings.extend(_cv1_automated_low_reversibility_high_impact(answers))
    warnings.extend(_cv2_informational_hard_to_reverse(answers))
    warnings.extend(_cv3_recommendations_safety_legal(answers))
    warnings.extend(_cv4_internal_public_scale(answers))
    warnings.extend(_cv5_not_regulated_safety_worst_case(answers))

    return warnings


def _cv1_automated_low_reversibility_high_impact(
    answers: IntakeAnswers
) -> list[ValidationWarning]:
    """
    CV1: Automated + Low Reversibility + High Impact = Critical Flag

    Trigger:
    - Q2 = "Automated" AND
    - Q4 = "Hard" OR "Partial" AND
    - Q3 = "Safety_Legal_Compliance" OR "Financial" OR "Reputational"
    """
    if answers.q2_influence != "Automated":
        return []

    if answers.q4_reversibility not in ["Hard", "Partial"]:
        return []

    if answers.q3_worst_failure not in [
        "Safety_Legal_Compliance",
        "Financial",
        "Reputational",
    ]:
        return []

    return [
        ValidationWarning(
            severity="CRITICAL",
            layer="CV1",
            message="Automated actions with low reversibility and high impact",
            recommendation="R3 classification strongly recommended. Implement fail-safes and human oversight.",
        )
    ]


def _cv2_informational_hard_to_reverse(
    answers: IntakeAnswers
) -> list[ValidationWarning]:
    """
    CV2: Informational + Hard to Reverse = Contradiction

    Trigger:
    - Q2 = "Informational" AND
    - Q4 = "Hard"
    """
    if answers.q2_influence != "Informational":
        return []

    if answers.q4_reversibility != "Hard":
        return []

    return [
        ValidationWarning(
            severity="WARNING",
            layer="CV2",
            message="Contradiction: Informational system with hard-to-reverse failures",
            recommendation="If system only shows information, failures should be reversible. Review Q2 or Q4.",
        )
    ]


def _cv3_recommendations_safety_legal(
    answers: IntakeAnswers
) -> list[ValidationWarning]:
    """
    CV3: Recommendations + Safety/Legal = R3 Consideration

    Trigger:
    - Q2 = "Recommendations" AND
    - Q3 = "Safety_Legal_Compliance"
    """
    if answers.q2_influence != "Recommendations":
        return []

    if answers.q3_worst_failure != "Safety_Legal_Compliance":
        return []

    return [
        ValidationWarning(
            severity="WARNING",
            layer="CV3",
            message="Recommendations with safety/legal consequences require careful consideration",
            recommendation="Even with human oversight, incorrect recommendations can cause serious harm. Consider R3.",
        )
    ]


def _cv4_internal_public_scale(answers: IntakeAnswers) -> list[ValidationWarning]:
    """
    CV4: Internal + Public Scale = Clarification Needed

    Trigger:
    - Q1 = "Internal" AND
    - Q6 = "Organization_Public"
    """
    if answers.q1_users != "Internal":
        return []

    if answers.q6_scale != "Organization_Public":
        return []

    return [
        ValidationWarning(
            severity="INFO",
            layer="CV4",
            message="Internal users with organization-wide/public scale",
            recommendation="Clarify: Internal org-wide = Multi_team, or Public users = External/Public",
        )
    ]


def _cv5_not_regulated_safety_worst_case(
    answers: IntakeAnswers
) -> list[ValidationWarning]:
    """
    CV5: Not Regulated + Safety Worst Case = Review

    Trigger:
    - Q7 = "No" AND
    - Q3 = "Safety_Legal_Compliance"
    """
    if answers.q7_regulated != "No":
        return []

    if answers.q3_worst_failure != "Safety_Legal_Compliance":
        return []

    return [
        ValidationWarning(
            severity="INFO",
            layer="CV5",
            message="Safety/legal worst case but not regulated",
            recommendation="Systems with safety consequences often face regulations. Consider Q7='Possibly'.",
        )
    ]
