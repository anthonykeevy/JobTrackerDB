# FS.3 - AI-Suggested Skill Inference

## Goal
Leverage AI to infer potentially missing skills from user profile content and suggest additions with contextual justification.

## Acceptance Criteria
- When fit score identifies unmatched skills, AI scans user profile for potential indirect indicators (e.g., similar project names, tools used)
- System surfaces inferred skills with:
  - Confidence score
  - Supporting context from profile (highlighted sentence or project)
  - Suggested source field for integration (e.g., “Project Experience” or “Certifications”)
- User can accept, reject, or revise inferred skill
- Accepted skills update the current profile version and are tagged as “AI-inferred”
- Rejected skills are stored for learning feedback but not suggested again
- All AI-generated inferences must be audit-tracked and reversible
- Inferences are marked distinctly in UI to avoid confusion with confirmed user entries
- Accepted inferences contribute to recalculated fit score

## Tags
`skill-inference`, `AI-augmentation`, `profile-enhancement`, `user-review`, `versioning`, `feedback-loop`

## Dependencies
- AI layer capable of semantic skill extraction
- Profile data access layer
- Skill taxonomy for mapping inferred terms
- Confidence scoring model
- User action tracking for AI suggestions
- Fit score update trigger on confirmation
