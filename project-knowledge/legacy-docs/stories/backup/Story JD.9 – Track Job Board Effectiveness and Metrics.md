### User Story JD.9 – Track Job Board Effectiveness and Metrics

**As a** platform administrator  
**I want** to analyze the effectiveness and characteristics of different job boards  
**So that** I can provide better recommendations to users and maintain a quality job board index

---

**Description:**  
The system should log metadata about job boards each time a job is captured, including the origin, redirect behavior, company relationships, and classification by industry or functional area. Over time, these attributes will build up a rich profile of each job board, which can then be surfaced to help users select high-quality sources. The system should track metrics such as job volume, job diversity, user success rate, and common redirect paths.

---

**Acceptance Criteria:**
- [ ] Log the source job board and any redirect path for each job logged
- [ ] Record job board classification (e.g., recruiter, corporate, aggregator)
- [ ] Track industry and functional domains inferred from job content
- [ ] Aggregate stats per job board:
  - Number of jobs logged
  - Average metadata completeness
  - Fit score averages
  - Redirect complexity
- [ ] Display job board guidance to users based on historical quality
- [ ] Periodic audit/report generation for job board performance

---

**Dependencies:**
- Job log metadata capture pipeline
- Job board schema with classification fields
- Job-to-industry and function inference module
- Analytics dashboard or reporting module

---

**Priority:** Medium  
**Tags:** job-board-metrics, analytics, source-quality, user-guidance, tracking
