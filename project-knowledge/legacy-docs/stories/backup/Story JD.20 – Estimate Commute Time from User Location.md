### User Story JD.20 – Estimate Commute Time from User Location

**As a** job seeker  
**I want** to see an estimated commute time from my current location to each job I log  
**So that** I can evaluate the job’s practicality based on travel effort

---

**Description:**  
When a job is logged and its location captured, the system should estimate how long it would take the user to reach that location by car (initially), based on their saved home address. This estimated commute time will be stored with the job log for visibility in fit assessments and decision-making.

---

**Acceptance Criteria:**
- [ ] User’s saved home location is securely stored and retrievable for use in commute calculations
- [ ] System extracts job location from logged data
- [ ] System uses an external or local service (e.g., Google Maps API or similar) to estimate commute time by car
- [ ] Commute estimate is saved with user’s job log record
- [ ] Commute time is displayed clearly on the job view interface
- [ ] Support for fallback/default messaging if location or commute data is unavailable

---

**Dependencies:**
- Secure storage of user home address
- Job location parsing and normalization
- Commute estimation API integration
- UI display component for commute time

---

**Priority:** Medium  
**Tags:** commute-awareness, location-data, job-insight, UX-enhancement, job-log-context
