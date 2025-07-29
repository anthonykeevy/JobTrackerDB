### User Story JD.21 – Allow Skill Feedback and Correction by User

**As a** job seeker  
**I want** to provide feedback or correct the extracted skills for a job I logged  
**So that** the fit score and future recommendations are more accurate

---

**Description:**  
After logging a job and viewing the inferred skills and their importance, the user should be able to flag inaccuracies, suggest corrections, or add skills they feel are missing from the system's analysis. The system will track these feedback actions and either trigger a review, create a new job version, or adjust the user’s personal fit score interpretation.

---

**Acceptance Criteria:**
- [ ] Users can flag extracted skills as incorrect or irrelevant
- [ ] Users can suggest missing skills and provide justification
- [ ] If a skill correction materially affects the skill map, system creates a new JobVersion
- [ ] Minor suggestions (e.g., spelling or tagging) are stored as user-specific overrides
- [ ] Users can provide context (e.g., “this skill actually refers to leadership, not Agile”)
- [ ] System logs feedback with timestamps and ties to job, version, and user
- [ ] Admin panel available for monitoring flagged skill entries (for future ML refinement)

---

**Dependencies:**
- Skill extraction and visualization UI
- JobVersion logic
- Feedback logging and review infrastructure
- Notification and version re-triggering mechanism
- Admin review interface (optional post-MVP)

---

**Priority:** Medium  
**Tags:** skill-correction, user-feedback, job-versioning, fit-score-accuracy, AI-trust
