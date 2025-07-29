### User Story JD.17 – Save Skill Weights and Text Associations Per Job Version

**As a** system  
**I want** to store each skill’s extracted importance and its originating job description text for each version of a job  
**So that** skill-based evaluations like fit scoring and profile recommendations are traceable and version-aligned

---

**Description:**  
When parsing a job description, each skill must be saved along with the text snippet it was derived from and its inferred weight. This information must be saved with the specific version of the job to support auditability, scoring comparisons, and user feedback loops.

---

**Acceptance Criteria:**
- [ ] When a job is parsed, each skill is stored with:
  - Importance rating (required, preferred, optional)
  - Weight score (numeric value)
  - Source text from the job description
- [ ] Each skill entry is tied to a specific `JobVersionID`
- [ ] Job versions retain a full skill map independently
- [ ] If a new version is created (e.g., due to user edit), the skills are re-extracted and stored anew
- [ ] The skill map can be retrieved via API for scoring or UI rendering
- [ ] Data model supports multiple skills sharing the same text source and vice versa

---

**Dependencies:**
- NLP skill extraction model
- JobVersion schema with foreign key to Job
- SkillMapping table (or similar) to store skill metadata and source links
- Version control logic for job changes

---

**Priority:** High  
**Tags:** skill-mapping, version-control, job-parsing, scoring-integrity, auditability
