# User Story 2.3: Skill Entry and Tagging

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** 2.3  
**Priority:** High  
**Status:** Revised  
**Owner:** Product Owner (PO)

---

## Description

As a **user**,  
I want **to enter and refine my skills**,  
So that **they accurately reflect my background and can be used to evaluate my job fit**

---

## Acceptance Criteria

1. Users can:
   - Add skills manually
   - Confirm or reject inferred skills
   - Associate each skill with a source (education, work, project, etc.)
   - Specify exposure duration and self-assessed competency
2. AI suggests relevant skills based on:
   - Resume data
   - Other profile sections
   - Target job role
3. Skills added without a source are flagged for user to clarify.
4. Skills influence:
   - Resume tailoring
   - Fit score calculations
   - Career suggestion logic
5. Skills are versioned and linked to profile milestones.
6. Users can edit, remove, or merge skills.

---

## Definition of Done

- Skill form supports source tagging, duration, and competency
- AI suggestions integrate with real-time profile context
- Inferred skills are distinct from user-added ones until confirmed
- Skill entries are stored with version tracking and source metadata

---

## Dependencies

- Skill inference engine  
- Resume parser  
- Profile schema and source mapping  
- Fit score and resume optimization modules
