### User Story JD.19 – Split Multi-Location Jobs (Not Multi-Unit Same Location)

**As a** job seeker  
**I want** job listings for multiple locations to be split into distinct entries  
**So that** each location-specific role can be evaluated independently for fit

---

**Description:**  
Some job descriptions advertise openings in multiple cities or regions. This story ensures these are split into separate job entries to allow tailored evaluation and commute estimation. However, if multiple hires are for the same role in the same location, only one job record is stored, and the total position count is noted.

---

**Acceptance Criteria:**
- [ ] System detects job listings with distinct locations (e.g., “1 in Sydney, 1 in Melbourne”)
- [ ] System creates separate job records for each location with inherited metadata
- [ ] System does **not** split jobs listing multiple hires at a single location (e.g., “5 developers in Sydney”)
- [ ] Job entries note the unit count (number of positions) per location
- [ ] Job versions remain linked to the same parent job ID
- [ ] Each split job triggers its own fit score and commute estimate

---

**Dependencies:**
- NLP location and quantity detection model
- Job model supports unit count and child records per location
- Fit score engine linked to location-specific data
- Commute time calculation logic

---

**Priority:** Medium  
**Tags:** job-location, role-splitting, job-normalization, metadata-accuracy, commute-awareness
