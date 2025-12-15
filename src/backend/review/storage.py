"""
Storage for expert review data.
File-based storage for review requests and responses.
Phase 7 WS-1: Uses centralized configuration.
"""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.review import (
    ReviewRequest,
    ReviewResponse,
    ReviewLog
    # ReviewMetrics - Phase 5 v2+ only
)
from config import get_config


class ReviewStorage:
    """File-based storage for expert reviews."""

    def __init__(self, data_dir: Path = None):
        """
        Initialize review storage.

        Args:
            data_dir: Base data directory (optional, uses config if not provided)
        """
        # Phase 7 WS-1: Use centralized config
        if data_dir is None:
            config = get_config()
            data_dir = config.data_root

        self.reviews_dir = data_dir / "reviews"
        self.reviews_dir.mkdir(parents=True, exist_ok=True)

        self.review_log_file = data_dir / "Expert-Review-Log.md"

    def save_review_request(self, review_request: ReviewRequest) -> None:
        """Save review request to JSON file."""
        file_path = self.reviews_dir / f"{review_request.review_id}.json"

        data = review_request.model_dump(mode='json')

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        print(f"[STORAGE] Review request saved: {file_path}")

    def load_review_request(self, review_id: str) -> Optional[ReviewRequest]:
        """Load review request from JSON file."""
        file_path = self.reviews_dir / f"{review_id}.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return ReviewRequest(**data)
        except Exception as e:
            print(f"[STORAGE] Error loading review request {review_id}: {e}")
            return None

    def save_review_response(self, review_response: ReviewResponse) -> None:
        """Save review response to JSON file."""
        file_path = self.reviews_dir / f"{review_response.review_id}_response.json"

        data = review_response.model_dump(mode='json')

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        print(f"[STORAGE] Review response saved: {file_path}")

        # Also update the review request status
        review_request = self.load_review_request(review_response.review_id)
        if review_request:
            review_request.status = review_response.decision
            self.save_review_request(review_request)

    def load_review_response(self, review_id: str) -> Optional[ReviewResponse]:
        """Load review response from JSON file."""
        file_path = self.reviews_dir / f"{review_id}_response.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return ReviewResponse(**data)
        except Exception as e:
            print(f"[STORAGE] Error loading review response {review_id}: {e}")
            return None

    def list_pending_reviews(self) -> list[ReviewRequest]:
        """List all pending review requests."""
        pending = []

        for file_path in self.reviews_dir.glob("*.json"):
            # Skip response files
            if "_response" in file_path.name:
                continue

            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                review_request = ReviewRequest(**data)

                if review_request.status == "pending":
                    pending.append(review_request)
            except Exception as e:
                print(f"[STORAGE] Error loading {file_path}: {e}")
                continue

        # Sort by request date
        pending.sort(key=lambda r: r.request_date)

        return pending

    def append_to_review_log(self, review_log: ReviewLog) -> None:
        """
        Append review log entry to Expert-Review-Log.md.

        Args:
            review_log: ReviewLog entry to append
        """
        # Create log file if it doesn't exist
        if not self.review_log_file.exists():
            self._initialize_review_log()

        # Format log entry
        entry = self._format_log_entry(review_log)

        # Append to file
        with open(self.review_log_file, 'a') as f:
            f.write("\n" + entry + "\n")

        print(f"[STORAGE] Review log entry added: {review_log.review_id}")

    def _initialize_review_log(self) -> None:
        """Create initial Expert-Review-Log.md file."""
        header = """# Expert Review Log

This document logs all expert reviews of quality intake classifications.

**Purpose:** Track expert review decisions, overrides, and effectiveness metrics.

**Version:** 1.0
**Date:** {date}

---

""".format(date=datetime.now().strftime("%Y-%m-%d"))

        with open(self.review_log_file, 'w') as f:
            f.write(header)

    def _format_log_entry(self, review_log: ReviewLog) -> str:
        """Format ReviewLog as markdown entry."""
        entry = f"""## Review: {review_log.project_name}

**Review ID:** {review_log.review_id}
**Date:** {review_log.date.strftime('%Y-%m-%d %H:%M:%S')} UTC
**Intake ID:** {review_log.intake_id}

**Reviewer:** {review_log.reviewer_name}
**Reviewer Qualifications:** {review_log.reviewer_qualifications}

**Review Type:** {review_log.review_type.upper()}
**Triggers:** {', '.join(review_log.triggers)}

**Original Classification:** {review_log.original_classification} (Confidence: {review_log.confidence})
**Expert Decision:** {review_log.expert_decision.upper()}
**Final Classification:** {review_log.final_classification}

**Justification:**
{review_log.justification}
"""

        if review_log.intake_discrepancies:
            entry += "\n**Intake Discrepancies Identified:**\n"
            for disc in review_log.intake_discrepancies:
                entry += f"- {disc.question_id}: {disc.explanation}\n"

        if review_log.additional_considerations:
            entry += f"\n**Additional Considerations:**\n{review_log.additional_considerations}\n"

        entry += f"\n**Outcome:** {review_log.outcome}\n"

        if review_log.artifacts_generated:
            entry += f"**Artifacts Generated:** {', '.join(review_log.artifacts_generated)}\n"

        entry += "\n---"

        return entry


# Global storage instance
_storage: Optional[ReviewStorage] = None


def get_review_storage(data_dir: Path = None) -> ReviewStorage:
    """
    Get or create review storage singleton.

    Args:
        data_dir: Base data directory (optional, uses config if not provided)
    """
    global _storage
    if _storage is None:
        # Phase 7 WS-1: Use centralized config
        _storage = ReviewStorage(data_dir)
    return _storage
