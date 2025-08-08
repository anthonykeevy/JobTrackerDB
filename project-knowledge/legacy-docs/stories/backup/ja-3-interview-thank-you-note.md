**Story ID:** JA.3  
**Title:** Interview Thank You Note Assistant  
**Epic:** Epic 6 – Job Search Artifacts & Communication Assistant  
**Owner:** Developer  
**Priority:** Medium  
**Story Points:** 3  
**Tags:** post-interview, ai-messaging, markdown-export, user-feedback, communication-assistant  

## Description:
As a job seeker, I want to generate a professional thank-you or follow-up message after an interview so that I can reinforce my interest and leave a positive impression.

## Acceptance Criteria:
- Users can initiate a follow-up message from a job log entry
- System provides templates or AI-generated drafts based on interview context
- Users can adjust tone and message length (e.g., brief thank-you or detailed follow-up)
- Message is editable and rendered in markdown
- Preview and export to PDF, HTML, or plain text supported
- Each message includes metadata: JobID, InterviewDate (if available), PromptID, Timestamp
- Filename follows structured format: `[FullName]_[JobTitle]_ThankYouNote_[Company]_[YYYYMMDD-HHMM].pdf`
- User feedback rating is logged per artifact

## Dependencies:
- Job log with interview date or notes (optional)
- Prompt engine with tone customization
- Markdown rendering and export service
- Artifact storage and versioning
