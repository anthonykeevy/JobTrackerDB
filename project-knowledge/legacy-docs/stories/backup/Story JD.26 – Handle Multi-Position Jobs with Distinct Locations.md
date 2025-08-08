### User Story JD.26 – Handle Multi-Position Jobs with Distinct Locations

**As a** system  
**I want** to split a single job listing into multiple entries when it lists roles across distinct locations  
**So that** each position is accurately represented and can be individually evaluated for fit

---

**Description:**  
Some job listings represent multiple openings in different cities (e.g., “1 role in Sydney, 1 in Melbourne”). This story ensures those listings are parsed into distinct job entries per location so each can have its own commute estimate, skill relevance, and fit score. However, if multiple hires are at the same location, the job should remain a single listing with a higher unit count.

---

**Acceptance Criteria:**
- [ ] System detects when a job listing refers to multiple geographic locations
- [ ] When different locations are listed, the job is split into separate entries (e.g., Job A – Sydney, Job A – Melbourne)
- [ ] If the job lists multiple hires at the same location (e.g., “15 engineers in Brisbane”), it remains a single job with a unit count of 15
- [ ] Each split job entry has its own fit score, commute time, and user logging data
- [ ] The original job description and source are preserved for traceability
- [ ] User sees each location-specific job in their dashboard independently

---

**Dependencies:**
- Location extraction from job description
- Unit count recognition and parsing
- Job split logic in job ingestion flow
- Commute and fit score calculations per split

---

**Priority:** Medium  
**Tags:** job-location, multi-position, split-logic, commute-evaluation, fit-score-integrity
