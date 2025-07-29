### User Story JD.33 – Include Location in Deduplication and Log Job Age Metadata

**As a** system  
**I want** to factor job location and age into deduplication and job metadata  
**So that** users get cleaner job listings and understand job posting timelines

---

**Description:**  
Job postings may appear identical but differ by location or posting age. This story ensures location is weighted in deduplication logic, and that each job captures an estimated "first seen" and "last seen" timestamp. Additionally, it tracks how long the job has been active and flags reposted listings for transparency and confidence.

---

**Acceptance Criteria:**
- [ ] Deduplication engine includes job location with moderate-high weight
- [ ] Location comparison handles fuzzy matches and multi-site listings
- [ ] Each job record includes:
  - `first_seen_date` (earliest timestamp seen)
  - `last_seen_date` (most recent timestamp seen)
  - `is_repost` flag (if same job reappears with gap or edits)
- [ ] UI shows job age and repost status to users
- [ ] Jobs split into separate entries if locations differ meaningfully
- [ ] Do not split jobs based solely on position count (e.g., 5 hires for one location)
- [ ] Job age and reposting data used in reuse and relevance scoring

---

**Dependencies:**
- Deduplication framework
- Job schema with age and location fields
- Fuzzy matching for multi-location detection
- Job logging audit trail with timestamps
- UI display for age and repost info

---

**Priority:** High  
**Tags:** deduplication, job-location, job-age, repost-detection, traceability
