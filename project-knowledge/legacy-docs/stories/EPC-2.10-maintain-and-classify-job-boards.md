### User Story JD.10 – Maintain and Classify Job Boards

**As a** system administrator  
**I want** to maintain a structured repository of job boards with classification metadata  
**So that** users and automated systems can rely on accurate, insightful job board data to enhance job discovery

---

**Description:**  
To support effective job logging and analysis, the platform should maintain a central job board registry. Each job board should include metadata such as its type (e.g., aggregator, recruiter, corporate), associated companies (if any), known redirect behaviors, and inferred dominant industries or functional focus. This allows users to navigate boards confidently and supports AI-assisted classification of new boards added via user discovery.

---

**Acceptance Criteria:**
- [ ] Each job board is stored in a structured registry with:
  - Domain and display name
  - Board type (aggregator, recruiter, corporate)
  - Company association (if any)
  - Industry/functional coverage (inferred or tagged)
  - Redirect patterns and landing behaviors
- [ ] System can auto-tag new boards based on observed behaviors and content
- [ ] Admin UI for manual editing and classification override
- [ ] Job loggers use this registry to guide metadata completion
- [ ] Boards are ranked for reliability and completeness over time
- [ ] Boards with sufficient traffic or usage flagged for deeper audit/review

---

**Dependencies:**
- Job board schema
- Classification engine (manual + AI-assist)
- Analytics tracking job board usage frequency
- Admin tools for registry curation

---

**Priority:** Medium  
**Tags:** job-board-registry, classification, metadata, admin-tools, board-quality, routing
