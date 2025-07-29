### User Story JD.60 – Incentivize User-Driven Job Listing Verification and Flagging

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Engagement Feature  

**Story:**  
As a system,  
I want to encourage users to help verify the status and accuracy of job listings they've logged or interacted with,  
So that the job data remains current and trustworthy, while promoting gamified engagement.

---

**Acceptance Criteria:**
- [ ] Periodically notify users to verify active jobs in their dashboard (e.g., "You have 6 jobs that may need rechecking").
- [ ] Allow users to click to open the job board link and confirm:
  - [ ] Job is still listed
  - [ ] Details are unchanged
  - [ ] Or mark as no longer available
- [ ] Reward users with gamification points for each verified check.
- [ ] Store verification timestamp and user ID.
- [ ] Maintain an audit log of who verified what and when.
- [ ] Flag users who:
  - [ ] Frequently submit incorrect data
  - [ ] Misuse metadata fields
  - [ ] Show patterns of low-accuracy input
- [ ] Alert moderators for manual review of repeat offenders.

---

**Dependencies:**
- Job interaction history model
- Notification and alert system
- Gamification and reward triggers
- User reputation scoring logic
- Admin/moderator flag review system

---

**Tags:** job-verification, user-engagement, gamification, data-integrity, moderation-alerts
