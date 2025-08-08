### User Story JD.50 – Support Recruiter–Company Employment History Tracking

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to maintain a historical record of the company affiliations of each recruiter,  
So that I can accurately reflect their employment timeline when evaluating job sources and recruiter influence across time.

---

**Acceptance Criteria:**
- [ ] Store recruiter–company relationships with timestamped ranges (e.g., Hayes: Jan 2023–Apr 2024, LinkedIn: May 2024–present).
- [ ] When associating a recruiter with a job, include the recruiter’s employer as of the job’s log date.
- [ ] Prevent overwriting prior employer info when recruiter changes roles in future.
- [ ] Display current and historical company affiliations in recruiter profiles.
- [ ] Allow manual confirmation or correction of recruiter–employer links by admins or users with permission.
- [ ] Use historical recruiter–company links for gamification (e.g., points for verified transitions).
- [ ] Ensure job deduplication and versioning logic uses recruiter–employer snapshot relevant at time of job log.

---

**Dependencies:**
- Recruiter entity model
- RecruiterCompanyHistory table
- Job–Recruiter association logic
- Admin recruiter profile UI
- Gamification logic for verification

---

**Tags:** recruiter-linkage, employment-history, version-integrity, job-timeline, recruiter-audit
