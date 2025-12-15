# Quality Intake Rules (Enhanced with Guidance)
## Project-Agnostic Risk Assessment

**Version:** 2.0 (Enhanced)
**Date:** 2025-12-12
**Replaces:** intake-rules.md (v1.0)
**Changes:** Added examples, guidance, clarifications for each question

---

## Purpose
Define the mandatory quality intake used at project start to determine risk, rigor, and required QMS artifacts. This enhanced version includes guidance and examples to improve comprehension and reduce misclassification risk.

---

## How to Use This Intake

1. **Answer all 7 questions honestly** - There are no "wrong" answers, only accurate or inaccurate ones
2. **Think about real-world consequences** - Not just technical failures
3. **Consider future state** - Not just current prototype
4. **When uncertain → Select higher risk** - Better to over-engineer than under-engineer safety
5. **Request expert review if unsure** - It's okay to ask for help

---

## 1. Mandatory Intake Questions

### Q1: Who are the users?

**Question:** Who will use or interact with this system?

**Options:**
- ☐ **Internal** - Only people within your organization
- ☐ **External** - Specific external parties (clients, partners, vendors)
- ☐ **Public** - Anyone (general public, unrestricted access)

**Guidance:**
- Choose based on **actual users**, not just who has access to the code
- If users change over time (internal prototype → external product), choose the **eventual state**
- "Internal" includes employees, but NOT contractors/partners/subsidiaries unless they're treated as employees
- If the system **affects** external parties (even indirectly), consider "External"

**Examples:**
- ✅ **Internal:** Employee productivity tool, internal dashboard, CI/CD pipeline
- ✅ **External:** Client portal, partner API, vendor integration, B2B SaaS product
- ✅ **Public:** Public website, mobile app, open-source tool, public API

**Edge Cases:**
- Internal tool that processes external customer data → **External** (affects external parties)
- Prototype that will eventually be public → **Public** (plan for end state)
- Internal team tool used by contractors → **Internal** (if contractors treated as team members)

---

### Q2: What decisions or actions will this system influence?

**Question:** How does this system affect human or automated decisions?

**Options:**
- ☐ **Informational only** - Provides data, but users independently verify and decide
- ☐ **Recommendations** - Suggests actions, users typically follow but can override
- ☐ **Automated actions** - System directly executes actions without human approval

**Guidance:**
- Think about **how users actually behave**, not ideal behavior
- If users **trust** the system and follow its output → It's decision-influencing
- "Informational only" means users have **independent verification methods**
- If system failure would cause wrong decisions → It's decision-influencing

**Examples:**
- ✅ **Informational only:**
  - Raw data dashboard where users verify data independently
  - Logging system (users analyze logs themselves)
  - Status page showing system health (users investigate issues independently)

- ✅ **Recommendations:**
  - Medical diagnosis assistant (doctor makes final call)
  - Code review suggestions (developer can ignore)
  - Quality management guidance ← **Our QMS Dashboard**
  - Risk assessment tool (user validates results)
  - Fraud detection alerts (analyst reviews)

- ✅ **Automated actions:**
  - Auto-trading system (executes trades automatically)
  - CI/CD deployment (deploys without approval)
  - Auto-moderation (bans users automatically)
  - Auto-billing (charges customers automatically)
  - Safety shutoff system (stops machinery automatically)

**Critical Question:** If this system provides wrong information, would users notice **before** acting on it?
- If YES → Informational
- If NO → Recommendations or Automated

**Edge Cases:**
- Dashboard that users "just use" without verification → **Recommendations** (implicit trust)
- Recommendations that are "almost always followed" → **Recommendations** (or Automated if no override)
- System that recommends then auto-executes after timeout → **Automated**

---

### Q3: What is the worst credible failure?

**Question:** What is the worst **realistic** consequence if this system fails?

**Options:**
- ☐ **Annoyance** - Minor inconvenience, temporary disruption, frustration
- ☐ **Financial loss** - Money lost, business costs, revenue impact
- ☐ **Safety / legal / compliance** - Physical harm, legal liability, regulatory violations
- ☐ **Reputational damage** - Brand harm, trust loss, bad publicity

**Guidance:**
- **"Credible"** means: Could reasonably happen (not theoretical worst case)
  - Probability > 1% over system lifetime, OR
  - Has happened in similar systems, OR
  - No technical safeguards prevent it
- Think about **indirect consequences**, not just direct failures
- Consider **downstream impact** of wrong information/actions
- If multiple apply, choose the **most severe**
- Err on the side of **higher impact** if uncertain

**Examples:**

**Annoyance:**
- UI bug causes confusion (fixed in minutes)
- Typo in documentation
- Slow performance on non-critical feature
- Non-critical feature breaks temporarily

**Financial Loss:**
- Wrong billing calculation → Customer overcharged
- Bug causes service downtime → Lost revenue
- Data processing error → Business decision costs money
- Security breach → Data breach fines

**Safety / Legal / Compliance:**
- Medical device software error → Patient harm
- Safety system failure → Workplace injury
- Wrong data triggers illegal action → Legal liability
- Compliance violation → Regulatory fines
- **Quality guidance error → Project produces unsafe system** ← **Our QMS Dashboard risk**

**Reputational Damage:**
- Public data breach → Brand damage
- Offensive content displayed → PR crisis
- Service failure during critical event → Trust loss

**Critical Questions to Ask:**
1. If this system fails, could someone get hurt? → **Safety**
2. If this system fails, could we face legal action? → **Legal**
3. If this system fails, could we violate regulations? → **Compliance**
4. If this system fails, could money be lost? → **Financial**
5. If this system fails, would customers lose trust? → **Reputational**
6. If this system fails, would we just restart it? → **Annoyance**

**Indirect Consequences Count:**
- QMS Dashboard gives wrong guidance → Downstream project has safety issues → **Safety** (indirect but credible)
- Recommendation system gives bad advice → Users act on it → consequences → **(Consider consequences)**

---

### Q4: How reversible are failures?

**Question:** If this system fails, how easily can the **consequences** be undone?

**Options:**
- ☐ **Easy** - Consequences can be quickly corrected with minimal impact
- ☐ **Partial** - Some consequences reversible, some are not
- ☐ **Hard / irreversible** - Consequences cannot be undone or extremely difficult to undo

**Guidance:**
- Think about reversing **CONSEQUENCES**, not just fixing the code
- Consider **time to detect** + **time to reverse consequences**
- "Easy" means: Detected quickly AND consequences undone quickly AND no lasting harm
- Consider **who** can reverse it (users? support team? requires emergency fix?)

**Critical Distinction:**
- ❌ "We can deploy a bug fix in 10 minutes" ← Fixing the CODE
- ✅ "Users can undo the wrong action in 10 minutes with no harm" ← Fixing the CONSEQUENCES

**Examples:**

**Easy:**
- Display bug → Refresh page → Fixed
- Wrong recommendation shown → User notices immediately, ignores → No harm
- Config error → Rollback config → Restored
- Internal tool crash → Restart → Users retry

**Partial:**
- Wrong data sent to customers → Can send correction, but trust damaged
- Auto-charged wrong amount → Can refund, but customer frustrated
- Wrong recommendation → User acted on it, some damage done but fixable
- Security breach → Can patch hole, but data already leaked

**Hard / Irreversible:**
- Wrong medical advice → Patient already harmed
- Auto-trading loss → Money already lost, cannot recover
- Data permanently deleted → No backup available
- Legal violation already occurred → Cannot undo legal consequences
- Reputation damage → Cannot undo public perception
- Safety incident → Cannot undo injury

**Critical Questions:**
1. Can users detect the failure immediately? (If NO → Harder to reverse)
2. Can consequences be undone without external impact? (If NO → Partial or Hard)
3. Does fixing the bug also undo all consequences? (If NO → Partial or Hard)
4. Is there a "CTRL+Z" for affected users? (If YES → Easy, If NO → Partial/Hard)

**Edge Cases:**
- Code easy to fix BUT consequences already happened → **Partial or Hard**
- Failure detected immediately + users can undo → **Easy**
- Failure detected hours later + consequences propagated → **Hard**

---

### Q5: Is the domain well understood?

**Question:** Does your team have solid understanding of the problem domain and requirements?

**Options:**
- ☐ **Yes** - Team has experience, domain is well-known, requirements clear
- ☐ **Partially** - Some knowledge exists, but gaps remain or domain is evolving
- ☐ **No (research required)** - Domain is new, complex, or poorly understood

**Guidance:**
- Be honest about **what you don't know**
- "Well understood" means: Team has built similar systems OR domain has established patterns
- Consider: Industry expertise, regulatory landscape, user needs, technical challenges
- **Uncertainty is risk** - If unsure, select "Partially" or "No"

**Examples:**

**Yes:**
- Building CRUD web app (done it many times)
- Standard REST API (well-known patterns)
- Typical business logic (clear requirements)

**Partially:**
- New domain for team but industry has standards
- Well-known domain but evolving requirements
- Some team members have expertise, others don't
- Domain has edge cases or special regulations
- **QMS framework exists but applicability uncertain** ← **Our QMS Dashboard**

**No (research required):**
- Cutting-edge technology (limited industry experience)
- Novel application of AI/ML (unknown behaviors)
- New regulatory environment (requirements unclear)
- Complex domain requiring specialized expertise
- Innovation with no established patterns

**Critical Questions:**
1. Has the team built similar systems? (If NO → Partially or No)
2. Are requirements clear and stable? (If NO → Partially)
3. Do industry best practices exist? (If NO → No)
4. Do we need external experts? (If YES → Partially or No)

---

### Q6: What is the expected scale?

**Question:** How many people or teams will use this system at **full scale** (not just now)?

**Options:**
- ☐ **Individual** - Single person or personal use
- ☐ **Team** - One team (typically 5-15 people)
- ☐ **Multi-team** - Multiple teams within organization
- ☐ **Organization-wide / public** - Entire organization or external/public users

**Guidance:**
- Choose based on **planned scale**, not current prototype
- Consider **eventual state**, not initial deployment
- If scale will grow over time, choose the **target scale**
- Scale affects impact: Failures at large scale affect more people

**Examples:**

**Individual:**
- Personal automation script
- Developer productivity tool (one person)
- Research prototype

**Team:**
- Team dashboard
- Department tool
- Single squad product

**Multi-team:**
- Company-wide internal service
- Cross-functional platform
- Multiple teams depend on it

**Organization-wide / public:**
- Customer-facing product
- Public API or website
- Company-critical infrastructure
- Platform serving external users

**Critical Questions:**
1. If this fails, how many people are affected?
2. Is this a "nice to have" or critical dependency?
3. Will this scale beyond the current team?

---

### Q7: Is the project regulated or auditable?

**Question:** Is this system subject to regulatory oversight, compliance requirements, or formal audits?

**Options:**
- ☐ **No** - No regulatory requirements, informal quality management
- ☐ **Possibly** - May face audits, industry standards apply, or unclear regulatory status
- ☐ **Yes** - Formally regulated, subject to audits, compliance mandatory

**Guidance:**
- Consider: **Regulatory bodies** (FDA, EMA, SEC, etc.), **Industry standards** (ISO, IEC, HIPAA, GDPR), **Internal compliance**
- If **uncertain** → Choose "Possibly" (safer)
- "Auditable" means: Someone external will review quality documentation
- Systems used **in regulated contexts** may inherit requirements

**Examples:**

**No:**
- Internal productivity tool
- Non-critical prototype
- Personal project
- **QMS Dashboard for internal use** ← **Our QMS Dashboard (current)**

**Possibly:**
- System used in regulated industry (healthcare, finance) but not directly regulated
- Industry standards exist but not legally required
- Internal compliance requirements
- Future regulation possible
- **QMS Dashboard managing regulated projects** ← **Could escalate to this**

**Yes:**
- Medical device software (FDA/EMA regulated)
- Financial trading system (SEC regulated)
- Pharmaceutical system (GAMP 5)
- Personal data system (GDPR compliance required)
- Safety-critical system (IEC 62304, ISO 26262)

**Critical Questions:**
1. Will external auditors review this? (If YES → Yes or Possibly)
2. Are there industry standards that apply? (If YES → Possibly or Yes)
3. Could regulatory status change in future? (If YES → Possibly)
4. Is this used in a regulated context? (If YES → Possibly)

---

## 2. Risk Classification (R0–R3)

Based on your answers, the system calculates your risk level:

### R0: Internal, Low Impact, Fully Reversible
**Typical Profile:**
- Internal users
- Informational only
- Worst case: Annoyance
- Easy reversibility
- Well-understood domain
- Individual or team scale
- Not regulated

**Rigor:** Advisory (minimal quality activities)
**Artifacts:** 5 baseline artifacts

**Example:** Personal automation script, team dashboard

---

### R1: Internal, Moderate Impact, Reversible
**Typical Profile:**
- Internal users
- Recommendations or moderate decision impact
- Worst case: Financial loss or reputational damage (minor)
- Partial reversibility OR easy but moderate impact
- Domain partially understood
- Team or multi-team scale
- Not regulated

**Rigor:** Conditional (moderate quality activities)
**Artifacts:** 8 artifacts (baseline + 3 more)

**Example:** Internal service, department tool with business impact

---

### R2: External Users, Decision-Impacting, or Auditable
**Typical Profile:**
- External users OR
- Decision-impacting (recommendations heavily relied upon) OR
- Auditable / possibly regulated
- Worst case: Financial loss, reputational damage, OR potential safety/legal consequences (with mitigation)
- Multi-team or organization-wide scale

**Rigor:** Strict (comprehensive quality activities)
**Artifacts:** 11 artifacts (all required)

**Example:** Customer-facing product, recommendation system, B2B platform
**Example:** **QMS Dashboard** ← Our classification

---

### R3: Safety, Legal, Financial, or Hard-to-Reverse Consequences
**Typical Profile:**
- Worst case: Safety/legal/compliance OR
- Hard to reverse consequences OR
- Automated actions with high impact OR
- Formally regulated
- **No downgrade allowed** (Strict rigor required)

**Rigor:** Strict (no downgrade permitted)
**Artifacts:** 11 artifacts (all required)

**Example:** Medical device software, financial trading, safety-critical system, regulated product

---

## 3. Classification Logic

```
IF Q3 = "Safety/legal/compliance" AND (Q2 = "Automated" OR Q4 = "Hard/irreversible")
    → R3 (CRITICAL: Safety + Automation or Irreversibility)

ELSE IF Q3 = "Safety/legal/compliance" OR Q3 = "Financial loss" (high) OR Q7 = "Yes"
    → R3 or R2 (depends on reversibility, scale, other factors)

ELSE IF Q1 = "External" OR Q1 = "Public" OR Q2 = "Automated" OR Q7 = "Possibly"
    → R2 (External, decision-impacting, or auditable)

ELSE IF Q2 = "Recommendations" AND Q3 != "Annoyance"
    → R1 or R2 (decision-impacting)

ELSE IF Q3 = "Annoyance" AND Q4 = "Easy" AND Q1 = "Internal"
    → R0 (low impact)

ELSE
    → R1 (default moderate)
```

**Important:** If uncertain or answers are borderline → **Select higher risk**

---

## 4. Safety Checks

The system will flag the following for review:

🔴 **Critical Safety Warnings:**
- Q3 = "Safety/legal/compliance" (always flags)
- Q2 = "Automated" + Q4 = "Hard/irreversible" + High impact

🔶 **Medium Risk Warnings:**
- Contradictory answers (e.g., "Informational" + "Hard to reverse")
- Q2 = "Recommendations" + Q3 = "Safety/legal"
- Q5 = "Partially/No" + Q3 = High impact

**If you see warnings → Take them seriously!**

---

## 5. Expert Review Triggers

Request expert review if:
- Multiple risk warnings appear
- You're uncertain about classification
- Answers seem contradictory
- This is a borderline R2/R3 case
- Safety/legal consequences are possible

**It's better to ask for review than to under-classify!**

---

## 6. Rigor Mode Selection

- **R0** → **Advisory** (recommendations, optional activities)
- **R1** → **Conditional** (required activities, some flexibility)
- **R2** → **Strict** (all activities required, no skipping)
- **R3** → **Strict** (all activities required, **no downgrade allowed**)

Any downgrade from Strict requires formal deviation approval.

---

## 7. Next Steps After Intake

After classification:
1. ✅ Risk level determined (R0, R1, R2, or R3)
2. ✅ Required artifacts identified
3. ✅ System generates artifact templates
4. ⏳ Review and approve quality plan
5. ⏳ Begin implementation following quality plan

**Remember:** Quality planning comes BEFORE coding!

---

## Questions or Concerns?

- If intake questions don't fit your project → Request expert review
- If classification seems wrong → Document why and request override review
- If uncertain about any answer → Select higher risk option
- When in doubt → Ask for help!

**Version:** 2.0 Enhanced
**Supersedes:** intake-rules.md v1.0
**Changes:** Added examples, guidance, edge cases, and clarifications throughout
