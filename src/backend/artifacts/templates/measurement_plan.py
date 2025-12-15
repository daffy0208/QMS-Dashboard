"""Measurement Plan Template."""
from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse

def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    today = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Measurement Plan
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** First-pass

---

## Key Metrics

### M-001: Defect Density
**Target:** <X defects per KLOC
**Measurement:** Count defects / code size

---

**Note:** Define project-specific metrics during planning.
"""
