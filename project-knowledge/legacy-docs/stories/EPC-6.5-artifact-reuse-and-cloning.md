**Story ID:** JA.5  
**Title:** Artifact Reuse and Cloning  
**Epic:** Epic 6 – Job Search Artifacts & Communication Assistant  
**Owner:** Developer  
**Priority:** Medium  
**Story Points:** 3  
**Tags:** artifact-reuse, cloning, markdown-editor, versioning, job-log-integration  

## Description:
As a user, I want to reuse or clone a previously generated artifact so that I can efficiently adapt it for a new job application without starting from scratch.

## Acceptance Criteria:
- Users can clone any previously generated cover letter, recruiter message, or thank-you note
- System creates a new editable instance linked to a new job log (user selects or creates target)
- Original version remains unchanged and traceable
- New instance inherits structure and markdown formatting from the original
- Metadata (PromptID, JobID, ProfileVersion) is updated to reflect the new context
- Export and feedback workflows apply to the cloned version

## Dependencies:
- Artifact history viewer
- Markdown editor and renderer
- Artifact versioning and logging infrastructure
- Job log and profile selection interface
