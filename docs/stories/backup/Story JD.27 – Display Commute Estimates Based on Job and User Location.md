### User Story JD.27 – Display Commute Estimates Based on Job and User Location

**As a** job seeker  
**I want** to see an estimated commute time for each job I log  
**So that** I can evaluate how feasible the job is based on travel requirements

---

**Description:**  
For logged jobs with a defined location, the system should calculate and display an estimated travel time by car from the user’s primary location. This helps users understand the daily impact of the job and supports better decision-making. The commute time should be included in the job summary and used optionally in fit evaluation logic.

---

**Acceptance Criteria:**
- [ ] System captures or infers job location during logging
- [ ] User location is either preset or requested upon job log
- [ ] Commute time is calculated using a geolocation service (e.g., Google Maps API or open source)
- [ ] Commute estimate appears in the job details summary
- [ ] Commute estimate is logged and versioned with the job entry
- [ ] Future scoring logic optionally includes commute factor if user enables this preference
- [ ] Users can provide feedback if commute estimate appears incorrect

---

**Dependencies:**
- Location parsing from job description
- User profile location data
- Geolocation and routing service integration
- Job detail summary UI
- Job version schema for storing commute-related metadata

---

**Priority:** Medium  
**Tags:** commute-evaluation, job-location, user-preference, decision-aid, location-services
