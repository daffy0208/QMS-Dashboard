# Quality Intake Rules (Project-Agnostic)

## Purpose
Define the mandatory quality intake used at project start to determine
risk, rigor, and required QMS artefacts.

---

## 1. Mandatory Intake Questions (ask in this order)

1. Who are the users?
   - Internal / External / Public

2. What decisions or actions will this system influence?
   - Informational only
   - Recommendations
   - Automated actions

3. What is the worst credible failure?
   - Annoyance
   - Financial loss
   - Safety / legal / compliance
   - Reputational damage

4. How reversible are failures?
   - Easy
   - Partial
   - Hard / irreversible

5. Is the domain well understood?
   - Yes
   - Partially
   - No (research required)

6. What is the expected scale?
   - Individual
   - Team
   - Multi-team
   - Organization-wide / public

7. Is the project regulated or auditable?
   - No
   - Possibly
   - Yes

---

## 2. Risk Classification (R0–R3)

- **R0:** Internal, low impact, fully reversible
- **R1:** Internal, moderate impact, reversible
- **R2:** External users, decision-impacting, or auditable
- **R3:** Safety, legal, financial, or hard-to-reverse consequences

If uncertain, select the higher risk.

---

## 3. Rigor Mode Selection

- R0 → Advisory
- R1 → Conditional
- R2 → Strict
- R3 → Strict (no downgrade)

Any downgrade requires a deviation record.

---

## 4. Required QMS Artefacts (by default)

All projects generate:
- Quality Plan
- CTQ Tree
- Assumptions Register
- Risk Register
- Traceability Index

Additional artefacts required when risk ≥ R1:
- Verification Plan
- Validation Plan
- Measurement Plan

Additional artefacts required when risk ≥ R2:
- Control Plan
- Change Log
- CAPA Log

---

## 5. No Silent Skipping Rule

Every artefact must be marked as:
- Done
- Deferred (with trigger)
- Deviated (with approval)

---

## 6. Output Requirement

After intake, the system must:
- Record risk class and rigor
- Generate required QMS files
- Populate first-pass CTQs, risks, and assumptions
- Stop and request confirmation before implementation
