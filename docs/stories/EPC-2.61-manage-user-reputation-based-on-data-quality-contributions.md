### User Story JD.61 – Manage User Reputation Based on Data Quality Contributions

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** System Feature  

**Story:**  
As a system,  
I want to track the quality and accuracy of user-contributed data over time,  
So that I can maintain platform integrity and assign user reputation scores accordingly.

---

**Acceptance Criteria:**
- [ ] Define a user reputation score model based on:
  - [ ] Accuracy of logged job metadata
  - [ ] Verification of job status
  - [ ] Acceptance rate of metadata suggestions
  - [ ] Frequency of corrections from moderators
- [ ] Increment reputation for:
  - [ ] Verified jobs that are accurate
  - [ ] Accepted metadata improvements
  - [ ] Helpful reporting of invalid or duplicate listings
- [ ] Decrease reputation for:
  - [ ] Repeated inaccurate entries
  - [ ] Metadata misuse or irrelevant tagging
  - [ ] Ignoring moderator feedback
- [ ] Visibly display user reputation (optional toggle) or use it for:
  - [ ] Prioritizing suggestions
  - [ ] Gating advanced features
  - [ ] Informing moderation trust levels
- [ ] Notify users when reputation changes with reasons (positive or negative).

---

**Dependencies:**
- User contribution analytics engine
- Moderator feedback system
- Gamification integration
- Notification service

---

**Tags:** user-reputation, data-quality, trust-signal, gamification, moderation-feedback
