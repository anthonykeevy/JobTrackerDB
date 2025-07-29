### User Story JD.14 – Show Related Jobs Logged by Other Users

**As a** job seeker  
**I want** to see if other users have logged or applied to the same job I'm viewing  
**So that** I can gain insight into its popularity and see possible enhancements to job metadata

---

**Description:**  
When a user views or logs a job, the system should indicate if the same job (by signature or ID) has been interacted with by other users. The system should highlight if other versions exist (due to edited metadata) and allow viewing differences. Popular jobs may be flagged as high-interest, and users can optionally view anonymized enhancement suggestions (e.g., improved title, missing tech stack).

---

**Acceptance Criteria:**
- [ ] Job detail view shows number of other users who logged this job
- [ ] If alternate versions exist, system surfaces these with change summaries
- [ ] System can highlight metadata improved by other users
- [ ] Users can opt in to view anonymized notes or enhancements
- [ ] Popular jobs may receive a tag or icon (e.g., 🔥 Trending Role)
- [ ] No personal details of other users are ever shown

---

**Dependencies:**
- Job deduplication and version tracking logic
- System to aggregate and compare metadata changes
- UI component for rendering version highlights
- Opt-in user settings for metadata enhancement suggestions

---

**Priority:** Medium  
**Tags:** collaboration, job-sharing, popularity-insight, version-awareness, metadata-enhancement
