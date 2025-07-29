### User Story JD.55 – Distinguish Between Job Closure and User Rejection

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** High  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to differentiate between when a user has been rejected versus when a job has been closed altogether,  
So that I can provide more accurate insights to users and support better decision-making on future applications.

---

**Acceptance Criteria:**
- [ ] Track job board status regularly to detect job deactivation (e.g., 404 page, job no longer listed).
- [ ] Log closure event with timestamp and job board source.
- [ ] Distinguish between:
  - [ ] Job closed for all applicants (removed from job board)
  - [ ] User specifically rejected while job remains active
- [ ] Notify all applicants when a job is officially closed.
- [ ] Preserve the last known status for each user’s application (e.g., rejected, awaiting response).
- [ ] Visualize job closure separately from personal application outcome.
- [ ] Include this information in analytics and application status filters.

---

**Dependencies:**
- Job board monitoring service
- Job application status tracking model
- Notification engine
- Analytics dashboard enhancements

---

**Tags:** job-status, closure-detection, rejection-clarity, application-tracking, user-analytics
