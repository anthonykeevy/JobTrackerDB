### User Story JD.39 – Track Reposted Jobs and Establish Posting History

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** High  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to track when a job listing is a repost of a previous role,  
So that I can build a posting history and help users understand job market persistence and employer behavior.

---

**Acceptance Criteria:**
- [ ] Deduplication logic includes job posting timestamp for age comparison.
- [ ] When a job reappears with highly similar content and a new posting timestamp, it is flagged as a repost.
- [ ] Reposted jobs retain a shared job signature but are tracked as separate posting events.
- [ ] System maintains a history of posting intervals, including:
  - First seen
  - Most recent repost
  - Frequency of reposting (e.g., monthly reposts)
- [ ] Users can view reposting history when reviewing the job.
- [ ] Reposting activity contributes to job age and scoring insights (e.g., “This job has been open on and off for 4 months”).

---

**Dependencies:**
- Job signature hashing logic
- Timestamp tracking engine
- Deduplication module with time-based enhancements
- Job repository with history versioning
- Epic: Job Discovery and Logging for Profile Matching

---

**Tags:** repost-detection, job-age, history-tracking, deduplication, job-metadata
