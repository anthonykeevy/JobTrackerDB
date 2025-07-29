### User Story JD.54 – Detect Job Application Outcomes from User Communication

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to detect if a user has been rejected or has advanced in the hiring process through follow-up communications,  
So that we can update the job application status and improve user engagement and analytics.

---

**Acceptance Criteria:**
- [ ] Enable users to forward or upload job-related email responses (e.g., rejections, interview invitations).
- [ ] Use AI to parse subject lines and body text to infer outcome:
  - [ ] Rejected
  - [ ] Invited to interview
  - [ ] Request for more information
  - [ ] No longer under consideration
- [ ] Log the outcome under the associated job application with a timestamp.
- [ ] Notify user to confirm or adjust the detected outcome.
- [ ] Allow user to manually select job if automatic linking fails.
- [ ] Update job dashboard with status progression and outcome timeline.
- [ ] Award gamification points for tracking outcome and keeping log updated.
- [ ] Differentiate outcome statuses from job closure (e.g., job taken down).

---

**Dependencies:**
- Email parsing and AI classification module
- Job application status model
- Notification system for confirmation
- Timeline visualization module
- Gamification event triggers

---

**Tags:** job-outcomes, email-inference, user-feedback, application-status, rejection-tracking, communication-parsing
