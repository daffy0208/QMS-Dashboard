"""Risk Register Template."""
from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse

def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    today = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Risk Register
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** First-pass

---

## Identified Risks

### R-001: [Risk Title]
**Description:** [Risk description]
**Likelihood:** [Low/Medium/High]
**Impact:** [Low/Medium/High]
**Risk Score:** [1-25]
**Mitigation:** [Mitigation strategy]
**Status:** [Open/Mitigated/Closed]

---

**Note:** Populate with project-specific risks during planning.
"""
