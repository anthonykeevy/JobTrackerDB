### User Story JD.58 – Suggest Corrections for Job Metadata and Structure

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a user,  
I want to suggest corrections to inaccurate job metadata (e.g., title, company, recruiter, location),  
So that the job database remains accurate, structured, and valuable for all users.

---

**Acceptance Criteria:**
- [ ] Allow users to flag job metadata fields (e.g., title, description, company) as incorrect or incomplete.
- [ ] Provide a correction interface for users to suggest updates.
- [ ] Track suggestions with timestamp and user ID.
- [ ] Allow moderators or system validation to review and approve/reject updates.
- [ ] Preserve original metadata while maintaining correction history (versioning).
- [ ] If accepted, update affected jobs and recalculate relevant fit scores.
- [ ] Award gamification points for accepted suggestions or helpful corrections.

---

**Dependencies:**
- Job entity model and versioning support
- Correction suggestion model
- Moderator or automated validation workflow
- Fit score recalculation pipeline
- Gamification engine

---

**Tags:** job-metadata, user-corrections, data-integrity, moderation, gamification
