# User Story 3.3: Profile Storage and Editing

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** 3.3  
**Priority:** High  
**Status:** Revised  
**Owner:** Product Owner (PO)

---

## Description

As a **user**,  
I want **my profile to be stored, versioned, and editable over time**,  
So that **I can build a reusable, evolving representation of my career that supports tailored outputs**

---

## Acceptance Criteria

1. User profile is saved after each confirmed milestone.
2. Each saved version includes:
   - Timestamp
   - Change summary
   - User-provided happiness score (optional)
3. Users can:
   - Edit any profile section
   - View previous profile milestones and revert to one if needed
   - See differences between current state and last confirmed version
4. Profile edits must be re-confirmed before downstream usage (resume, fit scoring).
5. New additions not yet confirmed are clearly marked.
6. Artifacts and fit scores always reference the exact profile version they were generated from.

---

## Definition of Done

- Profile data is stored with version history and milestone metadata
- Editable interface allows real-time changes to all fields
- Approval flow resets on change detection
- Profile version info is embedded into all resume/fit outputs
- Notification system alerts users when outputs are outdated

---

## Dependencies

- Profile schema  
- Version control and milestone manager  
- Resume/fit generation modules  
- Change detection and approval workflow
