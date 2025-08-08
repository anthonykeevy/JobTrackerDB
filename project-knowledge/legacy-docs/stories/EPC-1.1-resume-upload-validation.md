# User Story 1.1: Resume Upload and AI-Driven Parsing with Validation

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** 1.1  
**Priority:** High  
**Status:** Revised  
**Owner:** Product Owner (PO)

---

## Description

As a **new user**,  
I want to **upload my resume and have it parsed by AI**,  
So that **my career history can be quickly prepopulated and structured for confirmation**.

---

## Acceptance Criteria

1. Users can upload PDF/DOCX resumes.
2. AI parses key sections: experience, education, skills, certifications, projects.
3. Parsed data prepopulates relevant profile fields.
4. Unmatched or ambiguous entries are logged under “Additional Info”.
5. User is prompted to review and correct the parsed content before proceeding.
6. Parsing triggers the creation of an initial unconfirmed profile version.
7. Fit scores and resume generation remain disabled until user completes confirmation.
8. Parsing engine highlights errors or low-confidence fields for user review.

---

## Definition of Done

- Resume is parsed and structured data is mapped into the profile schema
- “Additional Info” captures edge cases for later schema review
- Profile version tracking initiated with status set to “unconfirmed”
- AI parser integrated with change log and approval system

---

## Dependencies

- AI resume parser  
- Profile schema model  
- Profile version and status tracker  
- Error flagging interface
