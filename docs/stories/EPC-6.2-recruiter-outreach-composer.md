**Story ID:** JA.2  
**Title:** Recruiter Outreach Composer  
**Epic:** Epic 6 – Job Search Artifacts & Communication Assistant  
**Owner:** Developer  
**Priority:** Medium  
**Story Points:** 3  
**Tags:** recruiter-contact, communication-assistant, ai-messaging, markdown-export, job-logging  

## Description:
As a job seeker, I want help composing a message to contact a recruiter about a role so that I can make a positive first impression and express genuine interest.

## Acceptance Criteria:
- Users can initiate a message composition from a job log entry
- System auto-fills recruiter name, company, job title, and any available contact platform (e.g., LinkedIn, email)
- AI generates message text based on user profile, job description, and selected tone
- Message content is rendered in markdown and editable
- User can preview or export message as plain text, HTML, or PDF
- All generated messages are stored with metadata (JobID, ContactMethod, PromptID, Timestamp)
- Filename format: `[FullName]_[JobTitle]_RecruiterMessage_[Company]_[YYYYMMDD-HHMM].txt`

## Out of Scope:
- Message sending via external platforms (e.g., LinkedIn API integration)

## Dependencies:
- JD and recruiter data from job log
- Profile versioning and prompt engine
- Markdown rendering and export service
- Prompt management console
