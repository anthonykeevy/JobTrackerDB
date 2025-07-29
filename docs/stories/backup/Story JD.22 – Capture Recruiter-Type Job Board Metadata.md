### User Story JD.22 – Capture Recruiter-Type Job Board Metadata

**As a** system  
**I want** to identify whether a job board is operated by a recruiter rather than an employer  
**So that** users can adjust expectations when applying and the platform can route jobs accordingly

---

**Description:**  
Not all job boards represent direct employers—some aggregate listings on behalf of third-party recruiters. This story ensures the platform captures recruiter-type classification for boards, and flags job entries that originate from these intermediaries. Users benefit by knowing whether they’re applying to a recruiter pipeline versus a company.

---

**Acceptance Criteria:**
- [ ] System captures a `JobBoardType` (e.g., "Recruiter", "Corporate", "General Aggregator") for each job board
- [ ] Recruiter boards are flagged in the job board metadata
- [ ] When a job originates from a recruiter board, the system tags the job record accordingly
- [ ] System displays a note to users explaining recruiter pipeline implications
- [ ] Metadata is available for filtering or analytics (e.g., “show only direct employer jobs”)
- [ ] Admin UI supports updating or confirming recruiter status of boards as patterns evolve

---

**Dependencies:**
- Job board metadata schema
- Job ingestion logic
- Admin console for job board management
- Job board classifier (manual or AI-assisted)

---

**Priority:** Medium  
**Tags:** job-board-metadata, recruiter-flagging, user-guidance, job-insight, classification
