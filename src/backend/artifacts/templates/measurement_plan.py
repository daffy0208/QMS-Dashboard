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

<!-- VALIDATION: Measurement Plan requirements
     R0: Key Metrics section (1 metric minimum, warning only)
     R1: Key Metrics + Measurement Approach (2 metrics)
     R2: Key Metrics + Measurement Approach + Targets (3 metrics)
     R3: Key Metrics + Measurement Approach + Targets + Monitoring Frequency (5 metrics)
-->

## Key Metrics
<!-- REQUIRED[R0,R1,R2,R3]: Metrics for monitoring system quality and performance -->

### M-001: Defect Density
**Target:** <X defects per KLOC
**Measurement:** Count defects / code size

---

**Note:** Define project-specific metrics during planning.
"""
