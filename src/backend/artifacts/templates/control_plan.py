"""Control Plan Template."""
from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse

def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    today = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Control Plan
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** First-pass

---

<!-- VALIDATION: Control Plan requirements
     R2: Control Objectives + Operational Controls
     R3: Control Objectives + Operational Controls + Monitoring and Review
-->

## Change Control Process
<!-- REQUIRED[R2,R3]: Operational Controls - controls to manage identified risks -->

All changes must be:
1. Documented
2. Reviewed
3. Approved
4. Tested
5. Deployed with rollback plan

---

**Note:** Implement formal change control process.
"""
