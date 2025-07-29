### User Story JD.43 – Track Job Reposts and Reopening Frequency

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to detect how often a job has been reposted or reopened,  
So that users can better understand market persistence, job demand, and possible role volatility.

---

**Acceptance Criteria:**
- [ ] For each unique job signature, track its first appearance date and maintain a repost count.
- [ ] Use job title, company, description, and location to determine if a repost is the same job or a similar new one.
- [ ] Adjust deduplication scoring logic to account for job age and previous post history.
- [ ] Surface the repost frequency and age metadata in the job details view for users.
- [ ] Allow users to filter jobs by age, repost frequency, or stability tags.
- [ ] Gamify logging of reposted jobs that are correctly linked to prior records.

---

**Dependencies:**
- Job deduplication engine with temporal awareness
- Job metadata enhancement for age and repost counters
- Dashboard metrics integration
- Gamification reward system

---

**Tags:** job-reposts, job-lifecycle, job-stability, metadata-tracking, deduplication
