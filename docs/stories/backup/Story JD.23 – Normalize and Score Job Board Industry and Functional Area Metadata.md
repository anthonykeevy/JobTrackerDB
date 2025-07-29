### User Story JD.23 – Normalize and Score Job Board Industry and Functional Area Metadata

**As a** system  
**I want** to infer and store the dominant industries and functional areas associated with each job board  
**So that** users can filter boards by relevance and the system can auto-recommend job boards by career interest

---

**Description:**  
Job boards serve different niches—some are tech-specific, others focus on accounting or medical fields. This story introduces logic to auto-categorize job boards based on the aggregate history of jobs posted through them, helping guide users toward relevant discovery points.

---

**Acceptance Criteria:**
- [ ] Each job board is linked to one or more inferred industries and functional areas (e.g., "Tech", "Finance", "Healthcare", "Marketing")
- [ ] System maintains running stats on job post frequency by category per board
- [ ] System updates board classification dynamically as new job logs are added
- [ ] Users can view board categories as tags or filters in the UI
- [ ] Admins can manually adjust or override inferred metadata
- [ ] Categories inform recommendation logic (e.g., “Top boards for Data Science roles”)

---

**Dependencies:**
- Industry and role taxonomy service
- Job logging and job board link structure
- Analytics engine or aggregation logic
- Admin interface for manual override and confirmation

---

**Priority:** Medium  
**Tags:** job-board-metadata, industry-normalization, board-relevance, intelligent-recommendation, job-sourcing
