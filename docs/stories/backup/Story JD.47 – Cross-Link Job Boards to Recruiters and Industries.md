### User Story JD.47 – Cross-Link Job Boards to Recruiters and Industries

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to classify job boards by recruiter association and industry alignment,  
So that I can help users target the most relevant boards for their sector and understand which listings are recruiter vs. employer driven.

---

**Acceptance Criteria:**
- [ ] Track recruiter classification for each job board and update over time based on job source patterns.
- [ ] Maintain a structured industry tagging schema for each board based on aggregated job content.
- [ ] Allow boards to be multi-tagged (e.g., technical + health for specialist sites).
- [ ] Present recruiter classification clearly to users (e.g., “This job board posts mainly recruiter listings”).
- [ ] Allow user-suggested classifications for unknown boards with manual review queue.
- [ ] Display dominant industries per board in UI to help user navigation.
- [ ] Use board classification to recommend more industry-aligned boards to users during job discovery.

---

**Dependencies:**
- Job board metadata engine
- Job-to-industry inference module
- Recruiter classification heuristic or ML model
- User suggestion interface for metadata
- Review queue workflow

---

**Tags:** job-board-classification, recruiter-detection, industry-alignment, job-discovery, user-guidance
