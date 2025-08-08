**Epic Title:** Job Discovery and Logging for Profile Matching

**Epic Owner:** Product Owner (PO)

**Goal:** Enable users to discover job opportunities across platforms, log relevant job data into the system, and structure job listings in a way that supports future fit scoring and resume tailoring.

**Background:**
This epic supports the core function of users identifying target roles and recording them within the platform. Jobs may originate from external job boards or corporate hiring sites. Users will engage with a guided browser experience to aid in collecting comprehensive and accurate job details, even when those jobs redirect through multiple layers (e.g., from LinkedIn to a company's internal portal).

**Key Features:**

1. **Job Board Navigation Framework**:

   * Maintain and display a curated list of supported job boards (e.g., LinkedIn, Seek, Indeed, company portals)
   * For each job board, capture metadata including:

     * Job board type (e.g., general aggregator, recruiter site, corporate career page)
     * Associated company (if applicable) and their industry classification
     * Known hierarchy if company operates as a parent with subsidiaries
     * Primary job board domain and known redirection behavior
     * Inferred dominant functional area(s) based on historical job postings (e.g., technical, finance, healthcare)
     * Source validation confidence score indicating data reliability per board
   * Launch embedded or parallel browser session using automated browser control (e.g., Playwright)
   * Track user's path from initial board through any redirection to final job application page
   * Provide user assistance metadata such as recruiter identification, regional specialization, board industry trends

2. **Job Data Extraction and Logging**:

   * Use browser automation and/or user-initiated logging to extract:

     * Job title
     * Company name
     * Full job description
     * Primary job board and final source of application
     * Job URL(s), captured from all navigation stages
     * Job location(s) and estimated commute time from user's location by preferred method (car, public transport, etc.)
     * Job unit count or number of positions advertised (e.g., 2 roles across different locations)
     * Job age estimation and repost detection (to identify recurring roles)
     * Recruiter or poster identity where available (name, company, LinkedIn profile)
     * Recruiter linkage should include timestamped records of employer history (e.g., Hayes 2023–2024, LinkedIn 2025–)
   * If job already exists in the system (deduplication logic), link user to existing record
   * Deduplication weighting includes title, company (fuzzy match), description, location, URL (with modifiers for dynamic boards)
   * Deduplication algorithm factors in job location and assigns a weighted score to each field
   * If the system identifies significant differences in user-modified metadata that impacts skill inference or fit scoring, create a new version of the job
   * Store the date/time of first appearance and track repost frequency
   * Include recruiter flags and board-level recruiter presence scores
   * Allow detection of multi-location job variants and split for clarity
   * Track if a recruiter is linked to multiple companies over time and when those links were active
   * Maintain a deduplication exception model for dynamic URL job boards

3. **Job Repository and User Association**:

   * Maintain a global job record repository keyed by unique job signatures (hash of title, company, description, URL, location)
   * Store all job versions if differences warrant (content-driven or structure-driven)
   * Job associations (viewed, logged, applied) are per-user records
   * Provide each user with the ability to maintain personalized metadata or view shared/public metadata
   * Maintain job closure detection engine
   * Notify users associated with job when status changes (e.g., closed, expired, reposted)

4. **Profile Linkage and Fit Scoring Flow**:

   * Automatically run fit scoring engine after job log completes
   * Extract and order job-required skills using AI/NLP
   * Rank skills by relevance: required, preferred, optional
   * Assign fit weights and allow user to explore gaps
   * Display source of skill match/mismatch via linked job text
   * Prompt profile enhancement for unmatched skills
   * Track changes and update fit scores post-profile revision
   * Record which profile version was used for the scoring
   * Use recruiter association and company context in skill evaluation weighting

5. **Path Traceability and Audit Trail**:

   * Capture navigation chain and redirection flow
   * Maintain browser session metadata
   * Display origin-to-destination journey per job

6. **User Experience and Automation Aid**:

   * Use AI prompts to clarify ambiguous or missing data (e.g., inferred salary, ambiguous company)
   * Provide watchlist/bookmark feature
   * Allow users to flag inaccurate metadata
   * Maintain user-submitted suggestions for metadata enhancements
   * Use recruiter–company change detection to prompt updates

7. **System-wide Job Matching Integrity**:

   * Track versions of job listings per user input
   * Distinguish cosmetic vs. structural changes
   * Store recruiter-association metadata and provide clarity per listing
   * Associate recruiters with their organization or platform where applicable
   * Capture recruiter contact metadata where possible (e.g., LinkedIn profile)
   * Timestamp recruiter–company relationships for historical accuracy (e.g., Hayes: Jan 2023–Apr 2024, LinkedIn: May 2024–present)
   * Track recruiter transitions across employers without overwriting history
   * Jobs with split locations are logged independently with shared parent record
   * Metadata suggestion submissions are tracked and reviewable

8. **Gamification Integration**:

   * Allocate points for full and partial job logs
   * Reward actions such as confirming metadata, disambiguating recruiter info, classifying industry fit
   * Encourage complete and high-quality job entries
   * Track job contributions as a shareable user achievement
   * Support metadata gamification (e.g., tagging job boards, resolving flags)

**Success Metrics:**

* Volume of unique jobs logged vs. duplicates detected
* Percentage of jobs with complete metadata after logging
* Time taken to log a job end-to-end
* Number of users reusing existing job entries
* Number of job versions created and reused
* User satisfaction with the logging and traceability process
* Gamification participation rate for job logging
* Completeness and accuracy of job board metadata
* Percentage of fit scores automatically triggered from new job logs
* Percentage of users updating profile based on skill mismatch
* Accuracy of deduplication logic based on weighted fields
* Percentage of jobs flagged for multi-location or multi-position splits
* Accuracy of job age detection and repost recognition
* Number of job closures detected and users notified
* Accuracy of recruiter vs. direct employer detection
* % of job logs flagged for metadata inaccuracy
* Bookmark/watchlist usage rate
* Number of job metadata suggestions submitted and accepted
* Recruiter company history data completeness
* Recruiter employer transitions confirmed via verification mechanism
* Accuracy of recruiter–company affiliation timestamps

**Dependencies:**

* Browser control layer (Playwright or alternative)
* Schema for global Job, JobVersion, JobBoard, Recruiter, RecruiterCompanyHistory, and user-specific JobLog tables
* AI prompt system for metadata completion
* Profile module integration for downstream scoring
* Fit Score engine and delta comparison logic
* Gamification engine and point tracking logic
* Location estimation service (e.g., commute time by car or public transport)
* Job age inference module
* Job closure detection and notification engine
* Recruiter detection heuristics or model
* Recruiter profile linking engine (e.g., LinkedIn parser)
* Metadata flagging and review queue
* Bookmark/watchlist data model
* Metadata improvement suggestion interface
* Recruiter employer change detector and confirmation engine

**Acceptance Criteria:**

* Users can log jobs from major boards with full traceability
* System deduplicates job records by weighted signature match
* Deduplication logic accounts for location and recruiter-level variation
* Users can edit and confirm job data
* System maintains a global job pool with version tracking
* Users are linked to job entries and version references
* After logging a job, system automatically calculates a Fit Score
* Users see matched and unmatched skills in a breakdown view
* System prompts profile updates for unmatched skills
* Updated profile triggers recalculation of the Fit Score
* Users receive points based on job logging completeness
* Downstream fit scoring and resume tailoring use structured job data from correct versions
* Job boards have accurate classification metadata and are maintained centrally
* Users receive job commute time estimates based on preferred travel mode
* Job age is estimated and displayed as part of job metadata
* Job closure detection notifies affected users automatically
* Users can bookmark jobs or flag job metadata for review
* Recruiter vs. direct company classification is stored per job
* Recruiter entities are associated with companies and optionally enriched with LinkedIn profile metadata
* Recruiter–company relationships are timestamped to reflect employment history
* Jobs with split locations are logged independently with shared parent record
* Metadata suggestion submissions are tracked and reviewable
* Recruiter–company transitions are prompted and recorded based on job logs
* Recruiter–company affiliations are confirmed or flagged via verification prompts

**Priority:** High

**Tags:** job-logging, job-discovery, browser-assist, AI-parsing, fit-score-prep, job-board-navigation, deduplication, traceability, version-control, gamification, profile-integration, location-awareness, job-age-tracking, job-status-tracking, recruiter-detection, recruiter-linkage, recruiter-history, recruiter-timestamping, recruiter-transition-detection, job-metadata-flagging, watchlist, metadata-suggestions
