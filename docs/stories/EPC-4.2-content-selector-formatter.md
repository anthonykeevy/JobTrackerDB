# RT.2 - Content Selector and Formatter

## Goal
Enable users to select which components of their profile to include in the resume and format them with job-aligned phrasing and structure.

## Acceptance Criteria
- Users can browse available content blocks drawn from their profile:
  - Work experience
  - Projects
  - Education
  - Skills
  - Certifications
  - Summary/About
- For each block, users can:
  - Include or exclude it
  - Reorder its position
  - Edit AI-generated bullet points or summaries
- AI offers rewritten bullets using terminology from the job description
- Content reflects confirmed profile data (version-aware)
- Rejected or hidden blocks are stored for reuse in other resume versions
- Formatter supports resume-friendly phrasing (e.g., action-result structure)
- AI-generated bullets highlight skills matched to the job
- Editing interface offers side-by-side view of job keywords and current phrasing

## Tags
`resume-content`, `block-selection`, `ai-rewriting`, `job-alignment`, `bullet-formatting`, `profile-integration`, `user-customization`

## Dependencies
- Profile data access layer
- JD parser and keyword highlighter
- AI summarization and bullet engine
- Resume template manager
- Editable UI content blocks with drag/drop and preview
