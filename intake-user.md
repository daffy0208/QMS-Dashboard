# Project Quality Intake
**Version 1.0**

**Purpose:** Answer 7 questions to determine your project's quality management needs. Takes about 5-10 minutes.

---

## The 7 Questions

### 1. Who are the users?

- [ ] **Internal** - Only people in your organization
- [ ] **External** - Specific clients, partners, or vendors
- [ ] **Public** - Anyone (general public)

<details>
<summary>💡 Examples</summary>

**Internal:** Employee dashboard, internal API, team tool
**External:** Client portal, partner integration, B2B product
**Public:** Public website, mobile app, open-source tool

</details>

---

### 2. What decisions or actions will this system influence?

- [ ] **Informational only** - Shows data, people verify independently
- [ ] **Recommendations** - Suggests actions, people usually follow
- [ ] **Automated actions** - System does things automatically

<details>
<summary>💡 Examples</summary>

**Informational:** Status dashboard, log viewer, monitoring display
**Recommendations:** Code review suggestions, risk assessment, diagnosis assistant
**Automated:** Auto-deploy, auto-trading, auto-billing, safety shutoff

**Key question:** If this gives wrong info, would people notice before acting on it?
- If YES → Informational
- If NO → Recommendations or Automated

</details>

---

### 3. What is the worst realistic failure?

- [ ] **Annoyance** - Minor inconvenience, easily fixed
- [ ] **Financial loss** - Money lost, business costs
- [ ] **Safety / legal / compliance** - Someone hurt, legal trouble, violations
- [ ] **Reputational damage** - Brand harm, trust loss

<details>
<summary>💡 Examples</summary>

**Annoyance:** UI glitch, slow performance, temporary outage
**Financial loss:** Wrong billing, service downtime costs, data error costs money
**Safety/legal/compliance:** Medical error → patient harm, safety failure → injury, compliance violation → fines
**Reputational damage:** Public data breach, offensive content, major service failure

**Think about:** Direct AND indirect consequences. What happens if people trust wrong information?

</details>

---

### 4. How easily can failures be fixed?

Can you undo the **consequences** (not just fix the bug)?

- [ ] **Easy** - Quick to fix, no lasting harm
- [ ] **Partial** - Some things can be undone, some can't
- [ ] **Hard / irreversible** - Damage is done, can't be undone

<details>
<summary>💡 Examples</summary>

**Easy:** Display bug → refresh → fixed; Config error → rollback → restored
**Partial:** Wrong data sent → can send correction, but trust damaged
**Hard/irreversible:** Patient already harmed, money already lost, data permanently deleted

**Important:** Think about fixing **consequences**, not fixing **code**.

</details>

---

### 5. Do you understand the problem domain?

- [ ] **Yes** - Team has experience, requirements are clear
- [ ] **Partially** - Some knowledge, but gaps remain
- [ ] **No** - New domain, needs research

<details>
<summary>💡 Examples</summary>

**Yes:** Building your 10th web app, standard CRUD, well-known technology
**Partially:** New domain but standards exist, evolving requirements
**No:** Cutting-edge AI/ML, new regulatory environment, requires specialized expertise

**Be honest:** Uncertainty is risk.

</details>

---

### 6. How many people will use this?

Think about the **final state**, not just the prototype.

- [ ] **Individual** - Just you or one person
- [ ] **Team** - One team (5-15 people)
- [ ] **Multi-team** - Multiple teams in your organization
- [ ] **Organization-wide / public** - Entire company or external users

<details>
<summary>💡 Examples</summary>

**Individual:** Personal script, your own tool
**Team:** Team dashboard, squad tool
**Multi-team:** Company-wide service, cross-functional platform
**Organization-wide/public:** Customer product, public API, company-critical infrastructure

</details>

---

### 7. Is this project regulated or auditable?

- [ ] **No** - No regulations, no audits
- [ ] **Possibly** - Might be audited, or unclear
- [ ] **Yes** - Definitely regulated or audited

<details>
<summary>💡 Examples</summary>

**No:** Internal tool, personal project, non-critical prototype
**Possibly:** Used in regulated industry, internal compliance, future regulation possible
**Yes:** Medical device (FDA/EMA), financial system (SEC), pharmaceutical (GAMP 5), personal data (GDPR)

**Not sure?** Choose "Possibly" to be safe.

</details>

---

## What Happens Next

1. System analyzes your answers
2. Risk level calculated (R0=low, R1=medium, R2=high, R3=critical)
3. Warnings shown if anything looks contradictory or high-risk
4. Quality plan generated with required activities

**You might see:**
- ✅ Classification successful - your quality plan is ready
- ⚠️ Warnings or questions - something needs clarification
- 🔍 Expert review recommended - an expert will confirm classification

**Tips:**
- Be honest about your project's reality
- Choose higher risk when uncertain (safer to over-prepare)
- Ask for help if you're unsure

---

**Need more detail?** See intake-rules-enhanced.md for comprehensive guidance
**Questions?** Contact the QMS team or request expert review

**Version:** 1.0
**Date:** 2025-12-12
