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

<!-- VALIDATION: Traceability Index requirements
     R0: Minimum 100 characters of content (warning only)
     R1: Traceability Matrix section (3 entries minimum)
     R2: Traceability Matrix + Coverage Analysis (5 entries)
     R3: Traceability Matrix + Coverage Analysis + Gap Analysis (10 entries)
-->

## Traceability Matrix
<!-- REQUIRED[R1,R2,R3]: Traceability matrix linking requirements to verification -->

| Requirement | Design | Implementation | Test | Status |
|-------------|--------|----------------|------|--------|
| REQ-001 | DES-001 | CODE | TST-001 | Pending |

---

**Note:** Maintain traceability throughout project lifecycle.
"""
