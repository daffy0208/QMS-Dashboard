"""Verification Plan Template."""
from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse

def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    today = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Verification Plan
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** First-pass

---

<!-- VALIDATION: Verification Plan requirements
     R0: Test Approach section (warning only)
     R1: Verification Strategy + Test Approach
     R2: Verification Strategy + Test Approach
     R3: Verification Strategy + Test Approach + Traceability to Risks
-->

## Verification Activities
<!-- REQUIRED[R0,R1,R2,R3]: Test Approach - how system will be verified -->

### Unit Testing
- Coverage target: >80%
- All critical paths tested

### Integration Testing
- System components tested together
- API contracts verified

---

**Note:** Expand with project-specific verification activities.
"""
