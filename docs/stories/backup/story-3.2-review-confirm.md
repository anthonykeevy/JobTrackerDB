# User Story 3.2: Review and Confirm View

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** 3.2  
**Priority:** High  
**Status:** Revised  
**Owner:** Product Owner (PO)

---

## Description

As a **user**,  
I want **to review and approve my profile with visibility into changes**,  
So that **I can confidently use it for resume generation and job-fit scoring**

---

## Acceptance Criteria

1. Structured profile is presented for final review, including:
   - Education, experience (with responsibility/achievement distinction), skills, certifications, etc.
   - Career aspiration and targeted role
2. Sections are collapsible and editable.
3. System highlights:
   - New entries since last approval
   - Fields with incomplete, outdated, or conflicting data
4. Shows:
   - Current version vs. previous approved version
   - Change summary
   - Prior happiness score and timestamp
5. User provides a new happiness score and optional comments.
6. User must explicitly approve the profile before downstream actions.
7. Visual indicators show pending confirmation for new content.
8. Fit score and artifact generation only run on confirmed versions.

---

## Definition of Done

- Review screen dynamically renders profile
- Change indicators and diff engine highlight updates
- Happiness scoring system with history view
- Approving profile creates a new milestone version
- Gated downstream usage respects version status

---

## Dependencies

- Profile versioning and milestone tracker  
- Change detection and diffing system  
- Profile renderer and inline editor  
- Approval gating for resume/fit engines
