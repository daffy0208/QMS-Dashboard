"""Traceability Index Template."""
from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse

def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    today = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Traceability Index
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** First-pass

---

## Traceability Matrix

| Requirement | Design | Implementation | Test | Status |
|-------------|--------|----------------|------|--------|
| REQ-001 | DES-001 | CODE | TST-001 | Pending |

---

**Note:** Maintain traceability throughout project lifecycle.
"""
