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

## Assumptions

### A-001: [Assumption Title]
**Assumption:** [Description]
**Impact if False:** [Impact]
**Validation Method:** [How to validate]
**Status:** Not validated
**Priority:** [Critical/High/Medium/Low]

---

**Note:** Populate with project-specific assumptions during planning.
"""
