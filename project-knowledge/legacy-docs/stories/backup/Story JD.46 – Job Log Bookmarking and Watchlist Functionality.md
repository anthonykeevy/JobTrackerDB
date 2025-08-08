### User Story JD.46 – Job Log Bookmarking and Watchlist Functionality

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a user,  
I want to bookmark jobs and add them to a personal watchlist,  
So that I can track roles I'm interested in and return to them later for deeper review or artifact creation.

---

**Acceptance Criteria:**
- [ ] Provide a bookmarking UI component on each job view and job list.
- [ ] Support toggling watchlist status from job listing or job detail screen.
- [ ] Store watchlist status and timestamp per user, per job.
- [ ] Display all bookmarked jobs in a centralized “Watchlist” section in the dashboard.
- [ ] Allow users to filter bookmarked jobs by log status, fit score, or status (open/closed).
- [ ] Persist watchlist even for jobs that later get removed from public view.
- [ ] Reward bookmarking and engagement via gamification points.

---

**Dependencies:**
- User-job relationship schema
- Job dashboard interface
- Gamification tracking for bookmark activity
- Job status monitoring for bookmarked items

---

**Tags:** bookmarking, watchlist, user-engagement, dashboard-features, gamification
