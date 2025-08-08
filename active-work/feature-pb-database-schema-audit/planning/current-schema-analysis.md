# Current Database Schema Analysis

## Schema Overview
The current database has a comprehensive schema with 31+ tables designed for a job tracking application. The schema includes profile management, job applications, authentication, and various supporting tables.

## Current Tables Analysis

### **Core Profile Tables**
1. **Profile** - Main user profile with basic information
   - ✅ Has audit fields: `createdDate`, `createdBy`, `lastUpdated`, `updatedBy`
   - ✅ Includes address fields: `AddressLine1`, `AddressLine2`, `AddressLine3`
   - ✅ Has contact info: `PhoneNumber`, `EmailAddress`
   - ✅ Social profiles: `LinkedInURL`, `GitHubURL`, `OtherSocialProfiles`

2. **User** - Authentication and user management
   - ✅ Has audit fields: `createdDate`, `createdBy`, `lastUpdated`, `updatedBy`
   - ✅ Links to Profile via `ProfileID`
   - ✅ Includes OAuth support: `Provider`, `ProviderUserID`

### **Profile Content Tables**
3. **Resume** - User resumes
   - ✅ Has audit fields
   - ✅ Links to Profile via `ProfileID`

4. **CoverLetter** - User cover letters
   - ✅ Has audit fields
   - ✅ Links to Profile via `ProfileID`

5. **Skills** - User skills with proficiency
   - ✅ Has audit fields
   - ✅ Links to Profile via `ProfileID`

6. **Languages** - User language proficiencies
   - ✅ Has audit fields
   - ✅ Links to Profile via `ProfileID`

7. **Hobbies** - User hobbies/interests
   - ✅ Has audit fields
   - ✅ Links to Profile via `ProfileID`

8. **Objective** - User career objectives
   - ✅ Has audit fields
   - ✅ Links to Profile via `ProfileID`

### **Job Application Tables**
9. **JobApplication** - Job applications
   - ✅ Has audit fields
   - ✅ Links to Profile via `ProfileID`

10. **JobApplicationAttachment** - Files attached to applications
    - ✅ Has audit fields: `uploadedDate`, `uploadedBy`
    - ✅ Links to JobApplication via `JobApplicationID`

11. **JobApplicationInterview** - Interview tracking
    - ✅ Has audit fields
    - ✅ Links to JobApplication via `JobApplicationID`

12. **JobApplicationNote** - Notes on applications
    - ✅ Has audit fields
    - ✅ Links to JobApplication via `JobApplicationID`

13. **JobApplicationStatusHistory** - Status change tracking
    - ✅ Has audit fields: `StatusDate`, `updatedBy`
    - ✅ Links to JobApplication via `JobApplicationID`

14. **JobApplicationTask** - Tasks related to applications
    - ✅ Has audit fields
    - ✅ Links to JobApplication via `JobApplicationID`

### **System Tables**
15. **Role** - User roles and permissions
    - ✅ Has audit fields

16. **UserPreferences** - User privacy preferences
    - ✅ Has audit fields
    - ✅ Links to Profile via `ProfileID`

17. **AuthLog** - Authentication logging
    - ✅ Tracks login attempts and success/failure
    - ✅ Includes IP address and error messages

18. **UserPasswordResetToken** - Password reset functionality
    - ✅ Has audit fields: `CreatedDate`, `CreatedBy`

19. **UserRoleOverride** - Individual user permission overrides
    - ✅ Has audit fields

20. **Message** - User messages
    - ✅ Has audit fields
    - ✅ Links to Profile and optionally JobApplication

## Critical Gaps Identified

### **1. Missing Profile Builder Step Data**
The current schema doesn't have dedicated tables for:
- **Education/Certifications** - No tables for education history
- **Work Experience** - No tables for work history
- **Projects** - No tables for portfolio projects
- **Career Aspirations** - No tables for career goals/preferences

### **2. Address Validation Data**
- **ProfileAddress** table is missing
- **Geolocation data** (latitude/longitude) not stored
- **Address validation results** not tracked

### **3. Resume Parsing Data**
- **Parsed resume data** not stored separately
- **AI parsing results** not tracked
- **Resume version history** not maintained

### **4. Audit Trail Improvements Needed**
While most tables have basic audit fields, we need:
- **Dedicated audit trail tables** for detailed change tracking
- **Before/after value storage** for complete audit history
- **Change reason tracking** (why changes were made)
- **Bulk operation tracking** for multiple record changes

### **5. Profile Builder Workflow Data**
- **Step completion tracking** not implemented
- **Form validation errors** not logged
- **User progress through builder** not tracked
- **Draft vs final data** not distinguished

## Data Persistence Requirements by Profile Builder Step

### **Step 1: WelcomeStep**
- **Data**: Mode selection (Guided vs Independent)
- **Current Gap**: No table for user preferences/workflow mode
- **Solution Needed**: Add to UserPreferences or create new table

### **Step 2: ResumeUploadStep**
- **Data**: Uploaded file, parsing results, extracted data
- **Current Gap**: No tables for parsed resume data
- **Solution Needed**: Create ResumeParsingData table

### **Step 3: BasicInfoStep**
- **Data**: Personal info, address with validation
- **Current Gap**: Address validation data not stored
- **Solution Needed**: Create ProfileAddress table with geolocation

### **Step 4: CareerAspirationStep**
- **Data**: Career goals, preferences, salary expectations
- **Current Gap**: No dedicated table for career aspirations
- **Solution Needed**: Create CareerAspiration table

### **Step 5: EducationStep**
- **Data**: Education history, certifications
- **Current Gap**: No education tables
- **Solution Needed**: Create Education and Certification tables

### **Step 6: WorkExperienceStep**
- **Data**: Work history, achievements, responsibilities
- **Current Gap**: No work experience tables
- **Solution Needed**: Create WorkExperience table

### **Step 7: SkillsStep**
- **Data**: Skills by category with proficiency levels
- **Current Gap**: Skills table exists but may need enhancement
- **Solution Needed**: Review and enhance Skills table

### **Step 8: ProjectsStep**
- **Data**: Portfolio projects with technology tags
- **Current Gap**: No projects table
- **Solution Needed**: Create Project table

### **Step 9: ReviewStep**
- **Data**: Complete profile summary
- **Current Gap**: No profile completion tracking
- **Solution Needed**: Add completion tracking to Profile table

## Audit Trail Requirements

### **Current Audit Fields**
Most tables have:
- `createdDate` - When record was created
- `createdBy` - Who created the record
- `lastUpdated` - When record was last updated
- `updatedBy` - Who last updated the record

### **Enhanced Audit Trail Needed**
1. **Dedicated Audit Tables**
   - Track all changes with before/after values
   - Store change reasons and context
   - Support bulk operation tracking

2. **Change Tracking by Field**
   - Track which specific fields changed
   - Store old and new values
   - Track change timestamps

3. **User Session Tracking**
   - Track user sessions during profile building
   - Log form validation errors
   - Track step completion times

## Performance Considerations

### **Current Schema Strengths**
- ✅ Proper indexing on foreign keys
- ✅ Unique constraints where needed
- ✅ Appropriate data types and lengths

### **Potential Issues**
- ⚠️ Audit trail overhead on high-frequency updates
- ⚠️ Large text fields (UnicodeText) for content
- ⚠️ No partitioning for large tables

## Next Steps

1. **Use @bmad-master to design missing tables**
2. **Design enhanced audit trail system**
3. **Create migration strategy**
4. **Plan data migration for existing data**
5. **Design API endpoints for new tables**

## BMAD Master Integration Points

### **For Schema Design**
```bash
@bmad-master *task brownfield-create-epic
# Input: Current schema + missing tables requirements
# Output: Complete schema with audit trails
```

### **For Audit Trail Design**
```bash
@bmad-master *kb
# Query: Database audit trail best practices
# Query: Performance optimization for audit trails
```

### **For Migration Strategy**
```bash
@bmad-master *create-doc brownfield-architecture-tmpl
# Document: Schema evolution and migration strategy
```
