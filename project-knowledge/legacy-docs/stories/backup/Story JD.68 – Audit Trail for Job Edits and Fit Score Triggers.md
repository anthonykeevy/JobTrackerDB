**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** High  
**Status:** Ready for Dev  
**Type:** System Logging  

**Story:**  
As a system,  
I want to track changes to job records and their downstream effects,  
So that we can understand when/why fit scores or profile prompts were triggered.

**Acceptance Criteria:**
- [ ] Log timestamped changes to job metadata and editor (user/system).
- [ ] Maintain version history with reason (e.g., resubmission, correction).
- [ ] Cross-reference job edit history with fit score recalculations and profile updates.
- [ ] Display audit log in admin or user transparency view.