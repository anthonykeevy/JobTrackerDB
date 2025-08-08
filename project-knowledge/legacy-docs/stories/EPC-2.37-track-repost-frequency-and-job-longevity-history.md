### User Story JD.37 – Track Repost Frequency and Job Longevity History

**As a** platform  
**I want** to track how often a job has been reposted and for how long it has been active  
**So that** users can gauge job urgency, persistence, and likelihood of success

---

**Description:**  
Jobs that are repeatedly reposted or remain open for long periods may signal different factors—high turnover, hard-to-fill roles, or lack of viable applicants. The system will log historical presence and reappearance of identical or near-identical jobs to support transparency and user judgment.

---

**Acceptance Criteria:**
- [ ] Each job has a `first_seen_date` and `last_seen_date`
- [ ] Jobs that disappear and later reappear trigger a `repost_count` increment
- [ ] Job versions retain a `job_lifetime_days` metric
- [ ] Reposted jobs inherit `JobGroupID` lineage for relational tracking
- [ ] UI includes:
  - “Previously posted X times”
  - “Last seen Y days ago”
  - “Active since [date]” summary
- [ ] Historical repost data available for sorting/filtering job lists
- [ ] Fit Score records log the repost version used for comparison

---

**Dependencies:**
- Deduplication and job versioning logic
- Audit trail of job appearances over time
- UI component for displaying repost history
- Fit Score engine support for job version lineage

---

**Priority:** Medium  
**Tags:** repost-tracking, job-metadata, job-visibility, time-awareness, traceability
