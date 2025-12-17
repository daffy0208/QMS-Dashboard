"""Assumptions Register Template."""
from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse

def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    today = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Assumptions Register
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** First-pass

---

<!-- VALIDATION: Assumptions Register requirements
     R0: Minimum 100 characters of content (warning only)
     R1: Critical Assumptions section (1 assumption minimum)
     R2: Critical Assumptions + Validation Status (3 assumptions)
     R3: Critical Assumptions + Validation Status + Risk if Wrong (5 assumptions)
-->

## Assumptions
<!-- REQUIRED[R1,R2,R3]: Critical Assumptions - assumptions that if wrong invalidate approach -->

### A-001: [Assumption Title]
**Assumption:** [Description]
**Impact if False:** [Impact]
**Validation Method:** [How to validate]
**Status:** Not validated
**Priority:** [Critical/High/Medium/Low]

---

**Note:** Populate with project-specific assumptions during planning.
"""
