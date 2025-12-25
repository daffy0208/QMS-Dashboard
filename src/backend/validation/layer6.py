"""
Layer 6: Override & Justification

Handle classification overrides with required justification.
Implements O1-O2 from intake-safety-mechanisms.md.
"""

from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime, timezone


def utcnow() -> datetime:
    """Timezone-aware UTC 'now' for timestamps."""
    return datetime.now(timezone.utc)


class OverrideRequest(BaseModel):
    """
    Request to override calculated classification.
    """
    calculated_risk: Literal["R0", "R1", "R2", "R3"] = Field(
        ..., description="Risk level calculated by system"
    )
    requested_risk: Literal["R0", "R1", "R2", "R3"] = Field(
        ..., description="Risk level user wants to use"
    )
    override_type: Literal["expert", "self"] = Field(
        ..., description="Expert override or user self-override"
    )
    justification: str = Field(
        ..., min_length=50, description="Detailed justification for override (min 50 chars)"
    )
    question_adjustments: dict[str, str] = Field(
        default_factory=dict,
        description="Questions that don't reflect reality: {question_id: explanation}",
    )
    risks_accepted: list[str] = Field(
        default_factory=list, description="Risks accepted by downgrade (if applicable)"
    )
    requested_by: str = Field(..., description="Name of person requesting override")
    approved_by: str | None = Field(
        None, description="Approver name (required for downgrades)"
    )
    timestamp: datetime = Field(default_factory=utcnow)


class OverrideValidationResult(BaseModel):
    """
    Result of validating an override request.
    """
    valid: bool = Field(..., description="Whether override request is valid")
    requires_approval: bool = Field(
        default=False, description="Whether approval is required"
    )
    errors: list[str] = Field(default_factory=list, description="Validation errors")
    warnings: list[str] = Field(default_factory=list, description="Warnings")


def validate_override_request(request: OverrideRequest) -> OverrideValidationResult:
    """
    Validate an override request.

    Rules:
    - Expert overrides: Always allowed with justification
    - Self overrides to higher risk: Always allowed
    - Self overrides to lower risk: Require approval + detailed justification
    - Downgrades from R2/R3: Require deviation record
    """
    errors: list[str] = []
    warnings: list[str] = []
    requires_approval = False

    # Parse risk levels
    risk_levels = {"R0": 0, "R1": 1, "R2": 2, "R3": 3}
    calculated_level = risk_levels[request.calculated_risk]
    requested_level = risk_levels[request.requested_risk]

    # Check if this is a downgrade
    is_downgrade = requested_level < calculated_level
    is_strict_downgrade = calculated_level >= 2 and requested_level < calculated_level

    # Expert overrides are always allowed
    if request.override_type == "expert":
        if is_downgrade and not request.approved_by:
            warnings.append("Expert downgrade should include approver name for audit trail")
        # Expert overrides always valid
        return OverrideValidationResult(
            valid=True,
            requires_approval=is_strict_downgrade,
            errors=[],
            warnings=warnings,
        )

    # Self overrides to higher risk: Always allowed
    if not is_downgrade:
        return OverrideValidationResult(
            valid=True, requires_approval=False, errors=[], warnings=warnings
        )

    # Self downgrade: Requires detailed justification
    if len(request.justification) < 100:
        errors.append(
            "Downgrade justification must be detailed (min 100 characters)"
        )

    if not request.question_adjustments:
        errors.append(
            "Downgrade must identify which intake questions don't reflect reality"
        )

    if is_downgrade and not request.risks_accepted:
        warnings.append(
            "Downgrade should explicitly list risks being accepted"
        )

    # Strict rigor downgrade (R2/R3 → R1/R0): Requires approval
    if is_strict_downgrade:
        requires_approval = True
        if not request.approved_by:
            errors.append(
                f"Downgrade from {request.calculated_risk} requires approval per intake-rules.md"
            )
        errors.append(
            "Downgrade from R2/R3 requires deviation record in CAPA Log"
        )

    valid = len(errors) == 0

    return OverrideValidationResult(
        valid=valid,
        requires_approval=requires_approval,
        errors=errors,
        warnings=warnings,
    )


def format_override_record(request: OverrideRequest) -> str:
    """
    Format override request as documentation record.
    This should be logged in Change Log or Quality Plan.
    """
    record = f"""
CLASSIFICATION OVERRIDE RECORD
{'='*60}

Override Type: {request.override_type.upper()}
From: {request.calculated_risk} → To: {request.requested_risk}
Requested by: {request.requested_by}
"""
    if request.approved_by:
        record += f"Approved by: {request.approved_by}\n"

    record += f"Date: {request.timestamp.isoformat()}\n"
    record += f"\nJustification:\n{request.justification}\n"

    if request.question_adjustments:
        record += "\nIntake Questions Not Reflecting Reality:\n"
        for q_id, explanation in request.question_adjustments.items():
            record += f"  - {q_id}: {explanation}\n"

    if request.risks_accepted:
        record += "\nRisks Accepted by Downgrade:\n"
        for risk in request.risks_accepted:
            record += f"  - {risk}\n"

    record += f"\n{'='*60}\n"

    return record
