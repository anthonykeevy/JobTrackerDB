**Story ID:** JA.7  
**Title:** Multi-format Export & Delivery Options  
**Epic:** Epic 6 – Job Search Artifacts & Communication Assistant  
**Owner:** Developer  
**Priority:** Medium  
**Story Points:** 3  
**Tags:** export-options, markdown-conversion, artifact-delivery, user-preferences, job-artifacts  

## Description:
As a job seeker, I want to export my generated job communication artifacts in different formats so that I can choose the most appropriate format for the application channel.

## Acceptance Criteria:
- Users can export any artifact (cover letter, recruiter message, follow-up) as PDF, DOCX, or HTML
- Export options are available from preview or artifact history view
- Exported documents preserve layout, tone, and formatting consistency
- Downloadable filenames use naming convention: `[FullName]_[JobTitle]_[ArtifactType]_[Company]_[YYYYMMDD-HHMM]`
- Optional user preference setting to auto-export a default format upon generation
- Export events are logged with timestamp, format type, and artifact ID

## Dependencies:
- Markdown renderer and export service
- File storage and delivery mechanism
- Artifact history module
