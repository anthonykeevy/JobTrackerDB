### User Story JD.44 – Determine Job Closure Reason and Notify Users Accordingly

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to distinguish between jobs that have closed due to completion and those still open to new applicants,  
So that I can notify users with accurate job status updates and help guide their expectations.

---

**Acceptance Criteria:**
- [ ] Monitor jobs for closure status from primary job board or source.
- [ ] Determine closure reason: filled, expired, hidden, or externally redirected.
- [ ] If job is closed because it's been filled or expired, notify all users who logged or applied.
- [ ] If job is hidden or redirect removed, attempt to confirm through repeated polling or user reports.
- [ ] If job is still open but user receives a personal rejection email, distinguish this in the user’s dashboard only.
- [ ] Mark closed jobs with appropriate status in the shared repository and per user view.
- [ ] Update dashboard statistics for active vs. closed jobs.
- [ ] Reward users with gamification points if they report closures accurately.

---

**Dependencies:**
- Job board closure detection engine
- Job status classification schema
- Notification engine
- User dashboard module
- Gamification engine

---

**Tags:** job-status, closure-detection, user-notification, metadata, gamification
