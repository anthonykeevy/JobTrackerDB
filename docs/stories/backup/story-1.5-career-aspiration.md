# User Story 1.5: Define Career Aspirations

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** 1.5  
**Priority:** High  
**Status:** Revised  
**Owner:** Product Owner (PO)

---

## Description

As a **user**,  
I want **to define my short-term and long-term career goals**,  
So that **AI can tailor profile prompts, resume suggestions, and job-fit analysis to my aspirations**

---

## Acceptance Criteria

1. User can:
   - Specify their next desired job role (short-term)
   - Define their 5-year aspirational role or direction
   - Choose from suggested options or enter custom inputs
2. AI provides clarification prompts and role examples based on:
   - Work history
   - Uploaded resume
   - Industry patterns
3. Career aspirations influence:
   - Role targeting module
   - Skill relevance inference
   - Resume generation priorities
4. AI checks for compatibility between next role and long-term aspiration and may offer guidance.
5. User can revise aspirations at any time.
6. Aspirations are logged and versioned in the profile.

---

## Definition of Done

- Input interface supports both predefined roles and freeform aspirations
- Role alignment logic provides user feedback
- Aspirations integrated with resume and fit logic
- Profile version includes timestamped aspiration milestones

---

## Dependencies

- AI guidance and reasoning engine  
- Role suggestion service  
- Profile schema and version tracker  
- Resume and fit score downstream engines
