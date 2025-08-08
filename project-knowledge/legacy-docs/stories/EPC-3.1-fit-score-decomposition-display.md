# FS.1 - Fit Score Decomposition Display

## Goal
Display structured comparison between job-required and user-profiled skills with visual indicators and traceable sources.

## Acceptance Criteria
- User sees visual breakdown of job vs. profile skills using icons (✓, ⚠️, ✕)
- Skills are grouped and tagged by match status, criticality, and type (hard/soft)
- Each skill shows its origin (JD text or profile section)
- Score summary appears alongside breakdown
- Partial matches use duration thresholds or inferred equivalency
- Supports display of detailed reasoning (e.g., "Skill matched via Project X, 3 yrs experience")
- Must support both rule-based breakdown and optional AI augmentation view
- Updates automatically when profile or job version changes

## Tags
`fit-score`, `UI`, `traceability`, `comparison-engine`, `version-awareness`, `skill-visualization`, `rule-logic`

## Dependencies
- Profile versioning module
- Skill extraction and mapping engine
- Job description skill parser
- Scoring engine (rule-based)
- Optional AI augmentation layer
- UI breakdown component
