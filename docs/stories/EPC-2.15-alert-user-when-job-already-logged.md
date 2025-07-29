### User Story JD.15 – Alert User When Job Already Logged

**As a** job seeker  
**I want** to be notified if I attempt to log a job that already exists in the system  
**So that** I avoid duplication and can view or enhance the existing record instead

---

**Description:**  
When a user logs a job, the system compares the job title, company, description, and URLs against existing records. If a match is found, the system alerts the user and offers to view or update the existing job. If the user’s details differ meaningfully, they are guided to create a new version of the same job.

---

**Acceptance Criteria:**
- [ ] System identifies potential duplicates based on content signature (title + company + description hash)
- [ ] User is alerted with a preview of the matched job
- [ ] User can:
  - Accept the match and view the existing job
  - Propose edits (which may trigger a new version)
  - Cancel and return to logging screen
- [ ] If no exact match found, user proceeds to log a new job
- [ ] Match results do not include personal information from other users

---

**Dependencies:**
- Job deduplication logic and signature generation
- Job preview display component
- Job versioning and edit proposal workflow

---

**Priority:** High  
**Tags:** deduplication, user-guidance, job-reuse, version-control, quality-assurance
