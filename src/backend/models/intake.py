"""
Data models for QMS Dashboard intake system.
Implements IntakeResponse structure from intake-validation-spec.md.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field, validator
from datetime import datetime
import uuid


class IntakeAnswers(BaseModel):
    """
    The 7 mandatory intake questions.
    Values match intake-rules.md classification logic.
    """
    q1_users: Literal["Internal", "External", "Public"] = Field(
        ...,
        description="Who are the users?"
    )
    q2_influence: Literal["Informational", "Recommendations", "Automated"] = Field(
        ...,
        description="What decisions or actions will this system influence?"
    )
    q3_worst_failure: Literal["Annoyance", "Financial", "Safety_Legal_Compliance", "Reputational"] = Field(
        ...,
        description="What is the worst realistic failure?"
    )
    q4_reversibility: Literal["Easy", "Partial", "Hard"] = Field(
        ...,
        description="How easily can failures be fixed?"
    )
    q5_domain: Literal["Yes", "Partially", "No"] = Field(
        ...,
        description="Do you understand the problem domain?"
    )
    q6_scale: Literal["Individual", "Team", "Multi_team", "Organization_Public"] = Field(
        ...,
        description="How many people will use this?"
    )
    q7_regulated: Literal["No", "Possibly", "Yes"] = Field(
        ...,
        description="Is this project regulated or auditable?"
    )


class IntakeRequest(BaseModel):
    """
    Complete intake submission from user.
    """
    project_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the project undergoing quality intake"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of intake submission (ISO 8601)"
    )
    answers: IntakeAnswers = Field(
        ...,
        description="Answers to the 7 intake questions"
    )


class ValidationWarning(BaseModel):
    """
    Warning or alert from validation layers.
    """
    severity: Literal["INFO", "WARNING", "CRITICAL"] = Field(
        ...,
        description="Severity level of the warning"
    )
    layer: str = Field(
        ...,
        description="Which validation layer triggered this (e.g., 'CV1', 'I2')"
    )
    message: str = Field(
        ...,
        description="Human-readable warning message"
    )
    recommendation: Optional[str] = Field(
        None,
        description="Suggested action to address the warning"
    )


class RiskClassification(BaseModel):
    """
    Risk level classification result.
    """
    risk_level: Literal["R0", "R1", "R2", "R3"] = Field(
        ...,
        description="Calculated risk level"
    )
    rigor: Literal["Minimal", "Moderate", "Strict", "Maximum"] = Field(
        ...,
        description="Required quality rigor"
    )
    rationale: str = Field(
        ...,
        description="Explanation of why this risk level was assigned"
    )
    borderline: bool = Field(
        default=False,
        description="True if classification is near boundary between levels"
    )


class IntakeResponse(BaseModel):
    """
    Complete response after intake processing.
    Includes classification, warnings, and next steps.
    """
    intake_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this intake session"
    )
    project_name: str = Field(
        ...,
        description="Name of the project"
    )
    timestamp: datetime = Field(
        ...,
        description="Timestamp of intake submission"
    )
    answers: IntakeAnswers = Field(
        ...,
        description="User's answers to intake questions"
    )
    classification: RiskClassification = Field(
        ...,
        description="Risk classification result"
    )
    warnings: list[ValidationWarning] = Field(
        default_factory=list,
        description="Validation warnings from 6-layer system"
    )
    expert_review_required: bool = Field(
        default=False,
        description="True if expert review is mandatory"
    )
    expert_review_recommended: bool = Field(
        default=False,
        description="True if expert review is recommended but not mandatory"
    )
    next_steps: list[str] = Field(
        default_factory=list,
        description="Actions user should take next"
    )
    artifacts_required: list[str] = Field(
        default_factory=list,
        description="QMS artifacts required for this risk level"
    )


class IntakeResponseSummary(BaseModel):
    """
    Simplified summary for listing intakes.
    """
    intake_id: str
    project_name: str
    timestamp: datetime
    risk_level: Literal["R0", "R1", "R2", "R3"]
    expert_review_required: bool
