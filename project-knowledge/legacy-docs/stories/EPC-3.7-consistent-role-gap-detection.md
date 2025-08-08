# FS.7 - Consistent Role Gap Detection

## Goal
Identify recurring skill gaps for a specific role across multiple job logs, enabling users to prioritize broader improvements and align career growth efforts.

## Acceptance Criteria
- System tracks and clusters jobs with the same target role or title (e.g., “Frontend Developer”)
- For each clustered group, the system identifies:
  - Skills frequently required but not present in the user profile
  - Patterns in required experience level (e.g., React 3+ years)
  - Gaps that appear in >50% of job logs for that role
- Results are displayed as a role-level gap analysis dashboard
- User can take action on each identified recurring gap:
  - Add missing skill to roadmap
  - Update profile with new evidence
  - Acknowledge as aspirational or not applicable
- System recommends skill priorities based on recurrence and criticality
- Fit score improvements can be tracked at a role-cluster level
- Analysis updates as more jobs are logged under the same role group

## Tags
`trend-detection`, `role-alignment`, `skill-gaps`, `career-guidance`, `fit-score-aggregation`, `roadmap-integration`

## Dependencies
- Role clustering and normalization engine
- Skill extraction and frequency analysis module
- Roadmap and profile linkage
- Role-focused UI module
- Fit score tracker across job cohorts
