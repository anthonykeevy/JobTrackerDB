# User Story 1.3: Memory Prompts for Recollection

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** 1.3  
**Priority:** High  
**Status:** Revised  
**Owner:** Product Owner (PO)

---

## Description

As a **user**,  
I want **AI to prompt me with memory cues about my past career activities**,  
So that **I can more easily recall key responsibilities, accomplishments, and projects**

---

## Acceptance Criteria

1. AI offers memory-stimulating prompts contextualized to:
   - Resume data (if available)
   - Career stage and industry (if known)
   - Previously entered profile fields
2. Prompts include categories such as:
   - Project highlights
   - Tools or technologies used
   - Problems solved
   - Team dynamics and leadership
   - Results achieved
3. AI tailors prompt tone and examples to experience level.
4. Users can respond in freeform and AI will structure responses into correct schema fields.
5. Suggestions include an option to "skip" or "refine later".
6. Prompts adapt based on gaps or incomplete sections in profile.
7. Structured responses are versioned as part of the editable profile.

---

## Definition of Done

- AI prompt engine generates adaptive questions
- User responses are stored in structured fields or "Additional Info" if not mappable
- Version tracking logs additions from prompt responses
- Experience is mobile-friendly and conversational
- Prompts contribute to improving completeness score of profile

---

## Dependencies

- AI guidance agent  
- Profile schema integration  
- Change detection and completeness engine  
- Responsive UI and mobile support
