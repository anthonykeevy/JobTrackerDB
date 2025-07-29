**Epic Title:** Job Search Artifacts & Communication Assistant

**Epic Owner:** Product Owner (PO)

**Goal:** Provide job seekers with high-quality, personalized cover letters and recruiter outreach messages while maintaining traceability, feedback loops, and export fidelity.

**Background:**
Cover letters and direct recruiter communication often enhance application outcomes. However, crafting these artifacts can be daunting for users. This epic delivers AI-generated, editable communication tools that align with the tone, job requirements, and user profiles. Artifacts are stored in markdown to facilitate version control, traceability, and efficient export into professional formats.

**Design Considerations:**

* Cover letters and recruiter messages generated via prompt-to-markdown pipeline
* Markdown storage allows editing, versioning, and lightweight storage
* Export engine supports PDF, DOCX, and HTML formats
* All messages linked to profile version, job log, and recruiter contact metadata
* Filename convention ensures clarity: `[FullName]_[JobTitle]_[ArtifactType]_[Company]_[YYYYMMDD-HHMM]`
* Feedback captured per message instance for prompt tuning

**Key Capabilities:**

1. **Cover Letter Generator**

   * Generate cover letters based on selected job log and profile version
   * Customize tone and structure
   * Store in markdown, export to PDF, DOCX, HTML

2. **Recruiter Outreach Composer**

   * Compose message drafts for email or platform-based recruiter contact
   * Auto-fill contact info, tone, and job metadata
   * Export and store each version

3. **Interview Follow-up & Thank You Notes**

   * Provide customizable templates post-interview
   * Enable prompt-driven tone adjustments

4. **Versioning & Metadata Logging**

   * Capture version history of each message artifact
   * Link messages to job logs and profile versions
   * Maintain promptID and AI model usage per output

5. **Export Management**

   * Unified markdown export pipeline for all artifacts
   * Support download previews, storage, and email-ready formats

**Success Metrics:**

* Number of generated messages per job log
* Export/download rates by format
* User satisfaction feedback scores on generated content
* Message reuse across multiple applications
* Prompt performance improvements based on feedback

**Dependencies:**

* JD parser and profile versioning
* Prompt management console
* Markdown renderer and export engine
* AI messaging prompt set
* Job log and recruiter metadata capture

**Acceptance Criteria:**

* Users can generate, preview, and export cover letters and messages
* Artifacts are stored in markdown with full version traceability
* Each output is linked to the relevant job and profile version
* Prompts and satisfaction scores are logged per artifact
* Export fidelity matches user-selected format expectations

**Priority:** High

**Tags:** cover-letter, recruiter-message, job-artifacts, markdown-storage, export-fidelity, prompt-traceability, versioning, communication-assistant
