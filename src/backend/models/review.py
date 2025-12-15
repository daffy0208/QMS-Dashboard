"""
Expert Review Data Models.
Implements Phase 5: Expert Review Workflow.
"""

from datetime import datetime
from typing import Optional, Literal
from uuid import uuid4
from pydantic import BaseModel, Field

from models.intake import IntakeRequest, IntakeResponse, IntakeAnswers, ValidationWarning


class ReviewTrigger(BaseModel):
    """Information about why expert review was triggered."""
    trigger_id: str = Field(..., description="Trigger identifier (e.g., ER1, ER2)")
    description: str = Field(..., description="Human-readable trigger reason")
    severity: Literal["mandatory", "recommended"] = Field(..., description="Review severity level")


class ReviewRequest(BaseModel):
    """Expert review request containing full context."""
    review_id: str = Field(default_factory=lambda: f"ER-{datetime.now().strftime('%Y%m%d')}-{str(uuid4())[:8]}")
    intake_id: str = Field(..., description="Associated intake ID")
    project_name: str = Field(..., description="Project name")
    requested_by: str = Field(default="System", description="Who requested the review")
    request_date: datetime = Field(default_factory=datetime.utcnow)
    review_type: Literal["mandatory", "recommended"] = Field(..., description="Review type")

    # Full intake context
    intake_answers: IntakeAnswers = Field(..., description="Original intake answers")
    calculated_classification: str = Field(..., description="Calculated risk level (R0-R3)")
    confidence: Literal["HIGH", "MEDIUM", "LOW"] = Field(default="MEDIUM", description="Classification confidence")

    # Validation results
    warnings: list[ValidationWarning] = Field(default_factory=list, description="All validation warnings")
    review_triggers: list[ReviewTrigger] = Field(..., description="Reasons for review")

    # Optional user context
    user_comment: Optional[str] = Field(None, description="Optional user explanation")

    # Review state
    status: Literal["pending", "in_review", "approved", "overridden", "info_requested"] = Field(default="pending")


class IntakeDiscrepancy(BaseModel):
    """Identified discrepancy between intake answer and reality."""
    question_id: str = Field(..., description="Question identifier (q1-q7)")
    original_answer: str = Field(..., description="User's original answer")
    actual_situation: str = Field(..., description="Expert's assessment of actual situation")
    explanation: str = Field(..., description="Why there's a discrepancy")


class ReviewApproval(BaseModel):
    """Expert approval of calculated classification."""
    review_id: str = Field(..., description="Review request ID")
    reviewer_name: str = Field(..., description="Expert reviewer name")
    reviewer_qualifications: str = Field(..., description="Expert's role/expertise")
    decision_date: datetime = Field(default_factory=datetime.utcnow)

    expert_comments: Optional[str] = Field(None, description="Optional expert comments or notes")
    classification_approved: str = Field(..., description="Approved risk level (same as calculated)")


class ReviewOverride(BaseModel):
    """Expert override of calculated classification."""
    review_id: str = Field(..., description="Review request ID")
    reviewer_name: str = Field(..., description="Expert reviewer name")
    reviewer_qualifications: str = Field(..., description="Expert's role/expertise")
    decision_date: datetime = Field(default_factory=datetime.utcnow)

    original_classification: str = Field(..., description="Calculated risk level")
    new_classification: str = Field(..., description="Expert-determined risk level")

    justification: str = Field(..., min_length=100, description="Detailed explanation for override")

    intake_discrepancies: list[IntakeDiscrepancy] = Field(
        default_factory=list,
        description="Questions where answers didn't reflect reality"
    )

    additional_factors: str = Field(..., description="Factors not captured by intake")

    risks_accepted: Optional[str] = Field(
        None,
        description="Risks accepted if downgrading (required for downgrades)"
    )


class ReviewInfoRequest(BaseModel):
    """Expert request for more information from user."""
    review_id: str = Field(..., description="Review request ID")
    reviewer_name: str = Field(..., description="Expert reviewer name")
    request_date: datetime = Field(default_factory=datetime.utcnow)

    questions: str = Field(..., min_length=50, description="Questions for the user")

    # User response
    user_response: Optional[str] = Field(None, description="User's response to questions")
    response_date: Optional[datetime] = Field(None, description="When user responded")


class ReviewResponse(BaseModel):
    """Complete expert review response."""
    review_id: str = Field(..., description="Review request ID")
    intake_id: str = Field(..., description="Associated intake ID")
    project_name: str = Field(..., description="Project name")

    reviewer_name: str = Field(..., description="Expert reviewer name")
    reviewer_qualifications: str = Field(..., description="Expert's role/expertise")
    decision_date: datetime = Field(default_factory=datetime.utcnow)

    review_type: Literal["mandatory", "recommended"] = Field(..., description="Review type")
    decision: Literal["approved", "overridden", "info_requested"] = Field(..., description="Expert decision")

    # Original context
    original_classification: str = Field(..., description="Calculated risk level")
    final_classification: str = Field(..., description="Final risk level after review")

    # Decision details (one will be populated based on decision type)
    approval: Optional[ReviewApproval] = Field(None, description="Approval details")
    override: Optional[ReviewOverride] = Field(None, description="Override details")
    info_request: Optional[ReviewInfoRequest] = Field(None, description="Info request details")

    # Audit trail
    review_triggers: list[ReviewTrigger] = Field(..., description="Why review was needed")
    outcome: str = Field(..., description="User notified, classification finalized, etc.")


class ReviewLog(BaseModel):
    """Single entry in expert review log."""
    review_id: str = Field(..., description="Review request ID")
    date: datetime = Field(default_factory=datetime.utcnow)
    project_name: str = Field(..., description="Project name")
    intake_id: str = Field(..., description="Associated intake ID")

    reviewer_name: str = Field(..., description="Expert reviewer name")
    reviewer_qualifications: str = Field(..., description="Expert's role/expertise")

    review_type: Literal["mandatory", "recommended"] = Field(..., description="Review type")
    triggers: list[str] = Field(..., description="List of trigger IDs")

    original_classification: str = Field(..., description="Calculated risk level")
    confidence: Literal["HIGH", "MEDIUM", "LOW"] = Field(..., description="Classification confidence")

    expert_decision: Literal["approved", "overridden", "info_requested"] = Field(..., description="Expert decision")
    final_classification: str = Field(..., description="Final risk level")

    justification: str = Field(..., description="Expert's detailed explanation")

    intake_discrepancies: list[IntakeDiscrepancy] = Field(
        default_factory=list,
        description="Questions where answers didn't reflect reality"
    )

    additional_considerations: Optional[str] = Field(None, description="Domain factors, policies, etc.")

    outcome: str = Field(..., description="User notified, classification finalized, etc.")
    artifacts_generated: list[str] = Field(default_factory=list, description="List of artifact files")


# ============================================================================
# PHASE 5 V2+ - QUARANTINED
# Metrics tracking is not part of Phase 5 v1 scope
# Phase 5 v1 is a RECORDED DECISION system, not a metrics engine
# ============================================================================
# class ReviewMetrics(BaseModel):
#     """Metrics for tracking expert review effectiveness."""
#     total_intakes: int = Field(default=0, description="Total intake submissions")
#     review_requests: int = Field(default=0, description="Total review requests")
#     mandatory_reviews: int = Field(default=0, description="Mandatory reviews")
#     recommended_reviews: int = Field(default=0, description="Recommended reviews")
#
#     approvals: int = Field(default=0, description="Classifications approved")
#     overrides: int = Field(default=0, description="Classifications overridden")
#     upgrades: int = Field(default=0, description="Risk level increased")
#     downgrades: int = Field(default=0, description="Risk level decreased")
#
#     avg_turnaround_hours: float = Field(default=0.0, description="Average review turnaround time")
#     sla_met_count: int = Field(default=0, description="Reviews meeting SLA")
#     sla_exceeded_count: int = Field(default=0, description="Reviews exceeding SLA")
#
#     @property
#     def review_request_rate(self) -> float:
#         if self.total_intakes == 0:
#             return 0.0
#         return (self.review_requests / self.total_intakes) * 100
#
#     @property
#     def override_rate(self) -> float:
#         if self.review_requests == 0:
#             return 0.0
#         return (self.overrides / self.review_requests) * 100
#
#     @property
#     def sla_compliance_rate(self) -> float:
#         total_completed = self.sla_met_count + self.sla_exceeded_count
#         if total_completed == 0:
#             return 0.0
#         return (self.sla_met_count / total_completed) * 100
# ============================================================================
