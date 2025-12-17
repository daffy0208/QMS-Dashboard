"""
Quality Plan Template Generator

Generates project-specific Quality Plan based on intake answers and classification.
"""

from datetime import datetime
from models.intake import IntakeRequest, IntakeResponse


def generate(intake_request: IntakeRequest, intake_response: IntakeResponse) -> str:
    """Generate Quality Plan content."""

    project_name = intake_request.project_name
    risk_level = intake_response.classification.risk_level
    rigor = intake_response.classification.rigor
    rationale = intake_response.classification.rationale
    answers = intake_request.answers
    today = datetime.now().strftime("%Y-%m-%d")

    # Determine user audience description
    user_desc = {
        "Internal": "internal users within the organization",
        "External": "external clients, partners, or vendors",
        "Public": "public users (general public)"
    }[answers.q1_users]

    # Determine influence description
    influence_desc = {
        "Informational": "provides informational displays",
        "Recommendations": "provides recommendations that influence decisions",
        "Automated": "performs automated actions"
    }[answers.q2_influence]

    # Determine worst case description
    worst_case_desc = {
        "Annoyance": "minor inconvenience or annoyance",
        "Financial": "financial loss",
        "Safety_Legal_Compliance": "safety, legal, or compliance violations",
        "Reputational": "reputational damage"
    }[answers.q3_worst_failure]

    # Get artifact count
    artifact_count = len(intake_response.artifacts_required)

    content = f"""# Quality Plan
## {project_name}

**Risk Level:** {risk_level}
**Rigor Mode:** {rigor}
**Date:** {today}
**Status:** Active

---

<!-- VALIDATION: Quality Plan requirements
     R2: Purpose, Scope, Roles and Responsibilities, Quality Objectives (4 sections minimum)
     R3: Same as R2 + Escalation and Governance (5 sections minimum)
-->

## 1. Project Overview
<!-- REQUIRED[R2,R3]: Purpose and Scope -->

### 1.1 Project Description
<!-- REQUIRED[R2,R3]: Clear project purpose -->
**{project_name}** is a {'regulated' if answers.q7_regulated == 'Yes' else 'non-regulated'} system that {influence_desc} for {user_desc}.

### 1.2 Risk Classification

**Risk Level:** {risk_level} ({rigor} Rigor)

**Classification Rationale:**
{rationale}

**Key Risk Factors:**
- **Users:** {answers.q1_users} ({user_desc})
- **System Influence:** {answers.q2_influence} ({influence_desc})
- **Worst Credible Failure:** {answers.q3_worst_failure} ({worst_case_desc})
- **Reversibility:** {answers.q4_reversibility}
- **Domain Understanding:** {answers.q5_domain}
- **Scale:** {answers.q6_scale}
- **Regulatory Status:** {answers.q7_regulated}

---

## 2. Quality Objectives
<!-- REQUIRED[R2,R3]: Quality goals and targets -->

### 2.1 Primary Quality Goals

"""

    # Add context-specific quality objectives
    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        content += """1. **Safety & Compliance:**
   - Ensure system meets all safety and regulatory requirements
   - Prevent failures that could cause harm or legal violations
   - Maintain audit trail for compliance verification

"""

    if answers.q2_influence == "Automated":
        content += """2. **Reliability & Availability:**
   - Ensure automated actions execute correctly
   - Implement fail-safes and error handling
   - Monitor system health and performance

"""

    if answers.q3_worst_failure == "Financial":
        content += """3. **Financial Accuracy:**
   - Ensure all financial calculations are accurate
   - Prevent financial losses through robust testing
   - Implement transaction logging and audit trails

"""

    content += """4. **Risk Management:**
   - Identify and mitigate project risks proactively
   - Maintain risk register with mitigation strategies
   - Review risks at each quality gate

5. **Quality Verification:**
   - Verify system meets all requirements through testing
   - Validate system solves user problems effectively
   - Track and measure quality metrics

---

## 3. Quality Management Approach

### 3.1 Rigor Level: {rigor}

"""

    if risk_level == "R0":
        content += """**R0 (Minimal Rigor):**
- Advisory quality activities
- Lightweight documentation
- Basic testing sufficient
- Continuous improvement encouraged but not mandated

"""
    elif risk_level == "R1":
        content += """**R1 (Moderate Rigor):**
- Conditional quality activities based on project needs
- Moderate documentation requirements
- Comprehensive testing required
- Risk-based approach to verification and validation

"""
    elif risk_level == "R2":
        content += """**R2 (Strict Rigor):**
- **Strict quality activities - no skipping without deviation**
- Comprehensive documentation required
- Full verification and validation mandatory
- Change control and CAPA processes required
- Expert review recommended for critical decisions

"""
    else:  # R3
        content += """**R3 (Maximum Rigor):**
- **MAXIMUM quality activities - no downgrade permitted**
- Complete documentation required for all activities
- Full V&V mandatory with traceability
- Change control, CAPA, and configuration management required
- Expert review mandatory for all critical decisions
- No artifact may be skipped without formal deviation approval

"""

    content += f"""### 3.2 Required QMS Artifacts

This project requires **{artifact_count} QMS artifacts** per intake-rules.md:

"""

    for i, artifact in enumerate(intake_response.artifacts_required, 1):
        content += f"{i}. {artifact}\n"

    content += """
**Status Tracking:** All artifacts must have explicit status (Done/Deferred/Deviated). No silent skipping permitted.

---

## 4. Roles and Responsibilities
<!-- REQUIRED[R2,R3]: Clear role assignments and accountabilities -->

**Project Owner:** [Name]
<!-- REQUIRED[R2,R3]: Assign project owner (no [Name] placeholders) -->
- Overall accountability for project quality
- Approves quality plan and deviations
- Reviews quality metrics and risks

**Development Team:** [Names]
- Implements system per requirements
- Conducts peer reviews and testing
- Documents design decisions

"""

    if risk_level in ["R2", "R3"] or answers.q3_worst_failure == "Safety_Legal_Compliance":
        content += """**Quality Expert:** [Name]
- Reviews risk classification
- Approves deviations from quality plan
- Conducts independent quality audits

"""

    if answers.q7_regulated != "No":
        content += """**Regulatory Compliance Lead:** [Name]
- Ensures regulatory requirements met
- Reviews compliance documentation
- Interfaces with regulatory bodies

"""

    content += """
<!-- REQUIRED[R3]: Escalation and Governance section needed for R3 -->
<!-- R3 projects must document: escalation procedures, governance structure, -->
<!-- oversight mechanisms, and decision authority boundaries -->

---

## 5. Quality Activities

### 5.1 Requirements Management
- Document functional and non-functional requirements
- Maintain traceability to design and test
- Review requirements for completeness and clarity

### 5.2 Design Review
"""

    if risk_level in ["R2", "R3"]:
        content += "- **Mandatory design reviews** before implementation\n"
    else:
        content += "- Design reviews recommended for complex features\n"

    content += """- Document design decisions and rationale
- Review for security, safety, and performance

### 5.3 Code Quality
- Peer code reviews for all changes
"""

    if risk_level in ["R2", "R3"]:
        content += "- Static analysis and linting enforced\n"

    content += """- Coding standards adherence
- Documentation of complex logic

### 5.4 Testing & Verification
"""

    if risk_level == "R0":
        content += "- Unit testing recommended\n- Integration testing as needed\n"
    elif risk_level == "R1":
        content += "- Unit testing required for critical paths\n- Integration testing required\n- Manual testing acceptable\n"
    else:
        content += "- **Comprehensive unit testing required**\n- **Integration testing required**\n- **System testing required**\n"

    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        content += "- **Safety testing with hazard analysis**\n"

    if risk_level in ["R2", "R3"]:
        content += "- **Regression testing for all changes**\n"

    content += """
### 5.5 Validation
- User acceptance testing with real users
- Validation that system solves intended problems
"""

    if risk_level in ["R2", "R3"]:
        content += "- **Formal validation report required**\n"

    content += """
---

## 6. Standards and References

**Applicable Standards:**
"""

    if answers.q7_regulated == "Yes":
        content += "- [Regulatory Standard] - To be identified based on domain\n"

    content += """- intake-rules.md - Risk classification rules
- QUALITY_KERNEL.md - Quality-first principles
"""

    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        content += "- [Safety Standard] - To be identified based on domain\n"

    content += """
**Internal References:**
- CTQ Tree (QMS-CTQ-Tree.md)
- Risk Register (QMS-Risk-Register.md)
- Traceability Index (QMS-Traceability-Index.md)

---

## 7. Quality Gates and Schedule

**Quality Gates:**
1. **Requirements Review** - Requirements complete and reviewed
2. **Design Review** - Design approved and documented
3. **Implementation Complete** - Code complete, reviewed, tested
"""

    if risk_level in ["R1", "R2", "R3"]:
        content += "4. **Verification Complete** - All tests passing, defects resolved\n"

    if risk_level in ["R2", "R3"]:
        content += "5. **Validation Complete** - User acceptance achieved\n6. **Release Approval** - All quality criteria met\n"

    content += """
**No quality gate may be skipped without deviation approval.**

---

## 8. Risk Summary

"""

    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        content += """**High Priority Risks:**
- R-XXX: Safety-critical failures could cause harm
- R-XXX: Regulatory non-compliance could result in violations

"""

    if answers.q5_domain != "Yes":
        content += """**Domain Uncertainty:**
- Domain is not fully understood - additional research and validation required
- Assumptions must be validated through testing and expert review

"""

    if answers.q2_influence == "Automated":
        content += """**Automation Risks:**
- Automated actions execute without human oversight
- Failure detection and recovery mechanisms required
- Comprehensive testing essential

"""

    content += """See Risk Register (QMS-Risk-Register.md) for complete risk analysis.

---

## 9. Measurement and Monitoring

**Key Metrics:**
"""

    if answers.q3_worst_failure == "Safety_Legal_Compliance":
        content += "- Safety incidents: 0 (target)\n"

    if answers.q2_influence == "Automated":
        content += "- System uptime: >99.9% (target)\n- Failed automated actions: <0.1% (target)\n"

    content += """- Defect density: <X defects per KLOC
- Test coverage: >X% (target TBD)
- Quality gate pass rate: 100%

See Measurement Plan (QMS-Measurement-Plan.md) for complete metrics.

---

## 10. Approval

This Quality Plan has been reviewed and approved:

**Project Owner:** _____________________________  Date: __________

"""

    if risk_level in ["R2", "R3"]:
        content += "**Quality Expert:** _____________________________  Date: __________\n\n"

    content += f"""---

**Version:** 1.0
**Date:** {today}
**Risk Level:** {risk_level}
**Rigor Mode:** {rigor}
"""

    return content
