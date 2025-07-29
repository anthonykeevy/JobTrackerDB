**Epic Title:** Unified Career Profile Intake for Resume Generation

**Epic Owner:** Product Owner (PO)

**Goal:** Design and implement a seamless, guided experience to collect comprehensive career history from users across all industries and career stages. This information will be structured into a professional profile used to generate tailored resumes aligned to specific job roles.

**Background:**
This is a critical onboarding component for new users. The career intake process must accommodate:

* Early-career individuals with limited work history
* Mid-career professionals with mixed experiences
* Senior executives with complex portfolios
* Users from a broad range of industries and job types

A unified model will be used to build flexible yet structured profiles, ensuring resume outputs meet diverse role requirements. The intake process should resemble an AI-driven interview, engaging users through a conversational format.

**Key Features:**

1. **Career Aspiration Guidance Module**:

   * Support users in defining the type of job or role they are best suited for next
   * Use AI-driven questioning to help experienced users reflect on past roles and select a target direction
   * Allow users to specify a short-term "next role" and a 5-year aspirational role
   * Provide AI-driven guidance on how the selected next role aligns with long-term aspirations
   * Capture career aspirations as a foundation for resume generation and future fit scoring
2. **Role Targeting Module**:

   * Allow user to select or specify the job role they want to apply for (based on aspirations or direct input)
   * Provide an option to derive the role from the career aspiration statement
   * Track which role was active during resume or fit score generation
3. **Career History Intake**:

   * Education
   * Work Experience (title, org, dates, achievements)
   * Certifications & Training
   * Skills (hard and soft)
   * Projects & Portfolio
   * Volunteer & Extracurriculars
   * Additional Industry-Specific Information (user-provided, reviewed weekly for schema evolution)
   * Indicate for each Work Experience entry whether the data provided is a responsibility or an achievement
4. **AI-Driven Interview Assistant**:

   * Request latest resume for parsing and prepopulation of profile
   * Engage users with memory-stimulating prompts and clarifying questions
   * Convert freeform answers into structured profile data
   * Assist user in verifying and refining auto-parsed information
5. **Skill Inference Engine**:

   * Infer skills based on relationships across education, work experience, training, projects, and volunteer work
   * Estimate exposure duration and competency level for each skill
   * Support user confirmation or correction of inferred skills
   * Prevent unsupported skill additions by ensuring source traceability
   * Map profile skills against job description requirements to determine skill fit
6. **Progressive Disclosure UI**: Show fields based on career stage and selected role complexity.
7. **Industry Agnostic Fields**: Design form logic and field types to support all verticals. Capture unmatched inputs in a generic 'Additional Info' category for later schema review and potential field inclusion.
8. **Optional AI Guidance**: Offer assistance (e.g., examples, auto-fill prompts, clarification helpers).
9. **Review and Confirm View**:

   * Display full structured profile for final review
   * Allow user to edit sections or return for revisions
   * Highlight incomplete fields or data conflicts
   * Show summary of changes since last confirmation
   * Capture a happiness score with this version of the profile
   * Compare with happiness score and content of previously accepted profile milestone
   * Indicate if new content has been added since last acceptance
   * Require user approval to use updated profile in downstream features such as fit scoring and artifact generation (defined in future epics)
10. **Profile Storage and Editing**:

* Persist user profile and allow for updates/resume reuse
* Track historical milestones and store a version reference
* When a resume, fit score, or other artifact is generated, capture which profile version was used
* Notify user if artifact or fit score was generated from outdated profile version
* Only use profile data from the confirmed version during fit score evaluation and artifact generation. If updates are added, notify user to reconfirm for new outputs.

**Note:** A separate epic will define the "Find Jobs and Fit Scoring" system, which includes searching and logging jobs, calculating fit scores against the profile, and updating the profile based on job-specific gaps.

**Success Metrics:**

* Completion rate of onboarding flow
* Average time to complete intake
* Accuracy and satisfaction ratings from resume output
* Return users editing/updating profile
* Precision of skill-to-role matching

**Dependencies:**

* Resume generation engine
* Authentication and user data storage
* UX design for multi-path form flows
* AI guidance and interview agent module
* Skill inference and job role comparison service

**Acceptance Criteria:**

* Flow supports users with 0-40+ years of experience
* Profiles generate valid inputs for resume engine
* Users can define their career aspirations or directly select a role
* Clear support for different levels of detail (e.g., internships vs executive summaries)
* Works responsively across devices
* Can prepopulate profile from uploaded resume
* Conversational prompts help users recall career experiences
* AI parsing includes validation and correction layer to address misinterpretations
* Inferred skills include estimated duration and competency level
* Skills mapped and scored against job descriptions
* Skill entries must have source traceability to discourage unsupported claims
* User must approve profile for final use if changes have occurred since last confirmation
* System displays profile change summary and previous version comparison before applying updates downstream
* All artifacts and fit scores generated are tagged with the profile version used
* Newly added profile data must be reconfirmed to generate updated outputs

**Priority:** High

**Tags:** onboarding, profile, resume, UX, AI-assist, universal-design, conversational-UI, skill-inference, job-fit, career-aspiration, profile-approval, version-tracking
