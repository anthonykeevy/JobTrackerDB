### User Story JD.53 – Recruiter Contact Discovery and Metadata Enrichment

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to enrich job entries by discovering and associating recruiter contact metadata,  
So that we can improve recruiter traceability, enable future verification, and support job evaluation integrity.

---

**Acceptance Criteria:**
- [ ] Automatically extract recruiter name, email, phone (if present) from job listing or redirected job board page.
- [ ] If not present, prompt user to optionally supply recruiter contact details (e.g., from follow-up emails or LinkedIn).
- [ ] Provide a recruiter enrichment workflow that:
  - [ ] Attempts LinkedIn discovery from name and company
  - [ ] Stores LinkedIn profile URL if found
  - [ ] Validates email format and deduplicates contact points
- [ ] Link recruiter contact metadata to recruiter entity in system.
- [ ] Maintain separation between public metadata and user-supplied contact info.
- [ ] Allow users to flag recruiter metadata for review or correction.
- [ ] Gamify the enrichment process with point incentives.

---

**Dependencies:**
- Recruiter entity model
- Metadata enrichment service
- LinkedIn scraping or search API (if permitted)
- Recruiter verification UI
- Gamification module
- Privacy and consent model for handling recruiter data

---

**Tags:** recruiter-enrichment, contact-metadata, LinkedIn-linking, job-metadata, recruiter-traceability
