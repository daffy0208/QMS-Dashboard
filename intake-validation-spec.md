# Intake Validation Specification
## Implementation Guide for Safety Mechanisms

**Date:** 2025-12-12
**Purpose:** Detailed specification for implementing validation rules, warnings, and safety checks
**For:** Developers implementing the QMS Dashboard intake system
**Verifies:** VER-001 (Risk classification accuracy), VER-005 (Status enforcement)

---

## Implementation Overview

The validation system has 6 layers (from intake-safety-mechanisms.md):
1. Input Validation (basic checks)
2. Cross-Validation (contradiction detection)
3. Risk Indicators (pattern matching)
4. Warnings & Confirmations (user acknowledgment)
5. Expert Review Triggers (escalation)
6. Override & Justification (documented exceptions)

Each layer builds on the previous, creating defense-in-depth.

---

## Data Model

### Intake Response Object
```json
{
  "intake_id": "string (UUID)",
  "project_name": "string",
  "timestamp": "ISO 8601 datetime",
  "answers": {
    "q1_users": "Internal | External | Public",
    "q2_influence": "Informational | Recommendations | Automated",
    "q3_worst_failure": "Annoyance | Financial | Safety_Legal_Compliance | Reputational",
    "q4_reversibility": "Easy | Partial | Hard",
    "q5_domain": "Yes | Partially | No",
    "q6_scale": "Individual | Team | Multi_team | Organization_Public",
    "q7_regulated": "No | Possibly | Yes"
  },
  "calculated_risk": "R0 | R1 | R2 | R3",
  "validation_results": {
    "rules_triggered": ["array of rule IDs"],
    "warnings_shown": ["array of warning IDs"],
    "flags": ["array of flag types"],
    "expert_review_required": boolean,
    "user_acknowledged": boolean
  },
  "override": {
    "applied": boolean,
    "from_risk": "R0 | R1 | R2 | R3",
    "to_risk": "R0 | R1 | R2 | R3",
    "justification": "string",
    "approved_by": "string",
    "approval_date": "ISO 8601 datetime"
  }
}
```

---

## Layer 1: Input Validation

### Rule V1: All Questions Required
```python
def validate_all_answered(answers):
    """Ensure all 7 questions have answers."""
    required_fields = ['q1_users', 'q2_influence', 'q3_worst_failure',
                       'q4_reversibility', 'q5_domain', 'q6_scale', 'q7_regulated']

    missing = [q for q in required_fields if answers.get(q) is None]

    if missing:
        return {
            'valid': False,
            'rule_id': 'V1',
            'message': f'All 7 intake questions must be answered. Missing: {", ".join(missing)}',
            'missing_questions': missing
        }

    return {'valid': True}
```

### Rule V2: Valid Option Values
```python
VALID_OPTIONS = {
    'q1_users': ['Internal', 'External', 'Public'],
    'q2_influence': ['Informational', 'Recommendations', 'Automated'],
    'q3_worst_failure': ['Annoyance', 'Financial', 'Safety_Legal_Compliance', 'Reputational'],
    'q4_reversibility': ['Easy', 'Partial', 'Hard'],
    'q5_domain': ['Yes', 'Partially', 'No'],
    'q6_scale': ['Individual', 'Team', 'Multi_team', 'Organization_Public'],
    'q7_regulated': ['No', 'Possibly', 'Yes']
}

def validate_option_values(answers):
    """Ensure all answers are valid options."""
    invalid = []
    for question, value in answers.items():
        if question in VALID_OPTIONS and value not in VALID_OPTIONS[question]:
            invalid.append({'question': question, 'value': value,
                          'valid_options': VALID_OPTIONS[question]})

    if invalid:
        return {
            'valid': False,
            'rule_id': 'V2',
            'message': 'Invalid option values detected',
            'invalid_answers': invalid
        }

    return {'valid': True}
```

---

## Layer 2: Cross-Validation Rules

### Rule CV1: Automated + Low Reversibility + High Impact
```python
def check_automated_high_impact(answers):
    """Flag dangerous combination: automated actions + low reversibility + high impact."""
    q2 = answers.get('q2_influence')
    q3 = answers.get('q3_worst_failure')
    q4 = answers.get('q4_reversibility')

    is_automated = (q2 == 'Automated')
    low_reversibility = (q4 in ['Hard', 'Partial'])
    high_impact = (q3 in ['Safety_Legal_Compliance', 'Financial', 'Reputational'])

    if is_automated and low_reversibility and high_impact:
        return {
            'triggered': True,
            'rule_id': 'CV1',
            'severity': 'CRITICAL',
            'message': '⚠️ SAFETY WARNING: Automated actions with low reversibility and high impact typically require R3 (Strict rigor, no downgrade).',
            'details': {
                'automated': True,
                'reversibility': q4,
                'impact': q3
            },
            'recommendation': 'R3',
            'requires_acknowledgment': True
        }

    return {'triggered': False}
```

### Rule CV2: Informational + Hard to Reverse
```python
def check_informational_contradiction(answers):
    """Flag contradiction: informational only but hard to reverse."""
    q2 = answers.get('q2_influence')
    q4 = answers.get('q4_reversibility')

    if q2 == 'Informational' and q4 == 'Hard':
        return {
            'triggered': True,
            'rule_id': 'CV2',
            'severity': 'WARNING',
            'message': '⚠️ POSSIBLE CONTRADICTION: System is "Informational only" but failures are "Hard to reverse"',
            'guidance': 'If the system only provides information, failures should be easy to reverse (fix bug, show correct data). Hard-to-reverse failures suggest the system influences decisions or actions.',
            'questions_to_review': ['Q2', 'Q4'],
            'requires_acknowledgment': True
        }

    return {'triggered': False}
```

### Rule CV3: Recommendations + Safety/Legal
```python
def check_recommendations_safety(answers):
    """Flag safety consideration: recommendations with safety/legal consequences."""
    q2 = answers.get('q2_influence')
    q3 = answers.get('q3_worst_failure')

    if q2 == 'Recommendations' and q3 == 'Safety_Legal_Compliance':
        return {
            'triggered': True,
            'rule_id': 'CV3',
            'severity': 'HIGH',
            'message': '⚠️ SAFETY CONSIDERATION: System provides recommendations that could lead to safety/legal/compliance failures.',
            'guidance': 'Even though humans make final decisions, incorrect recommendations can cause serious harm if users trust them.',
            'considerations': [
                'Will users have independent way to verify recommendations?',
                'What happens if users trust incorrect recommendations?',
                'Can users easily detect when recommendations are wrong?'
            ],
            'recommendation': 'Consider R3 classification if recommendations are heavily relied upon',
            'requires_acknowledgment': True
        }

    return {'triggered': False}
```

### Rule CV4: Internal + Organization-wide/Public Scale
```python
def check_internal_public_contradiction(answers):
    """Flag contradiction: internal users but organization-wide/public scale."""
    q1 = answers.get('q1_users')
    q6 = answers.get('q6_scale')

    if q1 == 'Internal' and q6 == 'Organization_Public':
        return {
            'triggered': True,
            'rule_id': 'CV4',
            'severity': 'WARNING',
            'message': '⚠️ CLARIFICATION NEEDED: Internal users but Organization-wide/public scale',
            'clarification': 'Please clarify: Internal organization-wide → Select Q6="Multi_team", Q1="Internal". Public users → Select Q1="Public".',
            'requires_acknowledgment': True
        }

    return {'triggered': False}
```

### Rule CV5: Not Regulated + Safety Worst Case
```python
def check_unregulated_safety(answers):
    """Flag consideration: safety/legal worst case but not regulated."""
    q3 = answers.get('q3_worst_failure')
    q7 = answers.get('q7_regulated')

    if q3 == 'Safety_Legal_Compliance' and q7 == 'No':
        return {
            'triggered': True,
            'rule_id': 'CV5',
            'severity': 'INFO',
            'message': '💡 REGULATORY CONSIDERATION: Safety/legal worst case but not regulated',
            'guidance': 'Systems with safety/legal worst cases are often subject to industry standards, internal compliance, or legal liability even without formal regulation.',
            'considerations': [
                'Could this system face future regulation?',
                'Are there industry standards that apply?',
                'Should we treat it as regulated for quality purposes?'
            ],
            'suggestion': 'Consider answering Q7="Possibly" if uncertain',
            'requires_acknowledgment': False
        }

    return {'triggered': False}
```

---

## Layer 3: Risk Indicators

### Indicator I1: Safety/Legal/Compliance Flag
```python
def check_safety_indicator(answers):
    """Always flag safety/legal/compliance as high risk."""
    q3 = answers.get('q3_worst_failure')

    if q3 == 'Safety_Legal_Compliance':
        return {
            'triggered': True,
            'indicator_id': 'I1',
            'severity': 'CRITICAL',
            'icon': '🔴',
            'message': 'HIGH RISK INDICATOR: Safety/Legal/Compliance worst case',
            'r3_info': {
                'triggered_by': 'Worst credible failure involves SAFETY / LEGAL / COMPLIANCE',
                'requirements': [
                    'Strict rigor mode (no downgrade allowed)',
                    '11 quality artifacts required',
                    'All verification and validation mandatory',
                    'No artifact may be skipped without formal deviation'
                ]
            },
            'requires_justification_if_r2': True
        }

    return {'triggered': False}
```

### Indicator I2: Financial Loss at Scale
```python
def check_financial_scale_indicator(answers):
    """Flag financial loss at significant scale."""
    q3 = answers.get('q3_worst_failure')
    q6 = answers.get('q6_scale')

    if q3 == 'Financial' and q6 in ['Multi_team', 'Organization_Public']:
        return {
            'triggered': True,
            'indicator_id': 'I2',
            'severity': 'MEDIUM_HIGH',
            'icon': '🔶',
            'message': 'FINANCIAL RISK AT SCALE',
            'guidance': 'Financial losses at scale can be significant. Consider potential impact and whether substantial financial loss warrants R3 classification.',
            'considerations': [
                'What is the potential financial impact?',
                'Is this customer money or company money?',
                'Could financial loss lead to legal liability?'
            ]
        }

    return {'triggered': False}
```

### Indicator I3: Partial Reversibility + High Impact
```python
def check_partial_reversibility_indicator(answers):
    """Flag partial reversibility with high impact."""
    q3 = answers.get('q3_worst_failure')
    q4 = answers.get('q4_reversibility')

    high_impact = q3 in ['Safety_Legal_Compliance', 'Financial', 'Reputational']

    if q4 == 'Partial' and high_impact:
        return {
            'triggered': True,
            'indicator_id': 'I3',
            'severity': 'MEDIUM_HIGH',
            'icon': '🔶',
            'message': 'LIMITED REVERSIBILITY WITH HIGH IMPACT',
            'guidance': '"Partial reversibility" with high impact can be as serious as "Hard/irreversible." Consider: Are you thinking about reversing the code, or reversing the consequences?',
            'example': 'Bug fixed quickly (easy), but wrong data already sent to customers (irreversible harm done)'
        }

    return {'triggered': False}
```

### Indicator I4: Domain Uncertainty + High Stakes
```python
def check_domain_uncertainty_indicator(answers):
    """Flag domain uncertainty with high stakes."""
    q3 = answers.get('q3_worst_failure')
    q5 = answers.get('q5_domain')

    uncertain_domain = q5 in ['Partially', 'No']
    high_stakes = q3 in ['Safety_Legal_Compliance', 'Financial']

    if uncertain_domain and high_stakes:
        return {
            'triggered': True,
            'indicator_id': 'I4',
            'severity': 'MEDIUM',
            'icon': '🔶',
            'message': 'DOMAIN UNCERTAINTY WITH HIGH STAKES',
            'guidance': 'Building systems in poorly understood domains with high-impact failures is risky.',
            'recommendations': [
                'Increase domain research and expert consultation',
                'Consider R3 classification due to uncertainty',
                'Add extra validation activities',
                'Document domain knowledge gaps in Assumptions Register'
            ],
            'rule_reminder': 'Per intake rule: "If uncertain, select the higher risk."'
        }

    return {'triggered': False}
```

---

## Layer 4: Risk Classification Logic

### Main Classification Function
```python
def classify_risk(answers):
    """
    Calculate risk level (R0-R3) based on intake answers.
    Implements logic from intake-rules-enhanced.md section 3.
    """
    q1 = answers.get('q1_users')
    q2 = answers.get('q2_influence')
    q3 = answers.get('q3_worst_failure')
    q4 = answers.get('q4_reversibility')
    q5 = answers.get('q5_domain')
    q6 = answers.get('q6_scale')
    q7 = answers.get('q7_regulated')

    # R3 Triggers (Critical)
    if q3 == 'Safety_Legal_Compliance' and (q2 == 'Automated' or q4 == 'Hard'):
        return {
            'risk_level': 'R3',
            'rationale': 'Safety/legal/compliance worst case with automated actions or hard-to-reverse consequences',
            'confidence': 'HIGH'
        }

    if q7 == 'Yes':  # Formally regulated
        return {
            'risk_level': 'R3',
            'rationale': 'Formally regulated project',
            'confidence': 'HIGH'
        }

    if q3 == 'Safety_Legal_Compliance':
        # Safety/legal but with some mitigating factors
        # Still likely R3, but could be R2 with justification
        if q4 == 'Easy' and q1 == 'Internal' and q6 in ['Individual', 'Team']:
            return {
                'risk_level': 'R2',  # Could argue R3
                'rationale': 'Safety/legal/compliance worst case BUT easy reversibility, internal use, small scale',
                'confidence': 'MEDIUM',
                'borderline': True,
                'alternative': 'R3',
                'requires_review': True
            }
        else:
            return {
                'risk_level': 'R3',
                'rationale': 'Safety/legal/compliance worst case',
                'confidence': 'HIGH'
            }

    # R2 Triggers
    if q1 in ['External', 'Public']:
        return {
            'risk_level': 'R2',
            'rationale': 'External or public users',
            'confidence': 'HIGH'
        }

    if q2 == 'Automated' and q3 != 'Annoyance':
        return {
            'risk_level': 'R2',
            'rationale': 'Automated actions with non-trivial impact',
            'confidence': 'HIGH'
        }

    if q7 == 'Possibly':  # Possibly regulated/auditable
        return {
            'risk_level': 'R2',
            'rationale': 'Possibly regulated or auditable',
            'confidence': 'MEDIUM'
        }

    if q2 == 'Recommendations' and q3 in ['Financial', 'Safety_Legal_Compliance', 'Reputational']:
        return {
            'risk_level': 'R2',
            'rationale': 'Recommendations with significant impact (decision-influencing)',
            'confidence': 'MEDIUM'
        }

    if q6 == 'Organization_Public' and q3 != 'Annoyance':
        return {
            'risk_level': 'R2',
            'rationale': 'Organization-wide scale with non-trivial impact',
            'confidence': 'MEDIUM'
        }

    # R1 Triggers
    if q2 == 'Recommendations' and q3 == 'Annoyance':
        return {
            'risk_level': 'R1',
            'rationale': 'Recommendations with low impact',
            'confidence': 'MEDIUM'
        }

    if q3 in ['Financial', 'Reputational'] and q1 == 'Internal' and q4 in ['Easy', 'Partial']:
        return {
            'risk_level': 'R1',
            'rationale': 'Moderate impact, internal use, reversible',
            'confidence': 'MEDIUM'
        }

    if q6 in ['Team', 'Multi_team'] and q3 != 'Annoyance':
        return {
            'risk_level': 'R1',
            'rationale': 'Team/multi-team scale with moderate impact',
            'confidence': 'MEDIUM'
        }

    # R0 Triggers
    if q3 == 'Annoyance' and q4 == 'Easy' and q1 == 'Internal' and q6 in ['Individual', 'Team']:
        return {
            'risk_level': 'R0',
            'rationale': 'Low impact, fully reversible, internal, small scale',
            'confidence': 'HIGH'
        }

    # Default: R1 (conservative)
    return {
        'risk_level': 'R1',
        'rationale': 'Default moderate classification (no clear R0 or R2+ triggers)',
        'confidence': 'LOW',
        'note': 'Consider expert review for borderline case'
    }
```

---

## Layer 5: Expert Review Triggers

```python
def check_expert_review_needed(answers, validation_results, classification):
    """Determine if expert review should be triggered."""
    triggers = []

    # ER1: Multiple high-risk indicators
    high_risk_count = sum(1 for r in validation_results['rules_triggered']
                          if r.get('severity') == 'CRITICAL')
    medium_high_count = sum(1 for r in validation_results['rules_triggered']
                             if r.get('severity') == 'MEDIUM_HIGH')

    if high_risk_count >= 2:
        triggers.append({
            'trigger_id': 'ER1',
            'reason': f'{high_risk_count} CRITICAL risk indicators detected',
            'mandatory': True
        })

    if medium_high_count >= 3:
        triggers.append({
            'trigger_id': 'ER1',
            'reason': f'{medium_high_count} MEDIUM-HIGH risk indicators detected',
            'mandatory': False
        })

    # ER2: Contradictory answers
    contradictions = [r for r in validation_results['rules_triggered']
                      if r.get('rule_id') in ['CV2', 'CV4']]
    if contradictions:
        triggers.append({
            'trigger_id': 'ER2',
            'reason': 'Contradictory answers detected',
            'mandatory': True
        })

    # ER3: Borderline classification
    if classification.get('borderline') or classification.get('confidence') == 'LOW':
        triggers.append({
            'trigger_id': 'ER3',
            'reason': 'Borderline or low-confidence classification',
            'mandatory': False
        })

    # ER5: Safety/legal + mitigating factors
    if answers.get('q3_worst_failure') == 'Safety_Legal_Compliance' and classification.get('risk_level') == 'R2':
        triggers.append({
            'trigger_id': 'ER5',
            'reason': 'Safety/legal worst case with R2 classification (not R3)',
            'mandatory': False,
            'requires_justification': True
        })

    return {
        'expert_review_triggered': len(triggers) > 0,
        'mandatory': any(t.get('mandatory') for t in triggers),
        'triggers': triggers
    }
```

---

## Complete Intake Validation Pipeline

```python
def validate_and_classify_intake(answers):
    """
    Complete validation and classification pipeline.
    Returns classification result with all validation checks.
    """
    result = {
        'intake_valid': True,
        'classification': None,
        'validation_checks': [],
        'warnings': [],
        'indicators': [],
        'expert_review': {}
    }

    # Layer 1: Input Validation
    all_answered = validate_all_answered(answers)
    if not all_answered['valid']:
        result['intake_valid'] = False
        result['validation_checks'].append(all_answered)
        return result

    option_validation = validate_option_values(answers)
    if not option_validation['valid']:
        result['intake_valid'] = False
        result['validation_checks'].append(option_validation)
        return result

    # Layer 2: Cross-Validation
    cross_validation_rules = [
        check_automated_high_impact,
        check_informational_contradiction,
        check_recommendations_safety,
        check_internal_public_contradiction,
        check_unregulated_safety
    ]

    for rule in cross_validation_rules:
        check_result = rule(answers)
        if check_result['triggered']:
            result['warnings'].append(check_result)

    # Layer 3: Risk Indicators
    indicator_checks = [
        check_safety_indicator,
        check_financial_scale_indicator,
        check_partial_reversibility_indicator,
        check_domain_uncertainty_indicator
    ]

    for indicator in indicator_checks:
        indicator_result = indicator(answers)
        if indicator_result['triggered']:
            result['indicators'].append(indicator_result)

    # Layer 4: Risk Classification
    classification = classify_risk(answers)
    result['classification'] = classification

    # Layer 5: Expert Review
    expert_review = check_expert_review_needed(answers, result, classification)
    result['expert_review'] = expert_review

    return result
```

---

## Testing Requirements

### Unit Tests Required

**Test Suite 1: Input Validation**
- Test V1: Missing answer detection
- Test V2: Invalid option values

**Test Suite 2: Cross-Validation**
- Test CV1: All combinations of (Automated, Low reversibility, High impact)
- Test CV2: Informational + Hard reversibility
- Test CV3: Recommendations + Safety/legal
- Test CV4: Internal + Organization-wide scale
- Test CV5: Not regulated + Safety worst case

**Test Suite 3: Risk Indicators**
- Test I1: Safety/legal/compliance always flags
- Test I2: Financial + Scale combinations
- Test I3: Partial reversibility + High impact
- Test I4: Domain uncertainty + High stakes

**Test Suite 4: Classification Logic**
- Test R0: All R0-qualifying combinations
- Test R1: All R1-qualifying combinations
- Test R2: All R2-qualifying combinations
- Test R3: All R3-qualifying combinations
- Test Borderline: Edge cases between levels

**Test Suite 5: Expert Review Triggers**
- Test ER1: Multiple indicators
- Test ER2: Contradictions
- Test ER3: Borderline cases
- Test ER5: Safety + R2 classification

### Integration Tests Required

- Full intake flow with all validation layers
- Warning acknowledgment workflow
- Expert review escalation
- Override and justification recording

---

## Implementation Notes

1. **Layer order matters** - Each layer builds on previous
2. **All warnings must be shown** - Don't hide any triggered rules
3. **User acknowledgment required** - For CRITICAL and HIGH severity warnings
4. **Expert review is advisory** - Unless mandatory flag set
5. **Log everything** - All validation results, warnings, classifications
6. **Traceability** - Link intake to generated artifacts

---

## Success Criteria

- All validation rules implemented and tested
- VER-001: Risk classification accuracy 100% on test cases
- VER-005: No silent skipping of validation checks
- M-001: Risk classification accuracy ≥95% in validation testing
- M-007: User comprehension ≥90% (understands warnings and classification)

---

**Version:** 1.0
**Related Documents:**
- intake-safety-mechanisms.md (design)
- intake-rules-enhanced.md (user-facing guidance)
- intake-analysis.md (issue identification)
