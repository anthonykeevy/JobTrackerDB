# FS.5 - Learning Path Suggestions for Missing Skills

## Goal
Guide users toward structured upskilling by suggesting courses, certifications, and practice projects to address identified skill gaps.

## Acceptance Criteria
- For each unmatched or aspirational skill, system provides curated learning resources:
  - Online courses (free/paid)
  - Certifications
  - Practice project templates or community challenges
- Suggestions are prioritized based on:
  - Skill criticality (from JD)
  - User's target role and career aspirations
  - Duration to complete vs. job application timelines
- Resources include metadata: provider, time required, level (beginner/advanced), cost
- Users can accept suggestions into a learning roadmap module
- Roadmap entries are linked to specific fit gaps and displayed in profile
- Users can manually mark completion or progress status
- System reminds users of pending roadmap items before re-evaluating fit
- Roadmap module supports multi-role tracking and filtering

## Tags
`upskilling`, `learning-path`, `roadmap`, `gap-resolution`, `career-growth`, `recommendation-engine`

## Dependencies
- Learning resource aggregation service or API (e.g., Coursera, Udemy, etc.)
- Skill tagging and prioritization logic
- Roadmap UI module
- Profile linkage for pending goals
- Reminder/notification system
- Fit score integration with roadmap completion
