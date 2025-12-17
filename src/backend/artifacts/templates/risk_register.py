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

<!-- VALIDATION: Risk Register requirements
     R2: Minimum 3 risks with all required fields
     R3: Minimum 5 risks with all required fields
     Required fields: id, description, likelihood, impact, mitigation, owner
-->

## Identified Risks

<!-- REQUIRED[R2,R3]: At least 3 risks for R2, 5 risks for R3 -->
<!-- Each risk must include: id, description, likelihood, impact, mitigation, owner -->

### R-001: [Risk Title]
<!-- REQUIRED[R2,R3]: Risk ID (e.g., R-001, R-002) -->
**Description:** [Risk description]
<!-- REQUIRED[R2,R3]: Clear description of the risk -->
**Likelihood:** [Low/Medium/High]
<!-- REQUIRED[R2,R3]: Probability assessment -->
**Impact:** [Low/Medium/High]
<!-- REQUIRED[R2,R3]: Consequence severity -->
**Risk Score:** [1-25]
**Mitigation:** [Mitigation strategy]
<!-- REQUIRED[R2,R3]: How risk will be addressed -->
**Owner:** [Name/Role]
<!-- REQUIRED[R2,R3]: Who is responsible for this risk -->
**Status:** [Open/Mitigated/Closed]

---

**Note:** Populate with project-specific risks during planning.
"""
