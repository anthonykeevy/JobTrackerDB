# RT.5 - JD–Resume Traceability

## Goal
Provide transparency between the job description requirements and the corresponding resume content, enabling users to validate alignment and ensure tailored relevance.

## Acceptance Criteria
- Each bullet or section in the resume can be linked back to a job description phrase or requirement
- JD terms are highlighted or annotated within the resume editor to indicate matches
- Users can hover or click to view the source JD snippet that inspired each line of resume content
- System provides a traceability audit mode to show a map of JD → Resume alignment
- Resume content that does not align with the JD is flagged (optionally) to guide user decisions
- Traceability view supports filtering (e.g., “show unmatched JD requirements”)
- Traceability can be toggled on/off during resume editing and preview
- Exported resumes optionally include a traceability appendix (for internal tracking or recruiter transparency)

## Tags
`traceability`, `jd-alignment`, `resume-transparency`, `audit-mode`, `resume-editor`, `jd-to-resume-mapping`

## Dependencies
- JD parsing and keyword extraction module
- Resume content generator with mapping metadata
- Resume editor with annotation support
- Traceability map engine
- Optional appendix generator for export
