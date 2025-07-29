**Story ID:** JA.4  
**Title:** Artifact History Viewer  
**Epic:** Epic 6 – Job Search Artifacts & Communication Assistant  
**Owner:** Developer  
**Priority:** Medium  
**Story Points:** 3  
**Tags:** versioning, artifact-traceability, markdown-storage, job-log-linking, export-viewer  

## Description:
As a user, I want to view a history of previously generated job communication artifacts so that I can reference, reuse, or revise them based on past applications.

## Acceptance Criteria:
- Users can access a chronological view of generated cover letters, recruiter messages, and thank-you notes
- Each entry shows metadata: Job title, Company, Artifact type, Date/Time, Profile version, PromptID
- Each version is viewable in rendered markdown
- Users can download past artifacts in multiple formats (PDF, DOCX, HTML)
- Linked job log and profile version can be accessed directly from artifact view
- Ability to rate each artifact post-viewing if not already done

## Dependencies:
- Artifact storage system with versioning
- Metadata logger (JobID, PromptID, ProfileVersion, Timestamps)
- Markdown renderer and export engine
- Job log and profile integration
