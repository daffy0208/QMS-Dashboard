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

## Verification Activities

### Unit Testing
- Coverage target: >80%
- All critical paths tested

### Integration Testing
- System components tested together
- API contracts verified

---

**Note:** Expand with project-specific verification activities.
"""
