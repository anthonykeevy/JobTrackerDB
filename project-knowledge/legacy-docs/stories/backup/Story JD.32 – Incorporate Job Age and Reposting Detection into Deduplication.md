### User Story JD.32 – Incorporate Job Age and Reposting Detection into Deduplication

**As a** job seeker  
**I want** the system to track the age and reposting status of job listings  
**So that** I can distinguish between newly posted jobs and those that have been previously advertised

---

**Description:**  
This story ensures that the system captures the first known logging date of a job, flags reposted listings, and incorporates job age and repost likelihood into job deduplication logic. It enhances both user confidence and deduplication accuracy.

---

**Acceptance Criteria:**
- [ ] Each job record includes a `first_seen_date` and `last_seen_date`
- [ ] System identifies reposting patterns (e.g., same job reappears with minor edits)
- [ ] Deduplication logic weighs age as a factor when resolving potential duplicates
- [ ] If a job appears with a significant time gap or edits, it is versioned or flagged as reposted
- [ ] Display job age and repost status in the UI
- [ ] Users can sort/filter jobs by age or freshness
- [ ] Jobs reposted with new details can optionally be linked to prior versions

---

**Dependencies:**
- Job logging pipeline with timestamp capture
- Job versioning system
- UI enhancements for job metadata
- Repost detection rules integrated into deduplication

---

**Priority:** Medium  
**Tags:** job-metadata, deduplication, repost-detection, job-age
