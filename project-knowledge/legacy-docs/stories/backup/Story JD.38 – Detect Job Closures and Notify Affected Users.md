### User Story JD.38 – Detect Job Closures and Notify Affected Users

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** High  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a user who has logged or applied to a job,  
I want to be automatically notified if the system detects that the job listing has been closed,  
So that I can focus my efforts on currently active opportunities.

---

**Acceptance Criteria:**
- [ ] System periodically checks known job URLs or associated job boards for status changes.
- [ ] Jobs can be flagged as:
  - `Open`
  - `Closed (System Detected)`
  - `Closed (User Declared)`
- [ ] If system detects closure (e.g., job removed, closed indicator), it updates status and logs closure time.
- [ ] All users associated with the job (logged or applied) are notified within their dashboard.
- [ ] Notification includes job title, closure date, and source.
- [ ] Users can archive or dismiss the notification.
- [ ] Closure detection does not override manual rejection tracking by individual users.

---

**Dependencies:**
- Job closure detection engine (scraping, polling)
- Job-user linkage and association tracker
- Notification service
- Audit log of job status changes
- Epic: Job Discovery and Logging for Profile Matching

---

**Tags:** job-status, closure-detection, notification, job-lifecycle, user-awareness, audit-tracking
