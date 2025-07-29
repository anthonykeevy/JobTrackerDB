# FS.8 - Fit Score History and Comparison View

## Goal
Provide users with a version-aware timeline of their fit scores, allowing comparison between profile changes and job matches over time.

## Acceptance Criteria
- System stores a timestamped history of fit scores per job and per profile version
- Users can select two or more fit scores to compare side-by-side
- Comparison view shows:
  - Job details
  - Profile version used
  - Skills matched, partially matched, and missing in each case
  - Delta in score and reason for change (e.g., “Added Python to profile”)
- UI includes timeline or graph showing score trends over time
- Users can filter history by job title, score range, or date
- Fit score events are linked to specific profile edits or skill confirmations
- Users can annotate or bookmark major changes (e.g., “Post-certification update”)

## Tags
`fit-score`, `history`, `comparison`, `version-tracking`, `timeline`, `delta-analysis`, `career-trend-visualization`

## Dependencies
- Fit score delta tracker
- Profile versioning engine
- UI comparison and diff module
- Timeline visual component
- Audit log with user edit history
