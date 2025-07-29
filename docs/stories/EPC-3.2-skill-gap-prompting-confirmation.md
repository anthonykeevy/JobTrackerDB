# FS.2 - Skill Gap Prompting and Confirmation

## Goal
When fit score reveals a skill gap, prompt the user to confirm the absence, supply additional profile detail, or flag it as an aspirational skill.

## Acceptance Criteria
- Upon identifying a missing skill in the fit score view, system presents user with a prompt:
  - Confirm skill is not currently present
  - Add skill with supporting context (e.g., project, role, training)
  - Mark skill as aspirational (to address later)
- Prompt includes pre-filled suggestions if the system suspects the skill might be inferred
- Skill additions or confirmations update the current working profile version
- Aspirational skills are logged in a roadmap module (not counted toward score, but saved)
- Confirmations include optional notes or rationale (e.g., “I used this skill in Project Y but didn’t list it”)
- System differentiates between confirmed and speculative skill gaps
- Changes to profile trigger fit score recalculation
- All actions are audit-tracked per user and profile version

## Tags
`gap-resolution`, `profile-edit`, `skill-confirmation`, `user-feedback-loop`, `aspirational-tracking`, `inferred-skill-suggestion`

## Dependencies
- Profile editor with inline skill edit interface
- Skill match and inference engine
- Fit score engine
- Audit/versioning logic
- Aspirational roadmap module (optional but recommended)
- UI prompt engine
