### User Story JD.12 – Track Fit Score History and Version Context

**As a** job seeker  
**I want** to view my fit score history for each job along with the profile version it was based on  
**So that** I can understand how my changes improve my fit for roles over time

---

**Description:**  
Each time a Fit Score is generated for a job, the system should log the job ID, the profile version used, the score breakdown, and timestamp. If a user updates their profile and re-runs the Fit Score, the system should preserve the old results and allow comparison. This will help users see the effect of profile updates and establish a progression timeline in their job readiness journey.

---

**Acceptance Criteria:**
- [ ] Each Fit Score result is logged with:
  - Job ID
  - Profile Version ID
  - Full score breakdown (e.g., matched vs unmatched skills)
  - Timestamp
- [ ] Re-scoring a job after profile updates does not overwrite the old score
- [ ] Users can view historical Fit Scores and associated profile versions
- [ ] Optionally highlight improvement delta between versions
- [ ] Fit Score logs support future analytics and recommendation models

---

**Dependencies:**
- Fit Score engine
- Profile versioning and snapshot storage
- Fit Score log table
- Score comparison module (for highlighting improvements)

---

**Priority:** Medium  
**Tags:** fit-score-history, profile-versioning, scoring-comparison, timeline-tracking, job-analysis
