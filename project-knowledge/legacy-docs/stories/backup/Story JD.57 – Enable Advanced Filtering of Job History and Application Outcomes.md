### User Story JD.57 – Enable Advanced Filtering of Job History and Application Outcomes

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** UX Enhancement  

**Story:**  
As a user,  
I want to filter and sort my job history and application outcomes based on various criteria,  
So that I can quickly find relevant applications, identify trends, and manage my job search more efficiently.

---

**Acceptance Criteria:**
- [ ] Allow filtering by:
  - [ ] Job status (active, closed, removed)
  - [ ] Application outcome (applied, rejected, interview, offer)
  - [ ] Fit score (range filter)
  - [ ] Job board or recruiter
  - [ ] Industry or company
  - [ ] Job location
- [ ] Allow sorting by:
  - [ ] Application date
  - [ ] Last status update
  - [ ] Fit score (ascending/descending)
- [ ] Support combined filters (e.g., all rejected jobs from LinkedIn with fit score >70%).
- [ ] Allow saving of filter presets for frequent use.
- [ ] Reflect filters in the dashboard view and timeline summaries.
- [ ] Update gamification dashboard with insights into filtering behavior (e.g., most-reviewed job types).

---

**Dependencies:**
- Job application and status models
- Dashboard filter engine
- Timeline view components
- Analytics model for gamified usage

---

**Tags:** job-history, advanced-filters, user-dashboard, UX-enhancement, fit-score-management
