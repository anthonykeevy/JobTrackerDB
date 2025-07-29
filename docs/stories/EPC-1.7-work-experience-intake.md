# User Story 2.2: Work Experience Intake

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** 2.2  
**Priority:** High  
**Status:** Revised  
**Owner:** Product Owner (PO)

---

## Description

As a **user**,  
I want **to enter my previous job roles with responsibilities and achievements**,  
So that **my career history is clearly captured and usable for resume and fit scoring**

---

## Acceptance Criteria

1. Users can enter one or more job entries with:
   - Job title
   - Employer/organization name
   - Start and end dates (or mark as current)
   - Responsibilities (ongoing tasks or expectations)
   - Achievements (impact or accomplishments)
2. AI assists user by:
   - Providing examples
   - Highlighting typical achievements for that role
   - Suggesting missing details based on other profile data
3. Resume upload prepopulates fields where possible.
4. Each entry includes tags for:
   - Industry
   - Role type (individual contributor, manager, etc.)
5. Entries are stored with version tracking and edit history.
6. Each responsibility or achievement is clearly labeled.
7. Information feeds into:
   - Skill inference
   - Resume content prioritization
   - Fit score evaluation

---

## Definition of Done

- Work history fields support multiple entries
- AI-enhanced input provides prompts and validation
- Responsibility/achievement distinction stored in schema
- All changes tracked as part of profile versioning
- Section supports progressive UI and mobile responsiveness

---

## Dependencies

- Resume parser  
- AI suggestion and clarification engine  
- Profile schema with responsibility/achievement tagging  
- Version control and edit history module  
- Skill inference engine
