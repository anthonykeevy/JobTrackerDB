**Epic Title:** Resume Tailoring Engine

**Epic Owner:** Product Owner (PO)

**Goal:** Empower users to generate tailored resumes that align with specific job descriptions by leveraging their structured profile data and contextual insights from job requirements.

**Background:**
With profiles and job data structured and analyzed through fit scoring, the next step is to generate resumes that reflect each user's best fit. Users require control over resume structure and emphasis to match career stage, industry norms, and job focus. A flexible resume generation engine, driven by profile–JD alignment, is needed to balance automation with personalization. Early-career users may highlight education or skills; senior professionals may lead with leadership outcomes or project scope.

**Design Considerations:**

* Resume is dynamically generated from user profile data, JD parsing, and tone preferences
* Include career highlights, key projects, skill clusters, and personalized narratives
* Use markdown format for storing resumes for version control and lightweight storage
* Markdown is exported to PDF, DOCX, or HTML using a unified export pipeline
* Resume layout fidelity preserved using enhanced markdown or CSS-styled HTML templates
* Support user preference for resume layout (e.g., skills-first vs. experience-first)
* Support multiple resume styles/templates depending on career level or role
* Offer modular section templates (e.g., summary, key skills, projects, outcomes)
* Resume content should trace back to confirmed profile data (version-aware)
* AI narrative tuning layer allows resume tone and content emphasis adjustments
* Resume version links to job log and prompt metadata for traceability
* Export filenames should be human-friendly and context-rich:

  * Format: `[FullName]_[JobTitle]_[Company]_[YYYYMMDD-HHMM].pdf`
  * If timestamp collision occurs, increment minute to ensure uniqueness

**Key Capabilities:**

1. **Resume Strategy Generator**

   * Analyze job description and fit score to determine optimal resume angle
   * Recommend emphasis zones (skills vs. experience vs. achievements)
   * Suggest layout structure type (e.g., functional, hybrid, chronological)

2. **Content Selector and Formatter**

   * Allow users to pick which profile components to include
   * Match JD language to user phrasing where appropriate
   * Automatically generate summaries and bullet points with AI assistance

3. **Design and Layout Control**

   * Offer templates with configurable styles
   * Let users prioritize sections based on role type or preference
   * Support output formats: PDF, DOCX, and Web view

4. **Narrative Tuning Layer**

   * Customize tone (e.g., confident, humble, assertive) and voice
   * Dynamically rewrite summaries and bullet points via prompt engine
   * Offer presets for tone (e.g., assertive, concise, formal, creative)
   * Allow users to reapply tone preferences dynamically

5. **JD–Resume Traceability**

   * Highlight which resume elements directly respond to job requirements
   * Provide audit view to show rationale for included content

6. **Artifact Versioning and Storage**

   * Store all generated resumes in markdown format
   * Attach metadata (job ID, profile version, prompt ID, tone, timestamp)
   * Allow full history tracking, comparisons, and rollback
   * Link resume to job and profile version for traceability

7. **Export Engine Integration**

   * Convert markdown to PDF, DOCX, and HTML
   * Use pre-defined templates to preserve visual fidelity in exports

**Success Metrics:**

* % of users who generate and export resumes from the platform
* Average time to create a resume from job log
* User satisfaction with resume customization options
* Resume reuse rate for similar roles
* Fit score correlation with interview callback rate (if feedback loop exists)
* Number of resume versions generated per job
* Successful exports and format preference breakdown
* Reduction in support requests tied to layout or tone errors

**Dependencies:**

* Fit score engine with skill mapping
* Profile versioning system
* JD parsing and highlighting module
* JD–Resume traceability and mapping engine
* AI summarization and text-generation engine with tone control
* Resume template renderer
* Markdown export engine with layout styling
* Storage module for resume versions
* Prompt management and tone control system
* Job log integration for resume traceability

**Acceptance Criteria:**

* System recommends resume layout type based on job and user profile
* Users can customize content and order of resume sections
* Resume text reflects accurate and verified profile data
* Generated content uses job-aligned terminology
* Multiple resumes can be saved and retrieved per job
* Resume builder supports different export formats
* Resume components are traceable back to profile and JD context
* Exported filenames are structured with: `[FullName]_[JobTitle]_[Company]_[YYYYMMDD-HHMM]`
* Users can reapply narrative tuning when modifying job target or style preferences
* All resumes are stored in markdown with exportable formats
* Resume artifacts support versioning and history review
* Export fidelity is maintained for structured layouts (e.g., PDF templates)
* Resume and job metadata are linked to generated output
* Prompts and tone configurations used are traceable per resume version

**Priority:** High

**Tags:** resume-generation, profile-integration, jd-alignment, content-strategy, customization, AI-assisted-writing, export-support, version-traceability, markdown-storage, pdf-export, docx-export, artifact-traceability, narrative-layer
