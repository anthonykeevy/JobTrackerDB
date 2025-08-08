# User Story CI.1: Database Schema Design

**Epic:** Core Infrastructure & Database  
**Story ID:** CI.1  
**Priority:** High  
**Status:** Draft  
**Owner:** Product Owner (PO)

---

## Description

As a **developer**,  
I want to **design a comprehensive database schema that supports all platform features**,  
So that **the system can efficiently store, retrieve, and manage all user data and platform functionality**.

---

## Acceptance Criteria

1. User management tables:
   - User table with authentication data
   - UserProfile table for extended profile information
   - UserSession table for session management
   - UserSettings table for user preferences
   - UserNotification table for notification preferences

2. Profile and skill management tables:
   - Profile table with basic profile information
   - ProfileVersion table for version tracking
   - ProfileSkill table linking profiles to skills
   - Skill table with skill definitions and metadata
   - SkillCategory table for skill organization
   - ProfileEducation table for education history
   - ProfileExperience table for work experience
   - ProfileProject table for project portfolio

3. Job logging and application tracking tables:
   - Job table with job posting information
   - JobVersion table for job posting versions
   - JobBoard table for job board metadata
   - Recruiter table for recruiter information
   - RecruiterCompanyHistory table for employment history
   - JobApplication table for user applications
   - JobApplicationStatus table for status tracking
   - JobLocation table for location information

4. Gamification and analytics tables:
   - GamificationPoints table for point tracking
   - Achievement table for achievement definitions
   - UserAchievement table for earned achievements
   - ActivityLog table for user activity tracking
   - FitScore table for job fit scores
   - FitScoreHistory table for score tracking
   - AnalyticsEvent table for analytics data

5. Artifact and content management tables:
   - Artifact table for generated content (markdown storage)
   - ArtifactVersion table for version tracking
   - ArtifactType table for content categorization
   - Template table for export templates
   - TemplateVersion table for template versions
   - ExportLog table for export tracking

6. Audit logging and security tables:
   - AuditLog table for security and activity events
   - SecurityEvent table for security incidents
   - DataAccessLog table for data access tracking
   - Permission table for access permissions
   - Role table for user roles
   - UserRole table for role assignments

7. Database design requirements:
   - Proper primary and foreign key relationships
   - Appropriate indexes for performance
   - Data constraints and validation rules
   - **Naming Conventions**:
     * Database name: `JobTrackerDB`
     * Schema: `dbo` (default)
     * Table names: Singular (e.g., `Profile`, `User`, `Job`)
     * Related tables: Hierarchical naming (e.g., `ProfileSkill`, `JobApplication`, `UserRole`)
     * Primary keys: Auto-incrementing `[TableName]ID` (e.g., `ProfileID`, `UserID`)
     * Views: `v_` prefix (e.g., `v_ProfileSummary`, `v_UserAnalytics`)
     * Stored procedures: `s_` prefix (e.g., `s_GetUserDetails`, `s_CalculateFitScore`)
     * Text fields: `nvarchar` for Unicode support
   - Timestamp fields for audit trails
   - Soft delete capabilities where appropriate

---

## Definition of Done

- Complete database schema is designed and documented
- All tables support required platform features
- Relationships and constraints are properly defined
- Indexing strategy is optimized for performance
- Schema follows established naming conventions
- Data integrity and validation rules are implemented
- Schema supports scalability and future enhancements

---

## Dependencies

- Requirements from all other epics
- Database design tools and documentation
- Performance and scalability requirements
- Security and compliance requirements 