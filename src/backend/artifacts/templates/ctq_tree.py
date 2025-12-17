"""CTQ Tree Template - Critical to Quality characteristics."""

from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse


def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    """Generate CTQ Tree with project-specific CTQs."""

    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    answers = intake_request.answers
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""# CTQ Tree
## {project_name}

**Risk Level:** {risk_level}
**Date:** {today}
**Status:** First-pass

---

<!-- VALIDATION: CTQ Tree requirements
     R0: User Needs section (1 item minimum)
     R1: User Needs + Quality Drivers (2 items minimum)
     R2: User Needs + Quality Drivers + Measurable Requirements (3 items)
     R3: Full tree with Traceability (5 items minimum)
-->

## Critical to Quality Characteristics
<!-- REQUIRED[R0,R1,R2,R3]: User Needs - what users need from system -->

### CTQ-1: Classification Accuracy
**Requirement:** Risk level must match intake responses per intake-rules.md
**Measurement:** Classification correctness
**Target:** 100%
**Priority:** Critical

"""

    if answers.q2_influence == "Automated":
        content += """### CTQ-2: System Reliability
**Requirement:** Automated actions must execute correctly
**Measurement:** % successful automated actions
**Target:** >99.9%
**Priority:** Critical

"""

    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        content += """### CTQ-3: Safety Compliance
**Requirement:** No safety violations or harm to users
**Measurement:** Safety incidents count
**Target:** 0
**Priority:** Critical

"""

    if answers.q3_worst_failure == "Financial":
        content += """### CTQ-4: Financial Accuracy
**Requirement:** All financial calculations accurate
**Measurement:** Financial error rate
**Target:** 0%
**Priority:** Critical

"""

    content += """### CTQ-5: Usability
**Requirement:** System must be usable by target audience
**Measurement:** User satisfaction score
**Target:** ≥4/5
**Priority:** High

### CTQ-6: Completeness
**Requirement:** All required artifacts generated
**Measurement:** % artifacts complete
**Target:** 100%
**Priority:** High

---

**Note:** Additional CTQs to be refined during requirements phase.
"""

    return content
