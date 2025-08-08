### User Story JD.51 – Detect Recruiter Employer Changes and Prompt Verification

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Enhancement  

**Story:**  
As a system,  
I want to detect when a recruiter’s employer has changed based on new job logs or metadata updates,  
So that I can prompt verification and preserve historical employment accuracy in recruiter–company associations.

---

**Acceptance Criteria:**
- [ ] Detect discrepancies between current recruiter–company metadata and new job associations.
- [ ] If a recruiter appears to be associated with a new company, initiate a verification prompt or flag for review.
- [ ] Log employer change with start date from the new job log (or manually entered).
- [ ] Do not retroactively update prior jobs—preserve existing employer history records.
- [ ] Show pending employer transitions on recruiter profile UI with confirmation status.
- [ ] Update recruiter–company employment history table with verified change.
- [ ] Allow manual override or correction by authorized users.

---

**Dependencies:**
- Recruiter entity and employment history model
- Job metadata extraction pipeline
- Recruiter verification interface
- Change flagging logic
- Admin override tooling

---

**Tags:** recruiter-history, employment-tracking, recruiter-verification, metadata-integrity, job-logging
