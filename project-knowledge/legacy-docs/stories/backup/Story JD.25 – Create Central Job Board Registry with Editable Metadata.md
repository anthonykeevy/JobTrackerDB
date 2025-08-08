### User Story JD.25 – Create Central Job Board Registry with Editable Metadata

**As a** system  
**I want** a central registry of known job boards with editable classification metadata  
**So that** the platform can accurately identify board behavior and guide users accordingly

---

**Description:**  
This story introduces the foundational registry for managing job board data. Each job board entry includes type, industry focus, redirection behavior, company affiliation (if applicable), and board specialization. This metadata improves job deduplication logic, traceability, skill inference accuracy, and gamification.

---

**Acceptance Criteria:**
- [ ] System stores job board entries in a structured schema (e.g., JobBoard table)
- [ ] Each entry supports the following metadata:
  - Board type (e.g., recruiter, corporate, aggregator)
  - Parent company (if applicable)
  - Known redirection behavior
  - Inferred industry categories
  - Common functional areas (e.g., engineering, marketing)
  - Dynamic URL behavior flag
- [ ] Admin users can update or override board metadata
- [ ] System references this metadata during:
  - Job deduplication
  - Job versioning
  - Commute estimation
  - Fit scoring context
  - Gamification contribution points
- [ ] Board details are accessible to users as part of job logging or review interface

---

**Dependencies:**
- JobBoard table schema
- Admin interface for metadata override
- Integration points across job parsing and fit scoring flows
- Gamification system linkage to metadata contribution points

---

**Priority:** High  
**Tags:** job-board-registry, metadata-governance, AI-context, classification, system-integrity
