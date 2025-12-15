# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **QMS (Quality Management System) Dashboard** project implementing a risk-based quality framework for software projects. The system enforces structured quality intake processes to determine project risk levels and required quality artifacts.

## Core Architecture

### Quality Kernel Override

The `QUALITY_KERNEL.md` file defines special initialization behavior:
- When `/init` is run, **do NOT generate application code first**
- Must read `intake-rules.md` and run quality intake before implementation
- Risk classification and rigor mode determine what gets built
- All required quality artifacts must be generated before build steps

### Risk-Based Framework

The system implements a 4-tier risk classification (R0-R3):
- **R0**: Internal, low impact, fully reversible → Advisory rigor
- **R1**: Internal, moderate impact, reversible → Conditional rigor
- **R2**: External users, decision-impacting, or auditable → Strict rigor
- **R3**: Safety, legal, financial, or hard-to-reverse → Strict rigor (no downgrade)

Risk determines which quality artifacts are mandatory.

### Quality Artifacts System

All projects require baseline artifacts:
- Quality Plan
- CTQ (Critical to Quality) Tree
- Assumptions Register
- Risk Register
- Traceability Index

Additional artifacts cascade based on risk level:
- **R1+**: Verification Plan, Validation Plan, Measurement Plan
- **R2+**: Control Plan, Change Log, CAPA Log

### No Silent Skipping Rule

Every artifact must have explicit status:
- **Done**: Artifact completed
- **Deferred**: Delayed with documented trigger condition
- **Deviated**: Skipped with formal approval record

Missing this creates non-compliance.

## Development Workflow

### Initialization Sequence

1. Run quality intake (7 mandatory questions in `intake-rules.md:9-45`)
2. Classify risk level (R0-R3) based on answers
3. Select rigor mode (Advisory/Conditional/Strict)
4. Generate required QMS artifact files
5. Populate first-pass CTQs, risks, and assumptions
6. **Stop and request confirmation** before implementation begins

### When Working on This Project

- Always check if quality intake has been completed before suggesting code changes
- When uncertain about risk level, select the higher risk classification
- Any rigor downgrade requires creating a deviation record
- Implementation decisions should reference the CTQ Tree and Risk Register
- Track all assumptions that could affect quality or compliance

## Key Principles

- **Risk-first approach**: Risk level drives all quality decisions
- **Mandatory traceability**: Requirements → Tests → Implementation must be linked
- **Explicit approval required**: Cannot skip artifacts silently
- **Stop-before-build**: Quality planning completes before coding starts

## File References

- Quality intake questions: `intake-rules.md:9-45`
- Risk classification rules: `intake-rules.md:48-55`
- Rigor mode mapping: `intake-rules.md:59-67`
- Artifact requirements: `intake-rules.md:70-88`
- Initialization override: `QUALITY_KERNEL.md:3-10`
