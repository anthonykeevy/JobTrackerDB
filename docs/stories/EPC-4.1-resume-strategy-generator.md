# RT.1 - Resume Strategy Generator

## Goal
Analyze the job description and user profile to recommend the optimal resume structure and emphasis strategy.

## Acceptance Criteria
- System reviews job description and associated fit score data
- Recommends one of the standard resume types:
  - Chronological (experience-focused)
  - Functional (skills-focused)
  - Hybrid (balanced)
- Suggests content emphasis zones:
  - Technical proficiency
  - Leadership/impact
  - Certifications/education
- Suggests optional elements to include or omit (e.g., summary section, project spotlight)
- Recommends tone and style presets (e.g., concise, assertive, creative)
- Explanations provided for recommendations (e.g., “Functional resume recommended due to early-career profile and high technical skill match”)
- Recommendations adjust if user toggles seniority, target role, or job sector
- User can accept or override strategy and proceed to customization

## Tags
`resume-strategy`, `layout-recommendation`, `fit-score-alignment`, `career-stage`, `tone-guidance`, `ai-recommendation`

## Dependencies
- Fit score analysis module
- JD parsing and tagging engine
- Profile structure and metadata
- Resume layout definition catalog
- UI component for strategy preview and selection
