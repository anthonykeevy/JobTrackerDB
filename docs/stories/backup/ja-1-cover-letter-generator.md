**Story ID:** JA.1  
**Title:** Cover Letter Generator  
**Epic:** Epic 6 – Job Search Artifacts & Communication Assistant  
**Owner:** Developer  
**Priority:** High  
**Story Points:** 5  
**Tags:** artifact-generation, cover-letter, ai-writing, markdown-export, personalization  

## Description:
As a job seeker, I want to generate a customized cover letter aligned with a specific job description and my profile so that I can submit a complete and compelling application.

## Acceptance Criteria:
- Users can select a job from their job log and a corresponding profile version.
- System analyzes JD and profile to recommend cover letter structure and emphasis.
- Users can select a tone (e.g., professional, enthusiastic, confident).
- AI generates the initial draft using the appropriate prompt and model.
- Cover letter is rendered in markdown format and editable.
- Users can preview the output in PDF, DOCX, or HTML format.
- Each generated version is stored with metadata (JobID, ProfileVersion, PromptID, Timestamp).
- Filename follows structured convention: `[FullName]_[JobTitle]_CoverLetter_[Company]_[YYYYMMDD-HHMM].pdf`.
- User feedback (rating) is captured post-preview or export.

## Out of Scope:
- Manual editing beyond markdown-rendered editor

## Dependencies:
- JD parser and profile versioning engine
- Prompt management system
- Markdown artifact renderer and export engine
- Artifact storage with traceability and versioning
