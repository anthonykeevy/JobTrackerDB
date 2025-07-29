### User Story JD.42 – Detect Reopened Job Postings and Inform User Dashboard Metrics

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to detect when a previously closed job has been reopened,  
So that I can update job market insights and inform users of renewed opportunities.

---

**Acceptance Criteria:**
- [ ] Jobs previously closed are monitored for reappearance through job board scanning.
- [ ] If a matching job (based on deduplication signature) is detected after closure, mark as reopened.
- [ ] Display reopening status and reopening timestamp in the job metadata.
- [ ] Update job statistics for that listing to include “Reopened” count.
- [ ] Notify users who bookmarked or applied to the job previously when a reopening is detected.
- [ ] Gamify user engagement if they were early loggers or re-applicants to reopened roles.

---

**Dependencies:**
- Job board scanning engine
- Deduplication logic and job signature tracking
- Notification service
- Gamification engine integration

---

**Tags:** job-status-tracking, reopening-detection, user-notification, dashboard-insights, job-lifecycle
