**Epic Title:** Fit Score Analysis and Skill Gap Resolution

**Epic Owner:** Product Owner (PO)

**Goal:** Empower users to evaluate their job fit using structured skill comparison and resolve gaps by refining profiles or planning upskilling strategies. A hybrid scoring model is planned, beginning with transparent rule-based logic and expanding into AI-augmented insights for deeper guidance.

**Background:**
Building on structured career profiles and logged job data, this epic focuses on interpreting fit scores generated for job roles, surfacing skill mismatches, and providing resolution paths. The initial scoring will use structured database-level logic to compare required job skills against user profiles, factoring in experience duration and skill criticality. This enables transparent, traceable results. AI will later be used to enhance gap insights and summarize fit explanations, possibly refining final scores or generating personalized advice.

**Key Features:**

1. **Fit Score Decomposition Engine**

   * Use rule-based scoring logic to compare job vs. profile skills
   * Breakdown score into matched, partial, and missing skills
   * Use visual cues (✓, ⚠️, ✕) and attribute source context
   * Tag skills as hard/soft, critical/optional, and score accordingly

2. **Gap Resolution Flow**

   * Prompt user to confirm, edit, or add missing profile elements
   * Provide AI-generated suggestions for where missing skills might exist based on profile
   * Offer career advice (e.g., "Consider gaining experience with X")

3. **Versioned Profile Update Tracking**

   * Profile changes from gap resolution create new version
   * Fit Score deltas are recorded with before/after comparisons

4. **Skill Learning Roadmap Generator**

   * Suggest online courses, certifications, or projects to fill gaps
   * Option to add these as career goals or pending profile items

5. **Gamified Fit Improvement Loop**

   * Award points for addressing skill gaps or confirming AI suggestions
   * Enable users to see "fit score improvement over time"

6. **Role Alignment Tracker**

   * Detect consistent gaps across multiple jobs targeting same role
   * Flag trends and suggest focus areas

7. **Fit Score Replay History**

   * Timeline view of fit scores by job and profile version
   * Click-to-compare previous versions and decisions

**Success Metrics:**

* Percentage of users resolving skill gaps after first Fit Score
* Number of profile versions triggered by gap resolution
* Frequency of AI-suggested skill confirmations
* Usage rate of suggested learning paths
* Fit Score improvement over time per user
* User satisfaction with the gap resolution experience
* Number of recurring role gaps identified and resolved
* Participation in gamified skill confirmation loop

**Dependencies:**

* Profile module with versioning logic
* Skill inference and validation engine
* Rule-based scoring engine (DB-level)
* AI prompt layer for enhanced gap guidance
* Fit Score delta and comparison logic
* Learning resource suggestion service
* Gamification engine and event tracker
* UI module for historical views and delta playback

**Acceptance Criteria:**

* Users see broken down fit score with clear matching logic
* Skill gaps prompt actionable user decisions
* Profile updates trigger version creation and audit log
* Suggested learning items are relevant and accepted by users
* Fit scores recompute on profile change
* Users can view and compare fit score history
* Gamification points allocated per resolution step
* Role gap detection functions across job logs
* Fit score UI supports interactive breakdown and feedback

**Priority:** High

**Tags:** fit-score, gap-resolution, skill-inference, profile-versioning, gamification, delta-analysis, learning-path, job-matching, ai-guidance, traceability
