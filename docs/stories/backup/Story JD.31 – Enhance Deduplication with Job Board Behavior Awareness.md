### User Story JD.31 – Enhance Deduplication with Job Board Behavior Awareness

**As a** system  
**I want** the deduplication engine to account for known dynamic behaviors of job boards  
**So that** identical jobs aren't mistakenly treated as separate entries due to changing URLs or formatting quirks

---

**Description:**  
Certain job boards (e.g., LinkedIn, company ATS platforms) dynamically alter job URLs or inject user/session metadata into descriptions. This story ensures the deduplication logic respects job board-specific rules and uses multiple weighted fields (title, company, description, job board source) to determine job uniqueness instead of over-relying on URLs.

---

**Acceptance Criteria:**
- [ ] Deduplication engine references job board metadata when comparing jobs
- [ ] System applies adjusted logic if the board is flagged as using dynamic URLs
- [ ] Deduplication uses a weighted scoring system across:
  - Job title (high weight)
  - Company name (medium-high, allow fuzzy match)
  - Description (high weight)
  - Source board and hierarchy (medium)
  - Final job URL (low for dynamic boards, medium-high for static)
- [ ] If a likely duplicate is found, prompt the user to confirm reuse or log as a new version
- [ ] Reused jobs retain shared metadata and audit references
- [ ] All deduplication outcomes are traceable and overrideable by admin

---

**Dependencies:**
- JobBoard metadata classification (dynamic/static URL behavior)
- Existing deduplication framework
- Fuzzy matching module for company comparison
- Admin override interface for duplicates

---

**Priority:** High  
**Tags:** deduplication, job-board-awareness, dynamic-url, metadata-precision, audit-traceability
