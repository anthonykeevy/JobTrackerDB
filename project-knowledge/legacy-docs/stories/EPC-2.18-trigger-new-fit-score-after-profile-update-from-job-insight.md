### User Story JD.18 – Trigger New Fit Score After Profile Update from Job Insight

**As a** job seeker  
**I want** my fit score to update automatically after I revise my profile in response to a job’s required skills  
**So that** I can immediately see the improvement in alignment for the job I’m interested in

---

**Description:**  
Once a job is logged and the initial fit score is calculated, users are prompted to enhance their profile by supplying experience that supports any unmatched skills. After updating their profile, the system should detect these changes, trigger a fresh fit score calculation using the current job version, and show a comparative result.

---

**Acceptance Criteria:**
- [ ] When the user updates their profile from a job prompt, the system stores a new ProfileVersion
- [ ] System recalculates the fit score for the same JobVersion using the new ProfileVersion
- [ ] User sees a before-and-after score comparison (e.g., from 62% to 83%)
- [ ] System highlights which additional skills were now matched due to the update
- [ ] Fit score history is stored per (JobVersion, ProfileVersion) combination
- [ ] User is notified when the recalculated score is available

---

**Dependencies:**
- Profile versioning logic
- Fit score engine
- JobVersion compatibility checks
- Fit score history tracking
- Notification engine (in-app or alert system)

---

**Priority:** High  
**Tags:** profile-update, fit-score-recalc, skill-alignment, job-insight, UX-feedback, scoring-history
