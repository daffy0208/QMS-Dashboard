# Phase 8A WS-1 Expansion: Complete the Foundation
## WS-1.7, WS-1.8, WS-1.9 - Detailed Execution Plan

**Date:** 2025-12-16
**Objective:** Complete artifact validation coverage before WS-2
**Scope:** Finish WS-1 properly (not scope creep - finish committed layer)
**Estimated Duration:** 3-4 days (mechanical work, pattern already established)

---

## Rationale (Engineering Justification)

**Why expand now:**
- Diagnostic layer is correct but incomplete (4/11 artifacts, R2/R3 only)
- WS-2 dependency logic depends on complete diagnostic signals
- Incomplete coverage → false "ready/blocked" states later
- This prevents unsafe systems from emerging accidentally

**Why not defer:**
- User testing now would surface known structural gaps (noise, not signal)
- Moving to WS-2 with partial diagnostics violates Teaching System principle
- Better to complete measurement layer before adding decision logic

**Result after expansion:**
- Artifact Health becomes authoritative across all risk levels
- WS-2 can be trusted, fast, and defensible
- No "silent skipping" possible
- System stops being clever, becomes safe

---

## Current State Analysis

### Coverage Status (Before Expansion)

**Artifacts with Acceptance Criteria:** 4/11
- ✅ Quality Plan (R2/R3)
- ✅ Risk Register (R2/R3)
- ✅ Verification Plan (R2/R3)
- ✅ Control Plan (R2/R3)

**Missing Acceptance Criteria:** 7/11
- ❌ CTQ Tree (R0/R1)
- ❌ Assumptions Register (R0/R1)
- ❌ Traceability Index (R0/R1)
- ❌ Validation Plan (R1)
- ❌ Measurement Plan (R1)
- ❌ Change Log (R2/R3)
- ❌ CAPA Log (R2/R3)

**Templates with Markers:** 2/11
- ✅ Quality Plan
- ✅ Risk Register
- ❌ 9 others

**Risk Levels Covered:** R2/R3 only
- ❌ R0 (5 artifacts)
- ❌ R1 (8 artifacts)

---

## WS-1.7: R0/R1 Acceptance Criteria

### Objective
Add lightweight, teaching-oriented criteria for R0/R1 projects.

### Design Principles (R0/R1 Specific)
1. **Warning-only semantics** - Issues are guidance, not blockers
2. **Teaching emphasis** - Explain why, not just what
3. **Minimal burden** - Don't over-police low-risk projects
4. **Completeness check** - Ensure artifact has substance (not empty shell)

### R0 Philosophy
- **Purpose:** Advisory quality activities
- **Validation:** Encouragement, not enforcement
- **Criteria:** Minimal (presence + basic structure)
- **Message:** "Consider adding..." not "You must fix..."

### R1 Philosophy
- **Purpose:** Conditional quality based on project needs
- **Validation:** Risk-aware guidance
- **Criteria:** Moderate (structure + key sections)
- **Message:** "Recommended..." not "Required..."

---

### WS-1.7.1: Quality Plan (R0/R1 criteria)

**Current:** Has R2/R3 criteria (4-5 required sections)

**Add R0 criteria:**
```json
"R0": {
  "required_sections": [
    "Purpose"
  ],
  "rules": {
    "placeholders_allowed": true,
    "min_sections_present": 1,
    "warning_only": true
  }
}
```

**Rationale:** R0 just needs to acknowledge project exists and has a purpose.

**Add R1 criteria:**
```json
"R1": {
  "required_sections": [
    "Purpose",
    "Scope",
    "Quality Objectives"
  ],
  "rules": {
    "placeholders_allowed": false,
    "min_sections_present": 3,
    "warning_only": false
  }
}
```

**Rationale:** R1 needs planning but not full governance.

---

### WS-1.7.2: Risk Register (R0/R1 criteria)

**Current:** Has R2/R3 criteria (3/5 risks minimum)

**Add R0 criteria:**
```json
"R0": {
  "rules": {
    "min_risks": 1,
    "required_fields": ["description"],
    "placeholders_allowed": true,
    "warning_only": true
  }
}
```

**Rationale:** R0 should identify at least one risk (teaching awareness).

**Add R1 criteria:**
```json
"R1": {
  "rules": {
    "min_risks": 2,
    "required_fields": ["id", "description", "mitigation"],
    "placeholders_allowed": false,
    "warning_only": false
  }
}
```

**Rationale:** R1 needs meaningful risk assessment with mitigations.

---

### WS-1.7.3: Verification Plan (R0/R1 criteria)

**Current:** Has R2/R3 criteria (2-3 required sections)

**Add R0 criteria:**
```json
"R0": {
  "required_sections": [
    "Test Approach"
  ],
  "rules": {
    "placeholders_allowed": true,
    "warning_only": true
  }
}
```

**Rationale:** R0 should think about testing, even if informal.

**Add R1 criteria:**
```json
"R1": {
  "required_sections": [
    "Verification Strategy",
    "Test Approach"
  ],
  "rules": {
    "placeholders_allowed": false,
    "warning_only": false
  }
}
```

**Rationale:** R1 needs formal test planning.

---

### WS-1.7 Deliverable
- Updated `acceptance_criteria.json` with R0/R1 for Quality Plan, Risk Register, Verification Plan
- 3 artifacts × 2 risk levels = 6 new criteria blocks
- Estimated: 1-1.5 hours

---

## WS-1.8: Remaining 7 Artifacts - Acceptance Criteria

### Artifact Classification (Minimal vs Moderate vs Full)

#### Tier 1: Full Criteria (Core Teaching Artifacts)
**Artifacts:** CTQ Tree, Validation Plan, Measurement Plan

**Why Full:**
- CTQ Tree: Defines what quality means (critical teaching moment)
- Validation Plan: Complements Verification Plan (paired importance)
- Measurement Plan: Teaches metrics-driven thinking

**Criteria Depth:**
- R0: 1-2 required sections, warning-only
- R1: 2-3 required sections, moderate rigor
- R2: 3-4 required sections, strict rigor
- R3: 4-5 required sections, maximum rigor

---

#### Tier 2: Moderate Criteria (Supporting Artifacts)
**Artifacts:** Assumptions Register, Traceability Index

**Why Moderate:**
- Important structure but less critical than core teaching
- Presence + basic structure checks sufficient
- Avoid over-policing documentation

**Criteria Depth:**
- R0: Presence check only (has content)
- R1: Basic structure (sections present)
- R2/R3: Key sections + format validation

---

#### Tier 3: Minimal Criteria (Audit Logs)
**Artifacts:** Change Log, CAPA Log

**Why Minimal:**
- These are living logs (content grows over time)
- Structure matters more than initial completeness
- Format validation > content validation

**Criteria Depth:**
- R0: Not required (optional)
- R1: Not required (optional)
- R2: Header + structure present
- R3: Header + structure + initial entry

---

### WS-1.8.1: CTQ Tree (Full Criteria)

**Purpose:** Critical-to-Quality analysis (what makes this project successful)

**R0 criteria:**
```json
"CTQ Tree": {
  "description": "Critical-to-Quality tree mapping user needs to measurable requirements",
  "risk_levels": {
    "R0": {
      "required_sections": ["User Needs"],
      "rules": {
        "placeholders_allowed": true,
        "warning_only": true,
        "min_items": 1
      }
    }
  }
}
```

**R1 criteria:**
```json
"R1": {
  "required_sections": ["User Needs", "Quality Drivers"],
  "rules": {
    "placeholders_allowed": false,
    "min_items": 2
  }
}
```

**R2 criteria:**
```json
"R2": {
  "required_sections": ["User Needs", "Quality Drivers", "Measurable Requirements"],
  "rules": {
    "placeholders_allowed": false,
    "min_items": 3
  }
}
```

**R3 criteria:**
```json
"R3": {
  "required_sections": ["User Needs", "Quality Drivers", "Measurable Requirements", "Traceability"],
  "rules": {
    "placeholders_allowed": false,
    "min_items": 5
  }
}
```

---

### WS-1.8.2: Validation Plan (Full Criteria)

**Purpose:** User acceptance testing strategy

**R0 criteria:**
```json
"Validation Plan": {
  "description": "Validation strategy ensuring system solves intended user problems",
  "risk_levels": {
    "R0": {
      "required_sections": ["Validation Approach"],
      "rules": {
        "placeholders_allowed": true,
        "warning_only": true
      }
    }
  }
}
```

**R1 criteria:**
```json
"R1": {
  "required_sections": ["Validation Approach", "User Scenarios"],
  "rules": {
    "placeholders_allowed": false
  }
}
```

**R2/R3 criteria:**
```json
"R2": {
  "required_sections": ["Validation Approach", "User Scenarios", "Acceptance Criteria"],
  "rules": {
    "placeholders_allowed": false
  }
},
"R3": {
  "required_sections": ["Validation Approach", "User Scenarios", "Acceptance Criteria", "Validation Report"],
  "rules": {
    "placeholders_allowed": false
  }
}
```

---

### WS-1.8.3: Measurement Plan (Full Criteria)

**Purpose:** Metrics and monitoring strategy

**R0 criteria:**
```json
"Measurement Plan": {
  "description": "Metrics for monitoring system quality and performance",
  "risk_levels": {
    "R0": {
      "required_sections": ["Key Metrics"],
      "rules": {
        "placeholders_allowed": true,
        "warning_only": true,
        "min_metrics": 1
      }
    }
  }
}
```

**R1 criteria:**
```json
"R1": {
  "required_sections": ["Key Metrics", "Measurement Approach"],
  "rules": {
    "placeholders_allowed": false,
    "min_metrics": 2
  }
}
```

**R2/R3 criteria:**
```json
"R2": {
  "required_sections": ["Key Metrics", "Measurement Approach", "Targets"],
  "rules": {
    "placeholders_allowed": false,
    "min_metrics": 3
  }
},
"R3": {
  "required_sections": ["Key Metrics", "Measurement Approach", "Targets", "Monitoring Frequency"],
  "rules": {
    "placeholders_allowed": false,
    "min_metrics": 5
  }
}
```

---

### WS-1.8.4: Assumptions Register (Moderate Criteria)

**Purpose:** Document critical assumptions and their validity

**R0 criteria:**
```json
"Assumptions Register": {
  "description": "Critical assumptions that if wrong would invalidate project approach",
  "risk_levels": {
    "R0": {
      "rules": {
        "min_content_length": 100,
        "warning_only": true
      }
    }
  }
}
```

**R1 criteria:**
```json
"R1": {
  "required_sections": ["Critical Assumptions"],
  "rules": {
    "min_assumptions": 1,
    "placeholders_allowed": false
  }
}
```

**R2/R3 criteria:**
```json
"R2": {
  "required_sections": ["Critical Assumptions", "Validation Status"],
  "rules": {
    "min_assumptions": 3,
    "placeholders_allowed": false
  }
},
"R3": {
  "required_sections": ["Critical Assumptions", "Validation Status", "Risk if Wrong"],
  "rules": {
    "min_assumptions": 5,
    "placeholders_allowed": false
  }
}
```

---

### WS-1.8.5: Traceability Index (Moderate Criteria)

**Purpose:** Link requirements → risks → tests

**R0 criteria:**
```json
"Traceability Index": {
  "description": "Traceability matrix linking requirements to verification",
  "risk_levels": {
    "R0": {
      "rules": {
        "min_content_length": 100,
        "warning_only": true
      }
    }
  }
}
```

**R1 criteria:**
```json
"R1": {
  "required_sections": ["Traceability Matrix"],
  "rules": {
    "min_entries": 3,
    "placeholders_allowed": false
  }
}
```

**R2/R3 criteria:**
```json
"R2": {
  "required_sections": ["Traceability Matrix", "Coverage Analysis"],
  "rules": {
    "min_entries": 5,
    "placeholders_allowed": false
  }
},
"R3": {
  "required_sections": ["Traceability Matrix", "Coverage Analysis", "Gap Analysis"],
  "rules": {
    "min_entries": 10,
    "placeholders_allowed": false
  }
}
```

---

### WS-1.8.6: Change Log (Minimal Criteria)

**Purpose:** Audit trail of changes

**R2/R3 criteria only:**
```json
"Change Log": {
  "description": "Audit trail of project changes with rationale",
  "risk_levels": {
    "R2": {
      "required_sections": ["Change History"],
      "rules": {
        "has_header": true,
        "has_structure": true
      }
    },
    "R3": {
      "required_sections": ["Change History"],
      "rules": {
        "has_header": true,
        "has_structure": true,
        "min_entries": 1
      }
    }
  }
}
```

**Note:** R0/R1 don't require Change Log, so no criteria needed.

---

### WS-1.8.7: CAPA Log (Minimal Criteria)

**Purpose:** Corrective and Preventive Action tracking

**R2/R3 criteria only:**
```json
"CAPA Log": {
  "description": "Corrective and Preventive Action log for continuous improvement",
  "risk_levels": {
    "R2": {
      "required_sections": ["CAPA Entries"],
      "rules": {
        "has_header": true,
        "has_structure": true
      }
    },
    "R3": {
      "required_sections": ["CAPA Entries"],
      "rules": {
        "has_header": true,
        "has_structure": true,
        "min_entries": 1
      }
    }
  }
}
```

**Note:** R0/R1 don't require CAPA Log, so no criteria needed.

---

### WS-1.8 Deliverable
- Updated `acceptance_criteria.json` with 7 new artifacts
- CTQ Tree: 4 risk levels (R0-R3)
- Validation Plan: 4 risk levels
- Measurement Plan: 4 risk levels
- Assumptions Register: 4 risk levels
- Traceability Index: 4 risk levels
- Change Log: 2 risk levels (R2/R3)
- CAPA Log: 2 risk levels (R2/R3)

**Estimated:** 3-4 hours

---

## WS-1.9: Template Markers for Remaining 9 Artifacts

### Objective
Add HTML comment markers to remaining templates (same pattern as Quality Plan / Risk Register).

### Marker Strategy
1. **VALIDATION block** at top - explains criteria for this artifact
2. **REQUIRED[Rx,Ry]** markers - inline markers for required sections
3. **Invisible to users** - HTML comments don't render in markdown
4. **Parseable by validator** - structured format for automated checking

### Template List

**Already have markers (2):**
- ✅ Quality Plan
- ✅ Risk Register

**Need markers (9):**
1. CTQ Tree
2. Assumptions Register
3. Traceability Index
4. Verification Plan
5. Validation Plan
6. Measurement Plan
7. Control Plan
8. Change Log
9. CAPA Log

---

### WS-1.9 Implementation Pattern

**Example marker block (CTQ Tree):**
```python
content = f"""# CTQ Tree
## {project_name}

<!-- VALIDATION: CTQ Tree requirements
     R0: User Needs section (1 item minimum)
     R1: User Needs + Quality Drivers (2 items minimum)
     R2: User Needs + Quality Drivers + Measurable Requirements (3 items)
     R3: Full tree with Traceability (5 items minimum)
-->

## User Needs
<!-- REQUIRED[R0,R1,R2,R3]: What users need from this system -->

## Quality Drivers
<!-- REQUIRED[R1,R2,R3]: What makes quality for this system -->

## Measurable Requirements
<!-- REQUIRED[R2,R3]: Quantifiable requirements -->

## Traceability
<!-- REQUIRED[R3]: Links to other artifacts -->
"""
```

**Implementation steps per template:**
1. Read template file
2. Add VALIDATION block after title
3. Add REQUIRED markers to key sections
4. Keep risk-level scoping accurate (R0/R1/R2/R3)
5. Test: Generate artifact, verify markers invisible in rendered markdown

---

### WS-1.9 Deliverable
- 9 template files modified
- ~5-10 lines of markers per template
- Total: ~90 lines of markers

**Estimated:** 1.5-2 hours

---

## Validator Updates Required

### WS-1.9.1: Update validator.py for new validation rules

**New validation types needed:**

1. **min_items check** (for CTQ Tree, Measurement Plan)
   - Count items in a section
   - Example: "At least 3 quality drivers"

2. **min_metrics check** (for Measurement Plan)
   - Count metric definitions
   - Example: "At least 5 key metrics"

3. **min_assumptions check** (for Assumptions Register)
   - Count assumption entries
   - Example: "At least 3 critical assumptions"

4. **min_entries check** (for Traceability Index, Change Log, CAPA Log)
   - Count table/list entries
   - Example: "At least 1 CAPA entry"

5. **has_header check** (for logs)
   - Verify log has proper header structure

6. **has_structure check** (for logs)
   - Verify log has proper table/list structure

7. **min_content_length check** (for lightweight checks)
   - Verify artifact isn't empty shell
   - Example: "At least 100 characters of content"

**Implementation:**
- Add new validation methods to ArtifactValidator class
- Extend `_validate_artifact_specific()` to handle each artifact type
- Keep deterministic (no AI/heuristics)

**Estimated:** 2-3 hours

---

## Testing Strategy

### WS-1.9.2: Expand test_ws1_artifact_health.py

**New test cases:**

1. **R0 Project Test**
   - Create R0 intake
   - Generate 5 R0 artifacts
   - Verify warning-only validation
   - Verify teaching-oriented messages

2. **R1 Project Test**
   - Create R1 intake
   - Generate 8 R1 artifacts
   - Verify moderate rigor validation
   - Verify all 8 artifacts validated

3. **R2/R3 Expanded Test**
   - Test all 11 artifacts (not just 4)
   - Verify full coverage

4. **Artifact-Specific Tests**
   - CTQ Tree: min_items validation
   - Measurement Plan: min_metrics validation
   - Assumptions Register: min_assumptions validation
   - Traceability Index: min_entries validation
   - Change Log: structure validation
   - CAPA Log: structure validation

**Estimated:** 1-2 hours

---

## Execution Checklist

### Phase 1: R0/R1 Criteria (WS-1.7)
- [ ] Add R0/R1 criteria to Quality Plan
- [ ] Add R0/R1 criteria to Risk Register
- [ ] Add R0/R1 criteria to Verification Plan
- [ ] Update acceptance_criteria.json
- [ ] Test: Create R0 intake, verify validation
- [ ] Test: Create R1 intake, verify validation
- [ ] Commit: "WS-1.7: R0/R1 acceptance criteria"

**Estimated:** 1-1.5 hours

---

### Phase 2: Remaining 7 Artifacts (WS-1.8)
- [ ] Add CTQ Tree criteria (R0-R3)
- [ ] Add Validation Plan criteria (R0-R3)
- [ ] Add Measurement Plan criteria (R0-R3)
- [ ] Add Assumptions Register criteria (R0-R3)
- [ ] Add Traceability Index criteria (R0-R3)
- [ ] Add Change Log criteria (R2/R3)
- [ ] Add CAPA Log criteria (R2/R3)
- [ ] Update acceptance_criteria.json
- [ ] Commit: "WS-1.8: Remaining 7 artifacts acceptance criteria"

**Estimated:** 3-4 hours

---

### Phase 3: Validator Extensions (WS-1.9.1)
- [ ] Add `_validate_min_items()` method
- [ ] Add `_validate_min_metrics()` method
- [ ] Add `_validate_min_assumptions()` method
- [ ] Add `_validate_min_entries()` method
- [ ] Add `_validate_has_header()` method
- [ ] Add `_validate_has_structure()` method
- [ ] Add `_validate_min_content_length()` method
- [ ] Extend `validate_artifact()` to use new methods
- [ ] Test each new validation type
- [ ] Commit: "WS-1.9: Validator extensions for new criteria"

**Estimated:** 2-3 hours

---

### Phase 4: Template Markers (WS-1.9)
- [ ] Add markers to ctq_tree.py
- [ ] Add markers to assumptions_register.py
- [ ] Add markers to traceability_index.py
- [ ] Add markers to verification_plan.py
- [ ] Add markers to validation_plan.py
- [ ] Add markers to measurement_plan.py
- [ ] Add markers to control_plan.py
- [ ] Add markers to change_log.py
- [ ] Add markers to capa_log.py
- [ ] Test: Generate each artifact, verify markers invisible
- [ ] Commit: "WS-1.9: Template markers for remaining 9 artifacts"

**Estimated:** 1.5-2 hours

---

### Phase 5: Testing (WS-1.9.2)
- [ ] Add R0 project test
- [ ] Add R1 project test
- [ ] Add R2/R3 expanded test (11 artifacts)
- [ ] Add CTQ Tree validation test
- [ ] Add Measurement Plan validation test
- [ ] Add Assumptions Register validation test
- [ ] Add Traceability Index validation test
- [ ] Add Change Log validation test
- [ ] Add CAPA Log validation test
- [ ] Run all tests, verify pass
- [ ] Run Phase 6 regression tests, verify still pass
- [ ] Commit: "WS-1: Complete expansion with full test coverage"

**Estimated:** 1-2 hours

---

### Phase 6: Documentation
- [ ] Update PHASE-8A-WS1-COMPLETION.md
- [ ] Add "WS-1 Expansion Complete" section
- [ ] Update coverage stats (4/11 → 11/11, R2/R3 → R0-R3)
- [ ] Create PHASE-8A-WS1-FINAL-REPORT.md
- [ ] Commit: "WS-1: Final expansion report"

**Estimated:** 30 min

---

## Total Estimated Duration

**Breakdown:**
- WS-1.7: 1-1.5 hours
- WS-1.8: 3-4 hours
- WS-1.9.1: 2-3 hours
- WS-1.9: 1.5-2 hours
- WS-1.9.2: 1-2 hours
- Documentation: 0.5 hours

**Total:** 9.5-13 hours (1.5-2 days of focused work, 3-4 days with breaks)

---

## Success Criteria

### Quantitative:
- ✅ 11/11 artifacts have acceptance criteria
- ✅ R0, R1, R2, R3 all covered
- ✅ 11/11 templates have validation markers
- ✅ Validator handles all artifact types
- ✅ Phase 6 regression tests still pass
- ✅ New tests pass (R0, R1, all 11 artifacts)

### Qualitative:
- ✅ R0/R1 validation is teaching-oriented (warning-only where appropriate)
- ✅ R2/R3 validation remains strict
- ✅ Messaging discipline maintained (descriptive, not prescriptive)
- ✅ Artifact Health API authoritative across all risk levels
- ✅ System prevents silent skipping of quality activities

---

## Result: System State After WS-1 Expansion

**Before Expansion:**
- Diagnostic capability: Partial (4/11, R2/R3 only)
- Safe to build WS-2: No (false ready/blocked states)
- Teaching system: Foundation only

**After Expansion:**
- Diagnostic capability: Complete (11/11, R0-R3)
- Safe to build WS-2: Yes (trustworthy signals)
- Teaching system: Fully operational measurement layer

**What this enables:**
- WS-2 Dependency Management can be trusted
- Smart Next Steps won't hallucinate readiness
- WS-4 Simulation has solid signal base
- AI assistants cannot "skip" quality silently
- System stops being clever, becomes safe

---

## Next Step (Immediate)

**If you approve this plan:**

> **Start WS-1.7: Add R0/R1 acceptance criteria to Quality Plan, Risk Register, Verification Plan**

This is the smallest, cleanest starting point. Should take ~1-1.5 hours.

After WS-1.7 complete:
- Can test R0/R1 validation immediately
- Validates the pattern before scaling to 7 more artifacts
- Builds confidence in approach

**Ready to proceed?**
