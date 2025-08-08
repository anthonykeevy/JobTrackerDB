**Story ID:** JA.6  
**Title:** Artifact Feedback & Prompt Improvement Logger  
**Epic:** Epic 6 – Job Search Artifacts & Communication Assistant  
**Owner:** Developer  
**Priority:** Medium  
**Story Points:** 3  
**Tags:** feedback, prompt-evaluation, ai-tuning, satisfaction-score, artifact-quality  

## Description:
As a platform administrator, I want to collect user feedback on generated artifacts and track prompt performance so that I can improve AI output quality across models and use cases.

## Acceptance Criteria:
- Users can rate each generated message (e.g., stars or thumbs) post-preview or post-export
- Optional text comment field for improvement suggestions
- Feedback is logged with PromptID, ModelID, ArtifactType, and Timestamp
- System aggregates satisfaction scores per prompt and per model
- Dashboard or exportable logs for prompt performance analysis
- Prompts flagged below threshold are reviewed or tuned in Prompt Management Console

## Dependencies:
- Prompt management system with prompt versioning
- Feedback form tied to artifact generation interface
- Prompt metadata logger (PromptID, ModelID, OutputTokenCount)
- Analytics dashboard or export service
