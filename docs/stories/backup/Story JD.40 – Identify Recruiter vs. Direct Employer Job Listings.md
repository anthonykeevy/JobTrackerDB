### User Story JD.40 – Identify Recruiter vs. Direct Employer Job Listings

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to detect whether a job is posted by a recruiter or by a direct employer,  
So that users can understand the hiring chain and tailor their application strategy accordingly.

---

**Acceptance Criteria:**
- [ ] Implement classifier logic to identify recruiter job listings vs. direct employer posts.
- [ ] Use job board metadata, posting company name, and historical patterns to infer source.
- [ ] If recruiter source is confirmed or highly likely, label the listing with a “Recruiter Listing” badge.
- [ ] If direct employer is detected, label with “Direct Employer” tag.
- [ ] Allow users to suggest corrections to source classification if needed.
- [ ] Store recruiter classification in job metadata and version history.
- [ ] Display this classification in job detail view and scoring dashboard.

---

**Dependencies:**
- Job board classifier module
- Recruiter identification heuristics and training dataset
- Metadata editing and review interface
- Epic: Job Discovery and Logging for Profile Matching

---

**Tags:** recruiter-detection, metadata-classification, job-insight, job-publisher-source
