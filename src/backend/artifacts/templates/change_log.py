"""Change Log Template."""
from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse

def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    today = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Change Log
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** Active

---

<!-- VALIDATION: Change Log requirements
     R2: Change History section with header and structure
     R3: Change History section with header, structure, and minimum 1 entry
-->

## Change Entries
<!-- REQUIRED[R2,R3]: Change History - audit trail of project changes -->

### CHG-001: Initial Quality Plan
**Date:** {today}
**Type:** Quality Artifact
**Description:** Initial QMS artifacts generated from intake
**Status:** Complete

---

**Note:** Log all changes to project.
"""
