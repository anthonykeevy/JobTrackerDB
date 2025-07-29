### User Story JD.30 – Enable Job Reuse with Confidence Indicators

**As a** job seeker  
**I want** to reuse job listings already captured by other users  
**So that** I can avoid duplicate effort while trusting the accuracy of the existing information

---

**Description:**  
Many job roles will be discovered by multiple users. Instead of forcing each to log the same role again, the system should offer reuse options for previously logged jobs. However, the platform must surface confidence indicators (e.g., how many users reused it, time since last update, completeness rating) so that users can judge the reliability of existing entries. This also supports community-driven quality improvement.

---

**Acceptance Criteria:**
- [ ] When logging a job, system checks for existing entries using deduplication logic
- [ ] If match is found, user is prompted to reuse or log a modified version
- [ ] Reusable job entries show metadata confidence indicators:
  - Number of users who reused it
  - Time since last metadata update
  - Completeness rating (based on fields present)
  - Fit score history reference (if applicable)
- [ ] Users can suggest edits or add missing data
- [ ] Users can log a new job version if reuse is unsuitable
- [ ] Reuse action awards points via gamification system
- [ ] Admin can promote high-confidence jobs to “Trusted” status

---

**Dependencies:**
- Deduplication engine
- Job reuse interface and metadata badge logic
- Fit score tracking by job version
- Gamification event hooks for reuse

---

**Priority:** Medium  
**Tags:** job-reuse, confidence-metrics, community-metadata, gamification, trust-signal
