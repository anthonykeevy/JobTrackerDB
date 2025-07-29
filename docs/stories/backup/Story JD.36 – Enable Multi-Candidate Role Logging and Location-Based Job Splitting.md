### User Story JD.36 – Enable Multi-Candidate Role Logging and Location-Based Job Splitting

**As a** system  
**I want** to intelligently distinguish between jobs with multiple open positions and jobs advertised across multiple locations  
**So that** I can accurately log job entries and ensure correct deduplication and user association

---

**Description:**  
Some job listings advertise multiple hires (e.g., “5 junior developers”) while others span multiple locations (e.g., “1 hire in Sydney, 1 in Melbourne”). This story defines logic to split job entries based on distinct locations but retain single entries for multi-candidate jobs at a single location.

---

**Acceptance Criteria:**
- [ ] System parses job details for:
  - Number of positions (`unit_count`)
  - Number and names of distinct locations
- [ ] If multiple **distinct locations** are detected, system creates a separate job version for each location
- [ ] If multiple positions exist **at one location**, system stores as a single entry with `unit_count > 1`
- [ ] Deduplication logic considers job location during comparison scoring
- [ ] Users can confirm or edit detected locations before logging
- [ ] Job entries with location-based splits maintain a shared `JobGroupID` for relational traceability
- [ ] Fit scoring and commute estimates reflect individualized location splits

---

**Dependencies:**
- Job logging pipeline with multi-location parser
- Job deduplication engine enhancement
- Fit scoring engine location integration
- Job versioning support for split handling
- UI indicator for split job entries across cities

---

**Priority:** High  
**Tags:** job-logging, location-awareness, multi-position, deduplication, job-splitting, traceability
