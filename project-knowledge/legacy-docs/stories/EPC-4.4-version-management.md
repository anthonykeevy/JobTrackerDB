# RT.4 - Version Management

## Goal
Support the creation, storage, and tracking of multiple resume versions per user, each tied to a specific job and profile version.

## Acceptance Criteria
- Each resume version is linked to:
  - A specific job description (JD)
  - A specific profile version
  - A creation timestamp
- Users can:
  - Create new resumes for the same or different jobs
  - Duplicate existing versions as templates
  - Rename, archive, or delete resume versions
- Fit score metadata and JD reference are embedded in each resume version
- Resume version list shows key attributes:
  - Job title or company
  - Resume structure type
  - Last modified date
- System prevents edits to locked versions (e.g., already submitted)
- Resume history can be filtered by job, date, or layout type
- Exported files include version metadata in filename (e.g., `resume-jd123-v2.pdf`)

## Tags
`resume-versioning`, `job-linkage`, `profile-snapshot`, `resume-management`, `audit-traceability`, `resume-history`, `export-naming`

## Dependencies
- Profile versioning engine
- Job log tracker
- Resume storage module
- Metadata tagging service
- UI list and filter components
