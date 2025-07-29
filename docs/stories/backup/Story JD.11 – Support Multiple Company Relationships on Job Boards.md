### User Story JD.11 – Support Multiple Company Relationships on Job Boards

**As a** data architect or platform admin  
**I want** to model and capture complex company structures associated with job boards  
**So that** users understand which company they’re applying to and the platform can maintain accurate associations for job tracking

---

**Description:**  
Some job boards are managed by parent companies but serve roles for multiple subsidiary or affiliate brands. The system must recognize and reflect these hierarchical relationships, allowing a single job board to serve multiple companies while still attributing each job correctly. This will enhance job analytics, improve deduplication, and support better industry classification over time.

---

**Acceptance Criteria:**
- [ ] A job board can be associated with one or many companies
- [ ] Each job logged includes the specific company offering the role
- [ ] Companies can be marked as:
  - Parent (managing the board)
  - Subsidiary (advertising roles via parent board)
- [ ] UI and analytics tools display these relationships clearly
- [ ] Users are made aware if a job board serves multiple entities
- [ ] Role-level metadata reflects the true company behind the job
- [ ] System tracks industry and functional stats per company, not just per board

---

**Dependencies:**
- Extended schema for JobBoard and Company relationships
- Job-to-Company attribution logic
- Industry tagging per company
- UI indicators and admin controls for hierarchy

---

**Priority:** Medium  
**Tags:** job-board-hierarchy, company-structure, data-integrity, analytics, job-attribution
