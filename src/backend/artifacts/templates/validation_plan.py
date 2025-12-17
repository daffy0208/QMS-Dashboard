"""Validation Plan Template."""
from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse

def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    today = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Validation Plan
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** First-pass

---

<!-- VALIDATION: Validation Plan requirements
     R0: Validation Approach section (warning only)
     R1: Validation Approach + User Scenarios
     R2: Validation Approach + User Scenarios + Acceptance Criteria
     R3: Validation Approach + User Scenarios + Acceptance Criteria + Validation Report
-->

## Validation Activities
<!-- REQUIRED[R0,R1,R2,R3]: Validation Approach - strategy for user acceptance testing -->

### User Acceptance Testing
- Test with real users
- Validate system solves intended problems

---

**Note:** Expand with project-specific validation criteria.
"""
