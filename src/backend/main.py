"""
QMS Dashboard - Main FastAPI Application
Implements Phase 1: Core Intake System
Phase 7 WS-1: Runtime & Environment Hardening
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Phase 7: Centralized configuration
from config import get_config, validate_configuration, ConfigurationError
# Phase 7 WS-2: Security utilities
from security import (
    validate_intake_id,
    validate_review_id,
    validate_json_depth,
    MAX_REQUEST_SIZE,
    ALLOWED_CONTENT_TYPES,
    SecurityError
)

from models.intake import (
    IntakeRequest,
    IntakeResponse,
    IntakeResponseSummary,
    ValidationWarning
)
from models.review import (
    ReviewRequest,
    ReviewResponse,
    ReviewApproval,
    ReviewOverride,
    ReviewInfoRequest,
    ReviewLog,
    ReviewTrigger,
    IntakeDiscrepancy
)

# Phase 8A WS-1: Artifact validation
from artifacts.validator import (
    ArtifactValidator,
    ValidationResult,
    ValidationIssue,
    validate_project_artifacts
)
# Phase 8A WS-2: Dependency management
from artifacts.dependency_manager import (
    DependencyManager,
    ReadinessAssessment,
    DependencyStatus,
    NextActionRecommendation
)
from validation.classifier import classify_risk, get_required_artifacts
from validation.layer1 import validate_intake_answers, validate_project_name
from validation.layer2 import cross_validate
from validation.layer3 import detect_risk_indicators
from validation.layer4 import generate_confirmation_warnings
from validation.layer5 import determine_expert_review
from artifacts.generator import generate_project_artifacts
from review.request_generator import create_review_request
from review.storage import get_review_storage

from pydantic import BaseModel, Field
from typing import Dict, List, Optional


# Phase 8A WS-1.4: Response contract for artifact health API
class ArtifactHealthSummary(BaseModel):
    """
    Health status for a single artifact.

    Contract: Reports current completeness state without prescribing action.
    """
    artifact_name: str = Field(description="Name of the artifact (e.g., 'Quality Plan')")
    risk_level: str = Field(description="Risk level this artifact was validated against (R0-R3)")
    completion_percent: float = Field(
        ge=0.0, le=1.0,
        description="Completeness score (0.0-1.0). NOT a quality grade, just current state."
    )
    valid: bool = Field(description="True if meets acceptance criteria with no errors")
    issue_count: int = Field(description="Total number of validation issues")
    error_count: int = Field(description="Number of error-severity issues")
    warning_count: int = Field(description="Number of warning-severity issues")
    missing_sections: List[str] = Field(description="Required sections not found or empty")
    placeholder_count: int = Field(description="Number of unfilled placeholders detected")

    # Top issues (limited to avoid overwhelming response)
    top_issues: List[str] = Field(
        max_length=5,
        description="Up to 5 most important issues (human-readable messages)"
    )


class ProjectArtifactHealth(BaseModel):
    """
    Overall health status for all artifacts in a project.

    Response contract - What this API promises:
    1. Reports current state (NOT predictions or judgments)
    2. Flags gaps (NOT prescriptive "you must fix X")
    3. Aggregates completeness (NOT workflow blocking)
    4. Surfaces issues (NOT solutions - that's WS-3)

    Messaging discipline - What this API does NOT imply:
    - Does NOT say "you cannot proceed"
    - Does NOT predict expert review outcome (that's WS-4)
    - Does NOT suggest next actions (that's WS-2 smart next-steps)
    - Does NOT provide improvement guidance (that's WS-3)

    This API is DIAGNOSTIC ONLY.
    """
    intake_id: str = Field(description="Intake ID these artifacts belong to")
    project_name: str = Field(description="Project name")
    risk_level: str = Field(description="Project risk level (R0-R3)")

    overall_completion: float = Field(
        ge=0.0, le=1.0,
        description="Weighted average completion across all artifacts. NOT a quality score."
    )

    artifacts: Dict[str, ArtifactHealthSummary] = Field(
        description="Per-artifact health summaries (keyed by artifact name)"
    )

    # Aggregate stats
    total_artifacts: int = Field(description="Number of artifacts validated")
    complete_artifacts: int = Field(description="Number of artifacts meeting acceptance criteria")
    artifacts_with_errors: int = Field(description="Number of artifacts with error-level issues")

    # High-level observations (NOT commands)
    observations: List[str] = Field(
        max_length=3,
        description="High-level observations about artifact state (e.g., 'Most artifacts incomplete')"
    )

    # Optional: Path to artifacts directory (for reference)
    artifacts_path: Optional[str] = Field(
        default=None,
        description="Filesystem path to artifacts (if available)"
    )


# ============================================================================
# Phase 8A WS-2: Dependency Management Response Models
# ============================================================================

class ProjectDependencyHealth(BaseModel):
    """
    Dependency health status for all artifacts in a project.

    Response contract - What WS-2 promises:
    1. Shows which artifacts are ready/blocked (diagnostic)
    2. Explains dependency relationships (teaching-oriented)
    3. Recommends (NOT commands) next actions
    4. NEVER blocks progression (soft blocking only)

    Messaging discipline - What WS-2 does NOT do:
    - Does NOT auto-generate missing artifacts
    - Does NOT auto-complete incomplete artifacts
    - Does NOT hard-block based on dependencies
    - Does NOT judge semantic quality (structural only)
    """
    intake_id: str = Field(description="Intake ID")
    project_name: str = Field(description="Project name")
    risk_level: str = Field(description="Project risk level (R0-R3)")

    dependencies: Dict[str, DependencyStatus] = Field(
        description="Dependency status per artifact (keyed by artifact name)"
    )

    cross_reference_issues: Dict[str, List[str]] = Field(
        description="Cross-artifact reference consistency issues (structural checks only)"
    )

    overall_ready: bool = Field(
        description="True if all required artifacts meet readiness thresholds"
    )

    blocking_count: int = Field(
        description="Number of artifacts blocked by dependencies"
    )


class NextActionsResponse(BaseModel):
    """
    Next action recommendations for user.

    Response contract - Recommendations, NOT commands:
    1. Suggests what to work on next (teaching-oriented)
    2. Explains reasoning (transparency)
    3. Shows what would be unblocked (context)
    4. NEVER prescribes or enforces (user agency preserved)

    Messaging discipline:
    - "Consider completing X" NOT "You must complete X"
    - "This would unblock Y" NOT "You cannot do Y until X"
    - Teaching tone throughout
    """
    intake_id: str = Field(description="Intake ID")
    project_name: str = Field(description="Project name")
    risk_level: str = Field(description="Project risk level (R0-R3)")

    recommendations: List[NextActionRecommendation] = Field(
        description="Ordered list of recommended actions (high priority first)"
    )

    can_proceed_anyway: bool = Field(
        default=True,
        description="User can always proceed despite recommendations (per WS-2 soft blocking)"
    )


# Phase 7 WS-1: Validate configuration on startup
try:
    validate_configuration()
    config = get_config()
except ConfigurationError as e:
    print(f"\n❌ Configuration Error:\n{e}\n", file=sys.stderr)
    print("Please check environment variables and try again.", file=sys.stderr)
    sys.exit(1)


# Initialize FastAPI app
app = FastAPI(
    title="QMS Dashboard API",
    description="Quality Management System intake and artifact generation",
    version="1.0.0"
)

# Phase 7 WS-1: Configure CORS from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# Phase 7 WS-2: Request validation middleware
@app.middleware("http")
async def validate_request_middleware(request, call_next):
    """
    Request validation middleware for security.

    Validates:
    - Request size limits (prevent DoS)
    - Content-type for POST/PUT requests
    - JSON depth (prevent stack overflow)
    """
    from fastapi import Request
    from starlette.responses import JSONResponse

    # Check request size
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_REQUEST_SIZE:
        return JSONResponse(
            status_code=413,
            content={
                "error": "Request too large",
                "detail": f"Maximum request size is {MAX_REQUEST_SIZE / (1024*1024):.1f} MB"
            }
        )

    # Validate content-type for POST/PUT requests with body
    if request.method in ("POST", "PUT") and content_length and int(content_length) > 0:
        content_type = request.headers.get("content-type", "").split(";")[0].strip()
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            return JSONResponse(
                status_code=415,
                content={
                    "error": "Unsupported Media Type",
                    "detail": f"Content-Type must be one of: {', '.join(ALLOWED_CONTENT_TYPES)}"
                }
            )

    # Process request
    response = await call_next(request)
    return response


# Phase 7 WS-1: Use centralized data paths
DATA_DIR = config.intake_dir

# Serve static frontend files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
else:
    print(f"[WARNING] Frontend directory not found: {FRONTEND_DIR}")


@app.get("/")
async def root():
    """Serve the intake form."""
    return FileResponse(FRONTEND_DIR / "intake.html")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/intake", response_model=IntakeResponse, status_code=status.HTTP_201_CREATED)
async def submit_intake(request: IntakeRequest):
    """
    Submit quality intake and receive risk classification.

    6-Layer Validation Process:
    1. Layer 1: Input validation (all questions answered, basic sanity)
    2. Layer 2: Cross-validation (detect contradictions)
    3. Layer 3: Risk indicators (flag high-risk patterns)
    4. Classification: Calculate risk level (R0-R3)
    5. Layer 4: Confirmation warnings (require acknowledgment)
    6. Layer 5: Expert review triggers (escalate if needed)
    (Layer 6: Override handled separately via /api/intake/override endpoint)

    Returns IntakeResponse with classification and next steps.
    """
    try:
        # 6-LAYER VALIDATION SYSTEM
        warnings: list[ValidationWarning] = []

        # Layer 1: Input Validation
        warnings.extend(validate_project_name(request.project_name))
        warnings.extend(validate_intake_answers(request.answers))

        # Layer 2: Cross-Validation (detect contradictions)
        warnings.extend(cross_validate(request.answers))

        # Layer 3: Risk Indicators (flag high-risk patterns)
        warnings.extend(detect_risk_indicators(request.answers))

        # CLASSIFICATION (using Phase 1 classifier)
        classification, classification_warnings = classify_risk(request.answers)
        warnings.extend(classification_warnings)

        # Layer 4: Confirmation Warnings
        warnings.extend(generate_confirmation_warnings(request.answers, classification))

        # Determine required artifacts
        artifacts_required = get_required_artifacts(classification.risk_level)

        # Layer 5: Expert Review Triggers
        expert_review_required, expert_review_recommended, review_reasons = determine_expert_review(
            request.answers,
            classification,
            warnings
        )

        # Generate next steps
        next_steps = _generate_next_steps(
            classification,
            expert_review_required,
            expert_review_recommended,
            artifacts_required
        )

        # Build response
        response = IntakeResponse(
            project_name=request.project_name,
            timestamp=request.timestamp,
            answers=request.answers,
            classification=classification,
            warnings=warnings,
            expert_review_required=expert_review_required,
            expert_review_recommended=expert_review_recommended,
            next_steps=next_steps,
            artifacts_required=artifacts_required
        )

        # Save intake response
        _save_intake_response(response)

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing intake: {str(e)}"
        )


@app.get("/api/intake/{intake_id}", response_model=IntakeResponse)
async def get_intake(intake_id: str):
    """
    Retrieve a saved intake response by ID.

    Phase 7 WS-2: Validates intake ID format for security.
    """
    # Phase 7 WS-2: Validate intake ID format
    if not validate_intake_id(intake_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid intake ID format"
        )

    file_path = DATA_DIR / f"{intake_id}.json"

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intake {intake_id} not found"
        )

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return IntakeResponse(**data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading intake: {str(e)}"
        )


@app.get("/api/intakes", response_model=list[IntakeResponseSummary])
async def list_intakes():
    """
    List all saved intake responses (summary view).
    """
    summaries = []

    for file_path in DATA_DIR.glob("*.json"):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            summary = IntakeResponseSummary(
                intake_id=data["intake_id"],
                project_name=data["project_name"],
                timestamp=data["timestamp"],
                risk_level=data["classification"]["risk_level"],
                expert_review_required=data.get("expert_review_required", False)
            )
            summaries.append(summary)
        except Exception as e:
            # Skip files that can't be loaded
            print(f"Warning: Could not load {file_path}: {e}")
            continue

    # Sort by timestamp, newest first
    summaries.sort(key=lambda x: x.timestamp, reverse=True)

    return summaries


@app.post("/api/intake/{intake_id}/generate-artifacts")
async def generate_artifacts_for_intake(intake_id: str):
    """
    Generate QMS artifacts for an existing intake.

    Phase 7 WS-2: Validates intake ID format for security.

    Returns:
        {
            "artifacts_generated": ["Quality Plan", ...],
            "file_paths": ["/path/to/file.md", ...],
            "zip_file": "/path/to/artifacts.zip"
        }
    """
    # Phase 7 WS-2: Validate intake ID format
    if not validate_intake_id(intake_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid intake ID format"
        )

    # Load intake response
    intake_file = DATA_DIR / f"{intake_id}.json"

    if not intake_file.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intake {intake_id} not found"
        )

    try:
        with open(intake_file, 'r') as f:
            data = json.load(f)

        # Reconstruct IntakeRequest and IntakeResponse
        intake_response = IntakeResponse(**data)
        intake_request = IntakeRequest(
            project_name=intake_response.project_name,
            timestamp=intake_response.timestamp,
            answers=intake_response.answers
        )

        # Generate artifacts
        result = generate_project_artifacts(intake_request, intake_response)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating artifacts: {str(e)}"
        )


# ============================================================================
# EXPERT REVIEW ENDPOINTS (Phase 5)
# ============================================================================

@app.post("/api/review-request/{intake_id}", response_model=ReviewRequest)
async def create_review_request_endpoint(
    intake_id: str,
    user_comment: str = None
):
    """
    Create an expert review request for an intake.

    This endpoint is typically called automatically when expert review is
    required/recommended, but can also be called manually by the user.

    Phase 7 WS-2: Validates intake ID format for security.

    Args:
        intake_id: ID of the intake to review
        user_comment: Optional comment from user explaining uncertainty

    Returns:
        ReviewRequest created
    """
    # Phase 7 WS-2: Validate intake ID format
    if not validate_intake_id(intake_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid intake ID format"
        )

    # Load intake response
    intake_file = DATA_DIR / f"{intake_id}.json"

    if not intake_file.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intake {intake_id} not found"
        )

    try:
        with open(intake_file, 'r') as f:
            data = json.load(f)

        intake_response = IntakeResponse(**data)
        intake_request = IntakeRequest(
            project_name=intake_response.project_name,
            timestamp=intake_response.timestamp,
            answers=intake_response.answers
        )

        # Determine review type
        review_type = "mandatory" if intake_response.expert_review_required else "recommended"

        # Create review triggers from Layer 5 validation
        # In a real implementation, we'd extract these from the validation results
        # For now, create based on review status
        review_triggers = []
        if intake_response.expert_review_required:
            review_triggers.append(ReviewTrigger(
                trigger_id="ER1",
                description="Mandatory expert review required",
                severity="mandatory"
            ))
        else:
            review_triggers.append(ReviewTrigger(
                trigger_id="ER2",
                description="Expert review recommended for validation",
                severity="recommended"
            ))

        # Create review request
        review_request = create_review_request(
            intake_request=intake_request,
            intake_response=intake_response,
            review_type=review_type,
            review_triggers=review_triggers,
            user_comment=user_comment
        )

        # Save review request
        storage = get_review_storage(config.data_root)
        storage.save_review_request(review_request)

        return review_request

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating review request: {str(e)}"
        )


@app.get("/api/review/{review_id}", response_model=ReviewRequest)
async def get_review(review_id: str):
    """
    Get details of an expert review request.

    Phase 7 WS-2: Validates review ID format for security.

    Args:
        review_id: Review request ID

    Returns:
        ReviewRequest details
    """
    # Phase 7 WS-2: Validate review ID format
    if not validate_review_id(review_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid review ID format"
        )

    storage = get_review_storage(config.data_root)
    review_request = storage.load_review_request(review_id)

    if not review_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review {review_id} not found"
        )

    return review_request


# ============================================================================
# PHASE 5 V2+ ENDPOINTS - QUARANTINED
# Queue management, workflow features, and metrics dashboards
# Phase 5 v1 is a RECORDED DECISION system, not a workflow engine
# ============================================================================
# @app.get("/api/reviews/pending", response_model=list[ReviewRequest])
# async def list_pending_reviews():
#     """
#     List all pending expert review requests.
#
#     Returns:
#         List of pending ReviewRequests sorted by request date
#     """
#     storage = get_review_storage(DATA_DIR.parent)
#     return storage.list_pending_reviews()
# ============================================================================


@app.post("/api/review/{review_id}/approve", response_model=ReviewResponse)
async def approve_review(review_id: str, approval: ReviewApproval):
    """
    Expert approves the calculated classification.

    Phase 7 WS-2: Validates review ID format for security.

    Args:
        review_id: Review request ID
        approval: ReviewApproval with expert details and comments

    Returns:
        ReviewResponse documenting the approval
    """
    # Phase 7 WS-2: Validate review ID format
    if not validate_review_id(review_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid review ID format"
        )

    storage = get_review_storage(config.data_root)
    review_request = storage.load_review_request(review_id)

    if not review_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review {review_id} not found"
        )

    try:
        # Create review response
        review_response = ReviewResponse(
            review_id=review_id,
            intake_id=review_request.intake_id,
            project_name=review_request.project_name,
            reviewer_name=approval.reviewer_name,
            reviewer_qualifications=approval.reviewer_qualifications,
            review_type=review_request.review_type,
            decision="approved",
            original_classification=review_request.calculated_classification,
            final_classification=approval.classification_approved,
            approval=approval,
            review_triggers=review_request.review_triggers,
            outcome="Classification approved, user notified"
        )

        # Save review response
        storage.save_review_response(review_response)

        # Create log entry
        review_log = ReviewLog(
            review_id=review_id,
            project_name=review_request.project_name,
            intake_id=review_request.intake_id,
            reviewer_name=approval.reviewer_name,
            reviewer_qualifications=approval.reviewer_qualifications,
            review_type=review_request.review_type,
            triggers=[t.trigger_id for t in review_request.review_triggers],
            original_classification=review_request.calculated_classification,
            confidence=review_request.confidence,
            expert_decision="approved",
            final_classification=approval.classification_approved,
            justification=approval.expert_comments or "Classification approved as calculated",
            outcome="User notified, classification finalized"
        )

        storage.append_to_review_log(review_log)

        # Send notification email to user (in real system, would get user email from intake)
        # For now, just log it
        print(f"[REVIEW] Classification approved for {review_request.project_name}: {approval.classification_approved}")

        return review_response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error approving review: {str(e)}"
        )


@app.post("/api/review/{review_id}/override", response_model=ReviewResponse)
async def override_review(review_id: str, override: ReviewOverride):
    """
    Expert overrides the calculated classification.

    Phase 7 WS-2: Validates review ID format for security.

    Args:
        review_id: Review request ID
        override: ReviewOverride with new classification and justification

    Returns:
        ReviewResponse documenting the override
    """
    # Phase 7 WS-2: Validate review ID format
    if not validate_review_id(review_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid review ID format"
        )

    storage = get_review_storage(config.data_root)
    review_request = storage.load_review_request(review_id)

    if not review_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review {review_id} not found"
        )

    # Validate override direction
    original_level = int(override.original_classification[1])
    new_level = int(override.new_classification[1])

    if new_level < original_level:
        # Downgrade - ensure risks_accepted is provided
        if not override.risks_accepted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Downgrades require 'risks_accepted' field documenting accepted risks"
            )

    try:
        # Create review response
        review_response = ReviewResponse(
            review_id=review_id,
            intake_id=review_request.intake_id,
            project_name=review_request.project_name,
            reviewer_name=override.reviewer_name,
            reviewer_qualifications=override.reviewer_qualifications,
            review_type=review_request.review_type,
            decision="overridden",
            original_classification=override.original_classification,
            final_classification=override.new_classification,
            override=override,
            review_triggers=review_request.review_triggers,
            outcome=f"Classification overridden from {override.original_classification} to {override.new_classification}, user notified"
        )

        # Save review response
        storage.save_review_response(review_response)

        # Create log entry
        review_log = ReviewLog(
            review_id=review_id,
            project_name=review_request.project_name,
            intake_id=review_request.intake_id,
            reviewer_name=override.reviewer_name,
            reviewer_qualifications=override.reviewer_qualifications,
            review_type=review_request.review_type,
            triggers=[t.trigger_id for t in review_request.review_triggers],
            original_classification=override.original_classification,
            confidence=review_request.confidence,
            expert_decision="overridden",
            final_classification=override.new_classification,
            justification=override.justification,
            intake_discrepancies=override.intake_discrepancies,
            additional_considerations=override.additional_factors,
            outcome=f"Classification overridden, user notified"
        )

        storage.append_to_review_log(review_log)

        print(f"[REVIEW] Classification overridden for {review_request.project_name}: {override.original_classification} → {override.new_classification}")

        return review_response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error overriding review: {str(e)}"
        )


# ============================================================================
# PHASE 5 V2+ ENDPOINTS - QUARANTINED
# Workflow features (request-for-info) and metrics dashboard
# Phase 5 v1 is a RECORDED DECISION system, not a workflow engine
# ============================================================================
# @app.post("/api/review/{review_id}/request-info", response_model=ReviewResponse)
# async def request_info(review_id: str, info_request: ReviewInfoRequest):
#     """
#     Expert requests more information from user.
#
#     Args:
#         review_id: Review request ID
#         info_request: ReviewInfoRequest with questions for user
#
#     Returns:
#         ReviewResponse documenting the info request
#     """
#     storage = get_review_storage(DATA_DIR.parent)
#     review_request = storage.load_review_request(review_id)
#
#     if not review_request:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Review {review_id} not found"
#         )
#
#     try:
#         # Create review response
#         review_response = ReviewResponse(
#             review_id=review_id,
#             intake_id=review_request.intake_id,
#             project_name=review_request.project_name,
#             reviewer_name=info_request.reviewer_name,
#             reviewer_qualifications="Expert Reviewer",
#             review_type=review_request.review_type,
#             decision="info_requested",
#             original_classification=review_request.calculated_classification,
#             final_classification=review_request.calculated_classification,  # Pending user response
#             info_request=info_request,
#             review_triggers=review_request.review_triggers,
#             outcome="More information requested from user"
#         )
#
#         # Save review response
#         storage.save_review_response(review_response)
#
#         print(f"[REVIEW] More information requested for {review_request.project_name}")
#
#         return review_response
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error requesting info: {str(e)}"
#         )
#
#
# @app.get("/api/reviews/metrics")
# async def get_review_metrics():
#     """
#     Get expert review effectiveness metrics.
#
#     Returns:
#         ReviewMetrics with statistics and calculated rates
#     """
#     storage = get_review_storage(DATA_DIR.parent)
#     metrics = storage.load_metrics()
#
#     # Return as dict with calculated properties
#     return {
#         "total_intakes": metrics.total_intakes,
#         "review_requests": metrics.review_requests,
#         "mandatory_reviews": metrics.mandatory_reviews,
#         "recommended_reviews": metrics.recommended_reviews,
#         "approvals": metrics.approvals,
#         "overrides": metrics.overrides,
#         "upgrades": metrics.upgrades,
#         "downgrades": metrics.downgrades,
#         "avg_turnaround_hours": metrics.avg_turnaround_hours,
#         "sla_met_count": metrics.sla_met_count,
#         "sla_exceeded_count": metrics.sla_exceeded_count,
#         "review_request_rate": metrics.review_request_rate,
#         "override_rate": metrics.override_rate,
#         "sla_compliance_rate": metrics.sla_compliance_rate
#     }
# ============================================================================


# ============================================================================
# End of Expert Review Endpoints
# ============================================================================


# ============================================================================
# Phase 8A WS-1.4: Artifact Health Endpoint
# ============================================================================

@app.get("/api/intake/{intake_id}/artifact-health", response_model=ProjectArtifactHealth)
async def get_artifact_health(intake_id: str):
    """
    Get health status for all artifacts in a project.

    Phase 8A WS-1.4: Diagnostic API - reports current artifact state.

    Returns:
        ProjectArtifactHealth with per-artifact validation results

    Contract:
        - Reports completeness (0.0-1.0) without judging quality
        - Flags validation issues without prescribing fixes
        - Aggregates results without blocking workflow
        - NO predictions, NO commands, NO guidance

    Messaging discipline:
        This endpoint is DIAGNOSTIC ONLY. It does not:
        - Block artifact generation
        - Predict expert review outcomes
        - Provide improvement suggestions (that's WS-3)
        - Dictate next actions (that's WS-2)
    """
    # Phase 7 WS-2: Validate intake ID format
    if not validate_intake_id(intake_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid intake ID format"
        )

    # Load intake response
    file_path = DATA_DIR / f"{intake_id}.json"
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intake {intake_id} not found"
        )

    with open(file_path, 'r') as f:
        intake_data = json.load(f)

    intake_response = IntakeResponse(**intake_data)
    project_name = intake_response.project_name
    risk_level = intake_response.classification.risk_level

    # Check if artifacts exist
    artifacts_dir = config.get_artifacts_path(intake_id)
    if not artifacts_dir.exists():
        # Artifacts not generated yet
        return ProjectArtifactHealth(
            intake_id=intake_id,
            project_name=project_name,
            risk_level=risk_level,
            overall_completion=0.0,
            artifacts={},
            total_artifacts=0,
            complete_artifacts=0,
            artifacts_with_errors=0,
            observations=["Artifacts not yet generated"],
            artifacts_path=str(artifacts_dir)
        )

    # Validate all artifacts
    validation_results = validate_project_artifacts(artifacts_dir, risk_level)

    # Aggregate results (Step 2: Aggregation logic)
    health = _aggregate_artifact_health(
        intake_id=intake_id,
        project_name=project_name,
        risk_level=risk_level,
        validation_results=validation_results,
        artifacts_path=str(artifacts_dir)
    )

    return health


@app.get("/api/intake/{intake_id}/dependency-health", response_model=ProjectDependencyHealth)
async def get_dependency_health(intake_id: str):
    """
    Get dependency health status for all artifacts in a project.

    Phase 8A WS-2: Dependency Management & Smart Next Steps

    Returns:
        ProjectDependencyHealth with per-artifact dependency status

    Contract:
        - Reports dependency readiness (diagnostic)
        - Explains blocking relationships (teaching-oriented)
        - Checks cross-artifact consistency (structural only)
        - NEVER blocks artifact generation (soft blocking only)

    Messaging discipline:
        This endpoint is DIAGNOSTIC + GUIDANCE. It does:
        - Show which artifacts are blocked by dependencies
        - Recommend completing prerequisites
        - Explain dependency relationships
        But it does NOT:
        - Auto-generate missing artifacts (non-goal #1)
        - Auto-complete incomplete artifacts (non-goal #2)
        - Hard-block generation (non-goal #3)
        - Judge semantic quality (non-goal #6)
    """
    # Validate intake ID format
    if not validate_intake_id(intake_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid intake ID format"
        )

    # Load intake response
    file_path = DATA_DIR / f"{intake_id}.json"
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intake {intake_id} not found"
        )

    with open(file_path, 'r') as f:
        intake_data = json.load(f)

    intake_response = IntakeResponse(**intake_data)
    project_name = intake_response.project_name
    risk_level = intake_response.classification.risk_level

    # Check if artifacts exist
    artifacts_dir = config.get_artifacts_path(intake_id)
    if not artifacts_dir.exists():
        # Artifacts not generated yet - return empty dependency status
        return ProjectDependencyHealth(
            intake_id=intake_id,
            project_name=project_name,
            risk_level=risk_level,
            dependencies={},
            cross_reference_issues={},
            overall_ready=False,
            blocking_count=0
        )

    # Get required artifacts for this risk level
    required_artifacts = get_required_artifacts(risk_level)

    # Initialize dependency manager
    dep_manager = DependencyManager()

    # Check dependencies for each artifact
    dependency_statuses = {}
    for artifact_name in required_artifacts:
        status = dep_manager.check_dependencies(artifact_name, artifacts_dir, risk_level)
        dependency_statuses[artifact_name] = status

    # Check cross-references (WS-2 structural validation)
    cross_ref_issues = dep_manager.check_cross_references(artifacts_dir, risk_level)

    # Calculate aggregate stats
    blocking_count = sum(
        1 for status in dependency_statuses.values()
        if not status.all_dependencies_ready
    )

    overall_ready = all(
        status.readiness.ready
        for status in dependency_statuses.values()
    )

    return ProjectDependencyHealth(
        intake_id=intake_id,
        project_name=project_name,
        risk_level=risk_level,
        dependencies=dependency_statuses,
        cross_reference_issues=cross_ref_issues,
        overall_ready=overall_ready,
        blocking_count=blocking_count
    )


@app.get("/api/intake/{intake_id}/next-actions", response_model=NextActionsResponse)
async def get_next_actions(intake_id: str):
    """
    Get recommended next actions for user.

    Phase 8A WS-2: Smart Next Steps

    Returns:
        NextActionsResponse with ordered recommendations

    Contract:
        - Recommends what to work on next (teaching-oriented)
        - Prioritizes based on dependency blocking
        - Explains reasoning transparently
        - NEVER commands or enforces (user agency preserved)

    Messaging discipline:
        This endpoint RECOMMENDS, does NOT command. It:
        - Suggests "Consider completing X"
        - Explains "This would unblock Y"
        - Uses teaching-oriented language
        But it does NOT:
        - Say "You must complete X" (prescriptive language, non-goal #4)
        - Auto-trigger generation (non-goal #1)
        - Block user choices (non-goal #3)
    """
    # Validate intake ID format
    if not validate_intake_id(intake_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid intake ID format"
        )

    # Load intake response
    file_path = DATA_DIR / f"{intake_id}.json"
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intake {intake_id} not found"
        )

    with open(file_path, 'r') as f:
        intake_data = json.load(f)

    intake_response = IntakeResponse(**intake_data)
    project_name = intake_response.project_name
    risk_level = intake_response.classification.risk_level

    # Check if artifacts exist
    artifacts_dir = config.get_artifacts_path(intake_id)
    if not artifacts_dir.exists():
        # Artifacts not generated yet
        return NextActionsResponse(
            intake_id=intake_id,
            project_name=project_name,
            risk_level=risk_level,
            recommendations=[
                NextActionRecommendation(
                    action="Generate all required artifacts",
                    artifact_name="All",
                    priority="high",
                    reason="Artifacts not yet generated",
                    unblocks=[]
                )
            ],
            can_proceed_anyway=True
        )

    # Get required artifacts for this risk level
    required_artifacts = get_required_artifacts(risk_level)

    # Initialize dependency manager
    dep_manager = DependencyManager()

    # Get next action recommendations
    recommendations = dep_manager.get_next_actions(
        artifacts_dir,
        risk_level,
        required_artifacts
    )

    return NextActionsResponse(
        intake_id=intake_id,
        project_name=project_name,
        risk_level=risk_level,
        recommendations=recommendations,
        can_proceed_anyway=True
    )


# ============================================================================
# Helper Functions
# ============================================================================

def _aggregate_artifact_health(
    intake_id: str,
    project_name: str,
    risk_level: str,
    validation_results: Dict[str, ValidationResult],
    artifacts_path: str
) -> ProjectArtifactHealth:
    """
    Aggregate validation results into project health summary.

    Aggregation logic (Step 2):
    1. Convert ValidationResult → ArtifactHealthSummary per artifact
    2. Calculate weighted average completion
    3. Count totals (complete, with errors, etc.)
    4. Generate observations (descriptive, NOT prescriptive)

    Messaging discipline enforced:
    - Observations describe state ("Most artifacts incomplete")
    - Observations do NOT command ("Fix X before Y")
    - Observations do NOT predict ("Will likely fail review")
    """
    artifact_summaries: Dict[str, ArtifactHealthSummary] = {}

    for artifact_name, result in validation_results.items():
        # Count issues by severity
        error_count = sum(1 for issue in result.issues if issue.severity == "error")
        warning_count = sum(1 for issue in result.issues if issue.severity == "warning")

        # Extract top 5 issues (most important)
        top_issues = [
            issue.message for issue in result.issues[:5]
        ]

        artifact_summaries[artifact_name] = ArtifactHealthSummary(
            artifact_name=artifact_name,
            risk_level=result.risk_level,
            completion_percent=result.completion_percent,
            valid=result.valid,
            issue_count=len(result.issues),
            error_count=error_count,
            warning_count=warning_count,
            missing_sections=result.missing_sections,
            placeholder_count=result.placeholder_count,
            top_issues=top_issues
        )

    # Calculate aggregate stats
    total_artifacts = len(artifact_summaries)
    complete_artifacts = sum(1 for summary in artifact_summaries.values() if summary.valid)
    artifacts_with_errors = sum(1 for summary in artifact_summaries.values() if summary.error_count > 0)

    # Calculate weighted average completion
    if total_artifacts > 0:
        overall_completion = sum(
            summary.completion_percent for summary in artifact_summaries.values()
        ) / total_artifacts
    else:
        overall_completion = 0.0

    # Generate observations (descriptive, NOT prescriptive)
    observations = _generate_observations(
        overall_completion=overall_completion,
        complete_artifacts=complete_artifacts,
        total_artifacts=total_artifacts,
        artifacts_with_errors=artifacts_with_errors
    )

    return ProjectArtifactHealth(
        intake_id=intake_id,
        project_name=project_name,
        risk_level=risk_level,
        overall_completion=overall_completion,
        artifacts=artifact_summaries,
        total_artifacts=total_artifacts,
        complete_artifacts=complete_artifacts,
        artifacts_with_errors=artifacts_with_errors,
        observations=observations,
        artifacts_path=artifacts_path
    )


def _generate_observations(
    overall_completion: float,
    complete_artifacts: int,
    total_artifacts: int,
    artifacts_with_errors: int
) -> List[str]:
    """
    Generate high-level observations about artifact health.

    Step 3: Messaging discipline
    - Use descriptive language ("X artifacts have Y")
    - Avoid commands ("You must fix X")
    - Avoid predictions ("This will fail review")
    - Avoid judgments ("This is poor quality")

    Acceptable:
    - "Most artifacts are incomplete"
    - "Several artifacts have validation errors"
    - "Placeholder text detected in multiple artifacts"

    NOT acceptable:
    - "Fix placeholders before review"
    - "You cannot proceed with incomplete artifacts"
    - "This project will fail expert review"
    """
    observations = []

    # Observation 1: Overall completeness
    if overall_completion >= 0.8:
        observations.append(f"Most artifacts complete ({int(overall_completion * 100)}% overall)")
    elif overall_completion >= 0.5:
        observations.append(f"Artifacts partially complete ({int(overall_completion * 100)}% overall)")
    else:
        observations.append(f"Most artifacts incomplete ({int(overall_completion * 100)}% overall)")

    # Observation 2: Valid artifacts
    if total_artifacts > 0:
        if complete_artifacts == total_artifacts:
            observations.append(f"All {total_artifacts} artifacts meet acceptance criteria")
        elif complete_artifacts == 0:
            observations.append(f"No artifacts currently meet acceptance criteria")
        else:
            observations.append(f"{complete_artifacts}/{total_artifacts} artifacts meet acceptance criteria")

    # Observation 3: Errors present
    if artifacts_with_errors > 0:
        if artifacts_with_errors == total_artifacts:
            observations.append(f"All artifacts have validation errors")
        else:
            observations.append(f"{artifacts_with_errors} artifact(s) have validation errors")

    return observations[:3]  # Max 3 observations


def _generate_next_steps(
    classification,
    expert_review_required: bool,
    expert_review_recommended: bool,
    artifacts_required: list[str]
) -> list[str]:
    """
    Generate list of next steps for the user.
    """
    steps = []

    # Step 1: Expert review if needed
    if expert_review_required:
        steps.append("🔴 REQUIRED: Submit for expert review before proceeding")
    elif expert_review_recommended:
        steps.append("🟡 RECOMMENDED: Consider expert review for validation")

    # Step 2: Review classification
    steps.append(f"Review your risk classification: {classification.risk_level} ({classification.rigor} rigor)")

    # Step 3: Review warnings
    steps.append("Review all warnings and recommendations above")

    # Step 4: Generate artifacts
    artifact_count = len(artifacts_required)
    steps.append(f"Generate {artifact_count} required QMS artifacts: {', '.join(artifacts_required[:3])}{'...' if artifact_count > 3 else ''}")

    # Step 5: Begin implementation
    steps.append("Review and approve quality plan before implementation begins")

    return steps


def _save_intake_response(response: IntakeResponse) -> None:
    """
    Save intake response to JSON file.
    """
    file_path = DATA_DIR / f"{response.intake_id}.json"

    # Convert to dict for JSON serialization
    data = response.model_dump(mode='json')

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

    print(f"Intake response saved: {file_path}")


if __name__ == "__main__":
    import uvicorn
    # Phase 7 WS-1: Use configuration for server settings
    uvicorn.run(
        "main:app",
        host=config.host,
        port=config.port,
        reload=(config.env == "development"),
        log_level=config.log_level.lower()
    )
