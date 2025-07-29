### User Story JD.8 – Handle Job Reuse and Confirmation Prompt

**As a** job seeker  
**I want** the system to detect if a job I am logging already exists and let me confirm or edit the record  
**So that** I can avoid duplicating existing data while ensuring accuracy for my version

---

**Description:**  
When a user begins logging a job, the system checks for similar or identical job entries in the repository. If a potential match is found, the user is presented with a summary of the existing record and asked to confirm if it's the same role. The user can choose to reuse the entry as-is, suggest edits, or create a personalized version if needed. This preserves data integrity while allowing personalization.

---

**Acceptance Criteria:**
- [ ] When job metadata is collected, the system checks for matching jobs using semantic and hash comparisons
- [ ] If a match is found, system displays existing job details with option to confirm reuse
- [ ] User may:
  - Accept the existing job as-is and link it to their profile
  - Edit the entry (if substantial changes are made, a new version is created)
  - Reject the match and proceed with logging a new job
- [ ] System guides user on the best choice to prevent redundancy
- [ ] Versioning rules apply when changes affect fit scoring
- [ ] User is always informed of which job version their Fit Score was based on

---

**Dependencies:**
- Job deduplication and similarity detection engine
- Job versioning system
- User guidance engine for reuse decisions

---

**Priority:** Medium  
**Tags:** reuse-detection, deduplication, user-confirmation, job-versioning, metadata-comparison
