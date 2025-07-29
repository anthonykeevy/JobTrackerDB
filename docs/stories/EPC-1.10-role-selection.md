# User Story 3.1: Role Selection and Targeting

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** 3.1  
**Priority:** High  
**Status:** Final  
**Owner:** Product Owner (PO)

---

## Description

As a **user**,  
I want to **define or select the job role I am targeting**,  
So that **the resume and AI assistance are tailored toward that role**.

---

## Acceptance Criteria

1. User can:
   - Select a role from a predefined taxonomy
   - Enter a custom role manually
   - Let AI derive a target role based on the Career Aspiration module
2. Role selection is editable at any time and must be confirmed before resume generation.
3. The selected role influences:
   - AI prompts and examples throughout profile intake
   - Resume formatting and content prioritization
   - Skill matching and recommendation logic
4. If multiple roles are supported in the career aspiration (for experienced users), AI recommends a primary target with the option to override.
5. User can set both a short-term role (next target) and a 5-year aspirational role.
6. AI can advise if the chosen next role supports the long-term aspiration.
7. System tracks which role was active at the time of resume or fit score generation.

---

## Definition of Done

- Role selection component integrated into intake flow
- Links with aspiration module for derived suggestions
- Role stored and retrievable with version tracking
- Resume and fit scoring modules use role data for optimization
- Fully responsive UI with accessibility compliance

---

## Dependencies

- Career Aspiration module  
- Resume generator logic  
- AI guidance engine  
- Skill-to-role fit algorithm
