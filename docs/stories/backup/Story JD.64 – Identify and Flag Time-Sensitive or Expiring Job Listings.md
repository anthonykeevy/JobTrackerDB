### User Story JD.64 – Identify and Flag Time-Sensitive or Expiring Job Listings

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** System Feature  

**Story:**  
As a system,  
I want to detect when job listings are nearing expiration or have a limited availability window,  
So that I can alert users in time to apply and take action.

---

**Acceptance Criteria:**
- [ ] Identify jobs with posted expiration dates or inferred availability windows (e.g., typical 30-day postings).
- [ ] Mark jobs as "Expiring Soon" within 3–5 days of end date.
- [ ] Display countdown timers or warning labels on expiring jobs in the dashboard.
- [ ] Notify users with bookmarked or unlogged jobs that are expiring.
- [ ] Provide options for quick-apply or immediate profile update prompts.
- [ ] Award bonus gamification points for logging or applying to time-sensitive jobs.

---

**Dependencies:**
- Job metadata parser (expiration detection logic)
- Dashboard and notification engine
- Gamification incentive model
- Bookmark and application status tracker

---

**Tags:** job-expiry, urgency-alerts, user-notification, dashboard-enhancement, gamification
