# FS.4 - Profile Version Triggered by Gap Resolution

## Goal
Ensure that any user-initiated change to the profile during skill gap resolution results in a new, traceable version for accurate fit score recalculations and historical audit.

## Acceptance Criteria
- When a user confirms, adds, or edits a skill during gap resolution, the system:
  - Captures the full profile state before and after change
  - Creates a new profile version ID
  - Logs timestamp and user identity linked to change
- All fit scores recalculated from the new version reference that version explicitly
- Previous fit scores are preserved and linked to their prior profile version
- Users can view the change summary (diff) between profile versions
- Versioning applies equally to accepted AI-inferred skills and manually added skills
- Rollback option exists to revert to any previous profile version
- UI must clearly indicate when a new version has been created and why

## Tags
`profile-versioning`, `gap-resolution`, `audit-trail`, `fit-score-trigger`, `change-log`, `traceability`, `rollback-support`

## Dependencies
- Profile versioning and snapshot engine
- Fit score recalculation module
- Skill confirmation and editing interfaces
- Audit log framework
- Version comparison and diff UI
