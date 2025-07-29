# AI-Powered Resume and Job Tracker Platform: Architecture Vision

## 1. Introduction

This Architecture Vision document outlines the strategic direction for an AI-Powered Resume and Job Tracker Platform, designed to streamline job application processes for job seekers, enhance recruitment efficiency for employers, and provide operational value to organizations by tracking employee skills and contributions. The platform leverages artificial intelligence to offer personalized resume optimization, job matching, application tracking, and internal talent discovery, with gamification integrated into both frontend and backend systems. This document aligns with TOGAF’s Architecture Development Method (ADM) Phase A to establish a clear vision for stakeholders and guide subsequent architecture development.

## 2. Scope

### Audiences:

* **Job Seekers**: Individuals from entry-level to executive roles
* **Employers/Recruiters**: Organizations seeking efficient candidate sourcing
* **Companies (Operational Use)**: Teams aiming for better internal staffing via up-to-date employee profiles

### Geographic Scope:

* Initially Australia; global expansion post-MVP

### Functional Scope:

* Profile creation via guided AI-driven intake
* Resume creation and AI-driven optimization
* Career aspiration capture and role targeting
* Skill inference based on profile components
* Job matching and application tracking (epic defined separately)
* API key management and cost tracking for AI services (epic defined separately)
* Billing and payment system with Stripe integration (epic defined separately)
* Fit scoring using confirmed profiles
* Artifact generation (resumes, cover letters, tailored summaries)
* Profile versioning with milestone history and user approval gating
* Gamification features, user feedback loops (happiness scoring)
* Schema evolution for industry-specific inputs
* Resume generation and fit scoring tied to specific profile versions
* **Job Discovery and Logging**:

  * Job board metadata capture (source, industry focus, ownership type)
  * Job role logging with company, recruiter, location, and URL history
  * Fit score triggers and profile update prompts
  * Recruiter linkage and employment timeline tracking
  * Gamification for job logging completeness
  * Job deduplication using multi-factor logic (title, company, description, URL, location)
  * Versioning for job postings and recruiter transitions
  * Watchlist, bookmarking, and closure notifications
  * Periodic user-prompted validation workflows

### Exclusions:

* No direct job placement services or staffing agency functions

## 3. Stakeholders and Concerns

* **Job Seekers**: Strong, competitive resumes; clear guidance; gamified engagement
* **Employers**: AI-powered job fit insights and post-MVP candidate screening
* **Companies**: Employee skill inventories and career mapping (post-MVP)
* **You (Developer)**: Clear development phases, manageable scope, modular architecture
* **Investors**: Market fit, monetization path, user satisfaction feedback

## 4. Business Goals and Drivers

* **Enhance User Experience**: Intuitive, AI-assisted onboarding and artifact generation
* **Improve Hiring Efficiency**: AI filtering and skill-role fit scoring
* **Market Differentiation**: Deep career profile model with transparency and user validation
* **Scalability and Compliance**: Local-first with global compliance
* **Revenue Generation**: Subscription model at \$10/month, 1000 subscribers target by month 3
* **Data Depth**: Longitudinal recruiter/job role history enhances analytics
* **User-Driven Quality**: Gamified accuracy and contribution loops for job metadata integrity

### Business Drivers:

* High demand for AI-driven personalization
* Resume fatigue and generic submissions
* Need for accurate internal talent visibility
* Marketplace reliance on reliable job metadata

## 5. Architecture Principles

* **User-Centric Design**: Progressive disclosure UI, responsive design
* **Hybrid Monolith-Microservices**: Monolith core with microservices (MCP, AI)
* **MCP API Layer**: Modular backend contract with strict permission and logging boundaries
* **AI Ethics**: All artifacts are user-reviewed before use; approval gating enforced
* **Data Security**: Australia-aligned compliance and encryption, secure API key management with Azure Key Vault integration, PCI-compliant payment processing
* **Gamification**: Milestone tracking and profile completeness scores; job logging rewards
* **Evolutionary Schema**: Additional user data routed to dynamic `Additional Info` capture with weekly schema review
* **Versioning & Traceability**:

  * Profile versioning tied to every generated artifact
  * Edit tracking and rollback support
  * Job versioning based on recruiter or metadata changes
  * Recruiter employment history tracked with company
* **Happiness Feedback**: Profiles rated by user at each milestone for quality feedback

### Naming Convention:

Maintain strict naming and typing across `JobTrackerDB` using:

* Singular table names (e.g., `Profile`, `User`)
* `ID` as suffix for PKs (`ProfileID`, `JobApplicationID`)
* `v_` for views (e.g., `v_ProfileSummary`)
* `s_` for stored procedures (e.g., `s_GetProfileHistory`)
* `nvarchar` for all text fields

## 6. Vision Statement

This platform revolutionizes career progression and job application processes using AI. It empowers users with an adaptive profile intake flow, real-time guidance, personalized artifacts, and milestone tracking. It also creates a centralized, accurate repository of job role data with recruiter and job board context. The system is built to scale globally with ethical, transparent AI logic and feedback loops.

## 7. Value Proposition

* **Job Seekers**: Intelligent profile builder, career trajectory insights, role-fit scores, guided resume output, and proactive job logging
* **Employers**: Streamlined access to verified, AI-enhanced candidate profiles (post-MVP)
* **Business**: Subscription-based SaaS with verifiable value delivery, gamified data quality, and job insight metrics

## 8. Constraints and Assumptions

### Constraints:

* Solo developer
* 3-month MVP goal
* Limited MVP hosting budget
* Dependence on third-party APIs (OpenAI, job search)

### Assumptions:

* MVP focuses on local use (Australia)
* Users will provide truthful data
* Resume parsing APIs will cover most resume formats
* Skills must be backed by traceable experience sources
* Jobs will be deduplicated using scoring heuristics, with recruiter metadata saved

## 9. High-Level Architecture Model

* **Frontend**: React SPA, responsive forms, progressive disclosure
* **Backend**: FastAPI (Python), hosted locally for MVP
* **Database**: MSSQL (`JobTrackerDB`)
* **AI Services**: OpenAI integration for NLP and resume generation with secure API key management and cost tracking
* **MCP Layer**: Mediates all DB writes/reads with validation and logging
* **Analytics**: Event triggers for profile changes, fit score requests, job tracking
* **Billing System**: Stripe integration for subscription management and payment processing
* **Gamification Engine**: Points per job added, validated, and verified
* **Backup**: Local first, Azure migration roadmap

### 9.1 Artifact Management and Export Architecture

To support traceable, versioned, and efficient artifact generation (resumes, cover letters, recruiter messages, etc.), the platform adopts the following architecture:

- **Markdown-First Storage Format**:
  - All AI-generated user-facing artifacts are stored as markdown documents
  - Enables lightweight storage, version control, and text-based editing
  - Each artifact includes metadata: JobID, ProfileVersion, PromptID, Timestamp, Tone

- **Unified Export Pipeline**:
  - Markdown content is converted into user-facing formats: PDF, DOCX, and HTML
  - Uses Pandoc or similar rendering engines with predefined templates
  - Resume exports leverage enhanced markdown or styled HTML for layout fidelity

- **Template Engine**:
  - Supports resume layout types (functional, chronological, hybrid)
  - Messaging templates vary tone and structure based on artifact type

- **Traceability and Logging**:
  - All artifacts are linked to the originating profile version and job log
  - Prompt usage, model details, token costs, and satisfaction scores are logged
  - Full rollback and comparison of artifact versions supported

- **Prompt-to-Artifact Mapping**:
  - Each output includes a reference to the prompt used and model invoked
  - Enables post-generation tuning and optimization for tone, clarity, and cost

This architecture ensures alignment between user-facing document quality, AI optimization workflows, and system cost controls. It also supports future enhancements like A/B testing, adaptive prompts, and model benchmarking per artifact type.


## 10. Risks and Mitigation

| Risk                     | Mitigation                                    |
| ------------------------ | --------------------------------------------- |
| Developer fatigue        | Scope guardrails, automation tools            |
| Resume misinterpretation | Resume parsing backed by user confirmation    |
| Job metadata corruption  | Version tracking and audit trail              |
| Recruiter ambiguity      | LinkedIn capture, company mapping with tenure |
| Data privacy gaps        | Encrypt data, follow AU compliance standards  |
| API key security         | Azure Key Vault encryption, role-based access |
| Payment processing       | Stripe integration, PCI compliance, webhook security |
| Over-complex UI          | Progressive UI and staged form flow           |
| AI bias                  | AI suggestions always user-editable           |

## 11. Next Steps

* Finalize this PRD and sync all epics and stories under `docs/epics/` and `docs/stories/`
* Build initial schema with version tracking: `Profile`, `ProfileVersion`, `ProfileSkill`, `Job`, `JobVersion`, `JobApplication`, `Recruiter`
* Begin development:

  * **Month 1**: Career intake flow, milestone tracking, versioning logic
  * **Month 2**: Fit scoring model, AI-generated resumes, feedback system, job registry
  * **Month 3**: Gamification, dashboards, recruiter timeline capture, local MVP launch
* Weekly review of `Additional Info` fields to identify new schema extensions
