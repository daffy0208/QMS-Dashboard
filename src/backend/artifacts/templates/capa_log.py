"""CAPA Log Template."""
from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse

def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    today = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# CAPA Log
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** Active

---

<!-- VALIDATION: CAPA Log requirements
     R2: CAPA Entries section with header and structure
     R3: CAPA Entries section with header, structure, and minimum 1 entry
-->

## Corrective and Preventive Actions
<!-- REQUIRED[R2,R3]: CAPA Entries - corrective and preventive action log -->

No entries yet.

**Note:** Log corrective and preventive actions as issues arise.
"""
