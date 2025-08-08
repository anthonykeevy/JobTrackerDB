### User Story JD.35 – Track User-Perceived Job Freshness and Engagement History

**As a** job seeker  
**I want** to see how recently a job was posted and how often it has been interacted with  
**So that** I can focus on timely, active opportunities and understand job traction on the platform

---

**Description:**  
Beyond technical deduplication and repost detection, users need visibility into a job’s freshness and popularity. This story adds support for displaying job posting recency and user interaction metrics to guide discovery decisions.

---

**Acceptance Criteria:**
- [ ] System stores `first_seen_date` and `last_seen_date` per job version
- [ ] Job listing includes calculated age display (e.g., "Posted 3 days ago")
- [ ] Job listing displays:
  - Total number of users who viewed it
  - Total number of users who logged/applied for it
  - Number of fit scores calculated against it
- [ ] Reposted jobs reflect history across versions with indicator (e.g., “previously posted 2x in last 6 months”)
- [ ] User dashboard shows a freshness score or ranking for jobs recently logged
- [ ] Metrics are stored in a form usable by sorting and analytics components

---

**Dependencies:**
- Job logging and deduplication engine
- Job versioning system
- Fit score tracking per job version
- Job view and interaction logging module
- UI components for metric display

---

**Priority:** Medium  
**Tags:** job-metadata, job-engagement, freshness-tracking, analytics, repost-awareness
