# User Story 4.4: Skill Inference from Profile Data

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** 4.4  
**Priority:** High  
**Status:** Draft  
**Owner:** Product Owner (PO)

---

## Description

As a **user building my career profile**,  
I want **the system to infer my skills based on my experience, education, projects, and certifications**,  
So that **I can quickly see a list of skills with estimated proficiency and relevance to my target role**.

---

## Acceptance Criteria

1. Skills are inferred from multiple profile sources:
   - Job responsibilities
   - Education fields
   - Certifications and training
   - Projects and volunteer work
2. Each inferred skill includes:
   - Estimated years of exposure
   - Estimated competency level (e.g., beginner, proficient, expert)
   - Source references (what data supported this inference)
3. User can:
   - Confirm or reject each inferred skill
   - Adjust years of experience and proficiency level
4. Inferred skills are matched to job descriptions for a skill fit score.
5. AI recommends missing skills based on job descriptions that are not yet evidenced in the profile.

---

## Definition of Done

- Skill inference engine implemented and tested
- Cross-profile correlation logic works across all data types
- UI allows user to review, edit, and confirm inferred skills
- Skill-to-role comparison module provides match score
- System logs source data used for each skill inference

---

## Dependencies

- Skill inference engine  
- Profile schema supporting skill attributes (duration, level, source)  
- Job description parser  
- AI mapping for skill taxonomy
