"""
Expert Review Request Generator.
Formats intake data into expert review requests.
"""

from datetime import datetime
from typing import Literal
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.intake import IntakeRequest, IntakeResponse, ValidationWarning
from models.review import ReviewRequest, ReviewTrigger


def create_review_request(
    intake_request: IntakeRequest,
    intake_response: IntakeResponse,
    review_type: Literal["mandatory", "recommended"],
    review_triggers: list[ReviewTrigger],
    user_comment: str = None
) -> ReviewRequest:
    """
    Create an expert review request from intake data.

    Args:
        intake_request: Original intake request
        intake_response: Intake response with classification
        review_type: "mandatory" or "recommended"
        review_triggers: List of triggers that caused review
        user_comment: Optional user explanation

    Returns:
        ReviewRequest ready to send to expert
    """
    # Determine confidence level based on classification borderline status
    confidence = "MEDIUM" if intake_response.classification.borderline else "HIGH"

    review_request = ReviewRequest(
        intake_id=intake_response.intake_id,
        project_name=intake_request.project_name,
        review_type=review_type,
        intake_answers=intake_request.answers,
        calculated_classification=intake_response.classification.risk_level,
        confidence=confidence,
        warnings=intake_response.warnings,
        review_triggers=review_triggers,
        user_comment=user_comment
    )

    return review_request


def format_review_request_text(review_request: ReviewRequest) -> str:
    """
    Format review request as human-readable text for email/display.

    Args:
        review_request: ReviewRequest to format

    Returns:
        Formatted text string
    """
    # Question ID to full question mapping
    question_map = {
        "q1_users": "Q1: Who will use this system?",
        "q2_influence": "Q2: How does the system influence decisions/actions?",
        "q3_worst_failure": "Q3: What's the worst credible failure?",
        "q4_reversibility": "Q4: How easily can failures be reversed?",
        "q5_domain": "Q5: Do you understand the domain deeply?",
        "q6_scale": "Q6: What's the scale of impact?",
        "q7_regulated": "Q7: Is this a regulated domain?"
    }

    # Format intake answers
    answers_text = []
    answers_dict = review_request.intake_answers.model_dump()
    for key, value in answers_dict.items():
        if key in question_map:
            answers_text.append(f"  {question_map[key]} → {value}")

    # Format warnings by severity
    errors = [w for w in review_request.warnings if w.severity == "error"]
    warnings = [w for w in review_request.warnings if w.severity == "warning"]
    infos = [w for w in review_request.warnings if w.severity == "info"]

    warnings_text = []
    if errors:
        warnings_text.append("\n  🔴 ERRORS:")
        for w in errors:
            warnings_text.append(f"    • [{w.layer}] {w.message}")

    if warnings:
        warnings_text.append("\n  ⚠️  WARNINGS:")
        for w in warnings:
            warnings_text.append(f"    • [{w.layer}] {w.message}")

    if infos:
        warnings_text.append("\n  🔶 INDICATORS:")
        for w in infos:
            warnings_text.append(f"    • [{w.layer}] {w.message}")

    # Format review triggers
    triggers_text = []
    for trigger in review_request.review_triggers:
        triggers_text.append(f"  • [{trigger.trigger_id}] {trigger.description}")

    # Build full text
    text = f"""
Expert Review Request
{'='*60}

Project: {review_request.project_name}
Requested by: {review_request.requested_by}
Date: {review_request.request_date.strftime('%Y-%m-%d %H:%M:%S')} UTC
Review Type: {review_request.review_type.upper()}

Intake Answers:
{chr(10).join(answers_text)}

Calculated Classification: {review_request.calculated_classification}
Confidence: {review_request.confidence}

Validation Results:
{chr(10).join(warnings_text) if warnings_text else "  No warnings"}

Expert Review Triggers:
{chr(10).join(triggers_text)}
"""

    if review_request.user_comment:
        text += f"""
User Comment:
  "{review_request.user_comment}"
"""

    text += f"""
{'='*60}

Expert Actions:
[Approve Classification]  [Override with Justification]  [Request More Info]

Review Checklist:
□ Do intake answers accurately reflect project reality?
□ Is calculated classification appropriate for described project?
□ Are there factors not captured by intake questions?
□ Do contradictions indicate user misunderstanding or system limitation?
□ What is the actual worst credible failure scenario?
□ Is domain-specific knowledge needed (medical, financial, safety)?
□ Are there regulatory or compliance factors?
□ Should rigor be increased or decreased?
"""

    return text
